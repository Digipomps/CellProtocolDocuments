# AI-agent provider onboarding og modell-RAG

Dato: 2026-06-18

Status: operativt oppsett pa plass for metadata og syntetiske tester; ingen
API-nokler er lagret i repo.

## Formaal

HAVEN trenger en modellverktoykasse som kan velge modell etter faktisk oppgave,
scaffold, hardware, kost, lisens, data-klasse og GDPR-risiko. For
konferanselosningen betyr det at Co-pilot Chat ma oppleves nyttig og kompetent
i normal dagligtale, samtidig som private data, sponsorleads og credentials
ikke sendes til feil sted.

NanoGPT og Featherless bor behandles som discovery- og bake-off-lag: vi tester
mange modeller med syntetiske eller offentlige prompts, finner kandidater som
er verdt a kjore lokalt, og promoterer bare modeller til produksjonsbruk nar
credential-, avtale-, privacy- og benchmarklaget er pa plass.

## Dette finnes na

- `Book/24_Model_Providers_Credentials_And_Selection.md` definerer
  providerstrategi, secret-regel, provider-policy og forelopig vurdering av
  NanoGPT, Featherless og lokal AgentD-rute.
- `Book/25_SecretCredentialCell.md` og
  `Book/secret_credential_cell_contract_v0.json` beskriver
  SecretCredentialCell-kontrakten: metadata ut, aldri raw secret ut.
- `Book/26_Model_Knowledge_And_Purpose_Matching.md` definerer
  modellkunnskap, purpose-profiler, hard filters og scoring.
- `Book/model_provider_catalog_v0.json` er maskinlesbar seed for provider- og
  modellvalg.
- `Tools/ModelKnowledge/` er ny operativ seed for en separat modell-RAG og
  provider-testpakke.
- Eksisterende credential-byggesteiner finnes allerede i kodebasen:
  `CredentialVaultService`, `SecureCredentialStore`,
  `AppleKeychainSecureCredentialStore`, `IdentityVault` som
  `ScopedSecretProviderProtocol`, og `ScopedCredentialCell`.
- `ScopedCredentialCell` er nyttig som eksplisitt bruker-/sessionflate, men
  dagens v1 er `session_only_redacted`; varige provider-nokler bor i
  secure-store/vault-laget bak en policycelle.

## Providerfakta sjekket 2026-06-18

### NanoGPT

- API-base: `https://nano-gpt.com/api/v1`.
- API-nokler opprettes/administreres fra `https://nano-gpt.com/api`.
- Dokumentasjonen sier nye nokler bruker formatet `sk-nano-<uuid>`.
- Auth kan sendes som `Authorization: Bearer <API_KEY>` eller `X-API-Key`.
- `GET /api/v1/models` kan brukes til a hente modell- og prisinformasjon.
- NanoGPT har BYOK, provider-routing og redaction-kontroller, men BYOK-ruter
  gar fortsatt via NanoGPT som proxy. Hvis provider-rute betyr noe, ma
  fallback deaktiveres eksplisitt.

### Featherless

- API-base: `https://api.featherless.ai/v1`.
- Quickstart viser OpenAI-kompatibel klient og `Authorization: Bearer`.
- Login-siden tilbyr blant annet "Sign in with Hugging Face". For kontoer som
  bruker Hugging Face-login, bor vi modellere Featherless som en
  provider-konto med ekstern login-provider, pluss separat Featherless API-key
  eller session-token for faktisk API-bruk.
- Providerens API returnerer en stor `/models`-liste uten at vi matte bruke
  nokkel via `curl`; Python-klienten trengte eksplisitt User-Agent for robust
  harvesting.
- Privacy/logging-dokumentasjonen hevder at API prompts/completions ikke
  lagres, mens hosted chat har egen historikk/retensjon.
- Planene er subscription/concurrency-basert. Det passer discovery godt, men
  privat HAVEN-data krever fortsatt DPA/subprocessor/region/lisensavklaring.

## Hva som ble testet lokalt

- Python-verktøyene i `Tools/ModelKnowledge/` kompilerer.
- Modellkunnskapscorpus ble bygget:
  `Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl`
- Corpus inneholder 96 chunks fra utvalgte Book-, katalog-, benchmark- og
  leveransefiler.
- Provider-snapshottene ble filtrert til en liten kandidatshortlist:
  `Tools/ModelKnowledge/generated/provider_model_candidates_latest.json`
- Kandidatshortlisten inneholder 106 modeller fordelt pa Gemma/Qwen,
  embedding, small-helper og agentic-coding regler.
- Lokal RAG-query for "hvilken modell bor brukes til konferanse multimodal QA"
  returnerte seed-katalogen, Gemma 4-runtime-notatet og
  purpose-mapping-kapittelet som toppkilder.
