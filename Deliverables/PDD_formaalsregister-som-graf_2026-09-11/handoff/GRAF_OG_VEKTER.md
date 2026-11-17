**Delvis.** En tekst kan uten AI kobles deterministisk til kjente formåls- og lærdomsnoder og brukes som signaler i den eksisterende perspektivgrafen. Det er avgrenset klassifisering og gjenfinning; en full graf over tekstens mening, negasjon, aktører og nye sammenhenger er ikke levert av dette leksikonet. Det trengs en registeradapter, eksplisitte tekstkoblinger og kontrollerbare tilbakemeldinger. Eksperimentet gir tre forbedringer på trente oppgaver, men ingen dokumentert fordel mot TF-IDF når oppgaven holdes utenfor treningen. Kravet «målbart bedre enn alternativene» er derfor **ikke oppfylt**; sammenligningen med lokale embeddings er **ukjent**.

# Perspektivgraf og lærte vekter

Dato: 2026-09-12. Arbeid: `perspektivgraf-og-laerte-vekter-20260912`.
Eier/integrator: Codex i denne tråden. Status: **VERIFIED – eksperiment og rapport**;
produktnytte ikke bekreftet. Ingen git-mutasjon, Docker, Swift-bygg eller installasjon.
Eksklusivt skrevet: de tre nye måleskriptene, denne rapporten og
`maaling/graf_resultater.json`. Teststrategiens eksisterende filer er gjenbrukt.
Kontakt med den parallelle kjøringens tråd: **ukjent**; integrasjonen er gjennom
dens tilgjengelige evaluator, frosne korpus og dokumenterte kontrakt.

Formål: etterprøvbar matching, forankret i eksisterende
`purpose://quality.build-and-regression`. Mål: samme fasit/k for alle alternativer,
tre etterprøvbare før/etter-eksempler og <100 ms ved oppslag. Brukerbestillingen
autoriserer disse avgrensede Python-eksperimentene; ingen overordnet produktport
er godkjent her.

«Uten AI» betyr her uten språkmodell- eller embedding-inferens. Vektoppdateringen
er enkel statistisk læring; forsøket trenger ingen modellleverandør.

| Deloppgave | Målt resultat | Vurdering |
|---|---|---|
| 1. Gjenbruk | 57 Book-noder, 13 ekstra pakkenoder, 44 lærdommer, 59 purposeRefs-kanter | Motoren kan gjenbrukes; rå JSON kan ikke dekodes direkte |
| 2. Tekstsignaler | Jaccard 0,195, null felles; R+@10 0,357 | Selektiv, ikke dokumentert bedre enn TF-IDF |
| 3. Forplantning | Ingen endret topp-10 for 19 fulltekstqueries; «deploy» går fra 2 til 22 aktiverte lærdommer | Bredere aktivering uten påvist relevansgevinst |
| 4. Læring | Tre trente oppgaver forbedres; holdout R+@10 0,357 | Mekanismen virker; nytte på nye oppgaver ikke etablert |
| 5. Hastighet | Se målingene under: varm batch og engangsbygg + batch <100 ms | Hele statistikkjobben og bygg for hvert oppslag overskrider grensen |

## Fasit og sammenligningsbetingelser

[Målt utgangspunkt](../maaling/MAALT_UTGANGSPUNKT.md) og
[TF-IDF-spiken](../maaling/spike_tfidf_baseline.py) ble lest først.
[Teststrategien](TESTSTRATEGI_MATCHING.md) og
[evaluer.py](../maaling/evaluer.py) var tilgjengelige. Jeg gjenbruker dens
`run_matcher`, `score`, `truth_labels`, `paired_stats` og snapshot-validering.

Primærkorpus: [korpus_44.json](../maaling/korpus_44.json), 19 oppgaver / 44 lærdommer.
Snapshot-hash: `1437e34b2faa23210156cc71ef981e20cdd57ec18a0c2739a49e1d06ab26f00f`. Dette er teststrategiens frosne kohort, ikke en påstand
om dagens bevegelige register. Alle kandidater får samme strenge §0 og samme
dokumentunivers. Tag-matcheren bruker de faktiske funksjonene i `purpose_dev.py
lookup` og beholder registerrekkefølgen. TF-IDF gjenbruker tokenizer, vekting,
cosinus og tie-rekkefølge fra spiken. BM25 bruker samme tekstfelt og tokenizer.

**15 source-positive par i fire oppgaver, ingen negative dommer, ingen fullstendig
vurdert oppgave.** De øvrige 15 oppgavene har uvurdert relevans. Source brukes til
evaluering og i den uttrykkelige treningsfasen, aldri som leksikonfelt eller
matcherens queryfelt. Holdout utelater hele oppgaven og dens dommer fra trening.
Foldvelgeren henter modellen for riktig utelatt query; dette er
evalueringsorkestrering, ingen planlagt produktruting.

