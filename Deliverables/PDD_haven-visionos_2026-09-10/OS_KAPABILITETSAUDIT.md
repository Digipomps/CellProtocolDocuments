# OS- og kapabilitetsaudit — hvilket OS bygges det for, og hvor sjekkene blir feil

Oppgavemappe: `CellProtocolDocuments::Deliverables/PDD_haven-visionos_2026-09-10` · 2026-09-10 · Losen
Bestilling (Kjetil, ordrett): «VI må teste det i simulator inntil videre. Bruk litt tid på å rygge opp i
hvilket os det bygges for slik at ikke os og kapabilitetssjekker blir feil.»

## 0. Formålet, og hvordan hvert avsnitt måles mot det

Formålet er at **en betingelse i koden skal svare riktig på alle verter appen bygges for** — Mac,
iPhone, iPad, visionOS-simulator nå, Vision Pro senere. En sjekk «blir feil» på to måter:

1. **Den sier feil om API-et** — koden kompilerer ikke, eller et API som finnes blir utestengt.
2. **Den sier feil om verten** — et UX-valg (paneler, avstander, materiale, menyer) er skrevet som
   «er dette iOS?» i stedet for «hva kan denne verten?», og en tredje vert faller i en tilfeldig gren.

§1 sier hvilket OS det faktisk bygges for i dag (og for simulator). §2 gir regelen som skiller de to
feiltypene. §3 er auditen: hvert eneste `#if`-sted med OS-innhold i Binding og CellApple, klassifisert.
§4 er listen over det som blir feil på visionOS. §5 er kapabilitetskontrakten som gjør regelen
håndhevbar, med tester og lint. §6 sier hva som ikke er sjekket.

Alt i §1 og §3 er `retrieved` — lest fra filene denne økten, med `Repo::sti:linje`. To Apple-fakta i §1
er merket der de er `recalled`.

## 1. Hvilket OS det bygges for — byggmatrisen

Kilde: `Binding::Binding.xcodeproj/project.pbxproj:425,534–553`, `Binding::Binding/Info.plist`,
`CellProtocol::Package.swift`.

| | macOS (i dag) | iPhone (i dag) | iPad (i dag) | visionOS-simulator (foreslått) |
|---|---|---|---|---|
| `SUPPORTED_PLATFORMS` | `macosx` | `iphoneos iphonesimulator` | samme | **må legges til:** `xros xrsimulator` |
| SDK | macosx26.2 (Debug `SDKROOT`) | iOS 26.2 (rammeverksstier i pbxproj) | samme | xrsimulator 26.x — **ikke verifisert installert** (Xcode-komponent) |
| Deployment target | 26.1 | 18.0 | 18.0 | **forslag 26.0** (`XROS_DEPLOYMENT_TARGET`); begrunnelse under |
| `TARGETED_DEVICE_FAMILY` | — | 1 | 2 | **7 må legges til** |
| Destinasjon (`xcodebuild`) | `platform=macOS,arch=arm64` (`Scripts/build_binding.sh`) | `platform=iOS Simulator,…` (`.vision-preview/run-ios18.sh`) | samme | `platform=visionOS Simulator,name=Apple Vision Pro` |
| Scene-manifest | — | generert (`INFOPLIST_KEY_UIApplicationSceneManifest_Generation[sdk=iphoneos*]`) | samme | **`UIApplicationSupportsMultipleScenes = YES` mangler** — uten den ignoreres `openWindow` |
| Delegate | `NSApplicationDelegateAdaptor` | `UIApplicationDelegateAdaptor` | samme | **ingen** (`os(iOS)`-gate) — push og URL-mottak faller bort |
| `targetEnvironment(simulator)` | false | false/true | false/true | **true** → Keychain uten `SecAccessControl` (`CellApple.swift:96`, `IdentityVault.swift:688,1408`) — riktig automatisk |
| Biometri | Touch ID | Face ID | Touch/Face ID | Optic ID på enhet; i simulator *simulert* — `recalled`: simulatoren har «Enrolled»-bryter |
| Haptikk | nei | ja | nei/ja | nei (Core Haptics spiller lyd; `UIImpactFeedbackGenerator` finnes ikke) |
| NearbyInteraction | nei | ja (UWB) | nei | nei (rammeverket finnes ikke i SDK-en) |
| MultipeerConnectivity | ja | ja | ja | ja (simulator går via Mac-ens nettverk; Bonjour `_haven-radar` i Info.plist) |
| Push | — | ekte token | ekte token | simulator: ingen ekte token (`recalled`: simulert push via `.apns`-fil) |
| Speech / mikrofon | ja | ja | ja | ja på enhet (Apple: sjekk `SFSpeechRecognizer`); simulator: Mac-ens mikrofon |
| Compatible iPad-app («Designed for iPad») | — | — | — | kan kjøres i visionOS-simulatoren som steg 0, uendret |

