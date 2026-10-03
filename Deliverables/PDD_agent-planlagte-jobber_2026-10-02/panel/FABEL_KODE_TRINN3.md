# Fabel: gransking av koden for trinn 3 (cron og planleggeren)

Dato: 03.10.2026. Gransket mot `BRIEF_KODE_TRINN3.md`, kontrakten i `contract/trinn3-cron.md`, styringsdelen i `contract/trinn4-jobber-og-godkjenning.md`, skjemaene `scheduled-job-control-v1` og `scheduled-job-ack-v1`, `fixtures/ScheduledJobs/worker.json`, og T1–T3/T10 i `FORMAALSSPEC.md` §5. Kildene fra `origin/main` `ea558ba` er lest for `ScheduledEventService.swift`, `AgentConfig.swift`, `SubprocessRunner.swift`, `LocalTaskRunner.swift`, `AutomationPolicy.swift`, `HavenAgentMain.swift` (bl.a. `AgentMonitorShutdown`, linje 1166–1196), `Scripts/install-agent-dev.sh`, `Launchd/io.digipomps.haven.agentd.plist` og `Package.swift`.

Alt som står som «målt» er målt her: Linux x86_64, Swift 6.2.3, i min egen mappe `S/fabel-trinn3/kopi/` (kopi av `S/trinn3-bygg-trinn3/`, bygget på nytt fra tom `.build`). Darwin-grenene er bare lest. Jeg har ikke endret noe i `S/trinn3/`, `S/impl/`, `S/koe/`, `S/pdd-cron/` (utenom denne fila) eller byggemappene.

Linjenummer uten filnavn viser til `S/trinn3/Sources/HavenAgentRuntime/ScheduledEventService.swift`.

## Slik prøvde jeg

```
cd S/fabel-trinn3/kopi && . S/swift-tc/env.sh
swift test --no-parallel -Xswiftc -Xfrontend -Xswiftc -disable-cross-import-overlays
→ ✔ Test run with 54 tests in 4 suites passed after 9.977 seconds.   (test-run-1.log)
```

Deretter la jeg til tre egne testfiler i kopien (ikke i `S/trinn3/`):

| Fil | Hva |
|---|---|
| `Tests/HavenAgentRuntimeTests/FabelTests.swift` | f1–f8: stopp etter avbrutt kjøring, stopp midt i en runde, uleselig tilstandsfil, første kjøring på intervall, post uten `countingFrom`, `changedAt` i framtiden, full disk før og etter kjøring (ekte 64k tmpfs montert på `S/fabel-trinn3/tiny`, nå avmontert) |
| `Tests/HavenAgentRuntimeTests/FabelCronDifferensial.swift` + `S/fabel-trinn3/lag_differensial.py` | `CronSchedule` mot kontraktens `cron_reference.py` på tilfeldige uttrykk, 16 soner, 16 starttider: 600 + 400 tilfeller (frø 3 og 7), hvert med 30 tidspunkt, telling, korteste avstand og baklengs søk |
| `Tests/HavenAgentRuntimeTests/FabelProcessTests.swift` | hva barnet faktisk arver fra arbeideren (fildeskriptorer, signalmaske, ignorerte signaler) |

Resultat (test-run-2.log, diff7-test.log): f1, f7, f8 grønne; f2, f3, f4, f5, f6 **røde** — det er funnene under. Differensialtesten: 600 av 600 og 400 av 400 like, 0 avvik. Forfatterens 54 tester kjørt 6 ganger på rad (stabilitet.log): 6 av 6 grønne; én gang til under 3× CPU-overbelastning (6 travle løkker på 2 kjerner): grønn, 20 s mot 10 s.

## Må rettes før koden legges i en PR

### 1. Stoppes arbeideren midt i en runde, tas tidspunktet til neste forfalte hendelse og merkes `interrupted`

**Fil og linje:** `ScheduledEventService.swift` 450–452 (`for id in dueIDs { await runEvent(id: id) }`) og 506–529 (`runEvent` tar tidspunktet på disk før `execute`).

