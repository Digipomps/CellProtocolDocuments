# Forsøk: kan AI Act-klassifisering avledes fra HAVENs formålserklæringer?

Dato: 2026-08-18

Status: forskningsartefakt. **Ingenting her er slått sammen med
`Book/haven_purpose_knowledge_base_v0.json`, og ingen indeks i `Book/` er rørt.**
Isolasjonen er et premiss fra Kjetil og en betingelse for at målingene skal bety
noe.

Oppfølging av `Deliverables/EU_AI_Act_Dekomponering_Til_Formaal_2026-08-18.md`,
spørsmål 5.

---

## Spørsmålet

Ikke «kan vi skrive AI Act inn i formål», men:

> Fordi HAVEN krever at hver Cell **erklærer formål eksplisitt, aldri avledet**,
> og fordi AI Act klassifiserer risiko ut fra **intended purpose** — kan
> klassifiseringen da *beregnes* fra formålserklæringen i stedet for å leses fram
> av et menneske?

Dette er også en test av selve formålsstrukturen: tåler den en oppgave den ikke
ble designet for?

---

## Metode

To kjøringer mot samme fasit, over alle 57 formålsnodene i kunnskapsbasen.

**Kjøring A — leksikalsk avledning fra dagens tekst.** Bruker feltene som
allerede finnes: `title`, `summary`, `goal.outcome`, `successSignals`,
`interests`, `matchingHints`. Samme normalisering som
`Tools/PurposeKnowledge/derive_purpose_index.mjs`, IDF-vektet, slik at generiske
ord teller mindre. Dette er den mest velvillige rimelige oppsettet for
hypotesen «teksten vi har er nok».

**Kjøring B — regelavledning fra fem erklærte fasetter.** Hver node erklærer
`domain`, `decisionEffect`, `dataSubjects`, `outputModality`, `aiInvolvement`,
pluss noen få valgfrie flagg. Klassifiseringen utledes med regler, ikke slås opp.

Trigger-ordene i overlayet er skrevet **kun fra lovtekstens ordlyd**. HAVENs
vokabular ble bevisst ikke konsultert. Ellers hadde kjøring A vært rigget.

Fasiten ble skrevet **før** noen kjøring, ved å lese hver node mot overlayet.

Filer:

| Fil | Innhold |
| --- | --- |
| `eu_ai_act_overlay_v0.json` | 27 regulatoriske noder: art. 5 (9), vedlegg III (8), art. 50 (4), GPAI (2), virkeområde/derogasjon (4) |
| `ground_truth_v0.json` | Fasit for alle 57 formål, med `confirmed` / `conditional` / `boundary` |
| `haven_purpose_regulatory_facets_v0.json` | De fem erklærte fasettene per node — forslaget til skjemautvidelse |
| `derive_ai_act_classification.mjs` | Selve harnesset |
| `results/summary.json`, `results/detail.json` | Målinger og full node-for-node-diff |

Kjør: `node derive_ai_act_classification.mjs`

---

## Resultat

|  | Kjøring A (dagens tekst) | Kjøring B (fem erklærte fasetter) |
| --- | --- | --- |
| Presisjon | **0,036** | **0,950** |
| Dekning | 0,182 | 0,864 |
| F1 | **0,060** | **0,905** |
| Falske positive | **108** | **1** |
| Noder helt riktig | 8 / 57 (14 %) | **53 / 57 (93 %)** |

Delt opp etter hvor sterk plikten er i fasiten:

| Fasitstyrke | Antall | Dekning A | Dekning B |
| --- | --- | --- | --- |
| `confirmed` — plikten fester seg på nodens egne premisser | 13 | 0,154 | **1,000** |
| `conditional` — fester seg avhengig av bruk noden ikke erklærer | 5 | 0,400 | **1,000** |
| `boundary` — fester seg ikke, men ligger nær et forbud | 4 | 0,000 | **0,250** |

---

## Funn 1: dagens formålstekst er ubrukelig til dette

Presisjon 0,036 betyr at 27 av 28 utslag er støy. 108 falske positive over 57
noder.