**Hvorfor 26.0 som deployment target:** Vision Pro (M2 og M5) kjører begge visionOS 26, så 26.0
utelukker ingen maskinvare — bare brukere som ikke har oppdatert. Til gjengjeld får vi
`.restorationBehavior`, `.defaultLaunchBehavior`, presentasjoner i volumer, `depthAlignment`,
`ViewAttachmentComponent` og `MeshInstancesComponent` uten `#available`-grener (WWDC25-listen i
`ANALYSE.md` §1.7). Alternativet 2.0 gir ingenting igjen for prisen.

## 2. Regelen som skiller riktige og gale sjekker

| Klasse | Hva | Riktig form | Feil form |
|---|---|---|---|
| **A · API-gate** | Koden bruker et API som bare finnes på én plattform (NSPanel, launchctl, NearbyInteraction, NSTextView) | `#if canImport(Rammeverk)` — rammeverket avgjør om koden kompilerer. `os(...)` bare når to plattformer deler rammeverk men ikke API (NearbyInteraction er iOS-only *inne i* iOS-SDK-familien) | `#if os(iOS) … #else <AppKit-kode>` — «alt som ikke er iOS er Mac» er feil så snart en tredje vert finnes |
| **B · vertsvalg** | Et UX-valg: paneler eller overlays, avstander, materiale, sheet-størrelse, menytype | `HavenHostCapabilities` (§5) — én profil per vert, avledet ett sted | `#if os(macOS)` rundt et layoutvalg |
| **C · feil på visionOS** | En A- eller B-sjekk som gir kompileringsfeil eller stenger ute et API som finnes | Rettes til A- eller B-form | — |
| **D · simulator-gate** | Simulator-feil (Keychain-tilgangskontroll) | `#if targetEnvironment(simulator)` | brukt til UX |

Tommelregel: **`os()` for API, kapabilitet for UX, `targetEnvironment` for simulatorfeil.** Og:
en `#else`-gren skal aldri inneholde AppKit- eller UIKit-kode; den skal være nøytral.

Mønsterfiler som allerede gjør det riktig: `Binding::Binding/ContactSourceBridge.swift` (visionOS
med i alle gater), `Binding::Binding/BindingExternalURLOpener.swift` (`canImport` + nøytral
`#else`), `Binding::Cells/AgentProvisioningCell.swift:289` (`supportsLocalAgentRuntime` — et
kapabilitetsflagg), `CellProtocol::Sources/CellApple/EntityRadar/ScannerService.swift:162`
(`platformSupportsNearbyPrecision`).

## 3. Auditen — alle 159 OS-avhengige `#if`-steder i Binding og CellApple

Grunnlag: 259 `#if`/`#elseif`-direktiver funnet i `Binding/Binding`, `Binding/Cells`,
`CellProtocol/Sources/CellApple` og `CellProtocol/Sources/CellBase`; 100 er plattformnøytrale
(`DEBUG`, `canImport(Combine)`, `canImport(EventKit)`, `canImport(FoundationModels)` …) og står
ikke i tabellen. De 159 under nevner `os(…)`, `canImport(UIKit/AppKit)`, `targetEnvironment` eller
visionOS-relevante rammeverk.

Fordeling: **A 103 · B 26 · C 27 · D 3.** Av de 27 C-stedene er 3 kompileringsfeil og 24 falske
negativer (API-et finnes på visionOS, men sjekken stenger det ute).

