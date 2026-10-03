# WP-R1 — CellProtocol: formatet og monteringskontrakten for Butler-flaten
STATUS: LEVERT — commit d224a4ed2b6b6b384dff4b8942978bae9f56ade0 på pdd/skjelett-elementer — T-F1/T-F2 grønne

Dato: 2026-09-19. Utfører: Astra (Codex). WP-R1c bygger videre på WP-R1b.
Hele `SKJELETT_ELEMENTER.md`, iterasjon 6, §2.2 er lest før implementering.
Feltlistene og de nyttige kontraktforklaringene fra R1b er beholdt nedenfor med
oppdaterte linjenumre.

**Den ekte pakken er bygget. T-F1: 71 tester, 0 feil. T-F2: 23 tester, 0 feil.**
Alle tre påkrevde kommandoer ga exit 0. Ingen avhengigheter eller runtime-typer
ble erstattet. R1bs isolerte probe brukes ikke som bevis for denne statusen.
T-F3, T-P1 og T-P2 inngår ikke i denne sertifiseringen.

## Gren, worktree og commit

- Repo: `CellProtocol`.
- Worktree: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918`.
- Gren: `pdd/skjelett-elementer`; samme worktree og gren som R1b.
- Direkte forelder: `287e191eac4adabb1a3c040a3f9a5c9a19db1466`.
- **Implementeringscommit: `d224a4ed2b6b6b384dff4b8942978bae9f56ade0`**.
- Commitmelding: `Add strict component mount contract and shared renderer fixture`.
- Sju filer i commiten: to kildefiler, to testfiler, to nye JSON-fixtures og README.
- Worktree var ren før endring og er ren etter commit.
- Ingen push, gh, ssh, curl, PR, merge eller deploy. Nett ble bare brukt av SwiftPM.
- `.build/` er beholdt med 34 dependency-checkouts for WP-R3b. Ingen rydding er kjørt.
- `Package.swift` og `Package.resolved` er uendret.
- Denne rapporten og de tilhørende loggene er skrevet i dokumentrepoet, uten
  dokumentcommit. Øvrige eksisterende dokumentendringer er beholdt.

## Nye cases og felt, med fil og linje

Kildereferanser nedenfor gjelder implementeringscommiten:

- **S** = [Sources/CellBase/Skeleton/SkeletonDescription.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellBase/Skeleton/SkeletonDescription.swift).
- **A** = [Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift).
- **T** = [Tests/CellBaseTests/SkeletonTests.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonTests.swift).
- **AT** = [Tests/CellBaseTests/SkeletonReachabilityAuditTests.swift](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/Tests/CellBaseTests/SkeletonReachabilityAuditTests.swift).

### Tree

`SkeletonElement.Tree(SkeletonTree)` er lagt til på **S:3625**;
`SkeletonTree` på **S:1963**. Kanonisk form er `{"Tree":{…}}`.

| Felt | Swift-type | Fil:linje |
|---|---|---|
| `keypath` | `String` | S:1965 |
| `idKeypath` | `String` | S:1966 |
| `parentIDKeypath` | `String` | S:1967 |
| `levelKeypath` | `String` | S:1968 |
| `leadingInsetKeypath` | `String` | S:1969 |
| `hasChildrenKeypath` | `String` | S:1970 |
| `expandedKeypath` | `String` | S:1971 |
| `selectedIDStateKeypath` | `String` | S:1972 |
| `selectionActionKeypath` | `String` | S:1973 |
| `expansionActionKeypath` | `String` | S:1974 |
| `rowSkeleton` | `SkeletonVStack` | S:1975 |
| `disclosureModifiers` | `SkeletonModifiers?` | S:1976 |
| `rowModifiers` | `SkeletonModifiers?` | S:1977 |
| `modifiers` | `SkeletonModifiers?` | S:1978 |

Alle ti keypaths er obligatoriske, ikke blanke strenger. `rowSkeleton` må være
en innpakket `VStack`; ukorrekt radform skal ikke bli en tom, tilsynelatende
vellykket rad. Valgfri dekorasjon gir ingen List-innpakning når den mangler.

Cellen leverer en ferdig ordnet synlig nodeliste. Rendereren skal ikke traversere
eller filtrere den. Stabil node-ID er atskilt fra indeks; nullable forelder ligger
i radens data. Semantisk nivå (rot = 1) og visningsinnrykk er forskjellige felt.
Valg sender `{nodeID:String}`; utbretting sender `{nodeID:String, expanded:Bool}`
og venter på cellebekreftelse. Dette er dokumentert formatkontrakt, ikke en
implementert tastatur-, fokus- eller innlastingsmekanisme.

### ComponentSurface

`SkeletonElement.ComponentSurface(SkeletonComponentSurface)` er lagt til på
**S:3626**; typen på **S:2108**. Kanonisk form er `{"ComponentSurface":{…}}`.

| Felt | Swift-type | Fil:linje |
|---|---|---|
| `sourceKeypath` | `String` | S:2110 |
| `instanceID` | `String` | S:2111 |
| `variant` | `SkeletonComponentVariant` | S:2112 |
| `modifiers` | `SkeletonModifiers?` | S:2113 |

`sourceKeypath`, `instanceID` og `variant` er obligatoriske; variant er
`inline` eller `pinned`, uten implisitt standard. De to strengene må være ikke
blanke. Kildens `componentID` og revisjon ligger i `SkeletonComponentMount`;
`instanceID` identifiserer monteringen og skal opprettes/persisteres av cellen.
To monteringer fra samme kilde får ulike ID-er. Layout-/variantskifte skal bevare
ID-en. Den interne, ikke serialiserte UUID-en `id` er ikke denne kontrakten;
WP-R2/R3 må bruke `instanceID` som monteringsidentitet.

Registerlagring, kildeoppslag, abonnement og persistens implementeres i R3/vert.
WP-R1 gjør ingen I/O og bestemmer ingen ny registerplassering i CellConfiguration.
Auditen får den konkrete oppløste definisjonen gjennom en eksplisitt callback.

### SkeletonComponentMount — iterasjon 6, §2.2

`SkeletonComponentMount: Codable` på **S:2169** er den konkrete verdien på
`ComponentSurface.sourceKeypath`. Den er et vanlig JSON-objekt uten egen
`SkeletonComponentMount`-wrapper og er ikke en ny `SkeletonElement`-case.

| Felt | Swift-type | Fil:linje |
|---|---|---|
| `componentID` | `String` | S:2170 |
| `revision` | `String` | S:2171 |
| `sourceCellEndpoint` | `String` | S:2172 |
| `skeleton` | `SkeletonElement` | S:2173 |
| `item` | `ValueType?` | S:2174 |

De fire første feltene er obligatoriske. Manglende, null, feiltype eller blanke
strengfelt avvises med feltnavn. `skeleton` må ha én element-wrapper med objekt-
eller array-payload; manglende/null/skalar/tom/ukjent wrapper og Unsupported på
roten avvises. Eksisterende dekoding av undertrær er bevart; en eventuell nested
Unsupported er fortsatt et auditfunn, aldri en vellykket definisjonstest.
Ukjente descriptor-felt avvises også. Strengvalideringen og avvisning av
Unsupported på roten gjelder ved encoding av programmatisk opprettede verdier.

`item` kan utelates eller være null; begge dekodes til nil. Andre gyldige
ValueType-verdier er tillatt, ikke bare objekter. `instanceID` bor på
`ComponentSurface`, ikke på monteringsbeskrivelsen. Ingen UUID serialiseres som
erstatning for denne identiteten.

Monteringskontrakten er dokumentert ved **S:2161** og i den delte fixturen:

- Keypaths i definisjonen leser monteringens item først, deretter vertens root.
  Uten item brukes bare root. Keypaths omskrives aldri per instans.
- Kildehandlinger sendes til `sourceCellEndpoint`. Metadata
  `{instanceID, componentID, revision}` sendes i et eget `mount`-felt ved siden
  av original `payload`. Kildecellen avgjør tilgang gjennom vanlig celleflyt.
- Vertshandlinger som løsne/flytt/full flate ligger utenfor definisjonen.
- Nytt item med samme instanceID oppdaterer på stedet. Ny revision monterer
  definisjonen på nytt med beholdt instanceID; fokus, scroll og utkast skal
  bevares der elementet fortsatt finnes. Rendererbeviset hører til T-F3.

Felles fixture:
[`component-mount-two-instances.json`](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918/fixtures/skeleton-wp-r1/component-mount-two-instances.json).
Den inneholder to ComponentSurface med ID `A` og `B`, separate sourceKeypaths,
samme `program-card`/`r1` og samme definisjon. A viser «Program», B «Sesjoner».
En ekstra `subtitle` viser fallback til vertens root. Knappen har uendret
`actions.refresh`; fasiten peker til `cell:///ProgramFixture`, som er forskjellig
fra vertens `cell:///HostFixture`. Payload har sin egen `instanceID` for å avdekke
uønsket sammenfletting med monteringsmetadata.

