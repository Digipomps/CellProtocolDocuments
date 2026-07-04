# Gemma 4 Local Runtime Test Log

Date: 2026-06-12

Status: Gemma 4 E2B/E4B are available for the next local HAVEN tests through
MLX/VLM QAT runtimes on Kjetil's MacBook Pro M5. The earlier CPU-only
conclusion was a Codex sandbox limitation, not a laptop limitation.

## Purpose

The purpose is to find a practical local model toolbox for HAVEN Co-pilot and
conference helper work:

- understand normal Norwegian everyday speech;
- support useful conference tasks, not just benchmark prompts;
- keep private or credentialed work inside HAVEN-controlled boundaries;
- use the actual M5/Apple Silicon hardware instead of treating the laptop as a
  slow CPU box;
- decide what belongs in the toolbox for the next test round.

## Source Models

- `google/gemma-4-E2B-it`
- `google/gemma-4-E4B-it`
- `mlx-community/gemma-4-E2B-it-qat-4bit`
- `mlx-community/gemma-4-E4B-it-qat-4bit`

Official model cards describe the Gemma 4 E2B/E4B models as Apache-2.0
instruction-tuned small models with 128K context and text/image/audio input
support. The practical local runtime that worked on this laptop is the
MLX/VLM QAT 4-bit variant, not the full safetensors CPU path.

Source links:

- <https://huggingface.co/google/gemma-4-E2B-it>
- <https://huggingface.co/google/gemma-4-E4B-it>
- <https://huggingface.co/mlx-community/gemma-4-E2B-it-qat-4bit>
- <https://huggingface.co/mlx-community/gemma-4-E4B-it-qat-4bit>

## Local Model Inventory

Working Gemma 4 models now kept on disk:

| Model | Local path | Size | Status |
| --- | --- | ---: | --- |
| `Gemma 4 E2B QAT MLX/VLM` | `Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E2B-it-qat-4bit` | 4.1 GiB | Available and benchmarked. |
| `Gemma 4 E4B QAT MLX/VLM` | `Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit` | 6.4 GiB | Available, benchmarked, best Gemma result so far. |

Removed after testing:

- full `google/gemma-4-E4B-it` safetensors, because E4B CPU generation was not
  practical and the QAT MLX/VLM runtime worked;
- full `google/gemma-4-E2B-it` safetensors, because the QAT MLX/VLM runtime is
  the version we want for M5 tests;
- broken or incompatible non-QAT MLX conversions that generated unusable text.

## Disk Cleanup

Cleanup performed during the Gemma setup:

- removed old Hugging Face cache entries for previous large model downloads;
- removed failed x86_64/Rosetta Gemma virtualenv;
- created an arm64 Python 3.11 virtualenv under
  `Artifacts/gemma4-runtime/venv-arm64`;
- purged pip cache, freeing about 867 MB;
- ran `brew cleanup -s`, freeing about 314 MB;
- removed broken/unavailable Ollama model storage containing `mistral:latest`,
  freeing about 3.8 GiB;
- removed full Gemma 4 safetensors after MLX/QAT variants were verified.
- removed old `/private/tmp` DerivedData/verification folders;
- removed Git garbage temp pack/object files that `git count-objects` reported
  as 81.49 GiB of garbage. This did not remove tracked working-tree files.

Current disk snapshot after cleanup:

- `Artifacts/gemma4-runtime`: about 12 GiB.
- `Artifacts/local-models`: about 10 GiB.
- `.git`: about 34 GiB after garbage cleanup.
- Disk free at last check: about 83 GiB.

## Runtime Setup

The working Python runtime is:

`Artifacts/gemma4-runtime/venv-arm64`

Installed runtime packages include:

- `torch 2.12.0`
- `transformers 5.11.0`
- `accelerate 1.14.0`
- `mlx 0.31.2`
- `mlx-lm 0.31.3`
- `mlx-vlm 0.6.3`

Runtime caveat:

- PyTorch MPS and MLX/Metal were not available inside the normal sandboxed
  Codex process.
- MLX/Metal worked from an unsandboxed local process.
- Therefore the right production-shaped path is a supervised local process,
  preferably through HAVENAgentD, not ad-hoc CPU execution from Codex.

## OpenAI-Compatible Local Server Test

Gemma 4 E4B QAT was started with:

```bash
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/venv-arm64/bin/python \
  -m mlx_vlm.server \
  --host 127.0.0.1 \
  --port 8094 \
  --model /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit \
  --max-tokens 256 \
  --log-level INFO
```

Verified:

- `/v1/models` responded on `http://127.0.0.1:8094`.
- `/v1/chat/completions` responded to a Norwegian one-sentence conference
  helper prompt.
- This server expects the local model path as the `model` value unless the
  caller uses exactly an id that the server can resolve. HAVENAgentD should
  hide that detail behind a stable local provider id.

Example response to:

`Hva bør jeg få med meg nå hvis jeg liker lokal AI og personvern?`

The model answered:

`Du bør se etter AI-løsninger som er lokalt hostet og som tilbyr full kontroll over dine data.`

## Benchmark Adapter

MLX/VLM benchmark runner:

`Tools/CoPilotChatLanguageBenchmark/run_mlx_vlm_cases.py`

Transformers/safetensors runner kept for reference:

`Tools/CoPilotChatLanguageBenchmark/run_gemma4_cases.py`

Both use the same Norwegian Co-pilot benchmark cases and scoring contract as
the GGUF runner.

## Representative 8-Case Results

| Model | Runtime | Score | Parse errors | Latency notes |
| --- | --- | ---: | ---: | --- |
| `Qwen3-8B-Q4_K_M` | GGUF/llama-cli | `38/48` (`79.2%`) | 0 | Best current local text-only score. |
| `Gemma 4 E4B QAT` | MLX/VLM | `36/48` (`75.0%`) | 0 | Roughly 8-11 seconds per case; best Gemma result. |
| `Gemma 4 E2B full` | Transformers CPU | `34/48` (`70.8%`) | 0 | 55-97 seconds per case; removed after QAT path worked. |
| `Gemma 4 E2B QAT` | MLX/VLM | `32/48` (`66.7%`) | 0 | Roughly 9-11 seconds per case. |
| `Qwen3-4B-Q4_K_M` | GGUF/llama-cli | `31/48` (`64.6%`) | 0 | Smaller comparison model. |

Gemma 4 E4B QAT dimension score:

- intent: `7/8` (`87.5%`)
- action: `8/8` (`100.0%`)
- clarification: `5/8` (`62.5%`)
- safety: `4/8` (`50.0%`)
- must mention: `4/8` (`50.0%`)
- must not mention: `8/8` (`100.0%`)

Gemma 4 E2B QAT dimension score:

- intent: `6/8` (`75.0%`)
- action: `5/8` (`62.5%`)
- clarification: `5/8` (`62.5%`)
- safety: `5/8` (`62.5%`)
- must mention: `4/8` (`50.0%`)
- must not mention: `7/8` (`87.5%`)

## Interpretation

Gemma 4 E4B QAT should be in the next toolbox as the primary Gemma candidate:

- it runs on Apple Silicon through MLX/VLM;
- it is close to the current Qwen3-8B text-only baseline;
- it gives us a path toward multimodal conference work: screenshots, posters,
  slides and audio snippets;
- it is practical enough for supervised local experiments.

Qwen3-8B remains the best tested local text-only benchmark result. Gemma 4 E4B
QAT is the better strategic candidate where multimodal input, M5 acceleration
and longer context matter.

## HAVENAgentD Recommendation

Use HAVENAgentD as the local model boundary:

- AgentD starts or supervises `mlx_vlm.server` on loopback.
- Co-pilot/Binding/Porthole call AgentD, not the raw model server directly.
- AgentD maps a stable provider id such as
  `local.gemma4.e4b.qat.mlx-vlm` to the local path.
- AgentD owns credentials and authenticated web-fetch cells.
- Model prompts/results must not contain raw credentials.
- Deterministic policy and action validation stay outside the model.

Gemma should phrase, summarize, classify and draft inside a bounded contract.
It should not be the policy authority for sponsor data, private contact data,
publishing, deletion or schedule mutation.

## Next Tests

1. Run the full 40-case Norwegian daily-speech benchmark through a persistent
   Gemma 4 E4B QAT server.
2. Add multimodal conference cases:
   screenshots, poster/slide summaries, simple audio snippets and UI QA.
3. Wire a HAVENAgentD local provider profile and run the same benchmark through
   the AgentD boundary, not just a standalone runner.
4. Keep Qwen3-8B as the text-only comparison baseline.