Terskelen er ikke problemet. Sveip over åtte terskler:

| Terskel | 0,2 | 0,4 | 0,6 | 0,8 | 1,0 | 1,5 | 2,0 | 3,0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | 0,049 | 0,055 | 0,060 | 0,019 | 0,039 | 0,067 | 0,083 | 0 |
| Falske positive | 137 | 120 | 108 | 81 | 28 | 7 | 1 | 0 |

F1 kommer aldri over 0,083. Kurven har ikke et punkt der metoden virker — den går
fra støy til taushet uten å innom noe brukbart.

Feilene er heller ikke tilfeldige. De er systematiske og lærerike:

- `purpose://self-determination.data.manner` treffer GPAI-dokumentasjon, vedlegg
  III.3, prediktiv politiarbeid og sosial scoring — på ordene *model*,
  *training*, *profiling*, *scoring*. Noden handler om eierens **kontroll over**
  profilering. Leksikalsk avledning kan ikke se forskjell på å *utøve* en praksis
  og å *forby* den. Det er ikke en justerbar svakhet, det er en egenskap.
- `purpose://root` — «Alle mennesker er like mye verdt» — treffer forbudet mot
  CSAM-generering, på ordet *child*, via `matchingHints`.
- `purpose://preference.owner-controlled` treffer prediktiv politiarbeid på
  *profiling*, i en node hvis hele poeng er at profilering ikke skjer.
- `purpose://source.methodology.current` treffer vedlegg III.8 (rettspleie) og
  III.6 (rettshåndhevelse) på *law*, *facts*, *evidence*. Noden handler om
  kildeferskhet.

Dette bekrefter §6 i mulighetsanalysen med tall: lovtekstens vokabular og HAVENs
vokabular kolliderer på nøyaktig de ordene som bærer mening i begge. Å slå
overlayet inn i hovedindeksen ville vært en målt katastrofe, ikke en antatt.

## Funn 2: fem erklærte fasetter er nok — for pliktene

F1 0,905, og **full dekning på alle 18 faktiske plikter** (13 `confirmed` + 5
`conditional`). Én falsk positiv i hele kjøringen.

Fasettene som gjør jobben:

```
domain          none | biometrics | critical-infrastructure | education |
                employment | essential-services | law-enforcement |
                migration-border | justice-democracy
decisionEffect  none | informational | influences-human-decision |
                automated-decision-with-legal-or-similar-effect
dataSubjects    none | self-owner | named-third-parties | public | vulnerable-groups
outputModality  none | structured-data | ui-render |
                natural-language-to-human | synthetic-media
aiInvolvement   none | deterministic-code | model-assisted | model-generated
```

Designkravet på vokabularet er strengt og bevisst: **hvert felt skal kunne fylles
ut av en Cell-forfatter som aldri har lest AI Act.** Et felt som bare en jurist
kan svare på, hører ikke hjemme her. Alle fem består den prøven.

At `aiInvolvement` og `outputModality` alene bærer hele art. 50 er verdt å merke
seg. Regelen «modell involvert **og** output går til et menneske → art. 50(1)» er
to felt og én linje, og den traff 7 av 7.

## Funn 3: den viktigste grensen går ikke ved plikt, men ved nærhet

Dekning på `boundary`-tilfellene er **0,25** — én av fire.

De tre bommene:

| Node | Fasit | Hvorfor regelen bommer |
| --- | --- | --- |
| `purpose://preference.owner-controlled` | art. 5(1)(c) grense | Forfatteren erklærer ærlig `infersPersonalCharacteristics: false`. Erklæringen er riktig. Regelen har ingenting å gripe i. |
| `purpose://event.privacy-preserving-networking` | art. 5(1)(c) grense | Å matche mennesker mot mennesker er evaluering av personer, men ingen fasett fanger det. |
| `purpose://value-and-commons` | vedlegg III.5 grense | Verdiretur er ikke «essential services» i dag, men kan bli det. Ingen fasett uttrykker «kan bli». |

Den ene treffet — `purpose://personal-context.semantic-state` — traff bare fordi
forfatteren erklærte `infersPersonalCharacteristics: true`.

