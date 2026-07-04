# Chapter 28 - RAGPromptTransformerCell

Status: Draft contract and local reference transformer.

Last verified: 2026-07-01

## Purpose

`RAGPromptTransformerCell` turns retrieved source material into a
model-targeted prompt package. It exists so the read-only docs MCP can stay a
lookup adapter, while RAG and CellProtocol cells own answer-preparation logic.

The cell is useful when the same RAG result must be sent to different model
families with different prompt needs:

- compact six-point answers for local Qwen-style instruction models
- citation-heavy answer packs for Gemma-style local VLM models
- stricter quote/source ledgers for source-auditor workflows
- shorter context packs for small local models
- longer context packs for approved frontier routes

## Boundary

Responsibilities:

- accept a RAG source package with canonical source chunks and citations
- accept a target model profile or model route decision
- emit a prompt package tuned for that model family and purpose
- emit a prompt manifest hash for audit and provider invocation
- emit quality checks that downstream agents can run after generation

Non-responsibilities:

- it does not search the corpus
- it does not call the language model
- it does not mutate docs, Vault, Todo, or RAG indexes
- it does not decide whether an external provider is approved for a data class
- it does not hide missing citations or weak retrieval coverage

This means:

- `Tools/HavenDocsMCP` remains a read-only lookup and resource surface.
- RAG owns retrieval, reranking, source coverage, and citation metadata.
- `RAGPromptTransformerCell` owns model-specific prompt packaging.
- Model/provider invocation stays behind the selected provider route,
  `SecretCredentialCell`, or HAVENAgentD.

## Input Shape

Minimum request:

```json
{
  "question": "Forklar hvordan CellProtocol Skeleton virker.",
  "purposeRef": "purpose://docs.rag.answer-with-citations",
  "targetModel": {
    "modelID": "qwen3-8b-q4",
    "providerID": "haven-local-m5",
    "route": "local-gguf",
    "family": "qwen3"
  },
  "answerStyle": {
    "language": "no",
    "format": "six_numbered_points",
    "maxWords": 550
  },
  "rag": {
    "query": "CellProtocol Skeleton keypath Explore owner access",
    "chunks": [
      {
        "path": "Book/12_Skeleton_Spec.md",
        "heading": "1. Encoding Rule (All Elements)",
        "lineStart": 37,
        "lineEnd": 59,
        "text": "Each element is encoded as a single-key object...",
        "score": 18.2
      }
    ],
    "coverageWarnings": []
  },
  "constraints": {
    "dataClass": "internal_non_sensitive",
    "mustCover": [
      "single-key JSON encoding",
      "Explore validation",
      "owner/entity access"
    ],
    "forbiddenClaims": [
      "unsupported Skeleton element types",
      "provider credentials",
      "uncited implementation claims"
    ]
  }
}
```

## Output Shape

Minimum response:

```json
{
  "status": "ready",
  "promptPackageVersion": 1,
  "targetModel": {
    "modelID": "qwen3-8b-q4",
    "family": "qwen3"
  },
  "systemPrompt": "Du er en HAVEN dokumentasjonsassistent...",
  "userPrompt": "GROUND TRUTH:\n...",
  "citationPolicy": {
    "required": true,
    "minimumSources": 2,
    "canonicalPathsOnly": true
  },
  "qualityChecks": [
    {
      "id": "covers_owner_access",
      "description": "Answer mentions owner/entity or Co-Pilot access affordance."
    }
  ],
  "promptManifest": {
    "promptHash": "sha256:<hex>",
    "sourceChunkRefs": [
      "Book/12_Skeleton_Spec.md:37-59"
    ],
    "dataClass": "internal_non_sensitive",
    "retentionClass": "hash_only"
  },
  "warnings": []
}
```

The prompt package is the object that may be passed to a provider invocation
cell. It should not contain raw provider secrets. If a route blocks prompt
logging, the manifest should still keep hashes and source refs without storing
the full prompt text in long-lived audit logs.

## Model Adaptation Rules

The transformer should adapt format, not facts.

Allowed adaptation:

- choose a compact answer shape for smaller local models
- reduce chunk text when context is tight
- add `/no_think` or equivalent when a model family supports it and hidden
  reasoning must stay out of user-visible output
- specify citation style, for example inline `Book/path.md:line-line`
- choose language and maximum word count
- ask for explicit "not in ground truth" statements when coverage is weak

Forbidden adaptation:

- invent source facts that were not retrieved
- remove citation requirements because the target model is weak
- convert retrieval warnings into confident claims
- include raw credentials, private keys, provider tokens, or hidden scaffold
  state in prompt text
- make model/provider approval decisions

## Explore Contract

Suggested public operations:

| Keypath | Method | Purpose |
| --- | --- | --- |
| `ragPrompt.transform` | `set` | Accepts a RAG source package and target model profile; returns a prompt package. |
| `ragPrompt.profiles` | `get` | Lists built-in model prompt profiles known to the transformer. |
| `ragPrompt.qualityCheck` | `set` | Runs deterministic checks against a generated answer and prompt manifest. |

`ragPrompt.transform` must be deterministic for the same request, transformer
version, and source chunks. If a future implementation uses a model to compress
or rewrite context, that must be a separate, explicitly labelled operation with
its own provider route and audit manifest.

## Local Reference Tool

The repository-local reference transformer lives at:

`Tools/RAGPromptTransformer/rag_prompt_transformer.py`

It is intentionally not a model runner. It exists to make the contract concrete
and testable:

```bash
python3 Tools/RAGPromptTransformer/rag_prompt_transformer.py \
  --input path/to/rag-source-package.json \
  --out /tmp/prompt-package.json
```

The tool is suitable for test fixtures, eval harnesses, and early
CellScaffold/HAVENAgentD integration experiments. A production Cell can reuse
the same input/output contract while implementing authorization, storage, and
provider routing in the owning runtime.

## Done Definition

This contract is implemented in a runtime when:

- the RAG gateway can emit source packages with canonical citation metadata
- `RAGPromptTransformerCell` can transform them without additional lookup
- provider invocation accepts a prompt package or prompt manifest, not ad hoc
  hidden prompt text
- post-answer quality checks can verify citation coverage, required concepts,
  and forbidden claims
- generated answers can link back to canonical `Book/*.md` sections
