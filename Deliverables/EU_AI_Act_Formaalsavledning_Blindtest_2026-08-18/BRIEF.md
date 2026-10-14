# Oppgave til Codex: erklær fem strukturerte felt for 57 formålsnoder

Dato: 2026-08-18
Arm: blind ekstern erklæring

## Hva dette er

Dette er én arm i et blindforsøk. **Skåringskriteriet er bevisst holdt tilbake.**
Det er ikke en felle — hele poenget er å måle hva en kompetent forfatter erklærer
når hun bare har nodeteksten, uten å vite hva erklæringen senere skal brukes til.
Kjenner du bruken, tilpasser du svaret, og målingen blir verdiløs.

Svar derfor **kun fra nodeteksten** i `input_nodes.json`. Ikke gjett deg fram til
formålet med forsøket, og ikke juster svar mot en antatt fasit.

## Hva du skal gjøre

For hver av de 57 nodene i `input_nodes.json`, erklær fem felt pluss eventuelle
flagg. Skriv resultatet til `declarations_codex.json` etter skjemaet i
`output_schema.json`.

Dette er produktmetadata, ikke juss og ikke arkitektur. Spørsmålet er hver gang:
**hva gjør denne funksjonaliteten faktisk, i verden, for hvem?**

## De fem feltene

### `domain` — hvilket område i den virkelige verden funksjonaliteten opererer i

```
none | biometrics | critical-infrastructure | education | employment |
essential-services | law-enforcement | migration-border | justice-democracy
```

- `employment` brukes når funksjonaliteten berører folks arbeid: fordeling av
  oppgaver, oppfølging av hvem som gjør hva, rekruttering, vurdering av innsats.
  Det gjelder også når verktøyet er generelt og bare *brukes* i arbeid.
- `essential-services` er tilgang til goder folk trenger: ytelser, kreditt,
  forsikring, nødtjenester.
- `none` når funksjonaliteten ikke hører hjemme i noen av områdene.

### `decisionEffect` — hva utdataene gjør med en beslutning om et menneske

```
none | informational | influences-human-decision |
automated-decision-with-legal-or-similar-effect
```

- `none`: ingen beslutning om noen person berøres.
- `informational`: viser fram noe; mennesket bestemmer selv, uten at systemet
  peker på et svar.
- `influences-human-decision`: systemet anbefaler, rangerer, foreslår eller
  fordeler, og mennesket lener seg på det.
- `automated-decision-with-legal-or-similar-effect`: systemet avgjør, og
  avgjørelsen har rettslig eller tilsvarende betydning for personen.

### `dataSubjects` — hvem sine data eller interesser berøres

```
none | self-owner | named-third-parties | public | vulnerable-groups
```

- `self-owner`: bare eierens egne data.
- `named-third-parties`: navngitte andre mennesker.
- `public`: allmennheten, eller innhold som når ut til ukjente.
- `vulnerable-groups`: barn, folk med nedsatt funksjonsevne, eller mennesker i
  utsatt økonomisk eller sosial situasjon.

### `outputModality` — hva som kommer ut, og hvem som mottar det

```
none | structured-data | ui-render | natural-language-to-human | synthetic-media
```

- `structured-data`: maskinlesbart som går videre i systemet.
- `ui-render`: en flate et menneske ser på.
- `natural-language-to-human`: tekst eller tale skrevet for at et menneske skal
  lese den.
- `synthetic-media`: generert bilde, lyd eller video.

Velg det som beskriver *hovedutgangen*. Går resultatet inn i en annen komponent
og ikke til et menneske, er det `structured-data` selv om det senere blir vist.

### `aiInvolvement` — hvor mye av utdataene en modell laget

```
none | deterministic-code | model-assisted | model-generated
```

- `none`: noden er en abstrakt gren, et kriterium eller en fasett, ikke kjørende
  funksjonalitet.
- `deterministic-code`: vanlig kode, ingen modell.
- `model-assisted`: en modell foreslår, rangerer eller utleder, men resultatet
  er strukturert eller etterbehandlet.
- `model-generated`: en modell produserte innholdet som slippes ut.

### Flagg — sett kun når det er klart sant

```json
"flags": {
  "allocatesTasksToPersons": true,
  "evaluatesPersonPerformance": true,
  "infersPersonalCharacteristics": true,
  "infersEmotion": true,
  "deducesSensitiveAttribute": true,
  "producesPersonScore": true,
  "publishedToPublic": true,
  "performsProfiling": true
}
```

Utelat feltet helt hvis ingen flagg gjelder. Ikke sett et flagg «for sikkerhets
skyld» — en falsk positiv her er like skadelig som en falsk negativ.

`infersPersonalCharacteristics` betyr at systemet *utleder* noe om en person som
personen ikke selv har oppgitt. Bruker som selv har oppgitt en preferanse, er
ikke en utledning.

## Regler

1. Bruk kun `input_nodes.json`. Ikke søk i HAVEN-repoene etter mer kontekst.
2. Ikke les andre filer i `Deliverables/EU_AI_Act_*`. De inneholder fasit.
3. Alle 57 noder skal ha en erklæring. Ingen hopp.
4. Er du i tvil mellom to verdier, velg den du faktisk tror er riktig og skriv
   tvilen i `note`. Ikke velg den forsiktige verdien systematisk — systematisk
   forsiktighet er en skjevhet som ødelegger målingen like mye som gjetting.
5. `confidence` skal være ærlig: `high`, `medium` eller `low`.

## Leveranse

`declarations_codex.json` i denne mappa, gyldig mot `output_schema.json`.
Ikke rør noen fil utenfor denne mappa.