Dette er det egentlige funnet, og det er en negativ resultat verdt mer enn F1-tallet:

> **Regelavledning finner plikter som fester seg. Den finner ikke funksjonalitet
> som ligger nær et forbud uten å utløse det.**

En grense oppstår av hva systemet *kunne blitt* med én designbeslutning til, og
det er per definisjon ikke i erklæringen. Grensedeteksjon krever et fiendtlig
pass — et menneske eller en modell som spør «hva skal til for at dette blir
forbudt?» — ikke en regel.

Praktisk: rapporten trenger to kolonner. *Plikter* kan avledes. *Grenser* må
gjennomgås, og gjennomgangen må ha dato og navn.

## Funn 4: én uenighet, og modellen har trolig rett

`purpose://content.review-before-publish`: regelen ga art. 50(1), fasiten ikke.

Ved gjennomgang tror jeg **regelen har rett og jeg tok feil**. Eieren som
gjennomgår modellgenerert innhold, interagerer med et AI-system. Fasiten er ikke
rettet i etterkant — å justere fasiten etter å ha sett resultatet er akkurat den
feilen som gjør slike målinger verdiløse. Uenigheten står, og den reelle
presisjonen i kjøring B er trolig 1,00, ikke 0,95.

---

## Hva forsøket *ikke* viser

Dette er den delen som avgjør om tallene kan brukes.

1. **Én annotatør skrev både fasit, fasetter og regler.** Det er den alvorligste
   svakheten. Kjøring B måler *om reglene dekker fasettene*, ikke om et menneske
   erklærer fasetter riktig. Ekte validering krever at noen andre enn
   regelforfatteren erklærer fasettene blindt.
2. **Fasettene er skrevet av noen som kjenner svaret.** At
   `purpose://project-work.work-items` fikk `domain: employment` er en riktig,
   men informert, erklæring. En Cell-forfatter ville kanskje skrevet `none` —
   og da bommer kjøring B på alle fem vedlegg III-treffene. **Dette er den
   sannsynlige feilmoden i produksjon, og forsøket måler den ikke.**
3. **Lovteksten er ikke lest fra EUR-Lex.** Overlayets `statutoryCore` er
   parafrasert fra sekundærkilder. Hver node bærer `textSourceStatus` som sier
   det. Nodene må forankres artikkel for artikkel før noe av dette brukes.
4. **57 noder er et lite datasett** med 22 positive etiketter. Et enkelt
   feilmerket grensetilfelle flytter `boundary`-dekningen med 25 prosentpoeng.
5. **Ingen bruksdata.** Klassifiseringen bygger på hva noden sier den er, ikke på
   hva scaffoldet faktisk gjør i drift.

---

## Konsekvens for formålsstrukturen

Kjetil spurte om dette også var en test av om formålsstrukturen tåler oppgaven.
Svaret er delt.

**Det som holdt:** enkeltforelder-tre med kryssende fasetter var riktig form.
Rolle, risikoklasse og livsløp lot seg legge som fasetter uten å forstyrre treet.
Kravet fra Book 23 om at hvert formål må ha et observerbart Goal, viste seg å
være akkurat riktig disiplin — det er den samme disiplinen som skiller
automatiserbar verifikator fra bevis-tilstedeværelse.

**Det som ikke holdt:** fri tekst er ikke en erklæring. Dagens noder *beskriver*
formål på prosa; de *erklærer* det ikke i noe maskinen kan regne på. Book 09 sier
formål skal være «explicit (never inferred)» — men eksplisitt for et menneske er
ikke det samme som eksplisitt for en regel. Kjøring A er hva som skjer når man
forveksler de to. Tallet er 0,06.

Det er en generell lærdom, ikke en AI Act-lærdom: enhver framtidig maskinell bruk
av formålstreet vil treffe den samme veggen.

