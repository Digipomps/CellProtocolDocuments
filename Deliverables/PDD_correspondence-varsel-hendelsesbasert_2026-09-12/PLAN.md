# PLAN — varsel om ny post, hendelsesbasert (HD-0069, vei A)

Oppgavemappe: `PDD_correspondence-varsel-hendelsesbasert_2026-09-12` · Skrevet 2026-09-12 etter G1 (godkjent samme dag) · Port: **G2 venter**

Én arbeidspakke per bladformål i FORMAALSSPEC.md §1, i avhengighetsrekkefølge. Hver pakke navngir purposeRef, utfører, testene den skal gjøre grønne (§5) og artefaktene den leverer til §3. Stier er `<repo>::<sti>`. Ingen git-mutasjon fra Cowork-VM-mount; alle commits og pushes gjøres av Codex eller Kjetil på Mac. Lange bygg kjøres som detached skript (`lesson.codex-workspace-write-cannot-build-cellscaffold`), aldri som `workspace-write`-køjobb.

## 0. Rekkefølge og blokkeringer

```
WP0 baseline ──┬── WP-S1 server-feed (CellScaffold) ──► WP-D1c staging-deploy (Kjetil) ──┐
               │                                                                          │
               ├── WP-A1 kilde fra hendelse ─► WP-A2 abonnement mot staging ◄─ WP-D1b WS-vei (Kjetil) ◄┘
               │        │
               │        └──► WP-A3 celle agent/challenges ─► WP-A4 kontraktsversjon
               │                                      │
               └── WP-M0 app-identitet ─────────────► WP-M1 app som bro-klient ─► WP-M2 adminflate
                                                                                      │
                                              WP-C commit/PR etter hvert grønt bygg   │
                                              WP-V kjøring på Kjetils maskin ◄────────┘  (blokkert av HD-0070)
```

Blokkeringer som ikke er denne PDD-ens: **HD-0070** (ny agentbinær drepes av macOS — blokkerer WP-V og alt som kjører på maskinen), **HD-0071** (PR for grenen fra 11.9 — WP-A1 bygger på den), **HD-0073** (WS-vei på staging — WP-A2 trenger den), **HD-0072** (= WP-S1, registrert som egen kø-post). Enhetstester og kontraktsarbeid går uavhengig av alle fire.

Testtall er «forventet ≈ N (fra kilde, dato)», aldri fra hukommelsen (`lesson.baseline-count-from-report-not-run`): HavenAgentD ≈ 224–243 (STATUS 10.–11.9), CellScaffold ukjent til WP0 har målt.

## 1. Arbeidspakker

### WP0 — Baseline på ren eksport
- purposeRef: `purpose://quality.build-and-regression`
- Utfører: **Codex** (detached skript, `danger-full-access`, Popen start_new_session), logg til `HAVEN/_handoff-<dato>/` eller oppgavemappens `evidence/`
- Gjør: `git fetch origin` i HavenAgentD, CellScaffold, CellProtocol (fra macOS, ikke mount); `git archive origin/main | tar -x -C <scratch>` per repo; `swift build` + `swift test` i HavenAgentD (les resultatet fra «Test run with N tests …», ikke exitkoden — `lesson.swift-test-exit-code-lies-in-havenagentd`); `Scripts/preflight_before_landing.sh` og `Scripts/assert_dependencies_are_on_their_main.sh`; i CellScaffold bare `swift build` + `swift test --filter AssistantCorrespondenceCellTests` (fullt løp er timeboxet, se HD-0027/HD-0032). Rød baseline = spørsmål, ikke tiltak (`lesson.a-red-baseline-is-a-question-not-an-answer`).
- Tester: test.build, test.regression (baseline-tall)
- Leverer: `TESTRESULT.md#build`, `#regression` (baseline-avsnitt), `evidence/wp0/`

