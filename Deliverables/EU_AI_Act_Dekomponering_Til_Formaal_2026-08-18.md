# EU AI Act dekomponert til Formål — mulighetsanalyse

Dato: 2026-08-18

Status: analyse og anbefaling. Ingen noder er lagt inn i
`Book/haven_purpose_knowledge_base_v0.json`. Dokumentet vurderer om det bør
gjøres, hvor mye av rettsakten som faktisk lar seg dekomponere, og hva som må
endres i skjemaet først.

Forutsetninger kontrollert mot: `Book/09_Purpose_Interests.md`,
`Book/23_Purpose_Knowledge_Base.md`, `Book/26_Model_Knowledge_And_Purpose_Matching.md`,
`Book/haven_purpose_knowledge_base_v0.json` (57 noder, 5 fasetter),
`Deliverables/Brukerkontroll_Kriterier_Til_Formaal_2026-08-04.md`,
`Deliverables/Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md`.

---

## 1. Kort svar

**Ja, men ikke som ett tre, og ikke «hele».**

Rettsakten lar seg dekomponere til testbare formål i tre klart adskilte
porsjoner, og bare den første av dem er formål i HAVENs forstand:

| Del av rettsakten | Blir til | Andel av artikkelmassen (grovt) |
| --- | --- | --- |
| Bruksformål som reguleres (art. 5, vedlegg III, art. 50, GPAI) | **Formålsnoder** | ~20 % |
| Krav og plikter knyttet til rolle og risikoklasse (kap. III, art. 53–55) | **Goals med verifikator + fasetter** | ~35 % |
| Institusjonelt maskineri (kap. VI, VII, IX, X, XII) | **Ingenting. Utenfor scope.** | ~40 % |
| Definisjoner, virkeområde, ikrafttredelse (art. 1–4, 111–113) | **Skjemametadata, ikke noder** | ~5 % |

Prosentene er anslag basert på artikkelfordeling og må kontrolleres mot EUR-Lex
før de brukes utad.

Den viktigste enkeltinnsikten er ikke i tabellen, men i seksjon 3: **AI Act er
selv formålsbasert regulering**, og HAVEN er trolig det eneste systemet i
porteføljen der bruksformål er eksplisitt erklært av konstruksjon. Det gjør den
*motsatte* retningen mer verdifull enn den etterspurte — se seksjon 12.

---

## 2. Hva et Formål er i HAVEN, og hva en plikt er

Book 09 er utvetydig:

> A **Purpose** is a declaration of what an Identity or Cell intends to do.
> [...] explicit (never inferred) [...] not an authority or permission on its own.

Formål er **erklært intensjon**. AI Act består derimot i hovedsak av **normer**:
forbud, plikter og vilkår som fester seg til en *rolle* (leverandør, ibruktaker,
importør, distributør, autorisert representant) og en *risikoklasse*.

En plikt er ikke en intensjon. «Leverandøren skal etablere et
risikostyringssystem» kan ingen Cell erklære som sitt formål — det er en byrde
som pålegges utenfra, ikke et ønske som uttrykkes innenfra.

Derfor er den naive avbildningen **én artikkel = ett formål en kategorifeil**.
Den ville produsert ~113 noder som ser ut som formål, oppfører seg som krav, og
arver semantikk fra treet som de juridisk ikke har.

Dette er samme feilklasse som Brukerkontroll-notatet fant i den gamle skissen:
bokser som ser ut som kriterier, men ikke er testbare fordi de blander lag. Her
er risikoen større, fordi resultatet ville sett *mer* seriøst ut.

---

## 3. Hvorfor koblingen likevel er ekte

Rettsakten hviler på begrepet **intended purpose** (art. 3(12)) og
**reasonably foreseeable misuse** (art. 3(13)). Hele risikoklassifiseringen er
en funksjon av hva systemet er *ment til*:

- Art. 5 definerer forbudte praksiser i stor grad ved formål — «for the purpose
  of», «in order to».
- Vedlegg III klassifiserer høyrisiko ved **bruksområde**, ikke ved teknologi.
- Art. 6(3) gir unntak når systemet ikke «materially influences the outcome» —
  igjen en formålsvurdering.

Det betyr at rettsaktens egen bærende akse og HAVENs bærende akse er den samme.
Det er uvanlig og det er en reell mulighet.

