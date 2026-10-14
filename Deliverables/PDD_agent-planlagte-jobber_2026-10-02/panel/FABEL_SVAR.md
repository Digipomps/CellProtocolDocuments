# Fabel: uavhengig gransking av «planlagte jobber i HavenAgentD»

Gransket 02.10.2026 av en uavhengig Claude-tråd («Fabel») mot `panel/BRIEF.md`. Teksten under er Fabels svar, uendret.

Alle stier er relative til worktreet `HavenAgentD/.worktrees/main-20260922/`. Løperen `Claude outputs/agentd-runner.command`, scheduler-plisten på Macen, `Contracts/agent-challenge-v1.schema.json` og `ActionDispatcher`/`LaunchAgentTemplate` lå ikke i utvalget Fabel fikk; alt om dem er merket [ikke belagt].

---

## P1 — Er D5 forenlig med sikkerhetsmodellen, og er den minst farlige formen?

**Konklusjon:** D5 bryter ikke bokstaven i `SecurityModel.md` (forbudene gjelder *fjernforespørsler*), men den gir for første gang en lokal skriveflate generell skalltilgang, og slik den er skissert er den ikke den minst farlige formen: det «faste programmet» ligger i en mappe Losen selv skriver til, så policyens garanti er tom.

**Belegg og argument**

1. Hva modellen faktisk forbyr: «Never execute raw shell commands from a remote request» og «The cloud does not get a general scripting channel» [belagt: Docs/SecurityModel.md:11, 15-17]. `AgentJobs.md` erkjenner allerede en lokal tillitsflate («any process running as the user can register a job») [belagt: Docs/AgentJobs.md:230-232], men den flaten gir bare policy-handlinger [belagt: Docs/AgentJobs.md:236-238; Sources/HavenAgentRuntime/JobStore.swift:195-214]. D5 er den første lokale flaten der det en skriver legger inn *er* programmet. `ScheduledEvents.md` sier eksplisitt at vilkårlig skall er utelukket med vilje [belagt: Docs/ScheduledEvents.md:54-57, 65-66]. D5 oppfyller den setningen formelt og opphever den reelt.

2. Losen er ikke «lokal» i modellens mening: instruksjonene kommer fra en skymodell som leser post, nett og repo. Prompt-injeksjon i Losen = kjøring som Kjetil, uten gjennomgang. Det er nøyaktig kanalen linje 11 skulle hindre. Kjetil har valgt dette; det må stå i klartekst (se P6).

3. Hvem kan skrive til kømappen: alt som kjører som Kjetils uid, og enhver Claude-økt (sky eller lokal) med mappen tilkoblet. Ingen eier-, rettighets- eller symlenkekontroll er beskrevet i D5. Hva løperen sjekker i dag: [ikke belagt] (skriptet er ikke i repoet).

4. **Svakeste punkt:** `losen-queue-ensure` får «fast program og faste argumenter» [AutomationPolicy sjekker bare at stien er absolutt og én linje; belagt: Sources/HavenMacAutomation/AutomationPolicy.swift:219-230]. Programmet er dagens løper i `Claude outputs/` — en mappe Losen skriver i. Den som kan skrive køen kan altså også bytte ut løperen. Policyens eneste reelle vern (fast kode) er dermed ikke der. Nest svakest: `queue/*.sh` plukkes i navnerekkefølge uten «ferdig skrevet»-protokoll (jf. `job.json`-sist-regelen i [belagt: Docs/AgentJobs.md:54-58]); et halvskrevet skript kan kjøres. Logg og `JOB-DONE`-markører ligger i samme skrivbare mappe, så en ferdigmelding kan forfalskes.

5. Rettigheter i scheduler-veien er dessuten videre enn D4 antyder: `execute` kjører alt med `origin: .local` og sender `inputPath`/`arguments` videre [belagt: Sources/HavenAgentRuntime/ScheduledEventService.swift:276-291; Sources/HavenAgentRuntime/AgentConfig.swift:11-28]. `.local` hopper over `allowedForRemoteExecution` [belagt: AutomationPolicy.swift:161-162, 180-182], og et AppleScript-argument uten egen constraint får 512 fri tegn [belagt: AutomationPolicy.swift:191]. En Losen-opprettet jobb får altså mer enn en fjernintent. `requiresUserSession` håndheves ikke noe sted i de opplastede kildene [belagt: grep, bare deklarert i AutomationPolicy.swift:79, 117].