| Fil | Linje | Direktiv | Klasse | Utfall på visionOS i dag | Foreslått form |
|---|---|---|---|---|---|
| `Binding/BackgroundTaskCoordinator.swift` | 3 | `#if os(iOS)` | C · feil på visionOS | UIKit importeres ikke → `beginBackgroundTask` faller bort selv om det finnes på visionOS | `#if canImport(UIKit)` |
| `Binding/BindingApp.swift` | 10 | `#if os(macOS)` | A · API-gate | AppKit-kommandoer og NSApplicationDelegate finnes ikke; riktig at de faller bort | uendret |
| `Binding/BindingApp.swift` | 16 | `#if os(iOS)` | C · feil på visionOS | Ingen `UIApplicationDelegateAdaptor` → ingen push-registrering, ingen `didReceiveRemoteNotification` | `#if os(iOS) \|\| os(visionOS)` |
| `Binding/BindingApp.swift` | 19 | `#if os(macOS)` | A · API-gate | AppKit-kommandoer og NSApplicationDelegate finnes ikke; riktig at de faller bort | uendret |
| `Binding/BindingApp.swift` | 27 | `#if os(macOS)` | B · vertsvalg → kapabilitet | `restorationBehavior(.disabled)` gjelder bare macOS; på visionOS beholdes gjenoppretting (ønsket for Porthole-instanser) | kapabilitet `windowRestoration` (mac: av, vision: på) |
| `Binding/BindingApp.swift` | 30 | `#if os(macOS)` | A · API-gate | AppKit-kommandoer og NSApplicationDelegate finnes ikke; riktig at de faller bort | uendret |
| `Binding/BindingApp.swift` | 38 | `#if os(macOS)` | A · API-gate | AppKit-kommandoer og NSApplicationDelegate finnes ikke; riktig at de faller bort | uendret |
| `Binding/BindingAppNotifications.swift` | 237 | `#if canImport(AppKit)` | A · API-gate | Faller i scene-ID-grenen (UIKit-vert) — riktig | uendret (vindusidentitet: windowNumber på AppKit, sceneID ellers) |
| `Binding/BindingAppNotifications.swift` | 301 | `#if canImport(AppKit)` | A · API-gate | Faller i scene-ID-grenen (UIKit-vert) — riktig | uendret (vindusidentitet: windowNumber på AppKit, sceneID ellers) |
| `Binding/BindingAppNotifications.swift` | 741 | `#if os(iOS)` | C · feil på visionOS | `BindingAppDelegate` kompileres ikke → push-mottak mangler | `#if os(iOS) \|\| os(visionOS)` |
| `Binding/BindingExternalURLOpener.swift` | 23 | `#if canImport(UIKit)` | A · API-gate | UIKit-grenen; `UIApplication.open` finnes | uendret (mønsterfil: canImport, ikke os) |
| `Binding/BindingExternalURLOpener.swift` | 26 | `#if canImport(AppKit)` | A · API-gate | UIKit-grenen; `UIApplication.open` finnes | uendret (mønsterfil: canImport, ikke os) |
| `Binding/BindingExternalURLOpener.swift` | 47 | `#if canImport(UIKit) && !os(watchOS)` | A · API-gate | UIKit-grenen; `UIApplication.open` finnes | uendret (mønsterfil: canImport, ikke os) |
| `Binding/BindingExternalURLOpener.swift` | 54 | `#elseif canImport(AppKit)` | A · API-gate | UIKit-grenen; `UIApplication.open` finnes | uendret (mønsterfil: canImport, ikke os) |
| `Binding/BindingMacAppDelegate.swift` | 3 | `#if os(macOS)` | A · API-gate | Faller bort — riktig | uendret |
| `Binding/BindingVoiceInputTranscriber.swift` | 52 | `#if (os(iOS) || os(macOS)) && canImport(Speech) && canImport(AVFoundation)` | C · feil på visionOS | Hele transkribenten byttes ut med stubben «unavailable» selv om Speech og AVFoundation finnes på visionOS (Apple: sjekk `SFSpeechRecognizer`) | `#if canImport(Speech) && canImport(AVFoundation)` (dropp os-delen) |
| `Binding/BindingVoiceInputTranscriber.swift` | 278 | `#if os(iOS)` | C · feil på visionOS | `AVAudioSession` konfigureres ikke → opptak uten aktiv økt | `#if canImport(UIKit)` (AVAudioSession finnes på iOS/tvOS/visionOS, ikke macOS) |
| `Binding/BindingVoiceInputTranscriber.swift` | 286 | `#if os(iOS)` | C · feil på visionOS | `AVAudioSession` konfigureres ikke → opptak uten aktiv økt | `#if canImport(UIKit)` (AVAudioSession finnes på iOS/tvOS/visionOS, ikke macOS) |
| `Binding/CellConfigurationEndpointRetargeting.swift` | 147 | `#if os(macOS)` | A · API-gate | macOS-sandkassebokmerke og getpwuid faller bort; NSHomeDirectory brukes — riktig | uendret |
| `Binding/CellConfigurationEndpointRetargeting.swift` | 191 | `#if os(macOS)` | A · API-gate | macOS-sandkassebokmerke og getpwuid faller bort; NSHomeDirectory brukes — riktig | uendret |
| `Binding/ChatWorkbenchParityCells.swift` | 587 | `#if os(macOS)` | A · API-gate | NSHomeDirectory-grenen — riktig | uendret |
| `Binding/ConferenceNearbyRadarSurfaceView.swift` | 828 | `#if canImport(UIKit)` | B · vertsvalg → kapabilitet | Kompilerer (UIKit-gren), men `secondarySystemBackground` på glass ser ut som papir | kapabilitet `surfaceMaterial` (glass → .clear/material) |
| `Binding/ConferenceNearbyRadarSurfaceView.swift` | 830 | `#elseif canImport(AppKit)` | B · vertsvalg → kapabilitet | Kompilerer (UIKit-gren), men `secondarySystemBackground` på glass ser ut som papir | kapabilitet `surfaceMaterial` (glass → .clear/material) |
| `Binding/ContactSourceBridge.swift` | 22 | `#if canImport(ContactsUI)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 25 | `#if canImport(UIKit)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 28 | `#if canImport(AppKit)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 203 | `#if os(iOS) || os(visionOS)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 213 | `#if (os(iOS) || os(visionOS)) && canImport(ContactsUI)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 268 | `#if os(macOS)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 281 | `#elseif os(iOS) || os(visionOS)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 330 | `#if os(iOS) || os(visionOS)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 395 | `#if (os(iOS) || os(visionOS)) && canImport(ContactsUI)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContactSourceBridge.swift` | 421 | `#if os(iOS) || os(visionOS)` | A · API-gate | Allerede visionOS-bevisst; pickere finnes | uendret (mønsterfil) |
| `Binding/ContentView.swift` | 12 | `#if canImport(UIKit)` | A · API-gate | UIKit importeres — riktig | uendret |
| `Binding/ContentView.swift` | 14 | `#elseif canImport(AppKit)` | A · API-gate | UIKit importeres — riktig | uendret |
| `Binding/ContentView.swift` | 466 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 479 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 532 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 737 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Editorpaneler blir overlays inne i vinduet (iOS-stil); på visionOS bør de være egne vinduer/ornaments | kapabilitet `editorPanels: floating \| windows \| overlay` |
| `Binding/ContentView.swift` | 763 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Editorpaneler blir overlays inne i vinduet (iOS-stil); på visionOS bør de være egne vinduer/ornaments | kapabilitet `editorPanels: floating \| windows \| overlay` |
| `Binding/ContentView.swift` | 774 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Diagnosepanelet blir sheet (iOS-stil) — akseptabelt | kapabilitet `diagnosticsPresentation: panel \| sheet` |
| `Binding/ContentView.swift` | 793 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Editorpaneler blir overlays inne i vinduet (iOS-stil); på visionOS bør de være egne vinduer/ornaments | kapabilitet `editorPanels: floating \| windows \| overlay` |
| `Binding/ContentView.swift` | 978 | `#if os(iOS)` | C · feil på visionOS | Minnevarsel abonneres ikke; `didReceiveMemoryWarningNotification` finnes på visionOS | `#if canImport(UIKit)` |
| `Binding/ContentView.swift` | 1033 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Sheet får detents (iOS-stil) i stedet for minstestørrelse — ok | kapabilitet `sheetSizing` |
| `Binding/ContentView.swift` | 1051 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Diagnosepanelet blir sheet (iOS-stil) — akseptabelt | kapabilitet `diagnosticsPresentation: panel \| sheet` |
| `Binding/ContentView.swift` | 1120 | `#if os(iOS)` | B · vertsvalg → kapabilitet | `compact` = false → split-shell — riktig for visionOS | kapabilitet `compactChrome` (fra størrelsesklasse, ikke OS) |
| `Binding/ContentView.swift` | 1158 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusleser faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 1195 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 1203 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 1248 | `#if os(iOS)` | B · vertsvalg → kapabilitet | `compact` = false → split-shell — riktig for visionOS | kapabilitet `compactChrome` (fra størrelsesklasse, ikke OS) |
| `Binding/ContentView.swift` | 1418 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 1426 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 1434 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 1687 | `#if os(iOS)` | C · feil på visionOS | **Kompileringsfeil**: `#else`-grenen kaller `Color(nsColor:)` som ikke finnes uten AppKit | `#if canImport(UIKit) … #elseif canImport(AppKit)`; på visionOS `.clear` (glass) |
| `Binding/ContentView.swift` | 1695 | `#if os(iOS)` | C · feil på visionOS | **Kompileringsfeil**: `#else`-grenen kaller `Color(nsColor:)` som ikke finnes uten AppKit | `#if canImport(UIKit) … #elseif canImport(AppKit)`; på visionOS `.clear` (glass) |
| `Binding/ContentView.swift` | 1703 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Desktop-avstander (16/18/24/12 pt); HIG vil ha ≥ 60 pt mellom mål på visionOS | kapabilitet `spacingProfile: compact \| regular \| spatial` |
| `Binding/ContentView.swift` | 2014 | `#if os(iOS)` | B · vertsvalg → kapabilitet | Label med tekst (regular) — riktig | kapabilitet `compactChrome` |
| `Binding/ContentView.swift` | 2173 | `#if os(macOS)` | B · vertsvalg → kapabilitet | `usesPerspectiveDrivenEdgeMenus = true` (iOS-atferd) — produktvalg, ikke OS-faktum | kapabilitet `edgeMenus` |
| `Binding/ContentView.swift` | 2972 | `#if os(iOS)` | B · vertsvalg → kapabilitet | `compact` = false → split-shell — riktig for visionOS | kapabilitet `compactChrome` (fra størrelsesklasse, ikke OS) |
| `Binding/ContentView.swift` | 3439 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 3567 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Editorpaneler blir overlays inne i vinduet (iOS-stil); på visionOS bør de være egne vinduer/ornaments | kapabilitet `editorPanels: floating \| windows \| overlay` |
| `Binding/ContentView.swift` | 4812 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 4959 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 6686 | `#if canImport(UIKit)` | A · API-gate | UIPasteboard finnes — riktig | uendret |
| `Binding/ContentView.swift` | 6689 | `#elseif canImport(AppKit)` | A · API-gate | UIPasteboard finnes — riktig | uendret |
| `Binding/ContentView.swift` | 6822 | `#if !canImport(AppKit)` | A · API-gate | No-op fokus — riktig | uendret |
| `Binding/ContentView.swift` | 6829 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 8168 | `#if canImport(AppKit)` | A · API-gate | Vindusautomasjon (AppKit) faller bort — riktig | uendret |
| `Binding/ContentView.swift` | 8475 | `#if canImport(UIKit)` | B · vertsvalg → kapabilitet | `UIColor.systemBackground` som canvas-bunn — mørk plate på glass | kapabilitet `surfaceMaterial` |
| `Binding/ContentView.swift` | 8477 | `#elseif canImport(AppKit)` | B · vertsvalg → kapabilitet | `UIColor.systemBackground` som canvas-bunn — mørk plate på glass | kapabilitet `surfaceMaterial` |
| `Binding/ContentView.swift` | 8772 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Sheet får detents (iOS-stil) i stedet for minstestørrelse — ok | kapabilitet `sheetSizing` |
| `Binding/Debug/BindingRuntimeDiagnostics.swift` | 770 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Full bredde (sheet-stil) — ok | kapabilitet `diagnosticsPresentation` |
| `Binding/EdgeMenus.swift` | 618 | `#if os(macOS)` | A · API-gate | `onExitCommand`/`onMoveCommand` finnes ikke — faller bort (tastaturnavigasjon i menyer mangler) | uendret; vurder `.focusable` + `onKeyPress` (iOS 17/visionOS 1) |
| `Binding/EdgeMenus.swift` | 632 | `#if os(macOS)` | A · API-gate | `onExitCommand`/`onMoveCommand` finnes ikke — faller bort (tastaturnavigasjon i menyer mangler) | uendret; vurder `.focusable` + `onKeyPress` (iOS 17/visionOS 1) |
| `Binding/FullLibraryView.swift` | 537 | `#if os(macOS)` | B · vertsvalg → kapabilitet | Ingen minstestørrelse — visionOS klemmer via `windowResizability` | kapabilitet `windowSizing` |
| `Binding/NotificationCallbackClient.swift` | 3 | `#if os(iOS)` | C · feil på visionOS | Fjernvarsel-håndtering kompileres ikke; `UIBackgroundFetchResult` finnes på visionOS | `#if os(iOS) \|\| os(visionOS)` |
| `Binding/NotificationCallbackClient.swift` | 28 | `#if os(iOS)` | C · feil på visionOS | Fjernvarsel-håndtering kompileres ikke; `UIBackgroundFetchResult` finnes på visionOS | `#if os(iOS) \|\| os(visionOS)` |
| `Binding/NotificationEnrollmentManager.swift` | 5 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 56 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 78 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 105 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 126 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 139 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/NotificationEnrollmentManager.swift` | 384 | `#if os(iOS)` | C · feil på visionOS | Ingen push-autorisasjon/registrering; `identifierForVendor` byttes med tilfeldig UUID per start (ny enhet hver gang) | `#if canImport(UIKit)` (alle API-ene finnes på visionOS) |
| `Binding/PortableSurfaceSupport.swift` | 4 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort — riktig | uendret |
| `Binding/PortableSurfaceSupport.swift` | 392 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort — riktig | uendret |
| `Binding/RootView.swift` | 20 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort; sceneID-grenen — riktig | uendret |
| `Binding/RootView.swift` | 26 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort; sceneID-grenen — riktig | uendret |
| `Binding/RootView.swift` | 73 | `#if os(iOS)` | C · feil på visionOS | `onOpenURL` registreres ikke → `haven://`-lenker døde på visionOS | `#if os(iOS) \|\| os(visionOS)` |
| `Binding/RootView.swift` | 87 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort; sceneID-grenen — riktig | uendret |
| `Binding/RootView.swift` | 115 | `#if canImport(AppKit)` | A · API-gate | AppKit-vindusnummer faller bort; sceneID-grenen — riktig | uendret |
| `Binding/RootView.swift` | 185 | `#if os(iOS)` | C · feil på visionOS | **Kompileringsfeil**: `Color(nsColor:)` i `#else` | `canImport`-par; `.clear` på visionOS |
| `Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` | 3 | `#if os(macOS)` | A · API-gate | NSPanel faller bort; kontrolleren blir tom — men vertsvalget bør bli eksplisitt | A i dag; B: `editorPanels` velger NSPanel / openWindow / overlay |
| `Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` | 9 | `#if os(macOS)` | A · API-gate | NSPanel faller bort; kontrolleren blir tom — men vertsvalget bør bli eksplisitt | A i dag; B: `editorPanels` velger NSPanel / openWindow / overlay |
| `Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` | 26 | `#if os(macOS)` | A · API-gate | NSPanel faller bort; kontrolleren blir tom — men vertsvalget bør bli eksplisitt | A i dag; B: `editorPanels` velger NSPanel / openWindow / overlay |
| `Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` | 36 | `#if os(macOS)` | A · API-gate | NSPanel faller bort; kontrolleren blir tom — men vertsvalget bør bli eksplisitt | A i dag; B: `editorPanels` velger NSPanel / openWindow / overlay |
| `Binding/SkeletonEditor/SkeletonEditorFloatingPanelsController.swift` | 46 | `#if os(macOS)` | A · API-gate | NSPanel faller bort; kontrolleren blir tom — men vertsvalget bør bli eksplisitt | A i dag; B: `editorPanels` velger NSPanel / openWindow / overlay |
| `Binding/SkeletonPresentationOverlayView.swift` | 982 | `#if os(macOS)` | A · API-gate | `onExitCommand` faller bort — riktig | uendret |
| `Cells/AgentEnrollmentCell.swift` | 6 | `#if os(macOS)` | A · API-gate | macOS-runtime-tilgang faller bort — riktig | uendret |
| `Cells/AgentEnrollmentCell.swift` | 1079 | `#if os(macOS)` | A · API-gate | macOS-runtime-tilgang faller bort — riktig | uendret |
| `Cells/AgentProvisioningCell.swift` | 5 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 290 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 776 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 1224 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 1234 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 1262 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 2382 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 2390 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 2401 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 2426 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/AgentProvisioningCell.swift` | 2479 | `#if os(macOS)` | A · API-gate | `supportsLocalAgentRuntime = false`; launchctl/Process faller bort — riktig og allerede kapabilitetsformet | uendret (mønster: `supportsLocalAgentRuntime`) |
| `Cells/EntityScaffoldExtensionCell.swift` | 766 | `#if os(iOS)` | A · API-gate | Rapporterer «visionOS» — riktig | uendret |
| `Cells/EntityScaffoldExtensionCell.swift` | 768 | `#elseif os(macOS)` | A · API-gate | Rapporterer «visionOS» — riktig | uendret |
| `Cells/EntityScaffoldExtensionCell.swift` | 770 | `#elseif os(visionOS)` | A · API-gate | Rapporterer «visionOS» — riktig | uendret |
| `Sources/CellApple/CellApple.swift` | 96 | `#if targetEnvironment(simulator)` | D · simulator-gate | Gjelder også xrsimulator (ingen SecAccessControl i simulator) — riktig | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonParityRenderer.swift` | 4 | `#if canImport(SwiftUI) && canImport(ImageIO) && (os(macOS) || os(iOS))` | C · feil på visionOS | Paritetsrendereren finnes ikke på visionOS selv om `ImageRenderer` finnes | `#if canImport(SwiftUI) && canImport(ImageIO) && !os(watchOS)` |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 9 | `#if canImport(UIKit)` | A · API-gate | UIKit importeres — riktig | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 12 | `#if os(macOS)` | A · API-gate | UIKit importeres — riktig | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 68 | `#if os(iOS)` | C · feil på visionOS | Tastaturhjelpere (skjul tastatur, `scrollDismissesKeyboard`, tastaturverktøylinje) faller bort; alle finnes på visionOS (virtuelt/fysisk tastatur) | `#if canImport(UIKit)`; verktøylinjen som kapabilitet `keyboardToolbar` |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 101 | `#if os(iOS)` | C · feil på visionOS | Tastaturhjelpere (skjul tastatur, `scrollDismissesKeyboard`, tastaturverktøylinje) faller bort; alle finnes på visionOS (virtuelt/fysisk tastatur) | `#if canImport(UIKit)`; verktøylinjen som kapabilitet `keyboardToolbar` |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 111 | `#if os(iOS)` | C · feil på visionOS | Tastaturhjelpere (skjul tastatur, `scrollDismissesKeyboard`, tastaturverktøylinje) faller bort; alle finnes på visionOS (virtuelt/fysisk tastatur) | `#if canImport(UIKit)`; verktøylinjen som kapabilitet `keyboardToolbar` |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 1488 | `#if os(macOS)` | C · feil på visionOS | Fil-drop (`onDrop`) slås av; visionOS støtter drag-and-drop mellom vinduer | kapabilitet `fileDrop` (mac + vision + iPad: på) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 1588 | `#if os(macOS)` | C · feil på visionOS | Fil-drop (`onDrop`) slås av; visionOS støtter drag-and-drop mellom vinduer | kapabilitet `fileDrop` (mac + vision + iPad: på) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 3403 | `#if os(macOS)` | A · API-gate | `onExitCommand` faller bort — riktig | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 3751 | `#if os(macOS)` | A · API-gate | Rich markdown (NSTextView) → vanlig editor — riktig i dag | A; senere kapabilitet `richTextEditor` (UITextView-variant) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 3811 | `#if os(macOS)` | A · API-gate | Rich markdown (NSTextView) → vanlig editor — riktig i dag | A; senere kapabilitet `richTextEditor` (UITextView-variant) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 4024 | `#if os(macOS)` | A · API-gate | Rich markdown (NSTextView) → vanlig editor — riktig i dag | A; senere kapabilitet `richTextEditor` (UITextView-variant) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | 4171 | `#if os(macOS)` | A · API-gate | Rich markdown (NSTextView) → vanlig editor — riktig i dag | A; senere kapabilitet `richTextEditor` (UITextView-variant) |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 9 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 11 | `#elseif canImport(UIKit)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 15 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 605 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 656 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 787 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 888 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 984 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonVisualizationMapView.swift` | 999 | `#if os(macOS)` | A · API-gate | UIKit/MKMapView-grenen; MapKit finnes på visionOS | uendret |
| `Sources/CellApple/EntityRadar/EntityScannerCell.swift` | 14 | `#if canImport(UIKit)` | A · API-gate | UIKit/UIPasteboard — riktig | uendret |
| `Sources/CellApple/EntityRadar/EntityScannerCell.swift` | 16 | `#elseif canImport(AppKit)` | A · API-gate | UIKit/UIPasteboard — riktig | uendret |
| `Sources/CellApple/EntityRadar/EntityScannerCell.swift` | 1675 | `#if os(iOS)` | A · API-gate | NI-token deles ikke — riktig (rammeverket finnes ikke) | uendret |
| `Sources/CellApple/EntityRadar/EntityScannerCell.swift` | 1774 | `#if canImport(UIKit)` | A · API-gate | UIKit/UIPasteboard — riktig | uendret |
| `Sources/CellApple/EntityRadar/EntityScannerCell.swift` | 1777 | `#elseif canImport(AppKit)` | A · API-gate | UIKit/UIPasteboard — riktig | uendret |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 13 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 17 | `#if canImport(UIKit)` | A · API-gate | UIKit importeres — riktig | uendret |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 163 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 255 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 266 | `#if canImport(UIKit)` | C · feil på visionOS | **Kompileringsfeil**: `UIImpactFeedbackGenerator` finnes ikke i visionOS-SDK (Apple-dok: iOS/iPadOS/Catalyst) | `#if os(iOS)`; kapabilitet `haptics` |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 690 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 716 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 750 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 1020 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 1095 | `#if os(iOS)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/EntityRadar/ScannerService.swift` | 1205 | `#if canImport(UIKit)` | A · API-gate | NearbyInteraction faller bort; `platformSupportsNearbyPrecision = false` → «Nearby precision unavailable» — riktig og ærlig | uendret (mønster: kapabilitetsflagg) |
| `Sources/CellApple/IdentityVault.swift` | 688 | `#if targetEnvironment(simulator)` | D · simulator-gate | Som over | uendret |
| `Sources/CellApple/IdentityVault.swift` | 1408 | `#if targetEnvironment(simulator)` | D · simulator-gate | Som over | uendret |
| `Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift` | 8 | `#if canImport(UIKit)` | A · API-gate | UIKit-varsler om forgrunn/aktivering finnes — riktig | uendret |
| `Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift` | 11 | `#if canImport(AppKit)` | A · API-gate | UIKit-varsler om forgrunn/aktivering finnes — riktig | uendret |
| `Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift` | 644 | `#if canImport(UIKit)` | A · API-gate | UIKit-varsler om forgrunn/aktivering finnes — riktig | uendret |
| `Sources/CellBase/Cells/Bridging/LightweightBridgeTransport.swift` | 667 | `#if canImport(AppKit)` | A · API-gate | UIKit-varsler om forgrunn/aktivering finnes — riktig | uendret |

