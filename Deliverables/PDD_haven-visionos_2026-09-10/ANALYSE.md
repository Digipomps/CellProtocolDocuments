# HAVEN på Apple Vision — læring, analyse, hypoteser, tester og forslag

Oppgavemappe: `CellProtocolDocuments::Deliverables/PDD_haven-visionos_2026-09-10` · 2026-09-10 · Losen
Status: **fot i bakken før G1**. Dette dokumentet er grunnlaget for `FORMAALSSPEC.md`; det inneholder
ingen plan og ingen implementering. Alt som er lest er lest fra hovedtrærne på `kjetil-sin-m5-local`
denne økten (ikke `origin/main` — se `lesson.mount-is-not-git` og «Hovedtreet er ikke det som kjører»).

---

## 0. Formålet med oppgaven, målt mot hvert steg

Kjetils bestilling (ordrett i `FORMAALSSPEC.md` §0) har to lag:

1. **Vurdere** en Apple Vision-versjon av HAVEN-appen og **kartlegge** hva som trengs, inkludert
   endringer og tillegg i rammeverkene (CellProtocol, Binding, skeleton).
2. **Fire konkrete ideer** som vurderingen skal måles mot: (a) vilkårlig mange Portholes som egne
   vinduer, (b) baksiden av en flate viser datastrømmene som leveres til den, (c) verktøy og celler
   for å inspisere celler og trafikkinnhold, (d) et rom der alt informasjonspress mot brukeren er
   synlig og kan filtreres.

Metoden han ba om — definere formål, lære, analysere, hypoteser, teste, diskutere, foreslå — er
rekkefølgen i dette dokumentet. Hvert avsnitt sier hva det bidrar med til lag 1 eller lag 2.

Én presisering som styrer alt under: **tre av de fire ideene er ikke visionOS-ideer.** Flere
Portholes, baksiden og inspeksjonen er egenskaper ved Porthole og CellProtocol som i dag mangler
på alle plattformer. Vision Pro er stedet de blir *naturlige* (vinduer i rommet, snu et kort,
gå rundt en ting), men verdien ligger i dataene og cellene, og de kan bygges og testes på Mac
uten Vision Pro. Bare idé (d), rommet, er genuint romlig. Dette er analysens viktigste funn,
fordi det bestemmer rekkefølgen og senker risikoen: rammeverksendringene kan leveres og gi
nytte før én linje visionOS-kode skrives.

---

## 1. Læring — hva HAVEN-appen faktisk er i dag

Alle påstander her er `retrieved` (fil lest denne økten) med sti.

### 1.1 Appen, plattformer og byggoppsett

| Fakta | Kilde |
|---|---|
| HAVEN-appen er `Binding.xcodeproj`, scheme HAVEN, SwiftUI, én `WindowGroup { RootView() }`, `NSApplicationDelegateAdaptor` på macOS, `UIApplicationDelegateAdaptor` på iOS. Ingen adaptor for andre plattformer. | `Binding::Binding/BindingApp.swift` |
| `SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx"`, `TARGETED_DEVICE_FAMILY = "1,2"`, `IPHONEOS_DEPLOYMENT_TARGET = 18.0`, `MACOSX_DEPLOYMENT_TARGET = 26.1`, Debug-`SDKROOT = macosx26.2`. Rammeverk lenket fra iOS 26.2-SDK: MultipeerConnectivity, NearbyInteraction. | `Binding::Binding.xcodeproj/project.pbxproj` |
| Én lokal pakkeavhengighet: `../CellProtocol` (produktene CellBase og CellApple). | samme |
| `CellProtocol/Package.swift`: `platforms: [.macOS(.v13), .iOS(.v16), .tvOS(.v13)]`. visionOS er ikke listet; SwiftPM antar støtte med standard minimumsversjon for ulistede plattformer, så pakken blokkerer ikke i seg selv. `CellVapor` (Vapor) må aldri havne i app-målet. | `CellProtocol::Package.swift` |
| `Info.plist` har `UIBackgroundModes: remote-notification`, `NSBonjourServices _haven-radar`, URL-scheme `haven`, dokumenttype cellconfig. **Ingen `UIApplicationSupportsMultipleScenes`.** | `Binding::Binding/Info.plist` |
| Plattformlogikken er binær. `#if os(iOS) … #else` (37 treff i 10 filer) og `#if os(macOS) … #else` (44 treff i 15 filer) brukes om hverandre i app-kildene (Binding + Cells); 75 `#if os(`-steder i 20 filer, hvorav ContentView alene har 13 `os(iOS)` og 9 `os(macOS)`. På en tredje plattform er begge false, og appen faller i `#else`-grenen — som noen steder er iOS-stil og andre steder macOS-stil (f.eks. `personalCopilotShell` → split-shell, `portholeCanvasContentPadding` → 16, editor-panelene → overlays). | `Binding::Binding/ContentView.swift:737–800, 1120–1258` |
| `os(visionOS)` finnes allerede 7 steder, alle i kontaktimport. | `Binding::Binding/ContactSourceBridge.swift:203–421`, `Binding::Cells/EntityScaffoldExtensionCell.swift:770` |

### 1.2 Porthole — én celle, én konfigurasjon

