# Fabel: tredje etterkontroll av koden for trinn 1 og 2 (signaler, alarm, siste utvei)

Dato: 03.10.2026. Gransket som uavhengig kodegransker, uten å ha sett koden før. Linjenumre uten filnavn viser til `impl/Scripts/scheduled/korrespondanse_vakt.py` (md5 `18757fa4…`, uendret under granskingen); «testene» er `impl/Tests/scheduled/test_korrespondanse_vakt.py` (md5 `995e6d19…`). Endringene siden forrige etterkontroll har jeg lest som `diff -u` mot `work/*.foer-etterkontroll2` (`fabel-trinn1-2-etterkontroll3/diff_vakt.patch`, `diff_test.patch`). Forsøkene mine ligger i `scratchpad/fabel-trinn1-2-etterkontroll3/` (`exp_*.py` med utskriftene i `exp*_resultat*.txt`), og en kopi av `impl/` med alle rettelsene jeg foreslår, i `impl_kopi/` (`forslag_rettelser.patch` er forskjellen). Alt er målt her, på Linux med Python 3.9.23 (og 3.11.15 der det står), med `/bin/sh` = dash og `/usr/bin/bash` 5.2. Det som bare gjelder macOS og 3.9.6, står under «Ikke kontrollert». Ingenting i `impl/`, `koe/`, `trinn3/`, `work/` eller `pdd-cron/` er endret, og ingen `.pyc` er lagt der (de tre `Tests/scheduled/__pycache__/test_installer.*.pyc` lå der fra før, se Bør 8).

Jeg fikk ikke lese agentens Swift-kilde i denne økten (tilgangen ble avslått av verktøyet), så premisset om planleggeren — `SIG_IGN` for SIGTERM og SIGINT, arvet over `exec` — tar jeg fra briefen og fra forrige rapports lesing av `HavenAgentMain.swift` 1171–1173.

**Testene.** De ni nye og omskrevne testene (`Signals`, `AfterARun`, `WatchdogOrdering`): OK på 3.9 (1,35 s) og 3.11 (1,37 s). Hele `test_korrespondanse_vakt.py` mot programmet som det står: `Ran 24 tests in 70.586s — OK` på 3.9 (`suite_impl_vakt_3.9.txt`; lastsnittet på maskinen var 1,9 da den startet, rett etter mine egne forsøk, og 0,6 da den var ferdig; `ProductionLimits` holdt sin grense på 55 s begge gangene jeg kjørte modulen, men testen skriver ikke ut tiden sin, så marginen har jeg ikke målt). `test_installer.py` (15 tester) har jeg ikke kjørt; den er ikke endret. Selvtesten: `SELVTEST OK 120 kontroller`, 13,7 s, også når selvtesten selv startes med SIGTERM og SIGINT oversett og `exec` (`expM_resultat.txt`). Kopien med alle forslagene mine: `Ran 24 tests in 71.107s — OK`, `SELVTEST OK 126 kontroller` på 3.9 og 3.11.

## De seks punktene

