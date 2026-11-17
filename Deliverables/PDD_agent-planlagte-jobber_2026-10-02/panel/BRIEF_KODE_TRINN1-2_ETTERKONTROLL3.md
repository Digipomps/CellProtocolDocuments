# Brief til Fabel: tredje etterkontroll av koden for trinn 1 og 2 (signaler, alarm, siste utvei)

Dato: 03.10.2026. Du har ikke sett dette før. Gransk som uavhengig kodegransker, og ta ikke mine konklusjoner for gitt.

Alt ligger under `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/` (heretter `S/`). Koden er `S/impl/` (hva filene er, står i `S/pdd-cron/panel/BRIEF_KODE_TRINN1-2.md`; kontrakten er `S/pdd-cron/contract/trinn1-2-programmer.md`).

## Bakgrunn

Forrige etterkontroll ga rapporten `S/pdd-cron/panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL2.md`: ingenting som måtte rettes, og seks ting som burde. Alle seks er tatt inn i `S/impl/Scripts/scheduled/korrespondanse_vakt.py` og `S/impl/Tests/scheduled/test_korrespondanse_vakt.py`. Hva som ble gjort med hvert punkt, står i tabellen etter «Disse tre rettelsene ble gransket av Fabel 03.10» i `S/pdd-cron/PLAN_VEDLEGG.md`. Utgavene fra før disse rettelsene ligger i `S/work/korrespondanse_vakt.py.foer-etterkontroll2` og `S/work/test_korrespondanse_vakt.py.foer-etterkontroll2`, så du kan se nøyaktig hva som er endret med `diff -u`.

Det nye i koden:

- `disarm_alarm()` står inne i `try` i `run_sjekk`, og kalles igjen der `Deadline` fanges.
- Siste utvei (`Watchdog.last_resort`) avbestilles ikke lenger i `stop()`, men i sluttblokken i `_run_with_lock`, etter `_finished.set()` og mens `_final_lock` holdes.
- `install_signal_handlers()` og `restore_signal_handlers()` rundt hele `run_task`, behandleren `_terminate`, `_current_lock` og `_term_was_ignored`. SIGTERM tas alltid over mens en kjøring varer; SIGINT bare når det ikke er oversett; SIGHUP røres ikke. `build_stamp` fører «startet med SIGTERM oversett» i `note`.
- Testklassene `Signals` og `AfterARun`, og den omskrevne `test_stop_leaves_the_last_resort_standing`.

Bakgrunnen for signalene: planleggeren som starter programmet, setter `signal(SIGTERM, SIG_IGN)` og `signal(SIGINT, SIG_IGN)` i sin egen prosess (`AgentMonitorShutdown` i `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/Sources/HavenAgentD/HavenAgentMain.swift`, omkring linje 1166), og et oversett signal arves over `exec`. En senere utgave av planleggeren (trinn 3) starter programmet i egen prosessgruppe med vanlig signalbehandling, og sender SIGTERM til gruppen når tidsgrensen er nådd, eller når planleggeren selv blir bedt om å stoppe.

## Det jeg ber om

1. **Er de seks punktene lukket**, og gjort riktig?
2. **`_terminate`.** Den kjører som signalbehandler i hovedtråden. Kan den vranglåse, kaste, etterlate låsfila, etterlate en klient, eller skrive mer enn én linje? Hva om signalet kommer mens `Lock.acquire()` holder på, mens vakttråden holder `_final_lock`, mens markører eller stempel skrives, mens `kill_all_clients()` går, eller to signaler rett etter hverandre? Hva om låsen i `_current_lock` tilhører en kjøring som fikk «kjører allerede» (kan den da slette en annen kjørings låsfil)? Hva etterlates i tilstandsmappen, og rydder neste kjøring det?
3. **Installasjon og tilbakestilling av behandlerne.** Riktig i hovedtråden og utenfor, når selvtesten kaller `run_task` mange ganger, når `run_task` returnerer tidlig («ikke kjørt», «kjører allerede»), og sammen med SIGALRM og vakttråden? Arver klienten det den skal?
4. **Alarmen og siste utvei.** Finnes det fortsatt en vei der programmet skriver to sluttlinjer, bruker mer enn 65 sekunder, mister en ferdig lesing, eller lar en tidtaker stå igjen etter en kjøring som ble ferdig (også når kjøringen ender med unntak, eller i de tidlige returene)?
5. **Testene.** Prøver de nye testene det de sier, på Python 3.9, og vil de gjøre det på macOS (`/bin/sh`, `/usr/bin/python3` 3.9.6)? Kan noen vakle? Mangler det noe?
6. **Kontrakten og dokumentet** (`S/pdd-cron/contract/trinn1-2-programmer.md`, `S/impl/Docs/ScheduledEvents.md`): sier de det koden gjør?

Testene kjøres slik (39 tester, omtrent fem minutter for hele mengden; selvtesten 120 kontroller på et kvart minutt):

```
cd S/impl && /root/.local/bin/python3.9 -B -m unittest discover -s Tests/scheduled -p "test_*.py"
/root/.local/bin/python3.9 -B S/impl/Scripts/scheduled/korrespondanse_vakt.py selvtest
```

De var grønne på 3.9.23, 3.11.15 og 3.13.13 i dag. Kjør heller enkelttester og egne forsøk mot en kopi enn hele mengden mange ganger, og bruk alltid `-B`.

## Slik svarer du

Skriv til `S/pdd-cron/panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL3.md`, på norsk: en tabell over de seks punktene med «lukket», «delvis» eller «ikke lukket» og hvordan du prøvde det; deretter **Nye funn som må rettes før installasjon**, **Nye funn som bør rettes**, **Kontrollert og funnet i orden**, **Ikke kontrollert**. Vis til linjer, og vis hvordan du har prøvd det du påstår.

Grenser: du kan lese alt som er nevnt, og kjøre programmet og testene. Egne filer legger du i `S/fabel-trinn1-2-etterkontroll3/` (lag mappen; kopier dit det du vil endre på for å prøve). Du skal ikke endre eller slette noe i `S/impl/`, `S/koe/`, `S/trinn3/`, `S/work/` eller `S/pdd-cron/` utenom rapportfila. Ingen verktøy som når Macen, nettlesere, korrespondanse eller andre tjenester, ingen nedlasting fra nettet, og ingen meldinger til noen. Ingen private detaljer fra `S/pdd-cron/panel/kilder-utdrag/` i rapporten.

Svaret ditt til meg skal være kortversjonen: status for de seks punktene, hvert nytt «må rettes» på én linje med fil og linje, og antallet nye «bør rettes» med stikkord.