| Fakta | Kilde |
|---|---|
| `cell:///Porthole` registreres som `OrchestratorCell` med `cellScope: .identityUnique`, `persistency: .persistant`, domene `private`. Kommentaren forklarer hvorfor identitetsunik (ikke scaffold-unik). | `Binding::Binding/BootstrapView.swift:399–420` |
| `OrchestratorCell` holder **én** `cellConfiguration`. `loadCellConfiguration` gjør `detachAll` og laster den nye; feiler den, rulles forrige tilbake. Absorberte celler = `cellReferences` (attach med label). Historikk og outward-menyer er lister av konfigurasjoner, ikke flere aktive. | `CellProtocol::Sources/CellApple/Cells/OrchestratorCell.swift:21–56, 423–444` |
| `CellResolver.loadCell(from:into:)` kobler referansene i to faser (parallell prefetch av fjernreferanser, sekvensiell innkobling) — det er «absorberingen». | `CellProtocol::Sources/CellBase/Cells/CellResolver/CellResolver.swift:926–967` |
| Cellescopene er `.template` (ny celle per resolve via `createCell`), `.scaffoldUnique`, `.identityUnique`. Template-celler kan adresseres med uuid etterpå. | `CellResolver.swift:1811–1850, 2470–2540` |
| Appen har **to** view-modeller mot samme celle: `PortholeBindingViewModel` (kanonisk, brukes av `PortholeCanvas`) og `PortholeViewModel` («legacy», CellApple). Begge holder de siste 10 `FlowElement`s (`flowLimit = 10`). | `CellProtocol::Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/PortholeBindingViewModel.swift`, `…/Utility Views/PortholeViewModel.swift:126–167` |
| Skeleton-relative keypaths er hardkodet til `cell:///Porthole` som base i rendereren (11 steder) og i modellen (5 steder). Dokumentert som utsatt arbeid: «fully generic relative references … CellProtocol needs a renderer-level change». | `…/Suggestion/SkeletonView.swift:367–478, 1169, 1934, 1964, 3681, 3969`; `Binding::Documentation/Porthole-and-skeleton.md` |

### 1.3 Datastrømmene bak en flate — det som finnes

| Begrep i Kjetils tekst | Hva det er i koden | Kilde |
|---|---|---|
| «hvilke celler Porthole absorberer» | `CellReference(endpoint, label, subscribeFeed, subscriptions, setKeysAndValues)` i `CellConfiguration.cellReferences`; `Absorb.attach(emitter:label:)`; tilkoblingsstatus via `attachedStatuses`. | `CellProtocol::Sources/CellBase/CellConfiguration/CellConfiguration.swift:120–150`, `CellBase/Protocols/CellProtocol.swift` |
| «hvilke Flows det er abonnert på» | `subscribeFeed` + `subscriptions` per referanse; `Absorb.absorbFlow(label:)`; `GeneralAuditor` holder abonnementene. | samme; `CellBase/Cells/GeneralCell/Cast/GeneralAuditor.swift:176–330` |
| «indikasjon når det kommer flowelements» | `Emit.flow(requester:) -> AnyPublisher<FlowElement>`; `FlowElement(title, topic, content, properties(type: event/alert/content/reference, contentType), origin)`; signert `FlowEnvelope` finnes som struct. | `CellBase/FeedItem/FlowElement.swift`, `CellBase/Flow/FlowEnvelope.swift` |
| «det vises når det kjøres set / get» | Hvert `get`/`set` kaller `CellResolver.logAction(...)`, som **bare skriver en tekstlinje** `INTR:<action>:<keypath>:<source>:<target>:<identity>:<ts>` via `CellBase.diagnosticLog(domain: .flow)`. Det finnes en `diagnosticLogHandler`-krok, men ingen strukturert hendelse, ingen utfall, ingen varighet. | `CellBase/Cells/GeneralCell/GeneralCell.swift:1556–1560, 1691–1697`; `CellResolver.swift:3000–3011`; `CellBase/Cells/CellBase.swift:97–150` |
| Signert bevis per handling | `EffectReceipt` / `ActionDecisionReceipt` med `ReceiptSignature` finnes og brukes av WebFetch og PurposeBoundAIGateway; Agent Trust Package bygger etterprøvingsdiff på dem. | `CellBase/Agreement/EffectReceipt.swift`; `CellProtocolDocuments::Book/36_Agent_Trust_Package.md` §7–8 |

### 1.4 Inspeksjonsceller som allerede finnes

| Celle | Gjør | Gjør ikke | Kilde |
|---|---|---|---|
| `FlowProbeCell` | Abonnerer på en målcelles flow, filtrerer (topics/origin/title/limit), lagrer observasjoner i en trace (historikk 20), sender egne `flowProbe.started/stopped`-hendelser. Grant `flowProbe rw--`. | **Videresender ikke** målcellens elementer. Er en sidelytter, ikke et ledd i kjeden. | `CellBase/Cells/Diagnostics/FlowProbeCell.swift:400–470, 713` |
| `StateSnapshotCell` | Tar øyeblikksbilde av navngitte keys på en målcelle (`get` per key, ok/error per item). | Ingen strøm; ingen set-observasjon. | `CellBase/Cells/Diagnostics/StateSnapshotCell.swift` |
| `EntityAtlasInspectorCell` | Inspiserer entitetsatlas (formål, celle-ID). | Ikke trafikk. | `CellBase/Cells/Commons/EntityAtlasInspectorCell.swift` |
| `GeneralCell.intercepts` | Én feed-intercept per celle (`FlowElementIntercept` som kan returnere elementet = videresende, endre det, eller `nil` = stoppe) + get/set-intercepts per key/keypath. **Dette er mekanismen en videresendende tapp-celle bygges av** — `OrchestratorCell` bruker den allerede slik («default: return flowElement»). | `CellBase/Cells/GeneralCell/Cast/Intercepts.swift`; `OrchestratorCell.swift:88–128` |
| `BindingRuntimeDiagnostics` / `BindingDiagnosticsPanel` | Validerer bindinger i en konfigurasjon, viser diagnoseposter (macOS-panel, iOS-sheet). | Ingen live trafikk. | `Binding::Binding/Debug/BindingRuntimeDiagnostics.swift:490–622` |

### 1.5 Skeleton-formatet og rendereren

