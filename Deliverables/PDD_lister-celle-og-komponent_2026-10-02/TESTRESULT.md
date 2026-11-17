# TESTRESULT — Mine lister: celle og listekomponent

Rå utdata under ankrene §5 i FORMAALSSPEC.md navngir. Alt er kjørt på Macen via `_losen-queue` (skript-modus) i
arbeidstreet `_worktrees/cellprotocol-lister` (gren `pdd/lister-celle`), med mindre annet står. Full logg per kjøring i
`HAVEN-Deploy/_handoff/LISTER/logg/`.

## #baseline

WP0, jobb `l3-lister-wp0-baseline-20261008` (rapport `HAVEN-Deploy/_handoff/LISTER/wp0-baseline.md`, logg
`HAVEN-Deploy/_handoff/LISTER/logg/wp0-baseline-20261008T090214Z.log`), uendret kode = `origin/main` `afa8cbf98f1b49dd8adee93f61a178b360afcc40`:

```
- swift build: exit=0 (6 min 9 s)
- swift test: exit=0 (2 min 21 s)
- siste «Executed»-linje: 	 Executed 1545 tests, with 5 tests skipped and 0 failures (0 unexpected) in 74.929 (75.030) seconds
- **GRØNN baseline**
```

Veien dit (tre forsøk samme formiddag, alle i rapporten `wp0-baseline.md` og `done/l*.svar.md`):
- `l0` 09:00Z: BLOKKERT av diskvakten — 55 GiB ledig, 45 GiB etter 10 GiB reserve, krav 46 GiB (5 % av 927 GiB).
- `l1` 09:01Z: `RYDD/wp-rydd-tmp-bygg.sh` → 68 GiB ledig.
- `l2` 09:02Z: arbeidstreet laget riktig; bygget stoppet i `haven-swiftpm.sh` exit 64: «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…». Rettet ved eget cache-key (`HAVEN_SWIFTPM_CACHE_KEY=lister-celle`), ikke ved å røre den delte cachen.

## #build

WP1–WP3, jobb `l4-lister-bygg-wp1-3-20261008` (rapport `HAVEN-Deploy/_handoff/LISTER/bygg-wp1-3.md`, logg `logg/bygg-20261008T091510Z.log`):

```
- swift build --build-tests: exit=0 (0 min 57 s)
- swift test: exit=0 (0 min 16 s)
- siste «Executed»-linje: 	 Executed 26 tests, with 0 failures (0 unexpected) in 0.157 (0.159) seconds
Test Suite 'ListsCellTests' passed … Executed 8 tests, with 0 failures
Test Suite 'ListsConfigurationTests' passed … Executed 8 tests, with 0 failures
Test Suite 'ListsStoreTests' passed … Executed 10 tests, with 0 failures
- **GRØNN**
```

Første forsøk: kompilerte uten feil, alle 26 grønne. `l5`/`l7`/`l9` (27 tester, eksporttesten lagt til): alle GRØNNE
(`bygg-wp5.md`, `bygg-wp5b.md`, `bygg-wp5c.md`). Commit `4ecd1d5651808b13e7308b0c24e9813668be1883` på `pdd/lister-celle` (`l6`, `commit-wp1-5.md`), 10 filer, +2272.

## #cell

`ListsCellTests` (8 → 9 tester), grønne i `l4`/`l5`/`l7`/`l9`:
`testCreateSelectRenameAddToggleRemoveThroughKeypaths` (create string/objekt → aktiv; rendererens valgpayload `{selected}`;
tekst uten id → aktiv liste; toggle → `done: true`; rename via string; `lists.state` med `counts {2 lister, 2 åpne, 1 utført}`,
`activeAsRows[0].items` åpent først/utført sist; remove item; clearDone `true` → `removed: 0`; remove list → aktiv faller tilbake),
`testNestedKeypathsResolveThroughRootIntercept` (`lists.state.lists`, `lists.state.mountsById.<id>` dekoder som
`SkeletonComponentMount` med `item.id == id`), `testStructuredErrorsForBadInput` (`no_target_list`, `invalid_title`,
`list_not_found`, `invalid_payload`, `item_done_cannot_move`), `testDropPayloadFromWebRendererMovesItem` (webens slipp-payload
→ `[i0, i2, i1, i3]`), `testMountedComponentContextTargetsTheMountedListNotTheActiveOne`, `testPrintsRealStateForTheWebHarness`.

