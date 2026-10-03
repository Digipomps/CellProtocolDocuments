# Brief til Fabel: gransk koden for trinn 3 (cron og planleggeren)

Dato: 03.10.2026. Koden for trinn 3 er skrevet og testet i skyen mens G2 venter. Ingenting er lagt på Macen eller i noe repo. Gransk den som en uavhengig kodegransker før den legges fram. Du har ikke sett noe av dette før, og du skal ikke ta mine konklusjoner for gitt.

Alt ligger under `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/` (heretter `S/`).

## Hva som finnes

`S/trinn3/` har filene slik de skal ligge i repoet HavenAgentD:

| Fil | Hva |
|---|---|
| `Sources/HavenAgentRuntime/CronSchedule.swift` | ny: cron-uttrykk i en navngitt tidssone |
| `Sources/HavenMacAutomation/BoundedProcessRunner.swift` | ny: kjører én kommando i egen prosessgruppe, med tidsgrense, loggfil og tak på utdata |
| `Sources/HavenAgentRuntime/ScheduledEventService.swift` | endret: planleggeren. Fila på `main` er erstattet i sin helhet; den offentlige API-en skal stå |
| `Sources/HavenAgentRuntime/ScheduledJobStateFiles.swift` | ny: lesere for `<id>.control.json` og `<id>.ack.json`, og tidsstempler |
| `Sources/HavenAgentRuntime/ScheduledWorkerPresence.swift` | ny: `worker.lock` og `worker.json` |
| `Tests/HavenAgentRuntimeTests/CronScheduleTests.swift`, `ScheduledEventScheduleTests.swift`, `Fixtures/cron-forventninger.json` | nye tester (Swift Testing, som repoet bruker) |
| `Tests/HavenMacAutomationTests/BoundedProcessRunnerTests.swift` | nye tester |
| `patcher/HavenAgentMain.swift.patch`, `patcher/install-agent-dev.sh.patch` | endringer i to filer som finnes på `main`. Ikke kompilert, ikke kjørt |
| `Launchd/io.digipomps.haven.agentd.scheduler.plist` | ny: planleggerens LaunchAgent som mal |
| `Docs/ScheduledEvents.md` | hele dokumentet etter trinn 3 |
| `sky/` | bare for bygget her: `Package.swift`, stedfortredere for typer som ikke kan bygges i skyen, og `bygg.sh`. Skal ikke til repoet |

Grunnlaget er `origin/main` `ea558ba` i HavenAgentD. Kildene derfra ligger under
`/mnt/user-data/uploads/HavenAgentD/.tmp-clang-module-cache/agentd-diag/origin-main-ea558ba/` (bl.a. `Sources/HavenAgentRuntime/ScheduledEventService.swift`, `AgentConfig.swift`, `AgentRuntime.swift`, `Sources/HavenMacAutomation/*.swift`, `Sources/HavenAgentD/HavenAgentMain.swift`, `Scripts/install-agent-dev.sh`, `Package.swift`). Testen som finnes på main: `/mnt/user-data/uploads/HavenAgentD/.worktrees/main-20260922/Tests/HavenAgentRuntimeTests/ScheduledEventServiceTests.swift`.

Kontrakten koden skal følge: `S/pdd-cron/contract/trinn3-cron.md`, delen «Styring: pause, fortsett, stopp» i `S/pdd-cron/contract/trinn4-jobber-og-godkjenning.md`, skjemaene `scheduled-job-control-v1.schema.json` og `scheduled-job-ack-v1.schema.json` og eksempelet `fixtures/ScheduledJobs/worker.json` i samme mappe, og testene T1, T2 og T3 i `S/pdd-cron/FORMAALSSPEC.md` §5. Der koden avviker fra kontrakten, er det enten en feil i koden eller noe kontrakten må si; si hvilket du mener det er.

## Slik bygges og kjøres det her

Swift 6.2.3 for Linux er pakket ut i `S/swift-tc/` (fra Ubuntu-arkivet). Private avhengigheter (CellProtocol, Sprout) kan ikke hentes, så bare `HavenMacAutomation` og de filene i `HavenAgentRuntime` som klarer seg med Foundation, bygges. macOS-grenen i koden (`#if canImport(Darwin)`) er derfor aldri kompilert.

