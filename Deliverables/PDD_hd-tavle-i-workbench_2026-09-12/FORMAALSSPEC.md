# Formålsspesifikasjon — hd tavle i workbench

Oppgavemappe: `PDD_hd-tavle-i-workbench_2026-09-12` · Opprettet 2026-09-12 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> HD-Tavla er veldig bra - dette må vi få inn i developer/admin workbench. Når de har status klar så bør jeg kunne starte jobben manuelt også. Dette mønsteret kan brukes for en liste med ideer jeg vil huske og eventuelt jobbe videre med - så vi trenger også referanser til eller direkte verktøy som vil hjelpe brukeren med å enten komme til konklusjonen at det skal forkastes - eller et ærefullt hjem (for ideen) i deployed prod. F.eks HD-0023: Her er det egentlig litt uklart hva jeg skal gjøre men om de to røde kunne tatt meg til et verktøy hvor jeg både kan få mer kontekst og funksjonalitet til å utføre det som enn skal til for å komme ett skritt videre, så hadde det hjulpet meg enormt.

| Påstand i intensjonen / antatt kapabilitet | Audit (retrieved / recalled / unavailable / contradicted) | Kilde |
|---|---|---|
| «HD-Tavla» finnes som artefakt med 68 HD-er, status, eier, behov, siste notat | retrieved | Cowork-artefakt «HD-tavla» (2026-09-12), data i `HAVEN-Deploy/index/hd-board.json` |
| Det finnes en developer/admin workbench i CellScaffold | retrieved, **delvis**: `/workbench` er en redirect til `/docs` (Documentation Workbench); chat har `workbench/modules`; egne workbench-celler finnes (SecurityWorkbench, AgreementWorkbench, TrustPacketWorkbench, WorkbenchAccessGrant). Ingen «HD»- eller kø-flate finnes | `CellScaffold/Sources/App/Controllers/VaporDocumentationWorkbench.swift:32`, `VaporPersonalCopilot.swift:554-558`, `Sources/App/Cells/*Workbench*` |
| Workitems finnes som celle | retrieved: `WorkItemCell` (3183 linjer) med `WorkItemKind` (idea, feature, bug, chore, docs, research, decision, question, implementation-gap), `WorkItemStatus` (new, triage, ready, blocked, in-progress, done, wont-do), prioritet, evidens-poster; `ProjectPortfolioCell` samler dem; `cell:///WorkItem` er katalogført | `CellScaffold/Sources/App/Cells/WorkItems/WorkItemCell.swift:7-68`, `ProjectPortfolioCell.swift:182,214` |
| «Status klar» finnes i hd | retrieved: hd-status `READY` (1 oppgave i dag: HD-0020); `hd task next` gir eldste utførbare | `HAVEN-Deploy/tools/hd.py` (`task {new,set,need,post,show,list,next}`) |
| Jobben kan startes manuelt | retrieved, **delvis**: hd har `--executor {codex,claude-local,claude-cloud,cell}` + `--job-prompt/--cwd` på `task new`, og en dispatcher-launchagent finnes men er ikke lastet (HD-0024); losen-queue kjører `.job`-filer i `_losen-queue/inbox`. Ingen «start»-kommando i hd som lager køjobb fra en eksisterende oppgave er funnet (`hd task --help`) | `hd.py`, HD-0024, HD-0025, `_losen-queue/logs/runner.log` |
| Workbench leser `index/status.json` | contradicted i dag: ingen fil i `Sources`/`Public` leser `haven.deploy.status.v1`; det er HD-0021 (PREPARING) | `grep -rln 'status.json' CellScaffold/Sources` → kun `HAVENAgentCapabilityBrokerCell.swift:87` (annen fil) |
| HD-0023 har «to røde» | retrieved: tre uoppfylte behov: `coordination:verten`, `approval:kjetil`, `script:CellScaffold/scripts/production/haven-deploy` (tavla viser 0/3, alle røde) | `HAVEN-Deploy/queue/tasks/HD-0023.json` |
| Behov (`needs`) har typer med kjent semantikk | retrieved: kind ∈ {file, script, approval, coordination, pin, secret, image, disk}; `hd task need --satisfied kind:ref --evidence` oppfyller ett behov | `hd.py`, `queue/tasks/*.json` |
| hd er eneste lager for oppgaver | recalled/besluttet i HD-0041 (PREPARING, venter på Kjetils bekreftelse). Legges til grunn som **premiss**, ikke som faktum | HD-0041 |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.hd-tavle.root | Oppgaver og ideer har ett sted i workbenchen, og hver post viser veien til neste skritt | purpose://gui.quality.functional-accessible | Kjetil åpner workbenchen og ser alle HD-er som workitems med status, eier, behov og siste notat, uten å spørre noen | Flaten viser samme antall som `hd task list` (68 i dag) | candidate |
| purpose://candidate.hd-tavle.projection | hd-oppgaver projiseres som WorkItems uten nytt lager | root | Hver HD-nnnn rendres som WorkItem (kind/status mappet 1:1, se §2), lest fra hd sin projeksjon (`index/status.json` + oppgave-JSON), aldri kopiert inn i WorkItemCell sitt lager | `test.hd.projection-count`: antall rader = antall `queue/tasks/HD-*.json`; en endring via `hd task set` er synlig i flaten etter neste regenerering | candidate |
| purpose://candidate.hd-tavle.filters | Status, eier og «venter på deg» kan filtreres | root | Samme filtre som HD-Tavla: status-fliser, eier, søk, «venter på deg» (uoppfylt approval-behov) | `test.hd.filter-waits-on-you`: tallet på flisen = antall oppgaver med uoppfylt `approval` | candidate |
| purpose://candidate.hd-tavle.start-ready | En oppgave med status klar kan startes manuelt fra flaten | root | «Start»-knappen på en READY-oppgave med registrert executor legger jobben i riktig kø (losen-queue `.job` + `.prompt.md` for codex; claude-local/cloud etter HD-0025) og oppgaven går til RUNNING; uten executor er knappen erstattet av «Mangler utfører» med lenke til å sette den | `test.hd.start-creates-job`: trykk Start på testoppgave → ny `.job` i inbox med samme id og `hd task show` viser status endret; `test.hd.start-refused-without-executor` | candidate |
| purpose://candidate.hd-tavle.need-to-tool | Hvert uoppfylt behov peker på verktøyet som oppfyller det | root | Et rødt behov er en lenke/handling, ikke bare tekst: `approval` → godkjenningsdialog som kaller `hd task need --satisfied`; `script`/`file` → åpner filen i workbench (eller sier at den mangler, med sti); `coordination` → viser `hd coord status` og lar Kjetil ta claim; `pin`/`image`/`secret`/`disk` → viser målt tilstand og den kommandoen som fikser det. HD-0023 skal vise tre slike veier | `test.hd.need-has-way-in`: for hver `needs.kind` i registeret finnes en handling i `reachableActionKeypaths`; HD-0023 rendres med tre klikkbare behov | candidate |
| purpose://candidate.hd-tavle.context | Flaten gir konteksten som trengs for å avgjøre neste skritt | root | Åpen rad viser formål, alle behov med bevis, avhengigheter (klikkbare), notater kronologisk, og lenkene i notatene (filstier, PR-er, kjøringer) som åpnbare | `test.hd.context-complete`: HD-0056 åpen viser 1 behov med bevis, 2 notater og lenke til run 34574674480 | candidate |
| purpose://candidate.hd-tavle.ideas | Ideer registreres i samme flate og følger samme vei | root | Kjetil kan legge inn en idé (kind=idea) med én setning; den får en HD-id via `hd task new` med `--origin kjetil`, status PREPARING, og ligger i samme liste med filter «ideer» | `test.hd.idea-roundtrip`: opprett idé i flaten → `queue/tasks/HD-nnnn.json` finnes med mutation_type=idea | candidate |
| purpose://candidate.hd-tavle.honourable-end | Hver post ender enten i prod eller som synlig forkastet | root | To sluttveier per post: «Forkast» (krever begrunnelse, skriver AVVIST + lesson-kandidat) og «I prod» (krever bevis: commit i `main_i_production`); ingen post kan forsvinne uten en av dem. Avhenger av HD-0045 (ferdig-tilstand for ikke-deploy) | `test.hd.no-silent-close`: en post uten AVVIST-grunn eller prod-bevis kan ikke settes til lukket | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke et nytt oppgavelager: WorkItemCell sitt eget lager brukes ikke som kilde; hd er kilden (premiss fra HD-0041, se §6 sp. 1).
- Ikke en erstatning for `hd`-CLI-en; flaten kaller de samme kommandoene/kontraktene.
- Ikke automatisk start av jobber (det er HD-0024/dispatcher); bare manuell start fra flaten.
- Ikke deploy: «I prod»-bevis leses fra `leveransegap.main_i_production`, flaten deployer aldri selv.
- Ikke Binding/iOS i første omgang; web (CellScaffold/Porthole) først. Paritet er egen slice (lesson.scaffold-without-porthole-host-has-no-preview).