**Tryggere form som fortsatt lar Losens skript kjøre uten at Kjetil starter noe** (i stigende kostnad):

- a) Flytt løper og ensure-skript til `~/Library/Application Support/HAVENAgent/bin/` (bare installskriptet skriver der), og pin sha256 i `LocalTaskDefinition` (nytt felt, sjekket i `authorize`). Løperen nekter symlenker, filer med gruppe/andre-skriv, filer eid av annen uid, og kjører bare `*.sh` med sidefil `.ready` skrevet sist. Logg og markører under `Logs/`, ikke i køen. Dette koster lite og lukker punkt 4.
- b) Egen launchd-jobb for løperen (`KeepAlive`) i stedet for ensure-hvert-minutt. Fjerner hele barn-av-scheduler-problemet (P4/P5) og trenger én `launchctl bootstrap` én gang — samme engangsinnsats som policy-redigeringen D5 krever uansett.
- c) Egen macOS-bruker (`losen`) med egen deploy-nøkkel og smal `gh`-token, køen i en delt gruppemappe. Dette er den eneste formen som *begrenser skaden* av vilkårlig skall (ingen tilgang til Kjetils nøkkelring, Dokumenter, korrespondansenøkler). Anbefales som mål, ikke som G2-krav.
- d) Mal-allowlist med constrained args (gjenbruk av `StringConstraint`) for de vanlige jobbene (build, test, push mot fast remote). Fjerner skallet. Trolig for stramt nå; bør stå som sluttilstand.

Dynamiske jobber i D4 bør bare ta `{kind, id}` som `AgentJobAction` gjør [belagt: Sources/HavenAgentRuntime/AgentJobModels.swift:109-116], ikke `arguments`/`inputPath`.

---

## P2 — Kappløp i D3

**Konklusjon:** Dagens kode har minst fem kappløp mellom arbeider og CLI/MCP, og D3 (les–endre–skriv for én post) løser bare ett av dem; den robuste formen er én skriver per fil: arbeideren eier kjøretilstanden, kontrollprosessene legger kommandoer eller ønsket tilstand i egne filer.

**Kappløpene, med linjer**

1. Hele-fil-tilbakeskriving: `persist()` skriver hele `records` [belagt: ScheduledEventService.swift:293-295] både ved start av kjøring (235) og slutt (268). Alt en annen prosess endret på *andre* poster mellom innlastingen (213-215) og 268 overskrives. Med D5 er vinduet hvert minutt; med et bygg, minutter. D3 fikser dette.

2. Stopp som ikke biter: arbeideren laster fila (213), CLI stopper hendelsen rett etter, `runEvent` sjekker status i minnet (230-231) og kjører én gang til; først etter kjøringen oppdages stoppet (248-253). Testen `workerObservesStopWrittenByAnotherProcess` dekker ikke dette: `firstFireAt` er 2099 og ingenting kjøres [belagt: Tests/HavenAgentRuntimeTests/ScheduledEventServiceTests.swift:102, 114-121]. Også sjekken på 248 er ikke-atomisk mot skrivingen på 268: et stopp som lander mellom dem forsvinner. `pause` (ny i D3) har ingen tilsvarende sjekk i det hele tatt.

3. `start()` fra ikke-arbeidere: `schedule-stop` kaller `start` med `persistConfiguration` = true [belagt: Sources/HavenAgentD/HavenAgentMain.swift:374-378] og skriver fila (168-170), og flipper enhver `.running` til `.scheduled` med feilmeldingen «Worker stopped while the event was running» [belagt: ScheduledEventService.swift:161-165] — mens arbeideren faktisk kjører den. Fila sier da «scheduled» med forfalt `nextFireAt`; dør arbeideren i det vinduet, kjøres hendelsen igjen. Med MCP-prosesser som kaller `start` skjer dette ved hvert verktøykall. Dagens `start` dropper også alle poster som ikke står i config (156-167) — det D3 retter.