| Fakta | Kilde |
|---|---|
| Skeleton er en 2D-deklarativ DSL (Text, TextField, Image, Spacer, H/VStack, List, Picker, Object, Reference, Button, Divider, ScrollView, Section, ZStack, Grid, Toggle, Visualization) med modifiers (padding, farger som hex, `styleRole`, `motionHint`, `presentation` for overlay/drawer/sheet/popover/modal). Ingen romlige begreper. | `CellProtocolDocuments::Book/12_Skeleton_Spec.md` §2–3 |
| Den kanoniske Apple-rendereren er `SkeletonView.swift` (4 535 linjer). Den er ren SwiftUI; plattformgrenene er `#if os(iOS)` (tastatur-hjelpere), `#if os(macOS)` (drag-and-drop, rich markdown via NSTextView, pil-navigasjon) — alle med nøytral `#else`. Ingen visionOS-blokker funnet ved lesing. | `…/Suggestion/SkeletonView.swift:9–13, 68–130, 1488, 1588–1660, 3403, 3751, 4024–4171` |
| `SkeletonParityRenderer` er `#if canImport(SwiftUI) && canImport(ImageIO) && (os(macOS) \|\| os(iOS))` — paritetsrendring finnes ikke for visionOS. | `…/Skeleton/SkeletonParityRenderer.swift:4` |
| Lokale flater bruker hex-bakgrunner i stor stil: 148 `background = "#…"` i app-kildene (125 i katalogen), mot 37 `styleRole`. På visionOS er standardbakgrunnen glass; en hvit `#FFFFFF`-flate ser ut som et fremmedelement. | `grep` over `Binding::Binding/*.swift`, `Binding::Cells/ConfigurationCatalogCell.swift` |

### 1.6 Kompileringsblokkere funnet uten å bygge

| Funn | Konsekvens | Kilde |
|---|---|---|
| `#if canImport(UIKit) let impactGenerator = UIImpactFeedbackGenerator(style: .medium)` | `canImport(UIKit)` er sant på visionOS, men klassen finnes bare for iOS/iPadOS/Catalyst (Apple-dok). **Kompileringsfeil** i CellApple. | `CellProtocol::Sources/CellApple/EntityRadar/ScannerService.swift:266–267`; developer.apple.com/documentation/uikit/uiimpactfeedbackgenerator |
| `NearbyInteraction` er `#if os(iOS)`-gated (ok), men rammeverket finnes ikke i visionOS-SDK. | Ingen kompileringsfeil; **nærhetspresisjon i EntityRadar bortfaller** på Vision Pro. MultipeerConnectivity finnes. | `ScannerService.swift:13–17, 162–165`; developer.apple.com/documentation/visionos/bringing-your-app-to-visionos (tabell over utilgjengelige rammeverk) |
| `UIApplicationDelegateAdaptor` bare `#if os(iOS)` | På visionOS ingen app-delegate → ingen push-registrering, ingen `didReceiveRemoteNotification`. Må bli `os(iOS) \|\| os(visionOS)`. | `Binding::Binding/BindingApp.swift:16–21`; `BindingAppNotifications.swift:741` |
| `UIDevice.current.identifierForVendor`, `UIApplication.shared.registerForRemoteNotifications`, `beginBackgroundTask`, `UIPasteboard`, `UIDocumentPickerViewController`, `CNContactPickerViewController` | Alle finnes på visionOS; bare gate-endring. | `NotificationEnrollmentManager.swift:57–163`, `BackgroundTaskCoordinator.swift`, `ContactSourceBridge.swift` |
| `SkeletonEditorFloatingPanelsController` bruker `NSPanel` (macOS) og overlays (iOS). | På visionOS: egne vinduer (`openWindow`) eller ornaments — se forslag. | `Binding::Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` |

### 1.7 visionOS — det som gjelder i september 2026

Alle rader er `retrieved` fra Apple denne økten (URL i kilde).

