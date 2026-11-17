# Formålsspesifikasjon — HAVEN på Apple Vision

Oppgavemappe: `PDD_haven-visionos_2026-09-10` · Opprettet 2026-09-10 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.
>
> Denne oppgaven er *bestilt* som vurdering, læring, analyse, hypoteser, tester, diskusjon og forslag —
> med stopp før implementering. Leveransen er derfor denne spesifikasjonen, `ANALYSE.md`, bildene i
> `images/` og den klargjorte (ikke kjørte) byggeproben i `handoff/`. Se `ANALYSE.md` for
> argumentene; dette dokumentet er det som skal godkjennes.

## 0. Intensjon (ordrett) og brief-audit

> Jeg vil at du skal vurdere å lage en Apple vision versjon av HAVEN app - og kartlegge hva vil vil trenge og eventuelle erdringer og tillegg i rammeverkene det vil kreve. Men først skal vi ,definere formålene, lære, analysere, lage hypoteser, teste hypoteser, diskutere, foreslå løsniger som er godt argumentert. Tenker vi stopper der for en fot i bakken før eventuell implementering. Jeg tenker at man burde kunne instansiere så mange Portholes man vil som da dukker opp som separate skjermer eller vinduer. Om man skal redigere på CellConfiguration vil jeg at det på baksiden av flaten vises datastrømmer som blir levert til flaten. Det gjelder hvilke celler Porthole absorberer, hvilke Flows det er abonnert på. Indikasjon når det kommer flowelements over den. Det vises når det kjøres set / get. Brukeren trenger verktøy for å inspisere celler, og se på innoldet i trafikken. (Også implementert i celler selvfølgelig - går f.eks an å sette inn en celle som bare videresender FlowElements, men fanger data om innhold og trafikk som kan brukes for å se hva som skjer eller taes opp for å generere innsikt.) Vurder dette nøye ut ifra alt du vet om HAVEN og alt vi kan finne ut om Vision os og GUI/UX konsepter for AR/VR opplevelser. Det kan være - kanskje mer gøy enn nyttig - interessant å se all informasjon som treffer brukeren i rommet fra foskjellige celler og scaffolds som kan filtreres så brukeren har en svært visuell måte å justere hvilket informasjonpress hen blir utsatt for. Lag noe forslag til hordan det kan sees ut.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «HAVEN app» = Binding-prosjektet, SwiftUI, bygger for iOS og macOS | **retrieved** — `SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx"`, `TARGETED_DEVICE_FAMILY = "1,2"`, SDK macosx26.2 | `Binding::Binding.xcodeproj/project.pbxproj:425,534–553` |
| Man kan «instansiere så mange Portholes man vil» | **contradicted i dag** — `cell:///Porthole` er én identitetsunik `OrchestratorCell` med én `cellConfiguration`; `loadCellConfiguration` gjør `detachAll` | `Binding::Binding/BootstrapView.swift:399–420`; `CellProtocol::Sources/CellApple/Cells/OrchestratorCell.swift:21–27,423–444` |
| …men rammeverket har en mekanisme for flere instanser | **retrieved** — `CellUsageScope.template` gir ny celle per resolve (`createCell`), adresserbar med uuid | `CellProtocol::Sources/CellBase/Cells/CellResolver/CellResolver.swift:1811–1820,2470–2540` |
| Skeletons kan adressere «sin» Porthole | **contradicted** — base er hardkodet `cell:///Porthole` (11 steder i rendereren, 5 i modellen); generisk base er dokumentert som utsatt | `CellProtocol::…/Skeleton/Suggestion/SkeletonView.swift:367–478,1169,1934,1964,3681,3969`; `Binding::Documentation/Porthole-and-skeleton.md` |
| «hvilke celler Porthole absorberer» finnes som data | **retrieved** — `CellConfiguration.cellReferences` (`endpoint`, `label`, `subscribeFeed`, `subscriptions`, `setKeysAndValues`); `attach`/`attachedStatuses` | `CellProtocol::Sources/CellBase/CellConfiguration/CellConfiguration.swift:120–150`; `CellBase/Protocols/CellProtocol.swift` |
| «hvilke Flows det er abonnert på» finnes som data | **retrieved** — `subscribeFeed`/`subscriptions` per referanse; `absorbFlow`; `GeneralAuditor` holder abonnementene | samme; `CellBase/Cells/GeneralCell/Cast/GeneralAuditor.swift:176–330` |
| «indikasjon når det kommer flowelements» finnes som data | **retrieved** — `Emit.flow` → `FlowElement(title, topic, content, properties.type, origin)`; view-modellene holder de siste 10 | `CellBase/FeedItem/FlowElement.swift`; `…/PortholeBindingViewModel.swift` (`flowLimit = 10`) |
| «det vises når det kjøres set / get» finnes som data | **delvis** — hvert get/set logges via `CellResolver.logAction` som tekstlinje `INTR:…` uten utfall og varighet; ingen strukturert strøm | `CellBase/Cells/GeneralCell/GeneralCell.swift:1558,1697`; `CellResolver.swift:3000–3011` |
| «en celle som bare videresender FlowElements, men fanger data» finnes | **contradicted, men nær** — `FlowProbeCell` fanger uten å videresende; feed-intercepten i `GeneralCell` kan videresende (brukt av `OrchestratorCell`) | `CellBase/Cells/Diagnostics/FlowProbeCell.swift:400–470,713`; `CellBase/Cells/GeneralCell/Cast/Intercepts.swift`; `OrchestratorCell.swift:88–128` |
| Signert bevis per handling finnes for noen celler | **retrieved** — `EffectReceipt`/`ActionDecisionReceipt` (WebFetch, PurposeBoundAIGateway); Trust Package-audit bygger på dem | `CellBase/Agreement/EffectReceipt.swift`; `CellProtocolDocuments::Book/36_Agent_Trust_Package.md` §7–8 |
| Skeleton-rendereren er portabel til visionOS | **retrieved ved lesing, ikke bevist ved bygg** — ren SwiftUI, `#else`-nøytrale grener; paritetsrendereren er `os(macOS) \|\| os(iOS)` | `…/Suggestion/SkeletonView.swift`; `…/Skeleton/SkeletonParityRenderer.swift:4` |
| Appen kompilerer for visionOS med små rettelser | **unavailable** — bygg ikke kjørt (`device_bash` nede; krever Mac). Én sikker feil funnet: `UIImpactFeedbackGenerator` under `canImport(UIKit)` (klassen finnes ikke i visionOS-SDK) | `CellProtocol::Sources/CellApple/EntityRadar/ScannerService.swift:266`; developer.apple.com/documentation/uikit/uiimpactfeedbackgenerator |
| Flere vinduer på visionOS | **retrieved** — krever `UIApplicationSupportsMultipleScenes = true` (mangler i `Info.plist`); `openWindow(value:)` + `WindowGroup(for:)`; appen kan ikke plassere vinduer absolutt; bare ett `ImmersiveSpace` om gangen | developer.apple.com/documentation/visionos/presenting-windows-and-spaces; …/positioning-and-sizing-windows; `Binding::Binding/Info.plist` |
| HIG tillater «så mange vinduer man vil» | **contradicted** — «Avoid displaying too many windows … overwhelmed, constricted … cumbersome to relocate» | HIG «Spatial layout» (visionOS) |
| Rom-visning er mulig | **retrieved** — `ImmersiveSpace(.mixed)` + `RealityView`; `MeshInstancesComponent` (1 000+ objekter), `ViewAttachmentComponent` (SwiftUI-paneler i rommet); HIG: anker i rommet, innenfor synsfeltet, foretrekk `.mixed` | WWDC25 «What's new in visionOS 26»; HIG «Immersive experiences» |
| Gjeldende plattform | **retrieved** — Vision Pro (M5) leveres med visionOS 26; visionOS 27 i beta (WWDC26) | apple.com/apple-vision-pro/specs; developer.apple.com/videos/play/wwdc2026/287 |
| Hvordan baksiden av et visionOS-vindu ser ut fysisk | **recalled** (frostet glass uten innhold) — **ikke bærende**: baksiden designes som eksplisitt handling | — |
| Kjetil har Vision Pro / visionOS-SDK er installert / enheten selges i Norge | **unavailable** — spørsmål 1 i §6 | — |
| Codex kan kjøre byggeproben via MCP | **contradicted** — 60 s-tak (`lesson.codex-mcp-60s`); må gå som køjobb/detached | `handoff/queue-ready/` |