**Hva skjer.** `stop()` kansellerer arbeideroppgaven. Kanselleringen stopper den kommandoen som går (riktig, utfallet `interrupted`). Men løkka i `runDueEvents` går videre til neste forfalte id, `runEvent` skriver `lastOccurrence`/`currentRun` til disk, og `BoundedProcessRunner.run` ser at oppgaven alt er kansellert (`withTaskCancellationHandler` kaller `onCancel` straks), starter prosessen og dreper den i første avlesning. Den andre hendelsens tidspunkt er brukt opp uten at noe ble gjort, utfallet blir `interrupted`, og `attention.kind: failed` gir en falsk sak i menylinjen. Dette skjer hver gang launchd stopper planleggeren (installasjon, utlogging) mens to hendelser er forfalt i samme runde, for eksempel kl. 09:00 når korrespondansesjekken og fristvarselet begge er forfalt.

**Målt** (`FabelTests.f2`): to cron-hendelser `*/30 * * * *`, `a-slow` (sleep 30) og `b-say` (echo), arbeider startet, klokke satt til 10:30, `stop()` når `a` kjører:

```
✘ Expectation failed: (b.runCount → 1) == 0
↳ b ble startet og avbrutt: runCount 1, lastOutcome interrupted, attention failed
✘ (b.lastOccurrence → "2026-10-05T10:30:00Z") == nil
✘ (b.nextFireAt → "2026-10-05T11:00:00Z") == "2026-10-05T10:30:00Z"
```

**Hva som bør stå.** Ta ikke et tidspunkt når oppgaven er kansellert: `guard !Task.isCancelled else { return }` øverst i `runEvent` (før `plan`/`persist`), og `if Task.isCancelled { break }` i løkka på linje 450. Da blir `b` liggende som forfalt (`nextFireAt` 10:30) og kjøres av neste arbeider, som kontrakten vil («Samme tidspunkt kjøres aldri to ganger», «ingenting tapt»). Legg f2-testen inn i `ScheduledEventScheduleTests`; ingen av de 54 testene ser dette, fordi alle som stopper arbeideren har bare én hendelse.

### 2. Blir tilstandsfila uleselig mens arbeideren går, står planleggeren stille for alltid, mens livstegnet fortsetter

**Fil og linje:** `ScheduledEventService.swift` 426–429 (`hasUnsavedChanges` → `persist()` eller `return`), 863–884 (`persist` → `store.update`), 219–233 (`ScheduledEventStore.update` leser med `read()` før den skriver).

**Hva skjer.** `update` krever at fila kan dekodes før den skrives. Kan den ikke det (fila er redigert for hånd, tømt, eller skrevet av noe annet), kaster `persist`, `hasUnsavedChanges` blir sann, og hver runde ender i `return` på linje 429 før noe kjøres. Ingen hendelse kjøres, ingenting skrives, `lastError` sier ingenting — og `worker.json` skrives videre hvert 30. sekund av den uavhengige oppgaven, så saken «Planleggeren går ikke» (trinn 4) kommer aldri. Koden på `main` oppfører seg bedre her: `runDueEvents` ignorerte lesefeilen og `persist` → `store.write` skrev fila på nytt fra minnet, så den helbredet seg selv. Ved *start* er det i orden: `store.load()` kaster, arbeideren avslutter, launchd starter den igjen, livstegnet uteblir, og feilen er synlig.

**Målt** (`FabelTests.f3`): arbeider startet med `*/30 * * * *`, fila overskrevet med `{ ikke json`, klokke til 10:30, 1,3 s venting:

```
✘ (commands.count → 0) == 1
↳ ingenting kjørte: commands=0, status=scheduled, lastError=nil
✘ (text → "{ ikke json").hasPrefix("[")        ← fila er fortsatt uleselig
   (later > early var sann: livstegnet ble skrevet videre)
```

