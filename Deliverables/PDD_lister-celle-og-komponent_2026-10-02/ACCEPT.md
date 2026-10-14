# ACCEPT — Mine lister: celle og listekomponent (P5, venter på G3)

FORMAALSSPEC §3 rad for rad: forventet → faktisk, med evidens. Bilder side om side der det er GUI.
G3 er Kjetils ord. Rad 14 (kjørende flate i Porthole/app) ble flyttet til integrasjonspakken ved §6 spm. 3 (Kjetil 2026-10-02).

**PR:** https://github.com/Digipomps/CellProtocol/pull/64 — gren `pdd/lister-celle` @ `29dbfa8f781ec58015826653ad32707658fca0ec`
(2 commits foran `origin/main` `afa8cbf`), pushet 2026-10-08 09:36Z (`origin/pdd/lister-celle == lokal HEAD`, `push-pr.md`).
**CI:** grønn 10:02Z — 5/5 sjekker pass, `mergeStateStatus: CLEAN` (`HAVEN-Deploy/_handoff/LISTER/pr-status-4.md`).

## Forventningskontrakten (§3)

| # | Leveranse | Forventet | Faktisk | Evidens | Status |
|---|---|---|---|---|---|
| 1 | «Mine lister», web, fylt | `images/mine-lister-web-fylt-v1.png` (godkjent G1-GUI) | Samme skjelett rendret fra **cellens ekte** `lists.state`: `images/mine-lister-web-fra-cellen-v1.png` — **0 av 3 870 400 piksler ulike** | TESTRESULT#component, `images/render-report-wp5.json` | oppfylt |
| 2 | web, tom | `mine-lister-web-tom-v1.png` | Tilstanden «ingen lister» gir `emptyHint` med én rad og `activeAsRows: []` (`ListsStoreTests.testListViewAndStateShapes`: `emptyHint.count == 1`, `activeListId == null`); bildet er uendret siden G1-GUI | TESTRESULT#order | oppfylt (ikke rendret på nytt fra celle — formen er testet) |
| 3 | web, ny liste | `mine-lister-web-ny-liste-v1.png` | Tom liste gir `emptyRows` med én rad og `summaryText: "tom"` (`testListViewAndStateShapes`) | TESTRESULT#order | oppfylt (som rad 2) |
| 4 | web, feil | `mine-lister-web-feil-v1.png` | `notice` får én rad når `persistCellSnapshot` returnerer `false` (`ListsCell.persistAfterMutation`, `ListsCell.unverifiedNotice`); formen testet (`emptyState["notice"].count == 1`). **Ikke utløst mot ekte lagring** i denne pakken (ingen resolver i enhetstestene) | TESTRESULT#persist | oppfylt i form; selve lagringsfeilen er ikke fremprovosert |
| 5 | app-bredde, fylt | `mine-lister-app-fylt-v1.png` | **Avvik, tilsiktet:** v1 ble rendret med webens kapabiliteter og skjulte pilene. `mine-lister-app-fylt-v2.png` er rendret uten `drag` (som Binding) og viser pilene; fra ekte state: `mine-lister-app-fra-cellen-v1.png` — **0 piksler ulike mot v2**. Forskjellen v1↔v2 er 0,913 % av pikslene, alle i pilkolonnen | `images/README.md` (WP5) | **ber om ditt ord på v2** |
| 6 | app-bredde, tom | `mine-lister-app-tom-v1.png` | `-v2` rendret uten `drag`; identisk med v1 (ingen piler i tom tilstand) | `images/` | oppfylt |
| 7 | vert med tre monteringer, web | `vert-komponenter-web-fylt-v1.png` | Fra ekte state: `vert-komponenter-web-fra-cellen-v1.png` — **0 av 5 026 800 piksler ulike**; `componentErrors: [ok, ok, ok]`; trykk i montering 2 (Huskeliste) sender `lists.item.toggle` og `lists.item.add` til `cell:///Lists` med `mount.instanceID == Huskelistens id` | TESTRESULT#component | oppfylt |
| 8 | samme vert, app-bredde | `vert-komponenter-app-fylt-v1.png` | `-v2` rendret uten `drag` (pilene synlige i monteringene) | `images/` | oppfylt (samme forbehold som rad 5) |
| 9 | skjelett-JSON og eksempeldata | `skeleton/*.json` | Uendret; i tillegg `skeleton/state-fra-cellen.json` = cellens ekte tilstand (49 341 byte) | `skeleton/` | oppfylt |
| 10 | oppførsel på web (5 handlinger) | `images/render-report.json` | Bekreftet på nytt mot ekte state, pluss handlinger inne i montering (`render-report-wp5.json`) | TESTRESULT#component | oppfylt |
| 11 | `ListsCell` + kontrakter + fabrikk på gren, PR mot main | kode på `pdd/lister-celle`, PR | `Sources/CellBase/Cells/Lists/{ListsModel,ListsPayloads,ListsConfiguration,ListsCell}.swift`, `Sources/CellBase/Skeleton/SkeletonComponentActionContext.swift`, tester, fixture, `Docs/ListsCell.md`; commits `4ecd1d5`, `29dbfa8`; **PR #64** | `push-pr.md`, `commit-wp1-5.md`, `commit-wp5.md` | oppfylt |
| 12 | kontrakt-JSON + fixtures | `contract/`, `Book/lists_cell_contract_v0.json` | `contract/lists_cell_contract_v0.json` + 18 fixtures, validator GRØNN; **kopien i `Book/` legges inn i CellProtocolDocuments i denne pakken** (ikke i PR #64, som bare rører CellProtocol) | TESTRESULT#contract | oppfylt |
| 13 | testutdata for alle §5-rader | TESTRESULT.md | Alle ankre fylt med rå utdata; `#load-time` er `blocked` til integrasjonspakken (flaten er ikke i noen meny) | TESTRESULT.md | oppfylt (1 blocked med grunn) |
| 14 | kjørende flate web + app side om side | — | Flyttet til integrasjonspakken (§6 spm. 3). Webens renderer er kjørt på ekte state (rad 1, 7); native er bevist strukturelt (reachability med begge kapabilitetssett), ikke visuelt | STATUS.md | utsatt, avtalt |
| 15 | dataflow.md | kanter ↔ kontrakt | 14 kanter, alle i kontrakten (`test.cells.dataflow-matches-contracts`: gjennomgått manuelt 2026-10-08, kant 1–13 ↔ `get`/`set`-tabellen, kant 14 ↔ `targetListRule`) | `dataflow.md` | oppfylt |

## Innganger (test.skeleton.purpose-actions-reachable) {#ways-in}

`reachableActionKeypaths(«Mine lister») ⊇ {my.lists.list.create, my.lists.list.select, my.lists.list.rename, my.lists.list.remove,
my.lists.list.clearDone, my.lists.item.add, my.lists.item.toggle, my.lists.item.move, my.lists.item.remove}` — grønn
(`ListsConfigurationTests.testEverySurfaceActionIsReachableAndNothingIsSilent`). Auditen gir 0 funn på flaten og 0 på
monteringens skjelett i radkontekst.

## Paritet {#parity}

| Flate | Referanse (godkjent G1-GUI) | Faktisk (ekte `lists.state`, samme renderer) | Diff |
|---|---|---|---|
| «Mine lister» web 1180 | `images/mine-lister-web-fylt-v1.png` | `images/mine-lister-web-fra-cellen-v1.png` | 0 px |
| «Mine lister» app 390 | `images/mine-lister-app-fylt-v2.png` (v1 uten piler) | `images/mine-lister-app-fra-cellen-v1.png` | 0 px (v1: 0,913 %, pilene) |
| vert med monteringer web | `images/vert-komponenter-web-fylt-v1.png` | `images/vert-komponenter-web-fra-cellen-v1.png` | 0 px |

Oppførsel (lesson.parity-was-correctness-not-decoration): knappene treffer riktige keypaths med riktige payloads, feltene tar
input og sender string ved Enter, radvalg sender `{selected: id}`, dra-og-slipp sender `{dragPayload, dropTargetPayload}` —
alle fem målt i `render-report.json` og `render-report-wp5.json`, og cellen tar imot nøyaktig disse formene
(`ListsCellTests`, `contract/fixtures`).

**Native (Binding/SwiftUI) er ikke sett.** Det er avtalt (§6 spm. 3). Det som er bevist for appen: skjelettet dekoder, auditen
finner alle innganger, og layoutvariantene gir piler uten `drag` og stabling under 700 px (`testArrowsHideWhereTheHostHasDragAndColumnsStackWhenNarrow`).
Ventede avvik når det måles: fylte knapper på web mot ikoner i appen (FORMAALSSPEC §0 B10).

## Docs {#docs}

`Docs/ListsCell.md` («Last verified against code: 2026-10-08») i PR #64 beskriver nøkler, invariant, persistens, skjelettvalg
og grensene. Kontrakten (`contract/lists_cell_contract_v0.json`) kopieres til `Book/lists_cell_contract_v0.json` i
CellProtocolDocuments. Ingen Book-kapittel er endret kanonisk.

## Stubber {#stubs}

Søk i `Sources/CellBase/Cells/Lists/` etter `not-implemented`, `TODO`, `fatalError`, tomme handlere: ingen. Alle ti
set-nøkler og begge get-nøkler har full implementasjon med strukturert feil ved ugyldig input.

## Status {#status}

STATUS.md speiler mappen: G1/G1-GUI/G2 godkjent med dato og Kjetils ord, G3 venter, planbytter ført (ingen), loggen har hver jobb.

## Avvik og ting Kjetil skal ta stilling til ved G3

1. **App-bildene v2** (rad 5, 6, 8): referansen for appen bør være v2 (piler synlige uten `drag`). v1 viste webens variant.
2. **Antiformålet `not.renderer-change`** ble skrevet før valg A: `Sources/CellBase/Skeleton/SkeletonComponentActionContext.swift`
   er en **ny** fil under `Skeleton/` (TaskLocal monteringskontekst for celler), men ingen endring i `SkeletonDescription.swift`,
   `SkeletonReachabilityAudit.swift` eller rendererne (diff tom, `push-sjekk.md`). Jeg regner det som innenfor antiformålet;
   si fra hvis du vil ha det flyttet (f.eks. til `Cells/`).
3. **Lagringsfeilen (rad 4)** er bare testet i form. Første gang cellen kjører i et scaffold med lagring, vil `persistCellSnapshot`
   enten lykkes stille eller vise `notice`-raden — det er integrasjonspakkens sak å se den.
4. **Rad 14** utsatt som avtalt.