## 4. Det som blir feil på visionOS — samlet

### 4.1 Kompileringsfeil (3)

| Sted | Hvorfor | Rettelse |
|---|---|---|
| `Binding::Binding/ContentView.swift:1687–1699` | `#if os(iOS) Color(uiColor:) #else Color(nsColor:)` — på visionOS finnes ikke AppKit | `#if canImport(UIKit) … #elseif canImport(AppKit) … #else .clear`; og på glass skal fargen være `.clear` (kapabilitet `surfaceMaterial`) |
| `Binding::Binding/RootView.swift:185–189` | samme mønster | samme |
| `CellProtocol::Sources/CellApple/EntityRadar/ScannerService.swift:266` | `UIImpactFeedbackGenerator` under `canImport(UIKit)`; klassen finnes ikke i visionOS-SDK | `#if os(iOS)`; kapabilitet `haptics` |

Sammen med prosjektinnstillingene (`SUPPORTED_PLATFORMS`, `TARGETED_DEVICE_FAMILY`,
`UIApplicationSupportsMultipleScenes`) er dette hele listen jeg kan finne ved lesing. H1-proben
(`handoff/h1_compile_probe.sh`) er det som avgjør om listen er komplett.

### 4.2 Falske negativer — API-et finnes, sjekken stenger det ute (24 steder i 9 filer)

