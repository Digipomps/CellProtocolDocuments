# Kapabilitetskartlegging — plangraf i Porthole, gren E

Dato: 2026-09-14. Omfang: E1–E6 og byggeklossene bak de elleve bildetilstandene. E7 er utenfor denne bestillingen.

**Kildekartleggingen er utført. Preview-delen er blokkert av kjøremiljøet, og ingen skjermbilder er produsert.** Første `npm run skeleton:iterate -- --mode preview` stoppet i Chromium-oppstart, før innlogging eller rendering. Ingen byggekloss er derfor godkjent som visuelt verifisert i denne rapporten. Det som nedenfor kalles «Støttet i dag», er presist avgrenset til funnet skjema- og rendererkode; det erstatter ikke det bestilte preview-beviset.

Hovedfunnet er at vanlige stakker kan uttrykke lanes, kort og paneler. `Visualization(kind: "graph")` har faktisk piler i web, men bruker prikknoder og tilbyr ikke kortmaler med separate handlinger. Det finnes ingen generell kobling fra disse grafkantene til vilkårlige `HStack`/`VStack`-kort. Apple-rendereren har et konkret avvik: grafkantene er linjer uten pilspiss.

Ingen kildekode, fabrikk, STATUS.md eller FORMAALSSPEC.md er endret. Ingen git-commit eller `commit-runtime` er utført. Midlertidige kandidater og verktøyutdata ligger utenfor repoet; kandidatene er også bevart nederst i denne rapporten. `screenshots/` er tom, uten mockuper eller plassholderbilder.

## 1. Kildegrunnlag og avgrensning

Den pålagte leserekkefølgen ble fulgt: authoring-skill, SkeletonDescription.swift, CellConfiguration.swift, de to Porthole-dokumentene, deretter E1–E6 og bildetabellen. Regelsettet er [SKILL.md:1](</Users/kjetil/.codex/skills/cellconfiguration-skeleton-authoring/SKILL.md:1>). Koden har nyere kapabiliteter enn skillens referanseliste; den faktiske enumen er autoritativ: [SkeletonDescription.swift:2747](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2747>).

`CellConfiguration` har `name`, `uuid`, `description`, `discovery`, `localization`, `cellReferences` og `skeleton`; det finnes ingen toppnivåkontrakt for plangraf, statusmaskin eller festing: [CellConfiguration.swift:147](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:147>) og [CellConfiguration.swift:182](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:182>). `Visualization` er en ekte case med `kind`, `keypath`, `stateKeypath`, `actionKeypath`, `spec` og `modifiers`: [SkeletonDescription.swift:2621](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2621>). At `spec` er `ValueType` betyr ikke at vilkårlige felter blir rendret. Kandidatene bruker bare felt som rendererfunksjonene nedenfor faktisk leser. `Markdown`, `Chart`, `Table`, `Lane`, `Card` og `Arrow` er ikke brukt som egne SkeletonElement-case.

Kravgrunnlaget er [FORMAALSSPEC.md:260](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:260>), [FORMAALSSPEC.md:272](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:272>), [FORMAALSSPEC.md:284](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:284>), [FORMAALSSPEC.md:297](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:297>), [FORMAALSSPEC.md:310](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:310>), [FORMAALSSPEC.md:323](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:323>) og de elleve bildetilstandene i [FORMAALSSPEC.md:416](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:416>). Dette er en byggeklossjekk, ikke leveranse eller akseptanse av disse bildene.

## 2. Støttet i dag — kildebekreftet, preview ikke gjennomført

1. **Lanes som eksplisitte rader.** `VStack.elements` samler én `HStack.elements` per gren. `Text.text` gir grenetikett, `spacing` avstand og `modifiers.padding`, `background`, `cornerRadius` innramming. Skjema: [SkeletonDescription.swift:1240](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1240>), [SkeletonDescription.swift:1307](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1307>), [SkeletonDescription.swift:797](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:797>), [SkeletonDescription.swift:519](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519>). Web: [skeleton-runtime.js:582](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:582>), [skeleton-runtime.js:4112](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4112>) og CSS [porthole-webo.css:2257](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/css/porthole-webo.css:2257>) / [porthole-webo.css:2282](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/css/porthole-webo.css:2282>). `ScrollView(axis: "horizontal", elements: …)` finnes for horisontal rulling, med skjema [SkeletonDescription.swift:1903](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1903>), renderer [skeleton-runtime.js:1431](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1431>) og CSS [porthole-webo.css:2271](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/css/porthole-webo.css:2271>). Det er vanlig layout, uten automatisk gren-/avhengighetsberegning. Minimal kandidat: `lanes`.

2. **Kort med tekstlig statusmerke og separat utførerfarge.** Et `VStack`-kort med `Text`-barn kan ha `padding`, `width`, `background`, `borderWidth`, `borderColor`, `cornerRadius`; statusmerket er et eget `Text` med `background`, `padding`, `cornerRadius`, og utførernavnet et annet `Text` med `foregroundColor`. `fontWeight`/`fontSize` kan skille tittel fra innhold. Skjema: [SkeletonDescription.swift:519](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519>) og [SkeletonDescription.swift:797](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:797>). Web bruker fargene og rammen i [skeleton-runtime.js:4127](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4127>), [skeleton-runtime.js:4137](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4137>), [skeleton-runtime.js:4167](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4167>). Apple har tilsvarende bakgrunn/ramme i [SkeletonView.swift:721](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:721>). Ingen særskilt `Badge`- eller `Card`-case er nødvendig. Dette beviser på kodenivå at navn, statusfarge og utførerfarge kan være separate; koden velger ikke utfører-/statuspalett fra PDD-data. Minimal kandidat: `kort-status-utforer`.

