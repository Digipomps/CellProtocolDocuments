# Skeleton Support For Graphs, Charts, And Network Visualizations

Dato: 2026-05-05
Status: analyse, ikke implementert

## Kort svar

Ja, dette kan støttes i skeleton, men ikke bare ved å legge til litt konferanse-JSON.
Det krever delt kontraktsarbeid i `CellProtocol`, rendererarbeid i både
`Binding` og `CellScaffold`, editor/parity-oppdateringer, og nye tester.

Det viktigste funnet er:

- dagens skeleton har ingen `Chart`, `Table`, `GraphCanvas` eller
  `NetworkGraph`-primitive i den delte modellen
- Apple-rendereren og web-rendereren er eksplisitte switch-baserte implementasjoner
- web-editoren og Binding-editoren har egne støttelister som også må utvides
- det finnes allerede et godt mønster for portable visualiseringer i
  `MermaidRendererCell`
- det finnes allerede en strukturert grafkontrakt i
  `CellAccessGraphContracts.swift`

Anbefalingen er derfor:

1. Ikke legg til tre separate primitives først (`Chart`, `Table`, `GraphCanvas`).
2. Legg heller til ett generisk visualiseringselement i skeleton.
3. La det elementet bruke portable spesifikasjoner og SVG/fallback som felles kontrakt.
4. La Apple ha native adaptere som optimalisering, ikke som eneste sannhet.

Dette siste punktet er en inferens fra repoet: det er ikke eksplisitt implementert i dag,
men det følger samme retning som eksisterende `MermaidRendererCell` og unngår at
`Binding` og `CellScaffold` driver fra hverandre.

## Bekreftet nåtilstand

### 1. Shared schema mangler visualiseringsprimitive

`CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift` definerer dagens
`SkeletonElement`-cases, og listen stopper ved `List`, `Object`, `Image`, `Text`,
`AttachmentField`, `FileUpload`, `TextField`, `TextArea`, `HStack`, `VStack`,
`Reference`, `Button`, `Divider`, `ScrollView`, `Section`, `Tabs`, `ZStack`,
`Grid`, `Toggle` og `Picker`.

Relevante steder:

- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:15`
- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1769`
- `../CellProtocol/Tests/CellBaseTests/SkeletonTests.swift:7`

Konsekvens:

- "charts" og "rich network visualization" er ikke skjult støtte som bare mangler docs
- det finnes heller ingen generisk `Canvas`- eller `HTML`-slot i shared skeleton

### 2. Apple-rendereren er hardkodet per elementtype

`Binding` renderer skeleton via `SkeletonView`, og den må eksplisitt kjenne hver case.

Relevante steder:

- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:645`
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:658`
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:693`
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:699`

Konsekvens:

- nytt element krever ny SwiftUI-renderer
- nytt element kan ikke "bare" decode og automatisk vises i Binding

### 3. Web-runtime er også hardkodet per elementtype

`CellScaffold/Public/js/skeleton-runtime.js` har både:

- en `SUPPORTED_TYPES`-liste
- en `renderElement(...)` switch
- egne binding-lister for ulike dynamiske elementtyper

Relevante steder:

- `../CellScaffold/Public/js/skeleton-runtime.js:7`
- `../CellScaffold/Public/js/skeleton-runtime.js:35`
- `../CellScaffold/Public/js/skeleton-runtime.js:109`
- `../CellScaffold/Public/js/skeleton-runtime.js:158`

Konsekvens:

- nytt element krever både decode-støtte og faktisk DOM-rendering
- hvis elementet har state, actions eller data-binding, må det inn i runtime-flush-logikken

### 4. Editorlagene må oppdateres separat

Binding-editoren har egen elementmeny og fabrikk:

- `../Binding/Binding/SkeletonEditor/SkeletonEditorPanels.swift:875`
- `../Binding/Binding/SkeletonEditor/SkeletonEditorPanels.swift:899`

Binding-tree/query-laget har egne navnelister og child-regler:

- `../Binding/Binding/SkeletonEditor/SkeletonTreeQueries.swift:49`
- `../Binding/Binding/SkeletonEditor/SkeletonTreeQueries.swift:79`
- `../Binding/Binding/SkeletonEditor/SkeletonTreeQueries.swift:117`