| # | Punkt | Status | Hvordan prøvd |
|---|---|---|---|
| Bør 1 | `disarm_alarm()` inne i `try` | **Lukket.** 893 inne i `try`, 896 først i `except Deadline`. | Forrige rapports `exp5` (SIGALRM reist synkront inne i `disarm_alarm()`) mot gjeldende kode: `kode 0`, «1 profil lest, 1 avsender med ulest post», stempel og markør skrevet, `disarm_alarm kalt med armed = [True, False, False]` (`exp5_resultat.txt`). Mot utgaven før ga samme forsøk kode 1 uten stempel (forrige rapport). Et restvindu av samme slekt, men bare for feil som ikke er `Failure`, står som Bør 1 under. |
| Bør 2 | Siste utvei avbestilles i sluttblokken, ikke i `stop()` | **Lukket.** `stop()` (1164–1168) rører den ikke; `_run_with_lock` avbestiller den under `_final_lock` etter `_finished.set()` (1391–1394). | `exp_b_stop_vindu.py`: vakttråden slippes løs i det `stop()` returnerer og står fast i `write_stamp`. Gjeldende kode: `siste utvei avbestilt: False`, hovedløpet får ikke låsen → «siste utvei står: prosessen ville avsluttet etter 3605 s». Kopien av utgaven før: «INGEN avslutter» (`expB_resultat*.txt`). `AfterARun` ser at ingen `Timer` står igjen etter en ferdig kjøring; jeg har gått gjennom alle veiene ut av `_run_with_lock` (under «Kontrollert»). |
| Bør 3 | SIGTERM avslutter ordnet | **Lukket.** `_terminate` 1278–1299 tar ingen lås, dreper gruppene, slipper låsen, én linje, `os._exit(128+signum)`. | `exp_c_signal_midt_i.py`: SIGTERM midt i en kjøring med hengende klient, startet gjennom `/bin/sh -c 'trap "" TERM INT; exec "$@"'`, gjennom `/usr/bin/bash` med samme `trap`, og uten skall: alle `avsluttet med 143 etter 0.4 s`, stdout tom, stderr én linje, låsen borte, intet stempel, klienten død; igjen ligger bare `.klient-stderr-<pid>-1.txt` (`expC_resultat.txt`). Forrige rapports `exp4` mot ny kode: neste kjøring straks går som vanlig (låsen er sluppet), og stderr-fila ryddes når den er ti minutter gammel (`exp4_resultat_naa.txt`). Restene står under Bør 3–4 og «Merknader» 1–3. |
| Bør 4 | Bare SIGTERM alltid; SIGINT bare når ikke oversett; SIGHUP urørt | **Lukket.** 1320–1331. | `exp_c`: SIGINT uten `trap` → `130`, én linje, ryddet. SIGINT med `trap "" TERM INT` gjennom bash → kjøringen går ferdig (kode 1 fordi klienten henger, stempel skrevet, 25 s). Testen `test_term_is_always_taken_over_and_an_ignored_int_is_left_alone` fester at SIGHUP som er `SIG_IGN` blir stående og at `previous` bare har SIGTERM. |
| Bør 5 | Testene prøver arven over `exec` | **Lukket.** `Signals.WRAPPER` (419) brukes i 445 og 463. | Kjørt på 3.9 og 3.11. `expL_note_bash.txt`: stempelets `note` er «startet med SIGTERM oversett» både gjennom dash og bash 5.2 med `trap "" TERM INT`, `None` med bare `trap "" INT` og uten `trap` — så arven går gjennom begge skallfamiliene her, og merknaden er knyttet til SIGTERM alene. Macens bash 3.2 står under «Ikke kontrollert». Én test lover mer enn den gjør (Bør 6 under). |
| Bør 6 | Kontrakten sier det samme som koden | **Lukket.** `contract/trinn1-2-programmer.md` linje 30 og 38; `Docs/ScheduledEvents.md` 148–158 og 209. | Lest setning for setning mot `_terminate`, `install_signal_handlers`, `build_stamp` og målingene over: kode 143/130, én linje på stderr, ingen stempel, klienten drept, låsen sluppet, SIGINT-unntaket, SIGHUP, merknaden i `note` — alt stemmer. Småting under Bør 8–9 og «Merknader». |

## Nye funn som må rettes før installasjon

Ingen. Jeg finner ingen vei som henger planleggeren, gir to sluttlinjer på stdout, gir feil sak eller bruker mer enn 65 sekunder. Det som er igjen, er restvinduer på mikrosekunder, en testlovnad som ikke holdes, et hull i selvtesten, og dokumentasjon.

## Nye funn som bør rettes

Alle fem kodeforslagene (Bør 1–5) står samlet i `fabel-trinn1-2-etterkontroll3/forslag_rettelser.patch` og er prøvd i `impl_kopi/`: 24 tester OK, selvtesten OK, og alle forsøkene under gir riktig utfall der.

### Bør 1. Alarmen står armert ut av lesefasen når feilen ikke er `Failure`; da kan `Deadline` kastes i `finally` i `_run_with_lock`, utenfor alt som fanger den

**Linjer.** 882–900 (`try … except Deadline` i `run_sjekk`), 1376–1388 (`except OSError`, `except Exception` og `finally` i `_run_with_lock`).

