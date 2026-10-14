# Fabel: etterkontroll av rettelsene etter kodegranskingen (trinn 1 og 2)

Dato: 02.10.2026, natt. Kontrollert mot `work/korrespondanse_vakt.py.foer-kodegransking` og `work/installer.py.foer-kodegransking` (diff lest linje for linje), `pdd-cron/PLAN_VEDLEGG.md` («Fabels gransking av koden for trinn 1 og 2»), kontrakten, `handoff/README.md` S2 og `impl/Docs/`. Linjenumre uten filnavn viser til `impl/Scripts/scheduled/korrespondanse_vakt.py`; «installer» viser til `impl/Scripts/scheduled/installer.py`. Egne forsøk ligger i `/tmp/fabel-kode/exp_k_final_lock.py` og `exp_n_r.py`.

**Testene.** `python3.9 -m unittest discover -s Tests/scheduled -p "test_*.py" -v`: 30 tester, OK, 277 s. `korrespondanse_vakt.py selvtest`: `SELVTEST OK 120 kontroller`, kjørt tre ganger (14,0 / 13,7 / 13,7 s), ingen `FEIL`-linjer. `ProductionLimits` (den på 50 sekunder) kjørt tre ganger til for seg: 50,09 / 50,09 / 50,09 s, OK. Ingenting var ustabilt. Ingen `__pycache__` ble lagt i `Scripts/scheduled/` av testene eller installasjonen. Omslaget `koe/korrespondansevakt.sh` har de nye sjekksummene (regnet etter med `sha256sum`: alle tre stemmer), og er mal-lik `lag_omslag.py`.

## Utfall

| # | Utfall | Hvor |
|---|---|---|
| Må 1 | **løst** | 679–683 (`if not messages: return`); kontrakten linje 72; selvtest `page50` 1345, 1633–1639; `Docs/ScheduledEvents.md` 166–169. Målt (`exp_n_r.py`): kall per profil = sider + 1; 0 meldinger → 1 kall, 3 → 2, 250 → 4, 60 med 50 per side → 3 kall og den uleste funnet, 1900 → 20 kall ok, 1901 → «for mange sider». Ingen evig løkke: `for _ in range(limits.max_pages)` (659) begrenser, og `highest <= after` (683–684) stopper en tjener som ikke blar. |
| Bør 1 | **løst** | 704–714 (`except Deadline` i `finally`, lesingen beholdes), 728–729 (ikke nytt forsøk), 861–862 (ingen ny profil), 874–876 (notat). Selvtest `test_alarm` 1677–1713, med `slow-close` 1368. Jeg finner ingen lås i den: `_deadline_seen` er en `Event`, ingen venter på den. Den skjuler ingen feil: profilen som ble lest, føres som `ok`, de som ikke ble begynt på, som `klienten svarte ikke i tide`, og stempelet får notatet. En klient som ble avbrutt midt i `_kill_group`, står i `_active_groups` til `kill_all_clients()` i `run_task` (1265) tar den. Rest: lander alarmen i `os.remove(error_path)` (712) eller mellom `return` og `read[profile] = …` (864), tapes lesingen som før; vinduet er ett systemkall. |
| Bør 2 | **delvis (ny feil 1)** | 1123–1125, 1132, 1137. Siste-utvei-tidtakeren finnes og virker når hovedløpet står, men `stop()` avbestiller den også når vakttråden alt er i gang. |
| Bør 3 | **løst** | 1259–1261 (`except Exception` → én linje, kode 1); 159–160 (årstall 2000–2999). Selvtest `test_unexpected` 1714–1752, `test_text` 1809–1810. |
| Bør 4 | **løst** | 496–509: `_error_tail` leser de siste 2000 byte (500–501), `_timeout` legger dem ved (506–508), brukt i 516, 519, 541, 544. Kontrakten linje 28, `Docs/ScheduledEvents.md` 145–147. |
| Bør 5 | **løst** | 66–67 (`{0,35}`); kontrakten linje 39; `Docs/ScheduledEvents.md` 171–172; selvtest 1824–1830 (37 avvises, 36 får plass). |
| Bør 6 | **løst** | 734–756 (`TEMPORARY_RE`, `is_leftover`, `remove_stale_leftovers`), kalt i 853 og 994; installer 674–680 og 700–701; selvtest 1740–1752; `test_installer` 399–418. |
| Bør 7 | **løst** | 934–938 og 1062–1066 (skriv, så fjern); 874 og 995 (`signal.alarm(0)` før filarbeidet). `Docs/ScheduledEvents.md` 133–136 og 170; kontrakten linje 27. Se ny feil 2 for den lille resten. |
| Bør 8 | **delvis** | 114, 1139–1141, 1267–1273. Låsen fjerner den doble linjen i det sannsynlige sammenfallet (vakttråden tar låsen mens hovedløpet er i `finally`): hovedløpet blokkerer da på 1267 og vakttråden avslutter prosessen. Men den innfører en vei der ingen avslutter (ny feil 1), og i det sjeldnere sammenfallet (vakttråden våkner etter at hovedløpet tok låsen) kommer fortsatt to linjer, for `fire()` sjekker ikke om hovedløpet er ferdig når den får låsen (1140–1142). |
| Bør 9 | **løst** | installer 646–665 (`wait_for_running_tasks`), 741–746; `Docs/OperatorRunbook.md` 547–551; `handoff/README.md` 93; `test_installer` 399–418. Venter på låsfiler yngre enn ti minutter, høyst 70 s, og sier fra når den rydder likevel. Vinduet som er igjen: en kjøring planleggeren startet like før omstarten, men som ikke har rukket å ta låsen når `fjern` ser (pythons oppstart, noen titalls millisekunder) — uten praktisk betydning. |
| Bør 10 | **løst** | installer 66–67, 371–392; `handoff/README.md` 85; `test_installer` 277–278, 316–320. Fire agentkall i stedet for to; verste vei i installasjonen blir ca. 7,5 minutter mot køens 10. |
| Bør 11 | **løst** | installer 771–778; `test_installer` 420–428. |
| Bør 12 | **løst** | installer 526, 533–556 (`describe_markers`: avsender og profil, antall andre), 692; `test_installer` 370–371, 387. |
| Bør 13 | **løst** | installer 36; `test_installer` 279. Bekreftet: ingen `__pycache__` etter testkjøringen. |
| Bør 14 | **delvis, med hensikt** | installer 262–265 (` : `), og `Docs/OperatorRunbook.md` 536–538 sier at skråstreker og tomme lister likevel skrives annerledes. Det holder. |
| Bør 15 | **løst** | installer 571–573. |
| Bør 16 | **løst** | installer 416–420 (`O_CREAT | O_TRUNC | O_WRONLY, 0o600`). |
| Bør 17 | **løst** | kontrakten 27, 28, 39, 72, 160 (120 kontroller, fjorten sekunder); `Docs/ScheduledEvents.md` 133–136, 145–147, 166–172, 210–214; `Docs/OperatorRunbook.md` 531, 536–538, 547–551. Ett nytt hull, se ny feil 3. |
| Bør 18 | **delvis, som sagt** | Lagt til: alarmen og treg lukking (selvtest 1677–1713), 50 per side (1633–1639), de ekte grensene (`test_korrespondanse_vakt.py` 314–340), `fjern` under en kjøring (`test_installer` 399–418), filfeil (selvtest 1732–1738, `test_installer` 420–428), tidspunkt som ikke kan tolkes (1641–1649). Omslaget har fortsatt ingen automatisk test; det står i sporingen. |

