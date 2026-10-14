# Plangraf — rendererkontrakt (iterasjon 1, etter kapabilitetskartleggingen)

Kilde: `../evidence/plangraf-porthole/CAPABILITET_RAPPORT.md` (Codex, 2026-09-14, 59 KB, med
fil:linje til `SkeletonDescription.swift`, `skeleton-runtime.js`, `SkeletonView.swift`,
`porthole-webo.css` og `SkeletonPresentationOverlayView.swift`).

**Alt under er kildebekreftet, ikke preview-bevist.** Previewdelen av jobben stoppet: sandkassen
avviste Chromium med `Permission denied (1100)`. Null skjermbilder ble produsert. At en case finnes
i skjemaet og i rendererkoden er derfor ikke det samme som at den er sett kjøre.

## 1. Støttet i dag — kan bygges uten nye skeleton-case

| Komponent i mockupen | Løses av | Kilde |
|---|---|---|
| Lane (rad per gren) | `VStack.elements` med én `HStack.elements` per gren; `ScrollView(axis:"horizontal")` finnes | SkeletonDescription.swift:1240, :1307, :1903; skeleton-runtime.js:582, :1431 |
| Kort med statusmerke og utførerfarge | `VStack`-kort med `Text`-barn; `padding`, `width`, `background`, `borderWidth`, `borderColor`, `cornerRadius`; statusmerket er et eget `Text` med egen bakgrunn | SkeletonDescription.swift:519, :797; skeleton-runtime.js:4127, :4137, :4167 |
| Avhengighet som lesbar referanse | `Text("Avhenger av …")` + piltegn i `HStack` — vanlig tekstlayout | SkeletonDescription.swift:797; skeleton-runtime.js:602 |
| Piler mellom **grafnoder** (web) | `Visualization(kind:"graph")` med `spec.nodes[]`/`spec.edges[]`; SVG-linjer og `marker-end`-pilspiss er innebygd | skeleton-runtime.js:1921, :1947, :3119, :3143 |
| Drilldown-panel | `Section(header, content, footer)` + `VStack`/`Text` som feltliste | SkeletonDescription.swift:1937, :1307; skeleton-runtime.js:1398, :5188 |
| Fire handlingstilstander (før/under/etter/blokkert) | `VStack`/`Text` + `modifiers.visibility.when` (`scope`, `keypath`, `equals`, `allOf`/`anyOf`) velger hvilken som vises | SkeletonDescription.swift:132, :174, :543; skeleton-runtime.js:4192, :4668 |
| Forklaringspanel ved siden av / som skuff | `HStack` med to `VStack`-barn, eller `VStack.modifiers.presentation` med `kind:"drawer"`, `placement:"trailing"`, `focusTrap`, `escapeKeyBehavior` | SkeletonDescription.swift:45, :86, :556; skeleton-runtime.js:4230, :4334; Binding: SkeletonPresentationOverlayView.swift:19 |
| Handlingsknapp (generisk) | `Button(keypath, label, url, payload)` med dynamisk `keypathKeypath`/`labelKeypath`/`payloadKeypath` | SkeletonDescription.swift:1752, :1864; skeleton-runtime.js:1233 |

Ingen `Badge`-, `Card`- eller `Lane`-case er nødvendig. Mockupens visuelle språk kan altså uttrykkes
med dagens format — det er sammenhengen, ikke byggeklossene, som mangler.

## 2. Ikke støttet uten implementasjon — gapliste til Kjetil

Dette er funn, ikke forslag om å bygge. Hvert punkt trenger ditt ord før noen rører rendereren.

1. **Piler mellom vilkårlige kort.** Ingen case eller modifikator binder en linjes endepunkt til to
   `HStack`/`VStack`/`Section`-elementers grenser. `Divider` er en separator, ikke en kant.
   (`SkeletonDescription.swift:2747` er den fullstendige enumen.) Piler finnes bare *inne i*
   `Visualization(graph)`, mellom dens egne noder.
