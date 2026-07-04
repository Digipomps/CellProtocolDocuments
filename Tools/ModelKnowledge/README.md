# Model Knowledge RAG And Provider Testing

Purpose: maintain a dedicated HAVEN knowledge base for language models,
providers, pricing/privacy posture, local runtimes and purpose matching.

This tool folder is intentionally secret-free. Do not paste API keys into
commands that will be saved in shell history, docs, benchmark JSON, or Git.

## Provider Keys

Use environment variables only as a temporary bridge until
`SecretCredentialCell` is implemented:

```bash
export FEATHERLESS_API_KEY="..."
export NANOGPT_API_KEY="..."
export MISTRAL_API_KEY="..."
```

NanoGPT API keys are created and managed in the NanoGPT dashboard/API page:

`https://nano-gpt.com/api`

NanoGPT docs say new keys use `sk-nano-<uuid>` and can be sent as
`Authorization: Bearer <API_KEY>` or `X-API-Key: <API_KEY>`.

Featherless docs say the API key comes from the dashboard and uses:

`Authorization: Bearer FEATHERLESS_API_KEY`

Featherless also offers account login through Hugging Face, Google, GitHub,
Discord and email/password. Treat Hugging Face as the external account login
provider when that is how the account was created, but use the Featherless
API key/session token for API calls. Do not store Hugging Face passwords in
this repo or in prompts.

Mistral API keys are managed in Mistral Studio at:

`https://console.mistral.ai`

Mistral's OpenAI-style chat and model-list endpoints use:

`https://api.mistral.ai/v1`

and bearer authentication:

`Authorization: Bearer MISTRAL_API_KEY`

## Build The Local Model-Knowledge Corpus

```bash
python3 Tools/ModelKnowledge/build_model_knowledge_corpus.py \
  --manifest Tools/ModelKnowledge/model_knowledge_sources.json \
  --out Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl
```

Query the local corpus:

```bash
python3 Tools/ModelKnowledge/query_model_knowledge.py \
  --corpus Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl \
  --query "hvilken modell bør brukes til konferanse multimodal QA"
```

This is a lightweight lexical RAG seed, not the final vector RAG. It gives
agents one dedicated corpus now, while the real embedding/reranker pipeline is
being wired.

## Fetch Provider Model Lists

Fetch Featherless:

```bash
FEATHERLESS_API_KEY="..." \
python3 Tools/ModelKnowledge/fetch_provider_models.py \
  --provider featherless \
  --out-dir Tools/ModelKnowledge/generated
```

Fetch NanoGPT:

```bash
NANOGPT_API_KEY="..." \
python3 Tools/ModelKnowledge/fetch_provider_models.py \
  --provider nanogpt \
  --out-dir Tools/ModelKnowledge/generated
```

Fetch Mistral:

```bash
MISTRAL_API_KEY="..." \
python3 Tools/ModelKnowledge/fetch_provider_models.py \
  --provider mistral \
  --out-dir Tools/ModelKnowledge/generated
```

The output is public-ish provider model metadata. It must still be reviewed
before being promoted into `Book/model_provider_catalog_v0.json`.

Summarize the latest provider snapshots into a smaller candidate list:

```bash
python3 Tools/ModelKnowledge/summarize_provider_models.py \
  --in-dir Tools/ModelKnowledge/generated
```

This extracts likely HAVEN-relevant model candidates such as Gemma, Qwen,
embedding, small-helper and agentic-coding models from very large provider
lists. The first-pass shortlist excludes obvious uncensored/abliterated-style
variants so they do not become default conference candidates by accident.

## Smoke Test A Provider Model

Featherless example:

```bash
FEATHERLESS_API_KEY="..." \
python3 Tools/ModelKnowledge/smoke_openai_compatible.py \
  --provider featherless \
  --model Qwen/Qwen2.5-7B-Instruct \
  --out Tools/ModelKnowledge/generated/featherless_smoke.json
```

NanoGPT example:

```bash
NANOGPT_API_KEY="..." \
python3 Tools/ModelKnowledge/smoke_openai_compatible.py \
  --provider nanogpt \
  --model gpt-4.1-nano \
  --out Tools/ModelKnowledge/generated/nanogpt_smoke.json
```

Mistral example:

```bash
MISTRAL_API_KEY="..." \
python3 Tools/ModelKnowledge/smoke_openai_compatible.py \
  --provider mistral \
  --model mistral-small-latest \
  --out Tools/ModelKnowledge/generated/mistral_smoke.json
```

Only synthetic/public prompts should be used until provider DPA/GDPR status and
`SecretCredentialCell` routing are implemented.
