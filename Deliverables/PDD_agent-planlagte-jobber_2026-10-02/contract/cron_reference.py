#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Referanse for cron-reglene i planlagte jobber (haven.scheduled-job.v1).

Dette er en kjørbar spesifikasjon, ikke produktkode. Swift-implementasjonen
(`CronSchedule` i HavenAgentRuntime) skal gi nøyaktig de samme tidspunktene som
`fixtures/cron-forventninger.json`, som er laget med denne fila.

Reglene:

1. Fem felt: minutt (0-59), time (0-23), dag i måneden (1-31), måned (1-12),
   ukedag (0-7, der både 0 og 7 er søndag). Hvert felt er en kommaliste av
   `*`, `*/n`, `a`, `a-b` eller `a-b/n`. Navn (JAN, MON) og makroer (@daily)
   støttes ikke.
2. Dag: er både dag i måneden og ukedag noe annet enn `*`, holder det at én av
   dem stemmer. Er den ene `*`, må den andre stemme.
3. Tidssonen er alltid oppgitt: `UTC` eller et IANA-navn på formen Område/Sted
   (`Europe/Oslo`). Forkortelser og eldre navn uten skråstrek avvises. Uttrykket
   leses i den sonen.
4. Sommertid, to slags uttrykk:
   - *Løpende*: minutt- eller timefeltet har et ledd som er `*` eller `*/n`,
     uansett hvor i kommalista det står. Uttrykket følger klokka slik den
     faktisk går. Når en time kommer to ganger, kjører det i begge.
     Klokkeslett som ikke finnes, kjøres ikke.
   - *Fast klokkeslett*: alle andre, også `0-59` i minuttfeltet. Et
     klokkeslett som finnes to ganger, gir én kjøring (den første). Et
     klokkeslett som ikke finnes, gir én kjøring i det klokka er ferdig med å
     hoppe. Flere slike i samme hopp gir én, også når det samme tidspunktet
     er et vanlig treff.
5. «Etter» er strengt: et tidspunkt lik `after` er ikke med. Tidspunktene er
   alltid hele minutter, og `after` kan ha sekunder.
6. Søket etter neste tidspunkt stopper etter åtte år. Finnes ingen, er
   uttrykket umulig og avvises.