### WP-S1 — Mottaker-skopet feed på serveren (= HD-0072)
- purposeRef: `purpose://candidate.corr-varsel.recipient-scoped-events`
- Utfører: **Codex** (kode + tester i CellScaffold, egen gren `pdd/corr-varsel-recipient-feed`), Claude gransker diffen linje for linje før PR (`lesson`: fire runder kodegjennomgang fant 24 feil i grønn kode)
- Gjør, i `CellScaffold::Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift`: (1) `validateCellSpecificAccess` som gir `r---` på `feed` til en identitet med aktiv grant (presedens `AgentConversationInboxCell.swift` l. 147, 290–319); (2) override av `flow(requester:)` som filtrerer til `recipientID == abonnentens principal` og bare `message.send` / `message.ack` (presedens `CellProtocol::…/Chat/ChatCell.swift` l. 517–525); (3) hendelser sendt via celle-eid emitter (`makeCellOwnedFlowEmitterForRuntimeBinding`, presedens `AgentTrustPackageCell.swift` l. 88), ikke `pushFlowElement(requester:)`; (4) ingen `content` i hendelsen (bevares); (5) `inbox.list`/`message.read`-hendelser når aldri en abonnent.
- Tester: test.cell.auth-negative (utvidet: uten grant → `StreamState.denied`; med grant → egen `message.send`, ikke andres; `inbox.list`-hendelse usynlig), test.corr.flow-received (server-halvdelen: én `message.send` → én FlowElement hos mottakerabonnent, i prosess)
- Leverer: kode + tester på gren, `TESTRESULT.md#auth`, `#flow-received` (server), docs-diff i `CellScaffold::Documentation/` for correspondence-cellen (`Last verified against code`)

### WP-D1b — WS-vei fra daemonen til cellen på staging (= HD-0073)
- purposeRef: D1b i §2 (avhengighet, ikke bladformål)
- Utfører: **Kjetil** velger (allowlist `SPROUT_NATIVE_ALLOWED_PUBLISHERS` utvidet med daemonens utgiver-ID, eller bridgehead gjenopprettet i `routes.swift`); driftsendring registreres som HAVEN-Deploy-post med Forutsetning/Kommando/Aksept/Rollback og claim før mutasjon
- Tester: daemonen får `BridgeCommand`-ready mot `AssistantCorrespondence` i staging-logg
- Leverer: `TESTRESULT.md#staging-path`

### WP-D1c — Staging kjører WP-S1
- purposeRef: D1c i §2
- Utfører: **Kjetil** (kjeden main → staging via `haven-deploy`; `lesson.codex-sandbox-cannot-reach-docker`); Losen forbereder posten i HAVEN-Deploy når WP-S1 er merget
- Tester: `/health/build` = commit med WP-S1
- Leverer: `TESTRESULT.md#staging-build`

### WP-A1 — Ny post blir én sak (agenten)
- purposeRef: `purpose://candidate.corr-varsel.challenge-per-message`, `purpose://candidate.corr-varsel.content-safe`, `purpose://candidate.corr-varsel.ack-resolves-case`, `purpose://candidate.corr-varsel.ack-stays-explicit`
- Utfører: **Codex**, gren `pdd/corr-varsel` fra `origin/main` **etter** at HD-0071 (grenen fra 11.9) er merget — den bærer `AgentChallengeSource.correspondence`, kontraktsutvidelsen og `handleAt`
- Gjør: oversetter en `message.send`-hendelse (uten content) til `AgentChallenge` (id `correspondence:<messageID>`, source `correspondence`, kind `agent-attention`, tittel «Ny post fra <avsender>» ≤ 80, detalj = emne ≤ 400 gjennom `AgentChallengeTextSafety`, `needsHuman: true`, svar `open` / `dismiss-today`, `handleAt: assistant`, `subject` = profil/kanal); dedupe på messageID (gjensending med `created:false` gir ingen ny sak); `message.ack`-hendelse → saken løst; ingen kodevei kvitterer. Markørdesignet (`CorrespondenceWaiting`) beholdes som mulig senere variant, ikke koblet inn.
- Tester: test.corr.challenge-shape, test.corr.no-duplicates, test.notify.no-body, test.notify.no-secrets, test.corr.ack-resolves, test.corr.no-auto-ack, test.cell.contract-fixtures (fixture `inbox-positive.json` med én ny-post-sak, `inbox-negative.json` med sak som bærer innhold)
- Leverer: kode + tester, `Contracts/agent-challenge-v1.example.json` oppdatert, `TESTRESULT.md#challenge-shape`, `#no-duplicates`, `#no-body`, `#no-secrets`, `#ack-resolves`, `#no-auto-ack`, `#contract`