P+@5 er **kjente treff / 5**, makrosnitt over 19 oppgaver: nedre grense for sann
presisjon. Øvre grense er 1,000 [1,000, 1,000] for alle kandidater. **Sann P@5 er
ukjent.** R+@10 har bare kjente positive i nevneren, makrosnitt over fire oppgaver;
sann total dekning er **ukjent**. MRR+ bruker første kjente positive i hele
rangeringen på de samme fire oppgavene; sann MRR er **ukjent**. MRR+@10 finnes
også i JSON. Alle kandidater bruker samme k for hvert mål. Lesebyrde er symptom
+ prevention, to avsnitt per vist lærdom, ikke antatte minutter.

Alle intervaller er diagnostisk 95 % persentil-bootstrap: 10 000 uttrekk av hele
oppgaver, seed 20260912. Parvise forskjeller resampler de samme oppgaveparene.
Fire positive oppgaver er et svært svakt usikkerhetsgrunnlag: et bootstrap-intervall
uten null kan fremdeles ha eksakt tosidig permutasjonsp >0,05. Alle parvise
metrikkprøver, intervaller, p-verdier og Bonferroni-korreksjon står i JSON.
De viste parvise relevansprøvene gir ikke korrigert p<0,05.

## Alle alternativer, samme fasit og samme k

| Kandidat | P+@5 nedre grense, n=19 | R+@10, n=4 | MRR+, n=4 | Avsnitt@10, n=19 |
|---|---:|---:|---:|---:|
| Vis alle 44, registerrekkefølge | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.036 [0.025, 0.046] | 20.000 [20.000, 20.000] |
| Dagens tag / praktisk vis-alt | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.050 [0.029, 0.072] | 20.000 [20.000, 20.000] |
| Tilfeldig, fast seed | 0.000 [0.000, 0.000] | 0.134 [0.000, 0.268] | 0.114 [0.081, 0.148] | 20.000 [20.000, 20.000] |
| Tilfeldig, eksakt forventning | 0.018 [0.002, 0.038] | 0.227 [0.227, 0.227] | 0.227 [0.136, 0.317] | 20.000 [20.000, 20.000] |
| TF-IDF, eksisterende spike | 0.063 [0.000, 0.158] | 0.476 [0.143, 0.833] | 0.642 [0.283, 1.000] | 20.000 [20.000, 20.000] |
| BM25 | 0.042 [0.000, 0.116] | 0.393 [0.000, 0.786] | 0.539 [0.079, 1.000] | 20.000 [20.000, 20.000] |
| Leksikon | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] |
| Graf, 1 hopp | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] |
| Graf, 2 hopp | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] |
| Graf, 3 hopp | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] |
| Lært bare purposeRefs (trening) | 0.042 [0.000, 0.116] | 0.357 [0.000, 0.750] | 0.531 [0.063, 1.000] | 20.000 [20.000, 20.000] |
| Lært signal+refs, bare + (trening) | 0.074 [0.011, 0.168] | 0.673 [0.417, 0.929] | 0.708 [0.417, 1.000] | 20.000 [20.000, 20.000] |
| Lært signal+refs, +/− (trening) | 0.105 [0.021, 0.232] | 0.917 [0.750, 1.000] | 0.875 [0.625, 1.000] | 20.000 [20.000, 20.000] |
| Ren hyppighet (trening) | 0.053 [0.000, 0.137] | 0.500 [0.000, 1.000] | 0.356 [0.087, 0.773] | 20.000 [20.000, 20.000] |
| Leksikon × hyppighet (trening) | 0.053 [0.000, 0.126] | 0.714 [0.250, 1.000] | 0.458 [0.167, 0.812] | 20.000 [20.000, 20.000] |
| Leksikon × hyppighet (holdout) | 0.000 [0.000, 0.000] | 0.071 [0.000, 0.214] | 0.066 [0.042, 0.095] | 20.000 [20.000, 20.000] |
| Lært signal+refs, +/− (holdout) | 0.032 [0.000, 0.084] | 0.357 [0.000, 0.750] | 0.233 [0.049, 0.417] | 20.000 [20.000, 20.000] |
| Lært +/−, blocker-vern (holdout) | 0.032 [0.000, 0.084] | 0.357 [0.000, 0.750] | 0.233 [0.049, 0.417] | 20.000 [20.000, 20.000] |
| Lokal embedding | ukjent | ukjent | ukjent | ukjent |

«Trening» betyr gjenmåling på utviklingsoppgavene som ga tilbakemelding, **ikke
gevinst på et uavhengig testsett**. «Holdout» betyr fire modeller: hver trenes
med ti hendelser fra de tre andre source-positive oppgavene, og måles på den
utelatte oppgaven. De 15 uvurderte oppgavene har ingen egne treningsdommer og
bidrar bare til presisjonsgrensene, spredningen og lesebyrden.