`sourceUpdates` erstatter bare `mounts.A`, med «Program oppdatert». Felles fasit
ligger i `expected.initial`, `expected.actions[].dispatch`,
`expected.afterUpdates`, `unchangedInstanceIDs`, `remountedInstanceIDs`,
`unchangedMounts` og `unchangedDefinition`. README beskriver hvordan begge
klienter skal kjøre samme scenario. Swift sammenligner byte-identisk skeleton
etter JSON-encoding med sorterte nøkler, både mellom A/B og etter oppdateringen.
Dette er en serialiseringsinvariant og en kontroll av fasiten; ingen Swift-test
her utgir seg for å ha klikket eller oppdatert en virkelig renderer.

### M1–M10: 23 nye toppnivåfelt

25 i kontraktens sammenslåtte liste minus utsatt `textTransform` og M11 gir 23.
`contentClip` er det eneste klippefeltet; ingen `clipsToBounds`-alias er innført.

| Felt | Swift-type | Fil:linje |
|---|---|---|
| `paddingInsets` | `SkeletonInsets?` | S:1050 |
| `fontFamilies` | `[String]?` | S:1051 |
| `lineHeightMultiple` | `Double?` | S:1052 |
| `letterSpacing` | `Double?` | S:1053 |
| `numericVariant` | `SkeletonNumericVariant?` | S:1054 |
| `itemSpacing` | `Double?` | S:1055 |
| `rowInsets` | `SkeletonInsets?` | S:1056 |
| `rowDecoration` | `SkeletonRowDecoration?` | S:1057 |
| `minHeight` | `Double?` | S:1058 |
| `maxHeight` | `Double?` | S:1059 |
| `minWidth` | `Double?` | S:1060 |
| `flexGrow` | `Double?` | S:1061 |
| `controlStyle` | `SkeletonControlStyle?` | S:1062 |
| `accessibilityLabel` | `String?` | S:1063 |
| `borderStyle` | `SkeletonBorderStyle?` | S:1064 |
| `shadowSpread` | `Double?` | S:1065 |
| `borderEdges` | `[SkeletonEdge]?` | S:1066 |
| `contentClip` | `Bool?` | S:1067 |
| `layoutVariants` | `[SkeletonLayoutVariant]?` | S:1068 |
| `interactionStyles` | `SkeletonInteractionStyles?` | S:1069 |
| `textDecoration` | `SkeletonTextDecoration?` | S:1070 |
| `textRotationDegrees` | `Double?` | S:1071 |
| `leadingMarker` | `SkeletonLeadingMarker?` | S:1072 |