4. Stille overskriving ved dekodefeil: `try? await store.load()` (213) beholder gammel tilstand hvis fila ikke kan dekodes, og neste `persist` overskriver den. Ny status-verdi (`paused`) eller nytt felt gjør at en *gammel* binær (rollback-stien i installskriptet finnes [belagt: Scripts/install-agent-dev.sh:288-295]) sletter nye poster uten en feilmelding.

5. To arbeidere: `guard worker == nil` (172) er per prosess. Ingen låsfil hindrer en manuell `schedule-worker` ved siden av launchd-jobben. Begge kjører forfalte hendelser.

6. Krasj mellom 235 og 268 gir kjøring på nytt ved omstart (161-165): minst-én-gang. `AgentJobs.md` velger motsatt («blocked», ikke gjenta usikre bivirkninger) [belagt: Docs/AgentJobs.md:92-93]. F3 sier «aldri flere ganger for samme tidspunkt». De tre er ikke forenlige i dag.

**Enklere og mer robust form**

- Én skriver per fil. Arbeideren eier `State/ScheduledEvents/<id>.runtime.json`. Kontrollprosesser (CLI, MCP, kontrollbro) skriver bare `<id>.spec.json` (definisjon + `desiredState: active|paused|stopped|removed`) atomisk. Ingen prosess gjør les–endre–skriv på en annens fil; ingen lås trengs. Arbeideren, som alt poller hvert sekund (173-182), ser spec-endringer, og sletter begge filer når `removed` er bekreftet. Det er samme mønster som `job.json`/`State/agent-jobs.json` [belagt: Docs/AgentJobs.md:59-60] og i tråd med at daemonen skal være effektgrensen, ikke MCP-adapteren [belagt: Docs/SecurityModel.md:73-77].
- Én arbeider: låsfil med pid i `State/`, nektet oppstart ved levende lås.
- Idempotens per forekomst: lagre `lastOccurrence` (planlagt tidspunkt) og nekt kjøring av samme forekomst to ganger — mønsteret finnes alt i `PersonalButlerScheduleService` (`lastScheduleSlot`) [belagt: Sources/HavenAgentRuntime/PersonalButlerScheduleService.swift:351-358]. Da blir F3 testbar og krasj-sikker.
- Fjern running→scheduled-resetten fra `start` for ikke-arbeidere; bare arbeideren får gjøre den, og da til «usikker» (vis som sak), ikke til ny kjøring, med mindre jobben er merket idempotent.

---

## P3 — Sommertid og `Calendar.date(from:)`

**Konklusjon:** Reglene er rimelige, men D1 definerer riktig svar som «det `Calendar.date(from:)` gir», og det gjør T1 tautologisk og resultatet avhengig av udokumentert Foundation-oppførsel; regelen må uttrykkes som instanter og implementeres eksplisitt.

**Belegg**