Tillegg 2026-09-10 (Kjetil, ordrett): «VI må teste det i simulator inntil videre. Bruk litt tid på å rygge opp i hvilket os det bygges for slik at ikke os og kapabilitetssjekker blir feil.» Svaret er `OS_KAPABILITETSAUDIT.md` + `contract/`. Nye audit-rader:

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Appen kompilerer for visionOS med små rettelser (H1) — presisert | **retrieved ved lesing** — tre kompileringsfeil funnet: `ContentView.swift:1687–1699` og `RootView.swift:185–189` (`Color(nsColor:)` i `#else` av `os(iOS)`), `ScannerService.swift:266` (`UIImpactFeedbackGenerator`); bygg fortsatt ikke kjørt | `OS_KAPABILITETSAUDIT.md` §4.1 |
| Alle OS-sjekker i appen er kartlagt | **retrieved** — 259 `#if`-direktiver, 159 OS-avhengige, alle klassifisert A/B/C/D med linje | `OS_KAPABILITETSAUDIT.md` §3 |
| Taleinndata virker på visionOS | **retrieved fra Apple, contradicted av koden** — Speech/AVFoundation finnes (Apple: sjekk `SFSpeechRecognizer`), men `BindingVoiceInputTranscriber.swift:52` stenger visionOS ute med `os(iOS) \|\| os(macOS)` | developer.apple.com/documentation/visionos/determining-whether-to-bring-your-app-to-visionos; `Binding::Binding/BindingVoiceInputTranscriber.swift:52,291` |
| Push, URL-mottak, bakgrunnsoppgave finnes på visionOS | **retrieved fra Apple, contradicted av koden** — alle er `os(iOS)`-gatet (9 filer) | `OS_KAPABILITETSAUDIT.md` §4.2 |
| visionOS-simulatoren kan brukes «inntil videre» | **retrieved** — layout, vinduer, volumer, rom og runtime kan testes; UWB, haptikk, ekte push-token og ekte Optic ID kan ikke; Keychain-tilgangskontroll slås av av `targetEnvironment(simulator)` | `OS_KAPABILITETSAUDIT.md` §1 |
| Simulert push/Optic ID i visionOS-simulator | **recalled** (ikke bærende) | — |

## 1. Formålstre

