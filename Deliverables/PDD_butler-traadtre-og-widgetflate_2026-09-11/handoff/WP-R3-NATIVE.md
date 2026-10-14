# WP-R3b — Native renderer (CellApple)
STATUS: DELVIS — commit c81a39799c3f664d77afa5f5de131ddac70f3c9c på pdd/skjelett-elementer — mangler: ComponentSurface (full kildehandlingsdekning og vertsadapter)

**Forbehold:** CellApple bygger og 132 tester passer, inkludert 21 nye native-tester.
**T-F3 native er ikke grønn.** Ingen Binding-app, virkelig tastatur-/VoiceOver-økt,
drag/drop-økt eller sammenlignbart native/web-skjermbilde er kjørt.
ComponentSurface har testet monterings-/datakontekst og kildehandlingsgrense, men
mangler full kildehandlingsdekning og integrasjon med kildecelle/Agreement.

Dato: 2026-09-19. Utfører: Astra (Codex).

## Port og arbeidsgrunnlag

Første kontroll leste første statuslinje fra `handoff/WP-R1-FORMAT.md`:

```text
STATUS: LEVERT — commit d224a4ed2b6b6b384dff4b8942978bae9f56ade0 på pdd/skjelett-elementer — T-F1/T-F2 grønne
```

Worktree-en var ren på nøyaktig denne SHA-en og grenen `pdd/skjelett-elementer`.
Arbeidet ligger direkte oppå R1c i `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918`.
Hele originalprompten `_losen-queue/done/wp-r3-native-20260919.prompt.md`, den nye
stoppregelen, `SKJELETT_ELEMENTER.md` iterasjon 6 med hele §2.2, og
[WP-R2-WEB.md](WP-R2-WEB.md) er lest. Webkilden er også kontrollert direkte i
CellScaffold-worktree-en på `943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5`.

Ingen parser-/CellBase-endring eller ny JSON-kontrakt er innført. R2 er en
CellApple-overlast av `SkeletonList.getElements(in:allowCellFallback:)` og en
felles `SkeletonRenderDataContext`. Den brukes av List-rader, Tree-rader og
ComponentSurface; Grid/Picker/felt leser samme kontekst.

## Per element — bygget, kilder og kjørte tester

«Ja» betyr implementert og kompilert for macOS/arm64. Testene under er kjørt
som del av den grønne sluttkjøringen. Der en test bare undersøker modell,
attributter eller statisk raster, står det eksplisitt; det er ikke interaksjonsbevis.

