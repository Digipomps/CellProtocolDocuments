# Chapter 26 — Model Knowledge and Purpose Matching

Status: draft operational strategy.

Last updated: 2026-06-18.

This chapter defines how HAVEN should collect enough model metadata to choose
models for a task without turning model choice into guesswork or hidden global
provider preference.

The short version:

1. Collect facts from provider APIs, model cards, pricing pages, legal/DPA
   notes, and local benchmark runs.
2. Normalize those facts into a model/provider catalog.
3. Map models to HAVEN purpose profiles.
4. Filter by data class, Agreement, credential policy, modality, hardware,
   cost, provider/GDPR status and model license.
5. Rank the remaining candidates by measured fit, not generic leaderboard
   glamour.

Seed catalog:

`Book/model_provider_catalog_v0.json`

Operational seed tooling:

`Tools/ModelKnowledge/`

This folder builds a dedicated model-knowledge corpus, queries it with a
lightweight lexical scorer, fetches OpenAI-compatible provider model lists, and
runs synthetic provider smoke tests. It is intentionally secret-free. Until
`SecretCredentialCell` exists in AgentD, provider scripts may use process-local
environment variables for credentials, but keys must never be written to files,
prompts, benchmark outputs, docs, logs or Git.

## 1. Why Purpose Matching

HAVEN should not ask "what is the best model?"

It should ask:

What is the safest and most capable available model for this purpose, data
class, scaffold, hardware boundary, cost limit and consent state?

That matters because:

- a great hosted frontier model may be wrong for private entity data;
- a local model may be right for privacy but too weak for a specific visible
  task;
- a cheap aggregator may be excellent for synthetic model discovery but wrong
  for sponsor leads;
- a multimodal model may be overkill for text routing but essential for
  screenshot/audio tasks.

## 2. Metadata Sources

Collect from these layers:

| Source | What to collect | Trust level |
| --- | --- | --- |
| Provider `/models` API | model ids, availability, context, route ids when exposed | operational, but incomplete |
| Provider pricing page/API | per-token cost, subscription tier, concurrency, markup, pinned-route cost | must be date-stamped |
| Provider privacy/DPA docs | logging, retention, subprocessors, region, DPA availability | claims until reviewed |
| Hugging Face model card/API | license, modality, context, model family, intended use, limitations | good source for open-weight candidates |
| Local benchmark results | quality, latency, memory, schema validity, failure modes | strongest HAVEN-specific signal |
| Runtime probe | tokens/sec, peak memory, supported quantizations, hardware backend | required before local default |
| Manual legal review | GDPR/DPA status, model license acceptance, commercial-use caveats | required for sensitive data |

Every record needs `sourceCheckedAt`.

## 3. Required Model Fields

Each model record should include:

- `modelID`
- `providerID`
- `family`
- `route`: local, hosted, aggregator, embedding, reranker, PII preflight
- `modalities`
- `contextWindow`
- `license`
- `commercialUseStatus`
- `providerPrivacyStatus`
- `dpaStatus`
- `dataResidency`
- `pricing`
- `hardwareRequirements`
- `runtimeCompatibility`
- `testedHardware`
- `benchmarkResults`
- `strengths`
- `weaknesses`
- `allowedDataClasses`
- `blockedDataClasses`
- `purposeFit`
- `sourceURLs`
- `sourceCheckedAt`

## 4. Purpose Profiles

Purpose profiles describe jobs HAVEN actually has, not generic model categories.

Initial profiles:

| Purpose profile | Purpose ref | Primary constraints |
| --- | --- | --- |
| Local private draft | `purpose://personal.ai.private-draft` | local/on-device preferred, no external provider unless explicitly approved |
| Conference participant guidance | `purpose://conference.co-pilot.participant-guidance` | Norwegian quality, low hallucination, agenda/policy grounding |
| Conference model evaluation | `purpose://conference.co-pilot.model-evaluation` | synthetic/public prompts only, broad provider/model access allowed |
| Multimodal conference QA | `purpose://conference.co-pilot.multimodal-qa` | image/audio support, explicit user selection, PII caution |
| Book/docs RAG answer | `purpose://docs.rag.answer-with-citations` | citations, embedding/reranking, source paths |
| RAG prompt adaptation | `purpose://model.prompt-adaptation` | target-model prompt shape, source manifest, no retrieval or provider invocation |
| Code/protocol reasoning | `purpose://developer.protocol-code-reasoning` | long context, code quality, private repo minimization |
| PII/safety preflight | `purpose://privacy.pii-preflight` | local preferred, false-negative minimization |
| Provider discovery | `purpose://model.provider-discovery` | public/synthetic, pricing/model metadata capture |

Purpose refs should be promoted into the purpose knowledge base when their
product semantics stabilize.

## 5. Matching Pipeline

### Step 1: classify request

Extract:

- purpose ref;
- scaffold id;
- data class;
- modality;
- expected output type;
- context length;
- latency need;
- user approval state;
- local hardware availability;
- budget/spend cap.

### Step 2: hard filters

Remove candidates when:

- modality is unsupported;
- context is too short;
- license blocks the use;
- provider DPA/GDPR status is insufficient for the data class;
- credential policy denies the purpose/scaffold;
- hardware cannot run the local model;
- requested external route lacks explicit approval;
- model is marked unavailable or failed in last health probe.

### Step 3: rank remaining candidates

Suggested ranking weights:

```json
{
  "quality": 0.35,
  "privacyLocality": 0.25,
  "taskSpecificBenchmark": 0.2,
  "latency": 0.1,
  "cost": 0.05,
  "operationalStability": 0.05
}
```

For security-sensitive flows, `privacyLocality`, `DPA` and `allowedDataClass`
are hard gates, not soft weights.

### Step 4: produce route decision

Return:

- selected provider/model;
- why it matched;
- why higher-ranked-looking models were rejected;
- required credential;
- required Agreement/capability;
- prompt retention class;
- fallback route.

## 6. Data Classes

Initial data classes:

- `synthetic`
- `public`
- `internal_non_sensitive`
- `private_profile`
- `private_contact_info`
- `private_notes`
- `sponsor_leads_with_consent`
- `sponsor_leads_without_consent`
- `payment`
- `health`
- `children`
- `credential_secret`

`credential_secret` must never be sent to a model.

## 7. Current Seed Mapping

| Model/provider | Good purpose fit | Avoid |
| --- | --- | --- |
| Local `Qwen3-8B-Q4_K_M` | text-only Norwegian Co-pilot baseline, participant guidance drafts | policy/action authority |
| Local `Gemma 4 E4B QAT MLX/VLM` | M5-local multimodal conference QA, screenshots, posters, audio snippets, private local fallback | sponsor-consent authority |
| `BAAI/bge-m3` | Book/docs RAG, agenda/policy retrieval | generation |
| `BAAI/bge-reranker-v2-m3` | rerank RAG candidates for citations | standalone answer generation |
| `urchade/gliner_multi_pii-v1` | PII/safety preflight | proof of compliance |
| Featherless | open-weight model discovery before local download | private data before DPA/legal review |
| NanoGPT | broad model/media/TEE-route discovery with synthetic prompts | private data before route-specific review |

## 8. Metadata Harvest Jobs

Create repeatable jobs:

1. `provider.models.fetch`: read provider model list/API where available.
2. `provider.pricing.fetch`: snapshot pricing plan/cost metadata.
3. `provider.privacy.fetch`: snapshot privacy/logging/DPA/source URLs.
4. `hf.modelcard.fetch`: snapshot model card metadata for open candidates.
5. `local.runtime.probe`: record hardware/runtime/token speed/memory.
6. `benchmark.run`: run HAVEN benchmark suites.
7. `catalog.merge`: update catalog with source timestamp and provenance.
8. `purpose.fit.score`: compute purpose fit from benchmark and policy gates.

For provider APIs that require credentials, these jobs must use
`SecretCredentialCell`/AgentD secret refs, not environment variables checked
into scripts or prompt text.

`SecretCredentialCell` here means the shared AI-provider credential policy
surface over the existing credential primitives: `ScopedCredentialCell` for
explicit UI/session use, `CredentialVaultService` + `SecureCredentialStore` for
durable secret handles, and Keychain/scoped secret providers for raw secret
material.

Current seed commands live in `Tools/ModelKnowledge/README.md`:

- `build_model_knowledge_corpus.py` builds
  `Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl` from the
  curated source manifest.
- `query_model_knowledge.py` gives agents a local query entrypoint before the
  final embedding/reranker pipeline is wired.
- `fetch_provider_models.py` snapshots provider `/models` metadata for
  NanoGPT and Featherless.
- `summarize_provider_models.py` filters large provider model snapshots into a
  small purpose-oriented candidate summary for RAG and review.
- `smoke_openai_compatible.py` runs a synthetic OpenAI-compatible chat
  completion check and stores hashes, usage and a bounded preview, not API
  keys.

## 9. Benchmark Packs

Minimum benchmark packs:

- Norwegian Co-pilot daily speech;
- sponsor/privacy refusal;
- agenda/policy grounded answer with citations;
- skeleton/config JSON validity;
- code/protocol reasoning;
- multimodal screenshot/poster QA;
- PII detection false-negative suite;
- latency/memory/runtime probe.

Every benchmark output should record:

- model id;
- provider id;
- credential route, not raw credential;
- data class;
- prompt manifest hash;
- result hash;
- timestamp;
- source corpus refs;
- score dimensions;
- notable failures.

## 10. Result Shape

Model matching should return a structured result:

```json
{
  "status": "matched",
  "purposeRef": "purpose://conference.co-pilot.participant-guidance",
  "selected": {
    "providerID": "haven-local-m5",
    "modelID": "Qwen3-8B-Q4_K_M",
    "route": "local-gguf"
  },
  "reasons": [
    "best measured local text score",
    "data class allowed locally",
    "no external DPA required"
  ],
  "rejected": [
    {
      "modelID": "hosted-frontier-example",
      "reason": "external route not approved for private profile data"
    }
  ],
  "requiredCapability": "credential.use.none-local",
  "promptRetentionClass": "hash_only",
  "fallback": {
    "providerID": "haven-local-m5",
    "modelID": "Gemma 4 E4B QAT MLX/VLM"
  }
}
```

## 11. Implementation Target

First implementation should live as a model-routing service/cell near
HAVENAgentD and the Co-pilot benchmark tooling:

- it can read `Book/model_provider_catalog_v0.json`;
- it can call `SecretCredentialCell` for provider availability;
- it can run benchmark packs;
- it can emit FlowElements describing route decisions.
- it can hand the selected route/model profile to `RAGPromptTransformerCell`
  when a RAG source package needs model-specific prompt formatting.

Later, stable model descriptors can be promoted into shared CellProtocol
metadata if multiple scaffolds need to evaluate them offline.