**Hva som skjer.** `disarm_alarm()` kalles bare på to veier ut av lesefasen: etter løkken (893) og i `except Deadline` (896). En `OSError` eller en annen feil som ikke er `Failure` fra lesefasen — `open(error_path, "wb")` i `Client.__init__` (497) når disken er full, `os.read`/`select` med EIO/EBADF, `os.makedirs` (708), eller en `TypeError` som i Bør 5 — går forbi begge. Da fanges feilen i `_run_with_lock` (1378/1381), men alarmen er fortsatt armert til `watchdog.stop()` i `finally` (1386). Går SIGALRM i det vinduet, kastes `Deadline` fra `except`-kroppen eller fra `_halt_if_fired()` (1385): `finally` avbrytes, `watchdog.stop()`, `kill_all_clients()` og `lock.release()` kjøres ikke, `with _final_lock` nås ikke, og unntaket går ut av `main`: traceback på stderr (12 linjer), ingen linje på stdout, kode 1, låsfila står (forlatt etter ti minutter). Prosessen avslutter (tidtakertrådene er daemon), så det er ikke et heng. Vinduet er mikrosekunder, og det krever samtidig en sjelden feil, så dette er teori — men det er samme slekt som forrige Bør 1, og det er like billig å lukke.

**Prøvd.** `exp_fgh_restvinduer.py G`: `Client.__init__` byttes med en som kaster `OSError(28)`, og `_halt_if_fired` med en som først reiser SIGALRM synkront. Gjeldende kode: `kode 1`, `stdout (0 linjer)`, `stderr (12 linjer): Traceback … korrespondanse_vakt.Deadline`, `tilstand: ['korrespondanse-sjekk.lock']` (`expFGH_resultat.txt`). Kopien: `kode 1`, «korrespondanse-sjekk: ikke fullført» / «en fil kunne ikke leses eller skrives (OSError)», `tilstand: []` (`expFGH_resultat_kopi_v2.txt`).

**Hva som bør stå.** Behold kallet inne i `try` (893), ta det bort fra `except Deadline`, og legg til `finally: disarm_alarm()` på samme `try`:

```python
    try:
        for profile in order:
            ...
        disarm_alarm()          # inne i try: et Deadline som kastes akkurat her, fanges under
    except Deadline:
        interrupted = True
        ...
    finally:
        disarm_alarm()          # sikkerhetsnett: også OSError og andre feil forlater lesefasen avslått
```

Merk: bare `finally`, uten kallet inne i `try`, åpner forrige Bør 1 igjen — et `Deadline` reist inne i `disarm_alarm()` i `finally` går da til `_run_with_lock` sitt `except Deadline` uten stempel. Jeg prøvde den varianten først; `exp5` mot den ga `stempel finnes: False` og `markører: []` (samme runde som `expFGH_resultat_kopi.txt`; utskriften av `exp5` i den runden er ikke lagret). Med begge kallene gir `exp5` kode 0 med stempel (`exp5_resultat_kopi_v2.txt`). Et `Deadline` reist inne i `finally`-kallet (bare mulig etter en slik feil) fanges av `_run_with_lock` og gir «avbrutt av tidsgrensen» med låsen sluppet, som er riktig.

### Bør 2. `os.remove(error_path)` står utenfor `except Deadline`, så en ferdig lesing kan fortsatt tapes i det kallet

**Linjer.** 717–727 i `read_profile_once`.

**Hva som skjer.** `client.close(graceful)` er dekket (720–723): et `Deadline` der setter `_deadline_seen`, og resultatet beholdes. `os.remove(error_path)` rett etter (725) fanger bare `OSError`. Kastes `Deadline` der, går `return result` tapt (et unntak i `finally` forkaster returverdien), `read_profile` lar det gå videre, og `run_sjekk` fører profilen som «avbrutt av tidsgrensen for hele kjøringen» — selv om innboksen var ferdig lest. Vinduet er ett `unlink`-kall per profil, mot de to sekundene `close()` dekker, så i praksis forsvinnende. Men det er den ene plassen i lukkingen som ikke er dekket, og rettelsen er fire linjer.