- Antakelsene om `date(from:)` i hull og dobbelttime er [ikke belagt]: Darwin-Foundation og swift-foundation har hatt ulik historikk, og API-et som *har* definert semantikk er `nextDate(after:matching:matchingPolicy:repeatedTimePolicy:)`. Design som hviler på default-oppførsel i `date(from:)` må enten bruke det eksplisitte API-et eller måle begge instanter selv via `TimeZone.secondsFromGMT(for:)`.
- Hull 28.03.2027 (02:00 CET → 03:00 CEST): «kjør på tidspunktet `date(from:)` gir». Hvis det blir 03:30 CEST, kolliderer `30 2 * * *` og `30 3 * * *` i samme minutt — to kjøringer, eller én hvis dedup på forekomst finnes (den finnes ikke i dag; `nextFireAt` er eneste nøkkel [belagt: ScheduledEventService.swift:216-223]). Vixie cron-regelen («fast klokkeslett i hullet kjøres én gang straks etter hullet») er den som bør stå, som instant: 2027-03-28T01:00:00Z for `30 2`.
- Dobbelttime 25.10.2026 (03:00 CEST → 02:00 CET): «første forekomst» er riktig for fast klokkeslett, men for `* * * * *` (D5 kjører hvert minutt) betyr dag-for-dag-bygging av lokale tider at 02:00–02:59 bare gir én instant hver — køoppvekkeren pauser én time. Regel: minuttfelt med jokertegn kjører i begge pass; fast klokkeslett én gang.
- Datamodellen passer ikke: `firstFireAt` er påkrevd og valideres [belagt: ScheduledEventService.swift:12, 301]; `intervalSeconds > 0` kreves for alt annet enn `once` [belagt: 305-307]. Cron-poster må enten få egen gren i `validate` eller MCP må fabrikkere felt. `scheduleNext` regner fra `now()` [belagt: 271-274] — for cron må neste regnes fra forekomsten, og forekomster som passerer *under* en lang kjøring må telles (som «overran», ikke «slept»; se D2).
- Uendelig løkke: `0 0 31 2 *` (aldri gyldig) i «gå dag for dag» uten øvre grense henger arbeideren — og dermed alle hendelser, siden løkka er sekvensiell (224-226). Avvis ved opprettelse og bind søket (f.eks. 8 år).
- Tidssone: `TimeZone(identifier:)` gir nil for ugyldig navn — valider ved opprettelse. `timeZone == nil` må bety eksplisitt lagret «Europe/Oslo», ikke prosessens `.current`, som følger systemets sone.
- Alternativ som slipper hele problemet: launchd `StartCalendarInterval` gjør «fast klokkeslett, én oppsamlet kjøring ved oppvåkning» innebygd, men bruker systemsonen og passer dårlig for dynamiske MCP-jobber. Nevnes for ærlighet; ikke anbefalt.

T1 må hevde UTC-instanter for: `30 2 28 3 *` og `30 3 28 3 *` 2027, `30 2 25 10 *` 2026, `* * * * *` over begge skift, `0 og 7 = søndag`, dag-ELLER-ukedag, lister/områder/steg, avvisning av ugyldig uttrykk og sone, samt uendret oppførsel for intervall/én gang.

---

## P4 — Sekvensiell kjøring og rørene

**Konklusjon:** Én hendelse kan henge hele planleggeren for alltid: `FoundationProcessRunner` leser rørene først etter avslutning, uten tidsgrense, og `runDueEvents` venter på hver hendelse i rekkefølge; D5 overlever bare hvis ensure-skriptet omdirigerer fd 1 og 2 før det løsriver arbeideren, og det må testes, ikke antas.

**Belegg**

- Sekvensielt og enkeltsporet: `for id in dueIDs { await runEvent(id:) }` [belagt: ScheduledEventService.swift:224-226]; ny runde først etter 1 s søvn (173-182); `isRunningDueEvents` avviser samtidige kall (207-211).
- Rørene: `readDataToEndOfFile()` i `terminationHandler` [belagt: Sources/HavenMacAutomation/SubprocessRunner.swift:61-71]. EOF kommer først når *alle* skrivere har lukket. Et barnebarn som arver fd 1/2 holder continuation åpen selv om barnet er avsluttet → posten står `running` (233-235) og ingen annen hendelse kjører til prosessen restartes. Siden barnet bare arver 0/1/2, holder det å omdirigere 1 og 2 i skriptet; men skriptet er [ikke belagt] og må ha en test (`/bin/sh -c 'sleep 30 &'` som localTask skal *ikke* henge).
- 64 KiB-vranglås: ingen leser rørene før avslutning; et barn som skriver mer enn rørbufferen blokkerer på write, avslutter aldri, og `runEvent` venter evig. `prefix(4_000)` (240) hjelper ikke, den skjer etter lesingen. F8/F10-sjekker som logger mye vil treffe dette.
- Ingen tidsgrense noe sted (LocalTaskRunner.swift:10-24; SubprocessRunner.swift:48-80).
- Nedstenging: SIGTERM → `stop()` avbryter Task men ikke barneprosessen, og venter på `runEvent` [belagt: ScheduledEventService.swift:185-190; HavenAgentMain.swift:347-348]. launchd SIGKILL-er etter `ExitTimeOut` [ikke belagt i repoet]; barnet lever videre, fila sier `running`, omstarten kjører hendelsen igjen (161-165) → to samtidige kjøringer. For `ensure` dekker låsen; for et bygg eller `git push` ikke.
- Ingen miljø/cwd settes (SubprocessRunner.swift:53-74): barnet arver launchd-miljøet (se P5).