| Fakta | Kilde |
|---|---|
| Apple Vision Pro selges nå med M5, 16 GB, 90–120 Hz, **visionOS 26** forhåndsinstallert. visionOS 27 er i beta (WWDC26, sesjon 287). Tilgjengelighet i Norge er **ikke verifisert**. | apple.com/apple-vision-pro/specs; developer.apple.com/videos/play/wwdc2026/287 |
| Scenetyper: `WindowGroup` (2D-vindu med glass), `WindowGroup … .windowStyle(.volumetric)` (volum, fast skala, størrelse i meter), `ImmersiveSpace` med `immersionStyle` `.mixed` / `.progressive` / `.full`. | developer.apple.com/documentation/visionos/presenting-windows-and-spaces; …/positioning-and-sizing-windows; …/creating-fully-immersive-experiences |
| Flere vinduer krever `UIApplicationSupportsMultipleScenes = true`; ellers ignorerer SwiftUI `openWindow` og logger runtime-feil. Flere instanser av samme `WindowGroup` åpnes med `openWindow(value:)` og `WindowGroup(for: ID.self)`. | …/presenting-windows-and-spaces; …/creating-a-new-swiftui-window-in-visionos |
| Appen kan **ikke** plassere vinduer absolutt. Første vindu legges der brukeren ser; nye vinduer foran eksisterende, forskjøvet. `defaultWindowPlacement` gir relativ plassering (`.trailing(window)` osv.). Etter visning kan appen ikke flytte eller skalere vinduet. Standardvindu 1280×720 pt, ca. 2 m foran, «apparent width» ca. 3 m. Dynamisk skala holder vinduer like store uansett avstand; volumer har fast skala. | …/positioning-and-sizing-windows; HIG «Windows» (visionOS) |
| **Bare ett `ImmersiveSpace` om gangen**; alle appens vinduer kan vises sammen med det; andre appers vinduer skjules mens det er åpent. Siste scene kan ikke lukkes programmatisk. | …/presenting-windows-and-spaces |
| HIG: «Avoid displaying too many windows. Too many windows can obscure people's surroundings, making them feel overwhelmed, constricted, and even uncomfortable. It can also make it cumbersome for people to relocate an app because it means moving a lot of windows.» Interaktive elementer minst 60 pt mellom sentre. Unngå hode-ankring; anker i rommet. Unngå dybde på tekst. | HIG «Spatial layout» (visionOS) |
| HIG: ornaments «float in a plane parallel to its associated window and slightly in front of it», følger vinduet, brukes til hyppige kontroller; toolbar/tab bar blir ornaments automatisk. | HIG «Ornaments» |
| HIG: «Prefer launching your app or game in the Shared Space or using the mixed immersion style»; «Reserve immersion for meaningful moments»; i `mixed` gjør systemet innhold halvgjennomsiktig nær fysiske objekter; 1,5 m-grense i progressive/full. | HIG «Immersive experiences» |
| visionOS 26 (nå): `depthAlignment`, `rotation3DLayout`, presentasjoner (alert/sheet/popover) inne i volumer, `.defaultLaunchBehavior(.suppressed)`, `.restorationBehavior(.disabled)`, `.manipulable()`, `ManipulationComponent`, `ViewAttachmentComponent` (SwiftUI-visninger som komponenter i RealityKit), `GestureComponent`, observerbare entiteter, `MeshInstancesComponent` (1 000+ objekter), spatial audio per vindu/volum, `RemoteImmersiveSpace` (render på Mac, vis på Vision Pro), «Nearby Window Sharing», Foundation Models, SpeechAnalyzer, look-to-scroll. | developer.apple.com/videos/play/wwdc2025/317 |
| visionOS 27 (beta): fysisk rombelysning, projektive teksturer, klessimulering, Gaussian splats, egendefinert spatial-tilbehør, Spatial Preview-rammeverk på macOS, Foveated Streaming. Ingenting nytt om vindusmodellen er nevnt i sesjonen. | developer.apple.com/videos/play/wwdc2026/287; developer.apple.com/visionos/whats-new |
| Alternativ vei: en iPad-app kan kjøre **uendret** som «compatible app» på Vision Pro (lenket mot iOS-SDK, iPad-utseende i ett vindu). Ingen glass, ingen volumer, ingen ImmersiveSpace, `NearbyInteraction` gjør ingenting. | developer.apple.com/documentation/visionos/determining-whether-to-bring-your-app-to-visionos |
| Rammeverk som oppfører seg annerledes: Core Haptics spiller lyd i stedet for haptikk; Core Location bare «When in Use»; systemdialoger (autorisasjon, Sign in with Apple) kjører asynkront utenfor prosessen; LocalAuthentication via `LAContext` (Optic ID); maks to samtidige «touch»-punkter. | samme |

Én ting er **recalled, ikke verifisert**: hvordan baksiden av et visionOS-vindu ser ut når man går
rundt det (jeg husker det som en frostet glassflate uten innhold). Ingen del av forslagene hviler
på det — «baksiden» er designet som en eksplisitt handling, ikke som en fysisk rundtur.

---

## 2. Analyse — hva ideene egentlig krever

### 2.1 Idé (a): «så mange Portholes man vil, som egne vinduer»

Kravet består av tre lag som må skilles:

1. **Cellelaget.** Én identitetsunik `cell:///Porthole` med én konfigurasjon gjør flere flater
   umulig uansett vert. To macOS-vinduer i dag lager hver sin `PortholeBindingViewModel` mot samme
   celle: laster du en konfigurasjon i det ene, endres cellen for begge, mens det andre vinduets
   `currentSkeleton` bare oppdateres om flowen bærer et skeleton-objekt. Tilstanden kan altså
   sprike. Det er ikke en visionOS-sak; det er en Porthole-sak.
2. **Adresseringslaget.** Skeletons adresserer absorberte celler som `cell:///Porthole/<label>…`
   eller relativt med Porthole som implisitt base (11 hardkodede steder i rendereren). Med N
   Portholes må «base» være *den Portholen som rendrer skeletonet* — akkurat den «container base
   context» som `Porthole-and-skeleton.md` allerede har utsatt. Uten dette vil to Portholes som
   begge har label `chat` treffe hverandre.
3. **Vertslaget.** SwiftUI gir flere vinduer per `WindowGroup(for: PortholeID.self)` på macOS og
   visionOS, og på iPadOS med multiscene. Vinduet bærer bare en ID; cellen bærer alt annet
   (konfigurasjon, referanser, historikk). Da overlever et vindu at appen restartes, og et
   Porthole kan flyttes mellom enheter uten å miste tilstand — fordi tilstanden er en persistert celle.

Diskusjon av alternativene for laget 1:

| Alternativ | For | Mot |
|---|---|---|
| **A. Porthole som template-celle + register.** `cell:///Porthole` blir en identitetsunik *register-celle* («Porthole-havnen») som lister åpne instanser; hver instans er en `OrchestratorCell` med `.template`-scope adressert med uuid (eller `cell:///Porthole/<navn>`), egen konfigurasjon og persistens. | Følger Kjetils regel «skal innholdet deles, skal det være en celle»: en Porthole-instans kan deles, tappes, inspiseres og gis grants som egen enhet. Ingen ny abstraksjon: scope-mekanismen finnes (`createCell`). Registeret gir «gjenopprett alle vinduene». | Migrering: dagens persisterte `CellConfiguration.json` i Porthole-katalogen må bli «instans 0». Rendererens base må gjøres eksplisitt (lag 2) — uansett nødvendig. |
| B. Sesjoner inne i én Porthole (`sessions[id].configuration`). | Ingen ny celleregistrering. | Bryter celle-som-delingsenhet; grants og tapper kan ikke skille sesjonene; `detachAll` og `loadCell(into:)` opererer på cellen, ikke på en sesjon — hele absorberingen må skrives om. Forkastes. |
| C. Flere vinduer mot samme Porthole (dagens macOS). | Null arbeid. | Er ikke «flere Portholes»; tilstanden spriker (se over). |

Konklusjon: **A**, med lag 2 som forutsetning. Dette er den største rammeverksendringen i
oppdraget og den eneste som rører CellProtocol-semantikk. Den er plattformuavhengig.

