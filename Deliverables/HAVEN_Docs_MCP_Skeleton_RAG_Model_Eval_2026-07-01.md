# HAVEN Docs MCP Skeleton RAG Model Eval

Date: 2026-07-01

## Kort konklusjon

Ja, read-only HAVEN Docs MCP er verdt aa stoette videre. Testen viser at
modellene kan gi gode, repo-groundede forklaringer naar de faar riktige
dokumentasjonsutdrag, men at kvaliteten avhenger sterkt av promptform,
tokenbudsjett, citation-krav og runtime-boundary.

Beste svar i siste runde var `qwen3-8b-q4` og `gemma4-e2b-qat-mlx`.
Manuelt vurdert er `qwen3-8b-q4` best som ferdig, kompakt forklaring, mens
`gemma4-e2b-qat-mlx` er naer og har bedre faktiske kildehenvisninger, men en
liten terminologisk glipp. `qwen3-1.7b-q8` er beste raske lokale kandidat:
mye kvalitet per sekund, men svakere kildehenvisninger.

## Ground Truth

Ground truth ble hentet gjennom den lokale HAVEN Docs MCP-indeksen, ikke fra
modellens egen hukommelse. Brukte seksjoner:

- `Book/12_Skeleton_Spec.md:1-853`
- `Book/12_Skeleton_Spec.md:37-59`
- `Book/12_Skeleton_Spec.md:823-845`
- `Book/22_Explore_Contracts_For_Skeleton_Authoring.md:165-221`
- `Book/22_Explore_Contracts_For_Skeleton_Authoring.md:251-336`

Eval-harness og raaresultater:

- `Tools/HavenDocsMCP/evaluate_skeleton_answer_models.py`
- `Tools/HavenDocsMCP/results/skeleton_answer_model_eval_2026-07-01.json`

Hosted API-modeller ble ikke testet i denne runtime-en fordi disse miljovariablene
ikke var eksponert: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `NANOGPT_API_KEY`,
`MISTRAL_API_KEY`, `FEATHERLESS_API_KEY`.

## Metode

Prompten ba modellene forklare hvordan CellProtocol Skeleton virker, kun basert
paa ground truth. Siste eval-runde brukte en stram struktur: seks nummererte
punkter, maks omtrent 550 ord, og minst en henvisning til `Book/12` og `Book/22`.

Heuristikken scoret 18 poeng:

- citations
- encoding/model
- CellConfiguration/default endpoint/cellReferences
- keypath/url og get/set-bindinger
- Explore-validering
- owner/entity access
- caveats/limits
- norsk/lesbarhet
- hallucination control

Jeg gjorde ogsaa manuell vurdering, fordi heuristikken ikke fullt ut skiller
mellom korrekte line citations, grove dokumentnavn, rare oversettelser og god
forklaringskvalitet.

## Resultater

| Modell | Runtime | Tid | Heuristikk | Manuell vurdering |
| --- | --- | ---: | ---: | --- |
| `qwen3-8b-q4` | GGUF / `llama-cli` / Metal | 57.5s | 18/18 | Beste kompakte forklaring. Dekker alle krav, men kildehenvisningene er mer dokumentnavn enn presise linjer. |
| `gemma4-e2b-qat-mlx` | MLX/VLM | 26.7s | 18/18 | Svart godt og med line citations. Nesten best, men skrev "selskaps-entiteter", som er en liten semantisk glipp. |
| `qwen3-1.7b-q8` | GGUF / `llama-cli` / Metal | 15.9s | 16/18 | Raskest og overraskende god. Mangler kildehenvisninger og blander litt engelsk/norsk. God som lokal draft/routing-kandidat. |
| `qwen3-4b-q4` | GGUF / `llama-cli` / Metal | 31.8s | 14/18 | Grei dekning, men svakere spraak og noen rare formuleringer som "enkel-knapp objekt". Ikke tydelig bedre enn 1.7B. |
| `gemma4-e4b-qat-mlx` | MLX/VLM | 66.1s | 14/18 | God struktur og citations, men svakere paa CellConfiguration/cellReferences og bindesemantikk enn E2B. Ikke beste valg for denne oppgaven. |

## Runtime-funn

Normal sandbox var ikke nok for lokal modellkjøring:

- Qwen via `llama-cli` med Metal feilet i sandbox med rask prosessfeil.
- Gemma via `mlx_vlm.generate` feilet i sandbox under MLX-import/compile.
- Samme eval fungerte usandboxet.

Det matcher tidligere HAVEN-observasjon: lokale Metal/MLX-modeller boer kjores
via en kontrollert lokal prosess, helst HAVENAgentD eller tilsvarende supervised
runtime, ikke direkte fra en trang agent-sandbox.

Promptform betydde mye:

- Bred prompt gav for lange og delvis avkuttede svar.
- Stram prompt med seks punkter gav bedre og raskere svar.
- `qwen3-8b-q4` gikk fra middels til beste resultat etter promptstramming.

## Anbefaling

1. Stott HAVEN Docs MCP videre som read-only oppslag for agenter og modeller.
2. Hold modelltilpasset promptpakking i RAG-laget eller i
   `RAGPromptTransformerCell`, ikke i MCP-adapteren. MCP-prompts skal bare
   vaere statiske lesestier for klienter som stotter MCP prompts.
3. La transformer-cellen lage "forklar fra docs"-promptpakker med fast struktur,
   ordgrense, "bare ground truth", eksplisitt citation-krav og prompt manifest.
4. Ha en post-check som validerer at svaret faktisk nevner paakrevde kilder,
   owner/entity access og Explore-validering.
5. Bruk `qwen3-8b-q4` eller `gemma4-e2b-qat-mlx` for kvalitetskontroll av
   docs/RAG-svar; bruk `qwen3-1.7b-q8` som rask lokal kandidat naar latency er
   viktigere enn perfekte citations.
6. Ikke presenter hosted modellkvalitet som testet foer runtime faktisk har
   noekler/ruter tilgjengelig.

Kort sagt: MCP-en gjor dette enklere for språknodeller ved aa gi trygg lookup.
RAG og `RAGPromptTransformerCell` bor levere kildepakker, model-adapted prompts,
citations og en enkel answer-quality check slik at modellen ikke bare skriver
pent, men faktisk holder seg til HAVEN-dokumentasjonen.