**Men:** `intended purpose` i art. 3(12) er et juridisk fagbegrep — det som
leverandøren *oppgir* i bruksanvisning, markedsføring og teknisk dokumentasjon.
Det er ikke identisk med en `purposeRef` i HAVEN. Avbildningen mellom dem må
**erklæres eksplisitt per node**, ikke antas fordi ordet er det samme. Ellers
gjentar vi feilen fra Bridge-notatet: å slutte fra sammenfallende navn til
sammenfallende egenskap.

---

## 4. Sorteringen: fire normtyper, fire skjebner

### 4a. Forbudte formål → formålsnoder med negativ polaritet

Art. 5 gir åtte forbudte praksiser (bokstav a–h), pluss den nye
NCII/CSAM-bestemmelsen som gjelder fra 2026-12-02. Disse er ekte formål — de
beskriver hva et system er ment å gjøre — bare med motsatt fortegn.

HAVEN har ingen representasjon for **anti-formål** i dag. Alle 57 noder er
tillatte intensjoner. Dette må inn i skjemaet som `polarity: prohibited`, ikke
smugles inn som en vanlig node med «ikke» i tittelen.

Verdien er konkret og umiddelbar: et anti-formål tester som **fravær i
kapabilitetsregisteret**. «Ingen registrert Cell eksponerer emosjonsgjenkjenning
på arbeidsplass eller i utdanning» (art. 5(1)(f)) er en deterministisk
negativ test mot resolverens kapabilitetsliste. Den kan kjøres i CI i dag.

Dette er den enkeltdelen med best forhold mellom arbeid og nytte.

### 4b. Høyrisiko bruksområder → klassifiseringsnoder

Vedlegg III har åtte områder med om lag 20–24 underpunkter (biometri, kritisk
infrastruktur, utdanning, arbeidsliv, essensielle tjenester, rettshåndhevelse,
migrasjon, rettspleie og demokratiske prosesser). Disse er bruksformål og lar
seg avbilde direkte.

Men de er **klassifiseringsnoder**, ikke intensjonsnoder: de svarer på «er denne
funksjonaliteten høyrisiko?», ikke på «hva vil denne cellen». Blandes de inn i
hovedtreet, forurenser de formålsruting med bruksområder HAVEN ikke har.

Forventet svar for det meste av HAVEN er **nei**. Det er ikke et argument mot å
gjøre jobben — verdien ligger i at «nei» blir *dokumentert og testbart* i stedet
for antatt.

### 4c. Krav → Goals med verifikator, ikke noder

Kapittel III seksjon 2 (art. 8–15: risikostyring, datastyring, teknisk
dokumentasjon, logging, transparens mot ibruktaker, menneskelig tilsyn,
nøyaktighet/robusthet/cybersikkerhet) og seksjon 3 (art. 16–27: rollepliktene)
er **vilkår festet til et formål**, ikke formål.

Book 23 sier regelen allerede: *«a purpose that cannot name an observable Goal
is not ready to become canonical»*. Kravene er nettopp Goal-materiale — de har
`outcome`, `successSignals` og `verifier` innebygd i lovteksten.

`matchingIndexPlan.goalVerifierIndex` er allerede designet for dette:
`goalRef → verifier/capability`. Maskineriet finnes.

### 4d. Institusjonelt maskineri → utenfor scope

Kapittel VI (sandkasser), VII (styring, AI Office, AI Board), IX
(markedsovervåking), X (adferdskodekser), XII (sanksjoner) regulerer
myndigheter og medlemsstater, ikke programvare. Om lag 40 % av artikkelmassen.

Å dekomponere disse til formål ville produsert noder ingen test kan røre. Det er
ikke bare bortkastet — det er aktivt skadelig, fordi det gir en kunnskapsbase
der «dekket» og «testet» ikke lenger betyr det samme.

**«Hele» AI Act er derfor ikke et fornuftig mål.** Det riktige målet er *hele
den delen som fester seg til programvare vi faktisk lager*.

---

## 5. Volum, og hva det gjør med taksonomien

| Kilde | Anslag noder | Anslag Goals |
| --- | --- | --- |
| Art. 5 forbud | 8–10 | 8–10 |
| Vedlegg III | 22–28 | 22–28 |
| Art. 50 transparens | 4–6 | 10–14 |
| GPAI art. 51–55 | 4–6 | 15–25 |
| Art. 8–15 krav | 0 (fasetter) | 40–70 |
| Art. 16–27 rolleplikter | 0 (fasetter) | 50–90 |
| **Sum** | **~40–50** | **~150–240** |

