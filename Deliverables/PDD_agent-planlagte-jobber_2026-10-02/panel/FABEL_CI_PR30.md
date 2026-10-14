# Uavhengig kontroll: rødt CI for PR #30 og arbeiderløkka i planleggeren

Kontrollert 2026-10-05, bare ved lesing og telling i `fabel-ci/`. Ingen Swift er bygget eller kjørt. Tellingene kan gjentas med `arbeid/analyse.py` (utskriften ligger i `arbeid/analyse-utskrift.txt`).

Kortversjon:

- Det synlige stoppet i de tre røde loggene er **ikke der testene stoppet**. Det er der et 16 KiB-buffer sist ble tømt. Belegg: nøyaktig samme byteantall i alle tre (32 710 byte fra XCTest-startlinja = 32 768 − 58), én eneste pause i mottaket, nøyaktig ved 16 384-grensen, og XCTest-linja som ble mottatt 3,7–3,9 s etter at den ble skrevet. Hva testverten gjorde etter det, er usynlig i inntil 16 383 byte til (mer hvis det er SwiftPM som stanset).
- I det usynlige vinduet ligger, for PR #30, hele `CronScheduleTests` (anslått byte 47 177–48 842 av et vindu som går til 49 178). Loggen kan derfor **ikke** vise at ingen PR-test hadde startet. De to andre nye suitene ligger utenfor vinduet hvis det er testverten som stanset; stanset `swift-package`, kan alt være kjørt.
- Det samme stoppet skjedde på `main` (`ea558ba`) og på en gren uten PR #30 (`b5adebd`), og bare med det gamle testskriptet (3 av 3 løp siden 29.09). To løp med det nye skriptet gikk grønt. Hvilken prosess som stanset (testverten eller `swift-package`), kan loggene ikke avgjøre.
- Koden: arbeiderløkka i `ScheduledEventService.start` (linje 403–412) **spinner uten å vente** når tjenesten slippes uten `stop()`. Sju tester starter en arbeider og har et `try`/`#require` før `stop()`. På en tre-kjerners løper tar hver slik lekkasje én av tre tråder i Swift-konkurrensens pool; tre lekkasjer stopper alt, stille. Dette er ikke årsaken til de tre røde løpene (de stoppet før disse testene), men det er en måte PR-en kan gi nøyaktig samme symptom på.

---

## 1. Funn

Sortert etter alvor. «Stopper» = må rettes før PR-en merges. Linjenumre viser til filene i `kilde/`.

### Stopper

#### F1. Arbeiderløkka spinner uten suspensjonspunkt når tjenesten slippes uten `stop()`

`kilde/Sources/HavenAgentRuntime/ScheduledEventService.swift:403–412`

```swift
worker = Task { [weak self] in
    while !Task.isCancelled {
        await self?.runDueEvents()
        do {
            try await self?.sleep(1_000_000_000)
        } catch {
            break
        }
    }
}
```

Hva som skjer: `self` er svakt fanget, så aktoren kan deallokeres mens oppgaven lever. Når `self` er `nil`, kortslutter begge de valgfrie kjedene: `await self?.runDueEvents()` kaller ingenting og suspenderer ikke, `try await self?.sleep(...)` sover ikke og kaster ikke. `Task.isCancelled` er falsk, for den eneste referansen til oppgaven (`worker`, linje 313) forsvant med aktoren, og det finnes ingen `deinit` som avbryter. Løkka går da rundt uten ett eneste suspensjonspunkt og holder én tråd i Swift-konkurrensens pool for resten av prosessens levetid, på 100 % CPU.

Konkret forløp (`kilde/Tests/HavenAgentRuntimeTests/ScheduledEventScheduleTests.swift:1029–1042`):

1. `worker.start(definitions:policy:)` (1030) oppretter arbeideroppgaven og tar arbeiderlåsen.
2. `try await bench.stored()` (1031) kaster hvis posten ikke finnes i fila (`#require` i `stored`, linje 157).
3. Testfunksjonen avsluttes; `await worker.stop()` (1042) nås aldri. `worker` går ut av skop; aktoren deallokeres (oppgaven holder bare en svak referanse). `ScheduledWorkerPresence.deinit` (ScheduledWorkerPresence.swift:66–71) avbryter hjerteslaget og lukker låsen, så lås og hjerteslag lekker ikke.
4. Arbeideroppgaven lever videre og spinner. Testverten (én prosess for alle 344+ tester i CI) har nå to brukbare tråder på en tre-kjerners løper. Alle senere tester går saktere, og tidsavhengige forventninger (F3) feiler lettere. Feiler en til på samme måte, er det én tråd igjen; en tredje gir null: hver `await` i prosessen venter for alltid, ingenting skrives, og steget står til tidsgrensen. Det er samme symptomklasse som CI viste.

Samme mønster (arbeider startet, kastende kall før `stop()`):