HIG-forbeholdet må tas på alvor: «avoid displaying too many windows». Kjetils ønske om «så mange
man vil» og Apples råd står ikke mot hverandre hvis verten gir *samling*: en «Porthole-kø» (dock
som ornament eller et lite volum) der åpne instanser ligger som kort, og hvor man tar ett kort ut
i rommet av gangen. Da er «mange» et faktum i cellelaget, og «få synlige» et valg i vertslaget.

### 2.2 Idé (b): baksiden viser datastrømmene

Det Kjetil vil se finnes nesten helt allerede — men i fire ulike former: referansene i
konfigurasjonen (struktur), abonnementene i auditoren (tilstand), flowElements i view-modellen
(de siste 10) og set/get som *tekstlinjer* i diagnoseloggen. Baksiden trenger én ting rammeverket
ikke har: **en strukturert hendelsesstrøm per celle** — `get`/`set`/`attach`/`detach`/`absorb`/
`flow inn`/`flow ut`/admission — med keypath, requester, utfall, varighet og sekvensnummer.
`logAction` bærer allerede nesten hele tuppelen som tekst; å strukturere den én gang gir:

- baksiden (live),
- inspektøren (historikk),
- tappcellen (opptak),
- rom-visningen (aggregat),
- og på sikt Agent Trust Package-auditen, som i dag bare har signerte kvitteringer fra to
  celletyper (`webFetch.receipts`, `ai.receipts`) og ellers ingen observasjon av hva agenter gjorde.

Viktig avgrensning: hendelsesstrømmen skal **ikke** gå gjennom cellens egen `flow` (da ville
inspeksjonen forurense det brukerne abonnerer på, og en celle som observerer seg selv gir sløyfer).
Den skal være en egen eier-skopet kanal med grant, og den skal ikke inneholde payload — bare
metadata; payload leses via tappcellen når eieren ber om det.

Ærlighetsregel fra lærdomsregisteret (`lesson.empty-list-must-not-look-like-calm`): en
abonnert flow som er *stille* må se annerledes ut enn en som er *uleselig* (grant nektet, bro
nede, timeout). Hver rad på baksiden har alltid tilstand `lest / uleselig / stille / ikke koblet`
med årsak. En rolig bakside skal bety at alt faktisk er lest.

Og: baksiden er ikke visionOS-spesifikk. På Mac og iPad er den et kort som snus
(`rotation3DEffect`); på Vision Pro kan den være et ekte bakstykke i et volum. Det gjør at
baksiden kan bygges, testes og godkjennes med Porthole-preview på Mac først.

### 2.3 Idé (c): inspisere celler og trafikkinnhold — også som celler

Kjetils formulering («går f.eks. an å sette inn en celle som bare videresender FlowElements, men
fanger data om innhold og trafikk») beskriver nøyaktig en *videresendende tapp*. `FlowProbeCell`
er en sidelytter og videresender ikke; `OrchestratorCell` viser derimot at feed-intercepten kan
returnere elementet uendret. En `FlowTap`-celle er dermed liten: GeneralCell som absorberer én
kilde under label `source`, registrerer en feed-intercept som (1) noterer metadata
(topic, type, contentType, origin, bytes, tidspunkt, sekvens), (2) valgfritt lagrer innholdet,
(3) returnerer elementet uendret; og som proxy-er `get`/`set` til kilden med samme notering.
Den settes inn i kjeden i `CellConfiguration`:

```
Porthole ──absorb──▶ cell:///FlowTap (label: chat, setKeysAndValues: tap.source = cell://…/ChatCell)
                        └──absorb──▶ ChatCell
```

Fordi tappen er en celle, får den alt celler har: grant-mal (bare eier kan lese opptak),
persistens (opptaket er entitetsdata: inspiserbart og slettbart), et `Explore`-manifest
(inspektøren kan oppdage den), og den kan deles med en agent (Kallimachos kan analysere et
opptak uten å få live-tilgang). Den kan også bli en **ventil**: samme intercept kan slippe
gjennom, dempe (rate), eller stoppe etter tema — det er mekanismen bak idé (d).

Sikkerhetsanalysen (må inn som antiformål): en tapp gir aldri mer enn kilden ville gitt
requesteren; formål er ikke rettighet (`lesson.purpose-never-grants-rights`); opptak av innhold
er av («metadata only») som standard (`purpose://self-determination.data.exercisability`:
beskyttende standardvalg); og kryptert innhold tappes som bytes, ikke klartekst, med mindre
eieren holder nøkkelen og slår det på.

### 2.4 Idé (d): rommet med informasjonspress

Dette er den eneste genuint romlige ideen, og Kjetil merket den selv som «kanskje mer gøy enn
nyttig». Argumentanalysen sier: den blir nyttig i nøyaktig den grad *justeringen virker*. Å se
partikler fly fra Butler, Correspondence, Palazzo og Kallimachos mot seg er en visualisering; å
skru ned Palazzo til «bare bestillinger» og få det til å *gjelde* er brukerkontroll
(`purpose://human-agency`, `purpose://preference.owner-controlled`). Derfor knyttes rommet til
ventilene i 2.3: rommet er baksiden av *alle* Portholes samtidig, og hver kilde har en ventil
som er en celle med persistert innstilling.

Teknisk plassering: `ImmersiveSpace` med `.mixed` (HIG: foretrukket), `RealityView`, kilder som
kropper ankret i rommet (ikke hodet), strømmer som `MeshInstancesComponent`-partikler (1 000+
objekter er innenfor), ventiler som `ViewAttachmentComponent`-paneler ved hver kilde. Bare ett
immersivt rom om gangen — greit, dette er ett rom. Samme aggregat bør ha en 2D-fallback
(«trykkpanel») på Mac/iPad, ellers kan det ikke testes uten Vision Pro.