Web-editoren i `porthole-webo.js` har egne hardkodede supported-lister og child-regler:

- `../CellScaffold/Public/js/porthole-webo.js:4703`
- `../CellScaffold/Public/js/porthole-webo.js:5568`
- `../CellScaffold/Public/js/porthole-webo.js:5604`
- `../CellScaffold/Public/js/porthole-webo.js:5623`

Konsekvens:

- nytt element må inn i minst fire editorsteder:
  - add element / palette
  - decode
  - tree traversal
  - child insertion rules

Viktig observasjon:

- web-editorens hardkodede lister ligger fortsatt litt bak modellen
- `skeleton-runtime.js` kjenner `Tabs`, men editorens decode-lister rundt
  `porthole-webo.js:4707` og `porthole-webo.js:5609` gjør det ikke

Det er et tydelig signal om at parity må planlegges eksplisitt.

### 5. Porthole bootstrap/projection må kjenne nye keypaths

Hvis et nytt element leser fra `specKeypath`, `stateKeypath`, `selectionKeypath` eller lignende,
må Porthole vite at disse er lesbare avhengigheter.

Relevant sted:

- `../CellScaffold/Sources/App/Controllers/PortholeBootstrapProjection.swift:76`

Konsekvens:

- et nytt visualiseringselement må registrere hvilke keypaths som skal trekkes inn i preview/bootstrap
- uten dette får man "støttet renderer" men tom eller uoppdatert preview

### 6. Vi har allerede to gode byggeklosser

Det finnes allerede et portabelt renderer-mønster:

- `../CellScaffold/Sources/App/Cells/Mermaid/MermaidRendererCell.swift:7`
- `../CellScaffold/Sources/App/Cells/Mermaid/MermaidRendererCell.swift:171`
- `../CellScaffold/Sources/App/Cells/Mermaid/MermaidRenderSupport.swift:1`

Det finnes også allerede en strukturert grafkontrakt:

- `../CellProtocol/Sources/CellBase/Cells/CellResolver/CellAccessGraphContracts.swift:6`
- `../CellProtocol/Sources/CellBase/Cells/CellResolver/CellAccessGraphContracts.swift:26`
- `../CellProtocol/Sources/CellBase/Cells/CellResolver/CellAccessGraphContracts.swift:76`
- `../CellProtocol/Sources/CellBase/Cells/CellResolver/CellAccessGraphContracts.swift:189`

Og en grafcelle som allerede kan produsere Mermaid-fallback:

- `../CellScaffold/Sources/App/Cells/EntityGraph/EntityCellGraphCell.swift:147`
- `../CellScaffold/Sources/App/Cells/EntityGraph/EntityCellGraphCell.swift:168`
- `../CellScaffold/Sources/App/Cells/EntityGraph/EntityCellGraphCell.swift:287`

Konsekvens:

- vi starter ikke fra null
- "portable render spec + renderer adapter + fallback" er allerede et repo-mønster

### 7. `Reference` er ikke en generisk visualiseringsslot

Det er fristende å tro at en renderer-cell bare kan legges inn via `Reference`,
men dagens implementasjon er smalere enn det.

På Apple-siden går `Reference` inn i `CellReferenceView` fra `SkeletonView`:

- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:699`

På web-siden rendres `Reference` som en enkel wrapper med tittel og listebinding:

- `../CellScaffold/Public/js/skeleton-runtime.js:1006`

Konsekvens:

- `Reference` er ikke en generisk "render arbitrary HTML/SVG/native view here"-primitive
- eksisterende renderer-celler er derfor et sterkt mønster, men ikke alene nok til
  å gi rik chart-/graph-støtte inne i dagens skeleton-tre

## Hva som faktisk må bygges

## Anbefalt retning: ett generisk visualiseringselement

I stedet for tre nye elementtyper anbefales ett delt element, eksempelvis:

- `Visualization`
- eller `RenderSurface`
- eller `DataView`

Dette er en inferens fra dagens kodebase, ikke noe som allerede finnes.

Hvorfor ett generisk element er bedre enn tre separate:

- samme parity-arbeid trengs uansett i Binding og web
- tabeller, charts og nettverksgrafer trenger mye av samme kontrakt:
  - datakilde
  - render spec
  - fallback
  - state
  - actions
  - height/width/aspect
  - selection/hover/focus
- en felles primitive gjør senere `map`, `timeline`, `heatmap` og lignende billigere

Et realistisk minimum for en delt kontrakt er:

- `kind`: `chart`, `table`, `network`
- `specKeypath` eller `spec`
- `stateKeypath`
- `actionKeypath`
- `fallbackTextKeypath` eller `fallbackText`
- `preferredRenderer`: `svg`, `canvas`, `native`, `html`
- `modifiers`

I tillegg bør selve spec-kontraktene leve i `CellProtocol`, for eksempel:

- `ChartSpec`
- `TableSpec`
- `NetworkGraphSpec`

Og ikke som web-only JSON eller SwiftUI Charts-spesifikke modeller.

## Shared work i CellProtocol

Hvis dette skal være ekte skeleton-støtte, må `CellProtocol` utvides med:

1. ny `SkeletonElement` case og tilhørende `Codable` type(r)
2. decode/encode-støtte i `SkeletonDescription.swift`
3. tester i `SkeletonTests.swift`
4. portable value/state/action-kontrakter
5. dokumentasjon i skeleton-spec

Minimumsliste:

- oppdater `SkeletonModifiers` bare hvis visualiseringene trenger ny felles metadata
- legg til ny `SkeletonElement` case i
  `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1769`
- legg til round-trip tester i
  `../CellProtocol/Tests/CellBaseTests/SkeletonTests.swift`
- vurder egne kontraktstyper i `CellBase` på linje med
  `CellAccessGraphContracts.swift`

## Binding / Apple work

I `Binding` må minst dette på plass:

1. ny renderergren i `SkeletonView`
2. ny `SwiftUI` view/adapter
3. editorstøtte
4. parameter-inspectorstøtte
5. tester

Konkret:

- legg til ny `case` i render-switch i
  `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:645`
- legg til nytt view, eksempelvis `CellVisualizationView`
- hvis Apple skal bruke native `Charts`, må det være adapter over samme portable spec
- legg til elementtype i `SkeletonEditorPanels.swift:875`
- legg til parameterstøtte i `SkeletonElementParameterCatalog.swift`
- legg til tree/query-regler i `SkeletonTreeQueries.swift`
- legg til render- og kontraktstester i `../Binding/BindingTests/BindingTests.swift`

Viktig parity-gap allerede i dag:

- `styleRole` og `styleClasses` finnes i shared modell
  (`SkeletonDescription.swift:41`)
- web bruker dem som CSS-klasser
  (`skeleton-runtime.js:1271`)
- Apple bruker dem i praksis mest som accessibility metadata
  (`SkeletonView.swift:104`)
- Binding-modifier-editoren eksponerer heller ikke `styleRole` eller `styleClasses`
  i `SkeletonModifierCatalog.swift:11`

Det betyr at nye visualiseringer ikke bør lene seg tungt på stylingmetadata alene.

## CellScaffold / web work

I `CellScaffold` må minst dette på plass:

1. ny type i `SUPPORTED_TYPES`
2. ny render-funksjon i `skeleton-runtime.js`
3. binding/state-flush hvis visualiseringen er dynamisk
4. editorstøtte i `porthole-webo.js`
5. bootstrap keypath-projection
6. tester og preview-scenarier

Konkret:

- legg til typen i `skeleton-runtime.js:7`
- legg til render-switch i `skeleton-runtime.js:158`
- legg til DOM-implementasjon og oppdatering
- oppdater `PortholeBootstrapProjection.collectReadableKeypaths(...)`
  i `PortholeBootstrapProjection.swift:76`
- oppdater editor-decode og child-regler i
  `porthole-webo.js:4703`, `porthole-webo.js:5568`, `porthole-webo.js:5604`
- oppdater komponentinnsetting og inspectorfelt
- legg til tester i `PortholeWebEditorSupportTests`
- legg til runtime/parity-scenarioer

## Data contract per visualiseringstype

### Tables

Enkle read-only tabell-lignende flater kan allerede fakes med `Grid` + `Text`.
Det er nok for KPI-kort og små matriser, men ikke for en ekte tabell.

Ekte tabellstøtte trenger typisk:

- kolonnedefinisjoner
- header-rader
- formattering per kolonne
- alignment per kolonne
- sortering
- paging/virtualisering
- radvalg og radhandlinger

### Charts

Charts trenger minst:

- serie-definisjoner
- akser
- labels
- skala/ticks
- formattering
- selection/tooltip-kontrakt
- fallback når native renderer ikke finnes

Repoet peker allerede mot riktig form:

- render spec
- deterministisk caching
- SVG som felles bærbar output
- native Apple-adapter som bonus

### Network graphs

Dette er den mest lovende typen fordi data-kontrakten i stor grad finnes allerede:

- `CellAccessGraphSnapshot`
- `CellAccessGraphNode`
- `CellAccessGraphEdge`

Det som mangler er ikke først og fremst domain-data, men en skeleton-egnet
visualiseringskontrakt og renderer.

Det finnes allerede Mermaid-fallback via:

- `CellAccessGraphContract.mermaidKeypath`
- `EntityCellGraphCell.mermaidPayload(...)`

Men det er fortsatt ikke en ekte interaktiv nettverksvisning i skeleton.

## Faseforslag

## Fase 0: billigste mellomstasjon

Hvis målet er å vise noe raskt uten ny shared primitive:

- tabeller: bruk `Grid`
- enkle KPI-visualiseringer: bruk `Grid`, `Section`, `Text`
- graf/nettverk: bruk Mermaid-fallback eller rendret SVG/PNG som `Image`

Dette er billigst, men gir ikke ekte interaktivitet eller god authoring.

## Fase 1: anbefalt MVP

Implementer én generisk visualiseringsprimitive med:

- portable spec
- SVG som primær fallback
- web-renderer i `CellScaffold`
- SwiftUI-renderer i `Binding`
- optional native Apple adapter for chart-typer

Denne fasen bør eksplisitt støtte:

- `table`
- `chart`
- `network`

## Fase 2: native-forbedringer

Når fase 1 er stabil:

- la Apple bruke `SwiftUI Charts` der det gir mening
- la web bruke `canvas` eller mer avansert DOM/SVG-interaksjon
- behold samme shared spec

## Verifikasjon som bør være obligatorisk

Før dette kan kalles støttet i både `Binding` og `CellScaffold`, bør følgende være grønt:

1. `CellProtocol` encode/decode tester for ny primitive
2. `BindingTests` for rendering og eventuelle actions
3. `PortholeWebEditorSupportTests`
4. JS syntax/runtime checks for `skeleton-runtime.js` og `porthole-webo.js`
5. minst ett preview-scenario i `CellScaffold` via `npm run skeleton:iterate`
6. Binding parity-kjøring via `../Binding/Scripts/run_skeleton_parity_suite.sh`

Relevante eksisterende testankre:

- `../CellProtocol/Tests/CellBaseTests/SkeletonTests.swift`
- `../Binding/BindingTests/BindingTests.swift`
- `../CellScaffold/Tests/AppTests/PortholeWebEditorSupportTests.swift`
- `../Binding/Scripts/run_skeleton_parity_suite.sh`

## Anbefaling til neste implementasjonstråd

Den neste tråden bør ikke starte med å bygge konferansespesifikke charts direkte.
Den bør starte med ett av disse to valgene:

1. `Visualization`-primitive i `CellProtocol`
2. eller en mer begrenset `ChartSurface`-primitive hvis du vil teste kontrakten på ett område først

Hvis målet er både charts, tabeller og rik nettverksvisning, er valg 1 det klart
mest robuste.

## Hva jeg ville gjort

Hvis jeg skulle tatt dette videre i kode, ville jeg valgt:

1. Definer en generisk visualiseringsprimitive i `CellProtocol`.
2. Bruk `MermaidRendererCell` som mønster for portable render requests/responses.
3. Bruk `CellAccessGraphSnapshot` som første ekte datakilde for `network`.
4. La `chart` bruke SVG-fallback først, ikke Apple-only `Charts`.
5. Legg parity- og editorstøtte inn som del av samme arbeidsordre, ikke som opprydding etterpå.

Det er den minste veien til "støttet i skeleton, Binding og CellScaffold" uten å
låse oss til én plattform eller tre separate primitives.