3. **Eksplisitt avhengighetsmarkering, med to forskjellige grenser.** `Text("Avhenger eksplisitt av DEMO-WP1")` og et piltegn i en `HStack` er vanlig tekstlayout, jf. [SkeletonDescription.swift:797](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:797>) og [skeleton-runtime.js:602](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:602>). Det er en lesbar referanse, ikke en tegnet forbindelse som følger kortene. Minimal kandidat: `avhengighetsmarkering`. Separat støtter `Visualization(kind: "graph")` i web `spec.nodes[]` med `id`, `label`, `kind`, `x`, `y`, `color`, samt `spec.edges[]` med `source`, `target`, `color`: [skeleton-runtime.js:1921](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1921>) og [skeleton-runtime.js:1947](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1947>). SVG-linjer og `marker-end`/pilspiss opprettes i [skeleton-runtime.js:3119](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3119>) og [skeleton-runtime.js:3143](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3143>). Ingen pilmodifikator kreves; pilspiss er innebygd i denne webvisningen. Minimal kandidat: `grafpiler`. Den undersøker piler mellom grafnoder, ikke mellom kort.

4. **En allerede åpnet drilldown-detalj.** `Section(header, content, footer)` og `VStack`/`Text` kan vise WP-ID, purposeRefs, gjør, tester, artefakter, avhengigheter, eier, utfører og status/bevis som separate felt. Skjema: [SkeletonDescription.swift:1937](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1937>), [SkeletonDescription.swift:1307](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1307>), [SkeletonDescription.swift:797](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:797>). Renderer: [skeleton-runtime.js:1398](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1398>) og [skeleton-runtime.js:5188](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:5188>). Samme kortmodifikatorer gir innramming. `Text.keypath` og `List(keypath, flowElementSkeleton: VStack)` er eksisterende databindinger, men kandidatens felt er uttrykkelig syntetiske, uten cellereads. Listeskjema: [SkeletonDescription.swift:1407](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1407>); oppdatering: [skeleton-runtime.js:5272](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:5272>). Minimal kandidat: `drilldown`. Åpne-/tilbakehandlingen og bevart grafutsnitt er ikke bevist av et allerede åpent panel.

5. **«Mine handlinger» som visning av før/under/etter/blokkert.** `VStack`/`Text` og samme flate-/tekstmodifikatorer kan vise når, hva, hvorfor bare deg, etterpå, mål, sidevirkning, kjørings-ID, bevis og blokkertgrunn. Fire separate minimale kandidater: `mine-for`, `mine-under`, `mine-etter`, `mine-blokkert`. `modifiers.visibility.when` kan velge hvilken ufarlig presentasjon som er synlig, med `scope`, `keypath`, `equals` og eventuelt `allOf`/`anyOf`: [SkeletonDescription.swift:132](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:132>), [SkeletonDescription.swift:174](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:174>), [SkeletonDescription.swift:543](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:543>); web [skeleton-runtime.js:4192](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4192>) og [skeleton-runtime.js:4668](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4668>). Kandidaten `tilstand-visibility` bruker bare et lokalt `List.elements`-objekt og `scope: "item"`, og lar bare «blokkert» være synlig. Det er ingen autorisasjons- eller utførelsessperre.

6. **Forklaringspanel ved siden av, og åpen presentasjon.** `HStack` med to `VStack`-barn gir valgt punkt til venstre og forklaring til høyre; `width`, `vAlignment: "top"`, `padding`, `background`, `borderWidth`, `borderColor`, `cornerRadius` er eksisterende felt. Minimal kandidat: `forklaring-side`; den viser en statisk utdatertmerking, ikke faktisk festing. `VStack.modifiers.presentation` kan også angi `kind: "drawer"`, `placement: "trailing"`, `backdropStyle`, `dismissOnBackdrop`, `escapeKeyBehavior`, `focusTrap` og `accessibilityLabel`. Skjema: [SkeletonDescription.swift:45](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:45>), [SkeletonDescription.swift:86](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:86>), [SkeletonDescription.swift:556](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:556>). Web: [skeleton-runtime.js:4230](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4230>), [skeleton-runtime.js:4334](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4334>), CSS [porthole-webo.css:2373](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/css/porthole-webo.css:2373>). Binding har en egen presentasjonsvert som pakker `SkeletonView`: [SkeletonPresentationOverlayView.swift:19](</Users/kjetil/Build/Digipomps/HAVEN/Binding/Binding/SkeletonPresentationOverlayView.swift:19>) og [SkeletonPresentationOverlayView.swift:743](</Users/kjetil/Build/Digipomps/HAVEN/Binding/Binding/SkeletonPresentationOverlayView.swift:743>). Minimal kandidat: `forklaring-overlay`. Den er statisk åpen og har ingen falske Fest-/Lukk-knapper.

**Eksisterende handlingsprimitiver, uten plangraf-kontraktbevis:** `Button(keypath, label, url, payload)` finnes, inklusive dynamisk `keypathKeypath`, `labelKeypath`, `payloadKeypath`: [SkeletonDescription.swift:1752](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1752>). Web sender handlingen i [skeleton-runtime.js:1233](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1233>); Swift velger `set` ved payload og ellers `get` i [SkeletonDescription.swift:1864](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1864>). URL-navigasjon er en særskilt form med tom `keypath` og `url`, jf. [SkeletonButtonNavigation.swift:23](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonButtonNavigation.swift:23>) og [skeleton-runtime.js:1179](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1179>). `Text.url` er derfor ikke brukt som om det automatisk var en klikkbar dokumentlenke. E3s konkrete målhandlinger er ikke koblet til kandidatene: det mangler et verifisert datagrunnlag/Explore-kontrakt for dem i denne kartleggingen.

## 3. Uklart — ikke avgjort eller målt