Vis-alt har ingen naturlig rangering: første k betyr faktisk registerrekkefølge.
Derfor kan første ti ha null kjente treff mens lesing av alle 44 gir R+=1.
Dagens uavkortede tag-liste viser **35,0 lærdommer**, mot utgangspunktets 34,9
fra en tidligere oppgaveavgrensning. I den frosne kohorten er uavkortet R+=0,9375.
Uavkortet tag-lesebyrde: 70.000 [66.526, 73.579] avsnitt; vis-alle-44: 88 [88, 88]. Alle topp-10-varianter viser 20 avsnitt. Faktisk lesetid er ikke målt.

Tilfeldig med seed er én deterministisk permutasjon per query. Den eksakte
forventningsraden integrerer alle uniforme permutasjoner: E(P+@5)=|R+|/44,
E(R+@10)=10/44; MRR+ summerer sannsynligheten for første positive på hver rang.
Bootstrap der måler variasjon mellom oppgaver, ikke tilfeldige kjøringer.
Denne ekstra kontrollen hindrer at en uheldig seed alene blir støygrensen.

`python3 -c 'import sentence_transformers'` ga `ModuleNotFoundError`.
`find_spec` fant heller ikke `torch`, `transformers`, `mlx` eller `gensim` i samme
Python 3.13.5. Andre Python-miljøer og kompatible modellvekter på maskinen:
**ukjent**. Ingen installasjon, modellnedlasting eller nettbasert inferens.
Det foreligger ikke evidens for at grafen slår AI-alternativet.

| Fra A til B (B − A) | Mål | Forskjell [95 % bootstrap] | Eksakt p |
|---|---|---:|---:|
| TF-IDF, eksisterende spike → Leksikon | r10 | -0.119 [-0.250, 0.000] | 0.500 |
| Leksikon → Graf, 3 hopp | r10 | 0.000 [0.000, 0.000] | 1.000 |
| Graf, 1 hopp → Lært signal+refs, bare + (trening) | r10 | 0.315 [0.107, 0.464] | 0.250 |
| Graf, 1 hopp → Lært signal+refs, +/− (trening) | r10 | 0.560 [0.167, 0.893] | 0.250 |
| Lært signal+refs, +/− (trening) → Leksikon × hyppighet (trening) | r10 | -0.202 [-0.750, 0.214] | 0.750 |
| Leksikon × hyppighet (holdout) → Lært signal+refs, +/− (holdout) | r10 | 0.286 [0.000, 0.750] | 0.500 |
| TF-IDF, eksisterende spike → Lært signal+refs, +/− (holdout) | r10 | -0.119 [-0.250, 0.000] | 0.500 |
| TF-IDF, eksisterende spike → Lært signal+refs, +/− (holdout) | mrr | -0.409 [-0.611, -0.144] | 0.125 |
| TF-IDF, eksisterende spike → Tilfeldig, eksakt forventning | r10 | -0.249 [-0.606, 0.084] | 0.375 |
| Leksikon → Tilfeldig, eksakt forventning | r10 | -0.130 [-0.523, 0.227] | 0.875 |


TF-IDF har best observert R+@10 og MRR+ blant de utrente tekstkandidatene.
Grafen vinner ikke over den. Holdout-læring reduserer observert MRR+ mot TF-IDF.
Ingen statistisk robust vinner er etablert, selv om enkelte treningsforskjeller
har positive bootstrap-intervaller.

## 1. Den eksisterende Swift-motoren

**OBSERVERT i kildekode; ikke bygd eller kjørt her:**

