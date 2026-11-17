# Utvidelsesforslag for skeleton — fra G1-GUI, entitetsdata egen kontroll

Skrevet 2026-09-15. Opphav: `Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/images/README.md`,
som listet hva dagens skeleton ikke kunne rendre av de seks godkjente G1-GUI-bildene.

**Hva dette dokumentet er:** en beslutningsklar sakliste for den tråden som eier skjelettformatet.
Hvert forslag er ført tilbake til faktisk kildekode med fil og linjenummer, og har et eksplisitt
alternativ *uten* utvidelse. Anbefalingen er min; avgjørelsen er ikke.

**Hva dette dokumentet ikke er:** en plan. Ingenting her er godkjent, og ingenting skal implementeres
før den som eier formatet har sagt ja. Det er billigere å avvise et forslag her enn å fjerne et felt
fra et format som allerede er i bruk.

Kildene er lest i CellProtocol på `main` slik den sto 2026-09-15.

---

## Sammendrag

| # | Sak | Type | Anbefaling |
|---|---|---|---|
| F1 | Tabell: kolonnejusterte rader som også kan trykkes | **funksjonshull** | Utvid — men ikke med et `Table`-element. To små grep, se under. |
| F2 | Monospace / talljustering | **funksjonshull** | Utvid. Ett valgfritt felt, `fontDesign`. |
| F3 | Asymmetrisk `cornerRadius` | dekorasjon | **Avvis.** |
| F4 | Maksbredde i prosent | layout | **Avvis nå.** Løses av F1 hvis F1 gjøres. |
| F5 | Blandet styling inne i én `Text` | **finnes allerede** | Ikke utvid — *dokumenter*. Men fiks defekten i F5b. |
| F6 | `styleRole` / `styleClasses` styrer ingenting | **feil forventning** | Ikke utvid før noen har bestemt hva de skal bety. |

To av seks punkter i README-en var altså feil fra min side: F5 finnes, og F6 gjør ikke det den ser ut
til å gjøre. Begge er dokumentasjonssaker, ikke formatsaker.

---

## F1 — Tabell

### Hva bildet ville ha
`import-forhandsbilde-v1.png`: 189 rader fra regnearket, kolonnene navn / e-post / telefon / gruppe
rett under hverandre, en overskriftsrad, og en rad man kan trykke på for å rette de to personene som
deler telefonnummer.

### Hva som finnes i dag

`SkeletonGrid` (`Sources/CellBase/Skeleton/SkeletonDescription.swift:2310`) har `columns`, `spacing`,
`keypath`, `itemSkeleton` og `elements`. Kolonnene er `fixed` / `flexible` / `adaptive`
(samme fil, `:2241`).

Rendereren er `CellGridView` (`Sources/CellApple/Cells/Porthole/Utility Views/CellGridView.swift:84`):

```swift
LazyVGrid(columns: resolvedColumns, spacing: ...) {
    if hasDynamicSource {
        ForEach(Array(valueTypeList.enumerated()), id: \.offset) { _, value in
            gridItemView(for: value)       // ett element  ->  én celle
        }
    } else {
        ForEach(skeletonGrid.elements, id: \.id) { element in ... }
    }
}
```

Tre ting følger av de ti linjene:

1. **Ett element i datakilden blir én rute, ikke én rad.** En tabell med fire kolonner må derfor
   levere 4 × N flate verdier, og raden finnes ikke lenger som en ting man kan peke på.
2. **`elements` og `keypath` utelukker hverandre.** `if / else`-en gjør at en statisk overskriftsrad
   ikke kan ligge i samme `Grid` som dynamiske rader. Man må ha to `Grid`-er, og to `LazyVGrid`-er
   deler ikke kolonnemåling. Med `fixed` faller de sammen fordi tallene er like; med `adaptive` gjør
   de det ikke.
3. **Med `flexible`/`adaptive` og rad-som-element får man ingen felles kolonnebredde.** Bredden må
   være kjent på forhånd, altså `fixed`, altså punkter valgt av den som skriver konfigurasjonen.