**Hva som bør stå.** I `ScheduledEventStore.update` (eller i `persist`): kan fila ikke dekodes (`DecodingError`, ikke I/O-feil), regn den som tom og skriv `mine` — det er det `main` gjorde, og det er det eneste stedet som har en god kopi. Skriv i tillegg årsaken i `lastError` på hendelsene, så `schedule-list` viser det. Og uavhengig av dette: når `hasUnsavedChanges` har stått i mer enn noen runder, bør livstegnet stoppe (eller `worker.json` si at arbeideren står), ellers lyver livstegnet også ved full disk.

### 3. Første kjøring av en intervallhendelse teller alle intervaller siden `firstFireAt` som passerte — og gir falsk sak for daglige hendelser

**Fil og linje:** `ScheduledEventService.swift` 601–623 (`plan`, intervallgrenen). Kontrakt: `trinn3-cron.md` «Regler for kjøring», punktene «Passerte tidspunkt (F3)» og «Intervall uten cron».

**Hva skjer.** For cron regner koden fra `countingFrom` («ingenting kjøres på etterskudd første gang», linje 715–719). For intervall finnes ingen slik regel: en hendelse som aldri har kjørt har `nextFireAt = firstFireAt`, og første `plan` teller `floor((nå − firstFireAt)/intervall)` som passerte. Installasjonsskriptet skriver `firstFireAt` ved installasjon (jf. eksempelet i `Docs/ScheduledEvents.md`, `2026-10-03T08:00:04Z`). Så lenge den nye arbeideren overtar tilstandsfila fra den gamle, er `nextFireAt` fersk og ingenting telles. Men startes den nye arbeideren uten tidligere tilstand for hendelsen — ny tilstandsmappe (T10 bruker en slik for den eldre binæren; gjøres det samme med den nye, eller tømmes `State/`), eller en intervallhendelse legges inn i `config.json` med en `firstFireAt` som er dager gammel — får fristvarselet (daglig, `intervalSeconds: 86400`) `missedCount` lik antall døgn siden `firstFireAt` og `attention.kind: missed`: saken «Planlagt jobb ble passert» vises uten at noe ble passert.

**Målt** (`FabelTests.f4`): `firstFireAt` 01.10 07:00, intervall 86 400, første runde 05.10 08:00, ingen tidligere tilstand:

```
✘ (record.missedCount → 4) == nil
↳ første kjøring telte 4 passerte, attention=missed, lastOccurrence=2026-10-05T07:00:00Z
```

**Hva som bør stå.** Koden følger ordlyden i intervallpunktet («Starter en kjøring senere enn planlagt, legges antall hele intervaller … til missedCount»), men bryter grunnregelen i F3-punktet, som bare er skrevet for cron. Dette må kontrakten si. Mitt råd: en post uten `lastOccurrence` og med `runCount == 0` har aldri hatt et planlagt tidspunkt som ble passert — kjør den én gang uten å telle (`missed: 0`), uansett intervall eller cron. Én `guard record.lastOccurrence != nil || record.runCount > 0 else { return RunPlan(occurrence: planned, missed: 0, ...) }` foran linje 612. Velger Kjetil heller ordlyden som den står, må T10 forvente saken, og dokumentet må si at en ny tilstandsmappe gir en passeringssak første gang.

## Bør rettes

1. **En post uten `countingFrom` som tas opp fra fila, kjører aldri igjen før omstart** (`cronBase` linje 630: `?? current`; `adopt` 853–860). Skriver en eldre binær fila på nytt mens den nye arbeideren går (eldre `schedule-stop` skriver hele fila, kontrakten linje 18–20), er `countingFrom` og `lastOccurrence` borte. Da er `base = nå`, `last(after: nå, through: nå)` er nil, `refreshNextInstant` flytter `nextFireAt` fram, og det gjentar seg hver runde. Målt (`FabelTests.f5`): fire runder 10:30–12:00, `kjørte bare ved []; nextFireAt=2026-10-05T12:30:00Z, countingFrom=nil`. Utenfor kontraktens forutsetninger (blandede binærer), men rettingen er én linje: kjør `alignSchedule` på det som tas opp i `adopt`, eller la `cronBase` bruke `lastOccurrence` når `countingFrom` mangler.

