"""Book 36 composition validation and evaluation. Standard library only.

Execution evidence is separate from reports (claimed conclusions) and opinions.
No composition is inferred for legacy parents. Input arrays are not child order.
"""
from __future__ import annotations

import datetime as dt

KINDS = {'allOf', 'sequence', 'anyOf', 'firstOf', 'invariant'}
STATES = {'green', 'red', 'blocked', 'unverified'}
LOG_FIELDS = ('attempts', 'measurements', 'reports', 'opinions')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('tidspunkt må være en ISO 8601-streng med tidssone')
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError('ugyldig ISO 8601-tidspunkt: ' + value) from None
    if parsed.tzinfo is None:
        raise ValueError('tidspunkt mangler tidssone: ' + value)
    return parsed


def outcome(state, reason, **extra):
    return dict(state=state, reason=reason, **extra)


class Composition:
    def __init__(self, nodes, execution=None):
        self.nodes = {}
        self.children = {}
        self.errors = []
        self.warnings = []
        self.missing_composition = []
        self.execution = execution if isinstance(execution, dict) else {}
        if execution is not None and not isinstance(execution, dict):
            self.errors.append('execution må være et objekt')
        if not isinstance(nodes, list):
            self.errors.append('nodes må være en liste')
            nodes = []
        for node in nodes:
            ref = node.get('purposeRef') if isinstance(node, dict) else None
            if not isinstance(ref, str) or not ref.startswith('purpose://'):
                self.errors.append('node mangler gyldig purposeRef')
            elif ref in self.nodes:
                self.errors.append(f'{ref}: duplikat purposeRef; rekkefølgen er tvetydig (regel 2)')
            else:
                self.nodes[ref] = node
        for ref, node in self.nodes.items():
            parent = node.get('parentRef')
            if parent is not None and (not isinstance(parent, str) or parent not in self.nodes):
                self.errors.append(f'{ref}: parentRef finnes ikke i treet')
            elif parent is not None:
                self.children.setdefault(parent, []).append(ref)
        self._validate_nodes()
        self._validate_execution()

    def _root(self, ref):
        seen = set()
        while ref in self.nodes:
            if ref in seen:
                return None
            seen.add(ref)
            parent = self.nodes[ref].get('parentRef')
            if parent is None:
                return ref
            if not isinstance(parent, str):
                return None
            ref = parent
        return None

    def _validate_nodes(self):
        for ref, node in self.nodes.items():
            children = self.children.get(ref, [])
            if self._root(ref) is None:
                self.errors.append(f'{ref}: treet har en syklus eller manglende forelder')
            if 'composition' not in node:
                if children:
                    self.missing_composition.append(ref)
                    self.warnings.append(f'{ref}: ikke-løvnode uten composition (regel 1; migrering gjenstår)')
                continue
            comp = node['composition']
            if not isinstance(comp, dict) or not isinstance(comp.get('kind'), str) or comp['kind'] not in KINDS:
                self.errors.append(f'{ref}: ukjent eller ugyldig composition.kind')
                continue
            kind = comp['kind']
            allowed = {'kind'} | ({'min'} if kind == 'anyOf' else {'over'} if kind == 'invariant' else set())
            if set(comp) - allowed:
                self.errors.append(f'{ref}: ukjente felt i composition: {sorted(set(comp) - allowed)}')
            if not children:
                self.errors.append(f'{ref}: composition trenger minst ett barn')
            order = node.get('childOrder')
            if kind in ('sequence', 'firstOf') or order is not None:
                if (not isinstance(order, list) or not all(isinstance(v, str) for v in order)
                        or len(set(order)) != len(order) or set(order) != set(children)):
                    self.errors.append(f'{ref}: childOrder må liste hvert direkte barn nøyaktig én gang (regel 2)')
            if kind == 'anyOf':
                minimum = comp.get('min', 1)
                if type(minimum) is not int or not 1 <= minimum <= len(children):
                    self.errors.append(f'{ref}: anyOf.min må være heltall fra 1 til antall barn (regel 3)')
            if kind == 'invariant':
                target = comp.get('over')
                if (not isinstance(target, str) or target not in self.nodes or target == ref
                        or self._root(target) != self._root(ref) or not self.children.get(target)):
                    self.errors.append(f'{ref}: invariant.over må peke på en annen samling i samme tre (regel 5)')

    def _validate_execution(self):
        if set(self.execution) - set(LOG_FIELDS):
            self.errors.append('execution har ukjente felt; målinger, rapporter og meninger må holdes atskilt')
        fields = {
            'attempts': ({'attemptRef', 'purposeRef', 'attemptedAt'}, {'finishedAt'}),
            'measurements': ({'purposeRef', 'measuredAt', 'state', 'evidenceRef'}, {'reason', 'attemptRef', 'phase'}),
            'reports': ({'purposeRef', 'reportedAt', 'state'}, {'reason', 'branchRef'}),
            'opinions': ({'purposeRef', 'text'}, set()),
        }
        attempts = {}
        for field in LOG_FIELDS:
            entries = self.execution.get(field, [])
            if not isinstance(entries, list):
                self.errors.append(f'execution.{field} må være en liste')
                self.execution[field] = []
                continue
            seen = set()
            for entry in entries:
                required, optional = fields[field]
                if (not isinstance(entry, dict) or required - set(entry)
                        or set(entry) - required - optional):
                    self.errors.append(f'execution.{field}: manglende eller ukjente felt')
                    continue
                ref = entry['purposeRef']
                if not isinstance(ref, str) or ref not in self.nodes:
                    self.errors.append(f'execution.{field}: ukjent purposeRef')
                    continue
                for key in required | optional:
                    if key in entry and (not isinstance(entry[key], str) or not entry[key].strip()):
                        self.errors.append(f'{ref}/{field}: {key} må være en ikke-tom streng')
                try:
                    for key in ('attemptedAt', 'finishedAt', 'measuredAt', 'reportedAt'):
                        if key in entry:
                            timestamp(entry[key])
                    if field == 'attempts':
                        aid = entry['attemptRef']
                        if not isinstance(aid, str):
                            continue
                        if aid in attempts:
                            self.errors.append(f'{ref}: duplikat attemptRef')
                        attempts[aid] = entry
                        if 'finishedAt' in entry and timestamp(entry['finishedAt']) < timestamp(entry['attemptedAt']):
                            self.errors.append(f'{ref}: finishedAt før attemptedAt')
                    if field in ('measurements', 'reports'):
                        state = entry['state']
                        if not isinstance(state, str) or state not in STATES:
                            self.errors.append(f'{ref}: ukjent state')
                        if state == 'blocked' and not entry.get('reason'):
                            self.errors.append(f'{ref}: blocked krever reason')
                        time_key = 'measuredAt' if field == 'measurements' else 'reportedAt'
                        identity = (ref, timestamp(entry[time_key]))
                        if identity in seen:
                            self.errors.append(f'{ref}: tvetydige {field} på samme tidspunkt')
                        seen.add(identity)
                    if field == 'measurements':
                        if self.children.get(ref):
                            self.errors.append(f'{ref}: samlingens slutning hører hjemme i reports, ikke measurements')
                        if ('phase' in entry) != ('attemptRef' in entry):
                            self.errors.append(f'{ref}: invariantmåling krever både phase og attemptRef')
                        if 'phase' in entry and entry['phase'] not in ('before', 'after'):
                            self.errors.append(f'{ref}: phase må være before eller after')
                    if field == 'reports':
                        comp = self.nodes[ref].get('composition', {})
                        if isinstance(comp, dict) and comp.get('kind') == 'firstOf' and entry['state'] == 'green' and not entry.get('branchRef'):
                            self.errors.append(f'{ref}: grønn firstOf uten registrert gren (regel 4)')
                        if 'branchRef' in entry and entry['branchRef'] not in self.children.get(ref, []):
                            self.errors.append(f'{ref}: branchRef må peke på et direkte barn')
                except (ValueError, TypeError) as exc:
                    self.errors.append(f'{ref}/{field}: {exc}')
        for entry in self.execution.get('measurements', []):
            if isinstance(entry, dict) and 'attemptRef' in entry:
                aid = entry['attemptRef']
                if not isinstance(aid, str) or aid not in attempts:
                    self.errors.append('invariantmåling peker på ukjent attemptRef')

    def _entries(self, field, ref=None, at=None):
        key = {'attempts': 'attemptedAt', 'measurements': 'measuredAt', 'reports': 'reportedAt'}[field]
        return sorted((e for e in self.execution.get(field, [])
                       if (ref is None or e['purposeRef'] == ref)
                       and (at is None or timestamp(e[key]) <= at)), key=lambda e: timestamp(e[key]))

    def _latest(self, field, ref, at):
        entries = self._entries(field, ref, at)
        return entries[-1] if entries else None

    def evaluate(self, ref, at=None, stack=()):
        """Derived conclusion, never written into the evidence log."""
        if self.errors:
            return outcome('unverified', 'ugyldig struktur eller kjøringslogg')
        if isinstance(at, str):
            at = timestamp(at)
        if ref not in self.nodes or ref in stack:
            return outcome('unverified', 'ukjent referanse eller sirkulær evaluering')
        node = self.nodes[ref]
        children = self.children.get(ref, [])
        if not children:
            measurement = self._latest('measurements', ref, at)
            attempt = self._latest('attempts', ref, at)
            if (measurement and measurement['state'] == 'blocked'
                    and (attempt is None or timestamp(measurement['measuredAt']) >= timestamp(attempt['attemptedAt']))):
                return outcome('blocked', measurement['reason'])
            violation = self._sequence_admission(ref, at, stack)
            if violation is not None:
                return violation
            if measurement is None or (attempt and timestamp(measurement['measuredAt']) < timestamp(attempt['attemptedAt'])):
                return outcome('unverified', 'mangler måling for gjeldende forsøk')
            return outcome(measurement['state'], measurement.get('reason', measurement['evidenceRef']))
        comp = node.get('composition')
        ordered = node.get('childOrder', children) if comp is not None else children
        values = {child: self.evaluate(child, at, stack + (ref,)) for child in ordered}
        blocked = [f"{child}: {v['reason']}" for child, v in values.items() if v['state'] == 'blocked']
        if blocked:
            return outcome('blocked', '; '.join(blocked))
        if comp is None:
            return outcome('unverified', 'mangler eksplisitt composition; ingen default')
        violation = self._sequence_admission(ref, at, stack)
        if violation is not None:
            return violation
        # An invariant constrains its over collection, including disjunctions and
        # targets in another branch. A successful alternative cannot bypass it.
        guards = []
        for guard_ref, guard_node in self.nodes.items():
            guard = guard_node.get('composition', {})
            if guard.get('kind') == 'invariant' and guard.get('over') == ref:
                guards.append(self._invariant(guard_ref, ref, self.children[guard_ref], at))
        for state in ('blocked', 'red', 'unverified'):
            matching = [g['reason'] for g in guards if g['state'] == state]
            if matching:
                return outcome(state, '; '.join(matching))
        kind = comp['kind']
        if kind == 'invariant':
            return self._invariant(ref, comp['over'], children, at)
        if kind == 'firstOf':
            report = self._latest('reports', ref, at)
            branch = report.get('branchRef') if report else None
            if branch is None:
                return outcome('unverified', 'firstOf mangler registrert gren')
            index = ordered.index(branch)
            if any(values[c]['state'] == 'green' for c in ordered[:index]):
                return outcome('red', 'registrert gren er ikke første grønne gren')
            if any(values[c]['state'] != 'red' for c in ordered[:index]):
                return outcome('unverified', 'tidligere grener er ikke avklart')
            # First success ends the run, even if a later measurement revokes it.
            event_times = sorted({timestamp(e[key]) for field, key in
                                  (('measurements', 'measuredAt'), ('reports', 'reportedAt'))
                                  for e in self._entries(field, at=at)})
            for event_time in event_times:
                successes = [c for c in ordered if self.evaluate(c, event_time, stack + (ref,))['state'] == 'green']
                if successes:
                    if successes[0] != branch:
                        return outcome('red', 'registrert gren var ikke første verifiserte grønne gren')
                    if any(timestamp(a['attemptedAt']) >= event_time for c in ordered
                           for a in self._entries('attempts', c, at)):
                        return outcome('red', 'forsøk registrert etter at firstOf var avsluttet')
                    break
            # Preference order and stop at the selected green branch.
            for pos, child in enumerate(ordered):
                attempts = self._entries('attempts', child, at)
                if pos <= index and not attempts:
                    return outcome('unverified', f'{child}: mangler registrert forsøk')
                if pos > index and attempts:
                    return outcome('red', 'gren forsøkt etter grenen som avsluttet firstOf')
                for attempt in attempts:
                    if pos:
                        previous = self.evaluate(ordered[pos - 1], timestamp(attempt['attemptedAt']) - dt.timedelta(microseconds=1), stack + (ref,))
                        if previous['state'] != 'red':
                            return outcome(previous['state'] if previous['state'] == 'blocked' else 'red',
                                           f'{child}: tidligere gren var ikke rød ved forsøk; {previous["reason"]}')
            return outcome(values[branch]['state'], values[branch]['reason'], branchRef=branch)
        minimum = comp.get('min', 1) if kind == 'anyOf' else len(children)
        green = sum(v['state'] == 'green' for v in values.values())
        unknown = sum(v['state'] == 'unverified' for v in values.values())
        if green >= minimum:
            return outcome('green', f'{green}/{len(children)} barn grønne; krever {minimum}')
        if green + unknown >= minimum:
            return outcome('unverified', f'{green}/{minimum} nødvendige grønne barn verifisert')
        return outcome('red', f'{green}/{minimum} nødvendige grønne barn; røde barn hindrer oppfyllelse')

    def _sequence_admission(self, ref, at, stack):
        parent = self.nodes[ref].get('parentRef')
        if parent not in self.nodes or self.nodes[parent].get('composition', {}).get('kind') != 'sequence':
            return None
        order = self.nodes[parent]['childOrder']
        attempts = self._entries('attempts', ref, at)
        if not attempts:
            return outcome('unverified', f'{ref}: mangler registrert forsøkstidspunkt')
        index = order.index(ref)
        if index:
            for attempt in attempts:
                before = timestamp(attempt['attemptedAt']) - dt.timedelta(microseconds=1)
                previous = self.evaluate(order[index - 1], before, stack + (ref,))
                if previous['state'] != 'green':
                    state = 'blocked' if previous['state'] == 'blocked' else 'red'
                    return outcome(state, f"{ref}: forsøkt før forrige barn var grønt; {previous['reason']}")
        return None

    def _invariant(self, ref, target, conditions, at):
        steps = [c for c in self.children[target] if self.nodes[c].get('composition', {}).get('kind') != 'invariant']
        attempts = [a for a in self._entries('attempts', at=at) if a['purposeRef'] in steps]
        measurements = [m for m in self._entries('measurements', at=at) if m['purposeRef'] in conditions]
        for m in measurements:
            if m['state'] == 'blocked':
                return outcome('blocked', m['reason'])
        failed = [m for m in measurements if m['state'] == 'red']
        if failed:
            first = timestamp(failed[0]['measuredAt'])
            continued = any(timestamp(a['attemptedAt']) > first for a in attempts)
            return outcome('red', 'invariant brutt' + ('; steg startet etter bruddet' if continued else '; stopp påkrevd, ingen automatisk rollback'))
        if not steps or not attempts:
            return outcome('unverified', 'mangler forsøk for steg i invariant.over')
        # Alternatives that were never taken need no before/after checks. Evidence
        # of work on a step, however, cannot bypass its missing attempt record.
        attempted = {a['purposeRef'] for a in attempts}
        evidence_refs = {e['purposeRef'] for field in ('measurements', 'reports')
                         for e in self._entries(field, at=at)}
        for step in steps:
            descendants = {step}
            pending = [step]
            while pending:
                child = pending.pop()
                descendants.update(self.children.get(child, []))
                pending.extend(self.children.get(child, []))
            if step not in attempted and descendants & evidence_refs:
                return outcome('unverified', f'{step}: evidens finnes, men forsøk mangler i invariant.over')
        for attempt in attempts:
            if 'finishedAt' not in attempt or (at is not None and timestamp(attempt['finishedAt']) > at):
                return outcome('unverified', 'steg er ikke registrert ferdig')
            start, end = timestamp(attempt['attemptedAt']), timestamp(attempt['finishedAt'])
            for condition in conditions:
                for phase in ('before', 'after'):
                    matches = [m for m in measurements if m['purposeRef'] == condition
                               and m.get('attemptRef') == attempt['attemptRef'] and m.get('phase') == phase]
                    if not matches or any(m['state'] != 'green' for m in matches):
                        return outcome('unverified', f'{condition}: mangler grønn {phase}-måling for {attempt["attemptRef"]}')
                    for m in matches:
                        measured = timestamp(m['measuredAt'])
                        if (phase == 'before' and measured >= start) or (phase == 'after' and measured <= end):
                            return outcome('red', f'{condition}: {phase}-måling på feil side av steget')
                        if phase == 'before' and any('finishedAt' in a and measured <= timestamp(a['finishedAt']) < start for a in attempts):
                            return outcome('red', 'før-måling gjenbrukt fra før et tidligere steg var ferdig')
                        # An after-check cannot be deferred until the next step has started.
                        if phase == 'after' and any(end < timestamp(a['attemptedAt']) <= measured for a in attempts):
                            return outcome('red', 'neste steg startet før invariantens etter-måling')
        return outcome('green', 'alle betingelser målt grønne før og etter hvert registrert steg')

    def validate(self):
        errors = list(self.errors)
        if not errors:
            for report in self.execution.get('reports', []):
                if report['state'] == 'green':
                    result = self.evaluate(report['purposeRef'], report['reportedAt'])
                    if result['state'] != 'green':
                        errors.append(f"{report['purposeRef']}: rapportert grønn i strid med composition (regel 6): {result['state']}: {result['reason']}")
        return errors, list(self.warnings)
