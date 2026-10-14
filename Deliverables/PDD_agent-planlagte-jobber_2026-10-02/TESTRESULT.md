# TESTRESULT: agent planlagte jobber

PDD `agent-planlagte-jobber`. Sist oppdatert 05.10.2026 kl. 19:45Z. Testene er de i `FORMAALSSPEC.md` §5. Det som står her, er kjørt og målt, og råutdataene ligger i `evidence/`. En test som ikke er kjørt, står som «ikke kjørt», med grunnen.

## Oversikt

| Test | Tilstand 05.10 | Kjørt | Gjenstår |
|---|---|---|---|
| T0 | delvis | køene, `gh`, signaturene, launchd, disk, klientens verktøy | første planlagte kjøring av sjekken uten dialog (kommer med `utfoer`) |
| T1 | grønn | 12 enhetstester på macOS | ingenting |
| T2 | grønn i enhetstester | 15 + 45 enhetstester på macOS (41 fra 14:08Z og fire nye fra 19:36Z, se «Rettelsene 05.10 kveld») | omstart under launchd med ny binær (T6) |
| T3 | grønn i enhetstester | de samme 45 | ingenting før T6 |
| T4 | ikke kjørt | | trinn 4 er ikke bygget. Det venter på at PR #25 er merget. |
| T5 | ikke kjørt | | samme |
| T6 | ikke kjørt | | krever ny agent installert, altså merge og køvindu |
| T7 | ikke kjørt | | trinn 4 og 5, og bildene (G1-GUI) |
| T8 | prøvedata grønn på Macen | selvtesten (128 kontroller) og tørrkjøringen av installasjonen | live: `utfoer` venter på Kjetils ja til forskjellen i `config.json` |
| T9 | prøvedata grønn på Macen | samme selvtest | live: samme |
| T10 | delvis. **CI er rødt** | hele testmengden på macOS, sammenlignet på testnavn: 398 tester 19:36Z. CI-løpet for PR #30 sto til tidsgrensen, se «CI for PR #30» | et grønt CI-løp, eldre binær mot nye filer, og inn og ut av de faste programmene |

## t0

Avhengighetene i `FORMAALSSPEC.md` §2, én rad per måling.

| Avhengighet | Målt | Resultat |
|---|---|---|
| En jobb fra tråden kjører i `.agent-spool` | 03.10 og 05.10 | ja. Bygget og testene under gikk gjennom den køen, og det samme gjorde alle commits og push. |
| `gh` fra `.agent-spool` | 03.10 | nei: `[Errno 2] No such file or directory: 'gh'` |
| `gh` fra `_losen-queue` | 05.10 kl. 14:16Z | ja: `/usr/local/bin/gh`, versjon 2.101.0, innlogget som `kjetilh`, med rettighetene `admin:public_key`, `gist`, `read:org`, `repo` og `workflow` |
| Planleggeren kjører | 05.10 kl. 14:16Z | `io.digipomps.haven.agentd.scheduler`: `state = running`, pid 18244, aldri avsluttet |
| Agenten kjører | 05.10 kl. 14:16Z | `io.digipomps.haven.agentd`: `state = running`, pid 17958 |
| Signaturen på binærene som er installert (S0 punkt 2) | 05.10 kl. 14:16Z | `haven-agentd`, `haven-agentd-scheduler` og `haven-agentd-mcp`: Developer ID Application: Stiftelsen Digipomps (5UT5HQTCV9), herdet kjøretid, signert 26.09 kl. 20:45–20:47, `codesign --verify --strict` gyldig. Menyappen (0.1.0) er ad hoc-signert. |
| Klienten har verktøyet programmet venter | 05.10 kl. 14:43Z | ja: fire verktøy, `correspondence.list_inbox` uten påkrevde argumenter |
| Klienten tar `--root` | 05.10 | ja, men som profilens egen mappe. Se t8. |
| `/usr/bin/python3` er 3.9 eller nyere | 05.10 | 3.9.6 |
| Nok disk til å bygge | 05.10 kl. 13:52Z | 80 GiB før bygget, 76 GiB etter. Regelen krever omtrent 57. |
| Menylinjen leser kilden `correspondence` | 02.10 | `read`. Ikke målt på nytt 05.10. |
| Korrespondanseklienten kan kjøres av planleggeren uten dialog | ikke kjørt | måles ved første planlagte kjøring, etter `utfoer` |
| Agentens MCP-server kan nås fra Claude-appen | ikke kjørt | hører til trinn 4 |