## #persist

`ListsCellTests.testEncodeDecodeRoundTripKeepsStateByteForByte` (grønn): `JSONEncoder().encode(cell)` → `decode(ListsCell.self)` →
`ensureRuntimeReady()`; `storeSnapshot` lik, `persistancy == .persistant`, `lists.state` kanonisk JSON byte-lik før/etter.
`ListsStoreTests.testStoreCodableRoundTrip` (grønn). `persistCellSnapshot` mot resolverens lagring er ikke kjørt her (ingen
resolver i enhetstestene; `notice`-raden er veien feilen vises på) — se ACCEPT.md.

## #auth

`ListsCellTests.testOtherIdentityIsDeniedOnReadAndWrite` (grønn): annen identitet (`someone-else` i `MockIdentityVault`) får
`denied`/`CellAuthorizationError` på `get lists.state` og `set lists.item.add`; ingenting skrevet (`activeList.items.count == 0`).
`testUnknownKeypathIsNotFoundForOwner` (grønn): `get lists.nope` og `set lists.nope` kaster for eieren.

## #order

`ListsStoreTests` (10 tester, grønne): `testToggleMovesItemToBottomAndBackToEndOfOpenZone` (avkrysset → sist; samme millisekund
beholder avkryssingsrekkefølgen via `max(now, latest+1)`; angret → sist blant åpne, `doneAt` fjernes),
`testAddPutsNewItemLastAmongOpenItemsEvenWhenDoneItemsExist`, `testStepMovesStayInsideOpenZoneAndEdgesAreNoOps` (kant = no-op som
lykkes; utført → `item_done_cannot_move`), `testDropPlacesDraggedItemBeforeTarget` (ned/opp/seg selv/på utført),
`testClearDoneRemovesOnlyDoneItems`, **`testInvariantHoldsForRandomOperationSequences`**: 200 sekvenser × 30 tilfeldige
operasjoner (seed `0x4C495354`), etter hver: `isNormalized`, `doneAt` stigende, åpne uten `doneAt`.

## #component

**Native (CellProtocol):** `ListsConfigurationTests` (8, grønne): `testFactoryProducesTheApprovedSkeletonByteForByte` — fabrikkens
«Mine lister»-skjelett er kanonisk byte-lik `Fixtures/ListsMineListerApproved.json` (= `skeleton/mine-lister.cellconfiguration.json`,
JSON-en de godkjente bildene ble rendret fra); `testSurfaceAndMountChecklistsDifferOnlyInKeypathPrefix`;
`testMountDecodesAsComponentMountWithTheListAsItem` (også via `ValueType`-veien rendereren bruker);
`testConfigurationMetadataMatchesTheApprovedFile`; `testCheckmarkIconsExistInBothRenderersAndUncheckedIsAGlyph`.

**Web (test.lists.component.web-mount), kjørt i skyen 2026-10-08 med CellScaffold `origin/main` `fdcfe7a5` sin
`skeleton-runtime.js`/`porthole-webo.css` (md5 i images/README.md) mot cellens EKTE `lists.state`
(`skeleton/state-fra-cellen.json`, skrevet av `testPrintsRealStateForTheWebHarness` i jobb `l9`):**

```
ok mine-lister-web-fra-cellen {"unsupported":[],"componentErrors":[],"unmappedIcons":[],"arrowsVisible":0,"titles":["Handleliste"]}
ok mine-lister-app-fra-cellen {"unsupported":[],"componentErrors":[],"unmappedIcons":[],"arrowsVisible":8,"titles":["Handleliste"]}
ok vert-komponenter-web-fra-cellen {"unsupported":[],"componentErrors":["ok","ok","ok"],"unmappedIcons":[],"arrowsVisible":0,"titles":["Handleliste","Huskeliste","Idéer"]}
mountBehaviour: mounts=3, secondInstance=6C01DACF-9CD6-486F-A485-CD34D62BAAB1
  lists.item.toggle  payload {listId: <Huskeliste>, itemId: …}  mount.instanceID == <Huskeliste>  sourceCellEndpoint cell:///Lists
  lists.item.add     payload "Kjøpe gave"                       mount.instanceID == <Huskeliste>  sourceCellEndpoint cell:///Lists
```

Trykk i den ANDRE monteringen (Huskeliste) ga handlinger med `mount.instanceID == Huskelistens id` — nøyaktig det
`ListsCell.targetListID` bruker (valg A). Full rapport: `images/render-report-wp5.json`.