Hjelpetyper og nested felt:

- **S:568–576**: `SkeletonNumericVariant(proportional, tabular)`,
  `SkeletonRowDecoration(platform, none)`, `SkeletonControlStyle(platform, plain)`,
  `SkeletonBorderStyle(solid, dashed, dotted)`, `SkeletonEdge(top, leading, bottom,
  trailing)`, `SkeletonTextDecoration(none, underline)`,
  `SkeletonLayoutAxis(horizontal, vertical)`,
  `SkeletonCapability(pointer, hover, keyboard, drag, touch)`,
  `SkeletonComponentVariant(inline, pinned)`.
- **S:580** `SkeletonInsets`: `top` (581), `leading` (582), `bottom` (583),
  `trailing` (584), alle `Double?`.
- **S:635** `SkeletonInteractionStyle`: `background` (636), `foregroundColor`
  (637), `opacity` (638); hver tilstand er en begrenset, delvis stil.
- **S:679** `SkeletonInteractionStyles`: `hover` (680), `focusVisible` (681),
  `dragSource` (682), `dragActive` (683), alle valgfrie stiler.
- **S:722** `SkeletonLeadingMarker`: `width` (723), `insetTop` (724),
  `insetBottom` (725), `offset` (726), `cornerRadius` (727), `color` (728).
  Alle er obligatoriske når markøren er angitt; ingen layout-/hitflate tilføres.
