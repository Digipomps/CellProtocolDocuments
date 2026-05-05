# SkeletonElement Rendering Handbook

## 1. Formål

Dette dokumentet beskriver hvordan `SkeletonElement` bør brukes og rendres i en runtime/UI-klient som skal være kompatibel med CellProtocol-dokumentasjonen.

Primærkilde: `source_docs/Book/12_Skeleton_Spec.md`.

## 2. Normative regler (må følges)

### 2.1 Encoding-struktur

- Hvert element er et single-key object:
  - eksempel: `{ "Text": { ... } }`
- Listecontainere (`VStack`, `HStack`, osv.) består av arrays av single-key objects.
- JSON som avviker fra dette formatet skal regnes som ugyldig input.

### 2.2 Canonical felter og kompatibilitet

- `flowElementSkeleton` er canonical stavemåte.
- Legacy `flowELementSkeleton` kan støttes i decoder for bakoverkompatibilitet.
- `Object` bør encode i wrapped form: `{ "Object": { "elements": ... } }`.
- Decoder kan støtte legacy unwrapped form med top-level `elements`.

### 2.3 Keypath/url

- `cell://` skal gå via resolver.
- Relative keypaths kan normaliseres til `cell:///Porthole/<keypath>` (i tråd med dagens UI-beskrivelse).

## 3. Rendering pipeline (anbefalt)

### 3.1 Steg 1: Parse

- Parse JSON til en lukket intern elementmodell (sealed type hierarchy).
- Valider tidlig:
  - nøyaktig én toppnøkkel per elementobjekt
  - felt-typer korrekt
  - obligatoriske felt finnes (f.eks. `Button.keypath`, `Reference.keypath`)

### 3.2 Steg 2: Resolve data

Før render av dynamiske noder:

- Løs opp `keypath` mot lokal/user data hvis tilgjengelig.
- Løs opp `url`/`cell://` via resolver + get/set-kall når det er definert av elementet.
- Kjør i deterministisk rekkefølge for å unngå ikke-deterministisk UI-state.

### 3.3 Steg 3: Render elementtre

- Render rekursivt fra rot-node.
- Render children i deklarert rekkefølge.
- Anvend `modifiers` konsekvent etter at base-widget er bygget.

### 3.4 Steg 4: Failure/fallback

- Ukjent elementtype: render no-op placeholder + logg advarsel.
- Ugyldige felt: ignorer feltet, ikke hele treet (med mindre struktur er ugyldig).
- Resolver-feil: render fallback content (f.eks. tom tekst/loader/feilmelding) uten å krasje hele visningen.

## 4. Element-for-element bruk og rendering

## 4.1 Text

Bruk:

- statisk tekst (`text`)
- data-bound tekst (`keypath`)
- remote-resolvert tekst (`url`)

Rendering-regel:

1. Hvis `keypath` er satt og verdi finnes: bruk den verdien.
2. Ellers hvis `url` er satt: hent data via resolver og render resultat.
3. Ellers bruk `text`.
4. Hvis ingen verdi finnes: render tom tekst eller definert fallback.

## 4.2 TextField

Bruk:

- input med valgfri initialverdi via `sourceKeypath`
- writeback via `targetKeypath`

Rendering-regel:

- bind input-state lokalt i komponenten
- ved commit/endring, send oppdatering til target keypath
- unngå å skrive tilbake på hvert tastetrykk dersom det skaper overbelastning; bruk debounce/commit-policy

## 4.3 Image

Bruk:

- asset-bilde (`name`)
- remote-bilde (`url`)

Rendering-regel:

- velg kilde i prioritet: `url` > `name`
- anvend `resizable`, `scaledToFit`, `padding` før øvrige modifiers
- ved feil i bildehenting: fallback-placeholder

## 4.4 Spacer

Bruk:

- layout-luft

Rendering-regel:

- `width` tolkes som eksplisitt størrelse der det er relevant
- ellers standard spacer-atferd i valgt UI-rammeverk

## 4.5 HStack / VStack

Bruk:

- lineær komposisjon av child elements

Rendering-regel:

- render children i deklarert array-rekkefølge
- unngå auto-sortering/regruppering

## 4.6 List

Bruk:

- vise flow/data-lister med valgfri `flowElementSkeleton` mal

Rendering-regel:

- hent datasett via `keypath`/topic/filter
- hvis `flowElementSkeleton` finnes: bruk som item-template
- ellers fallback til `elements`/standard-presentasjon
- list-oppdateringer bør være stabile (keying) for å unngå UI-flimmer

## 4.7 Object

Bruk:

- map-basert compositional node (`elements: map<string, SkeletonElement>`)

Rendering-regel:

- objektet representerer navngitte child-noder
- renderer må støtte wrapped format normativt
- decoder kan håndtere unwrapped legacy format

## 4.8 Reference

Bruk:

- koble UI-seksjon til en ekstern feed/reference

Rendering-regel:

- `keypath` + `topic` identifiserer datakilde
- `flowElementSkeleton` fungerer som mal for hvert element i referansen
- `filterTypes` anvendes før rendering

## 4.9 Button

Bruk:

- trigge get/set mot cell keypath/url

Rendering-regel:

- hvis `payload` finnes: utfør set
- hvis `payload` mangler: utfør get
- vis eksplisitt loading/disabled state under kall

## 4.10 Divider

Bruk:

- visuell separasjon

Rendering-regel:

- render enkel separator med modifiers

## 4.11 ScrollView

Bruk:

- scrollbar container med `axis`

Rendering-regel:

- render `elements` inni scroll-container
- default axis hvis ikke oppgitt (anbefalt: vertical)

## 4.12 Section

Bruk:

- semantisk gruppe med `header`, `content`, `footer`

Rendering-regel:

- render i rekkefølge header -> content -> footer
- header/footer kan være fraværende

## 4.13 ZStack

Bruk:

- overlay-lag

Rendering-regel:

- første element nederst, senere elementer over
- behold deklarert rekkefølge som z-order

## 4.14 Grid

Bruk:

- grid-layout via `columns`, `spacing`, `elements`

Rendering-regel:

- map `columns` til rendererens grid-definisjon
- valider kolonnedefinisjoner (`type`, `value|min|max`)

## 4.15 Toggle

Bruk:

- boolsk state-bryter bundet til `keypath`

Rendering-regel:

- initialiser med `isOn`
- ved brukerendring: push ny bool-verdi til keypath
- ved write-feil: revert state og vis feilindikasjon

## 5. Modifiers: anbefalt anvendelsesrekkefølge

For konsistent resultat på tvers av elementtyper:

1. størrelse: `width`, `height`, `maxWidthInfinity`, `maxHeightInfinity`
2. spacing/posisjon: `padding`, alignment
3. typografi/farge: `font*`, `foregroundColor`, `background`, `opacity`
4. dekorasjon: `cornerRadius`, `border*`, `shadow*`
5. visibility: `hidden`

Merk: Eksakt visual output vil variere mellom UI-rammeverk, men rekkefølgen bør være stabil.

## 6. Runtime- og resolverintegrasjon

- Alle `cell://` oppslag går gjennom resolver, ikke direkte nettverkskall i UI-komponenter.
- UI-laget bør bruke et tynt data-provider-grensesnitt som kapsler resolver-kall.
- Feil i én node må ikke stoppe rendering av resten av treet.

## 7. Determinismekrav

- Samme input-JSON + samme datasource + samme runtime state skal gi samme render-tre.
- Unngå skjulte sideeffekter i render-fasen.
- Del render og I/O i tydelige steg (resolve -> render).

## 8. Observability

Anbefalt logging per node:

- `nodeType`
- `path` i treet (f.eks. `root/Section[0]/content[2]/Text`)
- `decodeStatus`
- `resolveLatencyMs` (hvis keypath/url)
- `renderStatus`

Dette gjør det mulig å feilsøke store skeleton-trær uten å instrumentere ad hoc.

## 9. Vanlige feil og tiltak

- Feil toppnivåformat (ikke single-key): avvis node tidlig.
- Legacy-felt brukt ukritisk: støtt i decode, men skriv alltid canonical ved encode.
- Direkte resolver-kall fra UI-widgets: flytt til data-provider-lag.
- Ikke-deterministisk oppdatering av lister: bruk stabil keying og konsekvent sortering der datasett tillater det.

## 10. Minimal done-definition for renderer

- Alle elementtypene i kapittel 12 kan parses og rendres.
- `modifiers` anvendes uten runtime-krasj.
- `Object` wrapped + legacy decode støttes.
- `flowElementSkeleton` canonical støttes; legacy kan dekodes.
- Det finnes golden tests for encode/decode + snapshot/render-tester for sentrale elementkombinasjoner.
