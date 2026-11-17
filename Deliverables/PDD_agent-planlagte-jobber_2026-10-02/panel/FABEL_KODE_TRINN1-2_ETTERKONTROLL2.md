# Fabel: andre etterkontroll av koden for trinn 1 og 2 (vakttråd, alarm, årsvindu, arvede signaler)

Dato: 03.10.2026. Gransket som uavhengig kodegransker, uten å ha sett koden før. Linjenumre uten filnavn viser til `impl/Scripts/scheduled/korrespondanse_vakt.py` (md5 `119779a9…`, uendret under granskingen); «testene» er `impl/Tests/scheduled/test_korrespondanse_vakt.py`. Forsøkene mine ligger i `scratchpad/fabel-trinn1-2/` (`exp1_…` til `exp8_…`, og kopiene `vakt_kopi_*.py` med rettelsene jeg foreslår). Alt er målt her, på Linux med Python 3.9.23 (og 3.11.15 der det står); det som bare gjelder macOS og 3.9.6, står under «Ikke kontrollert».

**Testene.** Hele mengden på 3.9: `Ran 36 tests in 274.993s — OK` (`fabel-trinn1-2/suite-3.9.txt`; kjørt mens forsøkene mine gikk ved siden av, også `ProductionLimits` holdt). De seks nye testene alene (`WatchdogOrdering`, `InheritedSignals`): OK på 3.9 og 3.11, 0,6 s. Selvtesten: `SELVTEST OK 120 kontroller`, 13,8 s (kopiene med rettelsene mine: 13,7–13,8 s); kjørt inne i en prosess jeg styrte, som kontroll: 120 kontroller, ingen feil, én tråd igjen etterpå, `signal.alarm(0)` gir 0, `_alarm_armed` falsk, `_fired` falsk. Ingen `.pyc` ble lagt i `impl/` av testene slik de er dokumentert; de to `.pyc`-filene mine egne enkeltkjøringer la der, har jeg fjernet (se merknad 3).

## Må rettes før installasjon

Ingen. Jeg finner ingen vei som henger planleggeren, gir to sluttlinjer eller gir feil sak under forhold som kan oppstå på en Mac med lokalt filsystem. Det som er igjen, står under «Bør rettes»: to er restene av funn 1 og 2 fra forrige etterkontroll (smalere enn før, men ikke lukket; Bør 1–2), to gjelder følgene av at programmet nå kan drepes av SIGTERM og SIGINT (Bør 3–4), og to gjelder testene og kontrakten (Bør 5–6).

## Status for de tre funnene fra forrige etterkontroll

| # | Funn | Nå | Rest |
|---|---|---|---|
| 1 | `stop()` avbestilte siste utvei mens vakttråden kunne være i gang; to linjer mulig | **Lukket for det som kan skje i praksis.** `_fired` settes før låsen (1166), `stop()` lar siste utvei stå når `_fired` er satt (1161–1163), og en vakttråd som får låsen etter at hovedløpet er ferdig, rører ingenting (1169–1174, `_finished` settes under låsen i 1321). To linjer er ikke lenger mulig: den som har `_final_lock`, gjør seg ferdig, den andre sover (1315) eller ser `_finished`. | Sjekken i `stop()` (1161) og låsen i `run_task` (1319) er to steg: setter vakttråden `_fired` mellom dem og står så fast i `write_stamp`, er siste utvei avbestilt og ingen avslutter. Krever at tidtakeren går i akkurat dette vinduet **og** at filsystemet henger. Vist i `exp6`. Se Bør 2. |
| 2 | `signal.alarm(0)` stoppet ikke en behandler som alt var på vei | **Lukket for skrivingen.** `_raise_deadline` kaster bare når `_alarm_armed` er sant (1123–1126), og `disarm_alarm()` (124–126) setter flagget falskt før `alarm(0)`. Når markører og stempel skrives, kan ikke `Deadline` lenger komme. | Flagget settes falskt *inne i* `disarm_alarm()`, og kallet står utenfor `try` (894). Et signal som alt er notert når `disarm_alarm()` begynner, kaster `Deadline` før flagget er lagret, og det fanges ikke: kjøringen ender som «avbrutt av tidsgrensen» uten stempel og markører, selv om lesingen var ferdig. Vinduet er noen få bytekoder. Vist i `exp5`. Se Bør 1. |
| 3 | Årstallsvinduet sto bare i koden | **Lukket.** Kontrakten linje 45 og `Docs/ScheduledEvents.md` 218–220 sier det samme som koden (171–173), og selvtesten prøver `9999-…` og `1999-…` (1862–1868). | — |

