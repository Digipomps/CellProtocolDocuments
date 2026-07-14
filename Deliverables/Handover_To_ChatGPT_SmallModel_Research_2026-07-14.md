# Handover til ChatGPT (desktop/Codex): småmodell-formålsdekomponering + E3b

Dato: 2026-07-14. Fra: Claude-økt (tom for ukeskvote). Repo:
`~/Build/Digipomps/HAVEN/CellProtocolDocuments`, branch `main` (pushet).
Til: ChatGPT desktop med Codex, modell `gpt-5.6-sol`.

## Din oppgave

Fortsett forskningen på å heve småmodellers formålsdekomponering (Apple
Intelligence + små modeller generelt). Alt under er ferdig og committet unntatt
E3b, som er blokkert. Les full kontekst i:

- `Deliverables/Small_Model_Purpose_Decomposition_Research_2026-07-11.md` (hoved-leveranse, E1–E4 + arkitektur)
- `Deliverables/Codex_Handoff_E3b_Norwegian_LoRA_Adapter_2026-07-13.md` (E3b-spesifikasjon)
- `Deliverables/e3b_coreai_torch_provenance_2026-07-14.md` (hvorfor coreai-torch var feil pakke)

## Status på eksperimentserien (alt committet på main)

- **E1** (shortlist): deterministisk post-prosessering er største spak (+25–34 pp); hele pipelinen løfter ministral-3b 5,4 %→53,6 %, over naiv Qwen-8B. Arkitektur > modellstørrelse.
- **E2** (mikro-oppgaver): per-kandidat JA/NEI løser underseleksjon (seleksjon-kun 96–100 %), men overselekterer (81 % JA) → korrupt LCA. Fiks: LCA fra sikker kjerne (topp-2 resolver-score).
- **E2b** (JA-kalibrering): self-consistency (NanoGPT gir ikke logprobs). ministral +5 pp holdt-ut (t\*=0,65); Qwen no-op.
- **E3** (Apple on-device, EKTE kjøring): `@Generable` guided generation, norsk prompt mot engelske kandidater. Null formatfeil; seleksjon-kun 96 %; med resolver-score-gate **85 % holdt-ut test** — over alle API-småmodeller. Harness: `Tools/PurposeKnowledge/e3_apple_microtask.swift`.
- **E4** (kaskade): tier-2 kjørt både Qwen og ekte frontier gpt-5.5. **Ingen sterkere lane finnes** — gpt-5.5 = 60 % strict, likt Apple, under ministral. Kaskade betaler seg ikke; restgapet er deterministisk LCA under over-/underseleksjon, ikke modellkapasitet.

**Rigg gjenbrukes:** `Tools/PurposeKnowledge/` (`purpose_resolver.mjs`, `score_model_outputs.mjs`, `run_e*_*.mjs`, `fixtures/purpose_eval_cases.v0.jsonl` = fasit, 56 caser). NanoGPT-nøkkel: `security find-generic-password -a nanogpt -s com.digipomps.cellscaffold.aigateway -w` (aldri i fil). Train/test-splitt overalt: case-indeks `% 5 >= 3` = test.

## E3b — blokkert, trenger din beslutning + handling

E3b = norsk rank-32 LoRA-adapter for Apples on-device-modell. **Step 0 bestått**: adapter-lasting ER eksponert i Swift (`Adapter`, `Adapter.compile()`, `SystemLanguageModel(adapter:)`; probe `Tools/PurposeKnowledge/e3b_adapter_probe.swift`). Blokkering: det ekte Apple-toolkitet (v26.0.0) er **Account-Holder-gated** (godta toolkit-vilkår) + EOL på macOS 27+. `coreai-torch` var feil pakke (Core AI IR-konverter, ikke adapter-trening).

**Tre veier — velg med Kjetil:**
1. **Skaff Apple-toolkitet**: Account Holder for Digipomps godtar vilkårene på `developer.apple.com/apple-intelligence/foundation-models-adapter/#download-toolkit`, laster v26.0.0 til `~/Downloads`. Så: venv under `Tools/PurposeKnowledge/e3b_adapter/` (gitignore), SMOKE-før-skala (liten norsk treningssett fra `Book/haven_purpose_knowledge_base_v0.json`, engelske kandidater, få steg, last throwaway-adapter, kjør harness på noen caser, bekreft score), så full rank-32, så score på holdt-ut test. Manifest må logge eksakt basismodell-versjon. Baseline å slå: 85 % gated.
2. **Pivot til norsk lokal modell** (anbefalt av Claude): test samme hypotese med NbAiLab Llama-3.2 3B / NorMistral via NanoGPT-runneren — ingen gating, kjørbar nå.
3. **Legg E3b på is**: bruk kreftene på det deterministiske seleksjon/LCA-leddet (der E4 peker restgapet).

**Regler:** skriv kun nye `e3b_*`-filer; secret-fritt; ikke commit venv/vekter/toolkit; hold test-splitten ute av trening; negativt resultat er gyldig — rapportér ærlig.

## Separat spor (fra ChatGPT, ikke tapt)

ChatGPT meldte: «M0d er resolved, og M1+ er avblokkert. Bruk `origin/codex/admin-scaffold-m4` på `3180f23`.» Dette er admin-scaffold-milepæler — eget spor, ikke del av småmodell-forskningen. Fortsett det etter din egen kontekst; notert her så det ikke går tapt.

## Anbefalt neste steg

Start med å avklare E3b-veien med Kjetil (anbefaling: vei 2), og — uavhengig av E3b — angrip det deterministiske seleksjon/LCA-leddet, som E4 identifiserte som det egentlige restgapet (constrained multi-select / bedre nearestSharedPurposeRef-utledning), siden det løfter ALLE modell-lag inkludert Apples on-device 85 %.
