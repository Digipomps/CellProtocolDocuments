# Chapter 24 — Model Providers, Credentials, and Model Selection

Status: draft operational contract.

Last updated: 2026-06-18.

This chapter defines how HAVEN should handle language-model credentials and how
scaffolds should decide which model/provider to use for a task. It is not a
claim that any provider is production-approved for personal data. Provider
details change quickly; the machine-readable catalog and source links must be
refreshed before procurement or production routing decisions.

## 1. Current Local Ground Truth

Existing notes already cover parts of the model toolbox:

- `Deliverables/Model_Toolbox_Advisory_2026-06-11.md`
- `Deliverables/HuggingFace_Local_Model_Recommendations_2026-06-11.md`
- `Deliverables/CoPilot_Conference_Small_Model_Helper_Assessment_2026-06-11.md`
- `Deliverables/Gemma4_Local_Runtime_Test_Log_2026-06-12.md`
- `Deliverables/HavenAgentD_Gemma4_MLX_Runtime_Integration_2026-06-12.md`
- `Tools/CoPilotChatLanguageBenchmark/`

What was missing was one shared place for:

- API-key placement across scaffolds;
- provider privacy/GDPR posture;
- model selection by task, hardware, cost and data sensitivity;
- a machine-readable catalog that future agents can query.

Existing credential/vault primitives already exist and should be reused:

- `CellProtocol/Sources/CellBase/EntityAtlas/SecureCredentialStore.swift`
  defines `SecureCredentialStore` and `CredentialVaultService`, with raw
  secrets separated from syncable credential metadata.
- `CellProtocol/Sources/CellApple/EntityAtlas/AppleKeychainSecureCredentialStore.swift`
  provides the Apple Keychain-backed secure credential store.
- `CellProtocol/Sources/CellApple/IdentityVault.swift` implements
  `ScopedSecretProviderProtocol` and stores scoped secret material in Keychain.
- `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift`
  contains `ScopedCredentialCell`, but its current v1 storage is
  `session_only_redacted`; use it as an explicit UI/session surface, not as
  the durable provider-vault by itself.

The seed catalog is:

`Book/model_provider_catalog_v0.json`

Related detailed contracts:

- `Book/25_SecretCredentialCell.md`
- `Book/secret_credential_cell_contract_v0.json`
- `Book/26_Model_Knowledge_And_Purpose_Matching.md`

## 2. Secret Rule

Do not store provider API keys in prompts, CellConfiguration JSON, skeletons,
benchmark result files, logs, Book markdown, Git, or ordinary cell state.

An API key is a protected resource owned by an entity-controlled secret vault.
Scaffolds should receive a capability to use the key for a declared purpose,
not the raw key itself.

The preferred shape is:

```text
Entity / operator
  -> domain-scoped Identity
  -> SecretCredentialCell
  -> provider invocation cell or HAVENAgentD bridge
  -> external provider
```

Because the core identity model says Entities are conceptual and Identities are
the operational handles, implementation should bind credentials to an owning
Identity/Vault and expose them as entity-scoped resources only through
Agreement-backed capabilities.

## 3. SecretCredentialCell Contract

Proposed endpoint:

`cell:///entity/credentials`

Protected resources:

- provider API keys;
- short-lived provider session tokens;
- bring-your-own-key settings;
- billing/spend limits;
- provider routing policy;
- DPA/GDPR approval metadata.

Readable keys must expose metadata only:

- `credentials.list`
- `credentials.providerState`
- `credentials.policy`
- `credentials.audit`

Writable/action keys:

- `credential.register`
- `credential.rotate`
- `credential.revoke`
- `credential.test`
- `provider.invoke`

`GET` must never return raw secret material.

`credential.test` should verify the key through a minimal provider health call
and return status, provider id, model id, latency and masked billing metadata.

`provider.invoke` should make the provider call inside the trusted cell/AgentD
boundary and return a bounded response. This is safer than handing the API key
to every scaffold process.

## 4. Credential Metadata

Each credential should have metadata shaped roughly like:

```json
{
  "credentialID": "cred.nanogpt.primary",
  "providerID": "nanogpt",
  "secretRef": "secret://entity/provider/nanogpt/api-key",
  "storageBackend": "keychain-or-agentd-secret-store",
  "ownerIdentityDomain": "domain:personal:ai",
  "allowedPurposeRefs": [
    "personal.ai.provider.external-testing",
    "conference.co-pilot.model-evaluation"
  ],
  "allowedScaffolds": [
    "CellScaffold",
    "Binding",
    "Porthole",
    "HAVENAgentD"
  ],
  "allowedDataClasses": [
    "public",
    "internal_non_sensitive",
    "synthetic"
  ],
  "blockedDataClasses": [
    "private_contact_info",
    "sponsor_leads_without_consent",
    "health",
    "payment",
    "children"
  ],
  "maxMonthlySpendNOK": 500,
  "requiresUserApproval": true,
  "rotationDays": 90,
  "dpaStatus": "unknown"
}
```