Råutdata: `evidence/LES-INSTALLERT-20261005-utdrag.md` (uten profilene) og `evidence/KORRESPONDANSEVAKT-TOERR-3-20261005.md`.

## t1

`CronScheduleTests`, 12 tester, kjørt på Macen 05.10.2026 kl. 14:07Z med Swift 6.4.0-dev (`swift test --skip-build --no-parallel`, jobb `planlagte-jobber-s3-bygg-20261005` i `.agent-spool`). Fasiten er `Tests/HavenAgentRuntimeTests/Fixtures/cron-forventninger.json`.

```
Suite CronScheduleTests passed after 4.008 seconds.
  theAnswerKeyIsComplete
  instantsMatchTheAnswerKey
  countsAcrossTheClockChangesMatchTheAnswerKey
  expressionsInTheAnswerKeyAreRejected
  shortestGapsMatchTheAnswerKey
  runningMeansAStarAnywhereInTheMinuteOrHourField
  afterIsStrictAndMayCarrySeconds
  theExpressionIsStoredWithSingleSpaces
  errorsSayWhatIsWrong
  theLastInstantInAWindowAgreesWithTheForwardSearch
  aCountWithALimitStopsAtTheLimit
  theShortestGapCanStopAtTheFirstOneBelowAThreshold
```

## t2

`BoundedProcessRunnerTests`, 15 tester, samme kjøring. Dette er tidsgrensen, utdatataket og prosessgruppen.

```
Suite BoundedProcessRunnerTests passed after 4.719 seconds.
  aQuickCommandReturnsItsStatusAndTheEndOfItsOutput
  aFailingCommandKeepsItsStatusAndItsOutput
  aCommandThatEndsOnASignalReportsTheSignal
  aCommandThatRunsPastTheTimeLimitIsStoppedWithEverythingItStarted
  aCommandThatIgnoresTheRequestToStopIsRemovedAfterTheGracePeriod
  moreOutputThanAPipeHoldsDoesNotHoldTheRunnerUp
  aChildLeftBehindDoesNotHoldTheRunnerUp
  outputPastTheLimitStopsTheCommand
  cancellingTheTaskStopsTheCommand
  aTaskThatIsCancelledAlreadyStartsNothing
  aCancellationThatComesBeforeTheCommandExistsStartsNothing
  everySignalTheCallerIgnoresHasItsDefaultHandlingInTheCommand
  aCommandThatCannotBeStartedIsALaunchFailure
  theCommandRunsInItsOwnProcessGroupAndCanBeStoppedWithTerm
  aLogThatIsAppendedToGivesOnlyTheEndOfTheLastRun
```

Resten av T2 (omstart mellom to kjøringer, og at en arbeider nummer to ikke får låsen) står blant de 41 under t3: `theStateSurvivesThatTheWorkerIsStoppedAndStartedBetweenTwoRuns` og `aSecondWorkerIsTurnedAwayAndTakesOverWhenTheFirstHasStopped`. Begge holder de to arbeiderne i samme prosess. `flock` mellom to prosesser er ikke prøvd.

## t3

`ScheduledEventScheduleTests`, 41 tester, og `ScheduledEventServiceTests`, de 3 som fantes på `main`. Samme kjøring.