Ærlig vurdering av nytte: den første målbare nytten er *ikke* romlig. Aggregatet — «hva treffer
meg, fra hvem, hvor ofte» — er verdifullt som liste. Rommet er verdifullt hvis det får folk til å
faktisk justere. Det bør derfor testes som hypotese (H11 under), ikke antas.

### 2.5 Selve porten til visionOS

Utenom de fire ideene er det tre veier:

| Vei | Hva du får | Kostnad | Passer HAVEN? |
|---|---|---|---|
| **0. Compatible iPad-app** | HAVEN som iPad-vindu på Vision Pro, uendret. | Nesten null (App Store-flagg). | Nyttig som *øyeblikkelig* test av at runtime, bro og celler virker på enheten — men ingen glass, ingen flere vinduer, ingen rom. Bør gjøres først som eksperiment, ikke som mål. |
| **1. Nativt mål, 2D** | Glass, ornaments, flere vinduer, TabView-sidefelt, hover for gaze. | Legge til destinasjon, rette blokkere (1.6), innføre kapabilitetsakse, multiscene-nøkkel, glass-sikre stiler. | Ja — dette er det som gjør flere Portholes til vinduer i rommet. |
| **2. Nativt mål, romlig** | Volumer (Porthole-kø, ekte bakside), ImmersiveSpace (rommet). | Vei 1 + RealityKit-innhold. | Ja, for idé (a-samling), (b-volum) og (d). |

Den binære plattformmodellen er den skjulte kostnaden. `|| os(visionOS)` 75 steder gir en app
som er iOS noen steder og macOS andre steder. Riktig endring er en **kapabilitetsakse**: verten
sier hva den kan (`multiWindow`, `floatingPanels`, `ornaments`, `haptics`, `nearbyPrecision`,
`keyboardToolbar`, `immersive`), og ContentView spør om kapabiliteter, ikke om OS. Det er
testbart (en test kan kjøre ContentView-logikken med visionOS-kapabiliteter på Mac) og det holder
`SkeletonPortabilityRequirement` intakt: rendereren rendrer kontrakten, verten tilpasser bare
sin egen krom.

Glass-problemet: 148 hex-bakgrunner i lokale flater mot 37 `styleRole`. På glass ser
`#FFFFFF`-kort ut som papirlapper på et vindu. Løsningen er ikke å endre skeleton-formatet, men
en **vertsregel**: på visionOS mappes `styleRole` (card, page, primary…) til systemmaterialer,
og rå hex-bakgrunner beholdes bare når `styleRole` mangler — pluss en lint som teller dem. Dette
henger sammen med paritetsarbeidet (`PDD_skeleton-render-paritet_2026-09-07`), som allerede fant
at `styleRole` bærer flatene.

---

## 3. Hypoteser og tester

| # | Hypotese | Test | Resultat denne økten | Status |
|---|---|---|---|---|
| H1 | CellBase, CellApple og Binding kompilerer for `xros` etter få, lokale rettelser (< 10 steder). | Legg til Apple Vision-destinasjon i en ren worktree, bygg `-destination 'platform=visionOS Simulator'`, tell feil per fil. | **Ikke kjørt.** `device_bash` var nede hele økten (4 identiske feil), Codex-MCP har 60 s-tak, og bygget må skje på Mac-en. Lesing fant én sikker feil (`UIImpactFeedbackGenerator`) + prosjektinnstillinger. Jobb ligger klar i `handoff/queue-ready/` (se §5). | **blocked** — krever Kjetils ja |
| H2 | Flere Portholes er umulig i dag uten CellProtocol-endring. | Les registrering, `OrchestratorCell.loadCellConfiguration`, view-modellene. | Bekreftet: identitetsunik, én konfigurasjon, `detachAll` ved last (1.2). | **grønn** (retrieved) |
| H2b | Template-scope gir ny celle per resolve og kan adresseres med uuid etterpå. | Les `CellResolver` scope-switch. | Bekreftet (`case .template: createCell`; uuid-oppslag mot minne/persistens). | **grønn** |
| H3 | Skeleton-relativ adressering hardkoder `cell:///Porthole` og bryter med N Portholes. | `grep "cell:///Porthole"` i renderer og modell. | 11 treff i `SkeletonView.swift`, 5 i `SkeletonDescription.swift`, 3 i ContentView; dokumentert som utsatt arbeid. | **grønn** |
| H4 | Dataene til baksiden finnes allerede i appen. | Spor hver av de fire strømmene til kilde. | Tre av fire finnes strukturert; set/get finnes bare som tekstlinje uten utfall/varighet. | **delvis grønn** → formål «strukturerte hendelser» |
| H5 | `FlowProbeCell` videresender ikke. | Les `sink`-håndteringen. | Bekreftet: `record(flowElement:)`, ingen `pushFlowElement` av kildens elementer. Feed-intercept i GeneralCell kan videresende (OrchestratorCell gjør det). | **grønn** |
| H6 | visionOS tillater mange vinduer og ett immersivt rom, men ikke absolutt plassering; HIG fraråder mange vinduer. | Apple-dok og HIG. | Bekreftet (1.7). | **grønn** (retrieved) |
| H7 | Lokale flater har mange hex-bakgrunner som vil se feil ut på glass. | Tell `background = "#…"` mot `styleRole`. | 148 mot 37. | **grønn** |
| H8 | Simulatoren holder til vindus-/volum-/rom-layout, men ikke til blikk/hånd-komfort og ekte glass-lesbarhet; G3-GUI trenger enhet. | HIG (dynamisk skala, feltet, 60 pt-avstand) + Apple: «The system doesn't provide information about a person's field of view». | Sannsynliggjort; endelig svar krever enhet. | **åpen** — spørsmål til Kjetil |
| H9 | Baksiden og inspektøren kan leveres og godkjennes på Mac uten Vision Pro. | Argument: alle data er plattformnøytrale; flipp finnes i SwiftUI overalt. | Holder; eneste visionOS-spesifikke del er volum-bakstykket. | **grønn** (argument) |
| H10 | To macOS-vinduer i dag viser samme Porthole og kan sprike. | Les `PortholeBindingViewModel.load` og flow-håndteringen. | Bekreftet: `load` setter `currentSkeleton` lokalt og laster cellen; andre vindu oppdateres bare via flow-objekter med skeleton. | **grønn** |
| H11 | Rom-visningen er nyttig bare hvis ventilene virker. | Måles etter bygging: andel økter der en ventil justeres etter at rommet er åpnet, og om justeringen faktisk endrer trafikken (tapp-tall før/etter). | Ikke testbar før ventiler finnes. | **venter** |
| H12 | Kjetil har (eller får) en Vision Pro; visionOS-simulatoren er installert i Xcode 26.2 på maskinen. | Spør; `xcodebuild -showsdks`. | Ukjent; `SDKROOT macosx26.2` tyder på Xcode 26.2, men visionOS-SDK er et eget nedlastbart komponent. | **åpen** |