2. **`changedAt` i framtiden i styringsfila gir `lastOccurrence` i framtiden for intervallhendelser** (linje 604–607: `planned = resumedAt` etter at `planned <= current` alt var sjekket). Målt (`FabelTests.f6`): `lastOccurrence ligger i framtiden: 2026-10-05T12:00:00Z` med klokke 10:40. Klem `resumedAt` til `min(resumedAt, current)` i `runEvent`.

3. **`recoverInterruptedRun` (691–704) lar `lastLog` og `lastOutput` stå fra forrige kjøring.** Menyen og `schedule-list` viser da forrige kjørings sammendrag og loggsti sammen med utfallet `interrupted`. Sett `lastLog` til `<fileStamp(currentRun.startedAt)>.log` i hendelsens loggmappe (den fila finnes), og `lastOutput = nil`.

4. **`BoundedProcessRunner.swift` 191–195: den siste `kill(group, SIGKILL)` sendes også når løkka sluttet fordi gruppen var tom.** Mellom `kill(group, 0) != 0` og `kill(group, SIGKILL)` kan en ny, urelatert prosess få samme pid og bli gruppeleder. Vinduet er mikrosekunder, men følgen er at noe fremmed drepes. Send bare når løkka sluttet på tid. Samme fil, linje 152: `group = -processID` — en vakt `guard processID > 1` koster ingenting, mens `kill(-1, SIGKILL)` ville drept alt brukeren eier.

5. **Linje 251: bare seks signaler settes til standard.** swift-tools-support-core gjør `sigfillset` minus `SIGKILL`/`SIGSTOP` for samme formål. Arbeideren ignorerer bare `SIGINT`/`SIGTERM` i dag (`AgentMonitorShutdown`), så det virker nå; `sigfillset` gjør det uavhengig av hva som ignoreres senere.

6. **Testene med ekte kommandoer deler et tak på 0,5 s for alle hendelser** (`ScheduledEventScheduleTests.swift` linje 113, brukt i 928, 960, 1058). `say` og `fail` (`/bin/sh -c echo …`) må da bli ferdige på under et halvt sekund for at `lastOutcome == .ok`/`.failed` skal holde. Målt grønt her både tomgang (6 av 6) og under 3× CPU-last, så faren er liten, men den finnes på en Mac som samtidig bygger. Taket er eneste vei til tidsgrenser under 10 s (valideringen krever ≥ 10). Legg den hengende hendelsen i sin egen test med lavt tak, og gi de andre et tak på noen sekunder.

7. **Tester som mangler, og som ville funnet funnene over:** stopp midt i en runde med to forfalte hendelser (må 1), uleselig fil mens arbeideren går (må 2), første kjøring på intervall med gammel `firstFireAt` (må 3), `schedule-stop` etter at arbeideren ble drept midt i en kjøring (min f1 — den er grønn, fordi `persist` (867–876) henter stoppet tilbake fra fila etter at `settle` hadde satt `scheduled`; det bør stå en test på det, for det er lett å «rydde» bort merge-regelen uten å merke det), og en test på at tallene i kontrakten faktisk er standardverdiene (`BoundedProcessLimits()` 8 MiB, 2000 tegn, 5 s; `ScheduledEventService.logsKeptPerEvent` 50, 30 døgn) — i dag prøves grensene bare med 100 000/200 000 byte.

8. **Styringsfil med `stopped` for en fast hendelse** (linje 482): hendelsen kjøres aldri, status står som `scheduled`, ingenting sies. Kontrakten sier faste hendelser bruker bare `active`/`paused`. Enten skriv `lastError`, eller la kontrakten si at `stopped` på en fast hendelse behandles som pause.

9. **Uleselig styringsfil** (484–491): koden kjører ikke og skriver `lastError` («unknown means no»). Rimelig, men kontrakten for trinn 3 sier ikke noe om det, og det gir ingen sak fra arbeideren — bare trinn 4-leverandøren vil gjøre kilden `unreadable`. Kontrakten bør si det.

