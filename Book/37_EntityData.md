# Chapter 37 — EntityData

Last verified against code: 2026-09-16 (v2-skjema lagt til 2026-09-17)

Status: Struktur og nodemodell er kildebekreftet. Beslutningene i §7 er tatt av Kjetil
16.09.2026, men er **ikke implementert** — de står her fordi et kapittel som beskriver
dagens form uten å si hvor den er på vei, blir feil neste måned. Feltbeskrivelser i
skjemaet er på engelsk for å bevare betydningen; forklaringen her er på norsk.

## Formål

EntityData er navnet på **dataene en entitet holder under egen kontroll**: opplysninger om
seg selv, formål, relasjoner, dokumentasjon, avtaler og historikk. Kapittelet finnes for at
et menneske eller en agent skal kunne forstå strukturen uten å lese Swift — og for at ingen
skal måtte gjette på hva et felt betyr, slik situasjonen var frem til nå.

## 1. Konstruksjonen

`Entity` er ikke en lukket Swift-type:

```swift
public typealias Object = [String: ValueType]   // Object.swift:6
public typealias Entity = Object                // Object.swift:7
```

Det finnes altså ingen struct med alle feltene i dette kapittelet. EntityData er en fleksibel
trestruktur, og `EntityAnchorCell` er cellen som lagrer og betjener den
(`CellProtocol/Sources/CellVapor/Cells/EntityAnchorCell.swift`,
`CellProtocol/Sources/CellApple/Cells/EntityAnchorCell.swift`).

**Roten har ingen konvolutt.** Det lagrede treet begynner rett på røttene under. Det er ingen
obligatorisk `entityId`, `owner`, `domain` eller `schemaVersion` i roten, og det skal det ikke
være: eierkonteksten ligger i cellen og i autorisasjonskontraktene, ikke i JSON-en. Et
`entityId` i dataene ville vært en påstand uten bærekraft — den som leser dataene, har dem
allerede gjennom en celle som vet hvem eieren er.

Alle røttene er valgfrie. En ny eller delvis utfylt entitet kan være `{}`.

### Tre roller som blandes lett

| Begrep | Hva det er |
|---|---|
| **Entity** | Den begrepsmessige aktøren — et menneske, en organisasjon eller en enhet. |
| **Identity** | Den operative identiteten som brukes i autoriserte protokollkall. Én entitet kan ha flere, domeneavgrenset. Bærer som minimum uuid og offentlig nøkkel. |
| **EntityAnchorCell** | Cellen som lagrer og betjener dataene på vegne av eieren. |

Et navn, en UUID eller en referanse i JSON gir ikke i seg selv tilgang.

## 2. Røttene

| Rot | Hva den bærer |
|---|---|
| `person` | Navn, profil, kontakt, adresser, språk, arbeid, ferdigheter, preferanser og domenespesifikke data. |
| `purposes` | Eierens egne formål og interesser. Administreres av PerspectiveCell. |
| `relations` | Relasjoner til andre entiteter, identiteter og kontaktmuligheter. |
| `proofs` | Bevismateriale: credentials, identitetskoblinger, medlemskap, inklusjonsbevis. |
| `signedAgreementEntity` | Kanoniske signerte avtaleposter. Produksjonsgrensen for avtaler (se `book-04-agreements-contracts`). |
| `agreements` | Avledede indekser over avtaler. Skrives aldri direkte. |
| `entityRepresentation` | Registerets eldre, delvise representasjonsrot. Den komplette noden er `$defs.EntityRepresentation`. |
| `chronicle` | Hendelses- og samhandlingshistorikk. |
| `bindings` | Rute- og koblingsmetadata for celler bak entiteten. |
| `scaffoldPresence` | Hvor entiteten har materialisert nøkkelstiprefikser på tvers av scaffolds. |
| `identityLinks` | Vedvarende innmelding, godkjenning og tilbakekalling av operative identiteter. |
| `dataInventory` | Privat oversikt over autoriserte datarepresentasjoner og sikkerhetskopier. |

Tre av disse sier noe som er lett å lese feil:

- `bindings` er **strukturmetadata, ikke tilgang**. En rute her gir ingen rettighet.
- `scaffoldPresence` er **ikke bevis på aktiv forbindelse** — bare en registrering av at noe
  er materialisert et sted.
- `identityLinks.state` er en **beregnet API-visning**, ikke et lagret underfelt. Detaljtypene
  ligger i `IdentityLinkingModels.swift`.

## 3. Nøkkelstier

Nøkkelstier adresserer deler av treet:

| Form | Betydning |
|---|---|
| `person.name.first` | Ett felt. |
| `person.addresses[].street.name` | Samme felt i hvert element. |
| `person.addresses[label="home"].street.name` | Velger ett bestemt element. |
| `relations.entities.<entityID>` | Oppslag med dynamisk id. |
| `person.nicknames[+]` | Skrive-/append-syntaks. **Ikke** en bokstavelig nøkkel i lagret JSON. |

Selektorlogikk og ID-likhet kontrolleres i runtime, ikke av JSON Schema.

`proofs.index.byKeypath` kobler en escaped nøkkelsti til bevisene som støtter verdien der.
Det er mekanismen som gjør at et **enkeltfelt** kan være bevist, ikke bare et helt dokument.

## 4. Nodemodellen

Dette er kjernen. `EntityRepresentation`, `Interest` og `Purpose` arver alle samme baseklasse:

```swift
public class PerspectiveNodeImpl: PerspectiveNode, Referenceable   // PerspectiveNode.swift:41
public class EntityRepresentation: PerspectiveNodeImpl             // EntityRepresentation.swift:61
public class Interest: PerspectiveNodeImpl                         // Interest.swift:13
public class Purpose: PerspectiveNodeImpl                          // Purpose.swift:13
```

De er **noder i samme vektede graf**, ikke tre parallelle modeller.

- **Interest** er i praksis en node med en etikett. Etiketten er for gjenkjennelighet; noden er
  definert av sine relasjoner til andre noder. `constraint` (`InterestCondition`) er nyttig
  funksjonalitet der det er relevant, for eksempel at en opplysning må være fersk.
- **Purpose** er også en etikett definert av sine relasjoner, men har i tillegg et **målbart
  mål, og det er påkrevet**. Purpose er den utførende delen av en Interest.
- **EntityRepresentation** er min representasjon av en annen entitet — det jeg vet, tror eller
  har fått dokumentert. En kontakt er en node i min graf, det samme som jeg i mitt eget hode
  vet om mine relasjoner. Det er ikke den andres EntityData.

Kantene er `Weight<T>`:

```swift
public struct Weight<T: PerspectiveNode & Codable>: Weighted, Codable   // Weight.swift:13
```

Hver kant bærer `weight` og enten en innebygd `value` eller en `reference` til en
`nodeIdentifier`. **Det er kanten som har vekten** — samme formål kan ha ulik vekt i to
forskjellige relasjoner. Vektene er ikke garantert å ligge mellom 0 og 1; eldre eksempler
bruker verdier som 7.

Åtte relasjonsfamilier går på tvers av de tre nodetypene:

| Familie | Måltype fra EntityRepresentation | fra Interest | fra Purpose |
|---|---|---|---|
| `types`, `subTypes` | EntityRepresentation | Interest | Purpose |
| `parts`, `partOf` | EntityRepresentation | Interest | Purpose |
| `interests`, `states` | Interest | Interest | Interest |
| `purposes` | Purpose | Purpose | Purpose |
| `entities` | EntityRepresentation | EntityRepresentation | EntityRepresentation |

Et formål jeg selv har, og et formål jeg leter etter hos en annen, uttrykkes med samme
`Purpose`-type. Det finnes ingen `SearchPurpose`, og det skal ikke lages en.

`Purpose.goal` og `helperCells` peker på `CellConfiguration` — koblingen fra formål til noe
kjørbart. CellConfiguration kan også brukes til å utføre get/set, og er grundig dokumentert i
koden (se `book-12-skeleton-spec` og `book-22-explore-contracts-for-skeleton-authoring`).

### Sirkler og serialisering