**Prøvd.** `exp_fgh_restvinduer.py H`: `os.remove` reiser SIGALRM synkront når det er stderr-fila som fjernes. Gjeldende kode: `kode 1`, «0 av 1 profil lest», stempelet sier `failed / klienten svarte ikke i tide / avbrutt av tidsgrensen for hele kjøringen`, ingen markør. Kopien: `kode 0`, «1 profil lest, 1 avsender med ulest post», markøren skrevet, `note='kjøringen ble avbrutt av tidsgrensen'`.

**Hva som bør stå.** `except Deadline: _deadline_seen.set()` også rundt `os.remove(error_path)` (fila ryddes da av en senere kjøring, som i dag). Det irreduserbare som står igjen etter dette, er enkeltbytekoder (`return`-grensen i `read_profile`, tilordningen `read[profile] = …`); det kan ikke lukkes med en alarm som kaster unntak, og er ikke verdt å jage.

### Bør 3. Signalene bør blokkeres i tidtakertrådene, så et prosessrettet SIGTERM, SIGINT eller SIGALRM alltid lander i hovedtråden

**Linjer.** 1155–1162 (`Watchdog.start`).

**Hva som skjer.** Python kjører behandlerne i hovedtråden, men kjernen velger hvilken tråd som får et prosessrettet signal. Lander det i en av de to tidtakertrådene, avbrytes ikke hovedtrådens `select()` (12 s per forsøk), `time.sleep(3)` eller `process.wait()`; behandleren kjører først når kallet kommer tilbake. For SIGTERM betyr det at `_terminate` kan komme inntil 12 s etter signalet; for SIGALRM at `Deadline` kan komme inntil 12 s etter 55 s, så vakttråden ved 60 s tar over (kode 3 i stedet for 1). Ikke et heng, men unøyaktig, og det avhenger av noe som ikke er målt på macOS (forrige rapport, «Ikke kontrollert 4»). På Linux går signalet til hovedtråden (alle `exp_c`-kjøringene avsluttet på 0,4 s).

**Prøvd.** `exp_k_signal_til_tidtakertraad.py` tvinger valget med `signal.pthread_kill`, med `attempt_seconds = 10` og en klient som henger: mot hovedtråden `fra signal til avslutning: 0.00 s`; mot vakttrådens tidtaker `8.51 s` — nøyaktig til `select()` ga opp (`expK_resultat.txt`). Det viser mekanismen, ikke at XNU velger slik.

**Hva som bør stå.** Tidtakertrådene arver masken fra tråden som starter dem. Blokker de tre signalene rundt `start()`-kallene, så kjernen etter POSIX må levere til hovedtråden:

```python
        blocked = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGALRM, signal.SIGTERM, signal.SIGINT})
        try:
            self.timer.start()
            self.last_resort.start()
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, blocked)
```

Prøvd i kopien: selvtest og 24 tester OK, `exp_b`, `exp5` og `exp_c` som før. (Mitt eget `exp_k tidtaker` kan ikke brukes som bevis for rettelsen: et trådrettet signal mot en tråd som blokkerer det, blir liggende på den tråden; i programmet er signalene prosessrettede.)

### Bør 4. Et SIGTERM mellom `os.open` og `self.held = True` i `Lock.acquire()` lar den nye låsfila stå

**Linjer.** 421–436.

**Hva som skjer.** Låsfila opprettes i 421, men `held` settes først i 436, etter `fdopen` og skrivingen av pid og tidspunkt. Kommer `_terminate` mellom, ser `release()` `held == False` og rører ikke fila. Neste kjøring innen ti minutter sier «kjører allerede» (kode 0). Med 30 minutter mellom kjøringene er låsen alltid forlatt når neste kommer, så det merkes bare om planleggeren startes på nytt og kjører hendelsen straks innen ti minutter. Vinduet er omkring hundre mikrosekunder per kjøring.

**Prøvd.** `exp_fgh_restvinduer.py F`: `os.fdopen` reiser SIGTERM synkront første gang. Gjeldende kode: `kode 143`, `tilstand: ['korrespondanse-sjekk.lock']`. Kopien: `tilstand: []`.

**Hva som bør stå.** Sett `self.held = True` rett etter at `os.open` har lykkes, før innholdet skrives. Da er vinduet én–to bytekoder.

