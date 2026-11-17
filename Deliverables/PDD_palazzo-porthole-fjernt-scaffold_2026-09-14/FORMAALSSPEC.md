# Formålsspesifikasjon — Porthole laster flater fra eksternt scaffold (PalazzoScaffold over bro)

Oppgavemappe: `PDD_palazzo-porthole-fjernt-scaffold_2026-09-14` · Opprettet 2026-09-14 · Iterasjon 2 (G1 godkjent 2026-09-14, se §7) · HAVEN-Deploy: HD-0078

> Regel: ingen plan før G1 er godkjent av Kjetil. Et dokument om leveransen teller aldri som leveransen.
> Stier i dette dokumentet er relative til repoet de ligger i (`Repo::sti`). Hvor repoene ligger er en device-innstilling.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 2026-09-14 (svar på Losens forslag P1–P5 for HD-0078):

> Ja - men siden vi nå kjører i et eget scaffold kan vi flytte eventuelle https kall dit - så det ikke tynger CellScaffold. Pllazzo scaffoldet skal kunne kjøres selvstendig, men andre scaffold skal kunne nå Palazzo scaffoldet over Bridge. Kjør i gang Codex astra på dette så ser vi hvor langt vi kommer.

Utløsende måling samme dag: `run-g5.sh` (Sicilia G5) feilet i steg 4 for alle tre flater med Porthole `addConfiguration` → 400 «Configuration is not available in this Porthole yet.» (`PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.log`, `…/porthole-gjest-sicilia-liste/desktop/failure.txt`).

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Palazzo kjører i eget scaffold, selvstendig (bare CellBase+CellVapor+Vapor) | retrieved | `PalazzoScaffold::Package.swift`; git `6a3acf5` (main = origin/main, DiMy-io/PalazzoScaffold); 105 tester 2026-09-08 (`PalazzoScaffold::docs/Rapport_Sicilia_G7_2026-09-08.md`) |
| Andre scaffolds kan nå Palazzo over bro — transport | retrieved | `PalazzoScaffold::Sources/App/Controllers/PalazzoBridgehead.swift` (`isPublishable` inkl. `guestShell`, `content` — G7 B1); `CellScaffold::Sources/ScaffoldKit/RemoteBridgeheadAccess.swift` (`HAVEN_BRIDGEHEAD_TOKEN`/`HOSTS`, `registerRemoteHosts` → `resolver.registerRemoteCellHost`) — **ucommittet i CellScaffold-arbeidstreet per 2026-09-14** |
| Porthole i CellScaffold kan laste en flate publisert av Palazzo | **contradicted** | `CellScaffold::Sources/App/Controllers/PortholeWebSessionSupport.swift` `resolveRequestedCellConfiguration` (≈ linje 3644): oppslag `{name, sourceCellEndpoint}` matches bare mot `availableCellConfigurations` (egen katalog `availableCellConfigurations`, seks menykeypaths, delt workbench). `CellScaffold::Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift` `isPortholePublishedConfiguration` (≈ 2720) krever primærendepunkt i den statiske `portholeSupportedEndpoints` (≈ 134, kun `cell:///…`). Et fjernt endepunkt konsulteres aldri, og en direkte innsendt fjern konfigurasjon ville fått 422 «not web-ready». |
| Preview-verktøyet sender bare et navneoppslag | retrieved | `CellScaffold::scripts/skeleton-iterate.js` `ensureConfigurationLoaded` (≈ 362): `addConfiguration` med `configurationLookup: {name, sourceCellEndpoint}` |
| De eksporterte Palazzo-konfigurasjonene refererer lokale endepunkt | retrieved | `PalazzoScaffold::docs/sicilia-gui-evidence/inputs/gjest-sicilia-liste.cellconfiguration.json`: `discovery.sourceCellEndpoint = cell:///PalazzoGuestShell`, `cellReferences[].endpoint = cell:///PalazzoGuestShell`, `cell:///PalazzoEntity` |
| Palazzo publiserer konfigurasjonene på egne keypaths | retrieved | `PalazzoScaffold::Sources/App/Support/PalazzoScaffoldContract.swift`: `guest.configuration`, `guest.article.configuration`, `content.configuration`, `staff.configuration` |
| «HTTPS-kall kan flyttes til PalazzoScaffold» | retrieved (delvis) | `PalazzoScaffold::Sources/App/routes.swift` har full HTTP-API inkl. `POST /api/concierge/*`; `PalazzoScaffold::Public/` er tom (README) → den offentlige leaf-flaten porteres i `PDD_palazzo-concierge-native-web_2026-09-14`, ikke her |

