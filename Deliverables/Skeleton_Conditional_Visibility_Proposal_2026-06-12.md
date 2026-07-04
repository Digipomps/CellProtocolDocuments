# Skeleton Conditional Visibility Proposal

Dato: 2026-06-12
Status: implementert og testet 2026-06-12

## Kort svar

Ja, vi trenger conditionals i skeleton-formatet, men ikke som en ny
top-level `Conditional` elementtype i første runde.

Anbefalingen er:

1. Start med betinget synlighet som presentasjonslogikk.
2. Legg den som et valgfritt felt under `modifiers`, for eksempel
   `modifiers.visibility`.
3. Ikke bruk conditionals til autorisasjon, samtykke, dataminimering eller
   sikkerhet. Cellen og resolver-kontraktene må fortsatt håndheve dette.
4. Ikke legg inn et nytt wrapper-element som `{ "Conditional": ... }` før alle
   relevante decodere og renderere har støtte, fordi det ikke er trygt nok for
   dagens Swift-decoder.

Dette oppfyller den praktiske bakoverkompatibiliteten Kjetil ba om: eldre JSON
parsing skal ikke krasje når en skeleton inneholder det nye feltet. Eldre
runtime vil ignorere feltet og rendere elementet synlig, så dette er
parser-kompatibelt, men ikke semantisk kompatibelt for sensitive skjuleregler.

## Implementeringsresultat 2026-06-12

V1 er implementert som `modifiers.visibility`, ikke som et nytt
`Conditional`-element.

Endringer:

- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
  definerer `SkeletonVisibilityRule`, `SkeletonCondition`,
  `SkeletonConditionExpression`, `SkeletonVisibilityScope` og
  `SkeletonModifiers.visibility`.
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
  evaluerer visibility før elementet rendres.
- `../CellScaffold/Public/js/skeleton-runtime.js` evaluerer visibility i
  modifier-pass, setter `hidden`/`aria-hidden`, markerer
  `data-visibility-state`, og re-evaluerer ved runtime dataoppdateringer.
- `../CellProtocolDocuments/Tools/Explore/skeleton_explore_validator.py`
  samler root-scopede `modifiers.visibility.when.keypath` bindings og
  validerer dem mot Explore-manifest.
- Malformed visibility-regler i ny Swift-decode knekker ikke skeleton parsing;
  de evalueres fail-closed og skjuler elementet.
- Dokumentasjon og agent/skill-instruksjoner er oppdatert i
  `Book/12_Skeleton_Spec.md`,
  `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`,
  `Book/13_Agent_Instructions.md`, `Prompts/CurrentState.md` og relevante
  Codex skills.

Verifikasjon:

- `swift test --filter SkeletonTests` i `../CellProtocol`: 41 tester, 0 feil.
- `node --check Public/js/skeleton-runtime.js` i `../CellScaffold`: OK.
- `npx playwright test --config=playwright.config.js playwright/skeleton-visibility.spec.js`
  i `../CellScaffold`: 1 test, 0 feil.
- `python3 Tools/Explore/skeleton_explore_validator.py --configuration /private/tmp/skeleton_visibility_config.json --manifest /private/tmp/skeleton_visibility_manifest.json --default-endpoint cell:///Porthole --fail-on-error`:
  1 binding, 0 feil, 0 advarsler.

## Hvorfor vi trenger det

Dagens skeleton kan allerede gjøre mye med `Tabs`, `Picker`, `List`, `Grid`,
`Section` og statisk `modifiers.hidden`. Det dekker grove workflows, men ikke
state-drevet produkt-UI godt nok.

Typiske behov vi har sett i HAVEN:

- vise intent-spesifikke hjelpepaneler i Co-Pilot Chat bare når relevant intent
  faktisk finnes
- skjule capability-spesifikke UI, for eksempel upload, nearby, scanner,
  providervalg eller admin-kontroller når host eller Cell sier at funksjonen
  ikke er tilgjengelig
- vise empty, loading, error eller permission-needed seksjoner uten å lage flere
  nesten-like CellConfigurations