### Bør 5. `_find_tool` kaster `TypeError` når `inputSchema.required` er `true` eller et tall

**Linjer.** 630–632.

**Hva som skjer.** `required` skal være en liste etter JSON Schema, og klienten på `main` gir en liste. Men `if required: … ", ".join(str(item) for item in required)` itererer verdien uansett type: `True` og `5` gir `TypeError`, som ikke er `Failure`; kjøringen ender med «uventet feil (TypeError)», kode 1, uten stempel og markører, i stedet for «klienten har en annen kontrakt enn ventet» med stempel (og, via Bør 1, med alarmen armert ut av lesefasen). En tekst (`"relationshipID"`) gir en komisk men ufarlig detalj «verktøyet krever r, e, l, a, …».

**Prøvd.** Direkte kall på 3.9: `True -> TypeError 'bool' object is not iterable`, `5 -> TypeError`, `'relationshipID' -> Failure … verktøyet krever r, e, l, …`, `['relationshipID'] -> Failure`, `[]`/`None` -> verktøynavnet.

**Hva som bør stå.** Regn alt som ikke er en liste, som annen kontrakt: `if required is not None and not isinstance(required, list): raise Failure(F_CONTRACT, "required har ukjent form")`, og `if required: raise Failure(F_CONTRACT, "verktøyet krever %s" % ", ".join(str(item) for item in required))`.

### Bør 6. `test_an_int_that_is_not_ignored_ends_the_run_in_order_too` prøver ikke det navnet sier

**Linjer.** Testene 504–515.

**Hva som skjer.** Testen kontrollerer bare at `install_signal_handlers()` setter `_terminate` for SIGINT og at `restore_signal_handlers` setter `default_int_handler` tilbake. Ingen kjøring får SIGINT. Oppførselen er riktig — `exp_c` med `INT - nei`: `130`, én linje «avbrutt av signal 2», låsen borte, klienten død — men den er ikke festet, og navnet lover det. Legg til en søstertest til `test_term_in_the_middle_of_a_run_ends_it_in_order` uten `WRAPPER`, med `SIGINT` og `128 + signal.SIGINT`, eller gi testen et navn som sier hva den gjør («…installs the handler for int too»).

### Bør 7. Selvtesten prøver ikke signalene, og selvtesten er det eneste som kjøres på Macen før installasjon

**Linjer.** `run_all` 2112–2115; `test_watchdog` 2089–2110 viser mønsteret.

**Hva som skjer.** Installasjonen kjører `korrespondanse_vakt.py selvtest` med `/usr/bin/python3` før noe legges inn (kontrakten linje 161), ikke `unittest`. Selvtesten kaller `install_signal_handlers()` i hver kjøring, men `_terminate` kjøres aldri, og arven over `exec` gjennom `/bin/sh` prøves ikke. Dermed måles verken behandleren, bash 3.2 sin `trap ""; exec`, eller merknaden i stempelet på Macen før første ekte kjøring — nettopp de tre tingene forrige rapport lot stå under «Ikke kontrollert».

**Hva som bør stå.** Et `test_signals` i `SelfTest` etter mønsteret fra `test_watchdog`: start programmet som barn gjennom `/bin/sh -c 'trap "" TERM INT; exec "$@"'` med hengende klient, send SIGTERM når klienten er startet, og kontroller kode 143, tom stdout, én linje på stderr, låsen borte, intet stempel, klienten død; så en vanlig kjøring gjennom samme omslag med kontroll på `note == "startet med SIGTERM oversett"`. Mitt utkast står i `impl_kopi` (`forslag_rettelser.patch`, siste blokk): seks kontroller, +0,5 s, `SELVTEST OK 126 kontroller` på 3.9 og 3.11, også når selvtesten selv startes med signalene oversett (`expM_resultat.txt`). Kontrakten linje 143–161 og `PLAN_VEDLEGG` må da få én linje til om hva selvtesten dekker, og tallet 120 endres.

### Bør 8. Den dokumenterte testkommandoen legger `__pycache__` i `Tests/scheduled/`

**Linjer.** `Docs/ScheduledEvents.md` 240 og 243–244; testenes docstring linje 7.