| Hva faller bort | Steder | Konsekvens for brukeren |
|---|---|---|
| App-delegate | `BindingApp.swift:16`, `BindingAppNotifications.swift:741` | Ingen push-registrering, ingen `didReceiveRemoteNotification`, ingen `application(_:open:)` |
| Push-innrullering | `NotificationEnrollmentManager.swift:5,56,78,105,126,139,384`, `NotificationCallbackClient.swift:3,28` | Ingen varsler; **enhets-ID blir ny UUID ved hver start** (linje 56) — scaffoldet ser en ny enhet hver gang |
| URL-mottak | `RootView.swift:73` | `haven://`-lenker (invitasjoner) gjør ingenting |
| Bakgrunnsoppgave | `BackgroundTaskCoordinator.swift:3` | Bro-arbeid kan avbrytes ved bakgrunn |
| Taleinndata | `BindingVoiceInputTranscriber.swift:52,278,286` | Butler-chat sier «Speech input is unavailable on this platform» selv om Speech finnes |
| Minnevarsel | `ContentView.swift:978` | Ingen `handleMemoryWarning()` |
| Tastaturhjelpere | `SkeletonView.swift:68,101,111` | Tastaturet kan ikke skjules; ingen «skjul tastatur»-knapp |
| Fil-drop | `SkeletonView.swift:1488,1588` | Vedleggsfelt tar ikke imot drag-and-drop, som visionOS støtter |
| Paritetsrenderer | `SkeletonParityRenderer.swift:4` | Paritetstester kan ikke kjøres for visionOS |