Konsekvens for D5: ensure-skriptet må være stille, raskt, omdirigere alt og ikke kunne blokkere. Konsekvens for resten: per-hendelse `timeoutSeconds` (SIGTERM→SIGKILL), utdata til `Logs/ScheduledEvents/<id>/<ts>.log` (les hodet til `lastOutput`) i stedet for rør, og enten samtidige hendelser (`withTaskGroup`) eller i det minste at ensure-jobben ikke står bak en lang jobb i køen.

---

## P5 — Køarbeideren som barn av launchd-jobben

**Konklusjon:** Ingenting i repoet beviser at bygg, ssh, `gh` og nøkkelring virker fra scheduler-konteksten; scheduler-plisten er ikke versjonert, og uten eksplisitt ny sesjon dør arbeideren hver gang installskriptet restarter tjenesten.

**Hva som må måles (fra en planlagt hendelse, ikke fra Terminal)**

1. Prosessgruppe: `ps -o pid,pgid,sess,ppid` for arbeideren; `launchctl kickstart -k` av scheduleren; lever arbeideren? Default er at launchd dreper jobbens prosessgruppe ved avslutning med mindre `AbandonProcessGroup` er satt [ikke belagt: plisten mangler i `Launchd/`, som bare har `io.digipomps.haven.agentd.plist`; belagt: Scripts/install-agent-dev.sh:19-21, 78 definerer bare etiketten]. macOS har ikke `setsid`-kommando; skriptet må skaffe ny sesjon på annen måte (python `os.setsid`, eller egen launchd-jobb, P1 b). Installskriptet restarter tjenesten ved *hver* installasjon [belagt: install-agent-dev.sh:277] — midt i et bygg.
2. Miljø: `env` fra hendelsen. PATH mangler `/opt/homebrew/bin` (`gh`), `LANG` mangler, cwd er ikke repoet (SubprocessRunner setter ingen) — skriptet må sette alt.
3. ssh: `SSH_AUTH_SOCK` finnes i gui-domenet, men nøkkelen må være lastet (`ssh-add --apple-use-keychain`) og `ssh -T git@github.com` må gi kode 1 med «successfully authenticated», fra hendelsen.
4. `gh auth status` fra hendelsen. Nøkkelring-ACL følger den kjørbare (`gh`), så en ny `gh`-versjon kan utløse en dialog ingen ser.
5. TCC: tilgang til `~/Documents`, `~/Desktop`, `~/Downloads` tilskrives *ansvarlig prosess* = scheduleren, uten UI til å spørre → stille EPERM. Hvor `Claude outputs/` ligger er [ikke belagt]; ligger den under en beskyttet mappe, kan arbeideren ikke lese køen. Mål med `ls` fra hendelsen.
6. Søvn: en launchd-jobb hindrer ikke søvn; lukket lokk kl. 23:10 stopper bygget til morgenen — det kan være nattens egentlige årsak. Mål `pmset -g`, og vurder `caffeinate -i` rundt hver jobb.
7. Omstart av Macen: LaunchAgent starter først ved innlogging (FileVault). F2 «overlever omstart» må leses som «etter innlogging».
8. Bygg: `swift build` fra hendelsen (xcode-select, moduler, `CLANG_MODULE_CACHE_PATH` som testskriptet setter [belagt: Scripts/test_haven_agentd.sh:23-24]).
9. Krasjsikker lås: pid-sjekk (`kill -0`) og oppstartstid, så en gammel lås etter omstart ikke stopper køen for alltid.

Og dokumentér målingene i `OperatorRunbook.md`, som i dag ikke nevner scheduler-jobben i det hele tatt [belagt: grep på «scheduler» i Docs/OperatorRunbook.md gir null treff].

---

