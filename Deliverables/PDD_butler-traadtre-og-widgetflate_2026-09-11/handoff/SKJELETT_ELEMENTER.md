# WP-K2 — Nye skjelettelementer og modifikatorer: listen som skal godkjennes

Iterasjon 7, 2026-09-19. **Alle tre valg avgjort. Kontrakthull lukket etter WP-R1-stopp (§2.1), WP-R2/R3-stopp (§2.2) og integrasjonsfunn (§2.3).** Syntese av `handoff/SKJELETT_GAP_tre.md`,
`SKJELETT_GAP_chat.md` og `SKJELETT_GAP_flate.md` (WP-K1, Codex), korrigert mot
`handoff/ASTRA_SVAR_K2.md` (Astra, 2026-09-18 09:07Z).

**Kjetils ord 2026-09-18:** «Alle tilleggene til skeletonelements er godkjent.
Vi må ha lik tolkning av elementer på web og app. Jeg tror regelen om at app-DnD
er egen PDD var fordi vi skulle løse det på web først. Utvidelsene til WP-R er
også godkjent. Et tillegg vi bør vurdere er å gjøre layoutvalg på bakgrunn av
tilgjengelig plass i til skeletonview. Det er veldig forskjell på hva vi kan vise
på applewatch i forhold til en høyoppløslig widescreenskjerm.»

**Astra-gjennomgangen er kjørt** (`ASTRA_SVAR_K2.md`, 230 linjer). Den fant tre
blokkerende feil i iterasjon 1. Alle tre er rettet her, og de endrer hva som bør
bygges. Godkjenningen står, men **tre valg må tas før WP-R kan starte på E1, E2
og M7** — de står i §6.

## 0. Hvorfor listen finnes

`FORMAALSSPEC.md` §3 navngir fem ting mockupen viser som skjelettformatet ikke
dekker: navigerbart tre med utbretting og tastatur, skop som operasjon over
etterkommere, en widget som fortsetter å følge kilden etter at den er festet,
automatisk kolonnebytte mellom kompakt og full flate, og generisk dra-og-slipp i
appen. Referansebildene i `images/*-v1.png` er **mockups**, ikke Porthole-preview.

**Hva denne listen er, presist** (Astra rettet iterasjon 1 her): den er
*foreslåtte format- og rendererbidrag*. Den leverer **ikke** A3-ruting,
A4-hjelperforslag, B2c-propagering, levende abonnement og persistens (R3),
scenariodata for tom/feil/dra/full, eller alle renderersemantikkene. De står som
egne arbeidspakker i `PLAN.md`. Å si at listen er «det som skal til» var en
overdrivelse.

**Opptelling, rettet:** 2 arkitekturvalg (V1, V2), **11 modifikatorforslag med 25
toppnivå-feltnavn** etter at `clipsToBounds` og `contentClip` er slått sammen, og
**8 arbeidspunkter på tvers av renderer, vert og celle** (ikke «rendereravklaringer
uten formatendring» — R3 er cellearbeid, R5 er vertsintegrasjon, og R8 avhenger av
M6 for spread-delen). Chat-kartet har 49 rader, flate-kartet 26, tre-kartet 24.

### 0.0 Ferskhet — kartene er skrevet mot eldre ref-er

**Dette er det viktigste forbeholdet, og iterasjon 1 hadde det ikke.** Astras
ferskhetskontroll viser at K1-kartene oppgir CellProtocol HEAD `4096760…` og
CellScaffold `origin/main` `649255bb…`, mens de lokale main-ref-ene ved
gjennomgangen var CP `b5b7282b…` og CS `87256f9a…`.

To commits i mellomtiden endrer bildet:

| Commit | Hva den la til | Konsekvens |
|---|---|---|
| CP `cde2e0a` (#34, 2026-09-09) | **tre-`List`** — `childrenKeypath`, `expandedStateKeypath`, `selection*Keypath` | Grunnlaget for V1 vei A finnes allerede |
| CP `f114588` (#26, 2026-09-05) | **itembundne modifikatorer** — `hAlignmentKeypath`, `backgroundKeypath`, `foregroundColorKeypath` | Deler av det kartene beskriver som gap er allerede lukket |

Og avgjørende for rekkefølgen: **CellScaffold main pinner CP `533b42d5…`, og den
bloben har både tre-`List` og fargebindingene.** Det er altså ikke funksjoner på
en framtidig gren — de ligger i den CellProtocol-revisjonen CellScaffold bruker nå.

Det betyr to ting. Web-siden trenger ingen CellProtocol-endring for feltene som
allerede finnes; bare for de fire nye i V1 vei A. Og enkelte «gap»-rader i de tre
kartene kan være lukket siden de ble skrevet. **Presise delpåstander må erstattes
når det viser seg, men hele gapanalysen forkastes ikke** — itembundne farger gjør
ikke padding og fontSize dynamiske, gjør ikke `List` til et fullt tre, og gir
ikke automatisk kolonnebytte.

### 0.0.1 Hva som faktisk er implementert

Iterasjon 1 skrev «ingenting her er implementert». Det var upresist. Riktig:

- **Ingen av de konkrete nye feltnavnene og casene** i §1 og §2 ble funnet i den
  leste skjemalisten.
- **Deler av kapasiteten finnes likevel**: tre-`List` og itembundne
  modifikatorer, jf. 0.0.
- **#243** ligger i lokal CellScaffold-main. Koden lagrer `sourceDescriptor` i
  `PersonalCopilotPinnedWidget` som tråd-UI-tilstand, ikke som kildestyrt
  override, og footeren sier selv «lagret kort, uten løpende oppdatering».
- **Prod er ikke målt i denne runden.** Hva som kjører der er ikke verifisert her.

## 0.1 Hva Astra rettet — og hvorfor det endrer arbeidet

| # | Iterasjon 1 påsto | Kilden bærer |
|---|---|---|
| **B1** | «Uten E1 kan treet bare lages med nestede `List` i endelig dybde, og utbretting kan ikke leveres» | Feil. `List` har allerede `childrenKeypath`, `expandedStateKeypath`, `selectionValueKeypath`, `selectionStateKeypath` og `selectionActionKeypath` (`SkeletonDescription.swift:1424–1448`). Web traverserer barn rekursivt med samme radmal, har ID-oppslag, utbrettknapp med `aria-expanded` og stopper klikkpropagering (`skeleton-runtime.js:6491–6625`). Min påstand gjaldt den **eldre nestede komposisjonen**, ikke denne List-kontrakten. **Det reelle gapet er smalere:** `hasChildren` beregnes fra lastede barn, utbretting er renderer-lokal og ikke cellebekreftet, tastaturmodellen er ufullstendig, semantisk nivå er ikke skilt fra visningsinnrykk — og appens `CellListView` konsumerer ikke feltene i det hele tatt |
| **B2** | «Uten E2 forblir en festet widget et bilde; B2/B2b/B3 kan ikke oppfylles» | Feil som nødvendighetsbevis. `CellConfiguration.skeleton` + `cellReferences` kan holde materialiserte, instansspesifikke undertrær med levende keypath-bindinger. **Gapet er ekte:** dagens main lagrer `sourceDescriptor` i `PersonalCopilotPinnedWidget` som tråd-UI-tilstand, ikke som kildestyrt override, og footeren sier selv «lagret kort, uten løpende oppdatering». Men det beviser at **R3 (cellekontrakten)** mangler, ikke at E2 er løsningen. E2 er begrunnet hvis vi trenger et monteringsregister for **ukjente** komponentdefinisjoner — et videre krav som må skilles fra B2/B2b/B3 |
| **B3** | «T-P1 og T-P2 krever staging med WP-R ute, altså etter merge» | Feil. `skeleton-iterate.js` har `--base-url` og setter working skeleton uten `editor.apply` (`:183–201`, `:858–862`). `Package.swift` støtter `CELLPROTOCOL_LOCAL_PACKAGE_PATH` (`:102–128`), så en testvert kan bygges med CP-kandidaten før merge. `skeleton-element-catalog.spec.js` serverer grenens lokale runtime og CSS med fixturedata (`:11–47`). **Formålstesten kan kjøres før main.** Kravet ditt om testet funksjon og formål før main er dermed oppfyllbart, og K2-8 i iterasjon 1 bortfaller |

Astra rettet også opptellingen: tabellen har **26 toppnivå-feltnavn fordelt på 11
forslag**, ikke 12 felt. Etter sammenslåing av `clipsToBounds`/`contentClip`: 25.

## 0.2 Layoutvalg på tilgjengelig plass — Kjetils tillegg, og Astras samme funn

Kjetil: layoutvalg skal gjøres på **tilgjengelig plass til SkeletonView**, ikke på
klientnavn. Apple Watch og en widescreen-skjerm er ikke samme sak.

Astra kom til det samme uavhengig: *«`web/app` er en klientkategori, ikke
automatisk en breddeklasse: en smal webflate og en bred native flate må ikke få
feil layout bare på grunn av rendererens navn.»*

Det er ikke et tillegg til M7. **Det er rettelsen som gjør M7 riktig.** M7 er
omskrevet under. To ting skilles, fordi de er forskjellige:

- **Plass avgjør layout.** Målt tilgjengelig bredde og høyde til elementet, med
  deklarerte terskler. Dette er portabelt og gjelder begge klienter likt.
- **Kapabilitet avgjør interaksjon.** Peker/hover, tastatur, berøring, dra-og-slipp,
  begrenset skjermtid. En Apple Watch har ikke hover uansett hvor bred den er.

Det svarer samtidig på «vi må ha lik tolkning av elementer på web og app»: samme
JSON, samme målte plass, samme valg. Ulik layout er tillatt når plassen er ulik;
ulik oppførsel er det ikke (C1, `lesson.parity-was-correctness-not-decoration`).

---

## 1. Treet og den levende widgeten

Astra viste at begge disse ble lagt fram som nødvendige uten at kilden bar det.
De er skrevet om som **valg med to veier hver**, med det reelle gapet navngitt.

### V1 — Treet: **AVGJORT 2026-09-18 — ny `Tree`-case (vei B)**

Kjetils ord: «Jeg tror det er lurt å lage en Tree - case.» Claude anbefalte vei A
(utvide `List`); Kjetil valgte B. Begrunnelsen som bærer valget er sterkere enn
den jeg ga for A: `List` bærer allerede radskall, gap, valg- og
aktiveringskontroller — M3 finnes nettopp fordi de er i veien — så et tre med full
tastaturkontrakt inne i det skallet blir en case med to personligheter. En egen
case gir i tillegg den gjenbrukbare kontrakten C2 krever, og den har **to**
konsumenter fra dag én: Butlers hjelpertre og utviklerbenkens oppgavetre.

Det vei A-argumentet fortsatt koster oss: L i stedet for M, to
rendererimplementasjoner, egen audit-gren, og tilgjengelighet som må bygges fra
bunnen i begge klienter. Det er prisen, og den er akseptert.

**Det som allerede finnes** (`SkeletonDescription.swift:1424–1448`, web
`skeleton-runtime.js:6491–6625`): `childrenKeypath`, `expandedStateKeypath`,
`selectionValueKeypath`, `selectionStateKeypath`, `selectionActionKeypath`.
Web traverserer barn rekursivt med samme radmal, slår opp på ID, tegner
utbrettknapp med `aria-expanded` og stopper klikkpropagering ved utbretting.

**Det som faktisk mangler, uansett vei:**

| # | Gap | Hvorfor det betyr noe |
|---|---|---|
| G1 | `hasChildren` beregnes fra **lastede** barn | En node med ubesøkte barn ser ut som et blad. Pilen mangler til dataene er hentet |
| G2 | Utbretting er **renderer-lokal**, ikke cellebekreftet | To flater for samme bruker viser ulik utbretting; tilstanden overlever ikke |
| G3 | **Ingen tastaturmodell** | Opp/ned/Home/End/venstre/høyre/Enter mangler. Ingen fokus ved ID, ingen scroll-til-fokusert |
| G4 | **Semantisk nivå ikke skilt fra visningsinnrykk** | `aria-level` og innrykk er samme tall i dag. Butler-roten og de fire øverste samtalene har begge innrykk 8 i referansen — dybde × 16 gir feil bilde |
| G5 | **Appen konsumerer ikke feltene** | `CellListView:172–193` leser hverken `childrenKeypath` eller `expandedStateKeypath`. Samme JSON gir tre på web og flat liste i app. Dette er C1-brudd, ikke pynt |

**Vei A — utvid `List` (ikke valgt).** Legg til `hasChildrenKeypath`, `expansionActionKeypath`,
`levelKeypath`, `leadingInsetKeypath` på eksisterende `SkeletonList`, gjør
utbretting cellebekreftet, bygg tastaturmodellen i web-rendereren, og implementer
feltene i `CellListView`.
*For:* ingen ny case, ingen ny audit-gren, web er nesten der. *Mot:* `List` bærer
allerede radskall, gap, valg- og aktiveringskontroller (M3 finnes nettopp fordi de
er i veien), og et tre med full tastaturkontrakt inne i et listeskall blir en case
med to personligheter.

**Vei B — ny `Tree`-case (VALGT).** Over en ferdig ordnet synlig nodeliste fra
cellen. Rendereren filtrerer ikke og traverserer ikke; den tegner rader og eier
radens hitflate, utbrettpilen og fokus. Radmalen eier etikett, prikk, merke og
teller. Feltlisten (fra `SKJELETT_GAP_tre.md`, gjentatt her så kontrakten står
alene — Astra påpekte at iterasjon 4 bare viste til den):

| felt | type / semantikk |
|---|---|
| `keypath` | `String` — cellens synlige, ordnede noder |
| `idKeypath`, `parentIDKeypath` | `String` — stabile instans-ID-er, nullable forelder. Identitet er ikke indeks |
| `levelKeypath` | `String` — semantisk nivå (rot = 1) for tilgjengelighet, atskilt fra visningsinnrykk |
| `leadingInsetKeypath` | `String` — ferdig beregnet innrykk fra item |
| `hasChildrenKeypath`, `expandedKeypath` | `String` — booleans. `hasChildren` er ikke antall lastede barn |
| `selectedIDStateKeypath`, `selectionActionKeypath` | `String` — les valgt ID fra cellen, send `{nodeID:String}` |
| `expansionActionKeypath` | `String` — send `{nodeID:String, expanded:Bool}`, vent på cellebekreftet liste |
| `rowSkeleton` | `SkeletonVStack` — én radmal med itemdata |
| `disclosureModifiers`, `rowModifiers`, `modifiers` | `SkeletonModifiers?` |
*For:* rendereren eier radens hitflate, disclosure og fokus uten listeskall; ren
kontrakt for gjenbruk. *Mot:* to rendererimplementasjoner, ny audit-gren,
tilgjengelighet og oppdateringsatferd må avstemmes fra bunnen. L.

**Uansett vei** må dette spesifiseres, og det er ikke gjort: hva som skjer ved
**forsinket innlasting av barn** (loading/error-kontrakt), og at **fokus flyttes
til forelderen** når et fokusert barn skjules fordi forelderen lukkes.

**Til gjenbruk i utviklerbenken** mangler én ting Astra navnga: en
**flyttehandling**. `PDD_utviklerbenk-oppgavegraf_2026-09-10` krever at en idé kan
få forelder og flyttes med hele undertreet, med syklusavvisning. Verken vei A
eller B har den. Den trenger ikke være et skjemafelt — en `Button` i radmalen kan
kalle cellens `move(nodeID, newParentID)` — men den må navngis, og cellen eier
sykluskontrollen.

### V2 — Levende festet widget: **AVGJORT 2026-09-18 — R3 *og* `ComponentSurface` (vei B)**

Kjetils ord: «V2: R3 og `ComponentSurface`». Claude anbefalte A (bare R3 nå);
Kjetil valgte B. Det betyr at monteringsregisteret bygges nå, ikke senere.

**Konsekvenser som må med i WP-R:** `sourceKeypath` alene avslører ingen
handlinger, så auditen (T-F2) må se den **oppløste** definisjonen — ellers blir
B4 uetterprøvbar. Og kildeidentitet må skilles fra instansidentitet: to instanser
fra samme kilde skal kunne skilles, så `componentID` trenger en `instanceID` ved
siden av seg. R3 bygges uansett; den er ikke erstattet av E2.

**Gapet er ekte og målt.** Dagens main lagrer `sourceDescriptor` i
`PersonalCopilotPinnedWidget`, men koden sier selv at det er requester- og
tråd-UI-tilstand — **ikke** en kildestyrt CellConfiguration-override. Program- og
statrader settes til tomme lister, og footeren sier «lagret kort, uten løpende
oppdatering». **B2 er ikke oppfylt**, og å telle #243 som full B2b er misvisende
mot B2b-teksten, som krever Portholens CellConfiguration.

**Vei A — bare R3 (cellekontrakt).** `CellConfiguration.skeleton` +
`cellReferences` holder materialiserte, instansspesifikke undertrær med levende
keypath-bindinger. R3 leverer abonnementsvei, eierskap, persistens, siste kjente
verdi og feil.
*For:* ingen formatendring. Dekker de **to kjente** innholdsmalene (programrader,
statrader). *Mot:* hver ny korttype må materialiseres på nytt.

**Vei B — R3 **og** `ComponentSurface`.** I tillegg et monteringsregister som slår
opp en versjonert definisjon med stabil ID og revisjon.
*For:* nødvendig hvis en flate skal kunne montere en komponentdefinisjon den ikke
kjenner på forhånd. *Mot:* L, og `sourceKeypath` alene avslører ingen handlinger —
auditen må se den **oppløste** definisjonen, ellers blir B4 uetterprøvbar.

**R3 skal bygges uansett vei.** Og hvis vei B velges: kildeidentitet må skilles
fra instansidentitet. To instanser fra samme kilde skal kunne skilles; iterasjon 1
oppga `componentID`, men ingen `instanceID`.

---

## 2. Modifikatorfeltene — godkjent, med Astras presiseringer

11 forslag, 25 toppnivå-feltnavn etter sammenslåing. Disse er ukontroversielle i
Astras gjennomgang bortsett fra der det står noe annet, og de er **godkjent**.

| ID | Felt | Presisering fra Astra |
|---|---|---|
| **M1** | `paddingInsets: SkeletonInsets?` | Behold, men **ikke** som «umulig uten». Asymmetrisk plass *kan* komponeres med indre/ytre beholdere — tre-kandidaten gjør det allerede (5+3/11/27). M1 er direkte uttrykk i stedet for komposisjon, og fjerner en klasse tomme hjelpeflater |
| **M2** | `fontFamilies`, `lineHeightMultiple`, `letterSpacing`, `numericVariant: enum(proportional, tabular)?` | **`numericVariant` avklart 2026-09-19, se §2.1.** Reelt gap for eksakte verdier. Webens `fontStyle:"body"` har alt 1.45 linjehøyde, men det er en typografirolle, ikke garanti om native linjeboks. Tre-kartets absolutte 15 px linjeboks uttrykkes som forholdet 15/11 ved fontSize 11 — **hvis** multiplumkontrakten gjelder linjeboksen. Det må defineres, ikke antas. Fonttilgjengelighet i Binding er ukjent og avgjøres av pikseltesten |
| **M3** | `itemSpacing`, `rowInsets`, `rowDecoration` | Betinget. For data uten `List`s valg/aktivering finnes en mindre vei: énkolonnes `Grid` med `spacing`, som i appen bruker `LazyVGrid` uten `CellListView`s radpadding og ScrollView. **M3 løser ikke tomlisteteksten og heller ikke hvem som eier scrollingen** — `rowDecoration:none` skal ikke tolkes som «ingen ScrollView og ingen «Ingen elementer»-tekst». Det må avtales separat |
| **M4** | `minHeight`, `maxHeight`, `minWidth`, `flexGrow` | Behold. **`clipsToBounds` slås sammen med M6 `contentClip`** — én klippekontrakt, ikke to nesten like booleans. Avklar først eksisterende fyllingssemantikk (`Spacer`, Grid flexible-spor, `maxHeightInfinity` = max-height 100 % på web, native som utvider begge akser) før alt tilskrives nytt `flexGrow` |
| **M5** | `controlStyle`, `accessibilityLabel` | Skill de to. Navngapet er ekte: referansen viser bare ⤢ og ✕, og `SkeletonPresentation.accessibilityLabel` navngir presentasjonen, ikke en vanlig knapp. Men **`controlStyle:plain` skal ikke være forutsetningen for å rette R8** — at `borderWidth:0` ignoreres av webens `>0`-vakt er en feil som rettes for seg |
| **M6** | `borderStyle`, `shadowSpread`, `borderEdges`, `contentClip` | Behold. `borderEdges` er en forenkling, ikke eneste vei — kanter kan komponeres som tynne flater. Stiplet kant og spread-ring med null blur mangler derimot portable felt helt |
| **M7** | **omskrevet, se under** | |
| **M8** | `interactionStyles {hover, focusVisible, dragSource, dragActive}` | **Avklart 2026-09-19, se §2.1.** `dragging` er delt i to navngitte tilstander. `dragSource` gjelder når **dette** elementet er drakilden (kortet dimmes til 0.42). `dragActive` gjelder når **en hvilken som helst** dragoperasjon pågår i verten (`.msgs` til 0.82, `.composer` til 0.5 mens noe annet dras). Fravær = ingen stilendring |
| **M9** | `textDecoration`, `textTransform`, `textRotationDegrees` | `textTransform` **utsettes** — cellen leverer ferdig tekst for den faste starteroverskriften. De to andre beholdes. Understrek alene løser ikke inline tekstflyt rundt to knapper; `Text.url` skal ikke omtolkes til en handling |
| **M10** | `leadingMarker` | Behold for eksakt markørgeometri. **Rettelse:** A2 (skop) stopper ikke uten den — skopvalg og loggfiltrering virker uansett. Det er det visuelle skillet mellom valgt og i-skop som avhenger av den |
| **M11** | `paddingLeadingKeypath` | Utsettes hvis V1 gir innrykk fra data. Web har allerede dybdebasert innrykk, men ingen itemlest leading-padding i skjemaet |

### 2.1 To kontrakthull lukket 2026-09-19

WP-R1 (Astra, 2026-09-18 14:26–14:30Z) stoppet før implementering på to steder
der kontrakten ikke var bestemt nok til å bygge etter. Stoppen var riktig — jobben
var bedt om å stoppe framfor å finne på en variant. Begge hullene var i denne
kontrakten. Claude avgjør dem her med begrunnelse; **Kjetil kan overstyre begge.**

**M2 — `numericVariant`: `proportional` / `tabular`, og `nil` betyr skriftens standard.**

Kildene var uenige: tre-kartet sa `proportional/tabular`, flate-kartet
`normal/tabular`. Valget er `proportional/tabular` fordi `normal` ikke er entydig:
det betyr «skriftens standard», og den er proporsjonal i noen skrifter og tabulær
i andre. Formålet med feltet er identisk rendering på web og app, og da kan ikke
en verdi bety forskjellige ting i forskjellige skrifter. Begge valgte verdier er
navngitte OpenType-egenskaper (`pnum`, `tnum`) med direkte motpart på web
(`font-variant-numeric: proportional-nums | tabular-nums`) og i SwiftUI
(`monospacedDigit()` for tabulær). Tre tilstander, uten en uklar mellomting:
fravær (skriftens standard), `proportional`, `tabular`. T-F1 skal avvise `normal`
som ugyldig verdi.

**M8 — `dragging` deles i `dragSource` og `dragActive`.**

Mockupen trenger begge, og de er forskjellige tilstander: kortet som dras dimmes
til 0.42, mens meldingslisten dimmes til 0.82 og komponisten til 0.5 **når noe
annet dras**. Astra foreslo `draggingScope: self | global` som ett felt med et
valg. Valget her er i stedet **to navngitte nøkler**, fordi det lar et element ha
begge stilene samtidig uten at et scope-felt må ha en skjult default, og fordi
fravær av hver nøkkel da er entydig testbart.

- `dragSource` — stilen gjelder når **dette** elementet er drakilden.
- `dragActive` — stilen gjelder når **en hvilken som helst** dragoperasjon pågår i
  verten. Hvor det vites fra: R4, vertens kortlivede dragkontekst. Uten R4 har
  ingen renderer grunnlag for `dragActive`, så **M8 og R4 må leveres sammen**.
- Hvis begge gjelder samtidig (elementet dras, og det er en drag i verten — noe
  som alltid er sant når det dras), vinner `dragSource`.
- Samme begrensede stilstruktur som `hover` og `focusVisible`: `background`,
  `foregroundColor`, `opacity`. Ingen actions, ingen datafiltrering.

### 2.2 `ComponentSurface` — runtimebinding (lukket 2026-09-19)

WP-R2 og WP-R3 stoppet begge 2026-09-19 03:35–03:39Z på samme hull, og riktig:
kontrakten sa hvem en montering *er* (`componentID`, `revision`, `instanceID`),
men ikke hvordan en montering *får data* og *hvor handlingene går*. Astras
eksempel: to instanser av samme definisjon har `Text.keypath = "title"` og
`Button.keypath = "actions.refresh"`. Hvilken rot leser `title` fra, og hvilket
mål får `actions.refresh`? Vertsoppslag, omskriving av keypaths og en egen
dispatcher per instans gir tre forskjellige svar. Web og native kan ikke velge
hver sin.

**1. Hva verten leverer.** Verdien på `sourceKeypath` — løst som enhver annen
keypath, item først og så root — er en monteringsbeskrivelse levert av cellen
(R3-cellekontrakten). Rendereren slår aldri noe opp selv.

```
SkeletonComponentMount
  componentID         String         definisjonens identitet
  revision            String         definisjonens versjon
  sourceCellEndpoint  String         cellen som eier dataene og tar imot kildehandlinger
  skeleton            SkeletonElement definisjonen, uendret og lik for alle instanser
  item                ValueType?     DENNE instansens data
```

**2. Databinding: som en `List`-rad med nøyaktig ett item.** Inne i den monterte
definisjonen løses keypaths slik de gjør i en `List`-rad i dag: `item` er
monteringens `item`, `root` er vertens root, og oppslaget går item først og så
root. **Ingen ny oppslagsregel, og ingen omskriving av keypaths.** Mangler `item`,
løses keypaths bare mot root, slik en rad uten treff gjør.

Hvorfor dette og ikke de to andre:
- *Omskriving* (`title` → `widgets.<instanceID>.title`) ville gjøre definisjonen
  forskjellig per instans. Da betyr `revision` ingenting lenger, og hele poenget
  med en versjonert definisjon (V2-B) faller.
- *Egen dispatcher per instans* ville vært en ny mekanisme på siden av den som
  finnes.
- Item/root-regelen **finnes allerede**, og R2 i §3 gjør den lik på web og native.
  Paritet for monterte komponenter kommer dermed fra en rettelse som alt er i
  omfanget — ikke fra en ny.

**3. Handlingsbinding: kildehandlinger går til kildecellen.** En `Button` eller
annen handlings-keypath inne i definisjonen sendes til `sourceCellEndpoint`,
ikke til vertens celle. Monteringsmetadata `{instanceID, componentID, revision}`
følger som et eget felt `mount` **ved siden av** `payload` — aldri flettet inn i
brukerens payload. **Kildecellen avgjør tilgangen.** Nektes den, er det samme
Agreement-challenge som for enhver annen cellehandling.

Grunnlaget er Kjetils egen beslutning 2026-09-12 i `PDD_mcp-tilgangsbevis`:
*«Keypath er datareferanse uten egen autoritet; tilgang avgjøres av hver celle
ved traversering.»* Alternativet — at alle handlinger går til vertens celle som
videresender — ville lagt autoriteten hos verten som mellommann, og da er det
vertens grant som teller, ikke brukerens. Det strider mot den beslutningen.
**Kjetil kan overstyre; dette er det ene valget i §2.2 han kanskje vil se på.**

**Vertshandlinger bor utenfor definisjonen.** Løsne, full flate, flytt og fest
(`chatHub.widgets.unpin`, `…toggleFullSurface`, `…pinFromDrop` i dag) ligger i
vertens skjelett *rundt* `ComponentSurface`, ikke inne i definisjonen. Det holder
definisjonen flyttbar mellom verter, og det er slik #243 allerede er bygget.

**4. Kildeoppdatering.** Endres verdien på `sourceKeypath` med nytt `item` og
samme `instanceID`, oppdaterer rendereren på stedet. Identitet er **alltid**
`instanceID` — aldri indeks i en liste, aldri objektidentitet. Endres `revision`,
monteres definisjonen på nytt, men `instanceID` beholdes, og fokus, scroll og
utkast bevares der elementet fortsatt finnes.

**5. Felles fixture**, som begge rendererjobbene ba om:
`fixtures/skeleton-wp-r1/component-mount-two-instances.json` i CellProtocol. To
`ComponentSurface` med ulik `instanceID`, begge montert fra samme
`componentID`/`revision`, med ulikt `item` (`title: "Program"` og
`title: "Sesjoner"`), og en `Button` med `keypath: "actions.refresh"`.
Forventet: A viser «Program», B viser «Sesjoner»; knappen i A sender til
`sourceCellEndpoint` med `mount.instanceID = A`. Deretter en kildeoppdatering som
endrer A sitt `item` og lar B stå — begge identiteter uendret. Fixturen er fasiten
for T-F3 på **begge** klienter.

**Det åpne punktet rendererjobbene skal rapportere, ikke stoppe på:** om web i dag
har en vei til å sende en handling til en *annen* celle enn Portholens egen.
`/browserhead/porthole/action` går til Portholens celle. Finnes ikke veien, er
det et funn for kildehandlinger i `ComponentSurface` — ikke en grunn til å stoppe
`Tree`, M1–M10 eller layoutkonteksten.

### 2.3 Integrasjon — avgjort 2026-09-19 etter WP-R2c

**Offentlige konfigurasjoner avviser både `Tree` og `ComponentSurface`.**
`ConferencePublicConfigurationPolicy` slipper bare gjennom det som er
skrivebeskyttet: interaktive `List` avvises («public lists must be read-only»),
og `Reference` avvises fordi den løser opp nestede skjeletter. Et `Tree` har
**alltid** `selectionActionKeypath` og `expansionActionKeypath` — begge er
obligatoriske i formatet — så det kan aldri være skrivebeskyttet. En
`ComponentSurface` monterer en ekstern definisjon og sender kildehandlinger til
en annen celle, som er nøyaktig det `Reference`-regelen stenger for. Dette er
ikke et nytt valg; det følger av reglene policyen allerede har. Nye modifikatorer
tilfører ingen nye handlingsveier (`layoutVariants` og `interactionStyles`
avviser actions i formatet), så modifikatorsjekken er uendret.

**Kildehandlinger til fjerne celler er utsatt, og låst.** `Meddle` har bare
`get(keypath:requester:)` og `set(keypath:value:requester:)`; det finnes ingen
kanal for monteringsmetadata over broen. Lokale celler (`cell:///…`,
`cell://localhost/…`) fungerer. Fjerne endepunkter avvises med 501 før oppslag,
og WS/WSS godtas ikke som kildeendepunkt — ingen fallback til verten. Butlers
widgets monteres fra lokale celler, så dette blokkerer ikke leveransen. Å føre
metadata over broen er en portabel CellProtocol-endring og tas som egen oppgave
når en fjern kilde faktisk trengs. Grensen skal stå navngitt i `ACCEPT.md`.

**`ChatCell`-kollisjonen er ikke fra WP-R.** CellProtocol main har fått
`public final class ChatCell` i CellBase, som kolliderer med `App.ChatCell` i
testmål som importerer begge. CellScaffold main pinner fortsatt en eldre
CellProtocol (`533b42d5`), så dette slår inn ved **enhver** pinoppdatering — ikke
bare denne. Rettes med kvalifisert navn i testene.

### M7 omskrevet — `layoutVariants` på målt plass

**Dette er ikke lenger `viewportClass`.** Varianten velges på **målt tilgjengelig
plass til elementet**, med deklarerte terskler, pluss et separat
kapabilitetsfilter.

```
layoutVariants: [SkeletonLayoutVariant]?

SkeletonLayoutVariant:
  when            SkeletonCondition?        // itemdata, eksisterende betingelser
  minAvailableWidth   Double?               // målt plass til DETTE elementet
  maxAvailableWidth   Double?
  minAvailableHeight  Double?
  maxAvailableHeight  Double?
  requiresCapability  [enum(pointer, hover, keyboard, drag, touch)]?
  // typede overstyringer, ingen vilkårlig CSS, ingen nye actions:
  axis, columns, spacing, paddingInsets, minHeight, maxHeight, flexGrow,
  fontSize, borderColor, foregroundColor
```

Deterministisk **første treff**; grunnlayout når ingen treffer. Samme instans,
samme skop, samme utkast, samme valgte rad og samme kildeabonnement skal overleve
et variantskifte — det er akseptkravet, ikke at layouten endrer seg.

**Astras innvending står:** full/kompakt *kan* løses i dag med `visibility.when`
over to Grid-undertrær i itemkontekst. M7 er en vedlikeholdsgevinst som unngår
dupliserte maler — **ikke** et bevis for at B3 ellers er umulig. Det som gjør M7
verdt å bygge er plass-argumentet: dupliserte maler per klientnavn skalerer ikke
til klokke, telefon, nettbrett, laptop og widescreen, og de gir feil svar for en
smal webflate og en bred native flate.

**Avgjort 2026-09-18 (V3-A): verten deklarerer én containerstørrelse som
kaskaderer.** Rendereren måler ikke per element. Verten setter
`availableWidth`/`availableHeight` i en layoutkontekst på roten; containere som
kjenner sin egen størrelse — Grid-spor, faste panelbredder, en drawer med
deklarert bredde — snevrer konteksten inn for sine barn. Deterministisk og
testbar uten `ResizeObserver` og uten `GeometryReader` per element, og **samme
mekanisme i begge klienter**.

Prisen, som må stå: et element kan ikke reagere på plass ingen forelder har
deklarert. Når en container ikke snevrer inn, arver barnet forelderens tall. Det
må testes eksplisitt — en widget i en 236 px kolonne skal ikke tro den har hele
flatens bredde.

---

## 3. Rendereravklaringer — «lik tolkning på web og app»

Kjetils krav 2026-09-18. Dette er ikke pynt: `lesson.parity-was-correctness-not-decoration`.
Astra presiserte at disse **ikke** alle er ren rendererjobb — R3 er cellearbeid og
R5 er vertsintegrasjon, så «8 rendereravklaringer uten formatendring» var feil.
Riktig: **8 arbeidspunkter på tvers av renderer, vert og celle.**

| ID | Avklaring | Eier |
|---|---|---|
| **R1** | Numerisk og navngitt `fontWeight` tolkes likt. I dag blir `"600"` regular i appen | renderer ×2 |
| **R2** | `List`-radoppslag likt: appens `getElements()` mangler radkonteksten web har | renderer ×2 |
| **R3** | Cellekontrakt kilde → instans: materialisering, persistens, abonnementslevetid, feil, siste kjente verdi. **Bygges uansett hvilken vei V2 tar.** L | celle |
| **R4** | Vertens kortlivede dragkontekst: marker **alle** aksepterende flater fra dragstart til cancel/drop. Cellen validerer operasjonen — `dropValidationState` stanser den ikke i dag | vert + celle |
| **R5** | Vertskontrakt for full flate: kolonner, dokket chat, retur uten identitetstap. **M7 fjerner ikke dette arbeidet** | vert |
| **R6** | Binding-adapter for generisk drag/drop. **Sekvensert etter web** (se under) | app |
| **R7** | `vAlignment: firstTextBaseline` får definert betydning i begge. Appens `HStack` er hardkodet `center` | renderer ×2 |
| **R8** | `borderWidth: 0` fjerner faktisk webens CSS-kant; `shadowSpread` virker med `shadowRadius: 0`. **Avhenger av M6 for spread-delen** | renderer (web) |

**App-DnD, rettet etter Kjetils ord:** avgrensningen betyr **sekvensering, ikke
utelatelse** — web først, så app. Astras forbehold står likevel: så lenge R6 ikke
er levert, kan native drag/drop **ikke** telles som bestått T-F3, og avviket må
stå som en navngitt unntaksrad i `ACCEPT.md`, ikke som stilltiende godkjent.

**Fire hull Astra fant som ingen av M1–M11 eller R1–R8 dekker,** og som må ha en
eier før G3: tomlistetekst og eget rullefelt i `List`; intrinsisk størrelse og
tekstflyt (nowrap på chip, actionlenker i tekstflyt); TextArea-dobbeltdekorasjon
og faktisk kortpreview under dra; og tre-oppdateringens loading/error- og
fokuskontrakt.

---

## 4. Testkontrakt før main i CellProtocol

Kjetils krav: testet mot funksjon **og formål** før implementasjonen dyttes til
main i CellProtocol. **Astra viste at dette er gjennomførbart** — iterasjon 1 tok
feil da den kalte det en rekkefølgekonflikt.

**Veien før main, kildebelagt:**

1. `skeleton-element-catalog.spec.js` serverer grenens **lokale** runtime og CSS
   med fixturedata og samler opp `onAction` — webfunksjon og visuelle tester uten
   staging.
2. `Package.swift` støtter `CELLPROTOCOL_LOCAL_PACKAGE_PATH`, så en **lokal
   testvert** kan bygges med CellProtocol-kandidaten. `skeleton-iterate.js` har
   `--base-url` og setter working skeleton uten `editor.apply`.
3. Native bevis krever at CP-grenens renderer faktisk kjører i en Binding-/testvert
   med samme kandidat og samme data. **`SkeletonParityRenderer.renderPNG` alene
   beviser ikke T-F3** — den bygger en ny `PortholeViewModel` og har ingen
   parameter for nodeliste eller action-driver.

| Port | Hva den beviser | Astras korreksjon |
|---|---|---|
| **T-F1 format** | Codable tur-retur; ugyldig verdi avvises; fravær gir dokumentert default | Test **«ingen uventede `Unsupported` og ingen tapte obligatoriske felt»**, ikke bare at `JSONDecoder` lykkes — elementdekoderen kan gjøre en feil om til `Unsupported` i stedet for å kaste. At også gammel `padding` skal kaste ved feil **endrer dagens kompatibilitetsatferd** og må navngis som egen endring |
| **T-F2 nåbarhet** | Auditen utvides med barne-/radkontekst og elementets egne actions | For V2 vei B må den **oppløste** definisjonen inngå — `sourceKeypath` alene avslører ingen handlinger. Negative tester må vise at utelatt action faktisk oppdages |
| **T-F3 funksjon ×2** | Virkelige interaksjoner i begge renderere: payload, bekreftet tilstand, fokus, utbretting, tastatur, tilgjengelig navn, kildeoppdatering | En PNG er ikke en native funksjonstest. Test også at skjulte varianter ikke eksponerer doble handlinger |
| **T-P1 formål** | Navngitt formål + målbart signal | **Ikke krev pikselflytt for hvert felt.** `accessibilityLabel`, stabile ID-er, utbrettingsaction og levende binding forbedrer formålet uten å endre et statisk referansebilde. Visuelle felt måles mot referansen med samme data, panelmål, skala og font |
| **T-P2 innganger** | Faktisk alternativ inngang fra samtalen med riktig instans og payload | `reachableActionKeypaths` over GUI-skjelettet beviser **ikke** at samtalen kan utløse handlingen. B4 gjelder alle widgethandlinger, også de som er komponert og de som går gjennom drop-modifiers |

**Rekkefølge (Astras, vedtatt her):** godkjent redusert kontrakt → CP-, web- og
native-kandidater med registrerte revisjoner → T-F1/T-F2 → grenens web- og
native-funksjon → T-P1/T-P2 mot isolert testvert → **først deretter CP-main**.
CellScaffold-PR-en bærer integrasjonsbeviset uten å måtte merges først.
Miljøverifikasjon etter deploy kommer i tillegg og erstatter ikke pre-main-kravet.

---

## 5. Hva som bevisst *ikke* står på listen

- **Ingen ny generell evaluerings-, regne- eller traverseringsmotor.** (Rettet
  ordlyd: iterasjon 1 sa «ingen betingelser i JSON», som var feil — formatet har
  allerede `equals`/`allOf`/`anyOf`/`not`, og M7 gjenbruker dem.)
- **Ingen ny `Card`-case.** Stacks, Grid og Button beskriver kortet. Dette er
  **ikke** et indirekte argument for at E2 likevel må til.
- **Ingen ny `Error`-case.** Feildata og actions komponeres — men 0/1-repetisjon
  og inline layout må faktisk virke.
- **Ingen ny `Disclosure`-case.** Utbrettingen hører til V1, uansett hvilken vei
  som velges.
- **Ingen `full` i `SkeletonPresentationKind`.** Presentasjonsfeltene beskriver
  presentasjon, ikke kolonner eller dokking.
- **Ingen gjettet breakpoint, og ingen `viewportClass` i det portable formatet.**
  Plass måles; klientnavn brukes ikke som breddeklasse.
- **`textTransform`** utsettes; cellen leverer ferdig tekst.

**Og det denne listen *ikke* leverer, som iterasjon 1 overdrev:** A3-ruting,
A4-hjelperforslag, B2c-propagering, liveabonnement og persistens (R3),
scenariodata for tom/feil/dra/full, og flere av renderersemantikkene. Dette er
foreslåtte format- og rendererbidrag; øvrige celle- og vertsavhengigheter står i
`PLAN.md` som egne arbeidspakker.

---

## 6. Valgene

Godkjenningen din står for M1–M11 og for WP-R-utvidelsene. Disse tre endrer hva
som bygges, og Astras gjennomgang gjør dem til reelle valg framfor formaliteter.

| # | Valg | Claudes anbefaling |
|---|---|---|
| ~~V1~~ | ~~Treet~~ | **Avgjort 2026-09-18: ny `Tree`-case.** Se §1 V1 |
| ~~V2~~ | Levende widget: **A** bare R3 (cellekontrakt), eller **B** R3 **og** `ComponentSurface` | **A nå, B senere hvis behovet melder seg.** R3 må bygges uansett og er det som faktisk mangler. E2 er begrunnet først når en flate skal montere en definisjon den ikke kjenner på forhånd — det er ikke tilfellet for programrader og statrader |
| ~~V3~~ | ~~Plassmåling~~ | **Avgjort 2026-09-18: verten deklarerer én containerstørrelse som kaskaderer (vei A), begge klienter.** Dette fjerner tomekanisme-problemet jeg flagget: samme regel på web og native, ingen `ResizeObserver` mot `GeometryReader` å holde i synk, og ingen SwiftUI-layoutsykluser fra per-element-måling. Prisen er at et element ikke kan reagere på plass en forelder ikke har deklarert — containere som kjenner sin egen størrelse (Grid-spor, faste panelbredder) må derfor snevre inn konteksten videre nedover |

**Alle tre er avgjort 2026-09-18: V1-B (ny `Tree`-case), V2-B (R3 *og*
`ComponentSurface`), V3-A (vertsdeklarert containerstørrelse som kaskaderer).**
WP-R er satt i gang; første jobb ligger i `_losen-queue` som
`wp-r1-format-20260918`.

**Følger av V1-B som må med i WP-R:** `Tree` skal ikke arve `List`s radskall —
rendereren eier radens hitflate, disclosure og fokus direkte. M3 (`itemSpacing`,
`rowInsets`, `rowDecoration`) trengs derfor **ikke** for treet, men fortsatt for
widgetradene i flaten. Auditen får en egen gren for `Tree` (T-F2), og
tastaturmodellen i §1 er en del av akseptansen, ikke en senere forbedring.

---

## 7. Det jeg fortsatt ikke vet

- Hvilke skrifter som faktisk er tilgjengelige i Binding og i referansenes
  Chromium. Samme fontnavn er ikke fontbevis.
- Om M2s `lineHeightMultiple` faktisk styrer linjeboksen eller bare avstanden.
  15/11-konverteringen forutsetter det første.
- Hva `.inscope` på Arendalsuka betyr når den noden ligger over den valgte
  Program-noden, og om `.sel` på både Butler og Program betyr flervalg. A2 sier
  ett skop. Ikke utled domenet av CSS-klassen.
- Om «4 samtaler» er listelengde eller en definert teller.
- Prod er ikke målt i denne runden. #243 ligger i lokal CellScaffold-main;
  hva som faktisk kjører er ikke verifisert her.
- Ingen renderer er kjørt mot referansepikslene. Flate-kartets ene «eksakt»-rad
  gjelder at en dropzone utelates — det er ikke visuell runtimeparitet.