Kapabiliteter og avhengigheter oppgaven bygger på (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| hd-projeksjon `index/status.json` (schema haven.deploy.status.v1) og `queue/tasks/HD-*.json` | `HAVEN-Deploy/tools/hd.py status --write` | status.json har banene ko/forkastet/utført med endringspakker; HD-detaljer (purpose, needs, notes) må hentes fra oppgave-JSON + events. I dag er `index/hd-board.json` en engangsdump laget 12.09 — den må bli en del av `hd status --write` (egen WP) | ja |
| Projeksjonen servert fra verten (`/deploy/status.json`) | HD-0023 (HANDOFF_REQUIRED) | Uten dette virker flaten bare lokalt mot montert fil. Første leveranse er lokal; HD-0023 er avhengighet for deployet variant | nei for lokal, ja for prod |
| WorkItem-modellen | `CellScaffold/Sources/App/Cells/WorkItems/WorkItemCell.swift` | Statusmapping: PREPARING→triage, READY→ready, HANDOFF_REQUIRED→blocked, DEPLOYING/RUNNING→in-progress, COMMITTED_VERIFIED→done, AVVIST→wont-do. Kind: deploy→chore, code→feature/bug, idea→idea. Mappingen er en kontrakt (contract/) og testes | ja |
| Skeleton-format: List/Grid med radmal, betinget synlighet, actions med keypath | `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift` (KAPASITET_SKJELETT.md 11.09) | Ingen «Tree»; fliser+liste+åpen rad er innenfor formatet. Klikkbar lenke til ekstern URL (GitHub run) må verifiseres i rendereren før §3 lover det | ja |
| Start av jobb: losen-queue (`.job` + `.prompt.md` i `_losen-queue/inbox`) | `_losen-queue/logs/runner.log`, lesson.paste-command-instead-of-queue | Bare codex-executor er bevist i drift. claude-local/claude-cloud/cell avhenger av HD-0025-avgjørelsen | ja for codex |
| Godkjenning via `hd task need --satisfied approval:<ref> --evidence` | `hd.py` | Ingen autentisering i hd; flaten må være bak workbench-innlogging (`isAdmin`) — purpose gir ikke rettighet (lesson.purpose-never-grants-rights) | ja |
| Ferdig-tilstand for ikke-deploy-oppgaver | HD-0045 (PREPARING) | Uten den kan «Forkast»/«I prod» ikke lukke en ikke-deploy-oppgave. Blad `honourable-end` er blokkert til HD-0045 er løst | ja for honourable-end |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
**GUI-oppgave:** hver flate og hver viktig tilstand (tom, fylt, feil) må ha et rendret bilde i `images/` som Kjetil har godkjent før G1-GUI. Porthole-preview av skeleton-JSON når formatet tillater det; ellers mockup med eksplisitt liste over hva dagens skeleton ikke kan rendre.
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse (images/…-v1.png osv.) | Godkjent |
|---|---|---|---|---|
| HD-tavle i workbench, fylt tilstand (68 poster, fliser, filtre) | bilde → kjørende flate | Porthole-preview av skeleton-JSON; fallback HTML-mockup fra HD-Tavla-artefakten i samme viewport (1180 px) | images/hd-tavle-fylt-v1.png | nei |
| Åpen rad HD-0023 med tre klikkbare behov, hvert med «neste skritt»-verktøy | bilde → kjørende flate | samme | images/hd-tavle-hd0023-behov-v1.png | nei |
| Godkjenningsdialog for et `approval`-behov (kontekst + «Godkjenn»/«Avvis med grunn») | bilde → kjørende flate | samme | images/hd-tavle-godkjenn-v1.png | nei |
| READY-oppgave med «Start»-knapp, og samme oppgave uten executor («Mangler utfører») | bilde → kjørende flate | samme | images/hd-tavle-start-v1.png, images/hd-tavle-start-mangler-utforer-v1.png | nei |
| Ny idé: inntastingsrad + posten slik den ser ut i lista etterpå | bilde → kjørende flate | samme | images/hd-tavle-ide-v1.png | nei |
| Tom tilstand (ingen treff på filter) | bilde | samme | images/hd-tavle-tom-v1.png | nei |
| `hd status --write` skriver også `index/hd-board.json` (HD-detaljer) | fil + testutdata | HAVEN-Deploy/tools/hd.py, TESTRESULT.md#hd-board | — | nei |
| Kontrakt hd→WorkItem (status/kind-mapping, needs→handling) med fixtures | fil | contract/hd_workitem_projection_v1.json | — | nei |
| Skeleton/CellConfiguration for flaten | fil | skeleton/hd-tavle.json | — | nei |
| Kjørende flate lokalt i Porthole/web, alle §5-tester grønne | kjørende flate + testutdata | TESTRESULT.md, ACCEPT.md#parity | — | nei |

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
- **lesson.test-the-representation-not-the-issuance-flow** (2026-09-09, minor): Alle fire WP4-rolletestene feilet i oppsettet, ikke i det de skulle teste: `deniedNoGrant` på `requestEntry` mot `cell:///AdminEntry`. Testen fikk aldri gitt identiteten rollen.
    - forebygging: Skille to spørsmål: «hvordan får noen rollen» og «hva gir rollen». Tester du det andre, installer rollen på husets etablerte måte og test virkningen. Let alltid etter en eksisterende `*TestSupport`-hjelper før du bygger oppsettet selv — `grep -rn "TestSupport" CellScaffold::Tests` — og se hvilke argumenter de andre testene gir den.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.campaign.complete [active] — Complete questionnaire campaign
- purpose://questionnaire.admin.authoring [active] — Questionnaire admin authoring
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI

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
| test.hd.projection-count | purpose://candidate.hd-tavle.projection | Sammenlign antall rader i flaten med `ls queue/tasks/HD-*.json | wc -l`; endre én oppgave med `hd task set --note`, regenerer, se notatet i flaten. | TESTRESULT.md#projection | venter |
| test.hd.filter-waits-on-you | purpose://candidate.hd-tavle.filters | Tell oppgaver med uoppfylt approval i JSON; sammenlign med flisen. | TESTRESULT.md#filters | venter |
| test.hd.start-creates-job | purpose://candidate.hd-tavle.start-ready | Testoppgave READY med executor codex; trykk Start; forvent `<id>.job`+`.prompt.md` i `_losen-queue/inbox` og statusendring i `hd task show`. | TESTRESULT.md#start | venter |
| test.hd.start-refused-without-executor | purpose://candidate.hd-tavle.start-ready | Samme uten executor; forvent ingen jobbfil og synlig «Mangler utfører». | TESTRESULT.md#start | venter |
| test.hd.need-has-way-in | purpose://candidate.hd-tavle.need-to-tool | For hver behovstype i registeret: SkeletonReachabilityAudit viser en handling; HD-0023 rendres med tre klikkbare behov. | ACCEPT.md#ways-in | venter |
| test.hd.approve-writes-evidence | purpose://candidate.hd-tavle.need-to-tool | Godkjenn et approval-behov i flaten; `hd task show` viser satisfied=true med evidens som navngir hvem/når. | TESTRESULT.md#approve | venter |
| test.hd.context-complete | purpose://candidate.hd-tavle.context | Åpne HD-0056: 1 behov m/bevis, 2 notater, lenke til run 34574674480 er klikkbar (eller eksplisitt ikke støttet av renderer, se §2). | ACCEPT.md#context | venter |
| test.hd.idea-roundtrip | purpose://candidate.hd-tavle.ideas | Opprett idé i flaten; forvent ny HD-fil med origin=kjetil og kind idea; slett den igjen via AVVIST med grunn «test». | TESTRESULT.md#idea | venter |
| test.hd.no-silent-close | purpose://candidate.hd-tavle.honourable-end | Forsøk lukking uten grunn/bevis; forvent avslag. Blocked til HD-0045. | TESTRESULT.md#close | blocked (HD-0045) |

## 6. Åpne spørsmål til Kjetil

1. **Lager.** hd som eneste lager (HD-0041) og WorkItemCell som ren projeksjon — bekrefter du det? Alternativet er å importere HD-ene inn i WorkItemCell sitt lager og synke tilbake, som gir to sannheter.
2. **Hvor i workbenchen.** `/workbench` er i dag en redirect til `/docs`. Skal HD-tavla være (a) en egen rute `/workbench/hd` bak admin-innlogging, (b) en modul i chat-workbenchen (`workbench/modules`), eller (c) inn i ProjectPortfolio-flaten som en egen bane? Jeg foreslår (a) først, (c) når HD-0021 leveres.
3. **Start.** Skal «Start» bare gjelde executor=codex (bevist kø) i første leveranse, og claude/cell vente på HD-0025? Foreslår ja.
4. **Ideer.** Skal en idé være en HD-oppgave med `mutation_type=idea` (én liste, ett lager), eller en egen liste utenfor hd? Foreslår HD med kind idea, så «forkast/prod»-veien er den samme.
5. **Godkjenning i flaten.** En «Godkjenn»-knapp skriver `hd task need --satisfied approval:… --evidence "kjetil via workbench <ts>"`. Er det nok bevis for deg, eller skal den kreve en setning?
6. **Rekkefølge.** Første leveranse = lese + filtrere + behov-som-verktøy + godkjenn (blad projection, filters, need-to-tool, context). Start, ideer og honourable-end som andre leveranse etter HD-0025/HD-0045. Enig?

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-12 | Opprettet | Losen |
| 1 | 2026-09-12 | §0 audit (9 påstander), §1 åtte formål, §2 avgrensning + 7 kapabiliteter, §3 ti leveranser, §5 ni HD-tester, §6 seks spørsmål | Claude |