Det finnes en vei til trykkbare rader: `SkeletonList`
(`Sources/CellBase/Skeleton/SkeletonDescription.swift:1407`). Den har `flowElementSkeleton` for
radinnholdet (`:1421`) og hele interaksjonsmaskineriet allerede på plass — `selectionMode`,
`selectionActionKeypath`, `activationActionKeypath`, `allowsEmptySelection` (`:1413`–`:1419`).
Det den ikke har er kolonner.

### Det presise hullet

> I dag må man velge mellom **justerte kolonner** (`Grid`) og **rader man kan gjøre noe med** (`List`).
> En tabell er begge deler samtidig.

### Alternativ uten utvidelse

`Grid` med `fixed`-kolonner og flate celler. Det gir et lesbart forhåndsbilde av importen. Det man
mister er å trykke på raden med telefonkollisjonen for å rette den — og nettopp den handlingen er
formålet med skjermbildet. Alternativet holder til å *vise* importen, ikke til å *godkjenne* den.

### Minste utvidelse

**F1a — la `elements` og `keypath` leve i samme `Grid`.** Ingen endring i formatet. Rendereren tegner
`elements` først (overskriftsbåndet), så de dynamiske radene, i samme `LazyVGrid`. Fjerner hele
to-grid-problemet og innfører ingen nye begreper. Dette er den billigste endringen i dokumentet, og
den er nyttig uansett hva som skjer med F1b.

**F1b — rader med felles kolonnemåling.** To formuleringer, samme resultat. Først den på `Grid`-siden:
`rowSkeleton: SkeletonElement?` på `SkeletonGrid`. Når den er satt, blir hvert element i
`keypath` én *rad*, og radelementets direkte barn blir cellene i raden. Rendereren bytter da fra
`LazyVGrid` til SwiftUI-ens egen `Grid`/`GridRow`, som måler kolonnene på tvers av radene selv.
`itemSkeleton` er urørt; gammel konfigurasjon oppfører seg nøyaktig som før.

Det gir: felles kolonnebredde uten at noen gjetter punkter, radidentitet, trykk på raden,
`visible(when:)` i `.item`-scope per rad, og stripet bakgrunn.

Plattformkrav: `Grid`/`GridRow` er iOS 16 / macOS 13. `Package.swift:12` er allerede
`.macOS(.v13), .iOS(.v16)`. Ingen ny plattformbunn.

**F1b-alternativ, og etter gjennomgangen tror jeg dette er det riktige:** gi `SkeletonList` et
`columns: [SkeletonGridColumn]?` i stedet, og la rendereren bytte fra `List` til `Grid`/`GridRow`
når det er satt.

Grunnen til at jeg snudde: valget er ikke symmetrisk. `List` har allerede radvalg, radaktivering og
tomt-valg-policy (`:1413`–`:1419`); `Grid` har ingenting av det. Legger vi radidentitet på `Grid`,
må alle de fire feltene finnes opp på nytt der — og da har vi to elementer som begge kan gjøre rader,
med hver sin halvferdige interaksjonsmodell. Legger vi kolonner på `List`, gjenbruker vi ett felt
(`SkeletonGridColumn`) og får ingen nye begreper.

Kostnaden er at `columns` da bor to steder. Det er en billigere pris enn duplisert interaksjon.
Den som eier formatet bør likevel ta valget selv — begge veier er forsvarlige, og jeg har byttet
mening én gang allerede mens jeg leste.

### Bloat-risiko

F1a: ingen — det fjerner en begrensning uten å legge til noe.
F1b: ett valgfritt felt, og en `if let` i rendereren. Gjøres det på `Grid`-siden har `Grid` deretter
tre måter å fylles på (`elements`, `itemSkeleton`, `rowSkeleton`), og spesifikasjonen må si hvilken
som vinner når flere er satt. Gjøres det på `List`-siden er det to måter å tegne én liste på, og
spesifikasjonen må si at `columns` bare betyr noe sammen med `flowElementSkeleton`. Uansett vei bør
reachability-revisjonen si fra når en konfigurasjon setter to som utelukker hverandre.