- NanoGPT `/models` ble hentet uten API-nokkel og lagret som:
  `Tools/ModelKnowledge/generated/nanogpt_models_20260618T093151Z.json`
- NanoGPT-snapshoten inneholder 627 normaliserte modellposter.
- Featherless `/models` ble verifisert tilgjengelig via `curl` og viste blant
  annet `google/gemma-4-E2B`, `google/gemma-4-E4B`, `Qwen/Qwen3-8B`,
  `Qwen/Qwen3-VL-8B-Instruct`, `Qwen/Qwen3-Embedding-0.6B` og
  `TinyLlama/TinyLlama-1.1B-Chat-v1.0`.

Ingen hosted chat-completion smoke-test ble kjort, fordi API-nokler ikke skal
limes inn i chat eller skrives i repo. Neste sikre steg er a registrere dem via
SecretCredentialCell eller en midlertidig lokal env-var i en terminal som ikke
logges til docs.

## Hva vi trenger for full provider-stotte

1. Implementer `SecretCredentialCell`/AI-provider credential-fasade i
   HAVENAgentD forst, men bygg den oppa eksisterende
   `CredentialVaultService`/`SecureCredentialStore`/Keychain/scoped-secret
   primitives.
2. Lag en provider-descriptor per leverandor:
   providerID, baseURL, auth-type, models endpoint, chat endpoint, pricing
   source, privacy source, credential policy, allowed data classes og default
   smoke-testmodell.
3. Legg Featherless- og NanoGPT-noklene inn som entity-scoped credentials med
   owner identity, purpose policy, spend cap og data-class blokkering. For
   Featherless/Hugging Face-login: lagre ikke HF-passord; lagre providerens
   API-key/session eller en autorisert login-handle.
4. La scaffolds be om `credential.authorizeUse` eller `provider.invoke`; de
   skal ikke fa raw API-key.
5. Utvid Co-pilot benchmarken slik at den kan kjore samme norske dagligtale-,
   agenda-, privacy- og multimodal-caser mot lokale modeller, NanoGPT,
   Featherless og senere andre OpenAI-kompatible leverandorer.
6. Merge provider `/models`, pricing, privacy og benchmarkresultater inn i
   `Book/model_provider_catalog_v0.json` eller en etterfolger.
7. Bruk hosted providers kun for `synthetic` og `public` data inntil DPA,
   subprocessors, region og lisens er vurdert.

## Forelopig modellstrategi for neste tester

- Lokal tekstbaseline: `Qwen3-8B-Q4_K_M`.
- Lokal multimodal M5-kandidat: `Gemma 4 E2B`, `Gemma 4 E4B` og `Gemma 4 E4B
  QAT` via MLX/VLM der de finnes og gir mening.
- Embedding/RAG: `BAAI/bge-m3` og eventuelt `Qwen/Qwen3-Embedding-*` som
  kandidater for sammenligning.
- Reranking: `BAAI/bge-reranker-v2-m3`.
- PII preflight: `urchade/gliner_multi_pii-v1` eller tilsvarende lokal
  entity/PII-detektor.
- Hosted discovery: Featherless for open-weight modeller for eventuell lokal
  nedlasting; NanoGPT for bred aggregator/media/frontier-sampling.

## Standard testkommandoer

Bygg modellkunnskap:

```bash
python3 Tools/ModelKnowledge/build_model_knowledge_corpus.py \
  --manifest Tools/ModelKnowledge/model_knowledge_sources.json \
  --out Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl
```

Query modell-RAG seed:

```bash
python3 Tools/ModelKnowledge/query_model_knowledge.py \
  --corpus Tools/ModelKnowledge/generated/model_knowledge_corpus.jsonl \
  --query "hvilken modell bor brukes til konferanse multimodal QA"
```

Hent provider-modeller:

```bash
python3 Tools/ModelKnowledge/fetch_provider_models.py \
  --provider nanogpt \
  --no-auth \
  --out-dir Tools/ModelKnowledge/generated
```

```bash
python3 Tools/ModelKnowledge/fetch_provider_models.py \
  --provider featherless \
  --no-auth \
  --out-dir Tools/ModelKnowledge/generated
```

Kjor syntetisk smoke-test nar credentials er trygt tilgjengelige:

```bash
FEATHERLESS_API_KEY="..." \
python3 Tools/ModelKnowledge/smoke_openai_compatible.py \
  --provider featherless \
  --model Qwen/Qwen3-8B
```

```bash
NANOGPT_API_KEY="..." \
python3 Tools/ModelKnowledge/smoke_openai_compatible.py \
  --provider nanogpt \
  --model gpt-4.1-nano
```

Disse env-varene er kun en midlertidig bro. Den varige losningen er
`SecretCredentialCell` + AgentD-provider-invocation.
