# PLAN — Mine lister: celle og listekomponent (P2, venter på G2)

Grunnlag: FORMAALSSPEC.md iterasjon 2 — **G1 og G1-GUI godkjent av Kjetil 2026-10-02** (valg «G1 og G1-GUI godkjent» i chatten). §6-valg: piler + dra, cellen i CellProtocol som `cell:///Lists`, bare CellProtocol i denne omgangen, idéer er vanlig liste.

## Dette skal du gjøre (Kjetil)

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si **«G2 godkjent»**, og svar på **ett spørsmål** (under). | Ingen kode skrives før G2. |
| Under WP0–WP6 | Ingenting. Jeg legger jobber i `_losen-queue` (skript-modus, uten Codex-kvote) og skriver fremdrift i STATUS.md. Du får en melding når bygget er grønt første gang, og når PR-en er åpnet. | Du skal ikke lime inn kommandoer. |
| Når PR-en er åpnet | **Merge PR-en** mot `CellProtocol/main` (eller si at Codex skal gjøre det). | Losen kan ikke merge (sikkerhetsklassifisereren stopper det, jf. `_losen-queue/KOORDINERING.md`). |
| Ved G3 | Les `ACCEPT.md` (forventet → faktisk, rad for rad) og si **«G3 godkjent»** eller hva som er feil. | Bare ditt ord setter porten. |

**Spørsmålet (endrer WP2):** Tekstfelt kan ikke bære liste-ID inne i en komponentmontering (FORMAALSSPEC §0 B2/B8). Knapper kan (payload fra raden), så kryss av / flytt / fjern / slett liste er eksakte overalt. For «Legg til …» og nytt listenavn *i en montering* finnes bare én kanal: monteringsmetadataen (`mount.instanceID`) som Porthole web i dag legger i et TaskLocal i **ScaffoldKit** (`CellScaffold::Sources/ScaffoldKit/ComponentActionContext.swift`), som en celle i CellProtocol ikke kan lese.
- **A (anbefalt):** definer `ComponentActionContext` (samme struct + `@TaskLocal`) i **CellBase** nå, la `ListsCell` lese den, og la CellScaffold bytte til CellBase-typen i integrasjonspakken (én `typealias`). Dette er den «portable CellProtocol-endringen» som SKJELETT_ELEMENTER §2.3 allerede varslet. Ingen renderer- eller formatendring. Inntil integrasjonen går tekst i en montering til aktiv liste — men ingen bruker ser monteringer på web før integrasjonspakken uansett (pin + katalog).
- **B:** ikke rør CellBase; tekst i en montering går alltid til aktiv liste, dokumentert som kjent begrensning i kontrakten.

## Arbeidspakker (1:1 mot bladformål, i avhengighetsrekkefølge)

Utfører: **Losen (sky)** skriver filer rett inn i arbeidstreet på Macen; **kø (Mac, skript)** = jobb i `_losen-queue` i `skript`-modus som bygger/tester som Kjetils bruker, uten Codex; **Kjetil** = bare det som står i tabellen over.