## Bør rettes

### Bør 1. `disarm_alarm()` må stå inne i `try`, så det første `Deadline` alltid fanges

**Linjer.** 879–894 i `run_sjekk`: `try … except Deadline` dekker løkken (880–886), men `disarm_alarm()` kommer etter `except`-blokken (894).

**Hva som skjer.** Kommer SIGALRM i mikrosekundene før `_alarm_armed[0] = False` (125) lagres, kjører behandleren ved neste bytekode med flagget fortsatt sant, og `Deadline` kastes utenfor `try`. `run_task` fanger den (1306–1307): kode 1, «avbrutt av tidsgrensen», ingen markører, ingen stempel; en profil som var lest, er tapt for denne kjøringen. Kontrakten linje 27 holder for *skrivingen* (den avbrytes ikke), men «skriver markører og stempel som vanlig» holder ikke i dette vinduet.

**Prøvd.** `exp5_alarm_restvindu.py` bytter `disarm_alarm` med en som først gjør `signal.raise_signal(SIGALRM)` (leverer signalet synkront, akkurat der) og så det vanlige. Mot koden som den står: `kode 1`, `korrespondanse-sjekk: avbrutt av tidsgrensen`, `stempel finnes: False`, `markører: []`. Mot kopien `vakt_kopi_alarmfix.py`: `kode 0`, «1 profil lest, 1 avsender med ulest post», stempel og markør skrevet. Kopien: `SELVTEST OK 120 kontroller`.

**Hva som bør stå.** Flytt kallet inn i `try` etter løkken, og kall det også først i `except Deadline`:

```python
    try:
        for profile in order:
            ...
        disarm_alarm()            # inne i try: et Deadline som kastes her, fanges under
    except Deadline:
        disarm_alarm()            # behandleren kaster bare én gang per arming, så her kommer ikke et nytt
        interrupted = True
        ...
```

Resonnementet: `_raise_deadline` setter flagget falskt før den kaster, så det kan komme høyst ett `Deadline` per arming. Står alt som kan utløse det første inne i `try`, er resten trygt. `run_frist` (1015) trenger ingen endring: alarmen kan ikke gå noen millisekunder etter start.

### Bør 2. Siste utvei bør avbestilles der hovedløpet holder `_final_lock`, ikke i `stop()`

**Linjer.** 1158–1163 (`stop()` avbestiller `last_resort` når `_fired` ikke er satt), 1166 (`_fired.set()` i `fire()`), 1314–1319 (`finally` og `with _final_lock`).

**Hva som skjer.** Vinduet mellom sjekken i 1161 og låsen i 1319 inneholder `kill_all_clients()` og `lock.release()` (et `os.remove`). Setter vakttråden `_fired` der, tar den `_final_lock` og begynner på stempelet; hovedløpet har alt avbestilt siste utvei og blokkerer på `with _final_lock` uten tidsgrense. Står vakttråden fast i `read_stamp`/`write_stamp` (1177, 1183), er det ingen igjen som avslutter: akkurat det siste utvei skulle hindre. Det er restkappløpet fra forrige funn 1, smalnet til dette vinduet, og det samme skjer i rettelsen jeg selv foreslo da. Det krever et filsystem som står (da ville `lock.release()` også vært tregt, som er nettopp det som åpner vinduet), så på lokal APFS er det teori. Men det er billig å lukke helt.

**Prøvd.** `exp6_stop_restvindu.py` bruker programmets egne `Watchdog.stop()` og `fire()`, bytter `_fired` med en Event som slipper vakttråden løs første gang `stop()` spør `is_set()`, og bytter `write_stamp` med en som står. Mot koden: `siste utvei avbestilt: True`, `hovedløpet fikk _final_lock innen 3 s: False` → «INGEN avslutter». Mot kopien `vakt_kopi_lastresort.py`: `siste utvei avbestilt: False` → «siste utvei står: prosessen ville avsluttet etter 65 s» (3605 s med forsøkets grenser). Kopien: `SELVTEST OK 120 kontroller`.

**Hva som bør stå.** `stop()` avbestiller bare `timer` og slår av alarmen. Hovedløpet avbestiller siste utvei først når det holder låsen og er ferdig:

```python
    with _final_lock:
        _finished.set()
        watchdog.last_resort.cancel()   # før skrivingen, så et unntak i skrivingen ikke lar den stå i testprosessen
        sys.stdout.write(...)
```