| Kontrakt | Presis kilde |
|---|---|
| PerspectiveNodeImpl har navn, stabil nodeIdentifier/reference og åtte vektede relasjoner: types, subTypes, parts, partOf, interests, purposes, entities, states | `CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:41`, `:72` |
| Weight<T> tar Double-vekt, inline node eller reference. Referansen løses via decoded context for Interest/Purpose/EntityRepresentation; ukjent ref kaster feil | `CellProtocol/Sources/CellBase/PurposeAndInterest/Weight.swift:13`, `:28`, `:64` |
| Signal tar relationship, ønsket weight, tolerance, token, ttl, hops, localVariables og collector. Token er kjøringsidentitet, ingen teksttokenizer | `CellProtocol/Sources/CellBase/PurposeAndInterest/Signal.swift:20` |
| match(start:signal:configuration:) async throws → MatchResult starter fra én ferdig node. Config velger relasjoner, hops, ttl, maxHits, minScore, revisitPolicy og Interest-condition context | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:242`, `:420` |
| Kant godtas ved abs(edgeWeight−signal.weight)≤tolerance. Bidrag=max(0,1−delta/tolerance), eller eksakt 0/1 ved tolerance≤0. Bidrag multipliseres langs stien | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:475`, `:594`, `:602` |
| Køtraversal, sykluskontroll per sti, Interest-betingelser, implementert visit/hasVisited. never hindrer ny utvidelse, men senere bedre treff kan registreres | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:330`, `:334`, `:465`, `:516` |
| MatchHit: ref, node, score, depth, path, evidence. MatchEvidence: fra/til, relationship, kantvekt, ønsket vekt, toleranse, bidrag, akkumulert score, dybde | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:38`, `:72` |
| MatchResult: token, hits, visitedRefs, accumulatedEvidence, localVariables, elapsedSeconds, expired, maxDepthReached, diagnostics. Diagnostikk teller køarbeid, kanter, filtre, treff og besøk | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:97`, `:149`, `:399` |
| Høyeste score per ref beholdes; lik score favoriserer kort sti, så ref. maxHits avskjærer resultatet etter traversal, ikke arbeidsmengden | `CellProtocol/Sources/CellBase/PurposeAndInterest/WeightedGraphRuntime.swift:314`, `:338`, `:405` |

Weight er **nærhet til ønsket kantvekt**, ikke automatisk relevansstyrke eller
fortegn. Negativ feedback skal ikke ukritisk bli negative kantvekter. For et
ønsket bidrag c∈[0,1] kan en adapter bruke signal.weight=1, tolerance=1,
edgeWeight=c. Tekstaktivering trenger seed-kanter eller ytre sammenslåing av
flere startkjøringer. Collector beholder beste score; den summerer ikke støtte.

MatchStrategyPlanner tar MatchTaskProfile: kandidatantall, aktive interesser,
graf/indeks-tilgjengelighet, forklaringskrav, tvetydighet, latency-budsjett og GPU/
batch-tilgjengelighet. Den gir primary/fallback-estimater, escalationTriggers og
summary; ingen treffliste eller tekstdekomponering. Kilder:
`CellProtocol/Sources/CellBase/PurposeAndInterest/MatchStrategyPlanner.swift:35`,
`:129`, `:150`. ExpectedQuality 0,86/0,92 og 1 000-grensen er konstanter/
heuristikker (`:85`, `:228`, `:285`), **ikke målte kvalitets-/hastighetsgrenser**.

Også læring finnes: RelationalLearningEngine gjør success/failure-forsterkning
med eligibility, journal/replay og decay; scorePurposes summerer effectiveWeight
× eligibility med forklaringer. Kilder:
`CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalLearningEngine.swift:239`,
`:429`, `:629`, og
`CellProtocol/Sources/CellBase/PurposeAndInterest/RelationalDecayPolicy.swift:81`.
PurposeInterestAdjacencyIndex bygger interestRef→kanter og summerer treff:
`CellProtocol/Sources/CellBase/PurposeAndInterest/PurposeInterestAdjacencyIndex.swift:25`,
`:61`. Disse bør gjenbrukes ved integrasjon. Avkrysset relevans er likevel ikke
automatisk et succeeded-purpose-event: en feedbackadapter og en avklart kontrakt
mangler. Python her er et eksperiment, ikke en ny produktmotor.

### Kan 57 + 44 legges rett inn?

**Strukturelt ja, som rå JSON nei.** Book-registeret har purposeRef, parentRef,
title, summary, matchingHints og deklarative mål. Swift Purpose har andre
Codable-felt og goal: CellConfiguration?, se
`CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:20`, `:40`, `:58`.
Basisklassens decoder er tom og encoder skriver bare name:
`CellProtocol/Sources/CellBase/PurposeAndInterest/PerspectiveNode.swift:85`.
Den skal ikke brukes som ferdig registerdecoder.

11 distinkte mål for lærdommenes 59 kanter mangler blant de 57 Book-nodene:
`cell.authorization-honours-keypath`, `cell.contract-explicit`, `cell.no-empty-stubs`,
`cells.capabilities-declared-with-boundary`, `gui.expectation-agreed-before-build`,
`gui.parity-with-approved-image`, `gui.surface-loads-in-time`,
`handoff.runnable-without-guessing`, `quality.build-and-regression`,
`quality.docs-in-same-change`, `quality.work-is-visible` (alle med purpose://).
Alle finnes i de frosne formålspakkene. Eksperimentet inkluderer deres totalt
13 ekstra erklærte noder: **70 formål + 44 lærdommer = 114 noder**, ingen nye refs.
Kilder: `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json:28` og
eksempelpakkenoden i `CellProtocolDocuments/Book/haven_purpose_packages_v0.json:32`.

**FORESLÅTT adapter:** formål→Purpose med stabil purposeRef; lærdom→
EntityRepresentation med stabil lessonRef og egen metadataregistrering;
lesson.purposes→Weight<Purpose>; purpose.entities→inverse Weight<EntityRepresentation>.
EntityRepresentation støtter dette i
`CellProtocol/Sources/CellBase/PurposeAndInterest/EntityRepresentation.swift:79`.
Foreldre kan mappes som types/subTypes etter eksplisitt valg av taksonomisemantikk;
de er ikke med i denne purposeRefs-ablasjonen. Inverse kanter må konstrueres.
Status, mål, severity og provenance må bevares. Swift-adapter, wire-roundtrip og
runtime-paritet: **ukjent/ikke utført**.

## 2. Tekst → signaler

[leksikon.py](../maaling/leksikon.py) bruker formålenes faktiske matchingHints
aliases/tokens, interests, title og summary samt lærdommenes tags, symptom,
cause og prevention. Den beholder overflateformer og stammer→noder. Source,
taskRef og §4 er ikke leksikonfelt. Resultat: **2 734 stammer/tokenverdier,
5 610 teksttoken→node-koblinger**. Unike query-stammer matches med binær IDF-vektet
cosinus; 7/5-tegnsstammingen gjenbruker spiken. Query/tags er ikke slått sammen;
tag-baselinen bruker sine eksisterende oppgaveannotasjoner som før.

Spredning 0,195/0 mot TF-IDFs 0,197/0 ligger nær det gamle 0,20/0. Det beviser
ikke bedre matching: R+@10 er 0,357 mot 0,476; forskjellsintervallet står over.

**Negasjon:** «ikke bruk docker» og «bruk docker» gir samme aktivering av
`lesson.codex-sandbox-cannot-reach-docker` og
`lesson.pkill-pattern-killed-the-queue-job`. STOPP fjerner «ikke»; grafen kan ikke
gjenopprette meningen. Samme Docker-advarsel kan være relevant, men det betyr
ikke at samme handling er tillatt.

**Billigste foreslåtte mottrekk:** behold ikke/aldri/uten; merk negasjon med et
kort verb-/objektvindu som separat constraint og tekstspenn. Et kontrollert
kommandospråk kan bruke `forbiddenAction=docker`. Det trenger ingen AI, men
løser ikke «ikke bare docker», sitater, dobbel negasjon eller lange avhengigheter.
Usikre tilfeller må markeres og avklares. Kuraterte aliaser er billigste hjelp
mot parafraser. Åpen parafrasedekning og full semantisk dekomponering: **ukjent**.
Ingen nytt constraintspråk er implementert her.

## 3. Forplantning: bedre eller bare bredere?

[spredning.py](../maaling/spredning.py) lager begge retninger av de 59 purposeRefs-
kantene. Ingen deploy/rollback-synonymer er lagt til. For 1–3 hopp beregnes
`max(forrige score, nabo × 0,5 × kantvekt)`; startvekt 0,5. Beste sti beholdes.
Sykluser øker ikke score ved bidrag≤1; antall hopp er begrenset. Dette er en
max-product-ablasjon, ikke en full Swift-port: Python kan revurdere bedre ruter
per hopplag; Swift never viderefører ikke nødvendigvis en senere bedre vei.

| Hopp | Bidrag per kant | Jaccard@10, 19 oppgaver | Felles for alle | R+@10 [95 %] | Aktive lærdommer for «deploy» |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,5 × vekt 0,5 | 0.195 | 0 | 0.357 [0.000, 0.750] | 2 |
| 1 | 0,5 × vekt 0,5 | 0.195 | 0 | 0.357 [0.000, 0.750] | 2 |
| 2 | 0,5 × vekt 0,5 | 0.195 | 0 | 0.357 [0.000, 0.750] | 22 |
| 3 | 0,5 × vekt 0,5 | 0.195 | 0 | 0.357 [0.000, 0.750] | 22 |


For de 19 lange §0-queryene er topp-10 **identisk** før/etter forplantning.
For «deploy» går aktiveringen fra 2 til 22 etter to hopp. En faktisk ny sti er
`lesson.codex-sandbox-cannot-reach-docker` → `purpose://quality.build-and-regression`
→ `lesson.local-main-is-not-main`, score 0,012371. 17 lærdommer deler quality-noden.
Dette er en bred kobling. **Korpuset har null rollback-lærdommer** og formålsnodene
har ingen deploy/rollback-aliaser. Deploy→rollback kan ikke måles her; innholdet/
kanten mangler. Det er ikke oppfunnet et treff for å oppfylle eksemplet.