| Fil | Starter arbeider | Kan kaste før stop | `stop()` |
|---|---|---|---|
| ScheduledEventScheduleTests.swift | 564 | 565 `#require` | 576 |
| ScheduledEventScheduleTests.swift | 619 (`second`; `first` fra 611 er stoppet på 614) | 621 `#require` | 630 |
| ScheduledEventScheduleTests.swift | 1030 | 1031 `try await bench.stored()` | 1042 |
| ScheduledEventScheduleTests.swift | 1252 | 1259 `try await second.start(...)` | 1263 |
| ScheduledEventScheduleTests.swift | 1276 | 1288, 1290 `try modified()`; 1294 `try JSONDecoder().decode`; 1299 `try contentsOfDirectory` | 1302 |
| ScheduledEventServiceTests.swift (fantes fra før) | 88 | 89 `try await service.stopEvent` | 90 |
| ScheduledEventServiceTests.swift (fantes fra før) | 114 | 115–120 `try await controller.start/stopEvent` | 122 |

Testene på 841–850, 921–927, 1056–1066 og 1529–1539 er trygge: der kommer `stop()` før første kastende kall.

I produksjon oppstår dette bare hvis en `ScheduledEventService` slippes uten `stop()` mens arbeideren går. `HavenAgentMain.swift` er endret i PR-en men ligger ikke i `kilde/`, så det er ikke vurdert.

Minste rettelse (to deler):

1. Hold en sterk referanse bare mens en runde kjører, og sov via en kopi av lukkingen, ikke via `self`. Da deallokeres en sluppet tjeneste under søvnen, og løkka slutter ved neste runde:

   ```swift
   let sleep = self.sleep
   worker = Task { [weak self] in
       while !Task.isCancelled {
           do {
               guard let service = self else { return }
               await service.runDueEvents()
           }
           do { try await sleep(1_000_000_000) } catch { return }
       }
   }
   ```

   (Ikke `while let service = self`: da holdes referansen gjennom søvnen, tjenesten deallokeres aldri, og en eierløs arbeider fortsetter å kjøre jobber hvert sekund.)

2. Gi testene en hjelper som alltid stopper: `withWorker(service) { ... }` som kaller `await service.stop()` både ved retur og ved kast, og bruk den på de sju stedene i tabellen.

Test som ville fanget det: gjør `worker` lesbar for tester (`var workerTask: Task<Void, Never>? { worker }`), start en arbeider i et indre skop, hent oppgaven, slipp tjenesten uten `stop()`, og `await` oppgavens verdi i konkurranse med `Task.sleep(2 s)`. Med dagens kode kommer oppgaven aldri i mål; med rettelsen slutter den ved neste runde.

### Bør rettes

#### F2. Testens eget `runDueEvents()` blir en stille tom operasjon når arbeiderens runde er i gang

`ScheduledEventService.swift:464–469` returnerer straks når `isRunningDueEvents` er sann. `theStateSurvivesThatTheWorkerIsStoppedAndStartedBetweenTwoRuns` (`ScheduledEventScheduleTests.swift:610–615`) starter en arbeider, setter klokka til 10:30 og kaller `first.runDueEvents()` selv.

Forløp som feiler: arbeideroppgaven kommer til aktoren først, leser `now()` = 10:05 (før `clock.set`), og suspenderer i `store.load()` (478). Testens kall får aktoren, ser `isRunningDueEvents == true` og returnerer uten å gjøre noe. `stop()` (614). Arbeiderens runde fortsetter med 10:05: ingenting er forfalt. `#expect(commands.count == 1)` (615) feiler. Samme kappløp på 628–634. Dette er en flakende test, ikke et heng; `#expect` kaster ikke, så `stop()` nås, og F1 utløses ikke her. Lokalt gikk den grønt én gang.

Rettelse: la tester som driver rundene selv bruke `runWorker: false` (denne testen handler om tilstand mellom to tjenester, ikke om løkka). Alternativt i tjenesten: husk rundens `Task` og la et nytt `runDueEvents()`-kall vente på den i stedet for å returnere. Test: blokker en runde i `doWhileRunning` på en continuation, kall `runDueEvents()` fra en annen oppgave, og krev at kallet ikke returnerer før runden er ferdig.

#### F3. Tidsgrenser på 0,3–0,4 s i prosesstestene tåler ikke en belastet løper

`kilde/Tests/HavenMacAutomationTests/BoundedProcessRunnerTests.swift:109–128`: `timeoutSeconds: 0.3`, skriptet `trap '' TERM; echo $$ > pid; while :; do sleep 1; done`. Rekker ikke `/bin/sh` å kjøre `trap` innen 0,3 s etter `posix_spawn` (belastet maskin, tre kjerner, Vapor-tjenere fra tidligere tester i samme prosess), dør det på SIGTERM straks: `elapsed >= 0.8` (125) feiler, og `processID(in:)` (27–30) kaster fordi pid-fila mangler eller er tom. Samme type grense på 86–106 (0,4 s). Det blir ikke stående noe igjen: gruppen er drept før `run` returnerer. I CI målte jeg at én prosesspawnende suite tok 10,6 ganger lokal tid (CodexAppServerBridgeTests: 0,44 s lokalt, 4,65 s i CI), så marginen er ikke trygg.

Rettelse: 1,5–2 s tidsgrense i disse to testene (grace uendret), og krev `elapsed >= timeout + grace`. Testen tar da under 3 s.