Løst: 15 av 19 (Må 1 og 14 bør). Delvis: 4 (Bør 8, 14, 18 og Bør 2 med forbehold om ny feil 1). Ikke løst: 0.

## Nye feil

### 1. `stop()` avbestiller siste utvei mens vakttråden kan være i gang; står den fast med låsen, henger prosessen

**Fil og linje.** `korrespondanse_vakt.py` 1134–1137 (`stop()` avbestiller `timer` og `last_resort`), 1139–1142 (`fire()` tar `_final_lock` og setter `_fired` *etterpå*), 1262–1267 (`finally` kaller `stop()`, så `with _final_lock:`).

**Hva som skjer.** Går tidtakeren akkurat når hovedløpet er i `finally` mellom `_halt_if_fired()` (1263) og `watchdog.stop()` (1264), tar `fire()` låsen og begynner på stempelet. Hovedløpet avbestiller så `last_resort` (1137), slipper låsfila og blokkerer på `with _final_lock` (1267). Blir vakttråden ferdig, avslutter den prosessen med kode 3: én linje, men stempel og kode sier «avbrutt» om en kjøring som var ferdig. Står vakttråden fast i `read_stamp`/`write_stamp` (1145–1153, et filsystem som henger), er det ingen igjen som avslutter: hovedløpet venter på låsen, `last_resort` er avbestilt. Før rettelsen skrev hovedløpet linjen sin og avsluttet (to linjer, ingen heng); nå kan det bli heng. Begge krever at tidtakeren går i et vindu på mikrosekunder ved nøyaktig 60 s, det andre også et filsystem som står; dette er altså teori, men det er nettopp siste utvei som settes ut av spill. *Prøvd:* `exp_k_final_lock.py` kjører `fire()` i en tråd med `write_stamp` byttet med en som står; etter `stop()` er `last_resort.finished` satt, og `_final_lock.acquire(timeout=3)` fra hovedløpet gir `False`.