### WP-A2 — Agenten abonnerer på serveren (ingen polling)
- purposeRef: `purpose://candidate.corr-varsel.event-from-server`, `purpose://candidate.corr-varsel.no-polling`, `purpose://candidate.corr-varsel.absence-visible` (agent-halvdelen)
- Utfører: **Codex**, samme gren
- Gjør: ny `CorrespondenceFlowSubscriber` ved siden av `AgentConversationFlowSubscriber` (`HavenAgentD::Sources/HavenAgentRuntime/AgentConversationFlowSubscriber.swift` l. 118–196 som mønster: dedupe + engangs catch-up), én bro-sesjon per principal (`kjetil-codex-d`, `kjetil-vegar-codex-d`) over Sprout-ingress (`PortholeIngressSession.swift` l. 119–169) med profilene fra `CorrespondenceIdentityVault`/`AgentIdentityStore` (D2); reconnect med eksponentiell backoff og **ett** `inbox.list(afterSequence: sistSett)` per principal ved gjenoppkobling, filtrert `acknowledgedAt == nil`; kildestatus `read` / `unreadable(grunn)` / `not-configured` per principal; ingen Timer eller søvnsløyfe.
- Tester: test.corr.flow-received (agent-halvdelen, mot lokal scaffold eller staging), test.corr.no-polling (grep + gjennomlesing), test.corr.source-unreadable-visible, test.corr.catch-up-once, test.cell.auth-negative (agent: hendelse for annen mottaker gir ingen sak)
- Leverer: kode + tester, `TESTRESULT.md#flow-received` (agent), `#no-polling`, `#unreadable`, `#catch-up`

### WP-A3 — Innboksen er en celle
- purposeRef: `purpose://candidate.corr-varsel.challenges-as-cell`, `purpose://candidate.corr-varsel.change-signal-inside-agent`, «Ignorer i dag» som celletilstand (§6 spm. 10 → ii)
- Utfører: **Codex**, samme gren
- Gjør: celle `agent/challenges` (descriptor i `AgentCellRegistry.hostedRuntimeDescriptors`, `AgentCellRuntimeHost.swift` l. 353–372) + rute `agent-challenges` i `AgentConfig.defaultRoutes` (l. 153–209); `get` = innboksen (samme provider som `/challenges`, som blir projeksjon — beholdes for `status/summary` og HD-0070), `set` = svar gjennom sakens `answerPath` og demping («Ignorer i dag» = tilstand i cellen med utløp ved døgnskifte); cellen holder siste snapshot og pusher én FlowElement per endring (`haven.agent.challenge.created|updated|resolved`, uten innhold); endringssignal per kilde: correspondence (hendelse fra WP-A2), intent-review (`FolderMonitor`, `AgentRuntime.swift` l. 395–408), scaffold-queue og agent-health (eksisterende signal om det finnes — ellers dokumentert som unntak i `dataflow.md`, ikke en skjult timer). Kontrakt: `contract/agent_challenges_cell_contract_v0.json` løftes til `HavenAgentD::Contracts/` med fixtures.
- Tester: test.corr.challenge-flow, test.cell.contract-fixtures (cellen), test.cell.stub-scan, test.corr.no-polling (cellen)
- Leverer: kode + tester, kontrakt + fixtures, `TESTRESULT.md#challenge-flow`, `#contract`, `ACCEPT.md#stubs`

### WP-A4 — Kontrakt som tåler nye kilder (= HD-0074)
- purposeRef: D8 i §2
- Utfører: **Codex**, samme gren
- Gjør: `AgentChallengeSource` slutter å være lukket enum i klienten (ukjent kilde dekodes som `unknown(raw)` og vises som erklært ukjent rad), eller kontraktsversjon bumpes med eksplisitt avvisning i appen; valget dokumenteres i `Contracts/agent-challenge-v1.schema.json`.
- Tester: ny enhetstest «eldre app mot ny innboks gir erklært feil/ukjent rad, ikke malformed»
- Leverer: `TESTRESULT.md#contract-skew`