## 4. Ti simulerte hendelser og tre før/etter-eksempler

[laer_vekter.py](../maaling/laer_vekter.py) kjører ti hendelser i fast rundgang:
`PDD_agent-menylinje-og-varsler_2026-09-09` × 3, `PDD_palazzo-husk-det-jeg-sa_2026-09-05` × 3, `PDD_scaffold-admin-delegering_2026-09-08` × 2, `PDD_utviklerbenk-oppgavegraf_2026-09-10` × 2. Det er **fire distinkte oppgaver**, ikke ti uavhengige fasitoppgaver.
Ti forskjellige source-merkede oppgaver finnes ikke her; den delen av forsøket
er **ikke oppfylt**.

Startvekt 0,5. Demping per hendelse: `w ← 0,5 + 0,98 × (w−0,5)`.
Treff: `w ← w + 0,6 × eligibility × (1−w)`.
Bom: `w ← w − 0,3 × eligibility × w`. Vekter holdes i [0,1].
PurposeRefs-eligibility er formålsaktivering normalisert mot sterkeste formål;
tekstkant-eligibility er 1 ved en eksisterende token→lærdom-kobling.
Bare eksisterende koblinger oppdateres. Tid betyr diskrete brukshendelser her;
kalenderhalveringstid er **ukjent**, ikke estimert fra dataene.

