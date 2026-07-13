# Småmodell-kvalitet for formålsdekomponering: forskningsdypdykk og arkitektur

Dato: 2026-07-11. Status: forskningsgjennomgang med anbefalt arkitektur og
eksperimentplan. Kildene er datert 2024–2026; modell-/rammeverksfakta bør
refreshes før produksjonsvalg (jf. Book 24-regelen).

Spørsmål: hvordan får vi mindre kapable modeller — Apple Intelligence
on-device spesielt, småmodeller generelt — til å dekomponere tekst til formål
(purpose://-noder + Goals) med høy kvalitet? Hypotesen var at en form for
pre-parsing trengs. **Forskningen bekrefter hypotesen, og skjerper den.**

## 1. Hovedfunnet: formålsdekomponering er klassifisering, ikke generering

Det mest beslutningsrelevante funnet kommer fra «Let Me Speak Freely?»
(EMNLP Industry 2024, arxiv 2408.02442): formatrestriksjoner **skader**
resonneringstunge oppgaver, men **hjelper** klassifiseringsoppgaver — eksplisitt
inkludert *intent detection* og *slot-filling*. Formålsdekomponering mot en
lukket taksonomi ER intent detection + slot-filling. Konsekvens:

- For småmodeller skal formålsdekomponering **omformuleres fra åpen generering
  til valg blant kandidater**: den deterministiske pipelinen i Book 23 §6
  (alias-hashmaps, token-invertert indeks, LCA) produserer topp-K kandidater;
  småmodellen VELGER og binder slots — den genererer aldri purposeRefs fritt.
- Oppfunnede refs (hallusinasjonsgate-brudd) blir da *strukturelt umulige*,
  ikke bare policy-forbudt.

## 2. Constrained decoding: størst løft nederst i kapabilitetsskalaen

- Grammar-constrained decoding (GCD) garanterer at output følger en formell
  grammatikk ved token-maskering (Geng et al., arxiv 2305.13971; oversikt
  arxiv 2501.10868, 2502.05111).
- NVIDIAs Bash-studie: constrained retry løftet snitt-pass-rate 62,5 % → 75,2 %
  over 13 modeller, med størst enkeltgevinst på **Qwen3-0.6B, som endte nær
  modeller dobbelt så store**. Klinisk IE-litteratur (PMC11747381) finner at
  små/finetunede modeller i lavressurs-settinger tjener klart mest på GCD.
- Nyansen fra §1 gjelder: GCD på *svar-innholdet* i resonneringsoppgaver kan
  skade. Løsningen i litteraturen er **to-pass** («NL-to-Format», og «Thinking
  Before Constraining», arxiv 2601.07525): fri tenkning først, så konvertering
  under grammatikk. For ren kandidat-klassifisering er én-pass constrained OK.

## 3. Dekomponert prompting: mikro-oppgaver i pipeline

DECOMP-litteraturen (Khot et al., «Decomposed Prompting») viser at komplekse
oppgaver blir traktable for svakere modeller når de splittes i tett avgrensede
deloppgaver med egne, målrettede eksempler — og at deloppgaver kan rutes til
*ulike* handlere (deterministisk kode, klassifiserere, LLM-er). Vår egen
regime-test (2026-07-11) fant det samme empirisk: mellomsjiktmodeller (8B)
tjente mest på kritisk-spørsmål-stillas (+1,0 på 9-punkts gullsett), og
bestemte mikro-spørsmål ble levert 3/3 med stillas mot 0–1/3 uten.

For formålsdekomponering betyr det én modellkall-form per beslutning:
«gjelder kandidat X for denne teksten? (ja/nei/usikker)», «hvilket av disse 5
Goal-mønstrene passer?», «bind metric/target fra dette sitatet» — aldri
«dekomponer denne teksten» som én stor oppgave.

## 4. Kaskade med kalibrert eskalering

Cascade-/routing-litteraturen (survey arxiv 2603.04445; UCCI arxiv 2605.18796;
ICLR 2025-resultat: 85 % kostnadskutt med 95 % av GPT-4-Turbo-kvalitet ved å
sende 14 % av spørringene til stor modell) er samstemt: **strukturert
ekstraksjon er paradeoppgaven for småmodell-først** — og eskalering skal styres
av kalibrert usikkerhet, ikke magefølelse. Vår 5-lags modellstige (Book 24/27
§3) er allerede denne arkitekturen; det som mangler er usikkerhetssignalet
(logprob/selv-rapportert konfidens kalibrert mot fasit på purpose-casene) og
eskaleringsterskler satt på valideringssett.

## 5. Apple Intelligence spesifikt

Fra Apples tech report (arxiv 2507.13575) og 2025-oppdateringen
(machinelearning.apple.com):

- **~3B on-device-modell**, kontekst opp til 65K tokens, eksponert via
  FoundationModels-rammeverket i Swift — gratis, offline, ingen API-nøkkel.
- **Guided generation = innebygd constrained decoding**: `@Generable`/`@Guide`
  Swift-makroer tvinger output inn i Swift-typer på token-nivå (kombinert med
  spekulativ dekoding). Dette er *nøyaktig* mekanismen fra §2, levert som
  plattformfunksjon — og CellProtocol er Swift. En
  `@Generable enum PurposeCandidate` over topp-K-kandidatene gjør oppfunnede
  refs umulige på Apple-flaten.
- **Tool calling** håndteres automatisk (parallelle/serielle kallgrafer) —
  purpose.knowledge.resolve/purpose.context.pack kan eksponeres som tools.
- **Adapter-toolkit**: Python-toolkit for rank-32 LoRA-adaptere + valgfri
  draft-modell. Viktig driftskaveat: **adaptere må retrenes for hver ny
  basismodellversjon.**
- **Begrensninger**: modellen er eksplisitt *ikke* ment som
  verdenskunnskap-chatbot — den er god på entity extraction, summarization,
  tekstforståelse over *medsendt kontekst*. Det passer vårt bruk (dekomponere
  medsendt tekst mot medsendt kandidatliste) perfekt.
- **Norsk er IKKE blant de 15 støttede språkene.** Tre mitigeringer, i
  anbefalt rekkefølge: (a) deterministisk norsk pre-parse + presentér
  kandidater/mikro-spørsmål på engelsk (pre-parsen er språkuavhengig kode);
  (b) tren LoRA-adapter på norske dekomponerings-par — prompt-matrisene og
  purpose-casene våre er ferdige treningsdata; (c) bruk norsk-tunede små
  alternativer i samme lane: NbAiLab Llama-3.2 1B/3B (norsk-optimalisert),
  Borealis (Gemma-basert, åpne lisenser), NorMistral-11B-thinking (LTG/UiO,
  des. 2025) — kjørbare via MLX/llama.cpp i HavenAgentD som Gemma4 allerede er.

## 6. Anbefalt arkitektur: pre-parse → shortlist → velg → verifiser → eskaler

1. **Deterministisk pre-parse** (utvid Book 23 §6 + text_reliability-mønsteret):
   normalisering, segmentering med sitat-ankere, cue-ekstraksjon, topp-K
   purpose-kandidater fra indeksen, relevante Goal-/keypath-hint via
   `purpose.context.pack`. Ingen modell involvert.
2. **Mikro-oppgaver** (DECOMP): én beslutning per kall, med kandidatene og
   ankrede sitater som hele konteksten.
3. **Constrained output**: `@Generable`-enum på Apple; GCD-grammatikk
   (Outlines/XGrammar/llguidance) på andre lokale modeller. To-pass kun der
   deloppgaven krever resonnering.
4. **Deterministisk verifisering**: ref finnes i taksonomien, Goal er testbar,
   skjema validerer (gjenbruk `evaluate_purpose_cases.mjs`-harnesset).
5. **Kalibrert eskalering**: usikre/lavkonfidens-tilfeller til sterkere lane
   per dataklasse-policy (Book 24); `purpose://prompt.unknown` + candidate
   intake forblir fallback, aldri gjetting.

## 7. Eksperimentplan (falsifiserbar, gjenbruker eksisterende harness)

- **E1 (shortlist-effekten)**: CoPilot-prompt-matrisen kjørt mot småmodeller i
  to armer — rå tekst→dekomponer vs. pre-parse→velg-blant-K. Prediksjon fra
  §1–§3: stor gevinst; mål mot dagens 50–79 %-bånd.

### E1: KJØRT 2026-07-12 — resultat

Rigg: `Tools/PurposeKnowledge/run_e1_shortlist_experiment.mjs` (NanoGPT), 56
purpose-caser × 2 modeller × 2 armer = 224 kall, 0 parse-feil, shortlist
pipeline-recall 100 %. 2×2-design: armene (full taksonomi vs. topp-8-shortlist
fra deterministisk resolver) × visning (rå modelloutput vs. deterministisk
post-prosessering: verifiser refs → expandCoverage → utled goals/LCA). Scoret
med `score_model_outputs.mjs` mot fasit.

| Celle | Rå | Post-prosessert |
| --- | ---: | ---: |
| ministral-3b, full taksonomi | 5,4 % | 39,3 % |
| ministral-3b, shortlist | 14,3 % | **53,6 %** |
| Qwen3-8B, full taksonomi | 16,1 % | 51,8 % |
| Qwen3-8B, shortlist | 26,8 % | 51,8 % |

Funn:

1. **Deterministisk post-prosessering er den største enkeltspaken** (+25 til
   +34 pp i alle celler): modellenes semantiske utvalg er langt bedre enn
   bokføringen deres (goalRefs, LCA, facet-ekspansjon) — la maskinen bokføre.
2. **Shortlist-effekten er størst for den svakeste modellen**: +14,3 pp for 3B
   i post-visning (39,3→53,6), ~0 for 8B — samme omvendte-U/regime-mønster som
   Walton-testen. Rått dobler shortlisten pass-raten for begge.
3. **Hele pipelinen løfter 3B fra ubrukelig til bedre enn naiv 8B**: 5,4 % →
   53,6 % (10×); 8B: 16,1 % → 51,8 % (3,2×). Arkitektur slår modellstørrelse.
4. **Restfeilene er semantisk under-seleksjon** («smallest sufficient set»
   tolkes som «færrest mulig»; manglende must-include-refs drar også LCA feil)
   — nøyaktig det E2/mikro-oppgave-dekomponering (én ja/nei per kandidat) og
   constrained multi-select predikerer å fikse.

Ærlig kontekst: den deterministiske resolveren alene passerer 100 % på dette
fikstursettet (de er samutviklet), så på *disse* casene tilfører modellen
ingenting over deterministikken. E1 måler modellatferden når den først er i
løkka — det som overføres til input indeksen ikke løser. Rådata:
`Tools/PurposeKnowledge/results/e1_*_20260712T193912Z.*` + `e1_score_{raw,post}.json`.
- **E2 (constrained-effekten)**: samme, ± GCD/guided generation. Prediksjon:
  ugyldig-output-raten → ~0, kvalitetsgevinst størst for minste modeller.

### E2: KJØRT 2026-07-13 — mikro-oppgave-dekomponering

Rigg: `Tools/PurposeKnowledge/run_e2_microtask_experiment.mjs`. I stedet for ett
multi-valg-kall får modellen **ett JA/NEI/USIKKER-spørsmål per shortlist-kandidat**
(«krever brukerens forespørsel dette formålet?»), og settet settes sammen
deterministisk. 306 mikro-kall, 0 uparsede. To sammensettingspolicyer scoret fra
samme kall (strict = kun JA; lenient = JA+USIKKER); begge gjennom samme
post-prosessering som E1.

| Konfig | ministral-3b | Qwen3-8B |
| --- | ---: | ---: |
| E1 shortlist (multi-valg) | 48 % | 46 % |
| E2 mikro, naiv LCA | 38 % | 48 % |
| **E2 mikro + deterministisk LCA-kjerne** | **54 %** | **57 %** |
| E2 mikro, KUN seleksjon (ignorer LCA) | **100 %** | 90 % |

Funn (samme 50 caser der begge har data):

1. **Mikro-oppgaver LØSER underseleksjonen fra E1 — fullstendig.** Scorer man
   kun purpose-utvalget (ignorer det avledede LCA-feltet), går ministral fra
   56 % (E1) til **100 %**, Qwen fra 60 % til 90 %. Alle 31 ministral-feilene i
   full scoring var *ren* LCA — utvalget var korrekt i hver eneste feilende case.
   E1-prediksjonen bekreftet på seleksjonsnivå.
2. **Men naiv per-kandidat-JA overselekterer.** JA-rate 81 %; snitt valgt 2,92
   (ministral) mot fasit 1,84 og E1s 1,28. I isolasjon ser nesten hver kandidat
   «påkrevd» ut. Overseleksjonen skader *bare* det avledede
   nearestSharedPurposeRef (LCA trekkes grunt når kryss-gren-refs blir med), så
   naiv strict-score faller for den svake modellen (48→38).
3. **Feilen er i kode-laget, ikke modellen.** Å utlede LCA fra den *sikre
   kjernen* (topp-2 JA-refs etter deterministisk resolver-score, mens hele
   JA-settet beholdes som purpose-sett via expandCoverage) løfter til 54 %/57 %
   — over E1 for begge modeller (+6 pp / +11 pp). Rescore:
   `Tools/PurposeKnowledge/rescore_e2_lca_core.mjs`, ingen nye kall.
4. **Vinnende pipeline: shortlist → per-kandidat mikro-valg → deterministisk
   sammensetting med LCA på sikker kjerne.** Modellen er ikke lenger
   seleksjons-flaskehalsen; restfeilen er JA-kalibrering + LCA-derivasjon, begge
   deterministiske. USIKKER var sjelden (9/306), så strict≈lenient.

Rådata: `Tools/PurposeKnowledge/results/e2_*_20260713T055001Z.*`,
`e2_score.json`, `e2_score_lcafix.json`.

### E2b: KJØRT 2026-07-13 — kalibrer JA-terskelen

Mål: kutte overseleksjonen fra E2 ved å akseptere JA kun over en
konfidensterskel. NanoGPT eksponerer **ikke** token-logprobs, så konfidens
estimeres provider-agnostisk med **self-consistency**: hvert kandidat-spørsmål
samples 5× ved temp 0,8, P(JES) = JA-andel. Terskel sweepet 0→0,90 på 60 %
train-splitt, rapportert på holdt-ut 40 % test.
Rigg: `run_e2b_yes_calibration.mjs` + `score_e2b_threshold.mjs`. 1530 samples,
0 feil.

| Modell | t\* | Test naiv | Test kalibrert | Alle naiv | Alle kalibrert |
| --- | ---: | ---: | ---: | ---: | ---: |
| ministral-3b | 0,65 | 55 % | **60 %** | 54 % | 58 % |
| Qwen3-8B | 0,00 | 55 % | 55 % | 54 % | 54 % |

Funn:

1. **Kalibrering gir modest, reell gevinst for den svake modellen** (+5 pp
   holdt-ut, +4 pp totalt) ved å kutte de ~13 sub-enstemmige JA-ene. Platået er
   robust: train flat 53,3 % opp til t=0,60, så flat 56,7 % fra 0,65–0,90.
2. **No-op for den sterke modellen.** t\*=0 for Qwen: JA-fordelingen er bimodal
   (51 rene NEI, 102 rene JA), ingenting å terskle.
3. **Metodens tak: konsistent-men-feil overseleksjon.** ministral ga
   *enstemmig* JA på 135/153 kandidater — self-consistency kan ikke fange en
   modell som er trygt overinkluderende. Å gå lenger krever et bedre
   konfidenssignal (logprobs/ekstern verifiser) eller constrained decoding som
   demper JA-biasen ved kilden — begge peker mot E3 (Apple guided generation).

Konsolidert beste konfig per modell:
ministral 48 % (E1) → 54 % (E2) → **58 %** (E2b); Qwen 46 % → **57 %** (E2, uendret
av kalibrering). Regime-mønsteret holder: jo svakere modell, jo mer hjelper hvert
deterministisk/kalibrerings-lag. Rådata:
`Tools/PurposeKnowledge/results/e2b_*_20260713T134155Z.*`, `e2b_threshold_report.json`.
- **E3 (Apple-adapter)**: base ~3B med engelsk mikro-oppgave-innpakning vs.
  LoRA-adapter trent på norske dekomponerings-par. Måles på purpose-casene.

### E3: KJØRT 2026-07-13 — Apple on-device 3B, guided generation, norsk input

Ekte on-device-kjøring: macOS 26.5.1, Apple Silicon, FoundationModels-rammeverket,
`SystemLanguageModel.default` = available. Rigg: `e3_apple_microtask.swift`
(+ `gen_e3_input.mjs`, `assemble_e3_answers.mjs`). Samme mikro-oppgave som E2
(per-kandidat verdict), men med **`@Generable enum {yes,no,unsure}`** =
constrained decoding, og **norsk prompt mot engelske kandidatbeskrivelser**
(taksonomien er engelsk; norsk er IKKE blant Apples 15 støttede språk — dette
tester mitigering (a)). 153 kandidater, 46 s (3,3/s), fersk session per kandidat.

Funn:

1. **Null formatfeil.** Guided generation garanterer gyldig enum — ingen
   parse-feil mulig, mot API-modellenes behov for robust JSON-ekstraksjon.
   Dette er guided generations kjerneverdi, levert som plattformfunksjon.
2. **Norsk fungerer for klassifisering-over-engelske-kandidater.**
   Seleksjon-kun-score (ignorer avledet LCA) = **96 %** — nær-perfekt
   formålsutvalg på offisielt ustøttet språk. Mitigeringen (norsk brukertekst +
   engelske kandidater + constrained output) holder.
3. **Overselekterer mest av alle** (87 % JA, 133/20/0) — norsk gjør 3B-modellen
   ekstra permissiv — så naiv strict er 52 % (test 60 %).
4. **Deterministisk resolver-score-gate er kraftig.** Med gate valgt på train
   (score ≥ 8) er **holdt-ut test 85 %** (naiv 60 %). Single-shot Apple har ikke
   self-consistency-signal, så resolver-scoren er kalibreringsspaken — og den er
   svært effektiv fordi shortlist-ranken allerede bærer mye signal.

Konsolidert, holdt-ut der relevant: **Apple 3B i full pipeline = 85 %**, over
ministral 58 % (E2b) og Qwen 57 % (E2). Den minste, gratis, offline modellen
vinner når arkitekturen bærer den — hovedtesen bekreftet, og guided generation
fjerner formatproblemet helt. Rådata:
`Tools/PurposeKnowledge/results/e3_*`.

Neste (E4): kalibrert kaskade-terskel — la den deterministiske gaten + modell-
usikkerhet avgjøre hvilke caser som eskaleres til sterkere lane. Ikke kjørt.
Ekte LoRA-adapter (norske par) gjenstår som separat E3b.
- **E4 (kaskade-terskel)**: kalibrér konfidens på valideringssett; mål
  eskaleringsrate og totalkvalitet mot hosted-alene.

### E4: KJØRT 2026-07-13 — kalibrert kaskade betaler seg ikke

Rigg: `run_e4_cascade.mjs`. To kaskader på strict-metrikk (recall-komplett +
LCA-kjerne-match, den metrikken der overseleksjon straffes), holdt-ut test-
splitt som E3, terskel valgt på train. Tier-2 kjørt både som Qwen3-8B og som
ekte frontier-lane **gpt-5.5** (153 nye mikro-kall; gpt-5.5 JA-rate 55 % vs
Apple 87 %/ministral 81 % — langt mindre overselekterende).

| Kaskade | tier1 alene | tier2 alene | kaskade (test) | oracle |
| --- | ---: | ---: | ---: | ---: |
| A: Apple(gratis)→Qwen | 60 % | 55 % | 70 % @ 60 % esk. | 70 % |
| A: Apple(gratis)→**gpt-5.5** | 60 % | 60 % | 70 % @ **75 %** esk. | 75 % |
| B: ministral(billig)→Qwen | 65 % | 55 % | 65 % @ 0 % (degenerert) | 70 % |
| B: ministral(billig)→**gpt-5.5** | 65 % | 60 % | 65 % @ 5 % esk. | 75 % |

Funn:

1. **Det finnes ingen sterkere lane å eskalere til.** Frontier-modellen
   gpt-5.5 scorer **60 %** strict — likt Apple, *under* ministral (65 %).
   gpt-5.5 bytter bare overseleksjon mot underseleksjon (55 % JA → mister
   påkrevde formål). Modellkapasitet er ikke flaskehalsen.
2. **Kaskaden degenererer eller koster for mye.** B er en no-op (billig lane
   slår tier-2, terskel holder alt på tier-1). A når oracle, men bare ved å
   eskalere 60–75 % av casene — som eliminerer kostnadsgevinsten kaskaden
   fantes for.
3. **Restgapet er ikke modell, men deterministisk LCA-derivasjon under over-/
   underseleksjon.** Oracle 75 % viser reell komplementaritet, men ingen lane
   (gratis, billig eller frontier) passerer 65 % alene. Spaken er å fikse
   seleksjon→LCA ved kilden (constrained multi-select, bedre LCA-utledning),
   ikke å betale for en sterkere modell.

Dette lukker serien: **E1 viste arkitektur > modellstørrelse; E4 viser at selv en
frontier-modell ikke slår den gratis on-device-pipelinen.** Produktkonsekvens:
kjør alt på Apples on-device 3B i pipelinen; ikke bygg kaskade for denne
oppgaven; invester i det deterministiske seleksjon/LCA-leddet. Rådata:
`Tools/PurposeKnowledge/results/e4_cascade_report_*.json`.

Gjenstår: E3b (norsk LoRA-adapter) er delegert til Codex
(`Deliverables/Codex_Handoff_E3b_Norwegian_LoRA_Adapter_2026-07-13.md`) — kan
lukke deler av restgapet ved å dempe overseleksjon i modell-leddet.
- Rigg: NanoGPT-runneren for API-modeller; HavenAgentD/MLX for lokale;
  gullsett = purpose-casene + regime-test-metodikken (sitat-forankret scoring).

## 8. Kilder

- Let Me Speak Freely? (format vs. oppgavetype): arxiv.org/abs/2408.02442
- Thinking Before Constraining (to-pass): arxiv.org/abs/2601.07525
- GCD uten finetuning: arxiv.org/abs/2305.13971; benchmark arxiv.org/abs/2501.10868;
  effektiv GCD arxiv.org/abs/2502.05111
- NVIDIA GCD/Bash-småmodellstudie: developer.nvidia.com/blog/improving-bash-generation-in-small-language-models-with-grammar-constrained-decoding/
- Klinisk IE + GCD (småmodeller tjener mest): pmc.ncbi.nlm.nih.gov/articles/PMC11747381/
- Decomposed Prompting: semanticscholar.org (Khot et al., DecomP)
- Kaskade/ruting: arxiv.org/abs/2603.04445 (survey); arxiv.org/abs/2605.18796 (UCCI)
- Apple: arxiv.org/abs/2507.13575 (tech report 2025);
  machinelearning.apple.com/research/apple-foundation-models-2025-updates;
  developer.apple.com/apple-intelligence/foundation-models-adapter/
- Norske småmodeller: ai.nb.no/models/ (NbAiLab Llama 3.2 1B/3B, Borealis);
  mn.uio.no LTG (NorMistral-11B-thinking); arxiv.org/abs/2412.06484
  (kontinuerlig trening for norsk)
