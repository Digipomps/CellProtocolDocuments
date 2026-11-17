# Oppdrag: uavhengig kontroll av hvorfor CI ble rødt for PR #30, og av arbeiderløkka i planleggeren

Du er en uavhengig kontrollør. Jeg (en annen Claude-tråd) har en PR der CI ble rødt, og jeg har en forklaring. Jobben din er å finne ut om forklaringen holder, og å finne det jeg har oversett i koden. En konklusjon som ikke tåler loggene, skal felles.

## Hva det gjelder

PR #30 i `Digipomps/HavenAgentD` (grenen `claude/planlagte-jobber-20261002`, hode `653fb87`, bygget på `main` = `ea558ba`) legger til cron i planleggeren. Den har tre nye testsuiter: `CronScheduleTests` og `ScheduledEventScheduleTests` (i målet `HavenAgentRuntimeTests`) og `BoundedProcessRunnerTests` (i målet `HavenMacAutomationTests`). Lokalt på eierens Mac gikk hele testsettet grønt. I CI stoppet steget «Test and smoke-check HavenAgentD» på tidsgrensen etter 25 minutter.

Hver ny push starter et CI-løp på en macOS-løper, og eieren har bedt om få løp. Jeg skal derfor ikke pushe eller starte noe på nytt før jeg vet hva som skjedde. Det som står på spill: at jeg skylder på noe utenfor PR-en når feilen er min, eller omvendt, og at neste løp brennes på samme måte.

## Regler

- Du leser bare. Alt du trenger, ligger i `/tmp/claude-0/-home-claude/659b8e4f-cd7d-5f45-acab-087370954f18/scratchpad/fabel-ci/`.
- Du skriver bare i undermappen `arbeid/`. Rapporten din er `arbeid/rapport.md`. Små skript du lager for å telle i loggene, legger du også der.
- Ikke bruk verktøy som heter `mcp__remote-devices__*`, ingen korrespondanseverktøy, ingen nettleser, ingen meldinger, ikke noe nett. Ikke les utenfor denne mappen. Det finnes ingen Swift-kompilator du skal bruke: dette er lesing og telling.
- Skriv rapporten på norsk bokmål.

## Det du har

- `ci/CI-LOGG-37330064662-feilet.txt`: loggen for stegene som feilet i løpet for PR #30 (05.10).
- `ci/CI-LOGG-36573898495-feilet.txt`: det samme for et rødt løp på `main` (`ea558ba`, 29.09). `ci/CI-LOGG-37113316662-feilet.txt`: et rødt løp på en annen gren, `codex/file-provenance-20261002` (`b5adebd`, 03.10).
- `ci/CI-LOGG-37160743097-hele.txt`: hele loggen for et grønt løp på den andre grenen (`5cf3531`, 03.10), etter at den grenen hadde endret testskriptet.
- `ci/CI-HISTORIKK-1-20261005.md`: de 40 siste løpene med utfall og varighet. `ci/CI-LOGG-*-20261005.md` og `ci/PR-STATUS-5-20261005.md`: sammendragene mine av det samme.
- `ci/ci.yml` og `ci/test_haven_agentd.sh`: arbeidsflyten og testskriptet slik de står i PR-en (uendret fra `main`).
- `ci/gren-file-provenance-commits.log` og `ci/gren-file-provenance-CIPhaseDiagnostics-og-skript.log`: hva den andre grenen endret (`Docs/CIPhaseDiagnostics.md`, `Scripts/test_haven_agentd.sh`, `Scripts/run_ci_phase.py`, `Scripts/run_prebuilt_tests.py`).
- `ci/lokalt-S3-macos-bygg-og-tester-20261005.log`: den lokale kjøringen på Macen 05.10 (`swift build --build-tests`, så `swift test --skip-build --no-parallel`), med tiden hver test og suite tok.
- `kilde/Sources/` og `kilde/Tests/`: de nye og endrede Swift-filene i PR-en (blob-hashene er kontrollert mot grenen). `ScheduledEventServiceTests.swift` fantes fra før.

Linjene i CI-loggene har formen `jobb<TAB>steg<TAB>tidsstempel tekst`. Tidsstempelet er når GitHub tok imot linja, ikke når testen skrev den.

## Del 1: finn det ut selv, før du leser forklaringen min

Svar på disse fra loggene. Tell selv; ikke stol på sammendragene mine.