1. **Lanes:** faktisk horisontal rulling, tekstklipping og brukbarhet ved de to viewportene er umålt. Web `1900×1100` og web `780×1688` var planlagt; sistnevnte ville fortsatt vært nettleser, ikke Binding-bevis. Dynamisk gruppering fra samme normaliserte PDD-kilde er ikke validert. Det finnes dessuten web-`Visualization(kind: "gantt")` med `laneID`/`laneLabel`, jf. [skeleton-runtime.js:2042](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:2042>) og [skeleton-runtime.js:3451](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3451>). Denne visningen grupperer daterte tidslinjer og lager en egen rad per item ([skeleton-runtime.js:3356](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3356>), [skeleton-runtime.js:3448](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3448>)); den løser ikke uten videre E1s ene rad per gren med flere frie arbeidspakkekort. Den er ikke vurdert som en likeverdig kandidat.

2. **Kort:** runtimekoblingen fra en ekte arbeidspakke til tekststatus, utfører, farger og kildebevis er ikke undersøkt som brukerflyt. `background`, `borderColor` og `foregroundColor` er bokstavelige strenger, uten tilsvarende farge-keypath-felt ([SkeletonDescription.swift:528](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:528>), [SkeletonDescription.swift:535](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:535>), [SkeletonDescription.swift:545](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:545>)). Synlighetsvarianter og ny rendring finnes, men automatisk og konsistent statusfarging er ikke dermed bevist.

3. **Piler:** koden har pilspisser, men geometri, riktig retning i forhold til kildens `dependsOn`, overlapp og lesbarhet er ikke preview-testet. En konkret geometririsiko er at SVG-en har kvadratisk `viewBox="0 0 100 100"`, mens nodene legges med prosent av hele beholderen: [skeleton-runtime.js:3121](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3121>) og [skeleton-runtime.js:3174](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3174>). Om linjeendene treffer nodene i en bred beholder må avgjøres visuelt; dette er ikke rapportert som en observert feil. Panorering/zoom finnes i webkilden ([skeleton-runtime.js:3235](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3235>)), men er ikke utført her.

4. **Drilldown:** korrekt valg, fil:linje/anker, kildeversjon per felt, tastatursti og retur til samme utsnitt er umålt. `List` har `selectionStateKeypath`, `selectionActionKeypath`, `activationActionKeypath` og `selectionPayloadMode` ([SkeletonDescription.swift:1413](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1413>)); `Visualization` har én `actionKeypath` med nodepayload ([skeleton-runtime.js:2372](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:2372>), [skeleton-runtime.js:3224](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3224>)). Ingen av dem beviser at E2s konkrete kontrakt allerede er koblet opp.

5. **Mine handlinger:** filter på samme bokser, reelt grant, bekreftet kildeversjon, idempotens, maskinbro, menneskelig godkjenning og artefaktkvittering er ikke verifisert. Webknappen har midlertidig `disabled`/`aria-busy` mens ett løfte venter ([skeleton-runtime.js:1258](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1258>)), og lokal kvitteringsstyling ([skeleton-runtime.js:1290](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1290>)). Dette er ikke en kjøringsstatusmaskin eller bevis for levert arbeid. E3s svarvei er fortsatt en avhengighet i [FORMAALSSPEC.md:373](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:373>) og [FORMAALSSPEC.md:374](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:374>).

6. **Forklaring/festing:** kildekoden har eksisterende Co-Pilot-handlinger `chatHub.ui.pinComponentSurface`, `restoreComponentSurface`, `minimizeComponentSurface` og `dismissComponentSurface`, bygget med `Button`/`List`: [PersonalCopilotConfigurationFactory.swift:1602](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1602>) og [PersonalCopilotConfigurationFactory.swift:1619](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1619>). Registrering kontrollerer tilgang ([PersonalCopilotCells.swift:1614](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift:1614>)), pin-handlingen lagrer UI-tilstand ([PersonalCopilotCloudStore.swift:3358](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:3358>), [PersonalCopilotCloudStore.swift:10386](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:10386>)). Dette er et reelt gjenbruksfunn, men ikke bevis for E4s bruker-eide element i Portholens CellConfiguration, valgt skop, utdatertmerking og uendret chatlogg. Det er ikke avklart om den eksakte Butler B-varianten kan brukes direkte. Heller ikke forklarer, lesbare versjonerte kilder, oppfølgingsspørsmål, feil/prøv igjen eller gjenåpning i ny økt er kjørt. Se den eksplisitte avhengigheten [FORMAALSSPEC.md:377](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:377>).

7. **Miljø og kildeparitet:** den lokale serveren svarer på `/health/build`, men oppgir `app_revision`, `build_timestamp` og `environment` som `unknown`. Det er derfor ingen bevist kobling mellom disse lokale kildefilene og en servert versjon. Previewen kom aldri så langt at aktiv konfigurasjon, serverens skeleton-dekoder eller nettleserressursene kunne kontrolleres. Full web/Binding-paritet er uavklart selv der begge har implementasjon.

## 4. Ikke støttet uten implementasjon — presise gap

Dette er en gapliste til Kjetil, ikke forslag om å starte implementasjon.

1. **Piler mellom vilkårlige skeleton-kort:** ingen case eller modifikator binder linjens start/slutt til to `HStack`/`VStack`/`Section`-elementers grenser. `Divider` er en separator, ikke en forbindelseskant. Den fullstendige enumen er [SkeletonDescription.swift:2747](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2747>), modifierfeltene [SkeletonDescription.swift:519](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519>), og Dividers skjema [SkeletonDescription.swift:1880](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1880>). `Visualization(graph)`s interne SVG løser bare dens egne nodeposisjoner ([skeleton-runtime.js:3143](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3143>)). Påstanden «ingen linje/pil-tegning i dagens skjema» ville vært for bred og er **ikke** rapportens konklusjon.