The `secretRef` is not the secret. It is an opaque reference understood by the
vault/AgentD process.

## 5. Provider Invocation Policy

Every external model call should record:

- requester identity;
- purpose ref;
- provider id;
- model id;
- credential id;
- data class;
- whether PII redaction ran;
- whether fallback routing was allowed;
- prompt manifest hash;
- response hash;
- token/cost estimate;
- retention/DPA posture used for the routing decision.

This gives us a path to answer "why did this scaffold use this model?" without
leaking the prompt or the API key.

## 6. Model Selection Matrix

Use this order when deciding where a prompt should go:

| Data/task class | Preferred route | Reason |
| --- | --- | --- |
| Deterministic policy, grants, publish/delete/send | No LLM | Policy/action authority must stay deterministic. |
| Private local draft, short rewrite, helper-card explanation | Apple/on-device or local model | Keeps data local and cheap. |
| Conference participant text over public agenda/policy | Local Qwen/Gemma or approved hosted test provider | Competence matters, but data can be bounded. |
| Screenshot/poster/audio selected by user | Gemma 4 E4B QAT local first; hosted multimodal only with explicit approval | Media often contains personal data. |
| Coding, architecture, protocol reasoning | Frontier hosted model or local heavier model depending on sensitivity | Quality may justify cost after context minimization. |
| Model discovery / bake-off over synthetic prompts | NanoGPT or Featherless | Good for broad provider/model sampling before local download. |
| Personal data, sponsor leads, private profile notes | Local/AgentD only unless Agreement and DPA allow external routing | GDPR and trust boundary dominate model quality. |

## 7. Current Provider Assessment

### NanoGPT

Source checked: <https://nano-gpt.com/api>,
<https://docs.nano-gpt.com/authentication>, <https://nano-gpt.com/pricing>,
<https://nano-gpt.com/privacy>.

Useful facts observed 2026-06-18:

- OpenAI-compatible base URL: `https://nano-gpt.com/api/v1`.
- API keys are created and managed from the NanoGPT API/dashboard page; current
  docs say new keys use the `sk-nano-<uuid>` format.
- API docs listed 1,027 total models: 613 text, 186 image, 124 video, audio,
  speech-to-text and embeddings.
- API keys can be supplied as bearer or `x-api-key`; the UI said up to 20 keys.
- Pricing is pay-as-you-go; the pricing page says text model API usage is
  billed at list prices with no percentage markup except opt-in cases such as
  pinned provider routing and BYOK.
- The privacy page says browser conversation history is local by default, but
  providers receive the request content needed to answer.
- NanoGPT offers optional PII redaction, BYOK, provider fallback controls,
  and some TEE/private model paths. The same page warns that TEE is not one
  universal guarantee and that normal API/web requests may still pass plaintext
  through NanoGPT before routing.

HAVEN position:

- Good for broad model discovery, price/performance sweeps, media-model tests,
  and synthetic/non-sensitive benchmark prompts.
- Do not treat it as automatically GDPR-safe for personal data.
- If used with BYOK, remember BYOK still passes through NanoGPT as proxy
  according to their API page; disable fallbacks when provider routing matters.
- Prefer explicit provider/model pinning for reproducible tests even if it adds
  cost.

### Featherless

Source checked: <https://featherless.ai/>, <https://featherless.ai/docs/overview>,
<https://featherless.ai/docs/quickstart-guide>,
<https://featherless.ai/docs/plans>,
<https://featherless.ai/docs/privacy-and-logging>,
<https://featherless.ai/legal/privacy-policy>,
<https://featherless.ai/legal/terms-of-service>.

Useful facts observed 2026-06-18:

- Featherless describes itself as serverless access to open-weight AI models.
- The landing page advertises one API key and 30,000+ models.
- Docs describe an OpenAI-compatible API at `https://api.featherless.ai/v1`.
- Quickstart docs use dashboard-created API keys with bearer authentication.
- The Featherless login page offers sign-in with Google, Hugging Face, GitHub,
  Discord or email/password. If the operator uses Hugging Face sign-in, model
  the account credential as a Featherless provider account linked to a
  Hugging Face login route; do not store a Hugging Face password in HAVEN.
