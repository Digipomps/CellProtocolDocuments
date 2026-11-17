# Oppgave: erklær strukturerte felt for 57 formålsnoder (v1)

Dato: 2026-08-18
Arm: blind ekstern erklæring, andre runde

## Hva dette er

Dette er én arm i et blindforsøk. **Skåringskriteriet er bevisst holdt tilbake.**
Det er ikke en felle — poenget er å måle hva en kompetent forfatter erklærer når
hun bare har nodeteksten, uten å vite hva erklæringen skal brukes til. Kjenner du
bruken, tilpasser du svaret, og målingen blir verdiløs.

Svar derfor **kun fra nodeteksten**. Ikke gjett deg fram til formålet med
forsøket, og ikke juster svar mot en antatt fasit.

## Hva som er endret siden v0

Tre ting, alle fordi forrige runde avdekket feil i *oppgaven*, ikke i svarene:

1. **`systemKind` er nytt og påkrevd, og står først.** Forrige runde manglet en
   måte å si «dette er ikke kjørende funksjonalitet». 17 abstrakte grener ble
   erklært som om de var kode.
2. **`aiInvolvement` er fjernet.** Det viste seg umulig å avgjøre fra
   nodeteksten — informasjonen ligger i implementasjonen, ikke i formålet. Feltet
   avledes nå maskinelt fra kapabilitetsregisteret. Du skal ikke svare på det.
3. **Ett flagg er omdøpt og omdefinert.** Se `supportsWorkAllocationOrMonitoring`
   nedenfor. Det gamle navnet antydet at systemet måtte fordele oppgaver
   automatisk. Det var feil avgrensning.

Resten er uendret. Der du og forrige runde er uenige om et skjønnsspørsmål, er
det ikke rettet — bare definisjonsfeil er rettet.

## Hva du skal gjøre

For hver av de 57 nodene: erklær `systemKind`, deretter fire felt, pluss
eventuelle flagg.

Dette er produktmetadata, ikke juss og ikke arkitektur. Spørsmålet er hver gang:
**hva gjør denne funksjonaliteten faktisk, i verden, for hvem?**

## `systemKind` — påkrevd, svar først

```
capability | abstract | facet | governance-criterion | internal-test
```

- `capability`: kjørende funksjonalitet som gjør noe for noen.
- `abstract`: en gren i formålstreet som samler underformål, uten egen kjøring.
- `facet`: en tverrgående egenskap som festes til andre formål, ikke en funksjon.
- `governance-criterion`: et krav eller en rettighet som beskriver hvordan
  systemet skal oppføre seg, ikke en funksjon som kjøres.
- `internal-test`: kontroller som kjøres mot HAVEN selv.

Er `systemKind` noe annet enn `capability`, sett de fire feltene til `none`
(eventuelt `self-owner` på `dataSubjects` der noden åpenbart handler om eierens
egne data) og gå videre. Ikke strekk deg for å finne innhold i en abstrakt gren.

## `domain` — hvilket område i den virkelige verden funksjonaliteten opererer i

```
none | biometrics | critical-infrastructure | education | employment |
essential-services | law-enforcement | migration-border | justice-democracy
```

- `employment` brukes når funksjonaliteten berører folks arbeid: fordeling av
  oppgaver, oppfølging av hvem som gjør hva, rekruttering, vurdering av innsats.
  Det gjelder også når verktøyet er generelt og bare *brukes* i arbeid.
- `essential-services` er tilgang til goder folk trenger: ytelser, kreditt,
  forsikring, nødtjenester.

## `decisionEffect` — hva utdataene gjør med en beslutning om et menneske

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

## `dataSubjects` — hvem sine data eller interesser berøres

```
none | self-owner | named-third-parties | public | vulnerable-groups
```

## `outputModality` — hva som kommer ut, og hvem som mottar det

```
none | structured-data | ui-render | natural-language-to-human | synthetic-media
```

Velg det som beskriver *hovedutgangen*. Går resultatet inn i en annen komponent
og ikke til et menneske, er det `structured-data` selv om det senere blir vist.

## Flagg — sett kun når det er klart sant

```
supportsWorkAllocationOrMonitoring
evaluatesPersonPerformance
infersPersonalCharacteristics
infersEmotion
deducesSensitiveAttribute
producesPersonScore
publishedToPublic
performsProfiling
```

**`supportsWorkAllocationOrMonitoring`** — sett dette når funksjonaliteten på noe
vis er med på å fordele arbeid mellom mennesker, eller å vise, spore eller følge
opp hvem som gjør hva. Det holder at systemet *støtter* en menneskelig fordeling
eller gjør arbeidet synlig for andre. Systemet trenger **ikke** fordele
automatisk, og det trenger ikke vurdere innsats. Et verktøy som viser hvem en
oppgave ligger på, og om den er blokkert, oppfyller dette.

**`infersPersonalCharacteristics`** — systemet *utleder* noe om en person som
personen ikke selv har oppgitt. En preferanse brukeren selv har oppgitt, er ikke
en utledning.

Utelat `flags` helt hvis ingen gjelder. Ikke sett et flagg «for sikkerhets
skyld» — en falsk positiv her er like skadelig som en falsk negativ.

## Regler

1. Bruk kun nodeteksten du får. Ikke søk i HAVEN-repoene etter mer kontekst.
2. Ikke les filer i `Deliverables/EU_AI_Act_*`. De inneholder fasit.
3. Alle 57 noder skal ha en erklæring.
4. Er du i tvil mellom to verdier, velg den du faktisk tror er riktig og skriv
   tvilen i `note`. Ikke velg den forsiktige verdien systematisk — systematisk
   forsiktighet er en skjevhet som ødelegger målingen like mye som gjetting.
5. `confidence` skal være ærlig: `high`, `medium` eller `low`. Den brukes til å
   rute usikre erklæringer til menneskelig gjennomgang, så `medium` er et
   nyttig svar, ikke et dårlig et.

## Svarformat

```json
{"<purposeRef>": {"systemKind":"...","domain":"...","decisionEffect":"...",
 "dataSubjects":"...","outputModality":"...","flags":{...},
 "confidence":"...","note":"..."}}
```