Hva som **ikke virket** i undersøkelsen (dokumentert så det ikke gjentas):

- `device_bash` feilet identisk fire ganger («failed in the device workspace»); jeg sluttet å prøve
  etter fjerde og gikk over til `device_list_dir` + `device_stage_files`. Det virket for alle
  ~200 filer.
- Filsystem-MCP-ene `haven-gui-exchange` / `haven-conference-exchange` avviser alle kall med
  «invalid outputSchema (draft-07)». Ikke brukbare fra denne økten.
- `device_list_dir recursive` stopper på dybde 5 (`depthCapped`) og **skjulte** mappen
  `…/Skeleton/Suggestion/` der `SkeletonView.swift` og `PortholeBindingViewModel.swift` ligger.
  Jeg lette i 20 minutter etter en klasse som «ikke fantes». List dype mapper eksplisitt.
- `WebSearch` returnerte serverfeil på alle forsøk; Apples dokumentasjon lot seg hente som
  `.md`-varianter (`…/documentation/<sti>.md`) og HIG som `/tutorials/data/design/…/<side>.json`.

---

## 4. Forslag — godt argumentert, ikke planlagt

Hvert forslag sier hvilket formål det tjener, hva det koster, og hva som taler mot.

### F1. Kapabilitetsakse i stedet for OS-grener (tjener: `platform.visionos-native`, alle senere verter)

Innfør `HavenHostCapabilities` (struct/miljøverdi) som verten fyller ut ved oppstart; ContentView
spør `capabilities.multiWindow`, `.floatingPanels`, `.ornaments`, `.haptics`, `.nearbyPrecision`,
`.keyboardToolbar`, `.immersive`. OS-grener beholdes bare der API-et faktisk er plattformspesifikt
(importer, delegate-adaptorer). **For:** én sannhet, testbar på Mac med visionOS-profil,
fjerner «hvilken `#else` er jeg i». **Mot:** berører mange linjer i én stor fil (ContentView er
9 109 linjer); bør gjøres som ren refaktor med paritetsbilder før/etter. **Ordre:** først, fordi
alt annet på visionOS treffer den.

### F2. Porthole-instanser + havn (tjener: `many-portholes`)

`cell:///Porthole` → register-celle (identitetsunik, persisterer listen over instanser, deres
konfigurasjon-uuid og vindustilstand); `cell:///PortholeInstance` → template-celle
(`OrchestratorCell` som i dag, én per åpen flate). Rendereren får eksplisitt base-kontekst
(Environment `skeletonContainerBase`) som erstatter de 11+5 hardkodede stedene, med
bakoverkompatibilitet: mangler base, brukes instans 0. **For:** følger celle-regelen; gjør
«gjenopprett vinduene» og «flytt en flate til en annen enhet» til celleoperasjoner. **Mot:** det
er den dyreste endringen (CellProtocol + renderer + Binding), og den må ha migrering av dagens
persisterte Porthole-katalog. **Ordre:** etter F3/F4, fordi baksiden og tappen gir nytte uansett
og fordi F2 er lettere å teste når tappen finnes.

### F3. Strukturerte samhandlingshendelser (tjener: `backside`, `traffic-inspection`, Trust Package)

`CellInteractionEvent {seq, at, cell, kind: get|set|attach|detach|absorb|flowIn|flowOut|admission,
keypath?, label?, requester, outcome: ok|denied(reason)|error, durationMs?, bytes?}` publisert på
en eier-skopet observasjonskanal per celle (ny `Emit`-tilleggsprotokoll `Observed` med
`observe(requester:) -> AnyPublisher<CellInteractionEvent>`), gated på grant `observe r---`.
`CellResolver.logAction` blir én av sinkene (teksten beholdes). **For:** én kilde for fire
flater; ingen payload → lav risiko; gir Trust Package den observasjonen den mangler.
**Mot:** ytelse på travle celler — må ha «drop when no observer» og sekvensnummer så tap
er synlig, ikke stille. **Ordre:** først av rammeverksendringene; liten og plattformnøytral.

### F4. `FlowTap`-celle: videresendende tapp med opptak, som også kan være ventil (tjener: `traffic-inspection`, `pressure.valves`)

Som beskrevet i 2.3. Kontrakt (pkg.std.cell-contract): `tap.source` (set, eier), `tap.record.mode`
= `off | metadata | content` (default `metadata`), `tap.retention` (antall/tid), `tap.valve` =
`pass | mute | throttle(n/min) | allowTopics([...])`, `tap.recording` (get, eier), `tap.clear`
(set, eier). Negativ test: ikke-eier får `deniedNoGrant` på `tap.recording`. **For:** liten,
gjenbruker intercept-mekanismen, blir bruksklar i Porthole-konfigurasjoner uten kodeendring i
Porthole. **Mot:** en tapp i kjeden er et ekstra hopp (latens) og et ekstra sted for feil; må
være transparent (`origin` bevares, `FlowEnvelope`-signatur urørt).