### 4.3 Vertsvalg som faller i en tilfeldig gren (26 steder)

Editorpaneler som overlays (iOS-stil) i et vindu som burde åpne egne vinduer; desktop-avstander der
HIG vil ha 60 pt; `systemBackground`-plater på glass; `usesPerspectiveDrivenEdgeMenus = true` som
et biprodukt av «ikke Mac». Ingen av disse er feil i betydningen «krasjer»; de er feil i betydningen
«ingen har valgt dem». Kapabilitetskontrakten i §5 gjør valget eksplisitt per vert.

### 4.4 Det som er riktig og skal stå (103 + 3)

NSPanel, NSWorkspace, launchctl/Process, NearbyInteraction, NSTextView-markdown,
`onExitCommand`/`onMoveCommand`, AppKit-vindusnummer, macOS-sandkassebokmerker, simulator-Keychain.
Disse rører vi ikke; de står i tillatelseslisten `contract/platform_conditional_allowlist.txt`
med dagens antall, og linten sier fra hvis tallet vokser.

## 5. Kapabilitetskontrakten — slik regelen håndheves

Tre filer i `contract/`, alle referanse (ikke landet i repoet før G2 for gren E):

- `HavenHostCapabilities.swift` — strukturen med 20 felter (vindusmodell, layout, inndata,
  sensorer/tjenester), `profile(for:isSimulator:)` som rent oppslag (testbart på Mac for alle
  verter), og `resolveCurrent()` — **det eneste stedet i appen som spør `os(...)` for et UX-valg.**
  `compactChrome` er med vilje ikke en vertsegenskap: den leses av `horizontalSizeClass` i visningen,
  som er riktig på alle verter (også visionOS-vinduer kan gjøres smale).