#### F4. Signalhåndtering endres for hele prosessen mens testen går

`BoundedProcessRunnerTests.swift:316–317` (`signal(SIGUSR1, SIG_IGN)`) og `345–346` (`signal(SIGTERM, SIG_IGN)`), begge gjenopprettet med `defer`. Etter hverandre (`--no-parallel`, som CI og den lokale kjøringen bruker): ufarlig, og i CI kjører denne suiten sist i den ene prosessen (modulrekkefølgen, se del 2 spørsmål 3), så ingen test kommer etter. Samtidig (`swift test` uten `--no-parallel`, eller Swift Testings vanlige parallellitet): en test som samtidig starter en barneprosess uten å nullstille signaldisposisjoner, får et barn som arver `SIG_IGN` for SIGTERM; venter den så på at `terminate()` skal virke, venter den til prosessen drepes. Om Foundations `Process` på Darwin nullstiller disposisjoner ved spawn, har jeg ikke kunnet kontrollere her; `BoundedProcessRunner` gjør det (`POSIX_SPAWN_SETSIGDEF`, BoundedProcessRunner.swift:271–294).

Rettelse: `@Suite(.serialized)` på `BoundedProcessRunnerTests`, med en kommentar om hvorfor. Test: en sjekk i suiten etterpå om at `signal(SIGTERM, SIG_DFL)` returnerer `SIG_DFL`.

#### F5. `start()` på en tjeneste som allerede kjører arbeideren, behandler sin egen pågående kjøring som avbrutt

`ScheduledEventService.swift:372–391`: `holdsWorkerLock = acquired != nil || presence != nil`. Kalles `start()` en gang til på samme instans mens arbeideren lever (f.eks. ny innlesing av konfigurasjon), er `presence != nil`, og `recoverInterruptedRun` (792–817) kjøres på alle poster, også den arbeideren selv har i `.running`: posten får `interrupted`, `runCount += 1` og skrives. Når kjøringen så ender (631–654), telles den en gang til, og utfallet overskrives. Ikke et heng; feil tilstand. Om `HavenAgentMain` noen gang kaller `start()` to ganger, kan ikke ses i `kilde/`.

Rettelse: hopp over `recoverInterruptedRun` for poster hvor `currentRun` er satt av denne arbeideren (hold en mengde med id-er under kjøring), eller avvis `start()` mens `worker != nil`. Test: start arbeider med en langsom falsk kommando, kall `start()` igjen under kjøringen, krev at posten ikke blir `interrupted` og at `runCount` blir 1.

#### F6. `flock(LOCK_EX)` blokkerer en pool-tråd, uten avbrudd

`ScheduledEventService.swift:268–272`: blokkerende `flock` inne i en synkron aktormetode. Holder en annen prosess (eller en annen `ScheduledEventStore` i samme prosess, egen deskriptor) låsen lenge, står tråden til låsen slipper, og `stop()` kan ikke avbryte den. På en tre-kjerners løper er det en tredel av poolen. Normalt holdes låsen i millisekunder, så dette er en robusthetsmangel, ikke en observert feil.

Rettelse: `LOCK_EX | LOCK_NB` med en bundet, asynkron venteløkke (f.eks. 50 ms × 100), som kaster `stateLockUnavailable` når grensen er nådd. Test: ta låsen fra en annen deskriptor og krev at `update` kaster innen fristen.

### Merknader

- **M1. En `sleep 30` kan bli stående** (`BoundedProcessRunnerTests.swift:170–172`): barnet drepes bare hvis `processID(in:)` lykkes. Kaster den, lever `sleep 30` i 30 s med loggfila åpen. Ufarlig for andre tester. Rettelse: `defer`-drap på pid-en lest tidlig, eller `kill` i en `do/catch`.
- **M2. `pollIntervalSeconds` valideres ikke** (`BoundedProcessRunner.swift:23–35`, brukt på 212 og 220): 0 gir en travel løkke på runnerens egen tråd (ikke poolen). Klem til minst 0,01. Og: feiler `Thread.start()` (101–115), gjenopptas aldri continuationen; sjelden, men da henger kalleren for alltid.
- **M3. `aTaskThatIsCancelledAlreadyStartsNothing`** (`BoundedProcessRunnerTests.swift:238–243`): `while !Task.isCancelled { await Task.yield() }` spinner med yield til `cancel()` på linja etter. Bundet, men på en mettet pool holder den en tråd til den avbrytende oppgaven får kjøre. Bruk heller `withCheckedContinuation` eller start kommandoen direkte etter `cancel()`.
- **M4. `ISO8601DateFormatter()` lages per kall** (`ScheduledJobStateFiles.swift:130–138`): brukes per post per runde (499–505, 675–725). Med 50 ms-runder i tester er det støy; i drift (1 s) uvesentlig. Ytelse, ikke korrekthet.
- **M5. CronSchedule** (`CronSchedule.swift`): alle løkker er bundet. `forEachInstant` (358–366) går høyst 2 929 dager; `instants(onDay:)` (331–346) går 1 440 minutter per dag for «running»-uttrykk; binærsøket i `instant()` (319–327) halverer og garanterer framdrift; `last(after:through:)` (155–168) går én dag om gangen bakover; `count(..., limit:)` og `shortestGap(..., stoppingBelow:)` stopper tidlig. Kostnaden er `TimeZone.secondsFromGMT(for:)` per minutt for running-uttrykk; `theLastInstantInAWindowAgreesWithTheForwardSearch` (CronScheduleTests.swift:178–218) gjør 1 920 sammenligninger, med `* * * * *` over 40 dager = 57 600 instanter per kall. Det er CPU-bundet (3,4 s for suiten lokalt) og skalerer med CPU-fart, ikke med prosessbelastning.
- **M6. `ScheduledWorkerPresence`**: `acquire` bruker `LOCK_NB` (82), hjerteslaget sover (103–117), `deinit` rydder (66–71). Ingen funn.