- unngå at viewer-surfaces viser editor-only kontroller
- redusere støy i store konferanse- og workbench-skeletons uten å splitte alt i
  mange separate configs

Uten conditionals har vi tre workarounder:

- lage flere CellConfigurations for samme surface
- la cellen projisere et ferdig filtrert view state
- vise alt og stole på tekst, tabs eller disabled styling

De to første er fortsatt riktige for sikkerhet og større rolleforskjeller. Den
siste er dårlig UX når vi prøver å lage rene produktflater.

## Bekreftet før implementering

`SkeletonModifiers` har i dag statisk `hidden: Bool`, men ingen dynamisk
condition:

- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:25`
- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:42`

`SkeletonElement` har ingen `Conditional` case:

- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1880`
- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1902`

Swift-decoderen matcher kjente wrapper-nøkler eksplisitt og kaster til slutt
`corruptedData` når den ikke finner en støttet elementtype:

- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1977`
- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2205`
- `../CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:2248`

Web-runtime har også en hardkodet liste over støttede elementtyper:

- `../CellScaffold/Public/js/skeleton-runtime.js:7`
- `../CellScaffold/Public/js/skeleton-runtime.js:29`

Web og Apple bruker allerede `hidden` fra modifiers:

- `../CellScaffold/Public/js/skeleton-runtime.js:3453`
- `../CellScaffold/Public/js/skeleton-runtime.js:3521`
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:651`
- `../CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:704`

Ekstern kompatibilitetsnote: JSON Schema sin core-spesifikasjon beskriver at
ukjente individuelle keywords kan behandles som annotations, og at schema kan
utvides med nye keywords. Det er ikke automatisk en garanti for Swift `Codable`,
men det støtter designretningen: nye, valgfrie felter er tryggere enn nye
strukturelle wrapper-typer når gamle klienter finnes.

Kilde:

- https://json-schema.org/draft/2020-12/json-schema-core

## Forslag: `modifiers.visibility`

Legg til en valgfri visibility-regel på `SkeletonModifiers`.

Eksempel:

```json
{
  "Section": {
    "content": [
      { "Text": { "text": "Invite helper" } },
      {
        "Button": {
          "label": "Prepare invite",
          "keypath": "chat.intent.prepareInvite"
        }
      }
    ],
    "modifiers": {
      "visibility": {
        "when": {
          "scope": "root",
          "keypath": "chat.intent.kind",
          "equals": "invite"
        }
      }
    }
  }
}
```

Semantikk:

- Hvis `visibility.when` evaluerer til `true`, vises elementet.
- Hvis regelen evaluerer til `false`, mangler data, eller ikke kan evalueres,
  skjules elementet i nye renderere.
- `modifiers.hidden: true` har fortsatt forrang og skjuler alltid elementet.
- Eldre renderere som ikke kjenner `visibility`, ignorerer feltet og viser
  elementet.

Dette er parser-kompatibelt fordi `visibility` er et ukjent felt inne i en
allerede kjent `modifiers`-object. Det krever ikke en ny `SkeletonElement` case
for at gammel parsing skal komme videre.

## Foreslått regelmodell

Minimum v1 bør være liten nok til å implementere likt i SwiftUI og web.

```json
{
  "visibility": {
    "when": {
      "scope": "root",
      "keypath": "profile.capabilities.canUploadAvatar",
      "equals": true
    }
  }
}
```

Støttede condition-felter i v1:

- `scope`: `root`, `item` eller `context`. Standard: `root`.
- `keypath`: dot-path innen valgt scope.
- `exists`: Bool.
- `equals`: hvilken som helst JSON/`ValueType` verdi.
- `notEquals`: hvilken som helst JSON/`ValueType` verdi.
- `in`: liste med tillatte verdier.
- `contains`: verdi som må finnes i en liste eller substring som må finnes i en
  string.
- `allOf`: liste med conditions.
- `anyOf`: liste med conditions.
- `not`: en condition.

Eksempler:

```json
{
  "visibility": {
    "when": {
      "anyOf": [
        { "keypath": "provider.mode", "equals": "local" },
        { "keypath": "provider.mode", "equals": "approvedExternal" }
      ]
    }
  }
}
```

```json
{
  "visibility": {
    "when": {
      "allOf": [
        { "keypath": "nearby.available", "equals": true },
        { "keypath": "nearby.permission", "equals": "granted" }
      ]
    }
  }
}
```

```json
{
  "visibility": {
    "when": {
      "not": {
        "keypath": "messages.items",
        "exists": true
      }
    }
  }
}
```

## Keypath-regler

V1 bør ikke gjøre async Cell-oppslag fra conditionals. Regelen skal bare
evaluere data som allerede er i render-konteksten.

Foreslått scope:

- `root`: root data/state for skeleton-renderen.
- `item`: gjeldende liste-/gridrad når elementet rendres inne i
  `flowElementSkeleton` eller `itemSkeleton`.
- `context`: nærmeste eksplisitte render-kontekst, som kan være root eller item
  avhengig av elementet.

Hvis vi vil være enda strengere, kan `scope` gjøres påkrevd i første
implementasjon. Det gjør authoring litt tyngre, men reduserer tvetydighet.

`cell://` keypaths bør ikke være støttet i v1 conditions. Conditionals skal ikke
være en skjult datainnhentingsmekanisme.