Ingen `recalled`-påstand bærer planen.

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome · successSignals · verifier) | Status |
|---|---|---|---|---|
| purpose://candidate.palazzo-porthole-fjernt-scaffold.root | Flater publisert av PalazzoScaffold vises i Porthole i et annet scaffold over bro, uten at Palazzo-celler kopieres inn i CellScaffold | purpose://scaffold.operations (Book 23, candidate) | outcome: `run-g5.sh` avsluttes `G5 DONE` · signals: tre `porthole-*-{desktop,mobile}-v1.png` i sicilia-PDD-ens `images/verify/` · verifier: test.g5 (artifact, Kjetil kjører) | candidate |
| purpose://candidate.palazzo-porthole-fjernt-scaffold.remote-lookup | Et navngitt oppslag med fjernt `sourceCellEndpoint` og eksplisitt `keypath` henter konfigurasjonen fra den cellen | root | outcome: `addConfiguration {configurationLookup:{name:"Palazzo Gjest", sourceCellEndpoint:"cell://127.0.0.1:18083/PalazzoGuestShell", keypath:"guest.configuration"}}` → 200 og aktiv konfigurasjon heter «Palazzo Gjest» · signals: `expectActiveConfiguration` grønn i preview · verifier: test.remote-lookup (XCTVapor, bro i minnet etter mønster `PalazzoScaffold::Tests/AppTests/PalazzoBridgeheadTests.swift` B2) | candidate |
| purpose://candidate.palazzo-porthole-fjernt-scaffold.trust-boundary | Bare verter i `HAVEN_BRIDGEHEAD_HOSTS` (med token) kan være kilde for fjerne flater | root | outcome: oppslag mot vert utenfor listen → 400 som i dag, uten nettverkskall · signals: negativ test grønn; ingen resolver-kall i loggen · verifier: test.trust-boundary | candidate |
| purpose://candidate.palazzo-porthole-fjernt-scaffold.reference-rewrite | Referanser `cell:///X` i en fjern konfigurasjon skrives om til `cell://host:port/X` før lasting, så flaten leser data fra riktig scaffold | remote-lookup | outcome: `discovery.sourceCellEndpoint` og alle `cellReferences[].endpoint` bærer vert:port etter lasting · signals: lesing av `guest.guest.state.house.headline` gjennom lastet konfig gir Palazzos verdi · verifier: test.reference-rewrite (enhet) + test.remote-lookup (integrasjon) | candidate |
| purpose://candidate.palazzo-porthole-fjernt-scaffold.published-allowlist | `isPortholePublishedConfiguration` godtar en konfigurasjon hvis primærendepunkt ligger på en bridgehead-godkjent vert; lokal allowlist uendret | trust-boundary | outcome: true for `cell://127.0.0.1:18083/PalazzoGuestShell` når verten er godkjent, false ellers; uendret for lokale endepunkt · verifier: test.allowlist | candidate |
| purpose://candidate.palazzo-porthole-fjernt-scaffold.preview-tool | `skeleton-iterate` preview kan sende `keypath`, og `run-g5.sh`/inputs bruker det for alle tre flater | root | outcome: `--configurationKeypath` (eller scenario-felt) sendes i `configurationLookup`; `run-g5.sh` setter riktig keypath per flate · verifier: test.g5 + `node --check` | candidate |
| purpose://quality.build-and-regression | (pkg.std.everything-works) | root | test.build, test.regression (avgrenset, se §5) | package |
| purpose://quality.docs-in-same-change | (pkg.std.everything-works) | root | test.docs-updated: `CellScaffold::Documentation/Skeleton_Runtime_Iteration_Workflow.md` får avsnittet «Flater fra eksternt scaffold», datert | package |
| purpose://quality.work-is-visible | (pkg.std.everything-works) | root | test.status-current | package |

