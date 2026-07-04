# Hugging Face Local Model Recommendations For HAVEN

Date: 2026-06-11

Status: advisory shortlist. This is not a provider registry and not a
CellProtocol contract.

## Recommendation

Use a small local stack first, then benchmark before wiring anything into
runtime defaults:

1. `BAAI/bge-m3` for multilingual local embeddings.
2. `BAAI/bge-reranker-v2-m3` for local reranking after retrieval.
3. `urchade/gliner_multi_pii-v1` for local PII/entity preflight before any
   external prompt or publish/share action.
4. `Qwen/Qwen3-8B` as the first general local chat / reasoning candidate.
5. `Qwen/Qwen2.5-Coder-7B-Instruct` as the first local coding assistant
   candidate.
6. `google/gemma-4-E2B-it` as the first next-test multimodal candidate for the
   conference toolbox.
7. `google/gemma-4-E4B-it` as the Gemma quality step-up if disk, memory and
   runtime are acceptable.
8. `openai/gpt-oss-20b` as the first heavier local reasoning candidate once
   local memory/latency is verified.

Keep `mistralai/Mistral-Small-3.2-24B-Instruct-2506` as a stronger local or
near-local candidate for a beefier host. Treat `Ministral-8B-Instruct-2410` as
interesting technically, but blocked for default HAVEN use by the Mistral
Research License unless commercial terms are clarified.

## Resource Tiers

### Tier 0: Always-on small local helpers

Use for:

- PII detection
- entity extraction
- purpose / interest candidate extraction
- "should this leave the device?" checks
- RAG embedding and reranking

Candidates:

- `urchade/gliner_multi_pii-v1`
- `BAAI/bge-m3`
- `BAAI/bge-reranker-v2-m3`
- `nomic-ai/modernbert-embed-base` for English-heavy docs or browser-side /
  JS embedding experiments

### Tier 1: Small local generation

Use for:

- draft rewriting
- short summaries
- template matching
- helper-card explanations
- low-risk chat suggestions

Candidates:

- `microsoft/Phi-4-mini-instruct`
- `meta-llama/Llama-3.2-3B-Instruct`
- `google/gemma-4-E2B-it` for next multimodal conference tests
- `google/gemma-4-E4B-it` for quality comparison if the host can run it
- `google/gemma-3n-E4B-it` for multimodal cases

License notes:

- Phi-4 mini is MIT licensed.
- Llama 3.2 uses a custom Llama license and gated access; use only after
  reviewing terms.
- Gemma 4 E2B/E4B model cards list Apache-2.0. Older Gemma 3n candidates may
  still require Gemma-specific access/terms; review the exact model card before
  downloading.

### Tier 2: Local workhorse models

Use for:

- local chat workbench
- JSON drafting for review
- docs summarization
- structured helper-card generation
- lightweight agent planning with no tool execution

Candidates:

- `Qwen/Qwen3-8B`
- `Qwen/Qwen2.5-Coder-7B-Instruct`
- `mistralai/Ministral-8B-Instruct-2410` only if its license is acceptable

### Tier 3: Heavier local reasoning

Use for:

- deeper local analysis
- architecture/design critique
- code review before external escalation
- local planner/executor dry runs

Candidates:

- `openai/gpt-oss-20b`
- `Qwen/Qwen2.5-Coder-14B-Instruct`
- `mistralai/Mistral-Small-3.2-24B-Instruct-2506`

These should not be always-on defaults. Put them behind a visible local
provider choice with resource/cost/latency indicators.

## Model Notes