### WP-M0 — Appen har en identitet cellen kjenner igjen
- purposeRef: `purpose://candidate.agent-menu.app-identity`
- Utfører: **Codex**, samme gren
- Gjør (Kjetil 12.9: egen identitet; §6 spm. 11 standard): appen får egen CellProtocol-identitet (nøkkel i appens keychain-område), inngår kontrakt med cellen fra dens mal (admit → signContract → addAgreement, `GeneralCell.swift` l. 660–672) ved første oppstart, og forankres til agentens identitet gjennom den eksisterende paringsmekanismen (`AgentPairingArtifact`) som administrert identitet under Kjetil. **Ikke** enrollet i scaffoldet som egen entitet før Kjetil sier ja (eget steg, egen tillitspakke). Kontrollbro-tokenet brukes fortsatt ved WS-oppgraderingen (`CellBase.remoteWebSocketQueryItemsProvider`, `CellResolver.swift` l. 1664–1671).
- Tester: test.bridge.identity-negative (token uten identitet → `get` nektes; identitet + kontrakt → tillates; feil keypath nektes)
- Leverer: `TESTRESULT.md#identity`, avsnitt i `Docs/AgentMenylinje.md`

### WP-M1 — Appen er bro-klient og får hendelser
- purposeRef: `purpose://candidate.agent-menu.bridge-exists`, `purpose://candidate.corr-varsel.event-to-app`, `purpose://candidate.corr-varsel.absence-visible` (app-halvdelen), `purpose://candidate.corr-varsel.one-menubar-app`
- Utfører: **Codex**, samme gren
- Gjør: `AgentMenuModel` åpner én `BridgeBase` (transport: `LightweightBridgeTransport`, `ws://127.0.0.1:43110/bridgehead/agent-challenges/<bridgeId>`), abonnerer på cellens flow, gjør ett `get` ved oppstart og ved gjenoppkobling (backoff), fjerner `Timer` og `refreshInterval` (`AgentMenuModel.swift` l. 26–48); `/challenges`-HTTP beholdes bare som merket fallback når broen ikke kan åpnes (`test.bridge.only-path`); headeren viser bro-tilstanden («Bro til agenten: tilkoblet» / «Post: ikke lyttet» fra kildestatus, ikke antatt); varsler går som før via `ChallengeNotifier` (UNUserNotificationCenter), knapper `Åpne` / `Ignorer i dag` bygget av sakens svaralternativer; «Ignorer i dag» sendes som `set` til cellen (WP-A3); ingen ny seksjon i menyen (`MenuPresentation` uendret utover kildestatus).
- Tester: test.bridge.handshake, test.bridge.only-path, test.menu.event-latency (timer av, ≤ 5 s), test.menu.single-app, test.gui.parity (menu-new-message-v2, menu-correspondence-unreadable-v1)
- Leverer: kode + tester, `TESTRESULT.md#bridge`, `#menu-latency`, `ACCEPT.md#only-path`, `#single-app`, `#parity`

### WP-M2 — Oversikt og handling i adminflaten
- purposeRef: `purpose://candidate.corr-varsel.admin-overview-and-action`
- Utfører: **Codex**, samme gren
- Gjør: `AdminWindow` viser ny post som kort (fra, emne, kanal, svarvei) fra samme `get`, knappene «Åpne hos Losen» (åpner samtalen — kodevei defineres her: URL-scheme `haven://` mot Losen-flaten hvis den finnes, ellers adminvinduets egen visning med teksten «svar skrives hos Losen») og «Ignorer i dag» via `set`; kildelisten med correspondence «lytter» / «ikke lyttet». Ingen meldingstekst.
- Tester: test.challenge.answer-uses-real-path, test.gui.parity (admin-window-correspondence-v1)
- Leverer: `TESTRESULT.md#answer-path`, `ACCEPT.md#parity`