2. **Arbeidspakkekort inne i dagens graf:** `Visualization(graph)` har ingen konsumert node-skeleton/kortmal, ingen lane-layout for arbeidspakker og ingen separate Utfør/Forklar-knapper i hver node. Web bygger en prikk, etikett og én nodehandling ([skeleton-runtime.js:3165](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3165>), [skeleton-runtime.js:3189](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3189>), [skeleton-runtime.js:3224](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3224>)); den innebygde inspektøren viser navn, type og lenkeantall ([skeleton-runtime.js:3275](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3275>)). `groups` er en etikettstripe ([skeleton-runtime.js:3092](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3092>)), ikke lanes. Frie ekstra felter i `spec` vil ikke skape de manglende komponentene.

3. **Grafparitet i den inspiserte Apple-rendereren:** den tegner `Path.addLine` med stroke, uten pilspiss, og prikknoder i en visning med fast høyde 260; webens grafpanorering/zoom finnes ikke i denne komponenten. Kilde: [SkeletonView.swift:2845](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:2845>). Automatisk plassering er også forskjellig: Apple bruker sirkel ([SkeletonView.swift:2466](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:2466>)), web bruker valgt node/nabolag/grupper ([skeleton-runtime.js:3847](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:3847>)). Dette er kildepåviste forskjeller; eventuell omgivende appscroll er ikke testet.

4. **Generell deaktivert handlingsknapp med state og grunn:** `SkeletonButton`/`SkeletonModifiers` har ikke `enabled`/`disabled`, state-keypath for dette eller en grunnbinding. Feltlistene er [SkeletonDescription.swift:1752](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1752>) og [SkeletonDescription.swift:519](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:519>). Web har bare spesialtilfellet ugyldig navigasjonsmål ([skeleton-runtime.js:1209](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1209>)) og midlertidig ventetilstand ([skeleton-runtime.js:1258](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:1258>)). Skjult knapp med forklarende tekst er mulig, men oppfyller ikke E3s eksplisitte «deaktivert med grunn». Dempet `opacity` deaktiverer ikke klikk.

5. **Forankring direkte ved valgt grafnode:** `presentation.anchorRole`/`anchorKeypath` finnes i skjemaet, men web leser dem inn i normaliseringen uten posisjonsoppslag ([skeleton-runtime.js:4264](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4264>)); CSS-en har ingen tilsvarende ankerplassering ([porthole-webo.css:2373](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/css/porthole-webo.css:2373>)). Binding mapper `.anchor` til `.center` ([SkeletonPresentationOverlayView.swift:832](</Users/kjetil/Build/Digipomps/HAVEN/Binding/Binding/SkeletonPresentationOverlayView.swift:832>)). Sidepanel/overlay som generell flate har støtte; presis forankring til en konkret node er ikke implementert i disse stiene.

6. **Åpne/lukke bare via `openStateKeypath` i web:** feltet normaliseres ([skeleton-runtime.js:4285](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4285>)), men åpen tilstand bestemmes av elementets synlighet ([skeleton-runtime.js:4512](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:4512>)). `visibility.when` må bære synlighet i dagens websti; `openStateKeypath` alene er ingen virksom bryter. Ny feltbruk skal ikke presenteres som et ferdig alternativ.

**Tjeneste- og integrasjonsgrenser, ikke konstaterte nye rendererbehov:** ingen av disse visningselementene leser og normaliserer PLAN/STATUS/TESTRESULT, håndhever E3s utførelseskontrakt eller leverer E4s fullstendige festede forklaring. De konkrete plangraf-koblingene er ikke påvist i de inspiserte stiene; FORMAALSSPEC peker selv på A-10, A-11, A-12, A-14 og A-15 ([FORMAALSSPEC.md:370](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:370>)). Dette er ikke grunnlag for å erklære tilsvarende mekanismer fraværende i hele HAVEN, eller for å beslutte hva som eventuelt skal bygges.

## 5. E1–E6: støttegrad i dag

«Delvis» betyr at relevante eksisterende byggeklosser er funnet, mens hele E-bladets kontrakt ikke er påvist. «Helt» ville krevd både de nødvendige kapabilitetene og fungerende sammenheng. Tabellen er ikke en måling av E-verifierne; ingen E-blad er målt grønt her.

| E-blad | Støttegrad | Konkret støtte / gjenstående grense |
|---|---|---|
| E1 — visning | **Delvis** | Rader, kort, tekst/farge og grafpiler i web finnes separat. Kombinasjonen lanes + kort + piler + separate handlinger finnes ikke i dagens grafkomponent; Apple mangler pilspiss. Normalisering og paritet er umålt. |
| E2 — drilldown | **Delvis** | Feltpanel og generiske valg-/handlingsprimitiver finnes. Full feltproveniens, åpne/tilbake, beholdt utsnitt og tastaturflyt er ikke påvist. |
| E3 — Mine handlinger | **Delvis** | De fire presentasjonene og generisk handlingsdispatch kan uttrykkes. Generell deaktivert knapp mangler; faktisk svarvei/grant/idempotens/kvittering er ikke verifisert. |
| E4 — forklaring ved siden av | **Delvis** | Sidepanel og drawer finnes, og Co-Pilot har pin/restore. Forankring direkte til node mangler i undersøkte rendererstier; plangrafens forklaring, eierskap/skop, persistens og chat-uendret-krav er ikke påvist. |
| E5 — samme sannhet som filene | **Delvis, bare presentasjonen** | Tekstbinding, oppdatering av grafdata, feil-/konflikt-/ferskhetstekst kan vises ([skeleton-runtime.js:5188](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:5188>), [skeleton-runtime.js:5307](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Public/js/skeleton-runtime.js:5307>)). Ingen kildegaranti følger av dette: versjonert filprojeksjon, 5 s-frist, tilbakeføring av bevis og tilbaketrekking av grønt er ikke verifisert. |
| E6 — ingen niende inngang | **Delvis** | Eksisterende `HAVEN Workbench` er et faktisk sammensetningspunkt ([ConfigurationCatalogCell.swift:7672](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:7672>)). Intern komposisjon krever ingen ny SkeletonElement-case. Faktisk før/etter-inventar og bevart WP-/forklaringskontekst mellom linsene er ikke målt. |