**Hva som skjer.** `python3 -m unittest discover -s Tests/scheduled -p "test_*.py"` importerer `test_installer` først; dens `.pyc` skrives før dens egen `sys.dont_write_bytecode = True` kjører. Dokumentet anbefaler `-B` bare for enkeltklasser. Briefens egen kommando bruker `-B`.

**Prøvd.** I en ren kopi av `impl/`: den dokumenterte kommandoen (med `-k` som ikke treffer noen test, så bare importen kjører) gir `Tests/scheduled/__pycache__/test_installer.cpython-39.pyc`; med `-B` ingen. De tre `test_installer.*.pyc` som ligger i `impl/Tests/scheduled/__pycache__/` (datert 02.10 23:24 og 03.10 08:12), er fra tidligere kjøringer uten `-B`.

**Hva som bør stå.** `-B` i kommandoen på linje 240 og i docstringen, og den siste setningen (243–244) kan da sløyfes eller gjøres generell.

### Bør 9. «startet med SIGTERM oversett» legges sist i `note` og kan kuttes av `[:300]`

**Linjer.** 848–852.

**Hva som skjer.** Kjøringens egne merknader kommer først (`"; ".join(notes)`), og `store.details` kan alene være over 300 tegn («kunne ikke skrive <id på 120 tegn>: <feiltekst>» per markør). Da forsvinner målingen av arven i akkurat de kjøringene som gikk galt. Legg den først i lista i stedet (`notes = ["startet med SIGTERM oversett"] if _term_was_ignored[0] else []`, deretter `note`). Testen på linje 449 holder fortsatt for en ren kjøring.

## Kontrollert og funnet i orden