## Hva dette ikke skal brukes til

Conditionals i skeleton skal ikke være enforcement.

Ikke bruk dette til:

- tilgangskontroll
- skjuling av sensitive data som allerede er sendt til klienten
- samtykkehåndheving
- capability grants
- filtrering av private list items
- automatisk action-dispatch
- remote model/RAG eskalering

Riktig modell er:

1. Cell/Resolver avgjør hva requesteren faktisk får lese eller gjøre.
2. Explore-kontrakten beskriver nøklene og payloadene.
3. Skeleton conditional bestemmer bare hvilken trygg, allerede tilgjengelig UI
   som vises.

## Bakoverkompatibilitet

Det finnes tre nivåer her:

### 1. Parser-kompatibilitet

`modifiers.visibility` er anbefalt fordi gamle decodere forventes å ignorere
ukjente felter inne i `SkeletonModifiers`. Dette bør ikke krasje JSON parsing.

### 2. Renderer-kompatibilitet

Gamle renderere vil ikke evaluere regelen. De viser elementet. Derfor må innhold
som skjules med conditionals være trygt å vise også på gamle klienter.

### 3. Semantisk kompatibilitet

Semantisk skjuling på gamle klienter kan ikke garanteres uten capability-gating,
separat CellConfiguration, eller server/cell-side projection. Hvis en surface
ikke tåler at gammel runtime viser elementet, må vi ikke publisere conditional
som eneste mekanisme.

## Hvorfor ikke `{ "Conditional": ... }` nå

Et eget element ville vært pent:

```json
{
  "Conditional": {
    "when": { "keypath": "chat.intent.kind", "equals": "invite" },
    "then": [
      { "Text": { "text": "Invite helper" } }
    ],
    "else": [
      { "Text": { "text": "No invite intent" } }
    ]
  }
}
```

Men det er ikke parser-kompatibelt nok i dagens Swift-modell. `SkeletonElement`
har en eksplisitt case-liste og decoder-fallback som til slutt kaster
`corruptedData` når wrapperen ikke kan mappes til en kjent case.

Eget `Conditional`-element kan vurderes som v2 når vi har:

- feature negotiation eller `requiredSkeletonFeatures`
- decode-støtte i CellProtocol
- renderer-støtte i Binding og CellScaffold
- editor-støtte
- golden decode/encode fixtures

## Fallback og else

V1 trenger ikke `else` inne i selve condition-regelen. Bruk to søskenelementer
med inverse regler.

Eksempel:

```json
{
  "VStack": {
    "elements": [
      {
        "Text": {
          "text": "Nearby is available",
          "modifiers": {
            "visibility": {
              "when": { "keypath": "nearby.available", "equals": true }
            }
          }
        }
      },
      {
        "Text": {
          "text": "Nearby is not available on this device",
          "modifiers": {
            "visibility": {
              "when": {
                "not": { "keypath": "nearby.available", "equals": true }
              }
            }
          }
        }
      }
    ]
  }
}
```

Dette er mer repetitivt enn et `else`, men parser-kompatibelt og lett å rendre.

## Explore og validering

Condition keypaths må inn i samme valideringsdisiplin som andre skeleton
bindings.

Oppdater `Tools/Explore/skeleton_explore_validator.py` slik at den:

- finner `modifiers.visibility.when` overalt i skeleton-treet
- samler alle `keypath`-felt i condition expressions
- validerer root-scope keypaths mot lesbare Explore-kontrakter
- validerer item/context-scope keypaths mot deklarert item schema der det finnes
- advarer hvis condition bruker en keypath med `unknown`, manglende schema eller
  feil type

Minimum forventning:

- `exists` kan brukes med alle kjente typer.
- `equals`, `notEquals`, `in` og `contains` bør ha sammenlignbare typer.
- Conditions med ukjent kontrakt bør være warning i preview og failure i
  production promotion.

## Implementeringsplan

Fase 1: modell og tester i `CellProtocol`

- Legg til `SkeletonVisibilityRule` og `SkeletonCondition`.
- Legg til `public var visibility: SkeletonVisibilityRule?` i
  `SkeletonModifiers`.
- Legg til unit tests for decode/encode av `visibility`.
- Legg til evaluator-tester for `exists`, `equals`, `notEquals`, `in`,
  `contains`, `allOf`, `anyOf` og `not`.
- Legg til test som viser at ukjent wrapper-element fortsatt feiler, slik at
  bakoverkompatibilitetsbegrunnelsen er eksplisitt.

Fase 2: renderere

- Web: evaluer `modifiers.visibility` i `applyElementModifiers(...)`.
- Web: skjult conditional må også sette `aria-hidden` og deaktivere relevante
  interaktive children.
- Apple: evaluer samme regel i `applySkeletonModifiers(...)` eller før elementet
  pakkes i `AnyView`.
- Begge renderere må re-evaluere ved state/rootData updates uten å sende
  skjulte writes.

Fase 3: docs og authoring

- Oppdater `Book/12_Skeleton_Spec.md`.
- Oppdater `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`.
- Oppdater `cellconfiguration-skeleton-authoring` skill-reference etter at
  implementasjonen finnes.
- Oppdater skeleton editor/inspector slik at `visibility` vises som egen
  kontroll, ikke som tilfeldig raw JSON.

Fase 4: parity og rollout

- Golden fixtures for decode/encode.
- Web runtime screenshot/DOM tests.
- Binding render tests.
- En konferanse- eller Co-Pilot pilot-surface med ikke-sensitiv conditional UI.
- Ikke bruk i sikkerhetskritiske surfaces før gamle klienter er ute av
  målgruppen eller hosten gater på renderer capability.

## Foreslått akseptkriterium

En v1 implementation er godkjent når:

- gammel JSON uten `visibility` rendres uendret
- JSON med `modifiers.visibility` decodes i Swift og web
- gammel runtime som ignorerer `visibility` ikke krasjer
- ny runtime skjuler og viser elementer deterministisk basert på root/item data
- skjulte elementer ikke er fokuserbare eller tilgjengelige for screen reader
- conditionals sender ingen actions og gjør ingen async Cell-oppslag
- Explore validator rapporterer alle condition keypaths
- Binding og CellScaffold viser samme synlighet for samme input state

## Anbefalt beslutning

Gå videre med `modifiers.visibility` som v1 conditional visibility.

Ikke implementer `Conditional` element nå. Det kan bli en v2 når vi har
capability negotiation og full renderer/editor-paritet.

Viktig produktregel: alt conditionals skjuler må enten være ufarlig på gamle
klienter, eller også skjules/utelates av Cell/Resolver før skeleton i det hele
tatt får dataene.