Klassifisering først (Book 23), nye noder som `purpose://candidate.…`. Treet har én rot og fem grener;
forslaget er at hver gren blir sin egen PDD-mappe ved G2.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.spatial.haven-in-the-room` | HAVEN i rommet | `purpose://human-agency` (sekundært `purpose://digital-work`) | En person kan se og forstå hva HAVEN gjør for henne som ting hun kan ha flere av, snu, åpne og skru på: flere flater samtidig, datastrømmene bak hver flate på forespørsel, trafikken inspiserbar, og det samlede informasjonspresset synlig og justerbart — uten at flatene mister paritet med Mac/iPad/web | Alle grener under grønne; §3-bildene godkjent | candidate |
| **Gren A — flere Portholes** | | | | | |
| `purpose://candidate.porthole.many` | Flere Portholes samtidig | `…haven-in-the-room` | Eieren kan åpne N Portholes, hver med egen konfigurasjon, egne absorberte celler og egen persistens; å laste eller lukke én rører ikke de andre; settet gjenopprettes ved neste start | `test.porthole.instances`, `test.porthole.restore` | candidate |
| `purpose://candidate.porthole.many.instances` | Porthole er instansierbar | `…porthole.many` | `cell:///Porthole` er et register (identitetsunikt) over instanser; hver instans er en template-scope `OrchestratorCell` med uuid, konfigurasjon, referanser og historikk; dagens persisterte konfigurasjon migreres som instans 0 | `test.porthole.instances` | candidate |
| `purpose://candidate.porthole.many.addressing` | Skeleton adresserer sin egen Porthole | `…porthole.many` | Relative keypaths og `cell:///Porthole/<label>…` løses mot Portholen som rendrer skeletonet (eksplisitt base-kontekst), ikke mot en global; eksisterende skeletons virker uendret med én instans | `test.skeleton.base-context` | candidate |
| `purpose://candidate.porthole.many.windows` | Én Porthole per vindu | `…porthole.many` | Verten åpner ett vindu per instans (`WindowGroup(for: PortholeID.self)`), på macOS og visionOS; vinduet bærer bare ID, cellen bærer tilstand; `UIApplicationSupportsMultipleScenes` satt | `test.host.multiwindow` | candidate |
| `purpose://candidate.porthole.many.manageable` | Mange, men ikke overveldende | `…porthole.many` | Åpne instanser kan samles (kø/dock/volum) og tas ut én og én; HIG-rådet mot for mange vinduer er ivaretatt uten å begrense antall instanser | `test.gui.reference-image-exists` (bilde 1), `test.host.deck` | candidate |
| **Gren B — baksiden** | | | | | |
| `purpose://candidate.porthole.backside` | Baksiden viser datastrømmene | `…haven-in-the-room` | I redigeringsmodus (og på forespørsel) ser eieren for denne Portholen: absorberte celler (label, endepunkt, tilkoblingsstatus, agreement), abonnerte flows/topics, en puls per innkommende FlowElement (label, topic, type, tid), og hvert get/set (keypath, requester, utfall, ms) | `test.backside.four-zones`, `test.gui.parity` (bilde 2) | candidate |
| `purpose://candidate.cell.interaction-events` | Strukturerte samhandlingshendelser | `…porthole.backside` (deles med gren C) | Hver celle kan observeres av sin eier gjennom en egen kanal med `CellInteractionEvent {seq, at, kind get/set/attach/detach/absorb/flowIn/flowOut/admission, keypath, label, requester, outcome, durationMs, bytes}` — uten payload, gated på grant `observe r---`; tap i strømmen er synlig via sekvensnummer; `logAction`-teksten beholdes som én sink | `test.events.emitted`, `test.events.no-payload`, `test.cell.auth-negative` | candidate |
| `purpose://candidate.porthole.backside.honest-absence` | Stille er ikke det samme som uleselig | `…porthole.backside` | Hver kilde-rad finnes alltid, med tilstand `lest / uleselig / stille / ikke koblet` og påkrevd årsak når den ikke er lest; én boolsk `claimsAllClear` er sann på nøyaktig ett sted | `test.backside.absence-states` | candidate |
| `purpose://candidate.porthole.backside.flip` | Baksiden er en handling, ikke en rundtur | `…porthole.backside` | Baksiden nås med én handling («Bakside») på alle verter — som flipp (`rotation3DEffect`) på Mac/iPad/visionOS-vindu, valgfritt som ekte bakstykke i volum på visionOS; forsiden er urørt når man snur tilbake | `test.gui.parity` (bilde 2, begge tilstander) | candidate |
| **Gren C — inspeksjon** | | | | | |
| `purpose://candidate.cell.traffic-inspection` | Inspisere celler og trafikkinnhold | `…haven-in-the-room`; anker `purpose://self-determination.data.verifiability` | Eieren kan velge en celle og se hva den tilbyr (Explore), hva den holder (snapshot), hva som faktisk går gjennom den (live og opptak) og hvem som gjorde hva (hendelser) — og kan bevise det i etterkant uten å stole på operatøren | Alle blad under grønne | candidate |
| `purpose://candidate.cell.flowtap` | FlowTap: videresendende tapp med opptak | `…traffic-inspection` | En `cell:///FlowTap` absorberer én kilde og videresender hvert FlowElement uendret (origin og envelope bevart), proxy-er get/set, og noterer metadata; opptak av innhold er av som standard (`metadata`), har retention, og leses/slettes bare av eier; kontrakt i `contract/flowtap_contract_v0.json` | `test.tap.transparent`, `test.tap.records-metadata-only-by-default`, `test.cell.contract-fixtures`, `test.cell.auth-negative` | candidate |
| `purpose://candidate.cell.flowtap.valve` | Tappen kan være ventil | `…cell.flowtap` | `tap.valve` = `pass \| mute \| throttle(n/min) \| allowTopics([…])` endrer faktisk hva som videresendes, og innstillingen persisteres som eierens preferanse | `test.tap.valve-changes-traffic` | candidate |
| `purpose://candidate.cell.inspector-surface` | Inspektørflaten | `…traffic-inspection` | Ett vindu per celle-endepunkt med Explore, Snapshot, Live, Kjede (Porthole → Tap → Kilde) og Ta opp/Slett; åpnes fra baksiden; på visionOS plasseres det ved siden av Portholen | `test.gui.reference-image-exists` (bilde 3), `test.skeleton.purpose-actions-reachable` | candidate |
| `purpose://candidate.cell.inspection.no-leak` | *Antiformål:* inspeksjon gir aldri mer enn grants gir | `…traffic-inspection` | En tapp, en hendelseskanal eller en inspektør skal ikke vise en requester noe kilden ville nektet den; formål er ikke rettighet; kryptert innhold tappes som bytes | `test.cell.auth-negative`, `test.tap.no-plaintext-without-key` | candidate (prohibited) |
| **Gren D — informasjonspress** | | | | | |
| `purpose://candidate.information-pressure.visible-adjustable` | Informasjonspresset er synlig og justerbart | `…haven-in-the-room`; anker `purpose://preference.owner-controlled` | Eieren ser alt som når henne fra celler og scaffolds (kilde, tema, type, rate), og kan justere per kilde slik at justeringen faktisk endrer trafikken og huskes | `test.pressure.aggregate-complete`, `test.tap.valve-changes-traffic` | candidate |
| `purpose://candidate.information-pressure.aggregate` | Ett aggregat over alle kilder | `…visible-adjustable` | Et «Trykk»-aggregat samler hendelser fra alle åpne Portholes' absorberte flows + butler, correspondence og varsler, med rate per minutt per kilde; 2D-panel på Mac/iPad | `test.pressure.aggregate-complete` | candidate |
| `purpose://candidate.information-pressure.room` | Rommet | `…visible-adjustable` | `ImmersiveSpace(.mixed)`: kilder som kropper i en halvsirkel ankret i rommet, strømmer som partikler mot en «meg»-ring, ventil-panel ved hver kilde; innenfor synsfeltet, ikke hode-ankret, ingen dybde på tekst | `test.gui.reference-image-exists` (bilde 4), `test.room.hig-checks` | candidate |
| `purpose://candidate.information-pressure.useful-not-only-fun` | Nyttig, ikke bare gøy | `…visible-adjustable` | Rommet regnes som nyttig først når eiere faktisk justerer en ventil etter å ha åpnet det, og justeringen måles i tapp-tall før/etter; ellers forblir det en demo | `test.pressure.h11` (måling) | candidate |
| **Gren E — plattformen** | | | | | |
| `purpose://candidate.platform.visionos-native` | HAVEN bygger og kjører nativt på visionOS | `purpose://quality`; `purpose://gui.quality.functional-accessible` | Appen bygger for `xros`/`xrsimulator`, starter, laster runtime, kobler bro og rendrer lokale flater med samme innhold og handlinger som på Mac | `test.build` (visionOS), `test.regression`, `test.gui.parity` | candidate |
| `purpose://candidate.platform.capability-axis` | Verten beskrives med kapabiliteter, ikke OS-navn | `…visionos-native` | `HavenHostCapabilities` (20 felter: vindusmodell, layout, inndata, sensorer — se `contract/HavenHostCapabilities.swift`) erstatter de 26 B-stedene i auditen; profilen per vert (Mac, iPhone, iPad, vision × enhet/simulator) står i `contract/host_capability_profiles_v0.json`; `resolveCurrent()` er det eneste stedet som spør `os(...)` for UX | `test.host.capability-profile`, `test.host.current-is-known`, `test.gui.parity` (før/etter refaktor) | candidate |
| `purpose://candidate.platform.visionos-blockers-isolated` | Utilgjengelige API-er er isolert | `…visionos-native` | `UIImpactFeedbackGenerator`, `NearbyInteraction`, delegate-adaptoren og `SkeletonParityRenderer` er gated på kapabilitet/plattform slik at CellApple og Binding bygger; EntityRadar sier ærlig «uten presisjon» på Vision Pro | `test.build` (visionOS), `test.radar.no-precision-state` | candidate |
| `purpose://candidate.platform.conditionals-honest` | Sjekkene sier bare det som er sant | `…visionos-native` | Hver `#if os(...)` i appen gater et API som faktisk bare finnes der (klasse A); ingen `#else`-gren inneholder AppKit-/UIKit-kode; UX-valg går gjennom `HavenHostCapabilities`; en lint holder grunnlinjen (28 filer i dag) og faller når nye `os(`-valg legges til | `test.host.no-appkit-in-else`, `test.lint.platform-conditionals` | candidate |
| `purpose://candidate.platform.glass-safe-styles` | Flatene tåler glass | `…visionos-native` | På visionOS mappes `styleRole` til systemmaterialer; rå hex-bakgrunner (148 i dag) beholdes bare uten `styleRole` og telles av en lint; paritetsnivået for materiale er definert | `test.styles.hex-count`, `test.gui.parity` (nivå 2-unntak) | candidate |
| **Standardpakker** | | | | | |
| `purpose://quality.build-and-regression` m.fl. | pkg.std.everything-works, gui-surface, cell-contract, cell-combination, codex-handoff | pakker | Se §4 | Se §5 | active (pakke) |