- **`_terminate` (1278–1299) kan ikke vranglåse eller kaste.** Den tar ingen lås: ikke `_active_lock` (holdes av hovedtråden i 477–478, 506 og 619 — den var feilen i forrige rapports første utkast), ikke `_final_lock` (kan holdes av vakttråden). `list(_active_groups)` er ett C-kall. `os.killpg` er pakket i `except OSError` (dekker `ProcessLookupError` og `PermissionError`), `lock.release()` fanger `OSError` selv, `os.write` er pakket, `os._exit` kaster ikke. Et signal som kommer mens hovedtråden står i `Lock.acquire()`, `kill_all_clients()`, `write_stamp()`, `MarkerStore.write()`/`remove()`, `Client.close()`/`_kill_group()` eller `_halt_if_fired()`: behandleren kjører i hovedtråden så snart det pågående kallet avbrytes (`sleep`, `select`, `wait`) eller er over (filkallene), gjør sitt og avslutter.
- **Låsfila.** `_current_lock[0]` settes før behandleren installeres (1349–1350) og nulles før den tas bort (1354–1355), så behandleren ser alltid riktig lås eller `None`. En kjøring som fikk «kjører allerede» har `held == False` (428) og `release()` rører ikke andres fil (441); en kjøring som byttet en forlatt lås, eier den nye. Prøvd: `exp4` gir «neste kjøring straks: kode 1, 0 av 1 profil lest» (klienten henger i forsøket) i stedet for «kjører allerede». Resten er Bør 4.
- **Klienten.** Pid-en legges i `_active_groups` rett etter `Popen` (506–507) og tas ut først etter `_kill_group` (619–620), så behandleren dreper den også midt i en lukking. Med `_terminate` som Python-behandler får klienten `SIG_DFL` for SIGTERM over `exec` (testen 517–527 skiller: uten kallet ville barnet overlevd, forrige rapports `exp2`). SIGPIPE nullstilles av `restore_signals`. Igjen etter et signal ligger `.klient-stderr-<pid>-<n>.txt`, og hvis signalet kom midt i en skriving, `.<id>.tmp-<pid>-<tråd>` eller `.<oppgave>.stamp.tmp-…`; `is_leftover` (751–759) kjenner alle tre, og `remove_stale_leftovers` (876, 1020) fjerner dem etter ti minutter. Prøvd i `exp4`: `tilstand etterpå: ['korrespondanse-sjekk.stamp.json']`.
- **Stempel og markører ved signal.** Begge byttes med `os.replace` (337, 406), nye markører skrives før gamle fjernes (960–964), så det som ligger etter et signal er enten forrige eller neste utgave, aldri halvt. Testen 483–484 og `exp_c`: intet stempel etter SIGTERM midt i.
- **To signaler rett etter hverandre.** Pythons behandler kan kjøre nestet: kommer signal nr. 2 mens `_terminate` kjører, kjører en ny `_terminate` inne i den første. Prøvd i `vakt_kopi.py` med `signal.raise_signal(SIGINT)` lagt inn i behandleren (`expJ_dobbeltsignal.txt`): lander nr. 2 før `os.write`, blir det én linje (nr. 2 sin) og kode 130; lander det i den ene bytekoden mellom `os.write` og `os._exit`, blir det to linjer. Klienten drepes og låsen slippes uansett. Et vakt `_terminating`-flagg ville gjort det til nøyaktig én linje; jeg regner det som pynt (se Merknader).
- **Installasjon og tilbakestilling (1302–1342).** Bare i hovedtråden; `previous` har bare det som faktisk ble satt; `restore` setter `SIG_DFL` når `getsignal` ga `None` og fanger `TypeError`. Selvtesten kaller `run_task` flere titalls ganger i samme prosess: `AfterARun` ser `getsignal` identisk før og etter, `_current_lock[0] is None`, `alarm(0) == 0`, ingen `Timer`. De tidlige returene (1362–1367) går gjennom samme `finally` i `run_task`; ingen vakttråd og ingen alarm finnes da. `_term_was_ignored` beregnes på nytt i hver kjøring (1317), og bare for SIGTERM (`expL`). Sammen med SIGALRM: TERM/INT settes i 1350, ALRM i 1158 etter at låsen er tatt; `stop()` slår alarmen av, og `alarm(0) == 0` etter kjøringen.
- **Ikke over 65 sekunder.** Siste utvei står fra `start()` til hovedløpet holder `_final_lock` og er ferdig (1394), eller til vakttråden selv avbestiller den i `_finished`-grenen (1176) etter at hovedløpet var ferdig. Veier der hovedløpet ikke når 1394: `_halt_if_fired()` (vakttråden avslutter), eller et unntak ut av `finally`/`with` — da avslutter tolken (daemon-tråder), se Bør 1. Etter 1394 gjenstår to små skrivinger til rør. Før `watchdog.start()` finnes ingen tidsgrense (`Lock.acquire`), som før.
- **Ingen to sluttlinjer.** Uendret: hovedløpet skriver bare under `_final_lock` etter `_finished.set()`; vakttråden bare etter å ha fått låsen og sett `_finished` usatt. `_terminate` skriver bare til stderr.
- **Ferdig lesing.** `disarm_alarm()` inne i `try` (Bør 1 fra forrige rapport) og `_deadline_seen` rundt `close()` dekker lukkingen; `exp5` og `test_alarm` (1829–1836) viser at en ferdig lesing beholdes. Resten er Bør 2 over.
- **Testene gjør det de sier**, med unntaket i Bør 6, og kan ikke vakle av timing: `test_term_in_the_middle…` venter på at klienten er startet (≤ 20 s) og `communicate(timeout=20)`; `AfterARun` venter inntil 5 s på at tidtakertrådene har avsluttet; `starts.txt` skrives med én liten `write` ved lukking, så en halv pid kan ikke leses. `-B` i `run_snippet` og `command()`, og `sys.dont_write_bytecode` i testmodulen, holder `Scripts/scheduled/` fri for `.pyc`.
- **Dokumentene.** Kontrakten linje 30 og 38 og `ScheduledEvents.md` 148–158 og 209 sier det koden gjør, og `PLAN_VEDLEGG.md` 196–205 beskriver de seks rettelsene riktig. `OperatorRunbook.md` nevner ikke signaler og motsier ingenting; `kickstart -k` i `utfoer` (531–532) er for øvrig den veien et SIGTERM fra launchd ville nådd en kjøring som var i gang, så Bør 3 fra forrige rapport gjelder også installasjonen selv.

## Ikke kontrollert