| Element | Bygget | Fil/linje og atferd | Tester skrevet/kjørt og avgrensning |
|---|---|---|---|
| Tree | Ja | [CellTreeView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellTreeView.swift:86>), [SkeletonView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:817>). Én ScrollView/LazyVStack over cellens synlige rekkefølge. Unike streng-ID-er, fokus ved ID, opp/ned/Home/End/venstre/høyre/Enter/Space, egen disclosure, separat valg, ingen optimistisk utbretting. Nivå og innrykk er separate verdier. Fokus søker nærmeste gjenlevende forelder etter bekreftet lukking. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:121>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:142>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:164>): **3 bestått** mot den faktiske tastatur-/oppdateringsmodellen. Tastetrykk i NSWindow og VoiceOver er ikke kjørt. |
| ComponentSurface visning/databinding | Ja | [montering](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellComponentSurfaceView.swift:7>), [view](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellComponentSurfaceView.swift:37>), [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:9>). Lokal mount fra sourceKeypath, item først/root-fallback, null bevares, ingen omskriving. Samme revisjon beholder definisjonens Swift-ID-er; ny revisjon erstatter definisjonen med samme instanceID. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:53>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:109>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:245>): **3 bestått** for tofiksuren, revisjon, logiske søsken-ID-er og adskilte utkastlagre. Dette er ikke et faktisk ComponentSurface-klikk eller visuelt monteringsbevis. |
| ComponentSurface kildehandlinger | Delvis | [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:54>), [dispatch](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellTreeView.swift:208>), [SkeletonView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1691>). Request har keypath, original payload og separate sourceCellEndpoint/mount. Button, TextField, TextArea, Toggle, Picker, List, Tabs og Tree har scoped handlingsvei. Manglende adapter feiler eksplisitt. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:78>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:99>): **2 bestått**, eksakt fixturepayload/metadata og ingen fallback til vertscellen. Ingen virkelig kildecelle, avvisning eller Agreement-utveksling kjørt. Se begrensningene nedenfor. |
| ComponentSurface generisk drakilde | Renderergrense ja; R6 nei | [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:139>), [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:159>). Samme rolle/payload-utledning som andre elementer; adapteren får et inert kortpreview og generisk droppbeskrivelse. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:231>): **bestått** for descriptor/binding. Ingen dragstart, kortpreview-bilde eller drop er kjørt. |
| M1 paddingInsets | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:134>). SwiftUI EdgeInsets inni deklarert ytre boks. Eksplisitt 0 overstyrer uniform padding, utelatte kanter faller tilbake. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:201>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:287>): **bestått**. Både insets og faktisk 100×40-raster med asymmetrisk padding kontrolleres. |
| M2 typografi | Ja for macOS-rendereren | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:18>), [native-tekst](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeText.swift:57>), [native-tekst](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeText.swift:120>). Ordnet fontliste med plattformfallback, signert tracking, tabular via monospacedDigit/nummerfeatures, eksplisitt proportional. Linjeboks er fontSize×multiple i NSParagraphStyle for visning og vanlig TextArea; TextField får tilsvarende enlinjeboks. Typografi arves. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:257>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:269>): **2 bestått** for arving, 11→15-linjeboks, fontvalg, tracking, understrek og nummerfeature. Faktiske redigerings-/fontpikseltester, richMarkdown-typografi og iOS TextArea-paritet er ikke verifisert. |
| M3 listerader | Ja | [List](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:190>), [radstil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:253>). itemSpacing, rowInsets, rowDecoration:none; delvis rowInsets bruker 0 på utelatte kanter som web. Scroll og valg-/aktiveringsmodell består. | Bygd i sluttkjøringen; insets-hjelper inngår i [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:201>). **Ingen egen M3-rad-/scrolltest skrevet eller kjørt.** |
| M4 størrelse/flex | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:134>), [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:296>). min/max-størrelser og vektet fordeling av ledig plass i samme stabile H/V-layouttype. Nullverdier beholdes. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:310>): **bestått statisk rastertest** av to ulike flexvekter. Ingen full skjerm med blandede kontrolltyper er målt. |
| M5 controlStyle/accessibilityLabel | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:134>), [SkeletonView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1691>). Plain-kontrollstil, eksplisitt kontrollnavn, knappens tilgjengelige navn beholdes over den bundne etiketten. | Bygd; eksisterende knappetester inngår i 132/132. **Ingen ny AX-/VoiceOver-test av M5 skrevet eller kjørt.** |
| M6 border/shadow/contentClip | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:194>), [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:253>). Solid/dashed/dotted, logiske kanter med avrundede hjørnesegmenter, signert spread også ved blur=0; cornerRadius klipper ikke alene. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:334>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:344>): **bestått rastertest** for klipp og spread uten blur. Delkanter/dash og faktisk hit-test utenfor klippet har ikke egne funksjonstester. |
| M7 / V3-A | Ja | [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:258>), [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:291>), [Grid](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellGridView.swift:86>), [Porthole-vert](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/PortholeView.swift:36>). Første treff, inklusive grenser, alle kapabiliteter; ukjente dimensjoner matcher ikke terskler. Faste bredder, padding og Grid-spor snevrer inn. Én GeometryReader ved Porthole-vertsgrensen; **ingen ny GeometryReader per skjelettelement**. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:174>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:186>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:245>): **bestått** for 236/1200-kolonnen, arv, terskler, item-vilkår og stabile ID-er. GUI-fokus/scroll/utkast ved variantskifte er ikke endelig verifisert. |
| M8 + R4 | Ja som renderer-/vertskontekst; R6 gjenstår | [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:123>), [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:79>). Én kortlivet dragkontekst per Porthole; alle aksepterende flater kan markeres. Hover/fokus/dragActive/dragSource komponeres, source vinner per egenskap. begin/end er adaptergrensen. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:213>): **bestått** for to roller, prioritet og opprydding. Ingen faktisk OS-hover-/tastatur-/dragøkt kjørt. |
| M9 dekorasjon/rotasjon | Ja | [native-tekst](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeText.swift:57>), [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:134>). Understrek og rotasjon; textTransform er fortsatt utsatt. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:269>) kontrollerer understrek-attributtet: **bestått**. Ingen egen rotasjonsrastertest skrevet eller kjørt. |
| M10 leadingMarker | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:204>). Dekorativt leading-overlay med bredde/insets/offset/radius, uten hitflate eller egen layoutbredde. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:344>): **bestått** faktisk raster utenfor boksen, med uendret rasterstørrelse. |
| R1 fontWeight | Ja | [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:18>) og weightFrom/nsWeight i SkeletonView. Samme 100…900-tabell som web; 600→semibold, ukjent→regular. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:201>): **bestått** for alle ni navngitte/numeriske par. |
| R2 radkontekst | Ja | [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:9>), [runtime](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeRuntime.swift:45>), [List](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift:208>). Ett felles oppslag: item først, så hele keypathen fra root, uten sammensmelting. Manglende mountdata faller ikke gjennom til vertscelle-I/O. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:34>): **bestått** med nested fallback, eksplisitt null, ulik rad/root-liste og fraværende item. |
| R7 vAlignment | Ja | [SkeletonView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:795>), [native-stil](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonNativeStyle.swift:296>). HStack leser vAlignment; første/siste baseline bruker både ascent og descent. RTL håndteres av layouten. | [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:201>), [native-test](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonNativeRendererTests.swift:298>): **bestått** tabell og virkelig 40×50-layout med ulike baselineguider. Ikke en font-/web-baselinesammenligning. |

