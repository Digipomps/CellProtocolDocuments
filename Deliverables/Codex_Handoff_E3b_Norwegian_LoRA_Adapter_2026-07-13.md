# Codex-handoff: E3b — norsk LoRA-adapter for Apple on-device Foundation Model

Til: Codex (ChatGPT-appen). Anbefalt modell: GPT-5.6 (høy reasoning).
Fra: Claude-økt 2026-07-13. Status: klar til utførelse.

## Objective

Tren en rank-32 LoRA-adapter for Apples on-device Foundation Model som hever
norsk formålsdekomponering, og mål gevinsten mot den adapterløse baselinen fra
E3. Hypotese: adapteren lukker overselektjons-gapet (E3: 87 % JA-rate, naiv
strict 52 %) og løfter norsk ytelse ut over dagens engelsk-innpakning.

## Current state (verifisert på denne maskinen)

- macOS 26.5.1, Apple Silicon, Swift 6.2.4. `import FoundationModels` fungerer;
  `SystemLanguageModel.default.availability == .available`; `@Generable`
  guided generation kjører (bekreftet E3).
- E3 (adapterløs baseline) er ferdig og committet:
  - Harness: `Tools/PurposeKnowledge/e3_apple_microtask.swift` (per-kandidat
    `@Generable enum {yes,no,unsure}` mikro-oppgave, norsk prompt mot engelske
    kandidatbeskrivelser).
  - Input-generator: `Tools/PurposeKnowledge/gen_e3_input.mjs` →
    `results/e3_input.json` (56 caser, 153 kandidater).
  - Sammensetting/scoring: `Tools/PurposeKnowledge/assemble_e3_answers.mjs` +
    `Tools/PurposeKnowledge/score_model_outputs.mjs`.
  - Baseline-tall: seleksjon-kun 96 %; naiv strict 52 %; med deterministisk
    resolver-score-gate (train-valgt ≥8) holdt-ut test 85 %. Full analyse:
    `Deliverables/Small_Model_Purpose_Decomposition_Research_2026-07-11.md`.
- Fasit: `Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl` (56
  caser med `expected.mustIncludePurposeRefs`). Deterministisk resolver:
  `Tools/PurposeKnowledge/purpose_resolver.mjs` (100 % på fikstursettet — den
  er sannhet for shortlist/verifisering; adapteren skal forbedre modell-leddet).

## Oppgaver

1. **Skaff Apples adapter-treningstoolkit.** Python-toolkit for rank-32 LoRA
   (+ valgfri draft-modell for spekulativ dekoding). Se
   `developer.apple.com/apple-intelligence/foundation-models-adapter/`.
   Installer i et isolert venv under `Tools/PurposeKnowledge/e3b_adapter/`
   (IKKE i repo-roten; legg venv i .gitignore). NB fra E3-research:
   **adaptere må retrenes for hver ny basismodellversjon** — logg basismodell-
   versjonen i et manifest.
2. **Bygg norske treningspar.** Kilder som allerede finnes i repoet:
   - `Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl` (norske
     prompts + fasit-refs) — MEN: ikke tren på hele settet. **Hold ut samme
     ~40 % test-splitt** som E3-scoringen bruker (case-indeks i % 5 >= 3 =
     test) så E3b-tallet er sammenlignbart og ikke overtilpasset.
   - CoPilot-prompt-matrisene og purpose-KB-en (`Book/haven_purpose_knowledge_base_v0.json`)
     for å generere flere norske (prompt → korrekt kandidat-verdict) par
     syntetisk. Behold engelske kandidatbeskrivelser (mitigering (a)).
   - Format: følg toolkitets forventede treningsformat (typisk JSONL med
     instruction/målformat). Målet er samme mikro-oppgave som E3: per kandidat,
     yes/no/unsure, men nå med adapteren som demper norsk overselektjon.
3. **Tren adapteren** (rank 32). Logg hyperparametre, steg, tap, og tid.
4. **Kjør E3-harnesset på nytt med adapteren lastet.** Utvid
   `e3_apple_microtask.swift` (eller lag `e3b_apple_microtask.swift`) til å
   laste adapteren via `SystemLanguageModel(adapter:)`/tilsvarende API. Skriv
   svar til `results/e3b_apple_answers.jsonl` i SAMME format som E3.
5. **Score** med `assemble_e3_answers.mjs` (pek den på e3b-svarene) +
   `score_model_outputs.mjs`, og rapportér på **holdt-ut test-splitten**:
   seleksjon-kun, naiv strict, og gated (samme train/test-protokoll som E3).

## Constraints / non-goals

- Secret-fritt: ingen nøkler i filer. Norsk/syntetisk treningsdata er
  `synthetic`/`public` dataklasse — OK for lokal trening.
- Ikke rør eksisterende E1–E3-resultatfiler; skriv kun nye `e3b_*`.
- Ikke commit venv, modellvekter eller nedlastede toolkit-binærer (.gitignore).
  Commit: harness-endring, treningsskript, treningsdata-generator, adapter-
  manifest (hyperparametre + basismodellversjon + metرikk), og resultat-JSON.
- Behold determinisme i scoring-leddet; adapteren er den eneste nye variabelen.
- Hold train/test-splitten identisk med E3 (% 5 >= 3 = test) — ellers er
  sammenligningen ugyldig.

## Verification expected

- E3b-tall rapportert på **samme holdt-ut test-caser** som E3 (85 % gated er
  baselinen å slå).
- Manifest med basismodellversjon, rank, treningssteg, og par-antall.
- Ærlig konklusjon: løftet adapteren norsk ytelse, og lukket den overselektjons-
  gapet, eller ikke? Negativt resultat er et gyldig resultat.

## Open questions

- Eksponerer det nåværende FoundationModels-API-et adapter-lasting fra Swift på
  denne macOS-versjonen (26.5.1), eller kreves et spesifikt SDK/entitlement?
  Verifiser før trening; hvis adapter-lasting ikke er tilgjengelig fra Swift-
  runtime her, dokumentér blokkeringen og stopp etter treningssteget.
- Er 56 caser (minus test-hold-out) nok signal for en rank-32-adapter, eller
  bør syntetiske par fra KB-en dominere treningssettet? Anbefaling: syntetiske
  par dominerer, fikstur-train brukes til validering.

## Handoff-status

Claude gjør E4 (kalibrert kaskade-terskel) parallelt i CellProtocolDocuments —
koordinér ved å kun skrive `e3b_*`-filer for å unngå kollisjon.