## 6. De elleve bildetilstandene og hva kartleggingen dekker

Disse radene følger [FORMAALSSPEC.md:425](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md:425>). Ingen av dem har et levert referansebilde i denne rapporten.

| Bildetilstand | Byggekloss / grense |
|---|---|
| Fylt graf | `lanes`, `kort-status-utforer`, `grafpiler` er separate prober; ingen samlet kortgraf. |
| Tom plan | Eksisterende `Text`/`Section` kan vise forklart fravær; virkelig kildefravær er ikke koblet opp. |
| Manglende/utdatert kilde, motstridende status | Samme tekst-/panelprimitiver kan vise begge kildene og grunn; ingen ferskhets-/konfliktgaranti. |
| Åpen boks | `drilldown`, uten reell kildeproveniens eller valg-/tilbaketest. |
| Utfør før | `mine-for`, uten utførbar handling. |
| Utfør kjører | `mine-under`, syntetisk kjørings-ID. |
| Utfør etter | `mine-etter`, uttrykkelig syntetisk bevis. |
| Utfør blokkert | `mine-blokkert`; deaktivert knapp er et eget gap. |
| Forklaringsoverlay | `forklaring-overlay`; ingen forklarer eller oppfølgingshandling. |
| Forklarer utilgjengelig | Feiltekst kan vises; reell Prøv igjen-svarvei er ikke verifisert. |
| Forklaring festet, kilde endret | `forklaring-side` viser bare plasseringen/teksten. E4s Fest/persistens/utdatertkobling er ikke bevist. |

## 7. Previewforsøk, validering og manglende bevis

Valgt lokal base-URL: `http://127.0.0.1:9089`. Standardverdien i verktøyet er staging ([skeleton-iterate.js:10](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/scripts/skeleton-iterate.js:10>)), så lokal URL ble eksplisitt satt. Eksisterende kildepunkt er `HAVEN Workbench` / `cell:///WorkItem`, bekreftet i katalogfabrikken ([ConfigurationCatalogCell.swift:7672](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift:7672>)). Lasting av dette punktet ble ikke nådd.

Arbeidsmappe for kommandoen var `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`. Kommandoen som faktisk ble kjørt:

```sh
npm run skeleton:iterate -- --mode preview \
  --base-url http://127.0.0.1:9089 \
  --scenario /private/tmp/plangraf-porthole-capability-20260914/lanes.preview.json \
  --output-dir /private/tmp/plangraf-porthole-capability-20260914/test-results/skeleton-iterate/lanes
```

`--output-dir` flyttet verktøyets vanlige `test-results/skeleton-iterate/...`-artefakter til tempområdet, slik at verktøyet ikke skrev i CellScaffold eller andre PDD-filer. Utgangen var **1**. Feilen var:

```text
browserType.launch: Target page, context or browser has been closed
FATAL:base/apple/mach_port_rendezvous_mac.cc:158
bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.48868:
Permission denied (1100)
at main (.../CellScaffold/scripts/skeleton-iterate.js:27:34)
```

`input.json` ble skrevet. Verktøyet starter Chromium på linje 27, mens autentisering først skjer i `runViewport` på linje 114 ([skeleton-iterate.js:21](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/scripts/skeleton-iterate.js:21>), [skeleton-iterate.js:111](</Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/scripts/skeleton-iterate.js:111>)). Ingen innlogging, `editor.working.setSkeleton`, `editor.apply`, screenshot eller serverendring fra denne previewkommandoen ble derfor nådd. Det ble ikke gjort en alternativ kjøring som omgår sandboxens avslag. Resten av kandidatene ble ikke preview-kjørt etter denne felles oppstartsfeilen.

**Statisk Explore-sjekk:** alle 12 kandidater ble kontrollert med `Tools/Explore/skeleton_explore_validator.py`, hver pakket i en minimal `CellConfiguration` med `name`, `cellReferences: []`, `skeleton`. Alle ga exit 0, `bindings: 0`, `errors: 0`, `warnings: 0`. Dette er forventet for prober uten fjernbindinger; ingen Explore-manifest er fabrikkert. `tilstand-visibility` leser bare lokalt `item.phase`. Verktøyet er ikke en Swift JSONDecoder-test eller et bevis for rendering. Swift-testkilden bekrefter at graf og visibility har decode-tester ([SkeletonTests.swift:279](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/SkeletonTests.swift:279>), [SkeletonTests.swift:1111](</Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/SkeletonTests.swift:1111>)), men disse testene er ikke kjørt i denne runden.

Kandidatene er bevisst uten ekte kjøring, Fest, chatkall eller oppdiktede plangraf-keypaths. De statiske tekstene «levert», kjørings-ID og bevis er merket som syntetiske. Ingen slik tekst skal leses som faktisk status for en arbeidspakke.

| Kandidat | Previewstatus | Skjermbilde |
|---|---|---|
| `lanes` | Forsøkt; Chromium-oppstart avvist | Ikke produsert |
| `kort-status-utforer` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `avhengighetsmarkering` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `grafpiler` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `drilldown` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `mine-for` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `mine-under` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `mine-etter` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `mine-blokkert` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `forklaring-side` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `forklaring-overlay` | Ikke kjørt; samme miljøblokkering | Ikke produsert |
| `tilstand-visibility` | Ikke kjørt; samme miljøblokkering | Ikke produsert |

Den bestilte rendererverifikasjonen gjenstår i et kjøremiljø som kan starte Chromium. De faktiske previewbildene må da hentes fra verktøyets artefaktsti og kopieres til `screenshots/` med kandidatnavn og viewport. En smal webpreview skal navngis `smal-web`, aldri `Binding`.