## 2. Avgrensning og avhengigheter

Hva dette **ikke** er:
- Ikke en 3D-HAVEN. Skeleton-formatet forblir 2D; ingen nye elementtyper foreslås (`cellconfiguration-skeleton-authoring`: nye kapabiliteter krever Kjetils ja). Volumer og rom er *vertskrom* rundt uendrede flater.
- Ikke en omskriving av rendereren til RealityKit. Én renderer (`SkeletonView`) for alle Apple-verter.
- Ikke det utsatte «prosjektverktøy i 3D» (trær/assosiasjoner som noder i rommet). Det er et eget formål og en egen PDD; denne oppgaven gir det bare et fundament (instanser, hendelser, rom).
- Ikke implementering. Kjetil ba om fot i bakken; byggeproben (H1) ligger klar men kjøres bare på hans ord.
- Ikke fjernflater over bro. Bro-status følges i `Binding::Documentation/HAVEN_Bro_Forensikk_og_Status_2026-09-02.md`; visionOS endrer ikke broen.

| Kapabilitet / avhengighet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Xcode 26.2 med visionOS-SDK og simulator | `Binding::Binding.xcodeproj/project.pbxproj` (`SDKROOT = macosx26.2`) | SDK-en er en egen nedlasting; ikke verifisert installert | ja (gren E) |
| Vision Pro-enhet | — | Ukjent om den finnes; simulator dekker layout, ikke blikk/hånd-komfort eller ekte glass | ja for G3-GUI i gren A/E, nei for B/C |
| `CellProtocol` bygger for `xros` | `CellProtocol::Package.swift` (platforms uten visionOS) + `ScannerService.swift:266` | Én kjent feil; resten ubevist til H1 er kjørt | ja (gren E) |
| Porthole-instansiering | `CellResolver.swift` (`.template`/`createCell`) | Migrering av persistert `CellConfiguration.json` i Porthole-katalogen er ikke designet | ja (gren A) |
| Skeleton base-kontekst | `…/Suggestion/SkeletonView.swift` (11 hardkodede steder), `Porthole-and-skeleton.md` («Deferred work») | Bakoverkompatibilitet må bevises med hele det lokale korpuset | ja (gren A) |
| Feed-intercept for videresending | `CellBase/Cells/GeneralCell/Cast/Intercepts.swift`; `OrchestratorCell.swift:88–128` | Én feed-intercept per celle — en tapp med flere kilder må være flere tapper | ja (gren C) |
| `FlowProbeCell`, `StateSnapshotCell`, `ExploreManifest` | `CellBase/Cells/Diagnostics/*`, `CellBase/Cells/GeneralCell/ExploreManifest.swift` | Sidelyttere/øyeblikksbilder; ingen get/set-observasjon | ja (gren C) |
| `logAction`-kroken | `CellResolver.swift:3000` | Tekst; ingen utfall/varighet | nei — erstattes av `interaction-events` |
| Multiscene på visionOS | `Binding::Binding/Info.plist` (nøkkel mangler) | Uten nøkkel ignoreres `openWindow` | ja (gren A/E) |
| Paritetsverktøy for visionOS | `…/Skeleton/SkeletonParityRenderer.swift:4` | Finnes ikke for `xros`; alternativ er simulator-skjermbilder | ja (gren E, G3) |
| Codex-kjøring av bygg | `handoff/queue-ready/` | Må gå som detached jobb med `danger-full-access` (`lesson.codex-workspace-write-cannot-build-cellscaffold`); aldri via MCP | ja (H1) |
| Tilgang til `HAVEN/_losen-queue` | ikke tilkoblet denne økten | Jobben ligger i `handoff/queue-ready/`; flyttes til køen når Kjetil sier ja | ja (H1) |
| visionOS-simulator (bestemt: testes der inntil videre) | `OS_KAPABILITETSAUDIT.md` §1 | Kan ikke teste UWB, haptikk, ekte push-token, ekte Optic ID, blikk-/håndkomfort eller ekte glass-lesbarhet; `targetEnvironment(simulator)` slår av Keychain-tilgangskontroll | ja (gren A/E — G3-GUI for disse grenene er simulator-nivå inntil enhet finnes) |
| De tre kompileringsfeilene og prosjektinnstillingene er rettet | `OS_KAPABILITETSAUDIT.md` §4.1 | Bare det som er funnet ved lesing; H1 avgjør om listen er komplett | ja (H1) |