### Anbefaling

Gjør F1a uansett. Gjør F1b hvis svaret på «skal man kunne trykke på en rad i en tabell» er ja — og for
importflaten er det ja. Av de to formuleringene heller jeg mot `columns` på `List`, fordi
interaksjonen allerede er der. Ikke lag et `Table`-element: det ville være et fjerde container-begrep med sin
egen livssyklus, og alt det trenger finnes allerede i `Grid`.

### Test som må følge med

- Konfigurasjon med overskrift + dynamiske rader i samme `Grid` rendrer begge (F1a).
- To rader med ulik tekstlengde får samme kolonnebredde (F1b).
- En rad-handling havner i `reachableActionKeypaths` (`SkeletonReachabilityAudit`).
- Eksisterende `Grid`-konfigurasjoner rendrer uendret.

---

## F2 — Monospace

### Hva bildet ville ha
`keypath-chat-v1.png` viser keypaths (`person.endpoints[3].value`) og `entitetsdata-editor-v1.png`
viser tallkolonner. Begge leses feil i proporsjonal skrift: punktumene står ikke under hverandre, og
sifrene hopper.

### Hva som finnes i dag

`fontStyle` går gjennom `fontFromStyle`
(`Sources/CellApple/.../SkeletonView.swift:16`) som kartlegger til de elleve semantiske
`Font`-rollene — `largeTitle` … `caption2`. `fontSize` gir `.system(size:weight:)`
(samme fil, `:1693`). SwiftUI-ens tredje parameter, `design:`, settes ingen steder. Det finnes
altså ingen vei til `.monospaced`, `.rounded` eller `.serif` fra en konfigurasjon.

### Alternativ uten utvidelse

Ingen. Dette er ikke noe man kan uttrykke på omvei.

### Minste utvidelse

Ett valgfritt felt i `SkeletonModifiers`:

```swift
public var fontDesign: String?   // "default" | "monospaced" | "rounded" | "serif"
```

Kartlegges direkte til `Font.Design`. Ukjent verdi faller til `default`, som resten av
`fontStyle`/`fontWeight` allerede gjør.

Merk at dette *ikke* bør legges inn som en ny verdi i `fontStyle`. `fontStyle` er størrelsesrollen;
å blande skriftsnitt inn i den gir en verdiliste der `headline` og `monospaced` er gjensidig
utelukkende uten at noe sier hvorfor.

### Bloat-risiko

Lav. Feltet speiler en enum Apple selv har, det har en trygg standardverdi, og det påvirker ingenting
som ikke setter det. Dette er den typen utvidelse som er billig fordi den ikke innfører et begrep —
den eksponerer et som allerede finnes i laget under.

### Anbefaling

Utvid. Og bruk anledningen til å svare på om web-rendereren har en tilsvarende — hvis `fontDesign`
bare betyr noe på Apple-siden, hører det i spesifikasjonen.

---

## F3 — Asymmetrisk `cornerRadius`

`SkeletonModifiers.cornerRadius` er én `Double` (`SkeletonDescription.swift:529`). Bildene brukte
ulik radius per hjørne for å gi et faneuttrykk.

Det er dekorasjon. Ingen bruker forstår noe mer av at ett hjørne er rundere. Et felt som skal dekke
fire hjørner blir enten fire felter eller en streng med egen syntaks, og begge deler er kostnad uten
formål.

**Avvis.** Bildene tegnes om med én radius.

---

## F4 — Maksbredde i prosent

`maxWidthInfinity: Bool?` og `width: Double?` (`SkeletonDescription.swift:522` og `:524`) er det som
finnes. «60 % av forelderen» kan ikke uttrykkes.

Det jeg brukte det til i bildene — en lesbar tekstkolonne som ikke strekker seg over hele vinduet, og
kolonnebredder i forhåndsbildet — dekkes av `Grid` med `flexible`-kolonner, altså av F1. Et generelt
prosentfelt vil dessuten gjøre skjelettet til et halvt layoutspråk: prosent uten `min`/`max` er
sjelden det man vil ha, og med `min`/`max` har man gjenoppfunnet `GridItem`.