## Avvik fra web og uferdig ComponentSurface

1. **CS-SOURCE-HOST:** Native har ordinær ruting til andre celler, men
   `Meddle.set(keypath:value:requester:)` ([protokoll](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellBase/Protocols/CellProtocol.swift:52>))
   bærer ikke monteringsmetadata ved siden av payload. Ingen slik metadata er
   flettet inn i brukerdata. Den nye `skeletonNativeActionHandler` må integreres
   av verten med aktiv requester og kildecellens ordinære Agreement-flyt.
   Uten den feiler scoped handlinger eksplisitt. Web har tilsvarende uferdig
   kildeendepunkt/mount-grense i Porthole-transporten.
2. **CS-SCOPED-CONTROLS:** Native blokkerer foreløpig `Reference`,
   `AttachmentField`, `FileUpload`, `NavigationBar` og `Visualization` **inne i
   en montert definisjon**, med synlig melding ved [SkeletonView](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:758>). Disse eldre
   I/O-grenene er ikke flyttet til en kildebevisst adapter. Utenfor monterte
   definisjoner beholdes de ordinære grenene. Web har bredere renderer-callback-
   dekning her. Dette er uferdig native-implementering og en del av DELVIS,
   ikke et nytt kontrakthull som stopper andre elementer.
3. **TREE-AX-DISCLOSURE:** Web setter disclosureknappen aria-hidden og lar raden
   bære expanded. Native har en separat navngitt disclosureknapp for VoiceOver,
   slik oppdraget uttrykkelig krever. Radvalget er en egen tilgjengelig handling;
   nivået annonseres fra levelKeypath som radens tilgjengelige verdi. Faktisk
   VoiceOver-rekkefølge/uttale, roving tastaturfokus og handlinger i radmalen må
   verifiseres i Binding.