| Model | License on HF | Why useful for HAVEN | Caution |
| --- | --- | --- | --- |
| `BAAI/bge-m3` | MIT | Multilingual embeddings, dense/sparse/multi-vector retrieval, long-ish docs up to 8192 tokens. Good default for Book/RAG/Vault. | Embeddings over private text are still data processing; keep indexes owner-scoped. |
| `BAAI/bge-reranker-v2-m3` | Apache-2.0 | Multilingual reranker for better RAG precision after initial retrieval. | Cross-encoder reranking costs more than embeddings; use after top-k retrieval. |
| `urchade/gliner_multi_pii-v1` | Apache-2.0 | Local PII preflight for prompts, public profile copy, sponsor lead sharing and external provider escalation. | Trained on synthetic PII data; use as guardrail, not proof of compliance. |
| `Qwen/Qwen3-8B` | Apache-2.0 | Strong 8B general model with thinking/non-thinking modes, multilingual support, tool/agent capability and 32k native context. Good local workhorse. | Need prompt discipline around hidden reasoning; do not store/show thinking content as user-facing truth. |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | Apache-2.0 | Small local coding helper for Swift/JS/Python snippets, tests and contract sketches. | Use for reviewable drafts; not final authority for CellProtocol behavior. |
| `Qwen/Qwen2.5-Coder-14B-Instruct` | Apache-2.0 | Better local coding/reasoning if hardware supports it. | Heavier; benchmark before adoption. |
| `microsoft/Phi-4-mini-instruct` | MIT | 3.8B, 128k context, aimed at constrained/latency-bound environments and reasoning. Good candidate for Binding/local helper. | Requires `trust_remote_code` in HF examples; review serving path carefully. |
| `google/gemma-4-E2B-it` | Apache-2.0 | Priority next-test multimodal candidate: text/image/audio support, 128k context for the small Gemma 4 models, native system prompt support and function calling. Good for conference screenshots, posters/slides, audio snippets and long-context agenda/policy helper tests. | Official path is Transformers/Safetensors; local llama.cpp/GGUF path was not verified in this run. Media inputs may contain PII; require explicit user selection. |
| `google/gemma-4-E4B-it` | Apache-2.0 | Quality step-up for the same multimodal conference tasks if E2B is promising. Model card reports stronger benchmark results than E2B in the Gemma 4 family. | Larger effective parameter count and memory footprint; benchmark before putting it on a laptop default path. |
| `google/gemma-3n-E4B-it` | Gemma | Efficient multimodal local model: text, image, video, audio input, 32k context. Good for screenshots, simple speech/audio extraction and design inspection. | Gated access and Gemma terms; vision/audio inputs may contain PII. |
| `meta-llama/Llama-3.2-3B-Instruct` | Llama 3.2 | Small on-device-ish assistant for retrieval/summarization and mobile writing helpers. | Custom license/gated access; official supported languages do not include Norwegian. |
| `openai/gpt-oss-20b` | Apache-2.0 | Heavier open-weight reasoning, agentic tasks, configurable reasoning effort, function calling/structured outputs; intended to run within 16GB memory in MXFP4. | Requires Harmony format; benchmark carefully on Apple Silicon/Ollama/llama.cpp path before relying on it. |
| `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | Apache-2.0 | Stronger 24B text+vision candidate, improved instruction following and function calling. | Likely a workstation/server model, not small-device default. |
| `mistralai/Ministral-8B-Instruct-2410` | Mistral Research License | Good technical fit for edge/local intelligence and 128k context. | Not a default commercial HAVEN candidate without Mistral commercial license clarity. |
| `nomic-ai/modernbert-embed-base` | Apache-2.0 | Efficient English embedding model, supports 768d and Matryoshka 256d truncation; useful for browser/JS experiments. | Less attractive than BGE-M3 for Norwegian/multilingual default. |

## HAVEN Mapping

### Binding

Default:

- Apple Foundation Models where available
- `Phi-4-mini-instruct` or `Llama-3.2-3B-Instruct` for simple local text helper
- `gemma-4-E2B-it` or `gemma-4-E4B-it` only for explicit screenshot/audio/image
  tasks once tested

Use for:

- private draft rewrite
- intent classification
- helper-card drafts
- pending action explanation

### Porthole / Staging

Default:

- `bge-m3` + `bge-reranker-v2-m3` for local/server RAG
- `Qwen3-8B` for local workbench helper if server capacity exists

Use for:

- Book/docs RAG
- agenda/policy lookup
- visible helper card generation

### CellScaffold Workbench

Default test matrix:

- `gemma-4-E2B-it`
- `gemma-4-E4B-it`
- `Qwen3-8B`
- `Qwen2.5-Coder-7B-Instruct`
- `gpt-oss-20b`
- `bge-m3`
- `bge-reranker-v2-m3`
- `gliner_multi_pii-v1`

Use this scaffold for benchmarking and provider descriptor work before
promoting anything to product scaffolds.

### HAVENAgentD

Candidate local agents:

- `gpt-oss-20b`
- `Qwen2.5-Coder-14B-Instruct`
- `Mistral-Small-3.2-24B-Instruct-2506`

Rules:

- no raw shell from chat
- signed review intents only
- allowlisted tools
- prompt manifest hash + result hash in FlowElement audit

### DiMy / Conference

Default:

- `bge-m3` for domain docs, agenda, public content and policy retrieval
- `bge-reranker-v2-m3` for precision
- `gliner_multi_pii-v1` before sponsor/share/export flows
- `Qwen3-8B` for local concierge draft where host capacity allows

Do not use local LLMs to create sponsor leads from private participant context
without explicit consent and grant.

## First Benchmark Pack

Run each candidate against fixed local prompts before adoption:

1. Norwegian/English Purpose and Interest extraction.
2. PII detection on profile and sponsor-lead examples.
3. Book/RAG answer with citation grounding.
4. Skeleton JSON draft from a simple design brief.
5. Swift/JS code explanation from local source snippets.
6. Conference concierge answer from public agenda only.
7. Refusal / uncertainty when private cell data is missing.

For each run, record:

- model id
- quantization
- runtime (`ollama`, `llama.cpp`, `mlx-lm`, `transformers`, `vllm`)
- memory
- tokens/sec
- context limit
- pass/fail on schema validity
- PII false negatives
- hallucinated keypaths
- license notes

## Sources Checked

- https://huggingface.co/BAAI/bge-m3
- https://huggingface.co/BAAI/bge-reranker-v2-m3
- https://huggingface.co/urchade/gliner_multi_pii-v1
- https://huggingface.co/Qwen/Qwen3-8B
- https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct
- https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct
- https://huggingface.co/microsoft/Phi-4-mini-instruct
- https://huggingface.co/google/gemma-3n-E4B-it
- https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
- https://huggingface.co/openai/gpt-oss-20b
- https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506
- https://huggingface.co/mistralai/Ministral-8B-Instruct-2410
- https://huggingface.co/nomic-ai/modernbert-embed-base
