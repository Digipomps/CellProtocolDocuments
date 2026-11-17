# Brief til Fabel: andre etterkontroll av koden for trinn 1 og 2

Dato: 03.10.2026. Du har ikke sett noe av dette før. Gransk som en uavhengig kodegransker.

Alt ligger under `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/` (heretter `S/`). Koden er `S/impl/` (se `S/pdd-cron/panel/BRIEF_KODE_TRINN1-2.md` for hva filene er, og kontrakten `S/pdd-cron/contract/trinn1-2-programmer.md`).

## Hva som skal granskes

To ting er endret i `S/impl/Scripts/scheduled/korrespondanse_vakt.py` etter at koden sist ble gransket, og ingen av dem er sett på av andre enn den som skrev dem.

**A. Tre rettelser fra forrige etterkontroll.** Rapporten `S/pdd-cron/panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL.md` fant tre nye ting, og sporingen står nederst i `S/pdd-cron/PLAN_VEDLEGG.md` (avsnittet om etterkontrollen av koden). Rettelsene gjelder vakttråden (`Watchdog`: `_fired`, `_finished`, `_final_lock`, `last_resort`, `stop()`, `_halt_if_fired()`), alarmen (`_alarm_armed`, `disarm_alarm()`) og årsvinduet 2000–2999 for tidsstempler. Utgaven fra før rettelsene finnes ikke lenger, så les koden som den står og vurder om de tre funnene er lukket og om rettelsene har åpnet noe nytt.

**B. Arvede signaler.** Planleggeren som starter programmet (`haven-agentd schedule-worker`) setter `signal(SIGTERM, SIG_IGN)` og `signal(SIGINT, SIG_IGN)` i sin egen prosess (`AgentMonitorShutdown` i `/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/Sources/HavenAgentD/HavenAgentMain.swift`, omkring linje 1166). Et signal som overses, arves over `exec`. Programmet har derfor fått `reset_inherited_signals()`, som kalles først i `run_task`, og tre tester i klassen `InheritedSignals` i `S/impl/Tests/scheduled/test_korrespondanse_vakt.py`. Utgaven fra før denne endringen ligger i `S/work/korrespondanse_vakt.py.foer-signalretting` og `S/work/test_korrespondanse_vakt.py.foer-signalretting`, så du kan se forskjellen med `diff`.

## Det jeg ber om

1. Er de tre funnene fra etterkontrollen lukket? Finnes det fortsatt en vei der programmet skriver to sluttlinjer, bruker mer enn 65 sekunder, eller der et sent signal treffer skrivingen av markører og stempel?
2. Er `reset_inherited_signals()` riktig og trygg: i hovedtråden og utenfor, sammen med `signal.alarm`/SIGALRM og vakttråden, når programmet kjøres fra en terminal (Ctrl-C), og når selvtesten kaller `run_task` mange ganger i samme prosess? Endrer den noe for et program som ikke har arvet oversette signaler? Hva skjer med låsfila og stempelet når programmet nå kan drepes av SIGTERM midt i en kjøring, og tåler neste kjøring det?
3. Prøver de tre nye testene det de sier, på Python 3.9 og på macOS (`/usr/bin/python3` 3.9.6)?
4. Noe annet du ser i de berørte delene.

Testene kjøres slik (36 tester, omtrent fem minutter per kjøring; selvtesten 120 kontroller):

```
cd S/impl && /root/.local/bin/python3.9 -m unittest discover -s Tests/scheduled -p "test_*.py"
/root/.local/bin/python3.9 S/impl/Scripts/scheduled/korrespondanse_vakt.py selvtest
```

De var grønne på 3.9.23, 3.11.15 og 3.13.13 i dag. Kjør gjerne enkelttester og egne forsøk mot en kopi.

## Slik svarer du

Skriv til `S/pdd-cron/panel/FABEL_KODE_TRINN1-2_ETTERKONTROLL2.md`, på norsk: **Må rettes før installasjon**, **Bør rettes**, **Kontrollert og funnet i orden**, **Ikke kontrollert**. Vis til linjer, og vis hvordan du har prøvd det du påstår.

Grenser: du kan lese alt som er nevnt, og kjøre programmet og testene. Egne filer legger du i `S/fabel-trinn1-2/` (lag mappen; kopier dit det du vil endre på for å prøve). Du skal ikke endre noe i `S/impl/`, `S/koe/`, `S/trinn3/` eller `S/pdd-cron/` utenom rapportfila. Ingen verktøy som når Macen, nettlesere, korrespondanse eller andre tjenester, ingen nedlasting fra nettet, og ingen meldinger til noen. Ingen private detaljer fra `S/pdd-cron/panel/kilder-utdrag/` i rapporten.

Svaret ditt til meg skal være kortversjonen: hvert «må rettes» på én linje, og antallet «bør rettes».