```
. S/swift-tc/env.sh
S/trinn3/sky/bygg.sh grunnlinje     # main alene, med de tre testene som fantes
S/trinn3/sky/bygg.sh trinn3         # med filene i trinn3/ lagt oppå: 54 tester
```

`bygg.sh` skriver til `S/trinn3-bygg-grunnlinje/` og `S/trinn3-bygg-trinn3/`. Bruk ikke dem. Lag din egen arbeidsmappe `S/fabel-trinn3/`, kopier `S/trinn3-bygg-trinn3/` dit (uten `.build` om du vil), og bygg og prøv der:

```
cd S/fabel-trinn3/<kopien> && swift test --no-parallel -Xswiftc -Xfrontend -Xswiftc -disable-cross-import-overlays
```

(Flagget trengs fordi Ubuntu-pakken mangler `lib_Testing_Foundation.so`.) Skriv gjerne egne tester og små programmer der for å prøve det du mistenker.

## Det jeg ber om

1. **Samme tidspunkt aldri to ganger, og ingenting tapt.** Gå gjennom `runDueEvents`, `runEvent`, `persist`, `adopt`, `stopEvent` og `start` steg for steg, med arbeideren drept eller disken full på hvert sted, og med en annen prosess (`schedule-stop`, `schedule-list`) som leser og skriver samtidig. Aktøren slipper til andre kall ved hvert `await`: hva kan skje imellom?
2. **Reglene i kontrakten.** Passerte tidspunkt, `attention`, avbrutt kjøring, pause og fortsett (også for hendelser på intervall), kvittering, `firstFireAt`, endret uttrykk, `once` og `count` med cron, tak på loggfiler. Stemmer koden, og prøver testene det de sier?
3. **`BoundedProcessRunner`.** POSIX-bruken på både Darwin og Linux: `posix_spawn` med attributter og filhandlinger, signalmaske og standardsignaler, arv av fildeskriptorer (særlig låsene), ventingen, zombier, gjenbruk av prosess-ID, avbrudd, og at fortsettelsen gjenopptas nøyaktig én gang. Hva skjer når loggmappen ikke kan lages, eller disken er full?
4. **macOS.** Det som bygger og virker på Linux her, men ikke vil gjøre det med Xcodes Swift på macOS 13 og nyere: typer og funksjoner som er ulike i Darwin og Glibc, streng samtidighetskontroll (Swift 6-modus), Foundation-forskjeller (`ISO8601DateFormatter`, `TimeZone`, `FileHandle`, `Thread`, `ProcessInfo.systemUptime`), `flock`, `rename`, filrettigheter. Les Darwin-grenene som om du var kompilatoren.
5. **Eldre agent og kallsteder.** Kan agenten fra før trinn 3 lese `config.json` og `State/scheduled-events.json` slik den nye skriver dem? Bryter den nye API-en noen av kallstedene på `main` (se `HavenAgentMain.swift` og testen som finnes)? Er de to patchene riktige mot filene på `main`?
6. **Testene.** Tilfeller som mangler, tester som kan gå grønt av feil grunn, og tester som kan vakle på en treg eller travel maskin.
7. **Dokumentet.** Sier `Docs/ScheduledEvents.md` noe koden ikke gjør?

## Slik svarer du

Skriv til `S/pdd-cron/panel/FABEL_KODE_TRINN3.md`, på norsk. Del den slik: **Må rettes før koden legges i en PR** (nummerert, med fil, linje, hva som skjer, og hva som bør stå), **Bør rettes**, **Kontrollert og funnet i orden** (kort liste), **Ikke kontrollert** (det som bare kan måles på en Mac). Vær konkret: vis til linjer, og vis hvordan du har prøvd det du påstår (kommando og utdata, eller en test du skrev).

Grenser: du kan lese alt som er nevnt her, og bygge og kjøre i din egen mappe `S/fabel-trinn3/`. Du skal ikke endre noe i `S/trinn3/`, `S/impl/`, `S/koe/`, `S/pdd-cron/` (utenom rapportfila) eller byggemappene mine. Ingen verktøy som når Macen, nettlesere, korrespondanse eller andre tjenester, ingen nedlasting fra nettet, og ingen meldinger til noen. Ingen private detaljer fra `S/pdd-cron/panel/kilder-utdrag/` i rapporten.

Svaret ditt til meg skal være kortversjonen: hvert «må rettes» på én linje, og antallet «bør rettes».