Kunnskapsbasen har i dag **57 noder**. Et fullt AI Act-lag ville nesten doblet
den, med et fremmed domene som HAVEN ikke selv utvikler i.

Det er ikke uoverkommelig. Men det betyr at AI Act-laget ikke kan behandles som
«enda en gren» — det blir strukturelt likeverdig med resten av basen til sammen.

---

## 6. Treffkvalitetsrisikoen — den harde tekniske innvendingen

Dette er det sterkeste argumentet mot å slå AI Act inn i hovedtreet, og vi har
allerede måledata.

Brukerkontroll-notatet dokumenterte at én kandidatgren med norsk brødtekst dro
`evaluate_purpose_cases.mjs` fra **56/56 til 53/56**, fordi grenen kapret prompt
på generiske ord som «alle», «tilgang», «samtykke» og «profilering».

Det var **åtte noder**.

AI Act-teksten er bygget av nettopp de ordene som ødelegger en leksikalsk
invertert indeks: *system, data, risiko, bruk, person, vurdering, dokumentasjon,
transparens, tilsyn, tilgang, kvalitet, sikkerhet, formål*. Nesten hvert eneste
høysignal-token i dagens `tokenInvertedIndex` finnes i lovteksten, i høy
frekvens, i en helt annen betydning.

Førti til femti slike noder i samme indeks vil med stor sannsynlighet degradere
ruting for de eksisterende 57 alvorlig. Ikke marginalt — strukturelt.

**Anbefaling:** eget navnerom `purpose://regulatory.eu-ai-act.*` i et **eget
artefakt med egen indeks**, koblet til hovedtreet gjennom fasetter og eksplisitte
avbildningskanter. AI Act-noder skal treffes ved *eksplisitt ref-oppslag* og ved
*klassifisering av en kapabilitet* — aldri ved fritekstruting fra brukerprompt.

Regresjonsporten er ikke til forhandling: `evaluate_purpose_cases.mjs` skal stå
på 56/56 etter innføring, med nye fixtures lagt til, ikke gamle fjernet.

---

## 7. Strukturell mismatch: tre mot matrise

HAVEN har enkeltforelder-tre med kryssende fasetter. AI Act er en **matrise**:

```
(rolle × risikoklasse × livsløpsfase × modalitet) → plikt
```

Ett og samme system kan samtidig være vedlegg III-høyrisiko, bygget på en
GPAI-modell, og utløse art. 50-transparens. Samme plikt treffer leverandør og
ibruktaker forskjellig.

Modellen holder likevel — men bare hvis akseinndelingen er riktig:

- **Treakse = bruksformål.** Det er den eneste aksen som er hierarkisk.
- **Rolle, risikoklasse, livsløpsfase, modalitet = fasetter.**

Og én ting til, som er lett å ta feil av:

> **Arv i treet må ikke brukes til å propagere plikter.**

`ancestorBitsetIndex` og LCA-oppslaget er bygget for at mening skal arves
nedover. Juridisk gjelder det motsatte: plikter fester seg ved klassifisering,
ikke ved slektskap. At et underformål ligger under et høyrisiko-område betyr
ikke at det arver høyrisiko-plikter — art. 6(3) gir nettopp unntak for det.

Bruker vi arv her, produserer vi falske positiver som ser autoritative ut. Det
må stå som en eksplisitt begrensning i skjemaet, ikke som en muntlig avtale.

---

## 8. Testbarhet — tre nivåer, og de er ikke like mye verdt

Spørsmålet var «teste relevant funksjonalitet opp mot formålene». Da må vi være
ærlige om hva en verifikator faktisk kan avgjøre.

### Nivå 1 — deterministisk maskinell test (~25–35 % av pliktene)

Kan kjøres i CI uten menneske:

| Plikt | Verifikator mot eksisterende flate |
| --- | --- |
| Art. 50(1) opplysning om AI-interaksjon | skeleton-invariant, samme mekanikk som `purpose://skeleton.owner-entity-access` |
| Art. 50(2) maskinlesbar merking av syntetisk innhold | provenance-markør på generert output |
| Art. 50(4) merking av deepfake | tilstedeværelsestest på outputkontrakt |
| Art. 5(1)(f) emosjonsgjenkjenning arbeid/utdanning | **negativ test** mot kapabilitetsregisteret |
| Art. 5(1)(g) biometrisk kategorisering | negativ test mot kapabilitetsregisteret |
| Art. 12 logging | FlowElement-poster finnes, oppbevaringstid |
| Art. 14 menneskelig tilsyn | stopp-/overstyringsaffordanse finnes i skeleton |
| Art. 26 ibruktakers logging | avtalelivsløp og audit-assertions |