1. Hvor stopper testutskriften i hvert av de tre røde løpene? Er det samme sted? Hvor mange byte testutskrift kom ut før stoppet, regnet på teksten uten GitHubs forstavelse, og sier tallet noe?
2. Hva kom rett etter det stedet i det grønne løpet, og hvor lang tid tok det? Hvilke suiter ligger innenfor de neste 16 384 bytene med utskrift?
3. Hadde noen av de tre nye suitene i PR #30 startet da løpet stoppet? Hvor i rekkefølgen ville de ha kommet? Begrunn rekkefølgen fra loggene.
4. Hva støtter loggene som årsak: en test som henger, utskrift som ikke blir lest, eller tester som bare tar for lang tid? Hva kan loggene ikke avgjøre? Hva sier linjene etter tidsgrensen i de to andre røde løpene om hvilke prosesser som levde?
5. Hvor ofte har dette skjedd de siste ukene, og på hvilke grener? Finnes det et grønt løp av `ea558ba` eller av PR #30?
6. Den andre grenens endring av testskriptet: hva gjør den annerledes, og hvorfor skulle det hjelpe? Hvilke tidsgrenser setter den? Vil testene i PR #30 holde seg innenfor dem? Bruk tidene i den lokale loggen og forholdet mellom lokal tid og CI-tid som loggene gir deg.
7. Det lokale løpet og CI-løpet: hva er forskjellig (kommando, miljø, verktøykjede, rekkefølge)? Er det noe i forskjellen som kunne fått en test i PR #30 til å henge i CI og ikke lokalt?

## Del 2: påstander som skal avgjøres

For hver: **holder**, **holder ikke** eller **kan ikke avgjøres her**, med belegg (fil, linje eller tall du har telt).

- C1. De tre røde løpene stoppet på samme sted i testutskriften, og det stedet er før noen test fra PR #30 hadde startet.
- C2. Det samme stoppet har skjedd på `main` sitt eget hode (`ea558ba`), som PR #30 bygger på, og på en gren uten koden fra PR #30.
- C3. Stoppet skyldes ikke koden eller testene i PR #30.
- C4. Et nytt løp av PR #30 uten endringer har en reell sjanse for å stoppe på samme måte.
- C5. Endringen på grenen `codex/file-provenance-20261002` (`5dc229f`) fjerner stoppet. (Hvor sterkt er belegget?)
- C6. Med den endringen ville testene i PR #30 holde seg innenfor grensen på 120 sekunder for testfasen i CI.

## Del 3: gransk planleggerkoden for heng og løkker

Les `kilde/Sources/HavenAgentRuntime/ScheduledEventService.swift`, `ScheduledWorkerPresence.swift`, `ScheduledJobStateFiles.swift`, `CronSchedule.swift`, `kilde/Sources/HavenMacAutomation/BoundedProcessRunner.swift` og testene. Uansett hva del 1 viser, vil jeg vite om denne koden kan henge, spinne eller lekke.

- For hver løkke og hver venting (`while`, `Task.sleep`, `flock`, `waitpid`, `await … .value`, `for await`): under hvilke forhold blir den aldri ferdig, eller går rundt uten å vente? Se særlig på arbeiderløkka som `start` lager, og på hva som skjer med den når tjenesten slippes uten at `stop()` er kalt, for eksempel når en test kaster midt i.
- For hver test som starter en arbeider eller en ekte kommando: hva blir stående igjen hvis en `#require` eller en `try` kaster før opprydningen? Kan det som står igjen, få senere tester i samme prosess til å henge, på en maskin med tre kjerner?
- Testene endrer tilstand som gjelder hele prosessen (signalhåndtering). Kan det påvirke andre tester som går i samme prosess, når testene kjøres etter hverandre, og når de kjøres samtidig?
- Tidsavhengige forventninger (`Date()`, `Task.sleep` med faste tider, løkker som venter i høyst N runder): hvilke kan feile på en treg maskin, og hva skjer da med det de har startet?
- Foreslå den minste rettelsen for hvert funn, og en test som ville fanget det.

## Rapporten

`arbeid/rapport.md`, med disse delene:

1. **Funn**, sortert etter alvor: «stopper» (må rettes før PR-en merges), «bør rettes», «merknad». Hvert funn: fil og linje, hva som skjer, et konkret forløp, og rettelsen. Ingen ros.
2. **Svarene på del 1**, med tallene du telte og hvordan.
3. **Påstandene i del 2**, én linje hver med dom og belegg.
4. **Det du ikke kunne avgjøre**, og hva som skulle til for å avgjøre det (for eksempel hva et nytt CI-løp måtte samle inn).
5. **Det du kjørte**, med kommando og utfall.

Svar meg til slutt med de viktigste funnene i noen få linjer og banen til rapporten.
