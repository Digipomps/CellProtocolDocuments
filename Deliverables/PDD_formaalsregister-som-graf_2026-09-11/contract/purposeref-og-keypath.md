# purposeRef, keypath og interesser med constraints — designnotat

Skrevet 2026-09-13 av Losen, på Kjetils spørsmål: *«Vi trenger en entydig måte å referere til
en Purpose på samtidig som vi må kunne slå dem opp med keypaths.»*

**Forslag. Ikke avgjort.** Går til uavhengig motsvar før det legges fram som konklusjon.
Stier relative til `HAVEN/`.

## 1. Fem målte forhold som avgjør designet

Verifisert i kode 2026-09-13. Dette er ikke antakelser.

| # | Funn | Kilde |
|---|---|---|
| F1 | `PerspectiveNodeImpl.init(from:)` er **tom** — den dekoder ingenting | `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:85–87` |
| F2 | `get(keypath:)` splitter på `.` og har **tom løkkekropp** — bare en kommentar. `set(keypath:)` er tom | samme `:94–108` |
| F3 | `==` sammenligner bare type og navn; relasjoner ignoreres (`// TODO`) | samme `:112–117` |
| F4 | `Interest.constraint` blir **aldri dekodet** — alltid `DefaultInterestConstraint()`. Og `condition` lagres under kodenøkkelen som heter `constraint` | `Interest.swift:15,56,57,73,98` |
| F5 | `nodeIdentifier` er **reservert**: «Anything representing a person sets this to a salted, local identifier» | `PerspectiveNode.swift:68–70` |

**Konsekvens:** «slå opp med keypaths» finnes ikke i dag — det er en stubb (F2). Interesser med
constraints finnes heller ikke i praksis (F4). Og `nodeIdentifier` kan **ikke** gjenbrukes som
adresseringsnøkkel uten å kollidere med personvernrollen sin (F5) — det var min første tanke,
og den var feil.

Dessuten: `purposeRefIsValid` tillater allerede `.`, `_`, `/` og `-` i kroppen
(`PurposeBoundExternalAction.swift:921–929`). `/` er altså lovlig i en ref i dag.

## 2. Problemet, presist

Tre ting har blitt blandet til én streng:

1. **Identitet** — hva som entydig utpeker et formål, bundet i signerte A4-digester. Må være stabil.
2. **Adresse** — hvordan man navigerer dit i grafen, og hvordan en Grant kan avgrense til et undertre.
3. **Navn** — den lesbare strengen mennesker skriver.

I dag er alle tre den samme dotted strengen, og `AnyKeypathExpression` splitter keypaths på `.`
(`Agreement/Condition/KeypathExpression.swift:31–40`). En ref som `purpose://event.agenda.recommendation`
blir da *tre* keypath-komponenter. Det er samme feilklasse som D0: punktumet later som det betyr noe.

## 3. Forslag

**P1 — Ref er identitet, aldri adresse.** En ref splittes aldri, av noen kodevei. D0 gjelder:
kanter kommer fra `parentRef` og de erklærte relasjonene, aldri fra punktum i navnet.

**P2 — Nye refer bruker `/`, aldri `.`.** `/` er allerede lovlig. Eksisterende punktum-refer blir
stående som ugjennomsiktige navn — de er bundet i signerte digester, og å døpe dem om bryter A4.
Over tid forsvinner tvetydigheten uten et eneste brudd.
Eksempel på ny form: `purpose://sport/terrain-running`.

**P3 — En ref er nøyaktig én keypath-komponent, skrevet i klammeform.** Relasjonene er de dotted
segmentene; refer står inne i klammer og splittes aldri:

```
purposes[purpose://sport/terrain-running].interests[interest://color].constraint.value
```

`PerspectiveNodeRelation` har allerede de åtte segmentnavnene (`types`, `subTypes`, `partOf`,
`parts`, `interests`, `purposes`, `entities`, `states`) — stubben i F2 sjekker nettopp dem.