## 8. Minimale kandidater bevart for videre verifikasjon

Hver JSON-blokk nedenfor er én selvstendig `.skeleton.json`, ikke en samlet plangraf. `lanes` ble sendt til previewverktøyet, men nådde ikke rendereren. De øvrige er kildekontrollerte kandidater som ikke er visuelt prøvd.


<details>
<summary>Kandidat: lanes</summary>

```json
{
  "VStack": {
    "spacing": 12,
    "modifiers": {
      "padding": 16
    },
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · lanes · syntetiske data"
        }
      },
      {
        "HStack": {
          "spacing": 16,
          "modifiers": {
            "padding": 12,
            "background": "#EDF2F7",
            "cornerRadius": 8
          },
          "elements": [
            {
              "Text": {
                "text": "Gren A"
              }
            },
            {
              "Text": {
                "text": "WP-A1"
              }
            },
            {
              "Text": {
                "text": "WP-A2"
              }
            }
          ]
        }
      },
      {
        "HStack": {
          "spacing": 16,
          "modifiers": {
            "padding": 12,
            "background": "#EDF2F7",
            "cornerRadius": 8
          },
          "elements": [
            {
              "Text": {
                "text": "Gren E"
              }
            },
            {
              "Text": {
                "text": "WP-E1"
              }
            },
            {
              "Text": {
                "text": "WP-E2"
              }
            }
          ]
        }
      }
    ]
  }
}
```

</details>