- **Bare +:** source-positive forsterkes; uvurderte lærdommer blir aldri bom.
- **+/−, lukket simulert verden:** alle 44 vises, source-positive krysses av,
  resten antas negative **bare i simuleringen**. Dette er ingen menneskefasit.
  Ingen negative dommer er skrevet til originalfasiten. Antakelser og hendelser
  er synlige i råresultatet.

Læring av bare de 59 purposeRefs-kantene endret ingen topp-10. De tre forbedringene
under krever læring også av tekstsignal→lærdom-koblingene, og finnes allerede med
**bare sikre positive**. Gevinsten kan ikke tilskrives formålsgrafen alene.
Parametersettet ble valgt før første pilot; det er ikke søkt over parametere
eller seeds for å tvinge frem tre eksempler. Dette er likevel utviklingsdata.

### PDD_agent-menylinje-og-varsler_2026-09-09

Fasit: 7 source-positive. Her brukes bare positiv feedback; øvrige lærdommer
forblir uvurderte. **Fet skrift i topp-5 betyr kjent positiv.**

| Tilstand | Topp-5 i rekkefølge | Kjente positive i topp-10 | P+@5 | R+@10 | RR+ |
|---|---|---|---:|---:|---:|
| Før | **swift-test-exit-code-lies-in-havenagentd**, **pin-must-be-on-their-main**, `queue-job-file-before-prompt`, **empty-list-must-not-look-like-calm**, `stop-rule-too-wide-stops-the-job` | `swift-test-exit-code-lies-in-havenagentd`, `pin-must-be-on-their-main`, `empty-list-must-not-look-like-calm` | 0.600 | 0.429 | 1.000 |
| Etter ti hendelser | **swift-test-exit-code-lies-in-havenagentd**, **pin-must-be-on-their-main**, **empty-list-must-not-look-like-calm**, `queue-job-file-before-prompt`, **local-main-is-not-main** | `swift-test-exit-code-lies-in-havenagentd`, `pin-must-be-on-their-main`, `empty-list-must-not-look-like-calm`, `local-main-is-not-main`, `pkill-pattern-killed-the-queue-job`, `a-new-red-test-needs-a-repeated-baseline` | 0.800 | 0.857 | 1.000 |

Forsterket signal: `package` → `lesson.local-main-is-not-main`, fra 0,500 til 0.942.
Med den hypotetiske +/−-fasiten blir R+@10 1.000. Dette er
**gjenfinning av en trent oppgave**, ikke en uavhengig effektstudie. Intervallene
for samlet parvis forbedring står over; én oppgave gir ikke et meningsfullt
oppgave-bootstrap-intervall alene.

### PDD_palazzo-husk-det-jeg-sa_2026-09-05

Fasit: 3 source-positive. Her brukes bare positiv feedback; øvrige lærdommer
forblir uvurderte. **Fet skrift i topp-5 betyr kjent positiv.**

| Tilstand | Topp-5 i rekkefølge | Kjente positive i topp-10 | P+@5 | R+@10 | RR+ |
|---|---|---|---:|---:|---:|
| Før | `cellscaffold-two-holes`, `zsh-no-inline-comments`, `test-the-representation-not-the-issuance-flow`, `branch-is-empty-after-eight-work-packages`, `baseline-count-from-report-not-run` | ingen | 0.000 | 0.000 | 0.059 |
| Etter ti hendelser | `cellscaffold-two-holes`, `zsh-no-inline-comments`, **scaffold-without-porthole-host-has-no-preview**, `branch-is-empty-after-eight-work-packages`, `test-the-representation-not-the-issuance-flow` | `scaffold-without-porthole-host-has-no-preview` | 0.200 | 0.333 | 0.333 |

Forsterket signal: `palazzo` → `lesson.scaffold-without-porthole-host-has-no-preview`, fra 0,500 til 0.952.
Med den hypotetiske +/−-fasiten blir R+@10 0.667. Dette er
**gjenfinning av en trent oppgave**, ikke en uavhengig effektstudie. Intervallene
for samlet parvis forbedring står over; én oppgave gir ikke et meningsfullt
oppgave-bootstrap-intervall alene.

### PDD_scaffold-admin-delegering_2026-09-08

Fasit: 4 source-positive. Her brukes bare positiv feedback; øvrige lærdommer
forblir uvurderte. **Fet skrift i topp-5 betyr kjent positiv.**

