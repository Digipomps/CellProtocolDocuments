# Forsoning av taksonomien — forslag per node

Skrevet 2026-09-12 av Losen. **Forslag. Ingenting er avgjort før Kjetil har sagt ja eller nei.**

Kjetils føring (2026-09-12): *«analyser formålene og ta med alle som er viktige, kilden i seg
selv er ikke viktig, men det er viktig at vi dokumenterer hva vi kommer frem til.»*

Kilden blir derfor **resultatet av denne forsoningen** — ikke Book-JSON og ikke
runtime-tabellen. Begge genereres fra den etterpå.

Stier er relative til `HAVEN/`.

## Målt utgangspunkt (2026-09-12)

| | Antall |
|---|---|
| `purpose://`-noder i `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json` | 57 |
| `purpose://`-noder i `CellScaffold/Sources/App/Support/PurposeDecomposition.swift` | 44 |
| Felles | 31 |
| Bare i runtime | 13 |
| Bare i Book | 26 |
| Foreslått etter forsoning | 74 + 4 nye foreldre = **78** |

## D0 — Strukturfunn som må avgjøres først: ref-strengen er et navn, ikke en sti

Dette ble funnet mens tabellene ble laget, og det endrer broen (punkt 2).

**Punktnotasjonen i en `purpose://`-ref er ikke forelder-barn-relasjonen.**
`purpose://event.agenda.recommendation` har `parentRef: purpose://event.participation` —
ikke `purpose://event.agenda`. Og `purpose://event.agenda` finnes ikke som node i det hele
tatt.

Måling: **29 implisitte foreldre** som ref-formen antyder, finnes ikke som noder noe sted:
`access`, `access.audit`, `analysis`, `capability`, `contact`, `content`, `event`,
`event.agenda`, `event.meeting`, `event.schedule`, `gui`, `gui.quality`, `personal-context`,
`preference`, `project-work`, `prompt`, `purpose-taxonomy`, `questionnaire`,
`questionnaire.access`, `questionnaire.admin`, `questionnaire.delivery`,
`questionnaire.respondent`, `questionnaire.responses`, `scaffold`, `self-determination`,
`skeleton`, `source`, `source.methodology`, `test`.

Samtidig: **alle `parentRef` i Book peker på noder som faktisk finnes** (0 brutte).
Treet er altså gyldig — det er *navnene* som lyver om det.

**Forslag D0:** Kanter i registeret bygges **utelukkende fra `parentRef`** og de øvrige
erklærte relasjonene. Ingen kode skal utlede slektskap ved å splitte en ref på punktum.
Avledet test: `test.reg.ref-er-ikke-sti` — bygg grafen, og assert at ingen kant finnes som
bare kan forklares av ref-strengens form.

Konsekvensen hvis dette overses: broen bygger 29 fantomnoder og et tre som ser riktig ut og
er feil. Det er nettopp den feilklassen `en-kilde` skal fjerne.

## Avgjørelseskategorier

| Kode | Betyr |
|---|---|
| **INN** | Tas inn i den forsonte taksonomien som formål |
| **INN-IA** | Tas inn, men merket **ikke-autoriserende**: det er en metode eller en kapabilitet, ikke et brukerformål. Kan aldri være primærformål i A1/A4 purpose-bound external action |
| **OPPRETT** | Node som må opprettes fordi den er nødvendig som forelder |
| **UTGÅR** | Tas ikke inn. Grunnen skrives her — ingen node forsvinner uten skriftlig grunn |

Ingen node er foreslått **UTGÅR**. Se «Det jeg er minst sikker på» til slutt.

## Tabell A — de 13 som bare finnes i runtime

Alle 13 brukes i produksjonskode i dag, ikke bare i dekomponeringstabellen: `PersonalCopilot`,
`QuestionnaireCampaign`, `ConfigurationCatalog`, `ChatPurposeResourceRouter`,
`PurposeKnowledgeBase`, `BookProjectEntityPresenceSupport`. Et formål produksjonskoden
klassifiserer mot, er et formål i bruk.