`Weight<T>.encode` bærer tre typede `Facilitator`-registre gjennom `Encoder.userInfo` i alle
Codable-kall. Første gang en node møtes, skrives hele kroppen og referansen registreres; neste
møte skriver bare `{"weight": 0.8, "reference": "purpose-review-demo"}`. Registrenes levetid er
**ett dokument** — en ny, uavhengig lagring krever ny encoder med tomme registre.

## 5. Reglene for bruk

- **Rediger representasjonen, avled sammendrag.** De eldre feltene (`subject`,
  `interests.declared/inferred`, `purposeRefs`) leses fortsatt, men er en potensielt utdatert
  oppsummering. Det finnes ingen toveis synk. Bygg ikke enda en parallell person-/formålsmodell.
- **Et felt er ikke en tillatelse.** En lagret påstand i `proofs` er ikke dermed verifisert; en
  rute i `bindings` gir ingen tilgang.
- **Lagringen er åpen.** Store deler bruker `additionalProperties: true`, så et skjema fanger
  ikke alle skrivefeil. Signaturer, rettigheter og semantiske regler kontrolleres i runtime.
- **Avledede røtter skrives aldri direkte.** `agreements` er en indeks over
  `signedAgreementEntity`; endringer går via den autoritative avtalebanen.
- **`person.attributes[]` er sandkassen.** Navnerom-merkede attributter med kilde, konfidens,
  bevis og livsløpsstatus (`proposed`/`active`/`promoted`/`deprecated`) finnes slik at et nytt
  faktum ikke må bli en kanonisk nøkkelsti før det har bevist seg. `promotedTo` peker på stien
  det eventuelt ble forfremmet til.

## 6. Maskinlesbar kontrakt

For **formene** er JSON Schema (Draft 2020-12) det kanoniske verktøyet.

For **cellene som betjener dataene** er `ExploreContract` den maskinlesbare kontraktflaten —
se `book-22-explore-contracts-for-skeleton-authoring`. Explore svarer på hvilke nøkler som
finnes, om de er lese, skrive eller handling, hvilken payload som aksepteres, hva som
returneres, **hvilke rettigheter som kreves**, og hvilke flow-topics som sendes som
sidevirkning. De to siste er grunnen til at OpenAPI ikke er valgt her: i HAVEN er grants og
flow førsteklasses, og i OpenAPI ville de blitt fritekst. OpenAPI 3.1 bygger på JSON Schema
2020-12, så schema-komponentene kan gjenbrukes uten omskriving den dagen en ekstern
HTTP-grense faktisk skal dokumenteres for noen utenfor HAVEN.

## 7. Besluttet 16.09.2026 — ikke implementert

Kjetil gikk gjennom alle 253 elementene i `EntityData.review.schema.json` og besvarte hvert
enkelt. Dette er beslutningene som endrer strukturen. **Ingen av dem er implementert i kode.**

Beslutningene er ført inn i et eget skjema og eksempel, så det finnes en form å bygge mot:

- `CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.schema.json` — den besluttede
  formen, JSON Schema Draft 2020-12
- `CellProtocol/Docs/EntityData-Review-2026-09-11/EntityData.v2.example.json` — eksempel som
  validerer mot den
- `CellProtocol/Docs/EntityData-Review-2026-09-11/V2-BESLUTTET-FORM.md` — hva som endret seg
  og hvorfor

v1-filene er beholdt ved siden av og beskriver fortsatt **dagens** lagring, altså det koden
faktisk skriver. Fullt referat av beslutningene:
`CellProtocol/Docs/EntityData-Review-2026-09-11/GJENNOMGANG_KJETIL_2026-09-16.md`.