2. **Arbeidspakkekort inne i grafen.** `Visualization(graph)` har ingen kortmal per node, ingen
   lane-layout og ingen egne Utfør/Forklar-knapper per node — den tegner prikk, etikett og én
   nodehandling. `groups` er en etikettstripe, ikke lanes. (skeleton-runtime.js:3165, :3189, :3092)
3. **Grafparitet på Apple-siden.** Den inspiserte Apple-rendereren tegner `Path.addLine` uten
   pilspiss, i en visning med fast høyde 260, uten webens panorering/zoom, og med annen
   auto-plassering. (SkeletonView.swift:2845, :2466 mot skeleton-runtime.js:3847)
4. **Deaktivert knapp med grunn.** `SkeletonButton`/`SkeletonModifiers` har verken `enabled`/
   `disabled`, state-keypath eller grunnbinding. Web har bare ugyldig navigasjonsmål og en
   midlertidig ventetilstand. E3 krever «deaktivert med grunn» — skjult knapp med tekst ved siden av
   oppfyller ikke det, og dempet `opacity` stopper ikke klikk. (SkeletonDescription.swift:1752, :519)
5. **Forankring ved valgt node.** `presentation.anchorRole`/`anchorKeypath` finnes i skjemaet, men
   web normaliserer dem uten posisjonsoppslag, og Binding mapper `.anchor` til `.center`.
   Sidepanel/skuff som generell flate finnes; presis forankring gjør det ikke.
   (skeleton-runtime.js:4264; SkeletonPresentationOverlayView.swift:832)
6. **`openStateKeypath` som bryter.** Feltet normaliseres i web, men åpen tilstand avgjøres av
   elementets synlighet — `visibility.when` er det som faktisk bærer åpen/lukket i dag.
   (skeleton-runtime.js:4285, :4512)

## 3. Uklart — må måles, ikke antas

- Horisontal rulling, tekstklipping og brukbarhet ved 1900×1100 og 780×1688: umålt (ingen preview).
- **Farger er bokstavelige strenger.** `background`, `borderColor` og `foregroundColor` har ingen
  tilsvarende keypath-felt, så automatisk statusfarging fra data er ikke bevist.
  (SkeletonDescription.swift:528, :535, :545)
- Pilgeometri: SVG-en har `viewBox="0 0 100 100"` mens noder plasseres i prosent av beholderen —
  om linjeendene treffer nodene i en bred beholder må avgjøres visuelt. Ikke rapportert som
  observert feil. (skeleton-runtime.js:3121, :3174)
- Drilldown: valg, fil:linje-proveniens per felt, tastatursti og retur til samme utsnitt er umålt.
  `List` har `selectionStateKeypath`/`activationActionKeypath`; `Visualization` har én
  `actionKeypath` — ingen av dem beviser E2s kontrakt.
- Feste/pin: Co-Pilot har allerede `chatHub.ui.pinComponentSurface` / `restoreComponentSurface` med
  lagret UI-tilstand — et reelt gjenbruksfunn, men ikke bevis for E4s bruker-eide element, skop,
  utdatertmerking og uendret chatlogg. (PersonalCopilotConfigurationFactory.swift:1602;
  PersonalCopilotCloudStore.swift:3358)
- Miljøparitet: lokal `/health/build` svarer `unknown` på `app_revision`, `build_timestamp` og
  `environment` — ingen bevist kobling mellom de leste kildefilene og en servert versjon.

## 4. E1–E6, støttegrad

Alle seks står som **delvis**: byggeklossene finnes hver for seg, hele bladets kontrakt er ikke
påvist for noen av dem. Ingen E-verifier er målt grønn. Tabell med begrunnelse per blad i
`../evidence/plangraf-porthole/CAPABILITET_RAPPORT.md` §5.

## 5. Det som gjenstår før dette er en ferdig kontrakt

Preview. Ingen av påstandene over er sett kjøre, fordi Chromium ikke fikk starte i køens sandkasse.
Til det er gjort, er dette en kildelesning — presis, men ikke et rendringsbevis.