---

## 2. Svarene på del 1

Alle byteantall er regnet på teksten etter GitHubs forstavelse (jobb, steg, tidsstempel og ett mellomrom), med ett byte for linjeskift per linje, slik testverten ville ha skrevet dem. Skript: `arbeid/tell_logg.py` og `arbeid/analyse.py`.

**1. Hvor stopper testutskriften, og sier byteantallet noe?**

Alle tre røde løp (36573898495 main `ea558ba`, 37113316662 codex `b5adebd`, 37330064662 PR #30) slutter på samme linje: `◇ Test dismissingWhileTheNotificationIsInFlightIsNotUndoneByTheReceipt() started.` (FourthReviewFixTests). Fra `Build complete!` til og med den linja: 356 linjer, 32 736 byte, i alle tre. Fra XCTest-linja `Test Suite 'All tests' started`: 32 710 byte = 32 768 − 58. Fra `◇ Test run started.`: 32 517. Innholdet er ikke identisk (UUID-er, porter, tider skifter), men alle variable felt har lik bredde, så like tall betyr like linjer; det alene sier lite.

Det som sier noe, er tre uavhengige målinger:

- Mottakstidene. I de røde løpene kom hele testutskriften i to bolker: 158 linjer (byte 26–16 184 fra `Build complete!`) innen 19–31 ms, så én pause på 0,585–0,689 s, så 197 linjer (byte 16 184–32 736) innen 13–18 ms. Pausen ligger nøyaktig på linja som spenner over byte 16 384 regnet fra XCTest-linja (16 158–16 394). I det grønne løpet (nytt skript, utskrift arvet rett til `tee`) kommer linjene fortløpende, og pausene ligger der testene faktisk er trege (f.eks. 1,335 s ved en test som «passed after 1.3 s»). I de røde løpene finnes ingen pause ved de samme testene.
- XCTest-linja har eget tidsstempel i teksten. Den ble skrevet 3,795 s, 3,684 s og 3,897 s før GitHub tok den imot. Den satt i et buffer til første tømming.
- `Docs/CIPhaseDiagnostics.md` fra den andre grenen (ci/gren-file-provenance-CIPhaseDiagnostics-og-skript.log, linje 36–39) sier at den opplastede rå `test.log` for løp 37113316662 inneholder nøyaktig 32 768 byte fra XCTest-startlinja og slutter inne i en «passed»-linje. Det stemmer med min telling: 32 710 hele linjer + 58 byte av `✔ Test dismissingWhile… passed after …` (103 byte). GitHub-loggen viser ikke den avkappede linja fordi løperen venter på linjeskift.

Konklusjon: under `swift test` går testutskriften gjennom et buffer på 16 384 byte som tømmes når det er fullt. To tømminger kom; en tredje kom aldri. Det synlige stoppet er bufferets grense, ikke testenes siste linje. Det usynlige er alt skrevet etter byte 32 768: inntil 16 383 byte hvis det er testverten som stanset, mer (pluss rørets kapasitet, 16–64 KiB på macOS) hvis det er leseren i `swift-package` som stanset og testverten fortsatte til røret var fullt. Hvilken komponent bufferet sitter i, er min slutning, ikke noe loggene navngir; det passer med at `swift-package` leser testprosessens utskrift og skriver den videre selv.

**2. Hva kom rett etter i det grønne løpet, og hvilke suiter ligger i de neste 16 384 bytene?**

Rett etter: `✔ Test dismissingWhile… passed after 0.001 seconds.` 76 µs senere (23:13:33.571897), så `✔ Suite FourthReviewFixTests passed after 0.001 seconds.` Testen henger ikke i seg selv.

De neste 16 384 bytene (byte 32 661–49 045 fra `Build complete!`) rommer 18 suitestarter: AdvisorPanelSpawnServiceTests, AgentChallengeInboxTests, AgentChallengeVenueTests, AgentConfigTests, AgentConversationFlowSubscriberTests, AgentIdentityStoreTests, AgentJobRegistrationStoreTests, AgentMailDraftCommandServiceTests, AgentSetupServiceTests, AgentSignStatementCommandServiceTests, AgentStatusRegistrationObservationTests, ArtifactDeliveryTests, ArtifactProvenanceTests, BootstrapProbeServiceTests, BoundedPacketCaptureTests, ClaudeCodeBridgeTests (7,4 s), CodexAppServerBridgeTests (4,6 s), CorrespondenceWaitingTests. DeviceActionRelayTests starter rett utenfor (49 867). Tid fra stopplinja til siste av dem: 12,2 s. Hele testkjøringen: 344 tester i 58 suiter på 21,955 s; testfasen 24,0 s; `Build complete!` til siste smoke-linje 36 s.

**3. Hadde noen av de tre nye suitene startet? Hvor ville de kommet?**

Synlig: nei. Navnene `CronSchedule`, `ScheduledEventSchedule` og `BoundedProcessRunner` forekommer i PR-loggens teststeg bare i kompileringslinjer (`Compiling HavenAgentRuntimeTests ScheduledEventScheduleTests.swift`, fil-linje 3077; `Compiling HavenMacAutomationTests BoundedProcessRunnerTests.swift`, fil-linje 449; `CronScheduleTests.swift` nevnes ikke i det hele tatt, slik SwiftPM bare navngir noen av filene i en batch), aldri i testutskriften. Og de 352 testlinjene fra `◇ Test run started.` til stopplinja er strukturelt identiske med det grønne løpets (bare de fire hodelinjene skiller, 75 byte).

Rekkefølgen, lest ut av loggene: i det grønne løpet kommer suitene gruppevis etter testmål, målene i alfabetisk navneorden (HavenAgentCells… → HavenAgentMCP… → menylinjemodulen → HavenAgentRuntimeTests → HavenMacAutomationTests), og innenfor HavenAgentRuntimeTests alfabetisk etter suitenavn (filnavn). Den lokale loggen (PR #30 selv, `swift test --skip-build --no-parallel`, linje 2021–2596) viser samme orden innenfor målet med de nye suitene plassert: … CorrespondenceWaitingTests → **CronScheduleTests** → DeviceActionRelayTests … RemoteIntentVerifierTests → **ScheduledEventScheduleTests** → ScheduledEventServiceTests … og i HavenMacAutomationTests AutomationPolicyTests → **BoundedProcessRunnerTests** (sist av alt). Dette stemmer med Swift Testings sortering etter kildeplass (modul, fil, linje); det er en slutning fra mønsteret, ikke noe loggene sier rett ut.

Byteposisjoner i PR #30s CI-utskrift, anslått ved å ta det grønne løpets posisjon for AdvisorPanelSpawnServiceTests (+75 byte for PR-hodet) og legge til avstandene fra den lokale loggen omregnet til CI-tegn (de lokale SF-symbolene er 4 byte + 2 mellomrom, CI-tegnene 3 + 1; alt annet er likt): Advisor 32 947, CorrespondenceWaiting 45 801, **CronScheduleTests 47 177–48 842**, ScheduledEventScheduleTests 64 364–71 443, BoundedProcessRunnerTests ca. 80 218–82 664. Buffergrensene fra XCTest-linja ligger på 32 794, 49 178, 65 562, 81 946 byte fra `Build complete!`. Siden en tredje tømming (49 178) aldri kom, stanset testverten – hvis det var den som stanset – et sted i byte 32 794–49 178. Hele `CronScheduleTests` ligger i det vinduet. De to andre suitene kan ikke ha vært nådd uten at en tredje tømming hadde vist seg, med mindre det er `swift-package` som stanset (da kan testverten ha skrevet 16–64 KiB til inn i røret, og vinduet rekker til 65 562–114 714, altså forbi slutten av hele kjøringen).

**4. Hva støtter loggene som årsak, og hva kan de ikke avgjøre?**

- *Tester som bare tar for lang tid*: nei. Det grønne løpet kjørte samme 18 suiter på 12,2 s, og de røde var stille i 19–20 minutter etter siste tømming. Et fast tidsavbrudd på ≥ 20 minutter i en test ville vært noe annet, men da ville det ha skjedd i det grønne løpet også.
- *Utskrift som ikke blir lest* (leseren i `swift-package` stanser, testverten blokkerer på et fullt rør): forenlig med alt loggene viser. Forklarer også at testverten var i live uten å skrive.
- *En test som henger* (i testverten selv): også forenlig. Den hengende testen må da ligge i byte 32 794–49 178: på `main` AdvisorPanel… til CorrespondenceWaiting og de første ~2 000 bytene av DeviceActionRelayTests; i PR #30 i tillegg CronScheduleTests. De tunge kandidatene er prosesspawnende suiter (ClaudeCodeBridgeTests, CodexAppServerBridgeTests), hvis kode ikke ligger her. Mot: samme tester gikk gjennom i det grønne løpet med testverten startet direkte.
- Loggene kan ikke avgjøre hvilken av de to siste det er. Byteantallet er likt under begge, fordi bufferet tømmes ved 16 384 uansett hvem som stanser.
- Linjene etter tidsgrensen: i løp 36573898495 levde `swiftpm-testing-helper` (51948), `swift-package` (40545) og `tee` (40539) 4 s etter avbruddet; i 37113316662 bare `swiftpm-testing-helper` (20392). Testverten var altså i live ≥ 25 minutter etter sin siste synlige linje i begge; steget endte fordi tidsgrensen gikk ut, ikke fordi noe døde. At `swift-package` og `tee` var borte i det ene løpet, sier mest om løperens opprydding (prosesstreet drepes fra toppen) og skiller ikke modellene. Ingen barneprosess av testverten (`sh`, `sleep`, falske `claude`/`codex`) står i listene. PR-loggen inneholder bare steget, så der finnes ingen slik liste.

**5. Hvor ofte, og på hvilke grener? Grønt løp av `ea558ba` eller PR #30?**

Av de 40 løpene i `CI-HISTORIKK` (10.09–05.10): 32 grønne, 8 røde. Tre røde er tidsavbrudd i steg 11 etter 25 minutter: 29.09 13:16 `main` `ea558ba` (push), 03.10 09:31 `codex/file-provenance-20261002` `b5adebd`, 05.10 15:06 `claude/planlagte-jobber-20261002` `653fb87` (PR #30). Det er alle løp med det gamle skriptet siden 29.09 13:16 (3 av 3). De 30 grønne før det, alle med det gamle skriptet, inkluderer de to PR-løpene samme morgen (08:30 `ikon-varslingslisten`, 08:41 `mcp-oncomplete`, 96–106 min totalt, trolig køtid; jobbgrensen er 35 min). `ea558ba` er nettopp sammenslåingen av de to (gren-file-provenance-commits.log, linje 10–12). De to grønne etter 29.09 er begge på codex-grenen med det nye skriptet (5dc229f, 5cf3531). De fem andre røde feilet tidlig i andre steg (Sprout, Package.resolved, pin-sjekk) eller etter 9,8 min i steg 11 (18.09, en vanlig testfeil). Løperbildet er det samme i alle de fire loggene jeg har (`macos-26-arm64 20260907.0351.1`, Swift 6.2.4, Xcode 26.3), så bildet skiftet ikke mellom grønt og rødt.

Det finnes **ikke** noe grønt løp av `ea558ba` (dets eneste løp er rødt) og **ikke** noe grønt løp av PR #30 (ett løp, rødt).

**6. Den andre grenens skriptendring (`5dc229f`)**

Fra `gren-file-provenance-CIPhaseDiagnostics-og-skript.log`. `ci.yml` er uendret (den ytre grensen på 25 min står). Skriptet deler arbeidet i fire faser med egne frister via `Scripts/run_ci_phase.py`: kompilering `swift build --build-tests` 1 200 s, tester 120 s, `swift build --product haven-agentd` 120 s, smoke 30 s. Testfasen kjører ikke `swift test`; `Scripts/run_prebuilt_tests.py` finner `.xctest`-buntene i `.build/debug` (den samlede `HavenAgentDPackageTests.xctest`, eller nøyaktig én per testmål) og starter verktøykjedens `swiftpm-testing-helper` direkte med `--testing-library swift-testing --no-parallel`, med `DYLD_FRAMEWORK_PATH`/`DYLD_LIBRARY_PATH` satt. Utskriften arves rett til `tee` («Output is inherited rather than captured by SwiftPM»), ingen rør og ingen buffer i mellom. `xctest` kjøres ikke (den fant 0 tester før; skriptet nekter om XCTest-kilder dukker opp). Fasen får egen sesjon og prosessgruppe; ved frist tas `sample` av inntil fire prosesser i gruppen til `ci-logs/<fase>-stall/`, så SIGTERM og SIGKILL, og koden 124.

Hvorfor det skulle hjelpe: (a) er det `swift-package`s videreformidling som stanser, er den fjernet; (b) uansett årsak blir et stille 25-minutters stopp til et 2-minutters stopp med stakkprøver av de hengende prosessene, så neste røde løp kan leses; (c) utskriften kommer ustrukket, så siste linje i loggen er testens siste linje. Belegget for at det virker: to grønne løp etter ett rødt på samme gren (del 3, C5).

Holder PR #30 seg innenfor 120 s? Grønn testfase: 24,0 s for 344 tester. De nye suitene lokalt: CronScheduleTests 3,42 s, ScheduledEventScheduleTests 9,40 s, BoundedProcessRunnerTests 4,53 s, sum 17,3 s. Forholdet CI/lokal på de 54 felles suitene er 1,13 (21,4 s mot 19,0 s), men spredt: CodexAppServerBridgeTests 10,6×, ClaudeCodeBridgeTests 1,47×, det meste under 1×. Lavt anslag 24 + 17 ≈ 41 s; med 1,13× ≈ 44 s; høyt anslag der prosesspawning går 3–10× tregere mens faste søvner (0,2–1,5 s) står: 60–100 s. Under 120 s i alle anslag, men marginen i det høye er liten, og et heng (F1) bruker uansett hele fristen. Målingen av de nye suitene finnes bare lokalt, på en annen verktøykjede og i én prosess per mål (spørsmål 7).

**7. Lokalt mot CI**

| | Lokalt (05.10) | CI |
|---|---|---|
| Kommando | `swift build --build-tests` (903 s), så `swift test --skip-build --no-parallel --filter …` (34,7 s) og `swift test --skip-build --no-parallel` (46,2 s) | Gammelt: `swift test --no-parallel` i ett (bygg 283–392 s). Nytt: `swift build --build-tests`, så helper direkte |
| Verktøykjede | SwiftPM «Swift 6.4.0-dev», SDK MacOSX27.0, Testing Library 2084 | Swift 6.2.4, Xcode 26.3, Testing Library 1501 |
| Prosesser | Sju testprosesser, én per mål (20, 18, 240, 53, 25, 31 og 7 tester; sju «Executed 0 tests» fra XCTest) | Én prosess for alle 344+ tester (samlet bunt) |
| Rekkefølge | HavenMacAutomationTests først (AutomationPolicy, **BoundedProcessRunner**), så korrespondanse-, runtime-, menylinje-, MCP-, cells-mål, AgentCellRuntimeHost sist | AgentCellRuntimeHost først … HavenMacAutomationTests sist |
| Utskrift | Rett til logg | Gammelt: via `swift-package` og 16 KiB-buffer. Nytt: arvet til `tee` |
| Kjerner | Ukjent (Mac) | Tre (oppdragets opplysning; ikke lest i loggene) |
| Temp | `/var/folders/7s/…` | Testene bruker `/var/folders/36/…` selv om steget setter `TMPDIR=.build/tmp`; smoke-testen bruker `.build/tmp` |

Kunne noe her få en PR-test til å henge i CI og ikke lokalt? Ja, strukturelt: én prosess for alle mål pluss tre kjerner. En lekket arbeider (F1) tar en tredel av poolen og rammer alle suiter som følger; lokalt isoleres den til sin egen prosess med flere kjerner. Signalendringene (F4) gjelder hele prosessen, men suiten kjører sist i CI og alt går sekvensielt, så de rammer ingen der. Tidsgrensene på 0,3–0,4 s (F3) gir feil, ikke heng. Ingen kjent, deterministisk heng-mekanisme i PR-testene i CI-miljøet; de ble ikke observert å kjøre.

---

## 3. Påstandene i del 2

- **C1 – holder delvis.** Samme sted i synlig utskrift: ja (samme linje, 356 linjer, 32 710 byte fra XCTest-linja i alle tre). «Før noen test fra PR #30 hadde startet»: kan ikke avgjøres; stedet er en buffergrense, og hele `CronScheduleTests` ligger innenfor det usynlige vinduet (anslått byte 47 177–48 842 av vinduet 32 794–49 178).
- **C2 – holder.** Løp 36573898495 (`main` `ea558ba`) og 37113316662 (`b5adebd` på codex-grenen, hvis tre commit over `main` er provenance og skript, ikke PR #30; gren-file-provenance-commits.log 15–19) stopper på samme linje med samme byteantall som PR-løpet.
- **C3 – holder for de tre observerte stoppene, ikke som utsagn om PR-ens tester.** Stoppet skjer uten PR #30s kode (2 av 3 løp), så PR #30 er ikke nødvendig for det. At PR #30s tester i tillegg ville hengt i samme vindu, kan ikke avgjøres fra loggene; F1 er en konkret måte de kunne gjort det på hvis et `#require` feiler.
- **C4 – holder.** 3 av 3 løp med det gamle skriptet siden 29.09 13:16 stoppet likt, uavhengig av gren; PR #30 endrer ifølge oppdraget hverken `ci.yml` eller skriptet. Ingen tallfestet sannsynlighet ut over dette.
- **C5 – holder med moderat belegg.** To grønne løp (5dc229f, 5cf3531) etter ett rødt (b5adebd) på samme gren, uten Swift-endringer mellom rødt og første grønne (CIPhaseDiagnostics, linje 47–49). n = 2. Endringen fjerner ikke nødvendigvis årsaken: ligger den i en test, gir det nye skriptet et 120 s-stopp med stakkprøver i stedet for stillhet, og det har ikke inntruffet to ganger. Ligger den i `swift-package`s videreformidling, er den omgått.
- **C6 – holder sannsynlig, ikke bevist.** 24,0 s (grønn testfase) + 17,3 s (nye suiter lokalt) ≈ 41 s; CI/lokal 1,13 på felles suiter gir ≈ 44 s; høyt anslag 60–100 s. Eneste måling av de nye suitene er lokal, på Swift 6.4-dev i egne prosesser per mål.

---

## 4. Det jeg ikke kunne avgjøre, og hva som skal til

1. **Hvilken prosess som stanset** (testverten eller `swift-package`), og dermed om det er en test på `main` eller SwiftPM som henger. Uten nytt løp: last ned artefakten `ci-logs` for løp 37330064662 (ligger i 7 dager) og kontroller at `test.log` har nøyaktig 32 768 byte fra `Test Suite 'All tests' started` og ender midt i `✔ Test dismissingWhile…`; det bekrefter buffermodellen for PR-løpet (den andre grenen rapporterer det for 37113316662). Med nytt løp: kjør testfasen med det nye skriptet; et nytt stopp gir `ci-logs/test-stall/*.sample.txt` med stakker for inntil fire prosesser etter 120 s. Vil man beholde `swift test`, må testverten i tillegg skrive fortløpende til en egen fil (Swift Testings hendelsesstrøm; `--xunit-output` hjelper ikke, den skrives først ved slutten) så siste test blir synlig; selv ville jeg ikke brukt et løp på det.
2. **Om stoppet er deterministisk for det gamle skriptet.** 3 av 3 er det jeg har; flere løp koster.
3. **Hva som endret seg 26.09 → 29.09.** `main` var grønt 26.09; de to PR-ene var grønne hver for seg 29.09 om morgenen; sammenslåingen `ea558ba` hang. Diffen for #26/#27 ligger ikke her. Et løp av `1d95fc4` (bare #26) ville skilt «kombinasjonen» fra «tilfeldig siden 29.09», men koster et løp.
4. **Om de prosesspawnende suitene på `main`** (ClaudeCodeBridgeTests, CodexAppServerBridgeTests) er kandidaten under «test som henger». Koden ligger ikke i `kilde/`. Doc-kommentaren i BoundedProcessRunner.swift:65–67 beskriver at `FoundationProcessRunner` leser rør først etter avslutning, som er et kjent dødlåsmønster ved mer enn 16 KiB utskrift på macOS; om de testene bruker den og hvor mye de skriver, kan jeg ikke se.
5. **Om PR #30s tester går i CI-miljøet** (Swift 6.2.4, én prosess, tre kjerner). Bare et løp viser det; lokalt er en annen verktøykjede og prosessmodell.
6. **Om Foundations `Process` på Darwin nullstiller signaldisposisjoner** (avgjør alvoret i F4 ved parallell kjøring).
7. **Antall kjerner på løperen** står ikke i loggene; tre er oppdragets tall.

---

## 5. Det jeg kjørte

Alt i Python 3 mot filene i `ci/`, uten nett, uten Swift. Skriptene ligger i `arbeid/`.

| Kommando | Utfall |
|---|---|
| `find . -type f` med størrelser | 25 filer; loggene 409–589 KB; kilde og tester 6–75 KB |
| `python3 arbeid/tell_logg.py ci/CI-LOGG-{36573898495,37113316662,37330064662}-feilet.txt` | Teststegets grenser, siste linje, byteantall fra fire ankre, linjene etter avbruddet |
| Innebygd skript: diff av testutskriften mellom de tre røde (rå og normalisert) | 356 linjer og 32 736 byte i alle; innhold ulikt i UUID/tid/port, like bredder |
| Innebygd skript: normalisert diff grønn mot PR #30 fra `Build complete!` til stopplinja | Bare de fire hodelinjene skiller (75 byte) |
| Innebygd skript: suitestarter med kumulative byte og tid i det grønne løpet; neste 16 384 byte | 18 suiter, 12,2 s; kjøringen 74 239 byte, 21,955 s |
| Innebygd skript: 16 384-grenser regnet bakover fra stopplinja; søk etter nye suitenavn i PR-loggen | 32 768 faller mellom `Linking …` og `Build complete!`; navnene bare i kompileringslinjer |
| Innebygd skript: tidsgap > 50 ms mot byteposisjon, rødt og grønt | Rødt: ett gap, 0,585–0,689 s, ved byte 16 184–16 420; grønt: gap ved trege tester |
| Innebygd skript: XCTest-linjas eget tidsstempel mot mottak | 3,795 / 3,684 / 3,897 s forsinkelse |
| Innebygd skript: opplastings- og opprydningslinjer etter avbruddet | ci-logs.zip 35 938 / 36 211 byte (komprimert); orphan-prosesser som i del 2 spm. 4 |
| Innebygd skript: lokal logg – trinn, verktøykjede, suiter per prosess, suitetider; omregning til CI-tegn og byteanslag | Sju prosesser; Swift 6.4.0-dev; posisjoner som i del 2 spm. 3 |
| Innebygd skript: suitetider lokalt mot CI | 54 felles suiter, 19,0 s mot 21,4 s (1,13×); uteliggere 10,6× og 1,47× |
| Innebygd skript: løperbilde og toolchain i alle fire logger | Samme bilde og versjon i alle |
| `python3 arbeid/analyse.py` (i `ci/`) → `arbeid/analyse-utskrift.txt` | Reproduserer alle tallene over |
| Lesing: `OPPDRAG.md`, `ci.yml`, `test_haven_agentd.sh`, `CI-HISTORIKK-1`, de fem sammendragene (etter del 1), begge `gren-file-provenance-*.log`, alle filene i `kilde/Sources` og `kilde/Tests` (ScheduledEventScheduleTests delvis: 1–222, 514–643, 836–960, 1005–1134, 1245–1565, pluss indeks av alle funksjoner og venteløkker med `grep -n`) | Som i del 1 |

Ikke gjort: ingenting lest utenfor `fabel-ci/`, ingen Swift bygget, ingen nettoppslag (SwiftPM-/xnu-detaljer om buffer og rør er fra hukommelsen og merket som slutning der de brukes).