## 3. Forventningskontrakt — «Det du kommer til å se»

Denne iterasjonen (før G1) leverer vurderingen. Rader merket *senere* fylles inn ved G2 for den grenen som starter.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Formålsspesifikasjonen (dette dokumentet) | fil | `FORMAALSSPEC.md` | — | nei (G1) |
| Læring, analyse, hypoteser med resultat, forslag med argumenter | fil | `ANALYSE.md` | — | nei |
| Bilde 1 — Rommet med flere Portholes og Porthole-køen | bilde (mockup) | `images/rommet-portholes-v1.png` | mockup, ikke Porthole-preview | nei (G1-GUI) |
| Bilde 2 — Én Porthole snudd: baksiden med fire soner, inkl. en uleselig og en stille kilde | bilde (mockup) | `images/bakside-datastrommer-v1.png` | mockup | nei (G1-GUI) |
| Bilde 3 — Inspektørvinduet med kjeden Porthole → FlowTap → celle, opptak og ventil | bilde (mockup) | `images/inspektor-flowtap-v1.png` | mockup | nei (G1-GUI) |
| Bilde 4 — Rommet med informasjonspress: kilder, strømmer, ventiler, filter | bilde (mockup) | `images/informasjonspress-rom-v1.png` | mockup | nei (G1-GUI) |
| Mockup-kilden (samme fire scener, kan åpnes i nettleser) | fil | `mockups/haven-visionos-mockups.html` | — | — |
| Byggeprobe for H1, klar men ikke kjørt | fil (Codex-jobb) | `handoff/queue-ready/visionos-h1-compile-probe.job` + `.prompt.md` | tørrkjøring som standard | nei (krever ja) |
| OS- og kapabilitetsaudit: byggmatrise, regel, alle 159 steder klassifisert, feilene på visionOS | fil | `OS_KAPABILITETSAUDIT.md` | — | nei |
| Kapabilitetskontrakt (referansekode), profiltabell, lint + tillatelsesliste | fil | `contract/HavenHostCapabilities.swift`, `contract/host_capability_profiles_v0.json`, `contract/lint_platform_conditionals.sh`, `contract/platform_conditional_allowlist.txt` | — | nei |
| *Senere (gren B/C, på Mac):* baksiden rendret i Porthole-preview, tapp-kontrakt med fixtures, TESTRESULT | bilde/fil/testutdata | `images/bakside-*-v2.png`, `contract/flowtap_contract_v0.json`, `TESTRESULT.md` | — | — |
| *Senere (gren A/E):* HAVEN i visionOS-simulator med to Portholes åpne, skjermbilde side om side med Mac | bilde | `images/visionos-sim-*.png` | — | — |