- `host_capability_profiles_v0.json` — de 8 profilene (4 familier × enhet/simulator) som
  `test.host.capability-profile` sammenligner mot. Simulator-overlegget setter
  `nearbyPrecision`, `haptics`, `pushRegistration` til false og `biometrics = simulated`.
- `lint_platform_conditionals.sh` + `platform_conditional_allowlist.txt` — teller `#if os(` per fil
  mot dagens grunnlinje (28 filer). En ny `os(`-sjekk i en fil utenfor listen, eller flere enn
  tillatt, gir rødt. Tallene skal ned når B- og C-stedene ryddes, og listen oppdateres i samme
  endring (`purpose://quality.docs-in-same-change`).

Avledede tester (lagt inn i `FORMAALSSPEC.md` §5):

| testRef | Hvordan | Evidens |
|---|---|---|
| `test.host.capability-profile` | For hver rad i `host_capability_profiles_v0.json`: `profile(for:isSimulator:)` er lik raden | TESTRESULT.md#capability |
| `test.host.current-is-known` | `resolveCurrent().family != .unknown` på macOS, iPhone-sim, iPad-sim, visionOS-sim | TESTRESULT.md#capability |
| `test.host.no-appkit-in-else` | grep: ingen `Color(nsColor`/`NSColor`/`NSApp` i en `#else`-gren under `#if os(iOS)` | TESTRESULT.md#capability |
| `test.lint.platform-conditionals` | `contract/lint_platform_conditionals.sh` → exit 0 | TESTRESULT.md#lint |
| `test.h1.compile-probe` | `handoff/h1_compile_probe.sh --go` → 0 feil for CellApple og HAVEN mot xrsimulator etter at §4.1 er rettet | TESTRESULT.md#h1 |