| Tilstand | Topp-5 i rekkefølge | Kjente positive i topp-10 | P+@5 | R+@10 | RR+ |
|---|---|---|---:|---:|---:|
| Før | `test-the-representation-not-the-issuance-flow`, `entityanchor-keypaths-are-registered`, `cellbase-internal-members-look-public`, `worktree-created-from-vm-has-unusable-gitdir`, `codex-sandbox-cannot-reach-docker` | ingen | 0.000 | 0.000 | 0.067 |
| Etter ti hendelser | `test-the-representation-not-the-issuance-flow`, **baseline-measured-another-pdds-branch**, `queue-job-file-before-prompt`, `empty-list-must-not-look-like-calm`, `entityanchor-keypaths-are-registered` | `baseline-measured-another-pdds-branch`, `branch-is-empty-after-eight-work-packages` | 0.200 | 0.500 | 0.500 |

Forsterket signal: `tillits` → `lesson.baseline-measured-another-pdds-branch`, fra 0,500 til 0.887.
Med den hypotetiske +/−-fasiten blir R+@10 1.000. Dette er
**gjenfinning av en trent oppgave**, ikke en uavhengig effektstudie. Intervallene
for samlet parvis forbedring står over; én oppgave gir ikke et meningsfullt
oppgave-bootstrap-intervall alene.



### Hyppighet og sjeldne blockers

Kontrollene får samme hendelser, feedback, forsterkning og demping. Ren hyppighet
rangerer uten query. Den sterkere kontrollen multipliserer ubehandlet leksikalsk
grafscore med én global lært vekt per lærdom. Begge måles i tabellen; den sterke
kontrollen får også samme holdout-folds. Lærte tekstkanter oppfører seg annerledes
enn global popularitet, men materialet etablerer ikke at forskjellen gir robust
nytte. At popularitetskontrollen svikter, beviser ikke at grafen slår TF-IDF.

Ingen av de 15 source-positive lærdommene er blocker. **Source-basert dekning
for sjeldne blockers er ukjent.** En separat diagnose bruker hver blockers egen
forebygging som query: en lett gjenfinningsprobe, ingen uavhengig relevansfasit.

| Blocker, query = egen forebygging | Før rang | Etter +/− rang | Ren hyppighet rang |
|---|---:|---:|---:|
| `lesson.surface-load-alias-miss` | 1 | 1 | 34 |
| `lesson.cellscaffold-two-holes` | 1 | 1 | 20 |
| `lesson.purpose-never-grants-rights` | 1 | 1 | 33 |
| `lesson.unresolvable-condition-is-invisible` | 1 | 1 | 41 |
| `lesson.ciphertext-field-held-plaintext-hash` | 1 | 1 | 21 |


En separat **syntetisk** sjeldenhetsprøve gir `lesson.surface-load-alias-miss` én positiv
hendelse og deretter ni source-baserte hendelser. Ved gjenbesøk: opprinnelig
rang 1, lærte tekstkanter rang 1, ren hyppighet
rang 16, leksikon×hyppighet rang 2,
blocker-vern rang 1. Blockerens syntetiske relevans blandes
aldri inn i source-tabellen.

Et billig **separat visningsvern** hindrer at en blocker som var i topp-5 før
læring, faller ut av topp-5. Det er målt som egen kandidat med samme k og fasit.
Severity er frosset korpusmetadata, bare brukt i vernet; den er ingen source-dom.
Regelen redder ikke en blocker som aldri aktiveres leksikalsk, og garanterer ikke
semantisk relevans. Rangbevaringen er kontrollert for alle 19 queryene.

## 5. Hastighet, kompleksitet og indeksgrense

Prosessrapport: `macOS-26.5.1-x86_64-i386-64bit-Mach-O`, Python `3.13.5`.
Veggtid med perf_counter, 30 kjøringer per varm batch; ingen modell/nett.
Timing er ikke bootstrap for relevans. Bakgrunnslast kan påvirke tallene.

| Variant, alle 19 queryer, ferdig leksikon | Median ms | p95 ms | Maks ms |
|---|---:|---:|---:|
| leksikon | 6.11 | 6.30 | 6.42 |
| graf1 | 6.56 | 6.79 | 6.96 |
| graf2 | 6.79 | 6.99 | 7.14 |
| graf3 | 6.91 | 7.02 | 10.15 |
| laert | 7.50 | 7.59 | 7.65 |
| laert_med_blockervern | 13.80 | 13.96 | 14.07 |
| bm25 | 5.50 | 5.58 | 5.73 |

Bygg én gang + alle 19 queryer: median 13.45 ms,
p95 19.85 ms, maks 20.95 ms (20 kjøringer).
Ti feedback-hendelser, inkludert før/etter-oppslag: median
19.85 ms, maks 21.91 ms.
Bygg for hver av de 19 queryene: median 120.72 ms,
**over 100 ms**. En separat 12-gangers subprocess-måling av
`leksikon.py 'ikke bruk docker'`, med Python-oppstart og JSON-generering, ga
median 77.18 ms, maks 88.52 ms.
Hele statistikk-/skaleringsjobben tok 52.7 s.
Tolkes «alt under 100 ms» også om bootstrap-jobben, er det **ikke oppfylt**.
Servering, engangsinitialisering og ti feedback-hendelser holder grensen her.