Designvalg som følger av formålene (kan overprøves av Kjetil): oppslaget bærer **eksplisitt `keypath`** for fjerne kilder — ingen magisk konvensjon, og `purpose://prompt.unknown`-prinsippet: mangler keypath for et fjernt endepunkt, feiler oppslaget lukket med tydelig grunn. Tillitsgrensen gjenbruker B3 (`RemoteBridgeheadAccess`) — ingen ny konfigurasjon.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke native (Binding) visning — G6/NATIVE.md i sicilia-PDD-en er egen slice.
- Ikke flytting av Palazzo-celler inn i CellScaffold, og ingen endring i CellProtocol. Kan ikke resolveren gi en fjern celle for `cell://host:port/Cell` etter `registerRemoteHosts`, stoppes arbeidet og rapporteres — det skal ikke omgås.
- Ikke conciergen eller den offentlige leaf-flaten (`PDD_palazzo-concierge-native-web_2026-09-14`), ikke deploy (HD-0077), ikke identitets-/entitetsutvidelse (`PDD_palazzo-entity-utvidelse-begge-veier_2026-09-14`).
- Ikke endring av selve Palazzo-konfigurasjonene eller skeletons (de eksporterte er sannheten; kun endepunkt-omskriving ved lasting).

Kapabiliteter og avhengigheter (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Bridgehead-token/verter i CellScaffold (B3) | `CellScaffold::Sources/ScaffoldKit/RemoteBridgeheadAccess.swift`, `…/AdminAuthenticatedVaporBridgeTransport.swift`, `CellScaffold::Sources/App/configure.swift` | Ucommittet i arbeidstreet; dekker transport og ruting, ikke oppslag/allowlist | Ja — verifier: filene finnes, `RemoteBridgeheadAccessTests` grønn (`PalazzoScaffold::docs/sicilia-g7-evidence/b3-final.log`: 18/18 2026-09-08) |
| Palazzo publiserer `PalazzoGuestShell`/`PalazzoContent` over bridgehead (G7 B1) | `PalazzoScaffold::Sources/App/Controllers/PalazzoBridgehead.swift` `isPublishable` | Krever `PALAZZO_BRIDGEHEAD_ENABLED=true` + token; hydrering av lokale identitetsdeskriptorer er fortsatt merket i kilden | Ja — verifier: `PalazzoBridgeheadTests` grønn |
| Palazzo kjørende på 18083 med bridgehead, CellScaffold på 18080 (run-g5 steg 1–3) | `PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.sh` | Bare på Kjetils Mac (TCP-bind nektes i Codex-sandkassen) | Ja for test.g5 — verifier: `run-g5.log` «Klar: …18083», «Klar: …18080» (grønt 2026-09-14) |
| CellScaffold kan bygges/testes avgrenset i kø-sandkassen | `PalazzoScaffold::docs/sicilia-g7-evidence/swiftpm-local-runner.sh` + `CellScaffold::scripts/run_tests_isolated.sh --filter` | `lesson.codex-workspace-write-cannot-build-cellscaffold`: full regresjon er ikke mulig i kø; bare filtrerte klasser (virket 2026-09-08 for 18 tester) | Ja for test.regression (avgrenset) — ellers «skrevet, ikke verifisert» + KJOR-SELV |
| Preview-verktøy og eksporterte inputs | `CellScaffold::scripts/skeleton-iterate.js`, `PalazzoScaffold::docs/sicilia-gui-evidence/inputs/*.cellconfiguration.json`, `g5-*-preview.log` | Inputs er eksportert 2026-09-07 fra XCTVapor; ikke re-eksportert | Ja — verifier: filene finnes |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Kildeendringer i CellScaffold (PortholeWebPayloads.swift, PortholeWebSessionSupport.swift, ConfigurationCatalogCell.swift, scripts/skeleton-iterate.js) + nye tester | fil | `CellScaffold::…` (filliste i TESTRESULT.md#files) | §1 | nei |
| `run-g5.sh` og inputs oppdatert med keypath per flate | fil | `PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.sh`, `inputs/` | §1 preview-tool | nei |
| TESTRESULT.md med ankre #build #regression #remote-lookup #trust #rewrite #allowlist #files | testutdata | denne mappen | §5 | nei |
| `G5 DONE` og seks PNG-er (`porthole-{gjest-sicilia-liste,gjest-sicilia-artikkel,hus-artikkel-tagger}-{desktop,mobile}-v1.png`) | bilde | `CellProtocolDocuments::Deliverables/PDD_palazzo-sicilia-artikler_2026-09-07/images/verify/` | `images/` her (arvet fra sicilia G1-GUI, godkjent 2026-09-07) | nei — Kjetil kjører run-g5.sh etter Codex-leveransen |
| Avsnitt «Flater fra eksternt scaffold» | fil | `CellScaffold::Documentation/Skeleton_Runtime_Iteration_Workflow.md` (Last verified against code) | §1 docs | nei |
| ACCEPT.md: forventning mot faktisk, side om side for de tre flatene | fil | denne mappen | §3 | nei |

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
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra (når Porthole-preview er brukt).
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
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
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
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://scaffold.operations [candidate] — Scaffold operations

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | ./<skript>.sh (uten --go) | TESTRESULT.md#dry-run | venter |

## 6. Åpne spørsmål til Kjetil

1.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-14 | Opprettet | Losen |


## 5. Avledede tester

| test | type | hvordan | bevis |
|---|---|---|---|
| test.build | command | `swift build` av CellScaffold via isolert runner (se §2) | TESTRESULT.md#build |
| test.regression (avgrenset) | command | `HAVEN_SWIFTPM_RUNNER=<PalazzoScaffold::docs/sicilia-g7-evidence/swiftpm-local-runner.sh> zsh scripts/run_tests_isolated.sh --filter 'PortholeWeb|ConfigurationCatalog|RemoteBridgeheadAccess|AdminAuthenticatedVaporBridgeTransport|AdminControlPlaneRouting'` i CellScaffold; tallene oppgis som «forventet ≈ N (fra baseline samme kjøring)» | TESTRESULT.md#regression |
| test.remote-lookup | command | XCTVapor: Palazzo-app + CellScaffold-Porthole med bro i minnet; `addConfiguration` med keypath → 200, aktiv konfig «Palazzo Gjest», lesing av `guest.guest.state.house.headline` | TESTRESULT.md#remote-lookup |
| test.trust-boundary | command | samme oppslag mot vert utenfor `HAVEN_BRIDGEHEAD_HOSTS` → 400, ingen resolver-kall; uten keypath → 400 med grunn | TESTRESULT.md#trust |
| test.reference-rewrite | command | enhetstest: `cell:///PalazzoGuestShell` → `cell://127.0.0.1:18083/PalazzoGuestShell` for discovery + alle cellReferences; lokale CellScaffold-konfigurasjoner uendret | TESTRESULT.md#rewrite |
| test.allowlist | command | `isPortholePublishedConfiguration` true/false-matrise (lokal kjent, lokal ukjent, fjern godkjent, fjern ikke godkjent) | TESTRESULT.md#allowlist |
| test.preview-tool | command | `node --check scripts/skeleton-iterate.js`; `bash -n run-g5.sh`; keypath synlig i `input.json` for hver flate | TESTRESULT.md#preview-tool |
| test.g5 | artifact | Kjetil: `bash <PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.sh>` → siste linje `G5 DONE`, seks PNG-er | sicilia-PDD `images/verify/`, ACCEPT.md#parity |
| test.docs-updated | inspection | doc-diff for endret oppførsel, datert | ACCEPT.md#docs |
| test.status-current | inspection | STATUS.md speiler tilstand | ACCEPT.md#status |

## 6. Åpne spørsmål (bare de som endrer treet)

1. Eksplisitt `keypath` i oppslaget (valgt) mot discovery-basert oppslag via `PalazzoScaffoldInfo`. Valgt eksplisitt fordi det er testbart og feiler lukket; discovery kan legges oppå senere.
2. Skal godkjente fjerne verter på sikt være scaffold-policy (celle) i stedet for miljøvariabel? Ikke i denne slicen; notert for scaffold-admin-PDD-en.

## 7. Iterasjoner

| # | dato | hva endret seg |
|---|---|---|
| 1 | 2026-09-14 | P1–P5 lagt fram i chat (Losen) etter run-g5-feilen; Kjetil: «Ja», med presisering: HTTPS-kall kan bo i PalazzoScaffold, scaffoldet kjører selvstendig, andre scaffolds når det over bro |
| 2 | 2026-09-14 | Denne filen: tre + audit + kontrakt; presiseringen lagt i §2 (leaf/HTTPS → egen PDD). G1 satt godkjent på Kjetils ord; G2 auto («Kjør i gang Codex astra på dette») |