Dette er reell verdi og treffer flater HAVEN allerede tester.

### Nivå 2 — bevis-tilstedeværelse, ikke korrekthet (~35–40 %)

Art. 9 risikostyring, art. 10 datastyring, art. 11/vedlegg IV teknisk
dokumentasjon, art. 15 nøyaktighet/robusthet, art. 17 kvalitetsstyring.

Her kan en test avgjøre at *et dokumentert artefakt finnes, er datert, er ferskt
og er signert*. Den kan **ikke** avgjøre at innholdet er juridisk tilstrekkelig.
Benchmark-pakkene i Book 26 §9 er allerede riktig form for art. 15.

Forskjellen må være synlig i selve testresultatet. En grønn nivå-2-test som
rapporteres som «oppfylt» er en overpåstand.

### Nivå 3 — krever menneskelig skjønn (~30 %)

«Betydelig risiko for helse, sikkerhet eller grunnleggende rettigheter»,
«vesentlig forvrenge atferd», «rimelig forutsigbart misbruk», enhver
forholdsmessighetsvurdering.

Sterkeste mulige verifikator: *det finnes en menneskelig vurdering, av navngitt
person, med dato og begrunnelse, som ikke er utløpt*. Det er en
prosessverifikator, ikke en innholdsverifikator.

**Konsekvens:** `verifiability` må være et påkrevd felt per node, med disse tre
verdiene. Uten det kollapser skillet, og en suite som er 70 % nivå 2 og 3 vil bli
lest som om den var nivå 1.

---

## 9. Ferskhetsproblemet — hva som faktisk gjelder i dag

Kontrollert 2026-08-18. Digital Omnibus har flyttet på vesentlige datoer:

| Bestemmelse | Status per i dag |
| --- | --- |
| Art. 5 forbud | **I kraft** siden 2025-02-02 |
| Art. 4 AI-kompetanse | I kraft, men **svekket** — nå «støtte utvikling av» AI-kompetanse |
| GPAI art. 51–55 | **I kraft** siden 2025-08-02 |
| Art. 50 transparens | **I kraft** fra 2026-08-02 — altså to uker gammel |
| Art. 50(2) merking, systemer alt i markedet | frist **2026-12-02** |
| Nytt forbud mot NCII/CSAM-generering | fra **2026-12-02** |
| Vedlegg III høyrisiko (frittstående) | utsatt til **2027-12-02** |
| Vedlegg I høyrisiko (innebygd i produkt) | utsatt til **2028-08-02** |
| Regulatoriske sandkasser | utsatt til **2027-08-02** |

To ting følger av dette.

**For det første:** den delen som er tyngst å dekomponere — vedlegg III og
kapittel III-kravene — er også den som ikke gjelder på 16 måneder. Den delen som
gjelder *nå*, og som treffer det HAVEN faktisk sender ut (Co-pilot, lokal modell,
generert innhold), er art. 50 + art. 5 + GPAI + art. 4. Det er en langt mindre og
langt mer presserende porsjon.

**For det andre:** enhver dekomponering har en forfallsdato. Fasetten
`purpose://source.methodology.current` har allerede
`appliesTo: [..., "laws", ...]` — den er laget for akkurat dette. Hver node må
bære `sourceRef` på **CELEX-nivå med artikkel og ledd**, `sourceCheckedAt` og
`applicableFrom`. Advokatblogger, inkludert de som er brukt som kilde til
tabellen over, er *indikasjon*, ikke kilde. Selve nodene må forankres i EUR-Lex.

---

## 10. Gjelder AI Act HAVEN i det hele tatt?

Et scoping-funn som må avklares før noden skrives, ikke etter.

Art. 2(12) unntar systemer utgitt under fri og åpen lisens — **med unntak av**
høyrisiko, art. 5-forbudte praksiser og art. 50-transparens.

For HAVEN betyr det, hvis lisensvalget lander på fri/åpen:

- Kapittel III-kravene (art. 8–27) er trolig **ikke** anvendelige.
- Art. 5 og art. 50 gjelder **uansett**.