Da står siste utvei i alle veier der vakttråden har eller kan få låsen, og den avbestilles i alle veier der hovedløpet blir ferdig. Sjekken `if not _fired.is_set()` i `stop()` kan tas bort, og `fire()` sin egen avbestilling (1171) blir overflødig men ufarlig. Testen `test_stop_keeps_the_last_resort_when_the_watchdog_has_fired` (371–389) fester dagens oppførsel og må skrives om til den nye: «`stop()` lar siste utvei stå; sluttblokken i `run_task` avbestiller den».

### Bør 3. Når SIGTERM nå virker, bør programmet avslutte ordnet: drepe klienten, slippe låsen, én linje

**Linjer.** 1265–1281 (`reset_inherited_signals`), 1286 (kallet), 1288–1297 (låsen tas før vakttråden starter), 712 (`start_new_session=True`).

**Hva som skjer.** Før endringen overså programmet et arvet SIGTERM og ble ferdig (stempel, markører, én linje). Nå dør det på stedet, uten `finally`: låsfila står (regnes som forlatt etter ti minutter, 427), klientens stderr-fil står (ryddes etter ti minutter, 762–776), og klienten står — den lever i egen sesjon (712), så verken planleggerens prosessgruppe eller en terminal når den; bare programmet dreper den. Stempelet er det forrige (det skrives sist, atomisk), markørene er urørte eller delvis oppdaterte (hver skriving er atomisk, nye skrives før gamle fjernes). Neste kjøring innen ti minutter sier «kjører allerede» med kode 0 og rører ingenting; neste etter det går som vanlig. Så: neste kjøring tåler det, men med en ti minutters skygge og en klient som ingen tar.

Hvem sender SIGTERM? Planleggeren selv gjør det ikke: `ScheduledEventService.stop()` (185–190) venter på arbeideren, som venter på prosessen (`FoundationProcessRunner.run` har ingen avbryting, SubprocessRunner.swift 51–79), så en ordnet stopp av planleggeren venter på barnet. SIGTERM kommer fra en operatør (`kill`), eller fra launchd mot prosessgruppen når planleggeren dør mens et program kjører (se «Ikke kontrollert», punkt 2). Installasjonen venter selv i inntil 60 s på en hendelse som kjører før `kickstart -k` (installer 465–472).

**Prøvd.** `exp4_sigterm_midt_i.py` starter programmet gjennom `sh -c 'trap "" TERM INT; exec python …'` (så det arver SIG_IGN, som fra planleggeren), sender SIGTERM etter 3 s. Ny utgave: `avsluttet med -15 etter 3.0 s`, stdout og stderr tomme, `tilstand: ['.klient-stderr-…', 'korrespondanse-sjekk.lock']`, `klienter som lever: ['17950']`; «neste kjøring straks: kode 0, kjører allerede, stempel finnes: False»; med låsen ti minutter gammel: kode 0, «1 profil lest, 1 avsender med ulest post», restene ryddet. Utgaven før (`work/…foer-signalretting`): overså signalet, `avsluttet med 1 etter 26.1 s` med stempel. Kopien `vakt_kopi_sigterm.py` med behandleren under: `avsluttet med 143 etter 3.0 s`, én linje på stderr, låsen borte, klienten drept, bare stderr-fila igjen; `SELVTEST OK 120 kontroller`.

**Hva som bør stå.** En SIGTERM-behandler i `run_task` (hovedtråden), som verken skriver stempel eller markører:

```python
_current_lock = [None]

def _terminate(signum, frame):
    for group in list(_active_groups):     # ikke ta _active_lock her: hovedtråden kan holde den akkurat nå
        try:
            os.killpg(group, signal.SIGKILL)
        except OSError:
            pass
    if _current_lock[0] is not None:
        _current_lock[0].release()
    try:
        os.write(2, ("korrespondanse_vakt.py: avbrutt av signal %d\n" % signum).encode("utf-8"))
    except OSError:
        pass
    os._exit(128 + signum)
```

Behandleren kjører mellom to bytekoder i hovedtråden. Den må derfor ikke kalle `kill_all_clients()` (476–483), som tar `_active_lock`: holder hovedtråden den akkurat da (506, 619), vranglåser prosessen. Min første kopi gjorde nettopp det; den endelige leser mengden uten lås. `os.replace` gjør at et avbrutt stempel eller en avbrutt markør ikke kan bli halvskrevet.