- **S:522** `SkeletonFormatError(field, reason)` navngir avviste nye felt.

Fravær og intervaller er dokumentert ved typene og **S:1042**:

- Nye modifikatorfelt forblir `nil` ved fravær og bevarer grunnatferden.
  Insets arver skalar `padding` per utelatt side, deretter null. Eksplisitt null
  overstyrer skalar padding. Insets og størrelser er endelige og ikke negative.
- `fontFamilies` er prioritert; manglende/uttømt liste bruker vertens eksisterende
  skriftfallback. `numericVariant:nil` betyr skriftens standard. `normal` avvises.
- `lineHeightMultiple > 0` betyr linjebokshøyde / fontSize. `letterSpacing`,
  `shadowSpread`, `textRotationDegrees` og markørens `offset` er endelige og kan
  være negative. `itemSpacing` og `flexGrow` er endelige og minst null.
- `rowDecoration`/`controlStyle` uten verdi bruker platform; `borderStyle` uten
  verdi bruker solid. `borderEdges:nil` betyr alle, `[]` betyr ingen.
  `contentClip` uten verdi gir ingen eksplisitt klipping; true gjelder den
  avrundede innholdsgrensen. `rowDecoration:none` endrer ikke scroll/tomtekst.
- Fraværende interaction-tilstand gjør ingen stilendring. Når dragtilstandene
  overlapper, overstyrer `dragSource` de samme egenskapene fra `dragActive`;
  utelatte egenskaper beholder eksisterende stil. Opacity er i [0,1]. Verken
  `dragging` eller `draggingScope` godtas i dette nye objektet.
- Nye avgrensede objekter avviser ukjente nøkler, inkludert actions/CSS i stiler
  og layoutvarianter. Ingen `viewportClass`, `textTransform` eller M11 er lagt til.

### SkeletonLayoutVariant og V3-A

Typen begynner på **S:785**. Alle felt er valgfrie:

| Felt | Swift-type | Fil:linje |
|---|---|---|
| `when` | `SkeletonCondition?` | S:786 |
| `minAvailableWidth` | `Double?` | S:787 |
| `maxAvailableWidth` | `Double?` | S:788 |
| `minAvailableHeight` | `Double?` | S:789 |
| `maxAvailableHeight` | `Double?` | S:790 |
| `requiresCapability` | `[SkeletonCapability]?` | S:791 |
| `axis` | `SkeletonLayoutAxis?` | S:792 |
| `columns` | `[SkeletonGridColumn]?` | S:793 |
| `spacing` | `Double?` | S:794 |
| `paddingInsets` | `SkeletonInsets?` | S:795 |
| `minHeight` | `Double?` | S:796 |
| `maxHeight` | `Double?` | S:797 |
| `flexGrow` | `Double?` | S:798 |
| `fontSize` | `Double?` | S:799 |
| `borderColor` | `String?` | S:800 |
| `foregroundColor` | `String?` | S:801 |

Valget skjer med `SkeletonModifiers.layoutVariant(in:root:item:context:)`
(**S:1077**). Første treff i deklarert rekkefølge vinner; intet treff returnerer
nil, som betyr grunnlayout. Terskler er inklusive og endelige, minimum må ikke
overstige maksimum, og alle oppgitte kapabiliteter må finnes. En ukjent dimensjon
matcher ingen terskel på den aksen. `when` bruker eksisterende SkeletonCondition;
ingen ny uttrykksmotor, handling eller komponentinstans opprettes ved valg.