- API privacy/logging docs say API chats, prompts and completions are not
  logged and are processed in real time, while hosted chat history is stored
  separately and auto-deleted after 30 days of inactivity.
- Plans are subscription/concurrency based. The plans page listed consumer
  tiers at $10/month up to 15B parameters and $25/month for catalogue access,
  plus agentic/business tiers around $100-$200/month with larger model access,
  8 concurrent connections and up to 256K context.
- The privacy policy says they collect account/payment data and usage metrics,
  and says prompts/completions are not collected or stored.
- Terms say Featherless is a Delaware LLC, is in beta, and that users are
  responsible for model-license compliance.

HAVEN position:

- Good for testing many open-weight models before downloading them locally.
- Especially useful for deciding which Qwen, Gemma, Mistral, DeepSeek, Kimi,
  RWKV or GPT-OSS style models are worth local conversion or MLX/GGUF work.
- Not automatically approved for private HAVEN data until we verify DPA,
  subprocessors, processing regions and model-license terms for the chosen
  model.
- Hosted chat should not be used for sensitive HAVEN evaluation because it has
  a separate chat-history retention path. Prefer API for tests.

### Mistral AI

Source checked: <https://docs.mistral.ai/>, <https://docs.mistral.ai/api/>,
<https://docs.mistral.ai/api/endpoint/models>, <https://console.mistral.ai>.

Useful facts observed 2026-06-19:

- API-base: `https://api.mistral.ai/v1`.
- Chat endpoint: `POST /v1/chat/completions`.
- Model-list endpoint: `GET /v1/models`.
- API reference examples use bearer authentication with `MISTRAL_API_KEY`.
- Mistral documentation points users to Studio/console for API keys,
  playground, evaluations, agents and workspace/API-key management.

HAVEN position:

- Good for hosted EU/provider comparison, coding/protocol reasoning tests and
  synthetic Co-pilot benchmark sweeps.
- `mistral-small-latest` is a sensible first low-cost hosted benchmark model.
- Do not treat Mistral as approved for private HAVEN data until DPA, region,
  retention, subprocessors and workspace policies are reviewed.
- Keep Mistral credentials entity-scoped behind `SecretCredentialCell`/AgentD
  like other hosted providers.

## 8. Model Knowledge Base Fields

Every model/provider record should capture:

- provider id;
- model id;
- model family;
- modality: text, vision, audio, video, embeddings;
- local/hosted/aggregator route;
- license and model terms;
- context length;
- pricing model;
- rough latency;
- tested hardware/runtime;
- known strengths;
- known weaknesses;
- benchmark results;
- allowed data classes;
- GDPR/DPA posture;
- source URLs and date checked;
- current HAVEN recommendation.

The catalog should distinguish:

- model facts from provider claims;
- provider privacy claims from verified HAVEN policy;
- local test results from expected capability;
- "available" from "approved".

## 9. Initial Recommendation

Subscribe/test in this order:

1. Featherless first for open-weight model discovery, because it maps directly
   to the question "which model should we later run locally?"
2. NanoGPT next for broad aggregator testing across closed, open, image, video,
   audio and TEE/private routes.
3. Keep all first tests synthetic or public: Co-pilot benchmark cases, public
   agenda/policy, code snippets without secrets, and generated sample media.
4. Do not send private entity data, sponsor leads, contact info, meeting notes
   or user vault content until the credential cell, Agreement route and DPA
   status are explicit.

For local defaults today:

- `Qwen3-8B-Q4_K_M` remains the best tested local text-only score in the
  Norwegian Co-pilot benchmark.
- `Gemma 4 E4B QAT MLX/VLM` is the primary local M5/multimodal candidate.
- `bge-m3`, `bge-reranker-v2-m3` and `gliner_multi_pii-v1` remain high-value
  small helper candidates for retrieval and safety preflight.

## 10. Open Implementation Work

1. Implement the `SecretCredentialCell` draft from
   `Book/25_SecretCredentialCell.md` in HAVENAgentD first, reusing
   `CredentialVaultService`, `SecureCredentialStore`,
   `AppleKeychainSecureCredentialStore` and scoped secret providers instead of
   inventing a parallel credential vault.
2. Add provider descriptors for NanoGPT and Featherless to the runtime layer.
3. Add a provider invocation proxy through HAVENAgentD.
4. Extend the Co-pilot benchmark runner to support hosted OpenAI-compatible
   providers through secret refs, not raw environment variables.
5. Add a model-evaluation workbench surface that writes results into
   `Book/model_provider_catalog_v0.json` or its successor.
6. Verify DPA/GDPR status for any provider before using personal data.