Det er nøyaktig samme delmengde som seksjon 9 pekte ut som den som gjelder nå.
De to argumentene konvergerer på samme lille pakke, fra hver sin kant. Det er et
sterkt signal om hvor arbeidet skal begynne.

Videre unntas rent personlig ikke-yrkesmessig bruk (art. 2(10)) og forskning og
utvikling før markedsføring (art. 2(8) — men *ikke* testing under reelle
forhold). Begge treffer HAVENs nåværende fase.

Dette er en juridisk vurdering jeg ikke kan avgjøre. Det som *kan* avgjøres her
er at spørsmålet har store konsekvenser for omfanget, og at det bør besvares
først.

---

## 11. Skjemautvidelse som må på plass

Dagens `haven.purpose-knowledge-base.v0` mangler felt for dette. Konkret forslag
til regulatoriske noder:

```json
{
  "purposeRef": "purpose://regulatory.eu-ai-act.transparency.ai-interaction",
  "polarity": "required",
  "normType": "transparency",
  "legalRef": {
    "celex": "32024R1689",
    "article": "50",
    "paragraph": "1",
    "point": null,
    "consolidatedAs": "2026-08-18"
  },
  "addressee": ["provider"],
  "applicableFrom": "2026-08-02",
  "verifiability": "automatable",
  "havenApplicability": "applies",
  "inheritsObligations": false,
  "sourceCheckedAt": "2026-08-18"
}
```

Nye felt, med begrunnelse:

- `polarity`: `required` | `prohibited` | `classifying` — anti-formål trenger
  førsteklasses representasjon (§4a).
- `normType`: `prohibition` | `requirement` | `transparency` | `classification` |
  `derogation` | `definition`.
- `legalRef`: CELEX + artikkel + ledd + bokstav. Uten dette er noden ikke
  etterprøvbar.
- `addressee`: rolle. Dette er en fasettakse, ikke en treakse (§7).
- `applicableFrom` / `applicableUntil`: uunngåelig gitt §9.
- `verifiability`: de tre nivåene fra §8. **Påkrevd felt.**
- `havenApplicability`: `applies` | `not-applicable` med begrunnelse |
  `conditional`. Et dokumentert «gjelder ikke oss, fordi …» er en leveranse i
  seg selv.
- `inheritsObligations: false` som eksplisitt sperre mot LCA-propagering (§7).
- `derogatesFrom` / `conditionedBy`: rettsakten er full av unntak (art. 2, art.
  6(3)). Uten kantene blir nodene feil.

---

## 12. Den motsatte retningen er mer verdt

Oppdraget var: dekomponer rettsakten så vi kan teste funksjonalitet mot den.

Den er gjennomførbar. Men den mest interessante muligheten går andre veien.

Fordi HAVEN krever at hver Cell **erklærer formål eksplisitt, aldri avledet**,
og fordi AI Act klassifiserer risiko ut fra **intended purpose**, har HAVEN
tilfeldigvis akkurat det inputet klassifiseringen krever — og det har nesten
ingen andre systemer. I vanlig programvare må intended purpose rekonstrueres
etterpå, av mennesker, fra dokumentasjon som ikke ble skrevet for formålet.

Det åpner for at HAVEN kan **avlede sin egen risikoklassifisering fra
formålserklæringene**, som en beregning i stedet for en advokatoppgave, og at
klassifiseringen oppdateres automatisk når en ny Cell registreres med et nytt
formål.

Jeg vil ikke overselge dette. Det forutsetter at avbildningen fra §3 er gjort
eksplisitt og at nivå-3-skjønnet fortsatt gjøres av mennesker. Det gir ikke
etterlevelse. Men det er en reell strukturell fordel som er verdt å utforske før
vi bruker uker på å transkribere kapittel III.

---

## 13. Anbefalt trinnvis plan

**Trinn 0 — avklaring (før noe skrives).** Lisensspørsmålet i §10. Beslutning om
eget navnerom og egen indeks (§6). Beslutning om at «hele» erstattes av «hele
den anvendelige delen».

**Trinn 1 — pilot, det som gjelder nå.** Art. 5 + art. 50 + art. 4 + GPAI-berøring.
Anslag 15–18 noder. Alle med ekte verifikator koblet til eksisterende testflater.
Regresjonsport: 56/56 må holde. Dette er den eneste porsjonen som er både
rettslig aktuell, sannsynlig anvendelig og teknisk testbar i dag.