```
Suite ScheduledEventScheduleTests passed after 8.892 seconds.
  aCronEventRunsAtItsInstantsInItsTimeZoneAndNotForTheTimeBeforeItWasSeen
  whenSeveralInstantsHavePassedTheEventRunsOnceAndTheRestAreCounted
  anEventEveryHalfHourCountsANightOfSleepWithoutAskingForAttention
  aDailyEventThatWasPassedAsksForAttentionUntilItIsAcknowledged
  aDailyEventOnAnIntervalAsksForAttentionAfterTwoDays
  aFailedRunAsksForAttentionUntilARunSucceeds
  firstFireAtHoldsACronEventBack
  aCronEventThatRunsACountedNumberOfTimesCompletes
  changingTheExpressionStartsTheCountAgain
  theInstantIsTakenOnDiskBeforeTheCommandStarts
  aRunThatWasCutOffIsNotRepeatedAndAsksForAttention
  aRunningRecordLeftByAnAgentWithoutCronIsNotRepeatedEither
  theStateSurvivesThatTheWorkerIsStoppedAndStartedBetweenTwoRuns
  aPausedEventIsNotRunAndThePauseIsNeitherCaughtUpNorCounted
  anIntervalEventRunsAtOnceAfterAPauseAndThePauseIsNotCounted
  aControlFileThatCannotBeReadKeepsTheEventFromRunning
  aControlFileThatSaysStoppedKeepsAnEventFromRunningAndSaysSo
  aResumeTimeInTheFutureIsReadAsNow
  theFirstRunOfAnIntervalEventCountsNothingHoweverOldItsFirstInstantIs
  aRecordWrittenWithoutTheCronFieldsIsCountedFromThenAndStillRuns
  aStateFileThatBecomesUnreadableIsWrittenAgainAndTheEventStillRuns
  aWorkerRefusesAStateFileItCannotReadAndMovingItAsideStartsAgainFromTheConfiguration
  aStateFileWithAnOutcomeOrAKindThisAgentDoesNotKnowIsUnreadableToIt
  aStopGivenAfterARunWasCutOffSurvivesTheNextWorker
  stoppingTheWorkerDuringARoundLeavesTheNextDueEventDue
  aRunThatNeverStartedGivesItsInstantBack
  aConfigurationThatCannotBeUsedIsRefusedBeforeAnythingIsWritten
  anAgentWithoutCronReadsTheNewConfigurationAndStateAndTheNewOneReadsTheOld
  aSecondWorkerIsTurnedAwayAndTakesOverWhenTheFirstHasStopped
  theWorkerLeavesASignOfLifeAlsoWhileACommandRuns
  theSignOfLifeCanBeHeldBack
  theNumbersInTheContractAreTheDefaults
  aStopFromAnotherProcessKeepsWhatTheWorkerHasWritten
  aStoppedEventAsksForNothing
  aStopThatComesWhileACommandThatFailsIsRunningLeavesNothingAsked
  aRealCommandGetsALogAndTheEndOfItBecomesTheSummary
  aCommandThatHangsOrFloodsIsStoppedAndTheNextEventStillRuns
  stoppingTheWorkerStopsTheCommandAndTheRunIsNotRepeated
  anEventsOwnTimeLimitAppliesWhenItIsShorterThanTheCeiling
  oldLogsAreRemovedAndFiftyAreKept
  anIdBecomesAFolderNameThatCannotLeaveTheLogFolder
Suite ScheduledEventServiceTests passed after 0.065 seconds.
  countedEventRunsExactNumberOfTimesAndPersistsCompletion
  stoppedUntilStoppedEventDoesNotRunAgain
  workerObservesStopWrittenByAnotherProcess
```

Samlet for t1, t2 og t3:

```
Test run with 15 tests in 1 suite passed after 4.719 seconds.
Test run with 56 tests in 3 suites passed after 12.968 seconds.
```

Det var første gang macOS-grenene i koden ble kompilert. `swift build --build-tests` tok 903 sekunder og ga ingen advarsler i de nye filene.

## t4, t5, t6, t7

Ikke kjørt. T4 og T5 gjelder trinn 4 (jobber en assistent ber om, godkjenning og MCP-verktøy), som ikke er bygget: det endrer filer PR #25 også endrer, og bygges på `main` etter at den er merget. T6 og T7 krever at den nye agenten er installert, og T7 trenger i tillegg menyen fra trinn 5 og godkjente bilder.

## t8

**Første tørrkjøring på Macen, 05.10 kl. 14:20Z, stoppet i steg 2.** Det var første gang programmet kjørte på macOS. Selvtesten gikk gjennom (126 kontroller), men klienten svarte ikke:

```
klienten ga ikke verktøylista for kjetil-vegar-d: klienten startet ikke (klienten avsluttet med kode 1: error: No enrolled correspondence profile exists at /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/profile.json.)
STOPPET: korrespondanseklienten kan ikke brukes slik programmet venter. Ingenting er lagt inn.
```

