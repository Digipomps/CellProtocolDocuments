# Formålsspesifikasjon — testmatrise og APNs-chat

Oppgavemappe: `PDD_testmatrise-og-apns-chat_2026-09-29` · Opprettet 2026-09-29 · Iterasjon 1 (venter på G1)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Sett opp forskjellige tester som går mellom forskjellige scaffolds, en mellom to eller tre brukere på samme scaffold, en test fra prod til en bruker på palazzo (kanskje en kelner?) og test fra de forskjellige enhetene HAVEN app kan kjøre fra. Når alt er klart for APNs testing så vil jeg ha det også slik at man kan initiere en chat fra et skyscaffold til f.eks en iPhone. Test og push all ucommitted kode.

Svar på oppklaring 29.09 (Kjetil): push = «bare mitt + wip-snapshot»; scaffolds = «lokale instanser først, prod↔Palazzo som skrivebeskyttet røyktest»; enheter = «simulator + Mac + kontrakt, ekte iPhone i manuell sjekkliste»; APNs = **«full implementasjon mot Apple»** (se §2: krever nøkler som bare Kjetil har).

### 0.1 Det forespørselen forutsetter, revidert mot koden (29.09)

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| To brukere kan chatte via invitasjon (Kjetil↔Vegar) | **retrieved**: typer, verifisering og nøkkelavtale-nøkkel er på main (#51, 81601a6, 15/15 + 1277/0 feil). Aksept → to envelopes → ChatCell klar (WP7) er **ikke** gjort | CellProtocol `HavenInviteRoundATests.swift`; PLAN.md WP7 |
| Landing/reply/gravstein/410/sender-status mot ekte scaffold | **unavailable**: del 2 (CellScaffold + Binding) er ikke skrevet | STATUS.md 26.09 |
| Et skyscaffold kan sende APNs | **retrieved, delvis**: `APNSPushProviderAdapter` finnes (JWT ES256, `api(.sandbox).push.apple.com`, topic, alert/background), konfigurert av `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_P8`/`_BASE64`/`_PATH`, `APNS_BUNDLE_ID`, `APNS_USE_SANDBOX`. Bygget for konferansevarsler (`NotificationOutboxCell`), ikke for chat/invitasjon | `CellScaffold/Sources/App/Cells/ConferenceMVP/Notifications/PushProviderAdapter.swift:116-162,272-341` |
| iPhone registrerer push-token mot scaffold | **retrieved, delvis**: `NotificationEnrollmentManager` kaller `registerForRemoteNotifications`, `updateAPNSToken`, registrerer enhet med konferanse-ID og emner. Ikke knyttet til en entitet/relasjon eller chat | `Binding/Binding/NotificationEnrollmentManager.swift:45-232` |
| Palazzo er en scaffold-installasjon vi kan nå fra prod | **recalled**: Palazzo-celler (`Restaurant/*`, `PalazzoCommunaleServiceCell`, `RestaurantStaffShellCell`) ligger i CellScaffold-koden; **hvilken vert/miljø Palazzo kjører på er ikke funnet** i Documentation/Operations (kun `haven.digipomps.org`, `staging.haven.digipomps.org`, `admin.*`) | `Restaurant/RestaurantStaffShellCell.swift`; grep i `Documentation/Operations` |
| «Kelner» finnes som rolle | **retrieved, delvis**: `RestaurantStaffShellCell` (staff-forhåndsvisning, «denied: staff preview owner required»). Ingen kelner-*identitet* funnet | `RestaurantStaffShellCell.swift:52-76` |
| Flere scaffolds kan kjøres lokalt samtidig | **recalled**: startskript finnes (`run_local_kallimachos_butler_admin_demo.sh`, `run_porthole_chat_canary.sh`), men ikke målt at to instanser med egen eier/vault og egen port kjører side om side | `CellScaffold/scripts/` |
| Appen kan kjøre fra flere enheter | **retrieved**: `Binding.xcodeproj` `SUPPORTED_PLATFORMS = iphoneos iphonesimulator macosx`, `TARGETED_DEVICE_FAMILY = 1,2` (iPhone + iPad). Linux-scaffold via `Tests/Linux/` | `Binding/Binding.xcodeproj/project.pbxproj:668-721` |
| «All ucommitted kode» er håndterbar | **retrieved, rettet 29.09**: første måling fra VM-en ga «Binding 409 / CellScaffold 1 815 / CPDocs 883 endret» — **det var stat-støy** (`git diff-files` uten refresh; samme metode ga 882 «endrede» i CellProtocol der en ferskt refreshet indeks ga **0**). Ekte tall måles mot en refreshet kopi av indeksen (T6). Uspora filer (Binding ≈ 42 000) er bygg-rot og andre tråders worktrees og holdes ute etter mønster | `snapshot-alle.sh`, målt 29.09 |

## 1. Formålstre

Alle noder er `candidate` til Kjetil har sagt G1. Ingen gjenbrukes av Book 23 direkte, men rotens forelder er `purpose://contact.communication` (samme som invitasjonstreet).

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.testmatrise.root` | Samarbeid mellom inviterte kan bevises på alle veier | `contact.communication` | Hver vei en invitert kan komme inn og snakke — samme scaffold, mellom scaffolds, prod→Palazzo, alle enheter, skyscaffold→iPhone — har en kjørbar test som gir grønt eller `blocked` med grunn | §5 i sin helhet | candidate |
| **T1** `…testmatrise.same-scaffold-collaboration` | To–tre brukere på ett scaffold | root | Tre entiteter (egne vaults, tilfeldige UUID-er) inviterer, aksepterer og snakker i én invitasjonschat på ett scaffold; hver ser bare det de er invitert til; den tredje kan ikke lese de to andres samtale | `test.matrise.same-scaffold-three` | candidate |
| **T2** `…testmatrise.two-scaffolds-one-conversation` | Én samtale mellom to scaffolds | root | A på scaffold 1 inviterer B på scaffold 2 (lokale instanser, egen port, eier og vault hver); ja gir chat der begge ser samme meldinger, forseglet til hver mottakers nøkkel; ingen av scaffoldenes admin kan lese den andres celler | `test.matrise.cross-scaffold-chat`, `test.matrise.admin-cannot-enter-other-scaffold` | candidate |
| **T3** `…testmatrise.prod-to-palazzo-staff` | Prod → en bruker på Palazzo (kelner) | root | Fra prod-scaffold kan en invitasjon til en Palazzo-kelner *slås opp og leses* (røyktest, ingen skriving i prod uten Kjetils ja); det samme scenariet med skriving kjøres mot staging med en testkelner merket som test | `test.matrise.prod-readonly-smoke`, `test.matrise.staging-waiter-chain` | candidate |
| **T4** `…testmatrise.same-suite-on-every-device` | Samme suite på hver enhet | root | Chat-scenariene T1/T2 kjøres som *data-drevne enhetsprofiler*: Mac-app, iOS-simulator iPhone, iOS-simulator iPad, Linux-scaffold (klient uten UI). Ekte iPhone har en manuell sjekkliste med forventet observasjon per steg | `test.matrise.device-profiles`, `test.matrise.iphone-checklist` | candidate |
| **T5** `…testmatrise.cloud-scaffold-starts-a-chat-on-a-phone` | Skyscaffold starter en chat på en telefon | root | En eier på et skyscaffold inviterer en person som har HAVEN på iPhone; telefonen får en APNs-varsling som *ikke bærer innhold*, og trykk åpner invitasjonen i appen; ja gir chat | se T5.1–T5.5 | candidate |
| T5.1 `…apns.token-belongs-to-an-entity` | Push-token hører til en entitet, ikke en konferanse | T5 | iPhone registrerer token mot skyscaffoldet under entitetens egen identitet (signert), med `sandbox`/`production`, `bundleId`, og kan trekke det tilbake; scaffoldet lagrer token uten navn | `test.apns.token-registration-signed`, `test.apns.token-revoke` | candidate |
| T5.2 `…apns.payload-carries-no-content` | Varselet bærer ingen personinfo | T5 | Payload = `{aps:{alert:generisk tekst}, haven:{k:"invite", id:<ticketID>}}`. Ingen avsendernavn, ingen meldingstekst, ingen basis-felt. Tekst i §3 godkjennes av Kjetil | `test.apns.payload-has-no-content` | candidate |
| T5.3 `…apns.only-who-was-invited-is-pushed` | Bare den inviterte kan varsles | T5 | Varsel sendes bare til token registrert av entiteten billetten er adressert til (audience-token treffer); en annen entitets token, et utløpt eller trukket token, og en gravstein nekter | `test.apns.wrong-audience-not-pushed`, `test.apns.tombstone-blocks-push`, `test.apns.expired-not-pushed` | candidate |
| T5.4 `…apns.tap-opens-the-invitation` | Trykk åpner invitasjonen i appen | T5 | Appen mottar `haven.k/id`, henter billetten fra scaffoldet, verifiserer den (`HavenInviteVerifier`) og viser invitasjonsflaten. Ingen auto-aksept | `test.apns.tap-opens-verified-invitation` | candidate |
| T5.5 `…apns.real-sandbox-send` | Ekte sending mot Apple (sandbox) | T5 | Ett varsel går fra et skyscaffold til Kjetils iPhone via `api.sandbox.push.apple.com`; Apple svarer 200 med `apns-id`; varselet vises; trykk åpner appen | `test.apns.real-sandbox-send` (**blocked** til Kjetil har gitt nøkkel-oppsett og token, se §2) | candidate |
| **T6** `…testmatrise.nothing-uncommitted-is-lost` | Ingenting ucommittet går tapt | root | Alt ucommittet i CellProtocol, CellScaffold, Binding (og CellProtocolDocuments) ligger som en pushet wip-commit uten at noens checkout, indeks eller worktree er rørt; hemmeligheter og bygg-rot er ute; commit-hash er lest etter push | `test.push.snapshot-no-disturbance`, `test.push.no-secrets`, `test.push.hash-read-after-push` | candidate |

Regler: hvert blad har minst én test i §5. T5.5 er det eneste som ikke kan bli grønt uten noe bare Kjetil kan gi.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke skriving i prod uten et eget, eksplisitt ja fra Kjetil per gang. Prod-testen er lesing.
- Ikke en ny chat-implementasjon: T1–T4 tester kjeden som WP7 + runde A del 2 bygger. Der en test trenger noe som ikke finnes ennå, står den som `blocked: avhenger av WP<n>`, ikke som grønn.
- Ikke innhold i push. Aldri. Varselet sier at noe finnes, appen henter det selv.
- Ikke et varsel som kan sendes uten at den inviterte har registrert sitt eget token.
- Ikke å bygge inn andre tråders ucommitterte arbeid i mine PR-er, og ikke å røre deres checkouts (T6).
- Ikke å ta APNs-nøkkel, Team-ID eller token i hånden: jeg leser dem aldri, skriver dem aldri i chat eller repo. De settes som miljøvariabler på scaffoldet av Kjetil (se under).

Kapabiliteter og avhengigheter oppgaven bygger på:

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Invitasjonstyper, verifisering, gravstein, nøkkelavtale-nøkkel | CellProtocol main 81601a6 (#51) | ingen scaffold-side ennå | ja — **grønn** (15/15, 1277/0) |
| Aksept → to envelopes → ChatCell klar | PLAN.md WP7 | ikke skrevet | ja — T1/T2 `blocked` til den er grønn |
| CellScaffold-side av invitasjon (landing, reply, tombstone, 410, sender-status) | PLAN.md runde A del 2 | ikke skrevet | ja — T2/T3/T5 |
| `APNSPushProviderAdapter` + `PushHTTPTransport`-stub | `PushProviderAdapter.swift` | konferansevarsler; payload-form må byttes for invitasjon | ja for T5.2/T5.3 |
| Enhetsregistrering med `apnsToken` | `NotificationEnrollmentManager.swift`, `DeviceRegistrationReadinessTests` | knyttet til konferanse, ikke entitet | ja for T5.1 |
| Apple: APNs-nøkkel (.p8), Key-ID, Team-ID, bundle-ID/topic, push-entitlement i appen, enhets-token | **Kjetil** (Apple Developer) | kan ikke skaffes av meg | bare T5.5 |
| Palazzo-vert/miljø og kelner-identitet | ikke funnet | **åpent, se §6** | bare T3 |
| Xcode/simulator for enhetsprofiler | `Binding.xcodeproj`, macOS-skript via Finder | ekte iPhone styrer jeg ikke | T4 |

## 3. Forventningskontrakt — «Det du kommer til å se»

Etter G2 er dette det eneste som teller som fremdrift.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| **Testmatrisen**: én tabell scenario × miljø × enhet × resultat (grønn / rød / blocked + grunn) | fil | `TESTRESULT.md#matrise` | — | nei |
| Tre-brukere-på-ett-scaffold: testutdata + chronicle-spor per entitet | testutdata | `TESTRESULT.md#same-scaffold` | — | nei |
| Mellom-to-scaffolds: to kjørende lokale instanser, logg fra begge, samme meldinger på begge sider | testutdata + logger | `TESTRESULT.md#cross-scaffold`, `handoff/…/*.log` | — | nei |
| Prod-røyktest (bare lesing) med URL, statuskoder og hva som ble lest | testutdata | `TESTRESULT.md#prod-smoke` | — | nei |
| Staging-kjede prod-lignende → Palazzo-kelner (testentitet merket som test) | testutdata | `TESTRESULT.md#palazzo` | — | nei |
| Enhetsprofiler (Mac, iPhone-sim, iPad-sim, Linux) med resultat per profil | testutdata | `TESTRESULT.md#devices` | — | nei |
| Manuell iPhone-sjekkliste med forventet observasjon per steg | fil | `handoff/iphone-sjekkliste.md` | — | nei |
| APNs: `PushSendRequest` for invitasjon, stub-transport, payload-fixtures, kontrakt | kontrakt + fixtures | `contract/apns_invite_v1.json` + `contract/fixtures/` | — | nei |
| **Varslingsteksten** som vises på låseskjermen (hele teksten, ingen personinfo) | tekst — Kjetil dømmer | `FORMAALSSPEC.md §3.1` under | ja/nei | nei |
| Ekte sandbox-varsel på Kjetils iPhone | kjørende flate + apns-id i logg | `TESTRESULT.md#apns-real` | — | nei |
| Wip-snapshot per repo: commit-hash lest etter push, antall filer, hva som ble holdt ute og hvorfor | testutdata | `TESTRESULT.md#push` | — | nei |

### 3.1 Varslingsteksten (forslag — Kjetil godkjenner ordlyden i G1)

Låseskjerm, norsk: **tittel «HAVEN»**, **tekst «Du har en invitasjon å svare på.»** Ingen avsendernavn, ingen forhåndsvisning av melding. Det er avsenderens navn og grunnlag som vises *inne i appen*, etter at billetten er verifisert (jf. invitasjonsstripen, G1-GUI 24.09). Engelsk språkversjon følger appens språk; ordlisten fra invitasjons-PDD-en gjelder (ingen «entitet», «scaffold», «token» i teksten).


## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.test-the-representation-not-the-issuance-flow** (2026-09-09, minor): Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.
    - forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.
- **lesson.queue-job-file-before-prompt** (2026-09-10, minor): Køjobben `formaalskomposisjon-fullfor-commit-20260910-1020` ble avvist med «mangler promptfil» 13 sekunder etter at `.job` ble skrevet; promptfilen kom to sekunder etter avvisningen og ligger foreldreløs i `_losen-queue/inbox/`, der runneren aldri ser den igjen.
    - forebygging: Skriv `<id>.prompt.md` først og `<id>.job` sist, helst som `mv` fra en tmp-fil i samme mappe — `.job` er registreringssignalet, slik `job.json` er det i HavenAgentD::Docs/AgentJobs.md. Kan bli derivedTest: runneren eller `hd validate` rapporterer enhver `inbox/*.prompt.md` uten tilhørende `.job`, eldre enn to minutter, som foreldreløs.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.readonly-git-is-not-all-git** (2026-09-24, minor): Et `git status` fra device_bash i CellProtocolDocuments etterlot .git/index.lock (0 byte) som ikke kunne fjernes fra VM-en, selv om git show/grep/log/rev-parse i samme økt ikke gjorde det.
    - forebygging: Fra device_bash bare objektlesende git mot en revisjon (git show/grep/log/cat-file <rev>); aldri status, diff mot arbeidstreet, add eller commit. Finnes en lås likevel: flytt den til _to_delete/ (mv virker, rm gjør ikke).
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.jxa-objc-method-without-arguments-is-a-property** (2026-09-24, minor): `a.terminate()` i JXA ga `TypeError: a.terminate is not a function`, men appene avsluttet likevel.
    - forebygging: Skriv `a.terminate` (uten parentes) og sjekk etterpå med `pgrep` at prosessen er borte før du går videre.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://project-work.overview-and-sharing [active] — Project work overview and sharing
- purpose://project-work.current-status-and-outstanding [active] — Current status and outstanding work
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://quality [active] — Quality
- purpose://validation [active] — Validation
- purpose://test.acceptance [active] — Acceptance tests
- purpose://test.acceptance.purpose-decomposition [active] — Purpose decomposition acceptance
- purpose://test.acceptance.hallucination-evaluation [draft] — Hallucination evaluation gate
- purpose://test.acceptance.questionnaire [active] — Questionnaire acceptance tests
- purpose://test.acceptance.project-work [active] — Project work acceptance tests
- purpose://scaffold.operations [candidate] — Scaffold operations


## 5. Avledede tester (samlet)

Kolonnen «Kan kjøres» sier ærlig hva som er mulig før avhengighetene i §2 er grønne. En `blocked`-rad er ikke en grønn rad.

| Test | Type | Hva den viser | Hvor | Kan kjøres nå |
|---|---|---|---|---|
| `test.matrise.same-scaffold-three` | command | tre `SimulatedEntity`, invitasjonschat, C leser ikke A↔B | `TESTRESULT.md#same-scaffold` | delvis: nøkkelavtale-nøkkel og aksept-signatur ja; ChatCell-klar krever WP7 |
| `test.matrise.cross-scaffold-chat` | command | to lokale scaffolds (egne porter/eiere/vaults), samme meldinger begge veier | `#cross-scaffold` | nei — krever del 2 + WP7 |
| `test.matrise.admin-cannot-enter-other-scaffold` | command | admin på 1 nektes lesing/skriving/handlinger i celler på 2 (gjenbruker entitetsdata-fixtures) | `#cross-scaffold` | ja (fra runde 2-mønsteret) |
| `test.matrise.prod-readonly-smoke` | command | GET-oppslag mot prod: helse, offentlig invitasjonsoppslag av et *ikke-eksisterende* endepunkt gir samme svar som et ikke-publisert (A1). Ingen POST | `#prod-smoke` | ja, etter Kjetils ja til at jeg leser fra prod |
| `test.matrise.staging-waiter-chain` | command | testkelner-entitet på staging-Palazzo mottar invitasjon og chat | `#palazzo` | nei — krever §6.1–6.2 og del 2 |
| `test.matrise.device-profiles` | command | samme scenario med profil `mac-app`, `ios-sim-iphone`, `ios-sim-ipad`, `linux-client` (profil = data: plattform, destinasjon, hva som finnes av nøkkelchain) | `#devices` | delvis: profilene og kontraktnivå ja; app-kjøring via Xcode/Codex |
| `test.matrise.iphone-checklist` | inspection | Kjetil krysser av hvert steg | `handoff/iphone-sjekkliste.md` | ja, som fil |
| `test.apns.token-registration-signed` | command | usignert / feil-identitet registrering avvises; signert lagres uten navn | `#apns` | ja |
| `test.apns.token-revoke` | command | trukket token får aldri varsel | `#apns` | ja |
| `test.apns.payload-has-no-content` | command | golden fixture: payload inneholder bare generisk tekst + `haven.k/id`; sentinel i avsendernavn/basis/melding finnes ikke i noen byte | `#apns` | ja |
| `test.apns.wrong-audience-not-pushed` | command | token fra annen entitet → ingen sending | `#apns` | ja |
| `test.apns.tombstone-blocks-push` | command | «aldri» → ingen varsel, heller ikke ved ny billett | `#apns` | ja (gravstein fra #51) |
| `test.apns.expired-not-pushed` | command | utløpt/trukket billett → ingen varsel | `#apns` | ja |
| `test.apns.tap-opens-verified-invitation` | command | app-siden tar imot `haven.k/id`, henter, verifiserer, viser; ugyldig billett viser feilflate, ikke invitasjon | `#apns` | delvis: verifiseringsdelen ja; UI-delen krever Xcode |
| `test.apns.real-sandbox-send` | measurement | ekte 200 fra `api.sandbox.push.apple.com` + `apns-id` i logg; varsel vises på telefonen | `#apns-real` | **blocked** til Kjetil har satt `APNS_*` på scaffoldet og gitt et enhets-token |
| `test.push.snapshot-no-disturbance` | command | for hvert repo: HEAD, indeks og arbeidstre er byte-identiske før og etter (sha av `git diff-files` + `ls-files -o`) | `#push` | ja |
| `test.push.no-secrets` | command | skann av alt som ville gå med: `.p8`, `.pem`, `.env`, `*.key`, `*.mobileprovision`, `xcuserstate`, filer > 5 MB, `_wt*`, `_to_delete`, `.build` — ingen treff går med; hva som ble holdt ute listes | `#push` | ja (tørrkjøring først) |
| `test.push.hash-read-after-push` | command | `git ls-remote --heads origin <wip>` limt inn og lik lokal commit | `#push` | ja |
| `test.build` / `test.regression` | command | bygg CellProtocol/CellScaffold/Binding mot main; full CellBaseTests; scaffold- og Binding-tester som er grønne på main i dag forblir grønne | `#build`, `#regression` | ja |

Alle `command`-tester bruker de rette grønn-portene (`tail -1` av «Executed», POSIX `case`, jf. `lesson.green-gate-must-read-the-last-summary-line`).

## 6. Åpne spørsmål til Kjetil

Bare de som endrer treet.

1. **Palazzo — hvor kjører det?** Fant bare celler i CellScaffold-koden, ikke en vert. Er Palazzo (a) en egen scaffold-installasjon, (b) en konfigurasjon av samme prod-scaffold som `haven.digipomps.org`, eller (c) ikke oppe ennå? Svaret avgjør om T3 er «prod→annet scaffold» (som T2) eller «prod→annen rolle på samme scaffold» (som T1).
2. **Kelneren — ekte eller testentitet?** Skal røyktesten i prod bare lese, og staging-kjeden bruke en testkelner jeg oppretter (merket som test, i staging)? Eller finnes det en ekte kelner-identitet du vil bruke?
3. **APNs-oppsett (blokkerer bare T5.5):** hvilken bundle-ID er iPhone-appen (`org.digipomps.haven` eller `havenplayground`)? Bygges den fra Xcode (→ **sandbox**) eller TestFlight/App Store (→ **production**)? Og setter du selv `APNS_TEAM_ID`, `APNS_KEY_ID`, `APNS_PRIVATE_KEY_PATH` (peker på .p8 på scaffoldets disk — ikke inn i chat, ikke i repo) og `APNS_BUNDLE_ID` på det skyscaffoldet vi tester mot?
4. **Varselteksten** (§3.1): «HAVEN — Du har en invitasjon å svare på.» — ok, eller annen ordlyd?

## 7. Revisjonslogg

| Dato | Iterasjon | Hva endret seg |
|---|---|---|
| 2026-09-29 | 0 | Opprettet av `purpose_dev.py new` |
| 2026-09-29 | 1 | Full spec etter Kjetils svar (push-omfang, lokale instanser først, enhetsmatrise simulator+Mac, APNs full implementasjon). Audit mot kode: APNs-adapter og enhetsregistrering finnes, men er konferansevarsler; Palazzo-vert ikke funnet. T6 (snapshot uten å røre checkouts) lagt til; omfanget av «ucommittet» er *ikke* kjent før det er målt mot en refreshet indeks (første måling var stat-støy og er rettet i §0.1). |
| 2026-10-06 | 2 | Etter G2 (planbytte, se PLAN.md §6): T5.3 «audience-token treffer» erstattes av «oppslått entitet». Nytt blad `purpose://candidate.testmatrise.invite.resolve-recipient-to-an-entity` (WP13) med testene `test.invite.resolve-own-relations`, `test.invite.resolve-ambiguous-asks`, `test.invite.unresolved-falls-back-to-landing`, `test.apns.unresolved-not-pushed` og (blocked) `test.invite.resolve-other-scaffold-by-agreement`. G1 er ikke trukket tilbake; Kjetil har gitt regelen i chat. |