### Bør 4. Tilbakestillingen bør avgrenses til formålet: SIGTERM. SIGINT og SIGHUP har ingen begrunnelse og én ulempe hver

**Linjer.** 1275–1276 (de tre signalene), docstring 1266–1271 («så klienten … kan stoppes med SIGTERM»), `Docs/ScheduledEvents.md` 148–151.

**SIGINT.** Planleggeren overser SIGINT for å kunne stoppe pent på Ctrl-C i en terminal (HavenAgentMain.swift 1164–1179). Kjøres den i forgrunnen, går Ctrl-C til hele forgrunnsgruppen, altså også til programmet (så langt jeg vet bytter Foundation `Process` ikke prosessgruppe; det er ikke målt) — men ikke til klienten, som har egen sesjon. Før endringen overså programmet Ctrl-C og ble ferdig mens planleggeren ventet (`stop()` venter, 189); kjøringen fikk stempel og én linje. Nå får hovedtråden `KeyboardInterrupt`: `finally` rydder (klienten drepes, låsen slippes), men ingen stempel, og **20 linjer traceback på stderr**, mot kontraktens «høyst én» (linje 29). Planleggeren leser utdataene når barnet er ferdig og legger dem i `lastError`. `exp7_sigint.py` viser begge: ny `avsluttet med -2 etter 3.0 s`, `stderr (20 linjer)`, `tilstand: []`, klienten drept; gammel `avsluttet med 1 etter 26.1 s`, én linje, stempel. Enten tas SIGINT ut av lista (da er oppførselen som før, og den var god), eller `run_task` fanger `KeyboardInterrupt` som `Deadline` (én linje, ingen traceback), eller behandleren i Bør 3 brukes også for SIGINT.

**SIGHUP.** Planleggeren overser ikke SIGHUP, så det arves aldri som oversett fra den. Det eneste som gir et arvet, oversett SIGHUP i praksis, er `nohup` — og da gjør programmet om det brukeren ba om. `exp1` viser at HUP settes fra SIG_IGN til SIG_DFL. Ta det ut, eller skriv hvorfor det skal stå.

**Hva som gjelder uansett.** Et program som ikke har arvet oversette signaler, endres ikke (`exp1`, kontrollkjøringen uten `trap`: alt likt før og etter), og et nytt kall endrer ingenting (`igjen:`-linjen).

### Bør 5. Testene prøver ikke arven over `exec`, som er den veien planleggeren bruker

**Linjer.** Testene 408–416 og 427–437 setter SIG_IGN *fra Python i samme prosess* og kaller så funksjonen. Navnet `test_signals_inherited_as_ignored_are_set_back` lover mer: arven over `exec` (planleggeren → `posix_spawn`/`exec` → Python) prøves ikke. Den virker (målt i `exp1_arv_over_exec.py` på 3.9 og 3.11: `sh -c 'trap "" TERM INT HUP; exec python …'` gir `foer: TERM=SIG_IGN HUP=SIG_IGN INT=SIG_IGN`, `etter: SIG_DFL SIG_DFL default_int_handler`), fordi CPython ved oppstart fører et arvet SIG_IGN inn i `getsignal` som `SIG_IGN` (og lar SIGINT være oversett, mot sin vane). Men det er det testen burde feste, med `/bin/sh -c 'trap "" TERM INT HUP; exec …'` rundt utdraget — det går like godt på Macens `/bin/sh`. `preexec_fn` er ikke et alternativ: programmet har tråder når det starter klienten.

Den tredje testen har skillekraft: `exp2_test3_skillekraft.py` kjører samme utdrag uten kallet, og barnet lever etter 3 s («det overser SIGTERM»); med kallet dør det straks med −15. Den andre testen er rett fram. Alle tre gjør det de sier på 3.9 her; det macOS-spesifikke står under «Ikke kontrollert».

### Bør 6. Kontrakten mangler setningen om signalene

`Docs/ScheduledEvents.md` 148–151 beskriver tilbakestillingen; `pdd-cron/contract/trinn1-2-programmer.md` (tabellen 25–35, og linje 28 om barneprosesser) sier ingenting om den, og `PLAN_VEDLEGG.md` heller ikke. Kontrakten er den ene lista; legg inn én linje der (og rett den etter utfallet av Bør 4), så dokumentene sier det samme.

## Kontrollert og funnet i orden