| WP | Bladformål (purposeRef) | Hva det innebærer | Utfører | Gjør grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | `quality.build-and-regression` (baseline) | Arbeidstre `HAVEN/_worktrees/cellprotocol-lister` på gren `pdd/lister-celle` fra `origin/main` (låst mot prune, laget **på Macen**), diskvakt, `swift build` + `swift test` på uendret kode → tall vi måler mot. | kø (Mac, skript) `wp0-lister-worktree-baseline.sh` | test.build, test.regression (baseline) | TESTRESULT.md#baseline |
| WP1 | `order.toggle`, `order.done-bottom`, `order.manual`, `order.clear-done` | `ListsContracts.swift`: `ListRecord`, `ItemRecord`, `ListsState` (ren verdi-logikk, ingen celle): normalisering «åpne(manuell) + utførte(doneAt)», toggle, move (piler **og** slipp-payload), clearDone, payload-bygging for rader (togglePayload …). Tester inkl. property-test (200 sekvenser). | Losen → kø | test.lists.order.* | rad 11 (del) |
| WP2 | `cell`, `cell.lists-crud`, `cell.items-crud`, `cell.authorization-honours-keypath`, `not.leak-other-users` | `ListsCell.swift` (GeneralCell): grant `lists` rw-- for eier; nøkler `lists.state` (get, rot-intercept med nestet oppslag), `lists.list.create/select/rename/remove/clearDone`, `lists.item.add/update/toggle/move/remove`; strukturerte feil; `persistCellSnapshot` etter hver vellykket endring (VaultCell-mønster); `ComponentActionContext` (A) eller aktiv-liste-regel (B). Tester: crud, persist-rundtur, auth-negativ, ukjent keypath. | Losen → kø | test.lists.cell.crud, test.lists.cell.persist, test.cell.auth-negative | rad 11 |
| WP3 | `component.single-source`, `component.plain-surface`, `gui.ways-in-are-reachable`, `gui.capability-not-client`, `not.silent-section` | `ListsConfiguration.swift`: `checklistSkeleton(keypathPrefix:)`, `mineListerConfiguration()`, `componentMount(for:)`; `lists.state.lists[n].mount` og `mountsById`. Tester: (a) fabrikken gir **byte-lik** JSON som `skeleton/mine-lister.cellconfiguration.json` (bildet du godkjente); (b) prefiks-normalisert likhet flate/montering; (c) `SkeletonReachabilityAudit` 0 funn + de ni handlingene nåbare, med `SkeletonLayoutContext` både med og uten `drag`. | Losen → kø | test.lists.component.same-skeleton, test.lists.factory-matches-approved-skeleton, test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable, test.lists.gui.variants (native del) | rad 11, ACCEPT#ways-in |
| WP4 | `cell.contract-explicit`, `cell.no-empty-stubs`, `cells.dataflow-declared`, `quality.docs-in-same-change` | `contract/lists_cell_contract_v0.json` + fixtures + `validate_contract.py` (stdlib) kjørt grønt; kopi til `Book/lists_cell_contract_v0.json`; `CellProtocol::Docs/ListsCell.md` («Last verified against code»); `dataflow.md` (ferdig utkast nå, kontrolleres mot kontrakten). | Losen (sky) + kø for validatoren | test.cell.contract-fixtures, test.cell.stub-scan, test.cells.dataflow-matches-contracts, test.docs-updated | rad 12, 15 |
| WP5 | `component.mount` | Eksporter cellens **ekte** `lists.state` fra en test til `skeleton/state-fra-cellen.json`; kjør `images/render.js` mot den i skyen: tre monteringer `ok`, handling i montering bærer `mount.instanceID`; variant-test (0 piler med `drag`, 8 uten; 390 px stabler). | Losen (sky) | test.lists.component.web-mount, test.lists.gui.variants (web del), test.lists.web-render-of-reference | TESTRESULT.md#component, #variants |
| WP6 | `quality.build-and-regression`, `not.renderer-change` | Hele CellProtocol-testmengden grønn (siste «Executed»-linje), `git diff --stat` mot Skeleton/Porthole tom, commit etter **første** grønne bygg og etter hver pakke (ikke til slutt), push + PR mot `main` (`workspace-write-net`-jobb eller skript med `gh`), `git rev-parse` + `ls-remote` limt inn i STATUS. | kø (Mac) | test.build, test.regression, test.lists.no-format-change | rad 11 (PR-lenke) |
| WP6b (valgfri) | — | Uavhengig gjennomlesing av PR-diffen av Astra (Codex, `read-only`-jobb, rå utdata til fil) mot FORMAALSSPEC §1 — hvis kvoten tillater. | kø (Codex) | — | STATUS |
| WP7 | `gui.parity-with-approved-image` (web-del), `quality.work-is-visible` | `TESTRESULT.md` (alle §5-rader, rå utdata eller `blocked` + grunn), `ACCEPT.md` (§3 rad for rad; bilder side om side: godkjent referanse ↔ web-harness med cellens ekte state), STATUS, lærdommer i registeret (P6), `haven_learn.py capture`. | Losen | test.status-current | rad 13, ACCEPT.md |

