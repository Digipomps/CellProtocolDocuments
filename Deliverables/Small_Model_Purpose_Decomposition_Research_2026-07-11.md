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
- **E2 (constrained-effekten)**: samme, ± GCD/guided generation. Prediksjon:
  ugyldig-output-raten → ~0, kvalitetsgevinst størst for minste modeller.
- **E3 (Apple-adapter)**: base ~3B med engelsk mikro-oppgave-innpakning vs.
  LoRA-adapter trent på norske dekomponerings-par. Måles på purpose-casene.
- **E4 (kaskade-terskel)**: kalibrér konfidens på valideringssett; mål
  eskaleringsrate og totalkvalitet mot hosted-alene.
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