`SkeletonLayoutContext` (**S:954**) har `availableWidth` (955), `availableHeight`
(956) og `capabilities` (957). Verten deklarerer innholdsplassen på roten. En
container som kjenner sin plass gir barna `narrowed(availableWidth:availableHeight:)`
(**S:968**): oppgitt barnemål begrenses av kjent foreldremål; utelatt akse arves.
Nil betyr ukjent, ikke uendelig. Ugyldige verts-/barnemål kaster navngitt feil.

**Prisen i V3-A står:** uten eksplisitt innsnevring arver barnet forelderens tall.
Ingen per-element-måling finnes. En 236-enheters kolonne må derfor deklarere 236;
barna arver deretter 236, ikke flatens 1580. Grid-spor, paneler og drawere må kalle
denne mekanismen i WP-R2/R3. Bevaring av utkast, fokus, valgt rad og abonnement
ved en virkelig rendererovergang må fortsatt funksjonstestes der.

## Ekte bygg og testresultater

Arbeidskatalogen var worktree-en angitt over. Eksakte miljøvariabler for alle
kommandoene:

```sh
export CLANG_MODULE_CACHE_PATH=/tmp/wp-r1c-clang-cache
export SWIFTPM_MODULECACHE_OVERRIDE=/tmp/wp-r1c-swift-cache
```

Swift: `Apple Swift version 6.4 (swiftlang-6.4.0.34.1 clang-2100.3.34.1)`.
Target: `arm64-apple-macosx27.0.0`.

| Eksakt kommando | Exit-kode | Tester | Feil | Feilende testnavn |
|---|---:|---:|---:|---|
| `swift build --disable-sandbox` | 0 | 0 (bygg, ingen testkjøring) | 0 byggefeil | Ingen |
| `swift test --disable-sandbox --filter SkeletonTests` | 0 | 71 | 0 (0 unexpected) | Ingen |
| `swift test --disable-sandbox --filter SkeletonReachabilityAuditTests` | 0 | 23 | 0 (0 unexpected) | Ingen |

Alle tre lyktes på første kjøring i WP-R1c. Ingen tester ble svekket, fjernet
eller rettet for å gjøre resultatet grønt. Det var ingen feilende testnavn å
rapportere. Dette er 94 faktisk kjørte XCTest-metoder; antallet inkluderer både
eldre regresjonstester og R1/R1c-testene.

Rålogger er bevart i dokumentrepoet:

- [Bygg](wp-r1c-evidence/swift-build.log): `Build complete! (78,28 sek)`.
- [SkeletonTests](wp-r1c-evidence/swift-test-skeleton.log): 71 tester, 0 feil.
- [SkeletonReachabilityAuditTests](wp-r1c-evidence/swift-test-audit.log): 23 tester, 0 feil.
- [Maskinlesbare resultater og SHA-256 for loggene](wp-r1c-evidence/results.json).

Originalene ligger også i `/tmp/wp-r1c-swift-build.log`,
`/tmp/wp-r1c-swift-test-skeleton.log` og `/tmp/wp-r1c-swift-test-audit.log`.
`--disable-sandbox` slår av SwiftPMs ekstra prosess-sandkasse; miljøets tillatelser
er ikke endret. Avhengighetene ble løst av SwiftPM og kompilert i denne pakken.

Bygget ga advarsler, blant annet om manglende `Tree`/`ComponentSurface`-cases i
Apple-rendererens switch-er på `SkeletonView.swift:830` og `:1060`, og om Swift
concurrency-isolasjon. De gir ikke byggefeil i den gjeldende Swift 5.8-pakkemodusen.
WP-R3b må håndtere renderer-case-ene; et grønt formatbygg beviser ikke at de
nye elementene rendres. Øvrige advarsler står uavkortet i råloggen.

`git diff --check`, `git diff --cached --check` og JSON-parsing av alle seks
JSON-fixtures ga også exit 0. Ingen ny isolert probe eller erstattede avhengigheter
ble brukt.

## Testdekning med kildehenvisninger

De 11 R1-formatmetodene er beholdt på **T:1615**, **T:1627** og
**T:1813–1968**. De dekker Tree/ComponentSurface-tur-retur, alle nye modifierfelt,
63 negative modifier-fixtures, obligatoriske felt, ikke-endelige tall, undertrær,
defaults, dragSource-prioritet, layoutvalg, 1580 → 236-breddearv og gammel
padding-lossiness. Positive tester krever feltlikhet og ingen Unsupported.

