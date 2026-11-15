# PLAN — dokument- og argumentanalyse for studentene (G2-utkast 2026-11-15)

Grunnlag: FORMAALSSPEC.md iterasjon 1c, G1 og G1-GUI godkjent av Kjetil 2026-11-15.
Baser: CellScaffold `origin/main` `8e8f8e0` (= staging), CellProtocol `origin/main` `14fd9dc`.

## Hvor ting bygges og testes

- Skyøkten har ingen Swift-verktøykjede (download.swift.org er blokkert). Den skriver kode, JS-tester (Playwright) og Python-paritetsfixtures.
- Swift-bygg og tester (CellScaffold `ci/run-tests.sh`, CellProtocol `swift test`, Binding XCTest) kjøres på Mac-en via Remote Control i **egne ferske kloner under /tmp**, aldri i `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold` (den står på en Codex-gren med ukommitterte endringer).
- PR-CI i CellScaffold kjører bare «Focused control-plane gates» og bilde-sjekker, ikke hele testmengden. Derfor er Mac-kjøringen porten før noe går i Deploy-køen.
- Rekkefølge mellom repoer: CellProtocol-endringen (WP1, WP3) må merges og tagges av Kjetil før CellScaffold kan pinne den (WP9). Fram til da peker CellScaffold-grenen på CellProtocol-PR-ens commit bare i Mac-kjøringen, ikke i Package.swift på main.

## Arbeidspakker (1:1 mot bladformål)

| WP | purposeRef | Hva | Repo / gren | Utfører | Test som må bli grønn | Artefakt (§3) |
|---|---|---|---|---|---|---|
| WP0 | quality.build-and-regression | Baseline: CellScaffold `ci/run-tests.sh` og CellProtocol `swift test` på ren eksport av main; Binding macOS XCTest på main | Mac (RC) | Claude via RC | test.build, test.regression (tall registreres, røde = egne avvik) | TESTRESULT.md#baseline |
| WP1 | tekstanalyse.argumentgraf | `ArgumentMapVisualizationSpec` i CellBase (Codable, validering, fallback for ukjent rolle/relasjon) + kontrakt-fixtures fra `contract/argumentmap.v1.schema.json` | CellProtocol `claude/argumentmap-visualization` | Claude | test.cell.contract-fixtures (positive/negative) | PR i CellProtocol |
| WP2 | tekstanalyse.argumentgraf | Web-renderer `kind: "argumentmap"` i `Public/js/skeleton-runtime.js`: lagdelt layout ovenfra, SVG-kanter med tekst, stiplet for antatt, klikk → `selectedID` | CellScaffold `claude/tekstanalyse` | Claude | Playwright: noder/kanter/etiketter telles, klikk sender handling, bilde mot `images/argumentkart-mockup-laptop-v1.png` | TESTRESULT.md#graf |
| WP3 | tekstanalyse.argumentgraf | CellApple-renderer i `SkeletonView.swift` (samme layoutalgoritme som web, porteres linje for linje) + parity-matrise-oppføring | CellProtocol (samme PR som WP1) | Claude skriver, Mac bygger | Binding `SkeletonSnapshotRenderXCTest` med argumentmap-korpus; CellApple bygger for macOS og iOS | TESTRESULT.md#graf, ACCEPT.md#parity |
| WP4 | tekstanalyse.grunnlinje, .paastander, .kilder | `TextReliabilityAnalyzer` i Swift: setninger, markdown-struktur, påstandstype/styrke, kildereferanser, kildestatus, retorikk, argument_map. Golden-fixtures laget av Python-verktøyet | CellScaffold | Claude | T-PARITET (sortert JSON lik Python på alle fixtures), T-SITAT, T-KILDE | TESTRESULT.md#paritet |
| WP5 | tekstanalyse.inntak, .samarbeid, .tilgang | `TextAnalysisRoomCell`: inntak (lim inn, FileUpload ≤1 MB txt/md), state, markeringer per identitet, kommentarer, Flow `analysis.change`, chat via CellBase `ChatCell`, Agreement-vilkår `audience.admission.member` / `invitationAccepted`; provisioning-modus erklært (lesson.new-cell-must-declare-its-provisioning-mode) | CellScaffold | Claude | T-INNTAK, T-SAMARBEID, T-TILGANG (fremmed, tilbaketrukket, feil keypath, `purpose://prompt.unknown`) | TESTRESULT.md#inntak/#samarbeid/#auth |
| WP6 | tekstanalyse.modellhjelp, .panel | Modellforslag via `AIGatewayCell.invokePurposeBound`; `QuoteAnchorValidator`; forslag godta/avvis; panel via parallell orkestrering + dommer; feiler uavhengig av grunnlinjen | CellScaffold | Claude | T-MODELL-ANKER, T-MODELL-NEDE, T-PANEL (falsk modell i test) | TESTRESULT.md#modell/#panel |
| WP7 | tekstanalyse.eksport | JSON etter `haven.text_reliability.analysis.v1` + markeringer, og Mermaid | CellScaffold | Claude | T-EKSPORT (validerer mot `Book/text_reliability_analysis_contract_v1.json`) | `results/` |
| WP8 | tekstanalyse.root (flate) | Skeleton-fabrikk fra `skeleton/analyserom-skeleton.js` + argumentmap, katalogoppføring så Butler/Bibliotek finner «Analyserom», mobil: chat som egen fane | CellScaffold | Claude | test.skeleton.no-unreachable-elements, purpose-actions-reachable, test.gui.parity mot godkjente bilder | ACCEPT.md#parity |
| WP9 | quality.build-and-regression | Mac-kjøring: CellProtocol `swift test` + Binding mot PR-commit; CellScaffold `ci/run-tests.sh` mot samme; ingen nye røde mot WP0 | Mac (RC) | Claude via RC | test.build, test.regression | TESTRESULT.md#build/#regression |
| WP10 | tekstanalyse.root | Etter Kjetils merge/tag av CellProtocol: pin-løft i CellScaffold, FORESPOERSEL til Deploy, så to nye studentkontoer på staging (web + iPhone + Binding) | Kjetil (merge/tag), Deploy (utsetting), Claude (forespørsel og T-ROT) | T-ROT, test.gui.load-time | TESTRESULT.md#rot |

## Avhengigheter og risiko

- **Modell:** WP6 testes med falsk modell. Ekte modellhjelp på staging venter på beslutningen i modelltilgang-tråden; rommet virker uten.
- **Python/Go:** ikke portert i denne runden (FORMAALSSPEC §2).
- **PDF/DOCX:** utenfor runden.
- **Lærdommer som styrer planen:** syntax-check-reported-as-delivered (ingenting meldes levert før Mac-bygget er grønt), valuetype-equality-false-for-objects (sammenlign sortert JSON), branch-is-empty (push etter første grønne bygg), local-main-is-not-main (mål mot origin/main), pin-must-be-on-their-main (CellScaffold pinner først når CellProtocol-PR-en er på main og tagget).

## Leveranserekkefølge

WP0 → WP1+WP4 (parallelt) → WP2+WP3 → WP5 → WP6+WP7 → WP8 → WP9 → (Kjetil merger/tagger CellProtocol) → WP10.

## Ber om

G2: godkjenn planen, eller si «auto» for at jeg kjører den uten flere porter før G3.