## P6 — Hvordan dokumentere D5 ærlig

**Konklusjon:** Si rett ut at grensen i `ScheduledEvents.md` fortsatt gjelder for planleggeren, men at én godkjent policy-post delegerer skallet til en mappe, hvem som kan skrive der, hva det innebærer, og at det er Kjetils vedtak — ikke skriv om grensen slik at den ser ut til å stå.

**Konkret**

- `Docs/ScheduledEvents.md`: beholde linje 54-57 og 65-66, og legge til avsnittet «Delegerende lokale oppgaver»: «`losen-queue-ensure` er en localTask med fast program. Programmets *virkning* er å kjøre ethvert skript i `<kø>`. Planleggeren gir ikke skalltilgang; policyen gjør det, for denne ene posten, etter eiers vedtak 02.10.2026. Alle som kan skrive i `<kø>` kjører som eieren uten gjennomgang. Losen er en av dem, og Losen styres av en skymodell som leser innhold fra andre.» Så kontrollene (eier, rettigheter, ingen symlenker, `.ready`, logg utenfor køen, tidsgrense, STOP-semantikk), og det som *ikke* kontrolleres.
- `Docs/SecurityModel.md`, under «Config ownership» (331-339): én setning om at en localTask kan være en delegering, at det bare er akseptabelt når programmet ligger utenfor mapper den delegerte skriver i, og at kjerneregelen på linje 7-11 ikke dekker lokale delegeringer eieren selv gjør.
- Følg formen i `AgentJobs.md` sin «Security model» [belagt: Docs/AgentJobs.md:228-241], men vær ærligere på forskjellen: der gir lokal skriving policy-handlinger, her gir den skall.
- F5 i formålsspeken trenger fotnote: «med unntak av den delegerende posten».

---

## P7 — Hva mangler for at F1–F10 er oppfylt og testet

**Konklusjon:** F1–F6 er testbare med rettelsene over, F7 har ingen test av det den faktisk består av (et skript), og F8–F10 har ingen komponent i D1–D7 å planlegge — T6 er lastet med fem formål og måler bare ett.