| Ref | Treff i dekomponeringen | Forslag | Foreslått forelder | Begrunnelse |
|---|---|---|---|---|
| analysis.problem-framing | 3 | **INN-IA** | analysis *(ny)* | Rammer inn et problem — metode, ikke brukerformål |
| analysis.decision-support | 9 | **INN** | analysis *(ny)* | Mest brukte av de tretten. Å få beslutningsstøtte er noe en bruker faktisk vil |
| analysis.evidence-ledger | 3 | **INN-IA** | analysis *(ny)* | Belegg-hovedbok er apparat, ikke formål |
| analysis.synthesis | 3 | **INN-IA** | analysis *(ny)* | Metode |
| analysis.meta-evaluation | 3 | **INN-IA** | analysis *(ny)* | Metode, og den mest åpenbare kandidaten til å bli misbrukt som autorisasjon |
| analysis.advisory-panel | 4 | **INN-IA** | analysis *(ny)* | Panelmetoden. Et panel er en fremgangsmåte |
| capability.construct-cellconfiguration | 4 | **INN-IA** | capability *(ny)* | Navnet sier kapabilitet. A4: en kapabilitet er et tak, aldri en rett |
| capability.delivery | 7 | **INN-IA** | capability *(ny)* | Samme |
| capability.request-human-review | 4 | **INN** | capability *(ny)* | Å be om menneskelig gjennomgang **er** et brukerformål, og bør kunne være primærformål |
| capability.request-new-functionality | 6 | **INN** | capability *(ny)* | Samme — brukeren ber om noe |
| capability.reuse-visible-configuration | 4 | **INN-IA** | capability *(ny)* | Kapabilitet |
| questionnaire.campaign | 11 | **INN** | questionnaire *(ny)* | Book har allerede barnet `questionnaire.campaign.complete`, men ikke denne. Runtime har forelderen Book mangler |
| questionnaire.response | 5 | **INN** | questionnaire *(ny)* | Samme |

**Merk mønsteret:** de elleve `analysis.*`/`capability.*`-nodene er nesten alle metoder eller
kapabiliteter. At de har ligget i samme flate tabell som ekte brukerformål er selve grunnen
til at de aldri kom inn i Book — og det er også en reell risiko: A1/A4 krever eksakt
primærformålstreff, og en kapabilitetsnode som primærformål ville være en rett skapt av et
navn. **INN-IA er derfor ikke kosmetikk; det er en sikkerhetsegenskap.**

## Tabell B — de 26 som bare finnes i Book

| Ref | Status i Book | Forelder i Book | Forslag | Begrunnelse |
|---|---|---|---|---|
| human-agency | draft | root | **INN** | Forelder til contact.*, event.participation og personal-context.semantic-state. Faller den, faller ni noder |
| contact.communication | draft | human-agency | **INN** | Korrespondanse er i drift i HAVEN i dag |
| contact.introduction | draft | contact.communication | **INN** | Samme |
| contact.followup | draft | contact.communication | **INN** | Samme |
| event.participation | draft | human-agency | **INN** | Konferanse- og arrangementsarbeidet er i drift |
| event.agenda.recommendation | draft | event.participation | **INN** | Se D0: forelderen er `event.participation`, ikke `event.agenda` |
| event.meeting.draft-request | draft | event.participation | **INN** | Samme |
| event.schedule.change-request | draft | event.participation | **INN** | Samme |
| event.privacy-preserving-networking | draft | event.participation | **INN** | Bærer et personvernløfte; hører hjemme i registeret |
| content.review-before-publish | draft | digital-work | **INN** | `haven-claim-review` er en levende arbeidsflyt |
| knowledge.explain-policy | draft | knowledge | **INN** | — |
| personal-context.semantic-state | candidate | human-agency | **INN** | Er nøyaktig det `PDD_palazzo-husk-det-jeg-sa` handler om |
| purpose-taxonomy.capture-and-place | candidate | grounding | **INN** | Book 23 §8s fangstprosess. Dette er denne oppgavens eget formål |
| scaffold.operations | candidate | root | **INN** | Ubrukt i dag — men blir forelder til `capability.*`. To foreldreløse løser hverandre |
| skeleton.owner-entity-access | draft | gui.quality.functional-accessible | **INN** | — |
| test.acceptance.hallucination-evaluation | draft | test.acceptance | **INN** | Port vi faktisk vil ha |
| value-and-commons | candidate | root | **INN** | DiMy-verdiarbeidet er et levende område |
| self-determination.data | — | — | **INN** | Roten i selvbestemmelsesgrenen. Alle åtte barna under peker hit |
| self-determination.data.scope | candidate | self-determination.data | **INN** | Omfang av data som gjøres tilgjengelig |
| self-determination.data.use-purpose | candidate | self-determination.data | **INN** | Formålsbinding for databruk — bærebjelken i A1/A4 |
| self-determination.data.recipients | candidate | self-determination.data | **INN** | Mottakere og delegering |
| self-determination.data.duration | candidate | self-determination.data | **INN** | Varighet, tilbaketrekking og sletting |
| self-determination.data.locality | candidate | self-determination.data | **INN** | Sted og jurisdiksjon |
| self-determination.data.manner | candidate | self-determination.data | **INN** | Måte og avledede data |
| self-determination.data.verifiability | candidate | self-determination.data | **INN** | Etterprøvbarhet framfor tillit |
| self-determination.data.exercisability | candidate | self-determination.data | **INN** | Kontroll som faktisk kan utøves |