**Arv må fortsatt ikke brukes.** Reglene bruker `article6_3` per node.
`purpose://project-work.project-portfolio` og
`purpose://project-work.current-status-and-outstanding` fikk
`derogation-candidate` mens `purpose://project-work.work-items` ikke gjorde det —
tre søsken under samme forelder, forskjellig utfall. Hadde plikter blitt arvet
nedover treet, ville alle tre fått samme svar, og to av dem feil.

---

## Lisens og rolle — svar på spørsmål 2 og 3

Kjetil bekreftet Apache-2.0 for HAVEN-kode med DiMy holdt utenfor, og at
Digipomps er administrator, bruker, leverandør og garantist.

Tre konsekvenser, som alle peker samme vei:

**1. Art. 2(12) hjelper mindre enn det ser ut til.** Unntaket for fri og åpen
lisens gjelder ikke for art. 5, ikke for art. 50 og ikke der systemet settes i
drift som høyrisiko. Det unntar altså nettopp *ikke* den delen som gjelder nå.
Unntaket rydder bort kapittel III — som uansett er utsatt til 2027-12-02.

**2. Unntaket følger utgivelsen, ikke organisasjonen.** Koden Digipomps
*distribuerer* under Apache-2.0 er én ting. Instansen Digipomps *drifter* er en
annen: å sette i drift under eget navn er leverandørrollen, og den følger ikke
lisensen. Dobbeltrollen splitter analysen i to, og bare den ene halvdelen er
dekket.

**3. Rettsakten har ingen kategori for allmenningsforvalter.** Rollene er
leverandør, ibruktaker, importør, distributør og autorisert representant. At
funksjonaliteten er brukernes eiendom eller rettighet er en styringsmodell, ikke
en rolle i art. 3. Digipomps vil bli lest som leverandør *og* ibruktaker.
Allmenningsrammen gir ingen lettelse — den bør derfor ikke brukes som argument
utad om at HAVEN står utenfor.

Motstykket er reelt: art. 25 flytter leverandøransvaret til den som setter en
fork i drift under eget navn eller endrer den vesentlig. Digipomps svarer for det
Digipomps drifter, ikke for hver fork. Det er en styrke i modellen, og den bør
formuleres slik.

---

## Anbefaling

1. **Ta inn de fem fasettene** i formålsskjemaet, som valgfrie felt på
   `capability`-noder. De er billige, produktspråklige og gir målt 0,905.
2. **Ikke ta inn overlayet i `Book/`.** Det blir liggende her, med egen indeks,
   nådd ved eksplisitt oppslag.
3. **Neste eksperiment er blind erklæring.** La Codex — eller hvem som helst som
   ikke har sett fasiten — erklære de fem fasettene for de 57 nodene fra
   nodeteksten alene. Kjør på nytt. Det tallet er det ærlige tallet, og gapet
   mellom det og 0,905 er den reelle kostnaden ved metoden.
4. **Grensedeteksjon som eget spor.** Fire kjente grensetilfeller ligger i
   fasiten. De trenger et fiendtlig gjennomgangspass, ikke en regel.
5. **Forankre overlayet i EUR-Lex** før noe av dette forlater forskningsmappa.

Ingen del av dette er en samsvarsvurdering. En grønn kjøring betyr at reglene
dekker fasettene — ikke at HAVEN etterlever AI Act.

---

## Kilder

- [Regulation (EU) 2024/1689 — EUR-Lex, CELEX 32024R1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — må leses artikkel for artikkel før forankring
- [Article 2: Scope — artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/2/)
- [EU AI Act August 2026: What Applies After the Digital Omnibus — Certivo](https://www.certivo.com/blog-details/eu-ai-act-august-2026-what-applies-after-the-digital-omnibus)
- [EU AI Act Omnibus Agreement — Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)

Interne: `Book/09_Purpose_Interests.md`, `Book/23_Purpose_Knowledge_Base.md`,
`Book/haven_purpose_knowledge_base_v0.json`,
`Tools/PurposeKnowledge/derive_purpose_index.mjs`,
`Deliverables/HAVEN_Lisens_og_Governance_Forslag_2026-05-04.md`,
`Deliverables/EU_AI_Act_Dekomponering_Til_Formaal_2026-08-18.md`.