Python 3.9 eller nyere, bare standardbiblioteket.
"""
import json
import sys
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

UTC = timezone.utc
SEARCH_DAYS = 8 * 366
FIELD_BOUNDS = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 7))
FIELD_NAMES = ("minutt", "time", "dag i måneden", "måned", "ukedag")


class CronError(ValueError):
    """Uttrykket eller tidssonen kan ikke brukes."""


def _parse_number(text, name):
    # Bare sifrene 0-9, og høyst ni av dem, så regelen er lik i Swift.
    if not (text.isascii() and text.isdigit()) or len(text) > 9:
        raise CronError(f"{name}: «{text}» er ikke et tall")
    return int(text)


def parse_field(text, bounds, name):
    lo, hi = bounds
    if text == "":
        raise CronError(f"{name}: tomt felt")
    values = set()
    for item in text.split(","):
        if item == "":
            raise CronError(f"{name}: tomt ledd i «{text}»")
        base, slash, step_text = item.partition("/")
        step = 1
        if slash:
            step = _parse_number(step_text, name)
            if step < 1:
                raise CronError(f"{name}: steget må være minst 1")
        if base == "*":
            first, last = lo, hi
        elif "-" in base:
            a, _, b = base.partition("-")
            first, last = _parse_number(a, name), _parse_number(b, name)
            if first > last:
                raise CronError(f"{name}: området «{base}» går baklengs")
        else:
            if slash:
                raise CronError(f"{name}: steg krever `*` eller et område, ikke «{item}»")
            first = last = _parse_number(base, name)
        if first < lo or last > hi:
            raise CronError(f"{name}: «{item}» er utenfor {lo}-{hi}")
        values.update(range(first, last + 1, step))
    return values


class Cron:
    def __init__(self, expression, time_zone):
        if not isinstance(expression, str) or not isinstance(time_zone, str):
            raise CronError("uttrykk og tidssone må være tekst")
        fields = expression.split()
        if len(fields) != 5:
            raise CronError(f"uttrykket må ha fem felt, ikke {len(fields)}")
        # Sonen er `UTC` eller et IANA-navn på formen Område/Sted. Forkortelser («CET», «PST») og
        # eldre navn uten skråstrek avvises, så regelen er den samme på alle plattformer.
        if time_zone != "UTC" and "/" not in time_zone:
            raise CronError(f"tidssonen må være UTC eller et navn på formen Område/Sted, ikke «{time_zone}»")
        try:
            self.tz = ZoneInfo(time_zone)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise CronError(f"ukjent tidssone «{time_zone}»") from error
        parsed = [parse_field(f, b, n) for f, b, n in zip(fields, FIELD_BOUNDS, FIELD_NAMES)]
        self.minutes, self.hours, self.doms, self.months, dows = parsed
        self.dows = {0 if d == 7 else d for d in dows}
        self.dom_any = fields[2] == "*"
        self.dow_any = fields[4] == "*"
        self.running = any(item.startswith("*") for field in fields[:2] for item in field.split(","))
        self.expression = " ".join(fields)
        self.time_zone = time_zone

    def day_matches(self, day):
        if day.month not in self.months:
            return False
        dom_ok = day.day in self.doms
        dow_ok = (day.isoweekday() % 7) in self.dows
        if self.dom_any and self.dow_any:
            return True
        if self.dom_any:
            return dow_ok
        if self.dow_any:
            return dom_ok
        return dom_ok or dow_ok

    # --- ett døgn om gangen -------------------------------------------------

    def _day_bounds(self, day):
        start = self._first_instant_of(day)
        end = self._first_instant_of(day + timedelta(days=1))
        return start, end

    def _first_instant_of(self, day):
        naive = datetime.combine(day, time(0, 0))
        candidates = [naive.replace(tzinfo=self.tz, fold=f).astimezone(UTC) for f in (0, 1)]
        valid = [u for u in candidates if u.astimezone(self.tz).replace(tzinfo=None) == naive]
        if valid:
            return min(valid)
        # Midnatt finnes ikke denne dagen (sonen hopper over den): døgnet begynner etter hoppet.
        return self._transition_between(min(candidates), max(candidates))

    def _transition_between(self, before, after):
        """Første minutt der avstanden til UTC er den samme som ved `after`."""
        target = after.astimezone(self.tz).utcoffset()
        lo, hi = before, after
        while hi - lo > timedelta(minutes=1):
            mid = lo + (hi - lo) // 2
            mid = mid.replace(second=0, microsecond=0)
            if mid <= lo:
                mid = lo + timedelta(minutes=1)
            if mid.astimezone(self.tz).utcoffset() == target:
                hi = mid
            else:
                lo = mid
        return hi

    def _instants_on(self, day):
        if not self.day_matches(day):
            return []
        if self.running:
            start, end = self._day_bounds(day)
            found = []
            instant = start
            while instant < end:
                local = instant.astimezone(self.tz)
                if local.date() == day and local.hour in self.hours and local.minute in self.minutes:
                    found.append(instant)
                instant += timedelta(minutes=1)
            return found
        found = set()
        for hour in sorted(self.hours):
            for minute in sorted(self.minutes):
                naive = datetime.combine(day, time(hour, minute))
                candidates = [naive.replace(tzinfo=self.tz, fold=f).astimezone(UTC) for f in (0, 1)]
                valid = [u for u in candidates if u.astimezone(self.tz).replace(tzinfo=None) == naive]
                if valid:
                    found.add(min(valid))          # finnes én eller to ganger: den første
                else:
                    found.add(self._transition_between(min(candidates), max(candidates)))
        return sorted(found)

    # --- offentlig ----------------------------------------------------------

    def occurrences(self, after, limit=None, until=None):
        """Tidspunkter (UTC) strengt etter `after`, i stigende rekkefølge."""
        if after.tzinfo is None:
            raise CronError("`after` må ha tidssone")
        after = after.astimezone(UTC)
        day = after.astimezone(self.tz).date() - timedelta(days=1)
        last_day = day + timedelta(days=SEARCH_DAYS)
        produced = 0
        while day <= last_day:
            for instant in self._instants_on(day):
                if instant <= after:
                    continue
                if until is not None and instant > until:
                    return
                yield instant
                produced += 1
                if limit is not None and produced >= limit:
                    return
            day += timedelta(days=1)

    def next_after(self, after):
        for instant in self.occurrences(after, limit=1):
            return instant
        raise CronError("uttrykket gir ingen tidspunkt de neste åtte årene")

    def shortest_gap_seconds(self, after, until):
        """Korteste avstand mellom to påfølgende tidspunkt i (after, until].

        Brukes for grensen «ikke oftere enn». En jobb har alltid sluttdato, så
        hele levetiden regnes, verken mer eller mindre. None når det er færre
        enn to tidspunkt.
        """
        previous = None
        shortest = None
        for instant in self.occurrences(after, until=until):
            if previous is not None:
                gap = (instant - previous).total_seconds()
                shortest = gap if shortest is None else min(shortest, gap)
            previous = instant
        return shortest


def iso(instant):
    return instant.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def main(argv):
    if len(argv) >= 4 and argv[1] == "neste":
        cron = Cron(argv[2], argv[3])
        after = parse_iso(argv[4]) if len(argv) > 4 else datetime.now(UTC)
        count = int(argv[5]) if len(argv) > 5 else 5
        for instant in cron.occurrences(after, limit=count):
            print(iso(instant), instant.astimezone(cron.tz).strftime("%a %d.%m.%Y %H:%M %Z"))
        return 0
    if len(argv) == 3 and argv[1] == "kontroller":
        document = json.load(open(argv[2], encoding="utf-8"))
        failures = 0
        for case in document["gyldige"]:
            cron = Cron(case["cron"], case["timeZone"])
            got = [iso(i) for i in cron.occurrences(parse_iso(case["after"]), limit=len(case["expect"]))]
            if got != case["expect"]:
                failures += 1
                print("AVVIK", case["name"], got, case["expect"])
        for case in document["tellinger"]:
            cron = Cron(case["cron"], case["timeZone"])
            got = sum(1 for _ in cron.occurrences(parse_iso(case["after"]), until=parse_iso(case["until"])))
            if got != case["count"]:
                failures += 1
                print("AVVIK", case["name"], got, case["count"])
        for case in document["ugyldige"]:
            try:
                Cron(case["cron"], case["timeZone"]).next_after(parse_iso("2026-10-01T00:00:00Z"))
            except CronError:
                continue
            failures += 1
            print("AVVIK: skulle vært avvist", case["cron"], case["timeZone"])
        for case in document["korteste-avstand"]:
            cron = Cron(case["cron"], case["timeZone"])
            got = cron.shortest_gap_seconds(parse_iso(case["after"]), parse_iso(case["until"]))
            if got != case["seconds"]:
                failures += 1
                print("AVVIK", case["cron"], got, case["seconds"])
        total = sum(len(document[k]) for k in ("gyldige", "tellinger", "ugyldige", "korteste-avstand"))
        print(f"{total - failures} av {total} stemmer")
        return 1 if failures else 0
    print("bruk: cron_reference.py neste '<uttrykk>' <tidssone> [etter-UTC] [antall]\n"
          "      cron_reference.py kontroller fixtures/cron-forventninger.json")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