- **Ingen to sluttlinjer.** Den eneste linjen hovedløpet skriver, skrives under `_final_lock` (1319–1326) etter at `_finished` er satt; vakttråden skriver sin bare etter å ha fått låsen og sett at `_finished` ikke er satt (1167–1174, 1191). Sover hovedløpet i `_halt_if_fired()` (1315), skriver det aldri. Ingen buffret stdout fra før finnes (bare «ikke kjørt»/«kjører allerede», som returnerer før vakttråden starter). Null linjer er mulig når vakttråden ikke får låsen på to sekunder (1167–1168) — bare om hovedløpet holder låsen over to sekunder for to korte skrivinger til rør; ikke et heng. `exp8_kapplop_sluttlinje.py`: 200 kjøringer med vakttiden spredt fra 30 % til 150 % av `run_task`-tiden (28 ms), 83 ganger kode 0 og 117 ganger kode 3, alltid nøyaktig én linje, aldri over én på stderr. Samme forsøk mot utgaven før første kodegransking (uten lås) ga heller ingen dobbel linje, så forsøket er en kontroll, ikke et bevis; beviset er låsen.
- **Ikke over 65 sekunder.** Siste utvei står i alle veier der vakttråden kan ha låsen, utenom restvinduet i Bør 2. Et SIGALRM som eventuelt leveres til en tidtakertråd og ikke vekker hovedtråden fra `select` (hovedtråden merker det først ved neste bytekode, inntil 12 s senere), dekkes av vakttråden ved 60 s: utfallet blir kode 3 i stedet for kode 1, ikke et heng. Før `watchdog.start()` (1299) finnes ingen tidsgrense (`Lock.acquire`, 417–438), som før; det krever at et lokalt filsystem henger.
- **Et sent signal treffer ikke skrivingen.** Når flagget er falskt, kaster ikke behandleren, og alle skrivinger skjer etter `disarm_alarm()`. Resten (Bør 1) ligger *før* skrivingen begynner, ikke i den.
- **`reset_inherited_signals()` i seg selv.** Bare hovedtråden (1273–1274); bare signaler som er `SIG_IGN` (1278); `OSError`/`ValueError` fanges; idempotent; kalles før låsen og vakttråden, så ingen tråd finnes ennå; rører ikke SIGALRM; `start()` setter SIGALRM-behandleren for hver kjøring (1152). Selvtesten kaller `run_task` flere titalls ganger i samme prosess uten rester (målt: én tråd, alarm 0). Sammenlikningen `getsignal(n) == signal.SIG_IGN` virker både når SIG_IGN er satt fra Python og når det er arvet (3.9 gir `Handlers.SIG_IGN`, 3.11 gir `1`; begge er lik `signal.SIG_IGN`).
- **Hvorfor tilbakestillingen er riktig for klienten.** `Client` bruker `close_fds=True`, `cwd` og `start_new_session=True` (499–501), så 3.9 går via `fork_exec`, der `restore_signals` bare nullstiller SIGPIPE/SIGXFZ/SIGXFSZ; et arvet SIG_IGN for SIGTERM går videre til klienten. En hengende klient som overser SIGTERM, koster ett sekund per lukking i `_kill_group` (457–465). `exp3_term_ignorert_budsjett.py`: to hengende profiler med de ekte grensene og en klient som overser SIGTERM tar **52,08 s** (mot 50,09 s målt uten, forrige etterkontroll): ett sekund per profil, fordi det andre forsøket kappes av profilens frist. Fortsatt under alarmen på 55 s, men marginen er 3 s i stedet for 5. Med tilbakestillingen får klienten SIG_DFL (en Python-behandler blir SIG_DFL over `exec`, SIG_IGN ville blitt med).
- **Premisset i briefen stemmer i kilden.** `AgentMonitorShutdown.init` setter `signal(SIGINT/SIGTERM, SIG_IGN)` (HavenAgentMain.swift 1171–1173) og brukes av `schedule-worker` (347). Hva Foundation `Process` gjør med det over `posix_spawn`, står under «Ikke kontrollert».
- **De tre nye vakttråd-/alarmtestene** (346–389) prøver det de sier: en sen vakttråd rører ingenting og rydder flaggene; behandleren kaster bare når armert, og bare én gang; `stop()` lar siste utvei stå når `_fired` er satt og avbestiller ellers. De rydder etter seg (tidtakere og alarm). Den siste må skrives om hvis Bør 2 tas (se der).
- **Årsvinduet** (funn 3): kontrakt, dokumentasjon, kode og selvtest sier det samme.
- **`fire()` ellers.** `kill_all_clients()` før stempelet; `self.lock.release()` er ufarlig når hovedløpet alt har slippet (`held`, 441); `os.write(1, …)` på under hundre byte kan ikke blokkere på et tomt rør; `os._exit(3)` i `finally` kommer alltid.