<details>
<summary>Kandidat: kort-status-utforer</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · kort · syntetiske data"
        }
      },
      {
        "HStack": {
          "elements": [
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "DEMO-WP1",
                      "modifiers": {
                        "fontWeight": "bold"
                      }
                    }
                  },
                  {
                    "Text": {
                      "text": "Utfører: probe-agent A",
                      "modifiers": {
                        "foregroundColor": "#6D28D9"
                      }
                    }
                  },
                  {
                    "Text": {
                      "text": "Kjører",
                      "modifiers": {
                        "background": "#DBEAFE",
                        "padding": 6,
                        "cornerRadius": 6
                      }
                    }
                  }
                ],
                "spacing": 8,
                "modifiers": {
                  "padding": 12,
                  "width": 230,
                  "background": "#FFFFFF",
                  "borderWidth": 2,
                  "borderColor": "#6D28D9",
                  "cornerRadius": 10
                }
              }
            },
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "DEMO-WP2",
                      "modifiers": {
                        "fontWeight": "bold"
                      }
                    }
                  },
                  {
                    "Text": {
                      "text": "Utfører: probe-person",
                      "modifiers": {
                        "foregroundColor": "#0369A1"
                      }
                    }
                  },
                  {
                    "Text": {
                      "text": "Din handling",
                      "modifiers": {
                        "background": "#FEF3C7",
                        "padding": 6,
                        "cornerRadius": 6
                      }
                    }
                  }
                ],
                "spacing": 8,
                "modifiers": {
                  "padding": 12,
                  "width": 230,
                  "background": "#FFFFFF",
                  "borderWidth": 2,
                  "borderColor": "#0369A1",
                  "cornerRadius": 10
                }
              }
            }
          ],
          "spacing": 12
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: avhengighetsmarkering</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · tekstlig avhengighet · syntetiske data"
        }
      },
      {
        "HStack": {
          "elements": [
            {
              "Text": {
                "text": "DEMO-WP1"
              }
            },
            {
              "Text": {
                "text": "→"
              }
            },
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "DEMO-WP2"
                    }
                  },
                  {
                    "Text": {
                      "text": "Avhenger eksplisitt av DEMO-WP1"
                    }
                  }
                ],
                "spacing": 8
              }
            }
          ],
          "spacing": 12
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: grafpiler</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · grafpiler · syntetiske data"
        }
      },
      {
        "Visualization": {
          "kind": "graph",
          "spec": {
            "title": "Eksplisitt kant DEMO-WP1 → DEMO-WP2",
            "nodes": [
              {
                "id": "a",
                "label": "DEMO-WP1",
                "kind": "workitem",
                "x": 0.25,
                "y": 0.35,
                "color": "#A78BFA"
              },
              {
                "id": "b",
                "label": "DEMO-WP2",
                "kind": "workitem",
                "x": 0.75,
                "y": 0.35,
                "color": "#38BDF8"
              }
            ],
            "edges": [
              {
                "source": "a",
                "target": "b",
                "label": "dependsOn",
                "color": "#FBBF24"
              }
            ]
          },
          "modifiers": {
            "width": 640
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: drilldown</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · åpen detalj · syntetiske data"
        }
      },
      {
        "Section": {
          "header": {
            "Text": {
              "text": "DEMO-WP1 · åpen detalj"
            }
          },
          "content": [
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "purposeRef: purpose://example.probe"
                    }
                  },
                  {
                    "Text": {
                      "text": "Gjør: vis én detalj"
                    }
                  },
                  {
                    "Text": {
                      "text": "Tester: ingen virkelig kjøring"
                    }
                  },
                  {
                    "Text": {
                      "text": "Artefakt: ingen virkelig leveranse"
                    }
                  },
                  {
                    "Text": {
                      "text": "Avhengigheter: DEMO-WP0"
                    }
                  },
                  {
                    "Text": {
                      "text": "Eier: ukjent — ikke oppgitt i prøvedata"
                    }
                  },
                  {
                    "Text": {
                      "text": "Utfører: probe-agent A"
                    }
                  },
                  {
                    "Text": {
                      "text": "Status: ukjent — bevis mangler"
                    }
                  },
                  {
                    "Text": {
                      "text": "Kilde: syntetisk fixture, revisjon demo-v1"
                    }
                  }
                ],
                "spacing": 8
              }
            }
          ],
          "modifiers": {
            "padding": 16,
            "background": "#F8FAFC",
            "cornerRadius": 10
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: mine-for</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · Mine handlinger / for · syntetiske data"
        }
      },
      {
        "VStack": {
          "elements": [
            {
              "Text": {
                "text": "Mine handlinger"
              }
            },
            {
              "Text": {
                "text": "DEMO-WP1"
              }
            },
            {
              "Text": {
                "text": "Før trykk",
                "modifiers": {
                  "background": "#FEF3C7",
                  "padding": 6,
                  "cornerRadius": 6
                }
              }
            },
            {
              "Text": {
                "text": "Når: etter gjennomgang"
              }
            },
            {
              "Text": {
                "text": "Hva: godkjenne én bestemt revisjon"
              }
            },
            {
              "Text": {
                "text": "Hvorfor bare deg: menneskelig port"
              }
            },
            {
              "Text": {
                "text": "Etterpå: neste steg kan bli tilgjengelig"
              }
            },
            {
              "Text": {
                "text": "Mål: DEMO-WP1 / demo-v1"
              }
            },
            {
              "Text": {
                "text": "Sidevirkning: skrive beslutning"
              }
            },
            {
              "Text": {
                "text": "Grant/svarvei: ikke tilkoblet i denne visningsproben"
              }
            }
          ],
          "spacing": 8,
          "modifiers": {
            "padding": 16,
            "background": "#F8FAFC",
            "cornerRadius": 10
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: mine-under</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · Mine handlinger / under · syntetiske data"
        }
      },
      {
        "VStack": {
          "elements": [
            {
              "Text": {
                "text": "Mine handlinger"
              }
            },
            {
              "Text": {
                "text": "DEMO-WP1"
              }
            },
            {
              "Text": {
                "text": "Startet — ennå ikke levert",
                "modifiers": {
                  "background": "#DBEAFE",
                  "padding": 6,
                  "cornerRadius": 6
                }
              }
            },
            {
              "Text": {
                "text": "Kjørings-ID: DEMO-RUN-1 (syntetisk)"
              }
            },
            {
              "Text": {
                "text": "Resultatbevis: foreligger ikke"
              }
            }
          ],
          "spacing": 8,
          "modifiers": {
            "padding": 16,
            "background": "#F8FAFC",
            "cornerRadius": 10
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: mine-etter</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · Mine handlinger / etter · syntetiske data"
        }
      },
      {
        "VStack": {
          "elements": [
            {
              "Text": {
                "text": "Mine handlinger"
              }
            },
            {
              "Text": {
                "text": "DEMO-WP1"
              }
            },
            {
              "Text": {
                "text": "Levert — statisk prøveetikett",
                "modifiers": {
                  "background": "#DCFCE7",
                  "padding": 6,
                  "cornerRadius": 6
                }
              }
            },
            {
              "Text": {
                "text": "Kjørings-ID: DEMO-RUN-1 (syntetisk)"
              }
            },
            {
              "Text": {
                "text": "Artefaktbevis: demo-receipt (ikke reell kvittering)"
              }
            }
          ],
          "spacing": 8,
          "modifiers": {
            "padding": 16,
            "background": "#F8FAFC",
            "cornerRadius": 10
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: mine-blokkert</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · Mine handlinger / blokkert · syntetiske data"
        }
      },
      {
        "VStack": {
          "elements": [
            {
              "Text": {
                "text": "Mine handlinger"
              }
            },
            {
              "Text": {
                "text": "DEMO-WP1"
              }
            },
            {
              "Text": {
                "text": "Blokkert",
                "modifiers": {
                  "background": "#FEE2E2",
                  "padding": 6,
                  "cornerRadius": 6
                }
              }
            },
            {
              "Text": {
                "text": "Grunn: maskinbro utilgjengelig (syntetisk)"
              }
            },
            {
              "Text": {
                "text": "Ingen kjøring er startet"
              }
            },
            {
              "Text": {
                "text": "Utførbar/deaktivert knapp inngår ikke i proben"
              }
            }
          ],
          "spacing": 8,
          "modifiers": {
            "padding": 16,
            "background": "#F8FAFC",
            "cornerRadius": 10
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: forklaring-side</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · panel ved siden av · syntetiske data"
        }
      },
      {
        "HStack": {
          "elements": [
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "Valgt punkt: DEMO-WP1"
                    }
                  }
                ],
                "spacing": 8,
                "modifiers": {
                  "width": 260
                }
              }
            },
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "Forklaring til DEMO-WP1"
                    }
                  },
                  {
                    "Text": {
                      "text": "Demotekst — ikke et AI-svar"
                    }
                  },
                  {
                    "Text": {
                      "text": "Kilde: fixture / demo-v1"
                    }
                  },
                  {
                    "Text": {
                      "text": "Utdatert: kilden er endret (prøvetilstand)"
                    }
                  },
                  {
                    "Text": {
                      "text": "Festing/persistens er ikke tilkoblet"
                    }
                  }
                ],
                "spacing": 8,
                "modifiers": {
                  "padding": 16,
                  "width": 300,
                  "background": "#EFF6FF",
                  "borderWidth": 1,
                  "borderColor": "#93C5FD",
                  "cornerRadius": 10
                }
              }
            }
          ],
          "spacing": 12,
          "modifiers": {
            "vAlignment": "top"
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: forklaring-overlay</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · åpent drawer · syntetiske data"
        }
      },
      {
        "VStack": {
          "elements": [
            {
              "Text": {
                "text": "Valgt punkt: DEMO-WP1"
              }
            },
            {
              "VStack": {
                "elements": [
                  {
                    "Text": {
                      "text": "Forklaring — åpent panel"
                    }
                  },
                  {
                    "Text": {
                      "text": "Kilde: fixture / demo-v1"
                    }
                  },
                  {
                    "Text": {
                      "text": "Statisk prøve. Ingen Fest- eller Lukk-handling."
                    }
                  }
                ],
                "spacing": 8,
                "modifiers": {
                  "padding": 16,
                  "width": 280,
                  "background": "#EFF6FF",
                  "cornerRadius": 10,
                  "presentation": {
                    "kind": "drawer",
                    "placement": "trailing",
                    "backdropStyle": "none",
                    "dismissOnBackdrop": false,
                    "escapeKeyBehavior": "disabled",
                    "focusTrap": false,
                    "accessibilityLabel": "Forklaringsprobe"
                  }
                }
              }
            }
          ],
          "spacing": 8,
          "modifiers": {
            "width": 640,
            "height": 360
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>

<details>
<summary>Kandidat: tilstand-visibility</summary>

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "KAPABILITETSPROBE · vis kun blokkert · syntetiske data"
        }
      },
      {
        "List": {
          "elements": [
            {
              "phase": "blokkert"
            }
          ],
          "flowElementSkeleton": {
            "VStack": {
              "elements": [
                {
                  "Text": {
                    "text": "Synlig: for",
                    "modifiers": {
                      "visibility": {
                        "when": {
                          "scope": "item",
                          "keypath": "phase",
                          "equals": "for"
                        }
                      }
                    }
                  }
                },
                {
                  "Text": {
                    "text": "Synlig: under",
                    "modifiers": {
                      "visibility": {
                        "when": {
                          "scope": "item",
                          "keypath": "phase",
                          "equals": "under"
                        }
                      }
                    }
                  }
                },
                {
                  "Text": {
                    "text": "Synlig: etter",
                    "modifiers": {
                      "visibility": {
                        "when": {
                          "scope": "item",
                          "keypath": "phase",
                          "equals": "etter"
                        }
                      }
                    }
                  }
                },
                {
                  "Text": {
                    "text": "Synlig: blokkert",
                    "modifiers": {
                      "visibility": {
                        "when": {
                          "scope": "item",
                          "keypath": "phase",
                          "equals": "blokkert"
                        }
                      }
                    }
                  }
                }
              ],
              "spacing": 8
            }
          }
        }
      }
    ],
    "spacing": 8,
    "modifiers": {
      "padding": 16
    }
  }
}
```

</details>


## 9. Reproduserbarhet og kildeversjoner

Alle kandidater og scenarioer finnes foreløpig under `/private/tmp/plangraf-porthole-capability-20260914/`. JSON-blokkene over bevarer selve kandidatene dersom tempområdet forsvinner. Standardscenarioet er nedenfor; bytt bare kandidatnavnet. Kandidatene er diagnostiske og ikke beregnet på `commit-runtime`.

```json
{
  "configurationName": "HAVEN Workbench",
  "sourceCellEndpoint": "cell:///WorkItem",
  "skeletonFile": "lanes.skeleton.json",
  "viewports": [
    { "name": "web", "width": 1900, "height": 1100 },
    { "name": "smal-web", "width": 780, "height": 1688 }
  ],
  "expects": { "text": ["KAPABILITETSPROBE"] }
}
```

For `lanes` har scenarioet i tillegg tekstforventningene `Gren A`, `WP-A2`, `Gren E`, `WP-E2`. For `grafpiler` har det selectorforventningene `.skeleton-visualization-graph-scene svg line[marker-end]` og `.skeleton-visualization-graph-node`. For `tilstand-visibility` forventes `Synlig: blokkert`, mens scenariohandlingene `expectHiddenText` kontrollerer `Synlig: for`, `Synlig: under` og `Synlig: etter`. Dette er forberedte kontroller, ikke beståtte tester.

Explore-kommandoen som ble brukt per kandidat:

```sh
python3 /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/Explore/skeleton_explore_validator.py \
  --configuration /private/tmp/plangraf-porthole-capability-20260914/lanes.cellconfiguration.json \
  --json-output /private/tmp/plangraf-porthole-capability-20260914/lanes.explore-validation.json