**P4 — Constraints gjenbruker formen Conditions allerede har.** `AnyKeypathExpression` er
`keypathComponents` + `operatorString` + `ParsedValue` (string/int/double/bool/date/array). Det
*er* et constraint-språk. En interessekonstraint bør være den formen, ikke et nytt språk — og den
må faktisk dekodes, i motsetning til i dag (F4).

**P5 — Adresseringsnøkkel er ikke `nodeIdentifier`.** Den er opptatt (F5). Enten adresseres noder
ved ref i klammeform (P3, mitt forslag), eller det innføres et eget dot-fritt `slug`-felt. Jeg
foreslår det første, fordi det ikke legger til enda en identifikator å holde synkronisert.

## 4. Produktnormalisering — «noe som kan løse formålet mitt: å løpe i terreng»

Kjetils eksempel, oversatt til modellen:

| Delen | Hva den er i dag | Hva som mangler |
|---|---|---|
| formålet «løpe i terreng» | `Purpose`-node | finnes ikke i taksonomien ennå |
| produktet | `EntityRepresentation` via relasjonen `entities` | relasjonen finnes; ingen produktnoder |
| farge, størrelse | `Interest` med `constraint` | constraint dekodes ikke (F4) |
| pris ≤ 1500 | constraint med operator og typet verdi | `ParsedValue` har typene; ingen enhet/valuta |

Dette er den samme mekanismen som `goal-som-uttrykk`: en constraint **er** et typet uttrykk med
`gt`/`lt`/`and`/`or` over `real`/`bool`. Produkteksemplet bekrefter altså det formålet — og det
legger til ett krav: **enheter**. «Pris ≤ 1500» uten valuta og «størrelse 43» uten målsystem er
ikke etterprøvbart. `ParsedValue` har ingen enhet i dag.

**Skalaen kommer herfra.** Formål og interesser er få. Produkter er mange. Det er produktnodene
som gjør 100 000 til et realistisk tall, ikke taksonomien — den er 78 noder etter forsoningen.

### Foreslått antiformål: ingen betalt plassering

Et treff skal kunne forklares **fullt ut** av formålet og de oppgitte constraintene. Ingen node
rangeres høyere fordi noen har betalt for det, og ingen leverandør kan kjøpe seg inn i en
forklaring. Uten dette blir formålsregisteret en annonseplass med ekstra steg, og hele
troverdigheten til «matchen er forklarbar per kant» ryker.

Avledet test: `test.reg.ingen-betalt-plassering` — forklaringen for et treff skal bestå kun av
kanter og constraints. Et felt som kan påvirke rangering uten å stå i forklaringen, gjør testen rød.

## 4b. INN-IA: facet, ikke ny nodetype — og hvorfor koden avgjør det

Kjetil 2026-09-13: *«Jeg er litt usikker på konsekvensene av å velge ny nodetype eller facet. Vi må
holde ting enkelt samtidig som vi ikke lukker fremtidige muligheter.»*

**Facet-mekanismen finnes allerede, ferdig håndhevet.** Verifisert i
`CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift`:

| Hva | Hvor |
|---|---|
| `facetRefs: [String]?` på intensjonen | `:171` |
| `facetsAreNonAuthorizing: Bool = true` på både policy og intensjon, og **begge** må være satt | `:172,185,350,669,672` |
| `permittedFacetRefs` som tak på hva som er tillatt | `:294,711–713` |
| `deny(evidence.facetMatchOnly, "facet_match_is_non_authorizing")` | `:722` |
| `deny(!facetsAllowed, "facet_not_permitted")` | `:723` |
| Naboregel som viser mønsteret: `deny(evidence.parentMatchOnly, "parent_purpose_match_is_non_authorizing")` | `:721` |

Altså: en facet er allerede en `purpose://`-formet ref som **ikke kan autorisere**, håndhevet på
resolvergrensen med navngitt avslagsgrunn.

**Konsekvensen av de to valgene, målt mot dine tre krav:**