**Hva som bør stå.** Tre små endringer som også lukker den gjenværende doble linjen (Bør 8):

```python
_finished = threading.Event()   # hovedløpet har skrevet linjene sine

    def stop(self):
        signal.alarm(0)
        self.timer.cancel()
        if not _fired.is_set():          # er vakttråden i gang, skal siste utvei stå
            self.last_resort.cancel()

    def fire(self):
        _fired.set()                     # før låsen, så stop() ser det
        if not _final_lock.acquire(timeout=2):
            os._exit(3)
        if _finished.is_set():           # hovedløpet ble ferdig først: rør ingenting
            _final_lock.release()
            return
        ...

    # run_task
    with _final_lock:
        _finished.set()
        sys.stdout.write(...)            # uten _halt_if_fired() her: den som har låsen, gjør seg ferdig
```

Med `_fired` satt før låsen sover hovedløpet i `_halt_if_fired()` (1263) om vakttråden er i gang, og `stop()` nås ikke; nås den likevel, lar den `last_resort` stå. `_halt_if_fired()` inne i `with` (1268) må da bort, ellers kan hovedløpet sove med låsen. Selvtestens `test_watchdog` (1963–1984) dekker fortsatt veien der vakttråden slår inn.

### 2. `signal.alarm(0)` stopper ikke en behandler som alt er på vei

**Fil og linje.** 874 og 995 (`signal.alarm(0)`), 1103–1104 (`_raise_deadline`).

**Hva som skjer.** Kommer SIGALRM i mikrosekundene mellom siste sjekk i leseløkken og kallet `signal.alarm(0)`, har C-nivået alt notert signalet, og Pythons behandler kjører ved neste bytekode: `Deadline` kastes i markørfasen, utenfor `try` (859–871), og ender i `run_task` (1254–1255) som «avbrutt av tidsgrensen», uten stempel. Det er resten av Bør 7, og vinduet er like smalt som før; men kontrakten linje 27 sier nå at alarmen «aldri avbryter skrivingen».

**Hva som bør stå.** Et flagg i behandleren: `_alarm_armed = [False]`; `start()` setter det sant etter `signal.alarm(…)`, `run_sjekk`/`run_frist` setter det falskt rett før `signal.alarm(0)`, og `_raise_deadline` kaster bare når det er sant. Da er «aldri» sant.

### 3. Årstallsvinduet står bare i koden

**Fil og linje.** 159–160 mot kontrakten `trinn1-2-programmer.md` linje 45 («Tidspunkter») og `Docs/ScheduledEvents.md` (ingen setning om det).

**Hva som skjer.** Et tidspunkt med årstall utenfor 2000–2999 regnes nå som «kan ikke tolkes»: i `createdAt` teller det bare i stempelet (riktig), men i `expiresAt` gir det `frist-feilet-<profil>`, kode 1 og linjen «fikk ikke lest tilgangsbeviset» (`exp_n_r.py`: `9999-12-31T23:59:59Z` → `frist-feilet-kjetil-d`). Et bevis med «aldri» som frist er usannsynlig, men regelen bør stå der reglene står.

**Hva som bør stå.** I kontrakten linje 45 og `Docs/ScheduledEvents.md`: «Årstall utenfor 2000–2999 regnes som et tidspunkt som ikke kan tolkes.» Vil man heller behandle en frist etter år 2999 som «ingen frist», må `read_expiry` (968–986) få det, ikke `parse_time`.

## Merknader (ikke feil)

- `remove_own_files` (installer 674–680) fjerner enhver `.<navn>.tmp-<tall>-<tall>` i den delte markørmappen uansett alder og eier. Navnet er programmets eget, og `fjern` kjøres etter at ingen kjøring holder låsen, så det går bra; vil man være pirkete, krev prefiksene `ulest-`, `sjekk-` og `frist-`.
- `install_program` (installer 588–598) rydder ikke `bin/korrespondanse_vakt.py.tmp-<pid>` hvis `os.replace` feiler (tilfellet i `test_installer` 420–428 etterlater en slik fil). Harmløst.
- `Docs/ScheduledEvents.md` 210–212 sier «roughly a thousand messages»; målt grense er 1900 med 100 per side (20 kall), 950 med 50 per side. Forsiktig, og greit.
- `wait_for_running_tasks` brukes bare i `fjern`. I `utfoer` på nytt er «kjører allerede» som første utfall fortsatt mulig og står i `handoff/README.md` linje 91.