## Ikke kontrollert

1. **Om premisset holder på Macen.** Planleggeren starter programmet med Foundation `Process` (`posix_spawn`). Jeg vet ikke om Apples implementasjon setter signalbehandlingen tilbake til standard i barnet (`POSIX_SPAWN_SETSIGDEF`); gjør den det, arves ingenting, og `reset_inherited_signals()` gjør ingenting — ufarlig begge veier. Det kan måles i tørrkjøringen eller i første kjøring: la `reset_inherited_signals()` returnere hva den satte tilbake, og før det i stempelets `note` («arvet oversett: SIGTERM, SIGINT») — da er premisset målt der det gjelder, uten egen agentkode.
2. **Hva launchd gjør med prosessgruppen** når planleggeren dør mens et program kjører (etter `ExitTimeOut`, eller ved krasj). Jeg mener launchd sender SIGTERM til resten av gruppen når `AbandonProcessGroup` ikke er satt; det er dette som ville gjort Bør 3 aktuelt oftere enn ved et manuelt `kill`. Klienten i egen sesjon nås uansett ikke av det.
3. **Pilotklienten.** Om `haven-correspondence-mcp serve` selv overser SIGTERM (da gjelder målingen i `exp3`, 52 s, også etter rettelsen), og om den avslutter når stdin lukkes eller ved første skriving til et lukket rør (da løser den foreldreløse klienten i Bør 3 seg selv). Utdragene i `panel/kilder-utdrag/` sier ingenting om signaler.
4. **Python 3.9.6 på macOS.** Målt med 3.9.23 her; `signal`-modulens oppstartslogikk (arvet SIG_IGN → `getsignal` gir SIG_IGN; SIGINT-behandleren settes bare når SIGINT er SIG_DFL) er den samme i hele 3.9-rekken. `fork_exec`-veien for klienten gjelder også på macOS (3.9 bruker `posix_spawn` bare uten `close_fds`, `cwd` og `start_new_session`). Hvilken tråd XNU leverer et prosessrettet SIGALRM til: etter kilden den første tråden i listen som ikke blokkerer det, altså hovedtråden, som på Linux; vil man ta det helt bort, kan `start()` blokkere SIGALRM med `pthread_sigmask` rundt `timer.start()`/`last_resort.start()`, så tidtakertrådene arver masken.
5. **Vinduet i Bør 1 og Bør 2 i virkelig tid.** Begge er vist deterministisk ved å legge signalet eller tråden akkurat der; sannsynligheten for å treffe dem ved 55 og 60 sekunder på en Mac er ikke målt, og er liten.

## Merknader (ikke feil)

1. Kommer vakttråden *etter* at hovedløpet har skrevet markører og stempel, men før sluttblokken (kappløpet forrige rapport kalte C2a), ser `fire()` at `_finished` ikke er satt (1169) og skriver stempelet på nytt med kode 3, «failed» og `consecutiveFailures` + 1 for alle profiler (1177–1185), mens markørene står. Dette er lest ut av koden, ikke målt særskilt (`exp8` teller bare linjer og koder). Det er som forrige etterkontroll godtok: en kjøring som varer til 60 s har alt hatt alarm ved 55 s, så det krever fem sekunders filarbeid.
2. Docstringen til `Watchdog` (1130–1134) og kommentaren i `stop()` (1162) beskriver hensikten riktig, men gjennomføringen er den i Bør 2.
3. Kjøres ett testmodul eller én klasse direkte fra `Tests/scheduled` (`python3 -m unittest test_korrespondanse_vakt.InheritedSignals`), legges `__pycache__/test_korrespondanse_vakt.*.pyc` der: modulens eget `sys.dont_write_bytecode = True` (25) kommer etter at modulen selv er kompilert. Den dokumenterte `discover`-kommandoen slipper unna fordi `test_installer` lastes først og setter flagget. Bruk `python3 -B` ved enkeltkjøringer, eller sett flagget i `__init__`/en `conftest`-liknende fil. Jeg har fjernet de to filene mine kjøringer laget (`cpython-39`, `cpython-311`) og `Scripts/scheduled/__pycache__/korrespondanse_vakt.cpython-39.pyc`, som en av mine egne drivere laget (ikke testene); `impl/` er som før granskingen.