| Område | Beslutning |
|---|---|
| Kontaktopplysninger | Enkeltfeltene `person.contact.email` og `person.contact.phone` utgår. **Endpoints** blir formen for alt: telefon, e-post, SoMe-nick, URL, cellereferanse. For flere av samme type brukes label (`primary`). |
| Relasjonenes kontakt | `relations.people[].contact.*` skal ha **samme struktur som person** — endpoints, ikke egne felter. |
| `endpointCell` | Vurderes omdøpt til `cellReference`. |
| Foretrukket kanal | `person.contact.preferredChannel` beholdes; dubletten i `person.preferences.communication.preferredChannel` utgår. |
| Standard synlighet | `person.preferences.privacy.defaultVisibility` = **private**. |
| Konferanse | `person.conference` skal ut av `person` og bli **egen rot**. Domeneskiver hører ikke under person. |
| Organisasjon | Vurderes: `organization` som egen rot for organisasjonsentiteter, i stedet for å presse dem inn i `person`. |
| `relations` | Blir **object** med reserverte nøkler, slik at brukeren kan legge til egne navngitte relasjonslister. |
| Relasjonsform | `relations.people[]` vikes for `relations.records` / `entityRepresentation`. |
| `ownerUUID` | **Obsolet.** uuid hører i Identity. En EntityRepresentation peker på en entitet, som holder listen over hvilke identiteter vi har oppfattet at entiteten bruker. |
| Relasjonens formål | `purposeRefs` erstattes av grafen. |
| `EntityRelationInterests` | Erstattes av Interest/Purpose. |
| `EntityRelationChannel` | Erstattes av endpoints i EntityRepresentation. |
| `EntityRelationStanding` | Status og tillit måles i om relasjonens uttalte formål er oppfylt (vektet), ikke som eget felt. |
| `EntityRelationEvidence` | Erstattes av `proofs` med keypaths, som for egne bevis. |
| `signedAgreementEntity.records` | Forblir en **liste**. Dictionary-formen ble vurdert og forkastet: et JSON-objekt har ingen rekkefølge, og posten er en revisjonskjede der «hva skjedde først» må bevares. |
| `chronicle` | Legacy-initialiseringen med tomt objekt ryddes. |
| `scaffoldPresence.staging` | For spesifikk for utviklingsmiljøet; erstattes av en generell form. |

Dette står igjen som **ikke avgjort**:

- Skal skills være annonserte formål brukeren hevder å kunne løse, heller enn egne poster?
- Skal `person.work` bli et array med referanser til arbeidsorganisasjoner?
- Skal relasjonen ha toveis binding — et array som lister hvilke relasjoner personen er
  medlem av? Krever grundig vurdering: det avgjør om relasjonsgrafen har én eier av sannheten
  eller to som kan gå fra hverandre.
- Skal sensitive merkelapper kunne lagres i `entityRepresentation`, altså i det én bruker
  lagrer om en annen?
- Bør `chronicle` peke til en egen celle, eventuelt i et annet scaffold, siden den kan vokse seg
  stor?
- Hvordan avgjøres det sikkert og utvetydig at to identiteter representerer **samme** entitet?

## 8. Kilder

Kildefiler, alle bekreftet lest 16.09.2026:

- `CellProtocol/Sources/CellBase/ValueTypes/Types/Object.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/Interest.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/EntityRepresentation.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/Weight.swift`
- `CellProtocol/Sources/CellVapor/Cells/EntityAnchorCell.swift`
- `CellProtocol/Sources/CellApple/Cells/EntityAnchorCell.swift`

Diskusjonsskjema med 253 elementer og 240 beskrivelser fra nøkkelstiregisteret:
`CellProtocol/Docs/EntityData-Review-2026-09-11/`. Skjemaet er et **gjennomgangsdokument**, ikke
en vedtatt wire-kontrakt, og `$id` identifiserer dokumentet — ikke et felt som skal skrives inn
i dataene.

En advarsel som gjelder når du leser koden: deler av nodemodellens nyere arbeid —
`EntityRelationRecord.entityRepresentation`, `EntityRepresentationDataCodec.swift`,
`EntityRelationPerspective.swift` og bevaring av `nodeIdentifier` i `Purpose`/`Interest` sin
Codable — fantes 16.09.2026 kun i arbeidstreet på grenen `pdd/tillitspakke-agentflaate`, ikke
på `origin/main`. Leser du `origin/main`, finner du dem ikke.

## Relaterte kapitler

`book-03-identity-model`, `book-09-purpose-interests`, `book-14-perspective-runtime-matching`,
`book-21-contact-endpoint-cell`, `book-22-explore-contracts-for-skeleton-authoring`,
`book-23-purpose-knowledge-base`, `book-32-cross-scaffold-entity-enrollment`.