**Avvis nå.** Ta det opp igjen bare hvis det dukker opp et behov F1 ikke dekker.

---

## F5 — Blandet styling inne i én `Text`

**Dette var min feil. Det finnes allerede.**

`CellTextView.renderText` (`Sources/CellApple/.../SkeletonView.swift:1722`) kjører teksten gjennom
`AttributedString(markdown:options:)` med `interpretedSyntax: .full` når
`shouldRenderMarkdown` er sann (`:1667`). Den er sann når enten

- `modifiers.styleRole == "markdown"`, eller
- `keypath == "text"` og kontekstens `contentType` er `text/markdown`.

Så `**189 personer**` midt i en setning virker i dag, med riktig linjebryting, så lenge man setter
`styleRole: "markdown"`.

**Ingen utvidelse. Dette skal inn i skjelettdokumentasjonen** — det er en kapabilitet ingen kan gjette
seg til av feltnavnet `styleRole`.

### F5b — en defekt å melde videre

Linje `:1723` starter med

```swift
guard skeletonText.modifiers?.localization?["text"] == nil, shouldRenderMarkdown, ...
```

Har teksten en lokalisering, slås markdown av. En norsk streng med uthevet tekst i mister altså
uthevingen i det øyeblikket den oversettes — og stjernene blir stående synlig i teksten.

Det er et hull, ikke et valg, og det bør fikses der det er (send den lokaliserte strengen gjennom
samme parser) heller enn å bli et nytt felt. Verdt en egen sak.

---

## F6 — `styleRole` og `styleClasses` styrer ingenting

Ikke i README-en, men funnet under gjennomgangen, og det hører hjemme her fordi det vil bite den
neste som skriver en konfigurasjon.

`applyStyleMetadata` (`Sources/CellApple/.../SkeletonView.swift:199`) gjør bare dette med `styleRole`
og `styleClasses`:

```swift
view.accessibilityIdentifier("style-role-\(rolePart)|style-classes-\(classesPart)|presentation-…")
```

De blir en tilgjengelighets-id, altså et **testhåndtak**, og ingenting annet. Ingen farge, ingen
skrift, ingen avstand. De eneste unntakene er to innebygde strenger som er sjekket for hånd:
`"markdown"` på `Text` (`:1668`) og `"chat-primary-action"` på `Button` (`:1855`).

Navnet lover et temasystem. Implementasjonen er et testhåndtak med to spesialtilfeller. Den som
skriver en konfigurasjon vil anta det første.

To veier, og de bør ikke blandes:

- **Enten** si tydelig i spesifikasjonen at dette er testhåndtak og aldri utseende — da bør de to
  spesialtilfellene få egne felter i stedet, så regelen er uten unntak.
- **Eller** bestemme at `styleRole` er den semantiske stilhaken, og innføre et sted der roller
  oversettes til utseende. Det er en større sak enn resten av dokumentet til sammen, og den skal ikke
  gjøres i forbifarten.

**Anbefaling:** ikke utvid noe her før spørsmålet er besvart. Men skriv ned svaret — dette er en
felle uansett hvilken vei den går.

---

## Hva jeg ville tatt først

1. **F5 og F6 inn i dokumentasjonen.** Koster ingenting, og fjerner to gale antakelser som ellers
   vil bli bygget videre på.
2. **F1a.** Ti linjer i rendereren, ingen formatendring.
3. **F2.** Ett felt, ingen nye begreper.
4. **F5b** som egen defekt.
5. **F1b** når noen har tatt stilling til om tabellrader skal kunne trykkes.
6. **F3 og F4** avvist, med begrunnelsen her som svar hvis de kommer tilbake.

## Krav som gjelder alle utvidelser her

Ingen av forslagene endrer at en flate ikke får skjule sine egne veier inn. Et nytt felt som kan
gjøre et element usynlig, eller flytte en handling inn i et scope rendereren ikke fyller, skal
fanges av `SkeletonReachabilityAudit` — ellers gjentar vi
`lesson.unresolvable-condition-is-invisible`.