Årsaken: klienten leser `--root` som profilens egen mappe, og programmet ga den mappen profilene ligger i. Prøveklienten i testene hadde samme gale antakelse som programmet, og derfor var alt grønt i skyen. Rettet i commit `081d52d`: programmet gir `<klientrot>/<profil>`, og prøveklienten nekter nå slik den ekte gjør. Settes det gamle kallet tilbake, blir 55 av 128 kontroller i selvtesten røde.

**Tørrkjøringen etter rettelsen gikk gjennom alle seks steg uten å endre noe, to ganger:** kl. 14:43Z på `081d52d`, og kl. 15:02Z på `653fb87`, som er commiten PR #30 står på. Fra den siste:

```
1. Python og selvtest
   /usr/bin/python3 er 3.9.6
   SELVTEST OK 128 kontroller
2. Sjekksummer og korrespondanseklienten
   klienten tar --root: ja
   klienten svarte for kjetil-vegar-d: 4 verktøy (correspondence.list_inbox, correspondence.read_message, correspondence.send_message, correspondence.ack_message)
   innboksverktøyet heter correspondence.list_inbox, og krever ingen argumenter
   ingen innboks ble lest
4. Validering med agenten som er installert
   haven-agentd validate-config: ok
   haven-agentd schedule-list: ok, 3 hendelser (<id>: scheduled, korrespondanse-sjekk: scheduled, korrespondanse-frist: scheduled)
   haven-agentd-scheduler validate-config: ok
   haven-agentd-scheduler schedule-list: ok, 3 hendelser (<id>: scheduled, korrespondanse-sjekk: scheduled, korrespondanse-frist: scheduled)
   hver hendelse peker på et fast program i policyen: ok
   den ekte tilstandsfila er urørt: ok
6. Stopper her. Ingenting er endret.
```

Hele utskriften, med forskjellen i `config.json`, står i `evidence/KORRESPONDANSEVAKT-TOERR-3-20261005.md`. Den første, som stoppet, står i `evidence/KORRESPONDANSEVAKT-TOERR-1-20261005.md`, og den andre i `evidence/KORRESPONDANSEVAKT-TOERR-2-20261005.md`. Forskjellen i `config.json` er den samme i den andre og den tredje, bortsett fra tidspunktet for første kjøring. I den andre manglet parentesen rundt en skjult id i to linjer av utskriften; det er rettet i `04168c9` og `653fb87`.

På Linux: 44 tester og 128 kontroller i selvtesten er grønne på Python 3.9.23, 3.11.15 og 3.13.13, med filene slik de står i `653fb87`.

Live (en ekte ulest melding gir en sak, og menyen leses av 30 minutter etter at planleggeren er stoppet): ikke kjørt. Det krever `utfoer`, som venter på Kjetils ja til forskjellen.

## t9

Prøvedataene for fristvarselet er en del av selvtesten og de 44 testene over (8 døgn og 0 timer gir ingen sak, 7 døgn og 23 timer gir sak, passert frist gir «gikk ut», manglende bevis gir «uten bevis», fornyet tilgang fjerner saken). Grønt på Macen (selvtesten) og på Linux. Live: ikke kjørt, av samme grunn som t8.

## t10

**Hele testmengden, sammenlignet på testnavn.** `swift test --skip-build --no-parallel` på Macen 05.10 kl. 14:08Z:

```
Test run with 20 tests in 2 suites passed after 4.536 seconds.
Test run with 18 tests in 2 suites passed after 0.814 seconds.
Test run with 240 tests in 37 suites passed after 24.603 seconds.
Test run with 53 tests in 11 suites passed after 0.041 seconds.
Test run with 25 tests in 2 suites passed after 2.085 seconds.
Test run with 31 tests in 4 suites passed after 3.824 seconds.
Test run with 7 tests in 1 suite passed after 1.301 seconds.
```

Det er 394 tester i 59 suiter, ingen feilet og ingen hoppet over. Kildene har 394 funksjoner merket `@Test`: 326 i filene som er uendret fra `origin/main` (`ea558ba`), og 68 i de tre nye filene. Hver av de 394 har en linje med «passed» i loggen; ti av dem er tester med flere tilfeller, og står som «with N test cases passed».

Det som ble bygget, er treet til commit `9af7811`. De tre commitene etterpå (`081d52d`, `04168c9` og `653fb87`) endrer ingen Swift-filer.