| | Facet-flagg på noden | Ny nodetype |
|---|---|---|
| Enkelhet | ett erklært felt + **én** ny `deny`-linje ved siden av de to som finnes | nytt skjemabegrep, ny validering, ny håndheving et annet sted |
| Lukker det framtiden? | Nei — et facet-flagg kan **fjernes**. Noden blir et fullverdig formål uten migrering | Ja, delvis — å bytte type er en migrering, og refen er bundet i signerte digester |
| Troverdighet | håndhevingen bor **ett** sted, med avslagsgrunn i samme liste som de andre | to steder som kan bli uenige — nøyaktig feilklassen «to motorer» |
| Forståelse | «facet» er allerede et ord i Book og i koden | et nytt begrep å forklare hver gang |
| Smidighet | reversibelt med én flaggendring | ikke reversibelt uten migrering |

**Det som mangler i dag, og som er hele arbeidet:** facets er en egenskap ved *forespørselen*
(`intent.facetRefs`), ikke ved *noden*. «Denne noden kan bare brukes som facet» kan ikke uttrykkes.
Gapet er lite og har et opplagt hjem: ett erklært felt på noden, og én ny linje rett under `:722`:

```
deny(primaryPurposeIsFacetOnly, "primary_purpose_is_facet_only")
```

**Anbefaling: facet-flagg på noden.** Ikke fordi det er penere, men fordi det er det **reversible**
valget, og du er usikker. Viser det seg at `analysis.decision-support` er et ekte brukerformål, er
det én flaggendring. Viser det seg at en ny nodetype trengs likevel, har vi ikke mistet noe — vi har
bare ikke bygget den ennå.

Avledet test: `test.reg.facet-kan-ikke-autorisere` — et forsøk på å bruke en facet-only-node som
`primaryPurposeRef` skal avvises med `primary_purpose_is_facet_only`, ikke stilltiende lykkes.

## 5. Hva jeg er mest usikker på

1. **Klammeformen (P3) mot et eget slug-felt (P5).** Klammer krever at hver keypath-parser
   håndterer dem — og `AnyKeypathExpression` splitter i dag naivt på `.`. Et slug-felt er enklere
   å parse og vanskeligere å holde synkronisert. Jeg har valgt klammer for å unngå en fjerde
   identifikator, men det er et reelt valg.
2. **Om `/` i nye refer forvirrer mer enn det løser**, siden `://` allerede bruker skråstrek.
3. **Enheter** er et nytt krav jeg utleder av produkteksemplet, ikke noe Kjetil har bedt om.
4. F1–F3 betyr at broen må implementere `init(from:)`, `get`, `set` og `==` før noe av dette kan
   testes. Det er mer arbeid enn «koble på en motor».

## 6. Kjetils svar 2026-09-13/14 — alle fire avgjort

| Valg | Svar | Følge |
|---|---|---|
| Klammeform eller slug-felt | **Klammer.** En ref er én keypath-komponent: `purposes[purpose://sport/terrain-running].interests[interest://color].constraint.value` | Hver keypath-parser må håndtere klammer. `AnyKeypathExpression` splitter i dag naivt på `.` og må endres |
| `/` i nye refer | **Ja.** Nye formål skrives `purpose://sport/terrain-running` | Gamle punktum-refer står urørt — de er bundet i signerte digester. Tvetydigheten forsvinner ved kilden over tid |
| Enheter i constraints | **Nå.** | Constraint-typen vokser med enhet: valuta for pris, målsystem for størrelse. Billigere nå enn å migrere hver constraint når produktene kommer |
| Antiformålet om betalt plassering | **Ja — «en god ide».** | `skal-ikke.betalt-plassering` står som formål med `test.reg.ingen-betalt-plassering` |
| INN-IA: nodetype eller facet | **Facet** (avgjort 13. sept, se §4b) | Ett felt på noden + én deny-linje. Reversibelt |

Alle fem er dermed lukket. Designnotatet er ikke lenger et forslag på disse punktene.

## 7. Hva som fortsatt er åpent

- Klammeform eller eget slug-felt (§5 punkt 1).
- `/` i nye refer — ja eller nei.
- Skal enheter inn i constraint-typen nå, eller er det egen oppgave?
- Antiformålet om betalt plassering — ja eller nei.