1. **Premisset på Macen.** Hva Foundation `Process` gjør med signaldisposisjonene over `posix_spawn`, og hvilken tråd XNU velger for et prosessrettet signal (Bør 3). Det første måles av merknaden i stempelet ved første ekte kjøring (og av Bør 7 før installasjon); det andre blir uvesentlig med Bør 3.
2. **macOS `/bin/sh` (bash 3.2) og `trap "" TERM INT; exec`.** Målt her med dash og bash 5.2, begge gir `SIG_IGN` videre. Så vidt jeg kjenner bash-kilden (`reset_or_restore_signal_handlers` i `trap.c` beholder `trap ""`-signaler som `SIG_IGN` og nullstiller bare kommandotraps), har det vært slik lenge, og det er det `trap '' INT; exec cmd`-idiomet bygger på — men 3.2 er ikke prøvd, og Bør 7 ville målt det på Macen før installasjon.
3. **Python 3.9.6.** Målt med 3.9.23. Det nye bruker bare `signal.signal/getsignal`, `os.killpg`, `os._exit`, `os.write` og `threading.main_thread()`, som er uendret gjennom 3.9-rekken; `pthread_sigmask` (Bør 3) finnes fra 3.3.
4. **Pilotklienten.** Om `haven-correspondence-mcp serve` avslutter på SIGTERM, på EOF på stdin eller ved EPIPE — det bestemmer om en klient i Popen-vinduet (Merknad 2) blir foreldreløs. Utdragene sier ingenting om det.
5. **Agentens Swift-kilde** har jeg ikke lest i denne økten (tilgangen ble avslått); linjehenvisningene til `HavenAgentMain.swift` er forrige rapports.
6. **Sannsynlighet i virkelig tid** for vinduene i Bør 1, 2 og 4: vist deterministisk ved å legge signalet akkurat der; ikke målt, og liten.

## Merknader (ikke feil)

1. **Kode 143 etter en ferdig kjøring.** Behandleren står til `restore_signal_handlers` (1355), etter at linjene er skrevet. Et SIGTERM mellom `sys.stdout.write` (1395) og `flush` (1398) kaster den bufrede stdout-linjen (`os._exit` tømmer ikke); mellom `flush` og 1355 gir det kode 143 med linjen skrevet og stempelet på plass. Kontraktens «da skrives ikke stempel» er da unøyaktig i mikrosekunder. Ikke verdt å jage.
2. **Popen-vinduet.** Et signal mens `subprocess.Popen` kjører (noen millisekunder per klientstart), før pid-en er lagt i `_active_groups` (507), gir en klient ingen dreper. Den får EOF på stdin og EPIPE på stdout når programmet dør, og prøveklienten avslutter da; den ekte er «Ikke kontrollert 4».
3. **Nestet behandler** (se «Kontrollert»): et `_terminating`-flagg først i `_terminate` gir nøyaktig én linje og kode fra det første signalet.
4. **`skipTest` etter at halve testen har gått** (451–452): kjøres testene i en prosess som selv har SIGTERM oversett, rapporteres hele `test_term_inherited…` som hoppet over selv om første del passerte. `return` i stedet, eller to tester.
5. **Utenfor hovedtråden.** `install_signal_handlers` returnerer stille `{}`, men `Watchdog.start()` (1158) ville kastet `ValueError` etter at låsen er tatt, og låsen ble stående. Ingen kaller `run_task` fra en annen tråd i dag; blir det aktuelt (trinn 3-tester?), flytt `watchdog.start()` inn i `try` eller sjekk tråden først i `run_task`.
6. **Ctrl-C i selvtesten.** Mens en kjøring går, er SIGINT `_terminate` også i selvtestprosessen: Ctrl-C gir `os._exit(130)` uten at `selftest()` sin `finally` rydder `korrespondansevakt-selvtest-*` i `$TMPDIR`. Mellom kjøringene gir det vanlig `KeyboardInterrupt` med rydding.
7. **Kontrakten sier «det arves av programmene den starter» som faktum** (linje 30), mens merknaden i `note` finnes nettopp for å måle det. «Trolig arves», eller en henvisning til målingen, ville vært mer presist.
8. **`.klient-stderr-*` etter et signal** ryddes etter ti minutter som andre skjulte filer, men verken kontrakten (33) eller dokumentet (229–230) nevner den fila; begge snakker om filer fra «en skriving». Én setning i hver.