10. **Id-er som ikke er filnavn-trygge** (`ScheduledJobStateFiles.isFileSafeID`: små bokstaver, sifre, `._-`, ≤ 64) kan hverken settes på pause eller kvitteres: `control`/`ack` leses som `.missing`. Riktig etter skjemaet, men `Docs/ScheduledEvents.md` sier det ikke, og `config.json` har ingen regel for id-er (kontrakten linje 112 sier det selv).

11. **`Etc/GMT+2` godtas** som tidssone (har skråstrek og finnes i tzdata), selv om kontrakten avviser «avstander». Harmløst; nevnes så ingen tror `GMT+2`-regelen dekker det.

12. **`timeZone` uten `cron`** godtas stille. Trolig en skrivefeil hos den som konfigurerer; en feilmelding er billig.

13. **`stopEvent` på arbeiderens egen instans mens `hasUnsavedChanges` er sann** (403–411): `adopt(stored)` tar fila (eldre) over minnet (nyere) for alle hendelser, og det usparte går tapt. Når ingen kaller `stopEvent` i arbeiderprosessen i dag; trinn 5 (kontrollbroen) kan komme til å gjøre det. Ta bare den ene posten inn fra `stored`, ikke alle.

14. **Dokumentet:** sier ikke at passeringer telles høyst 10 000 per runde (`maximumMissedPerRound`), ikke regelen i punkt 10, og «installerer den» om plisten stemmer bare delvis: `install-agent-dev.sh` skriver plisten fra repoet bare når `~/Library/LaunchAgents/…scheduler.plist` mangler (`ensure_plist`); en eksisterende plist rører den ikke, og da er ikke `Launchd/…plist` i bruk. Det er et forsvarlig valg, men dokumentet og kontraktens «installerer den» bør si det.

15. **Linux-observasjon, ikke macOS:** barnet arver alle fildeskriptorer uten `O_CLOEXEC` fra arbeideren (målt: 12 rør-deskriptorer fra testprosessen, se `FabelProcessTests`). På macOS lukker `POSIX_SPAWN_CLOEXEC_DEFAULT` dem. Låsene arves ikke på noen av plattformene (de åpnes med `O_CLOEXEC`). Bare viktig om noen skulle kjøre arbeideren på Linux.

## Kontrollert og funnet i orden