**Ikke i denne planen (Kjetils valg, §6 spm. 3):** menyoppføring i HAVEN-appen (Binding) og CellScaffold-katalogen, pin-oppdatering i CellScaffold, ScaffoldKit-adopsjon av `ComponentActionContext`, native skjermbilde (§3 rad 14). Det blir integrasjonspakken `PDD_lister-integrasjon` når PR-en er inne.

## Rekkefølge og hva som stopper hva

```
WP0 baseline ──► WP1 logikk ──► WP2 celle ──► WP3 fabrikk ──► WP5 web-montering ──► WP6 regresjon+PR ──► WP7 aksept
                                   │              │
                                   └──► WP4 kontrakt/docs (parallelt fra WP2) ──────────┘
```

Grafisk: `images/plan-v1.png`.

- Et rødt WP0 stopper ikke arbeidet, men registreres som eget avvik med årsak (lesson.a-red-baseline-is-a-question-not-an-answer): tre spørsmål før jeg gjør noe med det.
- Hver pakke avsluttes med commit på grenen når byggejobben er grønn (lesson.branch-is-empty-after-eight-work-packages). STATUS får `git rev-parse --short HEAD` etter hver.
- En ny rød test etter mine endringer → basen kjøres tre ganger i rent tre før jeg tar på meg feilen (lesson.a-new-red-test-needs-a-repeated-baseline).

## Byggemiljø og kjøreregler (kø)

- Alle Swift-kjøringer: `skript`-jobb i `_losen-queue/inbox/` (bane a), skript under `HAVEN-Deploy/_handoff/LISTER/`, `ulimit -f unlimited` før bygget, logg til fil, `tail` i leveransen, exitkode lest, produkt sjekket. Diskvakt: minst 40 GiB ledig **og** 5 % etter 10 GiB reserve (KOORDINERING regel 1); blokkerer den, rydder jeg (`RYDD/`) i stedet for å omgå.
- Bygg via `CellProtocol/Scripts/haven-swiftpm.sh -- build|test` (delt, avgrenset SwiftPM-cache), i arbeidstreet `_worktrees/cellprotocol-lister` låst mot prune.
- Promptfil skrives før `.job`; `.job` via `mv` fra `.tmp`. Kontroll på Macen (md5) etter hver skriving fra skyen, nytt filnavn per utgave.
- Ingen `git` gjennom VM-montasjen; all git kjører i jobben på Macen.
- Tidsestimat: WP0 ≈ 20–40 min (full CellProtocol-test), WP1–WP3 én byggejobb hver (≈ 10–25 min), WP6 ≈ 40 min. Total: en arbeidsdag i køen hvis bygget er friskt.

## Dataflyt (kort; full tabell i dataflow.md)

Porthole («Mine lister») ──`my.*`──► `cell:///Lists` : `lists.state` (get), `lists.list.*`, `lists.item.*` (set)
Vert med `ComponentSurface` ──`sourceKeypath: mount`──► rendereren monterer; handlinger ──`lists.*` + `mount{instanceID}`──► `cell:///Lists`
`cell:///Lists` ──`persistCellSnapshot`──► resolverens persistens (eierens entitet)

## Kjente avvik som vil stå i ACCEPT.md uansett

- Web viser knapper i rader som fylte knapper (vertstemaet overstyrer `controlStyle: plain`, FORMAALSSPEC §0 B10); appen viser ikoner. Godkjennes eller rettes av deg i integrasjonspakken.
- Appen viser pilene «flytt opp/ned»; web skjuler dem (B6) — tilsiktet.
- Native rendering er ikke målt i denne pakken (§6 spm. 3); reachability-testen med begge kapabilitetssett er appens bevis her.