Hva dagens skeleton **ikke** kan rendre av det bildene viser (mockup-forbehold): vinduer i rom, glass,
ornaments, flipp/bakside, kjede-diagrammet, partikler, ventiler. Innholdet *i* hver Porthole på
bildene er ekte HAVEN-flater i stil, men ikke Porthole-rendret.

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra (når Porthole-preview er brukt).
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.
- **pkg.std.codex-handoff** — Overlevering til Codex/terminal
    - purpose://handoff.runnable-without-guessing: README.md i _handoff-mappen har rekkefølge, forventet utfall per steg, og alle skript støtter --dry-run/--go.
        - test test.handoff.dry-run [command]: Tørrkjøring gir 0 og lister hva som ville skjedd. → TESTRESULT.md#dry-run
    - artefakt handoff/README.md (port G2): Rekkefølge og kommandoer.

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.zsh-no-inline-comments** (2026-08-25, minor): Begge kommandolinjene feilet med 'ukjent argument: #' og ingenting kjørte.
    - forebygging: Aldri forklaring på samme linje som en kommando; skript har '"#"*) break ;;' i argumentparseren.
- **lesson.mount-is-not-git** (2026-08-25, major): Hver git-kommando fra device_bash etterlot en index.lock som ikke kunne fjernes og blokkerte Kjetils commits; seks repoer låst 24.08.
    - forebygging: Aldri git mot $HOME/mnt fra device_bash; les .git/refs som filer; all git kjøres av Kjetil eller codex exec.
- **lesson.codex-mcp-60s** (2026-08-18, major): Codex-MCP-kall kuttes etter ~60 s; registerlesning og Swift-bygg sprengte taket.
    - forebygging: Bygg/test/lange jobber går via terminal codex exec eller filbasert overlevering, aldri via Codex-MCP.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.stop-rule-too-wide-stops-the-job** (2026-09-09, minor): En commit-jobb til Codex stoppet før første `git add` fordi stoppregelen sa «finner du `.git/index.lock` eller annen låsefil: stopp». Et rekursivt søk fant 25 filer som heter `locked` under andre arbeidstrær — normale `git worktree lock`-markører som ikke blokkerer noe. Jobben gjorde ingenting, og hele runden gikk tapt.
    - forebygging: Skriv stoppregler som navn og sti, ikke som kategori: «stopp hvis `index.lock`, `HEAD.lock` eller `*.lock` finnes under `<denne stien>`». Navngi eksplisitt det som ser ut som en treffer men ikke er det, og si at det skal ignoreres. Legg alltid til «stopp hvis kommandoen faktisk avvises med denne feilen» — en filsøk-treffliste er ikke et bevis på blokkering. Samme gjelder alle vide vendinger i en prompt: «eller lignende», «eller annet», «eventuelle andre».
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.main-does-not-build-without-unlanded-changes** (2026-09-10, major): WP0-baselinen for HavenAgentD ga 79 kompileringsfeil mot de pinnede avhengighetene, og to feil selv i utviklingsmodus. HEAD-commiten på `main` heter «Land the correspondence MCP as a CellProtocol client» og kaller `AgentIdentityStore.loadExisting()` — en funksjon som bare finnes som ucommittet endring i det delte arbeidstreet. En ren klone av `main` kan verken bygge eller kjøre testene.
    - forebygging: Mål alltid WP0-baselinen i et **rent worktree fra revisjonen**, aldri i det delte treet — da fanges dette samme dag. Og etter enhver landing: bygg én gang fra et rent utsjekk før du sier at noe er landet. Bygger det bare der noen har ucommittede filer, er det ikke landet.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pkill-pattern-killed-the-queue-job** (2026-09-10, major): En commit-jobb i Losen-køen døde med EXIT=143 tolv sekunder etter start. Ingen feilmelding, ingen commit. Årsaken var min egen opprydding i et annet skript: `pkill -f "<appnavn>"`.
    - forebygging: Bruk aldri `pkill -f <mønster>` på en maskin der andre prosesser kan ha teksten i argv. Stopp en prosess ved PID du selv startet, eller ved `pgrep -x <prosessnavn>` kombinert med en sjekk av `ps -o comm=` mot den nøyaktige kjørbare stien. Dette gjelder særlig når en jobbkø kjører prompter som argument: alt du skriver i en prompt står på en kommandolinje et sted.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://questionnaire.responses.analyze [active] — Analyze questionnaire responses
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use