**Trinn 2 — vedlegg III som klassifiseringslag.** Ikke for å oppfylle
høyrisikokrav, men for å kunne svare dokumentert «nei, ikke høyrisiko, fordi …»
på hvert bruksområde. Forventet utfall er negativt og det er poenget.

**Trinn 3 — kapittel III som Goal-/verifikatorbibliotek.** Først når vedlegg III
faktisk treffer noe, eller når frist 2027-12-02 nærmer seg.

**Aldri — kapittel VI, VII, IX, X, XII.** Institusjonelt maskineri. Utenfor
scope, og det skal stå skrevet at det er et valg, ikke en forglemmelse.

---

## 14. Claim-sikkerhet

En grønn testsuite må aldri kunne presenteres som «HAVEN er AI Act-compliant».

Suiten er en **intern designkonformitetsport**, og skal hete det. Den bruker
rettsakten som kilde til testbare designkriterier — den er ikke en
samsvarsvurdering, ikke en juridisk vurdering og ikke et bevis.

Praktiske sperrer som bør inn samtidig med trinn 1:

- Rapportoverskrift som sier «designkriterier avledet av», ikke «etterlevelse av».
- Nivå-2- og nivå-3-resultater rapporteres i egen kolonne, ikke slått sammen med
  nivå 1 i én prosent.
- `sourceCheckedAt` eldre enn 90 dager gir gul status på hele suiten, ikke bare
  på noden.
- Ingen ekstern kommunikasjon om AI Act-arbeidet uten gjennomgang mot
  `haven-claim-review`.

---

## 15. Åpne spørsmål til Kjetil

1. **Hva er faktisk formålet med formålet her?** Tre helt forskjellige oppdrag
   ligger inni spørsmålet, og de gir ulik løsning: (a) intern designport som
   hindrer at vi bygger noe forbudt, (b) etterlevelsesdokumentasjon for søknader,
   investorer eller NLnet, (c) et produkt — at HAVEN *tilbyr* formålsbasert
   AI Act-klassifisering til andre. Mitt notat forutsetter (a). Er det riktig?

2. **Lisens.** Går HAVEN mot fri/åpen lisens i art. 2(12)-forstand? Svaret
   halverer eller dobler omfanget, og bør avgjøres før trinn 1.

3. **Rolle.** Er HAVEN leverandør, ibruktaker, eller begge — og for hvilke deler?
   Lokal modellruting, Co-pilot og scaffold-hosting kan lande på ulike roller for
   samme kodebase. `addressee`-fasetten er meningsløs uten dette svaret.

4. **Er anti-formål akseptabelt i modellen?** Book 09 sier formål er erklært
   intensjon. Et forbudt formål er ingen erklærer. Skal `polarity: prohibited`
   inn i selve formålsmodellen, eller skal forbud ligge som en egen normtype
   utenfor formålstreet? Dette er en ren modellbeslutning som er din.

5. **Prioritet mot §12.** Skal vi gjøre den etterspurte retningen først, eller
   bruke to dager på å teste om avledet klassifisering fra formålserklæringer
   faktisk virker? Den siste er mer usikker og potensielt mye mer verdt.

---

## Kilder

Rettsaktens innhold og status er kontrollert mot sekundærkilder 2026-08-18.
Nodene selv må forankres i EUR-Lex på artikkelnivå før de skrives.

- [EU AI Act August 2026: What Applies After the Digital Omnibus — Certivo](https://www.certivo.com/blog-details/eu-ai-act-august-2026-what-applies-after-the-digital-omnibus)
- [EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key Changes — Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- [Article 2: Scope — artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/2/)
- [EU AI Act unpacked #34: The final Digital Omnibus on AI — Freshfields](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-34-the-final-digital-omnibus-on-ai-key-amendments-to-the-a-102nber)
- [The Digital AI Omnibus: Proposed deferral of high risk AI obligations — DLA Piper](https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/The-Digital-AI-Omnibus-Proposed-deferral-of-high-risk-AI-obligations-under-the-AI-Act)
- [Regulation (EU) 2024/1689 — EUR-Lex, CELEX 32024R1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

Interne kilder: `Book/09_Purpose_Interests.md`, `Book/23_Purpose_Knowledge_Base.md`,
`Book/26_Model_Knowledge_And_Purpose_Matching.md`,
`Book/haven_purpose_knowledge_base_v0.json`,
`Deliverables/Brukerkontroll_Kriterier_Til_Formaal_2026-08-04.md`,
`Deliverables/Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md`.
