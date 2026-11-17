# WP-R2c — Kildehandlinger fra ComponentSurface
STATUS: DELVIS — commit bd60709b904244a804e1e4b49096ee1299d4dbd7 på pdd/skjelett-elementer-web — mangler: mount over brotransport; rent bygg/test mot d224a4ed på grunn av eksisterende kompileringsbrudd

## Leveranse og avgrensning

Én isolert CellScaffold-commit: `bd60709b904244a804e1e4b49096ee1299d4dbd7`, forelder `943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5`.
Worktree: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919`.
Ingen push. Nett ble bare brukt av SwiftPM til avhengighetsoppløsning. CellScaffold-worktree-en er ren etter commit; lokale SwiftPM-endringer i `Package.resolved` er tilbakeført. Eksisterende endringer i dokumentrepoet er urørt. Denne handoff-en og evidensen er lokale, nye filer i dokumentrepoet, uten egen dokumentcommit.

**Lokale kildehandlinger er implementert og funksjonstestet.** Med `mount` velges kildegrenen før redigeringskommandoer, navigasjon, referanseprefikser og annen vertsruting. Den bruker eksisterende `CellResolverProtocol.cellAtEndpoint` og kildens vanlige `Meddle.get/set`, med den autentiserte HTTP-brukerens Identity både ved oppslag og handling. Det finnes ingen `controlCell` i kildegrenens funksjonssignatur eller fallback.

`mount` ligger ved siden av `payload` i HTTP-forespørsel og svar. Lokale kildeintercepter kan lese den separat som `ComponentActionContext.mount` (TaskLocal). Loggen har et eget `mount`-objekt og logger ikke payload. Monteringsmetadata gir ingen autoritet. Tillatelse krever fortsatt kildecellens vanlige eierbevis eller signerte Agreement/grant. `CellAuthorizationError` beholdes og blir samme HTTP 403 med `userMessage`/`requiredAction` som øvrige Porthole-handlinger. Uløselig endepunkt gir eksplisitt HTTP 503. Ufullstendig monteringsrute gir 400.

Webadapteren sender feltene videre og viser avslag gjennom eksisterende Porthole-feiltilstand og `renderSkeletonValidationDiagnostic`. Kildehandlinger får ikke vertens keypath-omskriving, payload-dekorasjon, navigasjon eller optimistiske tilstandsoppdateringer. Feilkonvolutter vises også når kildens keypath har samme navn som en vertsnavigasjon. Handlinger uten begge tilleggsfeltene går fortsatt gjennom den gamle implementasjonen.

## Statusport og CellProtocol-pin

Første operasjon leste disse statuslinjene, begge på linje 2:

- `WP-R1-FORMAT.md`: `STATUS: LEVERT — commit d224a4ed2b6b6b384dff4b8942978bae9f56ade0 på pdd/skjelett-elementer — T-F1/T-F2 grønne`
- `WP-R2-WEB.md`: `STATUS: DELVIS — commit 943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5 på pdd/skjelett-elementer-web — mangler: ComponentSurface-kildehandlinger i Porthole, T-F3-nettleserbevis`

Porten var åpen. Den oppgitte CellProtocol-worktree-en sto faktisk på `c81a39799c3f664d77afa5f5de131ddac70f3c9c`, en native-renderer-commit direkte oppå `d224a4ed`. Den ble ikke flyttet eller endret. En separat detached worktree ble opprettet på den påkrevde revisjonen:

```sh
git -C CellProtocol worktree add --detach /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-wp-r2c-format-d224a4ed d224a4ed
git -C CellProtocol/_wt-wp-r2c-format-d224a4ed rev-parse HEAD
# d224a4ed2b6b6b384dff4b8942978bae9f56ade0
```

Begge kommandoer: exit 0. Den nye worktree-en er ren. Dette er et eksplisitt avvik fra den forespurte pakkestien, for å verifisere riktig commit uten å tilbakeføre eksisterende arbeid.

## Endringer — fil og linje

Alle stier i tabellen er relative til CellScaffold-worktree-en.

| Fil:linje | Endring |
|---|---|
| `Sources/App/Controllers/PortholeWebSessionSupport.swift:10` | Valgfrie `sourceCellEndpoint` og `mount`; eksisterende initialiseringskall virker fortsatt. |
| `Sources/App/Controllers/PortholeWebSessionSupport.swift:3195` | Velger kildegrenen før gammel dispatch; endpoint uten mount avvises. |
| `Sources/App/Controllers/PortholeWebSessionSupport.swift:3212` | Validerer rute, bruker resolver og uendret brukerrequester, utfører én kildehandling, bevarer autorisasjonsfeil, ingen vertsfallback. |
| `Sources/App/Controllers/PortholeWebSessionSupport.swift:3237` | Strukturert rutelogg med mount atskilt; ingen payload i loggen. |
| `Sources/ScaffoldKit/ComponentActionContext.swift:5` | Codable/Sendable metadata med instanceID/componentID/revision. |
| `Sources/ScaffoldKit/ComponentActionContext.swift:19` | Separat TaskLocal-kontekst tilgjengelig hos lokale kildeceller. |
| `Sources/App/Controllers/VaporBrowserhead.swift:396` | Monterte HTTP-handlinger bruker `authenticatedRequester`, ikke sesjonens/vertens requester. |
| `Sources/App/Controllers/VaporBrowserhead.swift:1620` | Den tidlige provider-register-snarveien får ikke fange monterte handlinger. |
| `Sources/App/Cells/interface/WebCellEmbeddings.swift:284` | Monterte WebSocket-handlinger avvises synlig; denne inngangen bruker fortsatt sesjonseieren. Webadapteren bruker HTTP. |
| `Sources/App/Cells/interface/WebCellEmbeddings.swift:337` | Socket-dekoderen får ikke strippe monteringsfelter og gjøre dem til vertshandlinger. |
| `Public/js/porthole-webo.js:3143` | Kildens feilfeedback behandles uten vertens spesialregler. |
| `Public/js/porthole-webo.js:8283` | Renderer-callback velger kildehandlingsløpet, også for dokumenthandlinger. |
| `Public/js/porthole-webo.js:8861` | Erstatter gammel generell avvisning med komplett rute; ugyldig metadata avvises fortsatt. |
| `Public/js/porthole-webo.js:8896` | HTTP-kildehandling med synlig feil; ingen bruk av resultatet som vertstilstand. |
| `Public/js/porthole-webo.js:9944` | Serialiserer `sourceCellEndpoint`/`mount` ved siden av uendret payload. |
| `Tests/AppTests/PortholeComponentSourceActionTests.swift:9` | Ti Swift-tester, virkelig resolver/GeneralCell, signerte Agreements, ulike bruker-/kildeeier-/vertseieridentiteter. |
| `Tests/AppTests/PortholeComponentSourceActionTests.swift:316` | Testeksekvering med større stack for uendret eldre Butler-konfigurasjonskode på macOS 15+. |
| `scripts/porthole-component-source-action.test.js:28` | Seks kjørte adapter-/transport-/feilfeedback-tester i Node VM. |
| `scripts/skeleton-wp-r2-contract.test.js:176` | WP-R2b-testen følger ny avtalt kontrakt: komplett kildeforespørsel tillates, manglende metadata avvises. |

## Swift-tester (a–f)

**Siste isolerte kjøring med midlertidig kompileringstilpasning: 10 tester, 0 feil, exit 0.** [Full logg](../evidence/wp-r2c-source-actions/swift-test-6-shim.log).
Dette er ikke et grønt bygg av leveringstilstanden uten tilpasningen.

| Krav | Testnavn (`PortholeComponentSourceActionTests`) | Linje |
|---|---|---|
| a | `testMountedActionReachesSourceEndpointNeverControlCell` | 88 |
| b | `testResolverAndSourceReceiveUsersOwnIdentity` | 99 |
| c | `testDeniedGrantReturnsVisibleForbiddenWithoutFallback` | 112 |
| d | `testUnresolvableEndpointReturnsVisibleErrorWithoutFallback` | 128 |
| e | `testUnmountedRequestRetainsLegacyControlCellDispatchAndCommandArgs` | 137 |
| e, referanser | `testUnmountedReferenceActionRetainsLegacyReferenceRouting` | 160 |
| f | `testMountReachesSourceSeparatelyWithoutChangingUserPayload` | 178 |
| Lesing | `testMountedReadUsesSourceAndPreservesMount` | 193 |
| Fail closed | `testMalformedRouteAndRemoteMetadataGapFailClosed` | 202 |
| Ingen vertsintercept | `testSourceCommandNamedLikeHostNavigationIsNotIntercepted` | 220 |

(c) tester faktisk avslag fra GeneralCell før source-interceptet og det vanlige 403-feilsvaret. HTTP-testene bruker en in-memory XCTVapor-rute med fastsatt requester og produksjonens dispatch/avslagsmapper; de er ikke et FIDO-innloggingstestløp. (b) sjekker både UUID og signeringsnøkkelfingeravtrykk hos resolver og kilde. Vertens tilsvarende handling har en gyldig signert grant i testen, slik at en utilsiktet fallback ville vært målbar. (f) sammenligner hele kanonisk JSON-payload, også brukerens egne felter kalt `instanceID`, `componentID`, `revision` og `mount`, mot den som faktisk når kildecellen. Testen kontrollerer også separat mount og at konteksten ryddes etter kallet.

## Eksakte kommandoer og utfall

Arbeidsmappe for Swift/Node, med mindre annet er oppgitt:

```sh
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919
export CELLPROTOCOL_LOCAL_PACKAGE_PATH=/tmp/wp-r2c-dependencies/CellProtocol
export CLANG_MODULE_CACHE_PATH=/tmp/wp-r2c-clang-cache
export SWIFTPM_MODULECACHE_OVERRIDE=/tmp/wp-r2c-swift-cache
swift build --disable-sandbox
swift test --disable-sandbox --filter PortholeComponentSourceActionTests
```

Dette er de nøyaktige build/test-kommandoene; stdout/stderr ble omdirigert til loggene under. Ingen ekstra build- eller testflagg ble brukt. De eksplisitte brukerkommandoene ble fulgt framfor AGENTS.md sin generelle bounded-runner-regel. `scripts/check_build_capacity.sh .` ble først kjørt, exit 0: 87,7 GiB ledig; skriptets gjeldende 5 %-grense passerte. Det var 8 % igjen etter skriptets 10 GiB-reserve, altså **ikke** den 10 %-grensen teksten i AGENTS.md beskrev.

Pakkelenkene ble opprettet lokalt fordi DiMy-pakkene krever identiteten `CellProtocol` og SwiftPM ikke tillater revision-pakkers avhengighet på lokale pakker:

```sh
mkdir -p /tmp/wp-r2c-dependencies
ln -s /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-wp-r2c-format-d224a4ed /tmp/wp-r2c-dependencies/CellProtocol
ln -s /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build/checkouts/DiMyMicropayments /tmp/wp-r2c-dependencies/DiMyMicropayments
ln -s /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build/checkouts/DiMyMint /tmp/wp-r2c-dependencies/DiMyMint
```

DiMy-checkoutene er de eksisterende manifestpinnene `cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0` og `ffdb0da85fc45be16926bfa5d335b247205f1b79`. Ingen avhengighetskilde ble endret.

Alle logger og `.exit`-filer ligger i [evidensmappen](../evidence/wp-r2c-source-actions/). [Maskinlesbar oversikt](../evidence/wp-r2c-source-actions/execution-results.json) inkluderer navn på feilende tester fra hver kjøring.

| Logg | Kommando/avvik fra miljøet over | Exit | Tester og utfall |
|---|---|---|---|
| `swift-build.log` | `swift build --disable-sandbox`; CP-sti var den nye worktree-ens absolutte sti, før symlenken | 1 | 0; SwiftPM: ukjent pakkenavn `CellProtocol` i DiMyMicropayments. |
| `swift-build-2.log` | Samme build, CP-symlenk opprettet, før DiMy-symlinkene | 1 | 0; SwiftPM: revision-avhengighet kan ikke avhenge av lokal pakke. |
| `swift-build-3.log` | Samme build, alle pakkelenker på plass | 1 | 0; egen kode: kastende JSON-serialisering i ikke-kastende logg-autoclosure. Rettet ved å beregne JSON før loggkallet. |
| `swift-build-4.log` | Samme build, rettet kode | 1 | 0; eksisterende ikke-uttømmende switcher i `ConferencePublicConfigurationPolicy.swift:51,114`. |
| `swift-build-5-shim.log` | Samme build + midlertidige stoppsaker for Tree/ComponentSurface i policyen | 0 | Bygg fullført. Ikke uendret policy. |
| `swift-test-1-shim.log` | `swift test --disable-sandbox --filter PortholeComponentSourceActionTests` + policytilpasning | 1 | 0; tvetydig `ChatCell` i `ConferenceEntityDiscoveryCellTests`. |
| `swift-test-2-shim.log` | Samme test + `App.ChatCell` i ovennevnte fil | 1 | 0; tvetydig `ChatCell` i `ConferenceShellCellsTests`. |
| `swift-test-3-shim.log` | Samme test + `App.ChatCell` også i shelltestene | 1 | 0; ikke-uttømmende switch i `ProductionSkeletonBindingIntegrityTests.swift:620`. |
| `swift-test-4-shim.log` | Samme test + komplett midlertidig evidenspatch | 1 | 8 startet, 7 fullført: 2 passerte, 5 feilet; stack-overflow/signal 10 under test 8. To tester ble ikke startet. Se navn nedenfor. |
| `swift-test-5-shim.log` | Samme test + korrekt signerte Agreements i fixture og større teststack | 1 | 10 kjørt, 2 feil i payload-sammenligning; se nedenfor. |
| `swift-test-6-shim.log` | Samme test + kanonisk JSON-sammenligning av payload | 0 | **10 kjørt, 0 feil, ingen hoppet over.** |
| `swift-build-final.log` | Samme build, alle midlertidige tilpasninger fjernet | 1 | Eksisterende policy-switcher mangler Tree/ComponentSurface. |
| `swift-test-final.log` | Samme test, alle midlertidige tilpasninger fjernet | 1 | **0 tester kjørt**; samme kompileringsfeil før teststart. Ingen testnavn feilet, fordi ingen test startet. |

Fem feilende testnavn i `swift-test-4-shim.log` var `testMountedActionReachesSourceEndpointNeverControlCell`, `testMountedReadUsesSourceAndPreservesMount`, `testMountReachesSourceSeparatelyWithoutChangingUserPayload`, `testResolverAndSourceReceiveUsersOwnIdentity` og `testSourceCommandNamedLikeHostNavigationIsNotIntercepted`. Årsaken var at testfixturen bare hadde grant-maler, ikke signerte Agreements. Tilgangskontrollen ble ikke svekket; fixturen oppretter nå signerte, avgrensede Agreements via kilde-/vertseieren. Testen som ble avbrutt av stack-overflow, var `testUnmountedReferenceActionRetainsLegacyReferenceRouting` ([diagnose](../evidence/wp-r2c-source-actions/stack-failure.txt)).

To feilende testnavn i `swift-test-5-shim.log` var `testMountReachesSourceSeparatelyWithoutChangingUserPayload` og `testUnmountedRequestRetainsLegacyControlCellDispatchAndCommandArgs`. `ValueType.==` returnerer ubetinget false for object/list (`CellProtocol/Sources/CellBase/ValueTypes/ValueType.swift:258`). Testene sammenligner nå alle payload-data som kanonisk JSON; ingen payload-assertion er fjernet.

JavaScript og øvrige kontroller:

```sh
node --check Public/js/porthole-webo.js
node --test scripts/porthole-component-source-action.test.js scripts/skeleton-wp-r2-contract.test.js
node --test scripts/porthole-component-source-action.test.js scripts/skeleton-wp-r2-contract.test.js scripts/porthole-arendalsuka-action-state.test.js
git diff --check
git diff --cached --check
```

| Kjøring | Exit | Utfall |
|---|---|---|
| `node --check` | 0 | Syntaks OK. |
| To fokuserte Node-filer, `node-focused-final.log` | 0 | **17 tester, 17 bestått, 0 feil.** |
| Tre Node-filer, `node-all-final.log` | 1 | 27 tester, 26 bestått; eksisterende `refresh, websocket, and heartbeat shell renders keep hostChanged at zero` feiler med `document.createElement is not a function`. |
| Samme eksisterende fil mot WP-R2b HEAD i `/tmp/wp-r2c-node-baseline`, `node-legacy-baseline.log` | 1 | 10 tester, 9 bestått; nøyaktig samme navngitte feil. |
| `git diff --check`, `git diff --cached --check` | 0 | Ingen whitespacefeil. |

Baselinekommandoen var `node --test /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/porthole-arendalsuka-action-state.test.js` fra `/tmp/wp-r2c-node-baseline`, hvor `Public/js/porthole-webo.js` var hentet med `git show HEAD:Public/js/porthole-webo.js` før denne commit-en.

Tidligere Node-kjøringer er også bevart: `node-source-actions.log` (5 tester, 2 feil på VM-array-prototyper; rettet med kanonisk sammenligning), `node-final.log` (26 tester, 2 feil: den kjente baselinefeilen og gammel forventning om at alle monterte handlinger måtte avvises), og `node-focused.log` (16/16 før en ekstra feilkonvoluttest ble lagt til). Den nye testens navn er `source rejection envelopes stay visible even for host navigation keypaths`.

## Navngitte resterende hull

1. **Mount over brotransport.** Ved `d224a4ed` har `Meddle` bare `get(keypath:requester:)` og `set(keypath:value:requester:)` (`Sources/CellBase/Protocols/CellProtocol.swift:50`). Ingen separat metadata i wire-kontrakten kan føre mount til en fjerncelle. Lokale `cell:///...` og `cell://localhost/...` bruker TaskLocal-konteksten. Fjernendepunkter avvises med 501 før resolveroppslag, og et lokalt oppslag som returnerer `BridgeBase` avvises også. WS/WSS er ikke godtatt som kildeendepunkt. Denne delen forblir fail closed, uten vertsfallback. En portabel metadata-/broendring i CellProtocol gjenstår; den er ikke sneket inn i denne CellScaffold-commit-en.
2. **Leveringstilstanden bygger ikke mot den krevde WP-R1-pinnen.** Policyen på linje 51/114 mangler de to nye enum-casene. Ved testkompilering kommer også de øvrige eksisterende feilene i tabellen fram. [Midlertidig patch](../evidence/wp-r2c-source-actions/test-only-build-shim.patch) gjorde bare disse uvedkommende delene kompilerbare; Tree/ComponentSurface-grenene stopper med `fatalError` hvis de brukes, og tvetydige klassenavn kvalifiseres. Alle fire filer ble gjenopprettet byte for byte før sluttbygg og commit. Patchen er **ikke** del av leveransen som kode. De ti grønne testene gir derfor avgrenset kildehandlingsbevis, ikke en generell grønn CellScaffold-build.

Ingen nettleser-/staging-/native-verifikasjon er påstått her. WP-R2b sitt separate T-F3-gap er ikke behandlet av denne jobben.