**Hele `self-determination.data`-grenen (9 noder) tas inn.** Den er dokumentert og aldri
implementert. Det er den grenen som mest direkte uttrykker hva HAVEN lover, og den er
forutsetningen for at `use-purpose` skal bety noe i A4.

## Tabell C — nye foreldre som må opprettes

| Ref | Forelder | Forslag | Begrunnelse |
|---|---|---|---|
| purpose://analysis | knowledge | **OPPRETT · INN-IA** | Samler de seks `analysis.*`. Ikke-autoriserende som gren |
| purpose://capability | scaffold.operations | **OPPRETT · INN-IA** | Samler de fem `capability.*`. Ikke-autoriserende som gren |
| purpose://questionnaire | digital-work.collect-structured-input | **OPPRETT** | Book har barn under `questionnaire.*` uten at forelderen finnes |
| purpose://self-determination | root | **OPPRETT** | `self-determination.data` trenger en forelder som ikke er `root` direkte |

De øvrige 25 implisitte foreldrene fra D0 opprettes **ikke**. De er artefakter av navngivning,
ikke manglende formål. Det er nettopp derfor D0 må avgjøres: uten den regelen ville en
generator laget alle 29.

## Det jeg er minst sikker på

1. **INN-IA er en ny egenskap i taksonomien.** Den finnes ikke i dagens format. Å innføre den
   er en endring i skjemaet, ikke bare i innholdet, og den binder seg til A1/A4. Hvis du heller
   vil ha det som en egen nodetype eller en facet, sier du det — men jeg vil ikke ta inn elleve
   kapabilitetsnoder som vanlige formål uten et skille.
2. **`analysis.decision-support` som INN og ikke INN-IA** er et skjønn. Ni treff gjør den til
   den mest brukte, og «få beslutningsstøtte» leses som et brukerformål. Men grensen mot
   `analysis.synthesis` er tynn.
3. **Ingen UTGÅR.** Jeg fant ingen node som var trygg å droppe. Det kan bety at jeg er for
   raus. Den mest åpenbare kandidaten hvis du vil beskjære: `analysis.evidence-ledger` og
   `analysis.meta-evaluation`, som begge har tre treff og er rene apparatbegreper.
4. **74 + 4 = 78 noder** er langt under 100 000. Rammekostnaden avgjøres ikke av dagens
   taksonomi, men av hva registeret skal inneholde når det er i bruk — det tallet er `ukjent`
   og bør måles, ikke antas.

## Kjetils svar 2026-09-13

- **D0: ja.** «Er forslag D0 en god ide» — ja, med det tillegget at vi trenger en entydig måte å
  referere til en Purpose på *samtidig* som de kan slås opp med keypaths. Det er behandlet i
  `contract/purposeref-og-keypath.md`.
- **Punkt 2: ja** — INN-IA som skille. **Besvart 2026-09-15 (Valgbenken v-innia, alternativ a): facet** — felles nodeform med erklært egenskap `INN-IA`; autorisasjonsgrensen (A1/A4) må uttrykkelig avvise slike noder som primærformål (håndhevet regel, ikke konvensjon). Ikke egen nodetype.
- **Punkt 3: ja** — de elleve INN-IA-radene og de to skjønnsmessige INN-radene i tabell A.
- **Punkt 4: ja** — tabell B i bulk, alle 26.
- **Punkt 5: ikke eksplisitt besvart.** Tabell C følger nødvendig av punkt 3: de elleve
  IA-radene trenger `purpose://analysis` og `purpose://capability` som foreldre, og
  `questionnaire.campaign`/`response` trenger `purpose://questionnaire`. Jeg tar C som implisitt
  ja og går videre — **si fra hvis det er feil.**
- Kjetil la til: *«Vi har foreløpig få noder og vi vil få mange fler. Vi skal bruke Purpose til å
  normalisere produkter etterhvert også.»* Det gjør produktnoder til volumet som bærer
  100 000-tallet — taksonomien selv er 78 noder.

## Det jeg trenger fra deg

- Ja/nei til **D0** (kanter bare fra `parentRef`, aldri fra punktum i ref-en).
- ~~Ja/nei til **INN-IA** som skille, og i så fall om det skal være nodetype eller facet.~~ **Avgjort: ja, facet (2026-09-13 / 2026-09-15).**
- Ja/nei til de elleve INN-IA-radene og de to skjønnsmessige INN-radene i tabell A.
- Ja/nei til tabell B i bulk, eller pek ut de du vil ta ut.
- Ja/nei til de fire nye foreldrene i tabell C.