Fem nye T-F1-metoder:

| Test | Fil:linje | Invariant |
|---|---|---|
| `testWPR1ComponentMountRoundTripPreservesEveryField` | T:1690 | A, B og oppdateringen beholder alle wire-felt gjennom tur-retur. |
| `testWPR1ComponentMountDefinitionsAreByteIdenticalAcrossInstancesAndItemUpdate` | T:1705 | Samme componentID/revision gir byte-identisk serialisert skeleton og uendrede keypaths, selv med ulike item. |
| `testWPR1ComponentMountSharedRendererOracleHasConsistentBindingsActionsAndUpdate` | T:1727 | Felles fasit har Program/Sesjoner, host-fallback, separat payload/mount, riktig kildemål og isolert A-oppdatering. |
| `testWPR1ComponentMountNegativeFixturesRejectWithFieldName` | T:1774 | Alle 35 navngitte negative fixtures avvises med riktig feltnavn. |
| `testWPR1ComponentMountOptionalItemAndProgrammaticValidation` | T:1785 | Fravær/null og gyldige ValueType-item samt avvisning av ugyldig programmatisk encoding. |

Alle 20 tidligere auditmetoder er beholdt. De 11 R1-metodene ligger nå på
**AT:146–203** og **AT:269–315** og tester Tree-actions/dekorasjon, scopes,
komponentoppløsning, manglende action, arv, instanser, duplikater, rekursjon,
skjulte undertrær, malformed betingelser og Section/header/footer/drop.

Tre nye T-F2-metoder:

| Test | Fil:linje | Invariant |
|---|---|---|
| `testWPR1WireMountAdapterPreservesHostRootAndReplacesEnclosingItem` | AT:217 | Mount-item erstatter radens item; nil/null arver ikke raden. |
| `testWPR1WireMountItemDoesNotInventHostRootAvailability` | AT:236 | Item-tilstedeværelse oppretter ingen host-root; eksplisitt root bevares. |
| `testWPR1WireMountSharedFixtureResolvesBothInstances` | AT:247 | Begge ekte fixture-descriptorer kan brukes direkte i auditen; actions.refresh er strukturelt nåbar. |

## Hva auditen nå avviser

**A:132** tar valgfrie `context`, `requiredActionKeypaths` og `resolveComponent`.
Eksisterende kall med bare et element fungerer fortsatt.

- Tree uten ikke-blank `selectionActionKeypath` eller `expansionActionKeypath`
  gir `missingRequiredAction`. JSON med manglende felt avvises allerede av
  dekoderen; programmatisk ufullstendige trær avvises også av auditen.
- ComponentSurface uten oppløst definisjon med componentID/revisjon gir
  `unresolvedComponentDefinition`, ikke et tomt vellykket auditresultat.
- `SkeletonResolvedComponent` (**A:100**) bærer `componentID`, `revision`,
  `skeleton`, `dataContext`. Definisjonen traverseres med monteringsidentitet og
  revisjon i funnstien. `SkeletonReachabilityContext` (**A:74**) angir tilgjengelig
  `root`/`item`/`context` uten å forveksle eksempeldata med permanente tilstander.
- Feil eller manglende scope kan gjøre en handling strukturelt utilgjengelig;
  den eldre initializer-stien arver monteringsposisjonen når ingen ny kontekst er gitt.
- `requiredActionKeypaths` oppdager en forventet handling som er utelatt helt
  fra en oppløst definisjon. Uten en slik forventningsliste kan ingen statisk
  audit utlede hvilke handlinger forfatteren unnlot å beskrive.
- Dupliserte instanceID-er, rekursiv komponentdefinisjon og Unsupported gir
  navngitte funn. Både synlige og skjulte deltrær må ha gyldig oppløsning.
- Tree-radens hitflate og disclosure får egne modifier-/action-kontekster;
  skjult disclosure eksponerer ikke utbrettingshandlingen som nåbar.
- Malformed og konstant falske betingelser kontrolleres også inne i rader.
- Section-header/footer og drop-/presentasjonslukk-/TextArea-submit-handlinger
  inngår nå. Object-barn og rapporterte tapte handlinger har deterministisk orden.