## 5. Avledede tester (samlet)

Pakketestene står først (auto). Deretter én rad per bladformål i §1 og per antiformål.

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | `xcodebuild -workspace Binding.xcworkspace -scheme HAVEN -destination 'platform=macOS'` og, for gren E, `-destination 'platform=visionOS Simulator,name=Apple Vision Pro'` | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | `Scripts/test_binding.sh`; sammenlign antall tester før/etter (baseline i ren worktree, `lesson.baseline-measured-another-pdds-branch`) | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md; `Porthole-and-skeleton.md` og Book 12 må oppdateres når base-kontekst/instanser lander | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | `purpose_dev.py validate` sjekker images/ mot §3 | images/ | **4 mockups finnes (v1)** |
| test.gui.parity | purpose://gui.parity-with-approved-image | Skjermbilde fra Porthole/Binding (Mac) og fra visionOS-simulator i samme viewport som referansen; lim inn i ACCEPT.md | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Terskel for denne oppgaven: baksiden synlig ≤ 300 ms etter «Bakside»; inspektør ≤ 1 s; tre forsøk | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | `xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | §3-handlingene (Bakside, Ta opp, Slett opptak, ventil) finnes i `reachableActionKeypaths` | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | Kontraktvalidator mot `contract/flowtap_contract_v0.json` + fixtures (positiv/negativ) | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre tester: feil requester på `tap.recording`, feil keypath, `purpose://prompt.unknown` — alle avvises | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk etter no-op-handlere i FlowTap og hendelseskanalen | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | `dataflow.md` med kantene Porthole→Tap→Kilde, Celle→Observasjonskanal→Bakside/Inspektør/Aggregat | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabellen i §0 — alle bærende rader er `retrieved` | FORMAALSSPEC.md#audit | **grønn for §0** |
| test.handoff.dry-run | purpose://handoff.runnable-without-guessing | Byggeproben kjørt uten `--go` gir 0 og lister stegene | TESTRESULT.md#dry-run | venter |
| test.porthole.instances | …porthole.many.instances | Enhetstest: opprett to instanser via registeret, last ulik konfigurasjon i hver, verifiser at `attachedStatuses` er disjunkte og at lukking av én ikke rører den andre | TESTRESULT.md#instances | venter |
| test.porthole.restore | …porthole.many | Restart runtime; registeret gir samme instanser med samme konfigurasjoner | TESTRESULT.md#restore | venter |
| test.skeleton.base-context | …porthole.many.addressing | Hele det lokale korpuset rendres med base = instans 0 og gir samme `reachableActionKeypaths` som før; to instanser med samme label `chat` treffer hver sin celle | TESTRESULT.md#base-context | venter |
| test.host.multiwindow | …porthole.many.windows | macOS: «Nytt Porthole» åpner nytt vindu med ny instans; visionOS-simulator: samme; `supportsMultipleWindows == true` | TESTRESULT.md#multiwindow | venter |
| test.host.deck | …porthole.many.manageable | Skjermbilde av køen med 5 instanser der bare 2 er ute i rommet | ACCEPT.md#deck | venter |
| test.backside.four-zones | …porthole.backside | Med en kjent konfigurasjon (3 referanser, 2 abonnement) viser baksiden nøyaktig disse, og et injisert FlowElement gir én puls på riktig label innen 300 ms | TESTRESULT.md#backside | venter |
| test.backside.absence-states | …backside.honest-absence | Simuler grant-nekt, bro nede og stille flow; baksiden viser tre ulike tilstander med årsak; `claimsAllClear == false` i alle tre | TESTRESULT.md#absence | venter |
| test.events.emitted | …cell.interaction-events | For hvert get/set/attach/absorb/flowIn/flowOut mottar observatøren én hendelse med stigende `seq`; teller stemmer med utførte kall | TESTRESULT.md#events | venter |
| test.events.no-payload | …cell.interaction-events | Hendelsene inneholder aldri `content`; test med sentinel-innhold | TESTRESULT.md#events | venter |
| test.tap.transparent | …cell.flowtap | Elementer gjennom tappen er byte-like (id, origin, envelope-signatur) med elementer direkte fra kilden | TESTRESULT.md#tap | venter |
| test.tap.records-metadata-only-by-default | …cell.flowtap | Uten `tap.record.mode = content` inneholder opptaket ingen `content`-felt | TESTRESULT.md#tap | venter |
| test.tap.valve-changes-traffic | …flowtap.valve, …visible-adjustable | `mute` gir 0 videresendte; `throttle(10/min)` gir ≤ 10; `allowTopics([a])` slipper bare `a`; innstillingen overlever restart | TESTRESULT.md#valve | venter |
| test.tap.no-plaintext-without-key | …inspection.no-leak (antiformål) | Kryptert FlowElement gjennom tapp med `content`-opptak: opptaket inneholder bytes, ikke klartekst | TESTRESULT.md#tap | venter |
| test.pressure.aggregate-complete | …information-pressure.aggregate | Med 3 Portholes og 5 kilder viser aggregatet 5 rader, alle med rate, og en kilde som er koblet fra vises som `ikke koblet` | TESTRESULT.md#pressure | venter |
| test.room.hig-checks | …information-pressure.room | Inspeksjon mot HIG: kilder innenfor synsfeltet ved åpning, ankret i rommet (ikke hodet), ingen tekst med dybde, interaktive elementer ≥ 60 pt mellom sentre | ACCEPT.md#room | venter |
| test.pressure.h11 | …useful-not-only-fun | Måling over N økter: andel med ventiljustering etter åpnet rom, og tapp-tall før/etter | TESTRESULT.md#h11 | venter |
| test.host.capability-profile | …platform.capability-axis | For hver av de 8 radene i `contract/host_capability_profiles_v0.json`: `HavenHostCapabilities.profile(for:isSimulator:)` er lik raden | TESTRESULT.md#capability | venter |
| test.host.current-is-known | …platform.capability-axis | `resolveCurrent().family != .unknown` på macOS, iPhone-simulator, iPad-simulator, visionOS-simulator | TESTRESULT.md#capability | venter |
| test.host.no-appkit-in-else | …platform.conditionals-honest | grep: ingen `Color(nsColor`, `NSColor`, `NSApp` i en `#else`-gren under `#if os(iOS)`; i dag 3 treff (ContentView 1687/1695, RootView 185) | TESTRESULT.md#capability | **rød i dag (3)** |
| test.lint.platform-conditionals | …platform.conditionals-honest | `contract/lint_platform_conditionals.sh` fra HAVEN-roten → exit 0; grunnlinje 28 filer | TESTRESULT.md#lint | venter (grunnlinje skrevet) |
| test.radar.no-precision-state | …visionos-blockers-isolated | På visionOS-profil rapporterer EntityRadar `precision: unavailable` i stedet for å love avstand | TESTRESULT.md#radar | venter |
| test.styles.hex-count | …platform.glass-safe-styles | Lint teller rå hex-bakgrunner uten `styleRole` i det lokale korpuset; tallet 148 skal ned, og hver gjenværende er begrunnet | TESTRESULT.md#styles | venter |
| test.h1.compile-probe | …platform.visionos-native (hypotese H1) | Byggeproben: feil per fil for CellApple og HAVEN mot `xrsimulator` | TESTRESULT.md#h1 | **blocked** — venter på Kjetils ja |