- **F1:** T1 må hevde instanter (P3). Mangler: regresjonstest for intervall/én gang, ugyldig sone, umulig uttrykk.
- **F2:** «kjører etter kickstart» beviser ikke «overlever omstart av Macen» eller «ingen tidsgrense». Koden har ingen tidsgrense (`while !Task.isCancelled` [belagt: ScheduledEventService.swift:174]); `KeepAlive`/`RunAtLoad` for scheduleren er [ikke belagt]. Må: plist inn i `Launchd/` og installskriptet, test at plisten har feltene, én målt omstart med innlogging.
- **F3:** T3 bra, men må også dekke krasj under `running` (i dag: ny kjøring, 161-165) og overkjøring (forekomster under lang jobb). Spesifiser `missedCount`-semantikk for de tre tilfellene.
- **F4:** T5 fin for MCP. Men F4 sier også at HAVEN når det samme via kontrollbro-celle; D6 gir bare status og stopp. Innsnevre F4 eller utvide D6. MCP-verktøyene finnes ikke i dag [belagt: Sources/HavenAgentDMCP/HavenAgentMCPService.swift:202-275]; husk at MCP-server og daemon er ulike prosesser [belagt: Sources/HavenAgentDMCP/HavenAgentDMCPMain.swift:222-235].
- **F5:** «ukjent handling avvises når jobben opprettes» er ikke sant for config-poster i dag — `validate` sjekker ikke policy [belagt: ScheduledEventService.swift:297-309], bare kjøringen gjør det [belagt: LocalTaskRunner.swift:11]. T4 må dekke `start` også. T4 måler API-et; systemet aksepterer skall via køen — fotnote (P6). Legg til tester på skriptet: symlenke, feil eier, skrivbar for andre, halvskrevet fil.
- **F6:** Ny kilde er kontraktsendring: `validate` krever alle kilder [belagt: Sources/HavenAgentRuntime/AgentChallenge.swift:353-355], gammel menyapp dekoder ukjent verdi som `malformed` [belagt: Sources/HavenAgentMenuCore/MenuPresentation.swift:98-103]; `job` ble deklarert på forhånd nettopp for å unngå dette [belagt: AgentChallenge.swift:21-23]. Må: skjema + fixtures + menyapp bygges sammen. Mangler design for kvittering: `dismissToday` håndteres i flaten [belagt: Sources/HavenAgentD/AgentChallengeWiring.swift:227-233], så en feilet `once`-jobb blir sak for alltid; og per-minutt-jobben etter en natts søvn må gi *én* sak, ikke én per passering. Kilden må melde `unreadable` når tilstandsfila ikke kan leses (test). Menyappen starter ikke ved innlogging [belagt: Docs/AgentMenylinje.md:146] — avhengighet §2 mangler.
- **F7:** Ingen test av løperen eller ensure-skriptet, og de er hele F7. Må: skript i køen kjører uten Terminal, markør og logg kommer, arbeideren overlever `kickstart -k` og agentinstallasjon, STOP stopper og ensure gjenoppliver ikke mens STOP finnes, P5-målingene 2–5 grønne fra hendelsen. Egne bevis, ikke T6.
- **F8/F9:** Ingen lokal oppgave finnes å planlegge. `CorrespondenceChallengeProvider` leser bare markører «den som poller skriver» [belagt: AgentChallengeWiring.swift:119-120, 124-135]; polleren er ikke bygget (speken §0). Fristberegning finnes ingen steder [ikke belagt at noe slikt eksisterer]. Enten egen PDD, eller ta F8/F9 ut som «muliggjort, ikke levert».
- **F10:** krever en policy-post for avdriftssjekken med fast program; om skriptet har fast program/argumenter er [ikke belagt].
- **T8:** riktig baseline er grenen i D7, ikke `origin/main` (jf. `cellscaffold_baseline`); kjør `swift test --no-parallel` som skriptet [belagt: Scripts/test_haven_agentd.sh:27].
- **Mangler helt:** tester for kappløp (to prosesser), >64 KiB-utdata, barnebarn med åpent rør, tidsgrense, bakoverkompatibel dekoding av gammel tilstandsfil, og `origin`-bevaring i `start`.

---

## Må endres før G2

1. Løper og ensure-skript ut av Claude-skrivbar mappe; hash eller signatur pinnet i policyen; eier/rettighet/symlenke/`.ready`-sjekk i løperen (P1-4).
2. Én skriver per fil (spec/runtime-split eller kommandospool), fjern running→scheduled-reset fra ikke-arbeidere, låsfil for én arbeider, idempotens per forekomst (P2).
3. DST-regelen som instanter + eksplisitt implementasjon, bundet søk, validering av sone/uttrykk, `validate` med cron-gren (P3).
4. Rør erstattes med logg-fil eller samtidig lesing; per-hendelse tidsgrense; test for barnebarn og >64 KiB (P4).
5. Dynamiske handlinger = `{kind, id}`; avgjør opprinnelse (ikke `.local` uten begrunnelse) (P1-5).
6. Scheduler-plist inn i repo og installskript; måleplan P5 1–5 utført før F7 påstås (P5).
7. Challenge-kontrakt, fixtures og menyapp oppdateres sammen; kvitteringsmekanisme og én-sak-per-jobb (P7 F6).
8. F8/F9 flyttes ut eller får komponent; F4 innsnevres eller D6 utvides; F5 får fotnote (P6/P7).

## Bør endres

- Egen launchd-jobb for løperen i stedet for ensure-hvert-minutt (P1 b, løser P4/P5 samtidig).
- `caffeinate -i` rundt køjobber; mål `pmset`.
- Per-jobb `catchUpWindowSeconds` med Kjetils regel som default.
- Håndhev eller fjern `requiresUserSession`.
- `OperatorRunbook.md` får scheduler-jobben og målingene.

## Kan vente

- Egen macOS-bruker for Losens kø (P1 c).
- Mal-allowlist med constrained args som sluttilstand (P1 d).
- Samtidige hendelser (`withTaskGroup`) når én-skriver-modellen er på plass.
- Kontrollbro-celle for opprett/pause (resten av F4).