4. **CS-REVISION-STATE:** Definisjons-/instansmodellen, stabile feltnøkler og
   separate utkastlagre er enhetstestet. macOS har scrollobservasjon i
   [SkeletonScrollState](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonScrollState.swift:8>).
   Full gjenoppretting av fokus, tekstmarkering og scroll ved endret
   understruktur/revisjon er **ikke** funksjonsbevist. Web bruker eksplisitt DOM-
   snapshot/restore; native bruker SwiftUI-identitet, feltlager og macOS-
   scrollobservasjon. iOS har ikke denne ekstra scrollobservatøren.
5. **NATIVE-FONT/EDITOR:** Fontlisten prøves på maskinen og ender i vertsfont.
   Ingen garanti om at Avenir Next/Segoe UI/glyfmetrikk blir lik på begge
   klienter. Vanlig macOS TextArea bruker native paragraph-attributter når M2
   krever dem; richMarkdown og iOS-redigering er ikke komplett M2-paritetsmålt.
6. **R6-NATIVE-DND:** Transferadapteren er en renderergrense med descriptor og
   inert preview. Den leverer ikke Binding sin OS-drag/drop-sesjon. Native
   drag/drop teller derfor ikke som bestått T-F3. Avviket står i
   [ACCEPT.md](../ACCEPT.md#parity).

Ingen Butler-spesifikk kode er lagt til. R3 i kontraktens §3 (abonnement,
persistens og kilde→instans-cellearbeid), R5 og R6 er ikke levert av denne pakken.

## Vertsintegrasjon

PortholeView deklarerer sin målte vertsgrense én gang og mater SkeletonView med
`viewModel.skeletonRootData`. Verten/cellen må oppdatere denne snapshoten; den
nye egenskapen er ikke et abonnement. En annen vert, som Binding, kan bruke:

```swift
SkeletonView(element: element, renderData: .init(root: rootSnapshot))
    .environmentObject(portholeViewModel)
    .environment(\.skeletonLayoutContext, declaredLayoutContext)
    .environment(\.skeletonNativeActionHandler, sourceAwareHandler)
    .environment(\.skeletonNativeDragContext, hostDragContext)
    .environment(\.skeletonNativeTransferAdapter, bindingTransferAdapter)
```

`sourceAwareHandler` mottar sourceCellEndpoint og `mount` separat fra payload;
verten må aldri bruke egne privilegier som erstatning for aktiv requester.
`bindingTransferAdapter` må kalle dragkontekstens begin/end ved dragstart,
drop, avbrudd og teardown. `drag` skal først deklareres som kapabilitet når
adapteren faktisk finnes. Udeklarerte containere arver tilgjengelig plass.

## Eksakte kjøringer og bevis

Arbeidsmappe for alle Swift-kommandoene var R1c-worktree-en over.
Avhengighetene i `.build/` var tilstrekkelige. Ingen fetch, resolve eller
nedlasting ble startet som separat steg; kommandoene fullførte under den
nettverksbegrensede kjørekonteksten. SwiftPM meldte eksisterende advarsler om
manifest-cache som ikke var skrivbar og tre ubehandlede markdownressurser.
De hindret ikke bygg/test.

```sh
export CLANG_MODULE_CACHE_PATH=/tmp/wp-r3b-clang-cache
export SWIFTPM_MODULECACHE_OVERRIDE=/tmp/wp-r3b-swift-cache
swift build --disable-sandbox --target CellApple
```

**Kjørt, exit 0**, `Build complete! (5,40 sek)` på endelig kode.
[Full bygglogg](../evidence/wp-r3-native/build-final.log).
Basen ble også bygget før endringene: exit 0,
[baselinelogg](../evidence/wp-r3-native/build-baseline.log).

```sh
export CLANG_MODULE_CACHE_PATH=/tmp/wp-r3b-clang-cache
export SWIFTPM_MODULECACHE_OVERRIDE=/tmp/wp-r3b-swift-cache
swift test --disable-sandbox --filter 'SkeletonNativeRendererTests|SkeletonTests|SkeletonReachabilityAuditTests|SkeletonStyleParityTests|SkeletonButtonResolutionTests|SkeletonActionButtonExecutionTests|PortholeViewModelAvailabilityTests'
```

**Kjørt, exit 0: 132 tester, 0 feil**, hvorav **21 nye** i
`SkeletonNativeRendererTests`. [Full testlogg](../evidence/wp-r3-native/tests-final.log).
Det ble også kjørt avgrensede `swift test --disable-sandbox --filter
SkeletonNativeRendererTests`-kjøringer under utviklingen. Første fullførte
native-kjøring hadde 14 tester og fem assertionsfeil: objektpayload ble
sammenlignet med ValueType sin objektlikhet. Testen sammenligner nå hele
kanoniske JSON-payloaden med sorterte nøkler. Tidlige rasterassertions brukte
feil side av en leading-justert boks og antok en fargeverdi uten referanseraster;
sluttesten bruker korrekt utløpsside og samme rendererfarge som kontrollflate.
Disse tidlige loggene ligger ved som `tests-first-execution.log` og
`tests-pixel-initial.log`. Ingen test er slettet for å få grønt.

`git diff --check` og `git diff --cached --check`: exit 0 før commit.
Verktøykjede: Apple Swift 6.4 (`swiftlang-6.4.0.34.1`, clang 2100.3.34.1),
target `arm64-apple-macosx27.0.0`. iOS/tvOS/Binding/Xcode-bygg er ikke kjørt.
[summary.json](../evidence/wp-r3-native/summary.json) har SHA-256 for alle
endrede kodefiler og den **uendrede felles tofiksuren**.

## T-F3 og videre arbeid

`SkeletonParityRenderer.renderPNG` er **ikke utvidet** med nodeliste eller
action-driver og er ikke brukt som T-F3-bevis. De statiske rastertestene bruker
ImageRenderer direkte for størrelser, baseline, flex, klipp, marker og spread.
De beviser ikke fungerende Tree-/ComponentSurface-interaksjon.

Kjetil må bygge Binding i Xcode med **c81a39799c3f664d77afa5f5de131ddac70f3c9c** og ta native
skjermbilde med **samme kandidat-JSON, nodedata, layoutkontekst og flate som web**.
Før komplett godkjenning må dette også dekke tastatur/VoiceOver,
cellebekreftet tree-state, oppdatering av to monteringer, kildehandling med
korrekt tilgang, og variantskifte uten tap av fokus/utkast/scroll. R6 må leveres
og dra/slipp/avbrudd kjøres før native drag/drop kan godkjennes.

[Apple: AnyLayout og bevaring av underliggende state](https://developer.apple.com/documentation/swiftui/anylayout)
og [Apple: tilgjengelighetsrepresentasjon](https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:))
ble kontrollert som API-bakgrunn. Implementeringen bruker én stabil egen Layout
i H/V-stackene; API-dokumentasjonen erstatter ingen test over.

## Git og dokumenter

Kodecommit: **c81a39799c3f664d77afa5f5de131ddac70f3c9c**, gren **pdd/skjelett-elementer**.
Worktree-en er ren etter commit. Ingen push, PR eller deploy.

Denne handoffen, `ACCEPT.md` og `evidence/wp-r3-native/` er skrevet i den allerede
urene CellProtocolDocuments-worktree-en, gren `codex/docs-cleanup-20260810`,
HEAD `cc31b5c37f5517a52e56fc7a3e93da4432022680`. De er ikke committet i
arbeidet her; øvrige dokumentendringer er beholdt.