Rekkefølgen som gir minst risiko når gren E starter: (1) rett de tre kompileringsfeilene og
prosjektinnstillingene, kjør H1 — bygger det? (2) legg inn `HavenHostCapabilities` og linten med
dagens grunnlinje — ingen atferdsendring ennå; (3) flytt C-stedene (falske negativer) over på
`canImport`/`os(iOS) || os(visionOS)` — atferd på Mac/iPhone urørt, paritetsbilder før/etter;
(4) flytt B-stedene ett om gangen til kapabiliteter, med grunnlinjetallet ned for hver fil.

## 6. Ikke sjekket

- `CellProtocol::Sources/CellBase` er lest bare for de 53 filene jeg hadde staget; resten bygger
  også for Linux (CellVapor) og kan derfor ikke ha ubeskyttet Apple-kode, men jeg har ikke bevist det.
- `#available(...)`-sjekker er ikke auditert (bare `#if`). `if #available(iOS 15.0, *)` i
  `ScannerService.swift:1204` ligger inne i en `os(iOS)`-gren og er uskadelig.
- Mac Catalyst og watchOS er ikke byggemål og er ikke vurdert.
- Om `ToolbarItemGroup(placement: .keyboard)` finnes på visionOS er `recalled` (jeg mener ja);
  bekreftes av H1 når `SkeletonView.swift:111` er flyttet til `canImport(UIKit)`.
- Hvorvidt visionOS-SDK-en faktisk er installert i Xcode 26.2 på `kjetil-sin-m5-local` —
  `xcodebuild -showsdks` i H1-proben svarer.