Enkle indekser er allerede i bruk: token→noder og leksikalske poster, pluss kantliste.
Med fast querylengde, dokumentlengde, H≤3 og k er serving-arbeidet
`O(tokens + berørte poster + H·E + N log k)`: lineært i korpusstørrelsen når antall
kanter per node er begrenset. Full rangering for MRR sorterer O(N log N); det er
ikke serveringsveien. Tett graf med E≈N² er ikke lineær i N. Leksikonbygging er
proporsjonal med tekstmengden ved begrenset tekstlengde; voksende dokumenter
krever også mer tokenarbeid.

Skalering: kopier av lærdommene med nye refs, samme 70 formål og 59×faktor kantpar.
Lengste query, 14 632 tegn, tre hopp, topp-10; syv målinger per størrelse.
Dette er en stressprøve med tette tekstposter, **ikke et nytt relevanskorpus**.

| Lærdommer | Noder | Rettede kanter | Bygg ms | Query median ms | Query p95 ms |
|---:|---:|---:|---:|---:|---:|
| 44 | 114 | 118 | 5.78 | 0.89 | 0.97 |
| 440 | 510 | 1180 | 33.82 | 2.79 | 2.82 |
| 4400 | 4470 | 11800 | 301.82 | 21.76 | 24.97 |
| 22000 | 22070 | 59000 | 1545.95 | 108.81 | 144.32 |


Målt <100 ms ved 4 400 lærdommer og >100 ms ved 22 000. Nøyaktig overgang er
**ukjent, mellom de målte punktene**. «Ingen indeks før X» er feil formulert:
tokenindeks brukes allerede. Før denne grensen må kandidater avgrenses og kanter
hentes fra aktive noder; eksisterende PurposeInterestAdjacencyIndex er et
gjenbrukspunkt. Plannerens konstante 1 000-grense er ingen målt produksjonsgrense.

## Reproduksjon og åpne begrensninger

Fra HAVEN-roten:

```sh
python3 CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/leksikon.py 'ikke bruk docker'
python3 CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/spredning.py deploy
python3 CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling/laer_vekter.py --out /tmp/graf-resultater.json
python3 -m unittest discover -s CellProtocolDocuments/Deliverables/PDD_formaalsregister-som-graf_2026-09-11/maaling -p test_evaluer.py
```

Den siste kommandoen ga **20 tester bestått**. Nye målrettede invariantkontroller
passerer: unike refs, full/topp-k-ekvivalens, bare eksisterende kanter oppdatert,
vekter i [0,1], uvurdert ikke negativ, fire holdout-modeller, negasjonsbegrensning
og blocker-bevaring. Leksikonets query-JSON er identisk med PYTHONHASHSEED=1 og 2.
Swift er bare lest.

`evaluer.load_matcher` + `evaluate` er også kjørt med de eksterne adapterne for
leksikon, ett hopp og BM25 samt original TF-IDF. Alle 76 rangeringer samsvarer
med sluttresultatet. Denne adapterkontrollen brukte 100 bootstrap-uttrekk;
rapportens primærintervaller bruker 10 000.

[graf_resultater.json](../maaling/graf_resultater.json) inneholder alle rangeringer,
per-oppgave-mål, intervaller, parvise tester, hendelser, purposeRefs-vekter, seed,
input-/kodehasher og timing. Book-registeret leses fra sin eksisterende fil;
hash lagres i resultatet. Endres den, er en ny kjøring en ny måling selv om
44-kohorten er frosset. Pilot ble fulgt av 10 000-bootstrap-runder;
visningsvernet og deterministisk summering ble kontrollert og rettet før sluttkjøringen.
Ingen kandidat ble utelatt fordi den tapte.

§0 er ikke et rent historisk førstegangsutsagn: noen tekster inneholder senere
auditnotater, og fem queryer har eksplisitte lesson-referanser. Harnessen
tilfører ikke source/§4 til matcheren, men slike ord kan finnes i §0. Ingen av
source-lærdommene er sikkert tilgjengelig før oppgaven oppsto, jf. teststrategiens
datofilter. Dette er **retrospektiv gjenfinning**, ikke bevis på forebygde feil.
Det som mangler for nyttekravet, er fremtidige menneskedommer, ti distinkte
oppgaver med positive og negative, reelle blocker-hendelser og en tilgjengelig
embedding-baseline. Sann presisjon, generell parafrasedekning, fremtidig
nytte og Swift-ytelse er fortsatt **ukjent**.

Metodekilder kontrollert på nett 2026-09-12: BM25 bruker log(N/df), k1=1,2,
b=0,75 og binære query-termer etter
[Stanford IR, Okapi BM25](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html).
Fast-k presisjon og makrosnitt følger
[Stanford IR, Evaluation of ranked retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html).
Intervallberegningen følger den felles lokale evaluatorens kode. Nettkildene
validerer ikke relevansen i HAVEN-korpuset.