- **Aldri samme tidspunkt to ganger.** `lastOccurrence`/`currentRun` skrives før `execute` (506–514); feiler skrivingen, startes ikke kommandoen og posten rulles tilbake i minnet (515–520). Målt med ekte full disk (64k tmpfs, `FabelTests.f7`): ingenting kjørte mens disken var full, én kjøring etter at den ble ledig, `lastOccurrence` 10:30, `runCount` 1. Full disk *etter* kjøringen (`f8`): på disk står `running`; neste arbeider gir `interrupted`, `runCount` 1, `nextFireAt` 11:00, ingen ny kjøring. Arbeideren drept før skrivingen → tidspunktet står igjen og kjøres; etter skrivingen → `recoverInterruptedRun`, ikke gjentatt (forfatterens tester, og mine).
- **`schedule-stop` mot arbeideren.** Begge går gjennom samme `flock` på `scheduled-events.json.lock`; `persist` beholder `stopped` fra fila (867–876), `stopEvent` endrer bare én post på plass. Stopp mens kommandoen går (forfatterens test) og stopp etter at arbeideren ble drept midt i en kjøring (min f1) gir begge `stopped` til slutt. `schedule-list` leser uten lås, og `.atomic`-skrivingen gir enten gammel eller ny fil.
- **Hva som slipper til ved `await`:** bare `stopEvent`, `snapshot`, `start`, `stop` på samme aktør; `runDueEvents` er vernet av `isRunningDueEvents`. Ingen av dem endrer `records` på en måte `persist`-sammenslåingen ikke tåler, med unntaket i «bør» 13.
- **Cron-reglene.** Fasiten (22/15/18/8) går gjennom, og 1000 tilfeldige uttrykk mot `cron_reference.py` i 16 soner (bl.a. Lord_Howe, Chatham, St_Johns, Kathmandu, Santiago, Havana, Casablanca, Tehran) gir 0 avvik på tidspunkt, telling, korteste avstand og baklengs søk (`last`). Løpende/fast-regelen, 0 og 7 som søndag, dag-eller-ukedag, strengt «etter», åtte år, heltallsregningen og `monthAndDay` (Hinnants algoritme) er lest og stemmer.
- **Reglene i kontrakten:** passerte tidspunkt (én kjøring for det siste, resten telt; første gang fra `countingFrom`), `attention` (`failed` foran `missed`, `missed` bare ved korteste avstand ≥ 23 t, `since` beholdes), kvittering (`throughOccurrence ≥ missedLatest` nuller tellingen), `firstFireAt` holder igjen (`notBefore = first − 1 s`), endret uttrykk eller sone starter tellingen på nytt (signaturen bruker det normaliserte uttrykket, så blanke endrer ingenting), `once` og `count` med cron, pause (beholder `nextFireAt`, kjøres ikke; `resume` regner fra `changedAt`; intervall kjøres straks etter `resume` og forsinkelsen regnes derfra), tidsgrense `min(tak, egen eller 900)`, 10–3600, tittel ≤ 40 tegn på én linje, loggtak 8 MiB/2000 tegn/30 døgn/50 filer, SIGTERM så SIGKILL etter 5 s, én om gangen, én arbeider (`flock` `LOCK_EX|LOCK_NB`, `O_CLOEXEC`), livstegn hvert 30. s fra egen oppgave også mens en kommando går, `worker.json` lik eksempelet i kontrakten.
- **`BoundedProcessRunner` på Linux:** egen prosessgruppe, `/dev/null` som stdin, stdout/stderr til loggfila med `O_APPEND`, tom signalmaske og standard `SIGTERM` selv når forelderen ignorerer det (målt: `SigBlk 0`, `SigIgn 0` i barnet), låsene arves ikke (målt), `waitpid` med `WNOHANG`/`EINTR`, barnet høstes (ingen zombie), 128 + signal ved signaldød, fortsettelsen gjenopptas nøyaktig én gang (tråden returnerer eller kaster, `Result` fanger begge), kansellering før eller under kjøring gir `interrupted`. Loggmappe som ikke kan lages eller fil som ikke kan åpnes gir `logUnavailable` → utfallet `failed` med `lastError`, og tidspunktet er tatt (ikke gjentatt).
- **Eldre agent og kallsteder.** Alle nye felt i `ScheduledEventDefinition` og `ScheduledEventRecord` er valgfrie; `repeatMode`, `action.kind` og `status` har ingen nye verdier; `JSONEncoder` utelater nil, så en hendelse uten cron skrives som før. `AgentConfig` på `main` trenger ingen endring (`scheduledEvents: [ScheduledEventDefinition]?`, syntetisert `encode`). Init-signaturen er bakoverkompatibel (`processRunner` ble valgfri med samme navn; nye parametre har standardverdier); `start`/`stop`/`stopEvent`/`snapshot`/`runDueEvents`/`ScheduledEventStore.load` er uendret. De tre testene på `main` går grønt i trinn3-bygget. Kallstedene på `main` er bare `HavenAgentMain.swift` 339–380 og testen; `AgentRuntime.swift` bruker ikke planleggeren.
- **Patchene** legger seg rent på kopier av filene fra `main` (`patch -p1 --dry-run`, ingen fuzz). `HavenAgentMain`: `logsDirectory:` finnes i den nye init-en, `paths.logsDirectory` brukes alt på `main` linje 105, `persistConfiguration: false` for `schedule-stop` er riktig (uten den ville `schedule-stop` skrevet hele fila). Installasjonsskriptet: `ensure_plist` kalles før `bootout`, `[[ -f … ]] && return 0` er ikke siste kommando i funksjonen (så zsh' `ERR_EXIT` slår ikke til), plistens sti `…/HAVENAgent/bin/haven-agentd-scheduler` stemmer med `BIN_DIR` og produktnavnet i skriptet.
- **Dokumentet** stemmer med koden på alt jeg kunne lese: at arbeideren ignorerer `SIGTERM`/`SIGINT` (`AgentMonitorShutdown` gjør `signal(…, SIG_IGN)`), rekkefølgen «skriv før start», pause- og kvitteringsreglene, loggtakene, låsen, livstegnet, hva som skrives per hendelse. Avvikene står i «bør» 14.
- **Stabilitet:** 6 av 6 kjøringer grønne, pluss én under 3× CPU-last.

## Ikke kontrollert (kan bare måles på en Mac)

- **Darwin-grenene kompilerer ikke her.** `posix_spawnattr_t?`/`posix_spawn_file_actions_t?` med `&`-overlevering, `POSIX_SPAWN_CLOEXEC_DEFAULT`, `Int16(truncatingIfNeeded:)` til `posix_spawnattr_setflags`, `sigset_t()` som `UInt32`, `stat()`, `mode_t` som `UInt16`, `open(_:_:_:)`, `flock`, `rename`, `strerror`, `errno`, `EWOULDBLOCK`. Lest som kompilator: det er samme idiom som swift-tools-support-core bruker på Darwin (bl.a. `var attributes: posix_spawnattr_t? = nil`, `CLOEXEC_DEFAULT|SETSIGMASK|SETSIGDEF|SETPGROUP`), så jeg venter at det går, men det må bygges med Xcodes Swift. Streng samtidighetskontroll (Swift 6-modus) er prøvd her med `swift-tools-version: 6.0` uten en eneste advarsel; forskjellen på macOS er bare Darwin-API-ene og Foundation-typenes `Sendable`-merking.
- **At `POSIX_SPAWN_CLOEXEC_DEFAULT` faktisk lukker alt unntatt 0/1/2**, og at `ProcessInfo.systemUptime` ikke går under søvn på macOS (Apples dokumentasjon sier det; ikke målt). Kontrakten/dokumentets «regnes mens Macen er våken» hviler på det.
- **De ekte `ShortcutRunner` og `AppleScriptRunner`** (ikke blant kildene; stedfortredere i `sky/stubs/`). Leser de for eksempel `outputPath` etter kjøringen, eller forventer rør, endrer `BoundedProcessRunner` oppførselen deres. For `localTask`, som de faste programmene bruker, er det ingen slik fare.
- **Patchene er ikke kompilert eller kjørt** (zsh, `plutil`, `launchctl`). At den installerte plisten i `~/Library/LaunchAgents/` har samme oppsett som malen (`bin/`-stien), kan jeg ikke se herfra.
- **Eldre binær mot nye filer (T10)** er bare etterlignet med håndkopierte strukturer i testen; den ekte binæren fra 26.09 må kjøres.
- **`flock` mellom to prosesser** er bare prøvd mellom to deskriptorer i samme prosess (det gir `EWOULDBLOCK` på Linux og BSD); APFS, filrettigheter under launchd, og tzdata-forskjeller mellom ICU (Darwin) og systemets `zoneinfo` (Linux) er ikke målt.
- **Flakkhet på en treg Mac** er bare vurdert ved lesing (bør 6) og under kunstig CPU-last på Linux.
- **At `Tests/HavenMacAutomationTests/` og `Tests/HavenAgentRuntimeTests/Fixtures/` finnes på `main`** slik `Package.swift` krever (`resources: [.copy("Fixtures")]` er alt der).

## Vedlegg: hvor det jeg skrev ligger

- `S/fabel-trinn3/kopi/Tests/HavenAgentRuntimeTests/FabelTests.swift`, `FabelCronDifferensial.swift`, `FabelProcessTests.swift`
- `S/fabel-trinn3/lag_differensial.py`, `differensial-3.json` (600), `differensial-7.json` (400)
- `S/fabel-trinn3/test-run-1.log` (54 grønne), `test-run-2.log` (63 med mine; f2–f6 røde), `diff7-test.log`, `stabilitet.log`
- `S/fabel-trinn3/patchtest/` (filene fra `main` med patchene lagt på)