### WP-C — Commit-pakke etter hvert grønt bygg
- purposeRef: `purpose://quality.work-is-visible` (`lesson.branch-is-empty-after-eight-work-packages`)
- Utfører: **Codex** (commit per bladformål med purposeRef i meldingen, push etter første grønne bygg); **Kjetil** merger PR-er
- Sjekk: `git rev-parse pdd/corr-varsel` ≠ `git rev-parse origin/main` etter WP-A1; `Scripts/preflight_before_landing.sh` grønn før PR
- Leverer: PR-lenker i `STATUS.md`

### WP-V — Kjøring på Kjetils maskin og ekte varsel
- purposeRef: `purpose://candidate.corr-varsel.actually-in-center`, `purpose://candidate.corr-varsel.root`
- Utfører: **Kjetil** (ny binær i drift — HD-0070; varselsamtykke; våken skjerm), **Losen** (ber en motpart om en testmelding; sender ingenting selv uten ja)
- Gjør: `Packaging/menu-app/make_app.sh` → HAVEN Agent.app; ny `haven-agentd` med rollback klar (`.candidate`, signer, `mv`, `launchctl kickstart -k gui/501/io.digipomps.haven.agentd`, 25 s, `lsof -nP -iTCP:43110`); samtykkedialog; en ekte melding fra Vegar eller Lille Robot; skjermbilde av varselet; tre målinger av tid fra `createdAt` til varsel.
- Tester: test.notify.appears-in-center, test.corr.e2e-latency (≤ 60 s, tre forsøk), test.gui.parity (notification-new-message-v1)
- Leverer: `images/notification-actual-v1.png`, `TESTRESULT.md#e2e`, `#running`, `ACCEPT.md#parity`

### WP-Docs — Dokumentasjon i samme endring
- purposeRef: `purpose://quality.docs-in-same-change`
- Utfører: **Codex** (i hver gren), Claude leser diffen
- Gjør: `HavenAgentD::Docs/AgentMenylinje.md` (ny kilde, broen app ↔ agent, hva som skjer når hendelsesveien er nede), `CellScaffold`-dokumentasjon for correspondence-cellens feed, `Book/33_Correspondence_First_Class.md` får et avsnitt om mottaker-skopede hendelser — alle med «Last verified against code: <dato>».
- Tester: test.docs-updated
- Leverer: `ACCEPT.md#docs`

## 2. Hva som IKKE er i planen
- Multipeer- eller IPC-transport (B/C i §1b) — egen kandidat i CellProtocol.
- Enrollment av app-identiteten som egen entitet i scaffoldet (§6 spm. 11) — eget steg når Kjetil sier ja.
- iOS/iPadOS/watchOS.
- Løsning av HD-0070 (Launch Constraint) — egen sak, egen eier.
- Deploy-status i HAVEN Agent.app (HD-0075, etter at SwiftBar-pluginen HD-0022 ble forkastet 12.9) — egen bilderunde og egen PDD; denne planen rører den ikke, men WP-M1/M2 skal ikke bygge noe som gjør den vanskeligere (samme bro, samme adminflate).

## 3. Codex-handoff (pkg.std.codex-handoff)
Hver Codex-slice legges som jobb i køen (`HAVEN/_losen-queue/inbox/<id>.job` + `<id>.prompt.md`; køeierskap er HD-0025), aldri som innlimingskommando (`lesson.paste-command-instead-of-queue`). Prompten sier: repo, gren, eksakt mål, filer, ikke-forhandlingsbare krav fra `HavenAgentD::Docs/Bygg_og_landing.md` og §2 i FORMAALSSPEC, tester som skal bli grønne, og at slicen rapporterer «skrevet, ikke verifisert» til et detached bygg har kjørt (`lesson.syntax-check-reported-as-delivered`). Bygg og test kjøres som detached skript med logg i montert mappe.

## 4. Dataflyt
Se `dataflow.md` (diagram + kanttabell). Hver kant peker på kontrakt eller endepunkt; testen `test.cells.dataflow-matches-contracts` går over tabellen.