### F5. Baksiden som flipp (tjener: `backside`)

Én `PortholeBacksideView` med fire soner: *Absorbert* (label → endepunkt, tilstand, agreement),
*Abonnert* (flows/topics per referanse), *Puls* (de siste hendelsene, én prikk per FlowElement
med label/topic, tidslinje siste 60 s), *set/get* (keypath, requester, utfall, ms). Hver rad
har tilstand `lest/uleselig/stille/ikke koblet` med årsak. På Mac/iPad: `rotation3DEffect` om
y-aksen, utløst av en knapp i redigeringsmodus («Bakside»). På visionOS: samme, pluss
valgfritt som ekte bakstykke i et volum. **For:** nyttig i dag for 46-sekunders-jakten og
bro-feilsøking; bygges og godkjennes med Porthole-preview på Mac. **Mot:** ingen — utover at den
er avhengig av F3 for set/get-sonen (de tre andre sonene kan bygges uten).

### F6. Inspektør-vindu (tjener: `traffic-inspection.inspect-surface`)

Eget vindu (`WindowGroup(id: "inspector", for: CellEndpoint.self)`) med: Explore (keys/typer
fra `ExploreManifest`), Snapshot (`StateSnapshotCell`), Live (F3-strøm + tapp-opptak),
Kjede-diagram (Porthole → Tap → Kilde) og «Ta opp»/«Slett opptak». På visionOS åpnes det ved
siden av Portholen med `defaultWindowPlacement(.trailing(porthole))`. **For:** samler tre
eksisterende celler i én flate. **Mot:** enda en flate i sidemeny-enumen (kjent gjeld:
`haven_surface_registry_gap`) — bør ikke legges i menyen, men åpnes fra baksiden.

### F7. Nativt visionOS-mål i to steg (tjener: `platform.visionos-native`)

Steg 0 (dag 1): compatible iPad-app på enhet/simulator for å se at runtime, vault, bro og
celler virker. Steg 1: Apple Vision-destinasjon, rett 1.6-blokkerne, `UIApplicationSupportsMultipleScenes`,
`WindowGroup(for: PortholeID.self)` når F2 finnes (før det: ett vindu), sidemeny som `TabView`
(blir ornament automatisk), editorpaneler som egne vinduer, `styleRole`→materiale-regel
(F8). Steg 2: volum for Porthole-kø og bakside; ImmersiveSpace for rommet (F9).
**Mot:** paritetsverktøyet (`SkeletonParityRenderer`) finnes ikke for visionOS; enten utvides
det, eller paritet for visionOS måles med skjermbilder fra simulator (`xcrun simctl io
screenshot`) mot Mac-referansen.

### F8. Glass-sikre stiler (tjener: `platform.visionos-native`, paritet)

Vertsregel + lint: `styleRole` mappes til systemmaterialer på visionOS; rå hex-bakgrunn
beholdes bare uten `styleRole`, og telles. Ingen endring i skeleton-formatet. **Mot:** flatene
vil se litt annerledes ut på Vision Pro enn i web — det er riktig (HIG: behold glass), men
paritetsdefinisjonen må få et «nivå 2»-unntak for materiale, slik `PDD_skeleton-render-paritet`
allerede skiller nivåer.

### F9. Rommet med ventiler (tjener: `information-pressure.room`)

`ImmersiveSpace(id: "pressure").immersionStyle(.mixed)`; `RealityView` med kilder som kuler
ankret i rommet i en halvsirkel foran brukeren (HIG: innenfor synsfeltet, ikke hode-ankret),
partikler fra kilde mot en «meg»-ring, tetthet = rate siste minutt, farge = type
(event/alert/content/reference), størrelse = bytes. Ved hver kilde en `ViewAttachmentComponent`
med ventilen (F4): pass/mute/throttle/tema. 2D-fallback «Trykkpanel» på Mac/iPad med samme
aggregat. **For:** gjør brukerkontroll fysisk. **Mot:** «gøy før nyttig» — bygges sist, og
H11 avgjør om det blir mer enn en demo.

### Foreslått rekkefølge (ikke en plan; grunnlag for G2 senere)

F3 → F4 → F5 (alle på Mac, ingen Vision Pro) → F1 → F7 steg 0–1 → F2 → F6 → F8 → F7 steg 2 → F9.
Begrunnelse: nytten kommer først der den er billigst og plattformnøytral; visionOS-koden
skrives når rammeverket har det den trenger; det dyreste (F2) gjøres når tappen kan bevise at
instansene oppfører seg.

Forslag til organisering: **dette er én formålsspesifikasjon med fem grener** (§1 i
FORMAALSSPEC). Ved G2 blir hver gren sin egen PDD-mappe med egen plan, slik at
`lesson.plan-instead-of-delivery` ikke slår til på en mappe som er for stor til å levere.

---

## 5. Det som ligger klart, men ikke er kjørt

- `handoff/queue-ready/visionos-h1-compile-probe.job` + `.prompt.md`: Codex-jobb som lager en
  ren worktree, legger til `xros xrsimulator` i `SUPPORTED_PLATFORMS`, bygger CellApple og HAVEN
  mot visionOS-simulator og skriver feiltellingen per fil til `TESTRESULT.md#h1`. Tørrkjøring
  som standard. **Kjøres ikke før Kjetil sier ja** (se §6 i FORMAALSSPEC), fordi han ba om fot i
  bakken før implementering, og fordi et bygg låser Xcode-maskinen i noen minutter.
- Mockups i `images/` (se FORMAALSSPEC §3): fire scener, rendret fra `mockups/haven-visionos-mockups.html`
  med Chromium. De er **mockups, ikke Porthole-preview** (lesson
  `scaffold-without-porthole-host-has-no-preview`): dagens skeleton kan ikke rendre vinduer i
  rom, flipp, partikler eller ventiler — bare innholdet *i* flatene.