**Pikselparitet referanse ↔ ekte state** (PIL `ImageChops.difference`, samme viewport, 2× skala):
`mine-lister-web-fylt-v1.png` ↔ `mine-lister-web-fra-cellen-v1.png`: **0/3 870 400 piksler ulike**;
`vert-komponenter-web-fylt-v1.png` ↔ `vert-komponenter-web-fra-cellen-v1.png`: **0/5 026 800**;
`mine-lister-app-fylt-v2.png` ↔ `mine-lister-app-fra-cellen-v1.png`: **0/1 316 640**. (`app-*-v1` var rendret med webens
kapabiliteter og skjulte pilene; `-v2` er rendret uten `drag` og viser dem — 0,913 % avvik mot v1, alt i pilkolonnen.)

## #variants

Web-harness (`images/render-report-wp5.json` → `variants`), samme skjelett og state, bare kapabilitetene byttes:

```
drag          {"arrowButtonsTotal":12,"arrowsLayoutHidden":12,"arrowsVisibleOpenRows":0,"columnsFlexDirection":"row"}
noDrag        {"arrowButtonsTotal":12,"arrowsLayoutHidden":0, "arrowsVisibleOpenRows":8,"columnsFlexDirection":"row"}
narrowNoDrag  {"arrowButtonsTotal":12,"arrowsLayoutHidden":0, "arrowsVisibleOpenRows":8,"columnsFlexDirection":"column"}
```

Native: `ListsConfigurationTests.testArrowsHideWhereTheHostHasDragAndColumnsStackWhenNarrow` (grønn) —
`layoutVariant(in: web)` gir `hidden == true` for pilene og `nil` for søppelkassen; `in: app` gir `nil` for pilene;
kolonnene får `axis == .vertical` ved 358 px og venstre kolonne `width == 300` ved 1148 px.

## #reachability

`ListsConfigurationTests.testEverySurfaceActionIsReachableAndNothingIsSilent` (grønn): `SkeletonReachabilityAudit.audit(«Mine lister»,
requiredActionKeypaths: de ni handlingene)` → 0 funn; `reachableActionKeypaths ⊇ {my.lists.list.create, list.select, list.rename,
list.remove, list.clearDone, item.add, item.toggle, item.move, item.remove}`.
`testMountedChecklistActionsAreReachableInsideARow` (grønn): monteringens skjelett i radkontekst, 7 handlinger nåbare, 0 funn.

## #contract

`contract/validate_contract.py` (stdlib), kjørt i skyen 2026-10-02 og på Macen 2026-10-02 (`purpose_dev.py gates` samme dag):

```
kontrakt v0: 10 set, 1 get, 11 positive, 7 negative fixtures
GRØNN
```

## #regression

WP6, jobb `m1-lister-regresjon-full-20261008` (`HAVEN-Deploy/_handoff/LISTER/regresjon-wp6.md`, logg `logg/bygg-20261008T093212Z-full.log`),
hele CellProtocol-testmengden på `pdd/lister-celle` (`4ecd1d5` + eksport-til-fil-endringen, committet som `29dbfa8` rett etter):

```
- swift build --build-tests: exit=0 (0 min 11 s)
- swift test (full): exit=0 (1 min 36 s)
- siste «Executed»-linje: 	 Executed 1572 tests, with 5 tests skipped and 0 failures (0 unexpected) in 86.389 (86.442) seconds
- **GRØNN**
```

Baseline (uendret kode) var 1545 tester; 1545 + 27 nye = 1572. Ingen test fjernet eller svekket. CI på PR #64 (GitHub Actions)
leses av `wp-lister-pr-status.sh` når den har kjørt.

## #format

`m3-lister-push-sjekk-20261008` (`push-sjekk.md`): `git diff --stat origin/main..HEAD -- Sources/CellBase/Skeleton/SkeletonDescription.swift
Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift Sources/CellApple/Cells/Porthole` → **tom**. Grenen legger til én ny fil under
`Sources/CellBase/Skeleton/` (`SkeletonComponentActionContext.swift`, Kjetils valg A) og ellers bare `Cells/Lists/`, tester, fixture og `Docs/`.

## #load-time

**blocked** — flaten «Mine lister» er ikke i noen meny i Binding/CellScaffold ennå (§6 spm. 3: integrasjonspakken). Måles der, tre ganger, ≤ 5 s.