```

SHA-256 for sentrale lokale kilder ved ferdigstilling (full hash, ingen påstand om servert revisjon):

| Kilde, relativt HAVEN | SHA-256 |
|---|---|
| `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift` | `963fa632935d2bf93383d383f68153f84fc2618023deda2e183b5cc9d6bd7575` |
| `CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift` | `b86a5749fd6e04d6ba5ec35d5c413a9237049d4221502c5c57df1fa96f9e9cc0` |
| `CellScaffold/Public/js/skeleton-runtime.js` | `1f1d3e8c93b31e23d5a90750ed97a369d85d39919738099f4a1613f4f4906bd8` |
| `CellScaffold/Public/css/porthole-webo.css` | `af3fe75191a79275ab547666471a8cc0fdadb25243d8a0a383a6f41bc516cf4f` |
| `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift` | `7033de03522f596ae4d805fb2dc1d2480e1e162f987ef5b8c60676cf30185300` |
| `Binding/Binding/SkeletonPresentationOverlayView.swift` | `51f9a7d2852444de3d6938f43eba21b931c79f942eaeb6dcd76b87bbaa1ca12d` |
| `CellProtocolDocuments/Deliverables/PDD_utviklerbenk-oppgavegraf_2026-09-10/FORMAALSSPEC.md` | `c228820bd21029a98258e09e4ac13bb0004dc77b193982d2f424d3f0741794e3` |
| `CellScaffold/scripts/skeleton-iterate.js` | `878d032f3b3c4d2e237b7e540c1a8244d64828f9cff876146fcd1cae5c099d0b` |

Kandidatene har alle `bindings=0`, `errors=0`, `warnings=0` i den statiske Explore-sjekken. Det foreligger **0 previewbilder, 0 gjennomførte viewport-kjøringer og 0 E-akseptansemålinger**.