## 6. Åpne spørsmål til Kjetil

Bare spørsmål som endrer treet eller rekkefølgen.

1. ~~Vision Pro og SDK~~ **Besvart 2026-09-10: simulator inntil videre.** Gjenstår: er visionOS-komponenten installert i Xcode 26.2? (H1-proben svarer selv med `blocked` hvis ikke.) Og: er **26.0** riktig `XROS_DEPLOYMENT_TARGET`? Begrunnelse i `OS_KAPABILITETSAUDIT.md` §1 — begge Vision Pro-modellene kjører 26, så bare ikke-oppdaterte brukere utelukkes.
2. **Kjøre H1 nå?** Byggeproben er klar i `handoff/queue-ready/`. Den endrer ingenting i hovedtreet (ren worktree), men opptar Mac-en noen minutter. Skal den kjøres nå, eller vente til G1?
3. **Én PDD eller fem?** Forslaget er å godkjenne dette treet som helhet (G1) og så åpne én PDD per gren ved G2, i rekkefølgen B → C → E → A → D. Er rekkefølgen riktig for deg — særlig at Porthole-instanser (A) kommer *etter* baksiden og tappen?
4. **Porthole-instanser som celler.** Alternativ A (register + template-instanser) er valgt over sesjoner-i-én-celle med begrunnelse i celle-som-delingsenhet. Er du enig i at hver Porthole-instans skal være en celle med egen grant-mal?
5. **Opptak av innhold.** Standard `metadata` (ikke innhold) i FlowTap, innhold bare når eieren slår det på, og kryptert innhold aldri i klartekst uten nøkkel. Er beskyttende standard riktig også for utviklerbruk, eller vil du ha `content` som standard i debug-bygg?
6. **Baksiden på visionOS.** Flipp i vinduet (som på Mac) eller ekte bakstykke i et volum? Volumet gir «gå rundt», men Portholen får fast skala (HIG: interaktivt innhold bør ha dynamisk skala). Forslaget er flipp som standard, volum som eksperiment.
7. **Rommet.** Skal rommet (D) inn i dette treet nå, eller parkeres til ventilene (C) har vist at justering virker? Det står i treet med `useful-not-only-fun` som vakt, men det er ditt valg om det er en gren eller en fremtidig idé.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-10 | Opprettet; læring fra Binding/CellProtocol/CellProtocolDocuments og Apple-dokumentasjon; §0–§6 skrevet; fire mockups; H1-jobb klargjort (ikke kjørt) | Losen |
| 1 | 2026-09-10 | Kjetil: simulator inntil videre; rydd i OS- og kapabilitetssjekker. Lagt til `OS_KAPABILITETSAUDIT.md` (byggmatrise, regel, 159 steder klassifisert, 3 kompileringsfeil + 24 falske negativer), `contract/` (HavenHostCapabilities-referanse, profiltabell, lint, tillatelsesliste), nytt bladformål `platform.conditionals-honest`, nye tester, §0/§2/§3/§6 oppdatert | Losen |