Røyktesten CI kjører til slutt (`haven-agentd smoke-test` i en midlertidig mappe) gikk grønt på Macen 05.10 kl. 15:04Z, rett før PR #30 ble opprettet: `evidence/OPPRETT-PR-20261005.md`. CI-løpet for PR-en ble rødt; se «CI for PR #30» under.

Ikke kjørt: binæren fra 26.09 mot ny konfigurasjon og ny tilstandsmappe, at den nye binæren skriver `config.json` uten å miste de nye feltene mot den ekte fila, og at de faste programmene tas ut og legges inn igjen. Alt det krever installasjon. Enhetstesten `anAgentWithoutCronReadsTheNewConfigurationAndStateAndTheNewOneReadsTheOld` dekker lesingen begge veier med typene i koden, ikke med den gamle binæren.

## CI for PR #30

**Rødt.** Løp 37330064662 (05.10 kl. 15:06Z, hode `653fb87`) sto i steget «Test and smoke-check HavenAgentD» til tidsgrensen på 25 minutter. Ingen test er meldt som feilet; utskriften bare stopper.

Det som er målt (jobbene `b20-planlagte-jobber-ci-logg-1` til `-3`, `…-ci-historikk-1` og `…-ci-logg-hele-1` i bane b, og en uavhengig kontroll, `panel/FABEL_CI_PR30.md`):

| Måling | Resultat |
|---|---|
| Samme stopp på andre grener | Ja. `main` `ea558ba` (løp 36573898495, 29.09) og `codex/file-provenance-20261002` `b5adebd` (løp 37113316662, 03.10) stopper på samme linje. Det er alle løp med det gamle `Scripts/test_haven_agentd.sh` siden 29.09 kl. 13:16Z: tre av tre. |
| Grønt løp av `main` slik den står | Finnes ikke. `ea558ba` har ett løp, og det er rødt. |
| Hvor testene stoppet | Kan ikke leses av loggen. Utskriften slutter på samme byte i alle tre, 32 768 byte etter XCTest-startlinja. Det er to tømminger av et buffer på 16 KiB; en tredje kom aldri. I vinduet etter ligger blant annet hele `CronScheduleTests` for PR #30. |
| Hvilken prosess som sto | Kan ikke avgjøres av loggene: testprosessen selv, eller `swift-package` som leser utskriften dens. |
| Med nytt testskript | To løp på `codex/file-provenance-20261002` etter commit `5dc229f` (fasegrenser, og testprosessen startes direkte med utskriften rett til loggen) er grønne. To av to. |

**Min første lesning holdt ikke:** at løpet stoppet før noen av PR-ens tester hadde startet. Loggen viser ikke det. Den uavhengige kontrollen felte lesningen før den ble lagt fram (`panel/BRIEF_CI_PR30.md`, påstand C1). PR-en ble opprettet uten at løpene på `main` var lest først; det kostet ett løp på 25 minutter.

## Rettelsene 05.10 kveld

Kontrollen over leste også koden og fant seks ting (`panel/FABEL_CI_PR30.md`, F1–F6). De to første står på `main` i dag (`ea558ba`, `Sources/HavenAgentRuntime/ScheduledEventService.swift` linje 173–177 og 206–211). Ingen av dem er årsaken til de røde løpene, som stoppet før disse testene.

| Funn | Rettet slik | Test som holder det fast |
|---|---|---|
| F1: arbeiderløkka gikk i ring uten å vente når tjenesten ble sluppet uten `stop()` | Løkka holder tjenesten bare mens en runde går og sover gjennom en kopi av lukkingen; `deinit` avbryter arbeideren | `aServiceThatIsLetGoOfWithoutStopTakesItsWorkerWithIt` |
| F2: `runDueEvents()` gjorde stille ingenting når en runde alt gikk | Kallet venter på runden og gjør så sin egen, med eget blikk på klokka | `aRoundAskedForWhileAnotherRunsWaitsForItAndThenLooksAtTheClockItself` |
| F5: `start()` to ganger på samme tjeneste regnet arbeiderens egen kjøring som avbrutt | Bare kallet som tar arbeiderlåsen, rydder etter avbrutte kjøringer | `startingAWorkerAgainWhileItsCommandRunsLeavesTheRunAlone` |
| F6: låsen til tilstandsfila ble ventet på uten grense | Fem sekunder, så feiler endringen med «Cannot take the lock» | `aChangeGivesUpWhenSomeoneElseHoldsTheStateFilesLockAndGoesThroughWhenItIsFree` |
| F3: tidsgrenser på 0,3 og 0,4 sekunder i prosesstestene | 1,5 sekunder | de to testene selv |
| F4: to tester endrer signalhåndteringen for hele prosessen | Suiten er seriell (`@Suite(.serialized)`) | |
| M1–M3: et barn kunne bli stående, et poll-intervall på null ga travel løkke, en test snurret med `Task.yield()` | `defer`-drap, minst 0,01 sekund, en port i stedet for snurring | |