Dette er strukturell nåbarhet. Faktiske actionpayloads, cellens adgangskontroll,
innlasting av rader og alternativ inngang fra samtalen må fortsatt testes i
integrasjonen. Ingen grønn B4-/T-P2-påstand følger av settet med GUI-handlinger.

### Valg: direkte adapter fra SkeletonComponentMount

**A:118** legger til
`SkeletonResolvedComponent(mount:hostContext:)`. Dette er riktig fordi auditen
skal undersøke nøyaktig definisjonen som skal monteres, uten en parallell kopi
av wire-formatet. Den gamle initializer-stien beholdes for eksisterende kall.

Adapteren beholder `componentID`, `revision` og `skeleton`, samt tilgjengelig
root/context fra eksplisitt `hostContext`. Item-tilgjengeligheten erstattes med
monteringens eget item; nil og `.null` gir false selv inne i en rad som hadde
item. Et mount-item oppretter aldri en host-root som ikke finnes. Tre nye tester
på **AT:217**, **AT:236** og **AT:247** beviser dette og leser den delte fixturen.

`sourceCellEndpoint` legges ikke inn som en ny autorisasjons-/dispatchmekanisme i
auditen. Auditen beregner strukturell nåbarhet, ikke handlingsruting eller tilgang.
Derfor lover adapteren heller ikke at en handling vil bli autorisert eller sendt.

## Kompatibilitetsendringer, navngitt

1. **Nye JSON-/Swift-cases:** Tree og ComponentSurface. Eldre renderere har ikke
   støtte. Eksisterende Apple-renderer er urørt; dens fallback leverer ikke de nye
   funksjonene. WP-R2/R3 må konsumere feltene og håndtere enum-utvidelsen.
2. **Streng dekoding av nye felt:** feil type, verdi eller ukjent nested nøkkel
   avvises. Eksisterende SkeletonElement-fallback kan representere avvisningen
   som Unsupported med årsak; dette er bevisst beholdt. Positive tester krever
   riktig case og feltlikhet, ikke bare vellykket JSONDecoder-kall.
3. **Gammel `padding` er uendret:** den bruker fortsatt `decodeLossy`; ingen
   skjerping av eldre modifierverdier er gjort. Ukjente toppnivå-modifiers følger
   fortsatt gammel ignoreringsatferd, så utsatte felt er heller ikke nye aliaser.
4. **Audit er strengere:** flere tidligere oversette feil rapporteres, og flere
   handlinger oppdages. Tillegg til funn-enumen og deterministisk sortering av
   `lostActionKeypaths` kan påvirke konsumenter som sammenligner funn/arrays.
5. Nye objekter og optional-defaults er dokumentert i kildekommentarer og fixtures.
   Book/renderer-kataloger utenfor CellProtocol er ikke endret, i tråd med scope;
   denne rapporten er dokumentoverleveringen for WP-R2b/R3b.

## Overlevering til WP-R2b og WP-R3b

Bruk commiten øverst og den delte monteringsfixturen. T-F1/T-F2 er grønne i den
virkelige pakken; det tidligere cache-/DNS-forbeholdet fra R1b er dermed lukket.
`.build/` med løste avhengigheter er bevart for videre bygg uten nett. R3b kan
bruke de samme cachevariablene og `--disable-sandbox` i denne worktree-en.

Rendererne må fortsatt kjøre T-F3 mot felles fasit: faktisk item/root-binding,
kildehandling gjennom klientens virkelige action-vei, separat mount/payload,
oppdatering av A uten endring/remontering av B og stabile instanceID-er. Det
inngår også å teste Agreement-challenge ved avvist kildehandling, revisjonsskifte
og bevaring av fokus/scroll/utkast. Disse handlingene er kontrakt, ikke utført
rendererfunksjon i WP-R1c. Webs eventuell manglende vei til en annen celle enn
Portholens egen rapporteres som funn etter §2.2, uten å stoppe øvrig rendererarbeid.

Ingen rendererimplementering, pikseltest, R3-abonnement, R4-dragvert, fullflate-
integrasjon eller samtaleinngang inngår her. Ingen merge eller push er utført.