Ikke rettet: M4 (`ISO8601DateFormatter` lages per kall), som er ytelse og ikke korrekthet. Og den andre halvdelen av M2: lar tråden i `BoundedProcessRunner` seg ikke starte, venter kalleren for alltid. Foundation melder ikke at en tråd ikke startet, så det er ikke rørt. M5 og M6 var gjennomganger uten funn.

**Linux (Swift 6.2.3), i skyen:** 75 tester i de fire suitene, grønne ti av ti ganger (fire etter hverandre, tre parallelt, tre med maskinen holdt travel). Hver av de fire nye testene blir rød når rettelsen den vokter, tas ut igjen, og de åtte eldre mutasjonene er fortsatt røde. For F1 er det to sikringer (løkka og `deinit`); tas bare én ut, holder den andre, og testen er grønn. Tas begge ut, er den rød.

**macOS (Swift 6.4), jobb `planlagte-jobber-ci-rettelser-bygg-20261005` i `.agent-spool`, 05.10 kl. 19:31–19:36Z:** `swift build --build-tests` ok på 117 sekunder, ingen advarsler. Planleggersuitene tre ganger:

```
Test run with 15 tests in 1 suite passed after 6.945 seconds.
Test run with 60 tests in 3 suites passed after 13.950 seconds.
Test run with 15 tests in 1 suite passed after 6.828 seconds.
Test run with 60 tests in 3 suites passed after 12.570 seconds.
Test run with 15 tests in 1 suite passed after 6.807 seconds.
Test run with 60 tests in 3 suites passed after 12.458 seconds.
```

Hele `swift test --skip-build --no-parallel` to ganger, likt begge ganger:

```
Test run with 20 tests in 2 suites passed after 6.646 seconds.
Test run with 18 tests in 2 suites passed after 0.561 seconds.
Test run with 244 tests in 37 suites passed after 24.916 seconds.
Test run with 53 tests in 11 suites passed after 0.033 seconds.
Test run with 25 tests in 2 suites passed after 1.397 seconds.
Test run with 31 tests in 4 suites passed after 3.229 seconds.
Test run with 7 tests in 1 suite passed after 0.941 seconds.
```

Det er 398 tester i 59 suiter: de 394 fra kl. 14:08Z og de fire nye. Råutdata: `evidence/CI-RETTELSER-macos-bygg-og-tester-20261005.log`.

**Med løperen CI vil bruke etter `5dc229f`** (jobb `b20-planlagte-jobber-ci-loeper-proeve-1-20261005`, kl. 19:37Z): de samme ferdigbygde testene, startet med `Scripts/run_ci_phase.py` og `Scripts/run_prebuilt_tests.py` fra `origin/codex/file-provenance-20261002`:

```
løperen ga kode 0 etter 28 sekunder
i alt 398 tester
CI phase finished in 27.8s, exit 0
TESTFASEN ER GRØNN med løperen fra origin/codex/file-provenance-20261002, på denne Macens verktøykjede.
```

Råutdata: `evidence/CI-LOEPER-PROEVE-1-20261005.md`. Grensen for fasen er 120 sekunder.

**Commit `ffe1aae0bcc0a77ab64f9a8fe72e297ecf1a0a29`**, lokalt på `claude/planlagte-jobber-20261002`, én foran `origin` (`evidence/CI-RETTELSER-commit-20261005.log`). Ikke pushet.

**Ikke bevist:** at et CI-løp blir grønt. CI har Swift 6.2.4, én samlet testbunt og en løper med få kjerner; Macen har Swift 6.4 og sju bunter. Med det gamle testskriptet er tre av tre løp røde uansett gren, så et nytt løp sier først noe når testskriptet fra `5dc229f` er med.
