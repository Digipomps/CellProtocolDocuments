# Hosted model API test log

Dato: 2026-06-19

Status: NanoGPT virker etter at credits ble lagt inn. Mistral API-key virker.
Mistral er lagt til i provider-verktøy, modellhøsting og Co-Pilot benchmark.

Ingen API-nøkler er skrevet til resultfiler, Book, benchmarkfiler eller Git.
Nøklene ble lest inn som prosess-lokale env-vars via stdin med terminal-echo
av.

## Kilder sjekket

- NanoGPT API/dashboard: `https://nano-gpt.com/api`
- NanoGPT auth docs: `https://docs.nano-gpt.com/authentication`
- Mistral docs: `https://docs.mistral.ai/`
- Mistral API reference: `https://docs.mistral.ai/api/`
- Mistral model endpoint: `https://docs.mistral.ai/api/endpoint/models`
- Mistral Studio/API-key console: `https://console.mistral.ai`

## Provider-verktøy oppdatert

- `Tools/ModelKnowledge/fetch_provider_models.py` støtter nå `mistral`.
- `Tools/ModelKnowledge/smoke_openai_compatible.py` støtter nå `mistral`.
- `Tools/CoPilotChatLanguageBenchmark/run_openai_compatible_cases.py` støtter
  nå `mistral`.
- `Book/model_provider_catalog_v0.json` har Mistral-providerpost.
- `Book/24_Model_Providers_Credentials_And_Selection.md` har Mistral-vurdering.

## Modellhøsting

Mistral:

- `GET https://api.mistral.ai/v1/models`
- Resultat: 71 modeller
- Snapshot:
  `Tools/ModelKnowledge/generated/mistral_models_20260619T073528Z.json`
- Første observerte modeller i snapshot:
  `mistral-medium-2505`, `mistral-medium-2508`, `open-mistral-nemo`,
  `open-mistral-nemo-2407`, `mistral-tiny-2407`, `mistral-tiny-latest`,
  `codestral-2508`, `codestral-latest`, `mistral-code-latest`,
  `mistral-code-fim-latest`, `devstral-2512`, `devstral-medium-latest`.

## Smoke tests

| Provider | Model | Resultat | Latency | Tokens | Output |
| --- | --- | --- | ---: | ---: | --- |
| Mistral | `mistral-small-latest` | OK | 0.828s | 108 | Kort norsk svar om representativ validering. |
| NanoGPT | `openai/gpt-4.1-nano` | OK | 1.522s | 79 | Kort norsk svar om data, kriterier og dokumentasjon. |

Resultfiler:

- `Tools/ModelKnowledge/generated/mistral_small_latest_smoke_20260619.json`
- `Tools/ModelKnowledge/generated/nanogpt_gpt41_nano_smoke_20260619.json`

## Co-Pilot Chat benchmark

### Mistral `mistral-small-latest` + JSON-mode

Resultfil:

`Tools/CoPilotChatLanguageBenchmark/results/mistral_small_latest_jsonmode_limit5_20260619.jsonl`

- Cases: 5
- Score: 22/30, 73.3%
- Parse errors: 1
- Intent: 3/5
- Action: 3/5
- Clarification: 4/5
- Safety: 4/5
- Must mention: 4/5
- Must not mention: 4/5

Vurdering:

- Teknisk API-rute virker godt.
- Benchmark-resultatet er research-nivå, ikke deltakerklart.
- Første case feilet parsing; resten var sterke nok til videre prompt/adapter-
  arbeid.

### NanoGPT `openai/gpt-4.1-nano` + JSON-mode

Resultfil:

`Tools/CoPilotChatLanguageBenchmark/results/nanogpt_gpt41_nano_jsonmode_limit3_20260619.jsonl`

- Cases: 3
- Score: 14/18, 77.8%
- Parse errors: 0
- Intent: 2/3
- Action: 0/3
- Clarification: 3/3
- Safety: 3/3
- Must mention: 3/3
- Must not mention: 3/3

Vurdering:

- NanoGPT-kontoen har nå fungerende credits for syntetiske API-tester.
- Modellen svarte strukturert, men actionKeypath var for svak i denne runden.
- Brukbar for billig smoke/discovery, men ikke nok til Co-Pilot action routing
  uten bedre prompt eller post-normalisering.

## Sammenligning med 2026-06-18

| Provider | Model | Cases | Score | Parse errors | Foreløpig bruk |
| --- | --- | ---: | ---: | ---: | --- |
| Featherless | `google/gemma-4-E2B-it` + JSON-mode | 3 | 16/18, 88.9% | 0 | Mest lovende korttest, må utvides. |
| NanoGPT | `openai/gpt-4.1-nano` + JSON-mode | 3 | 14/18, 77.8% | 0 | Billig hosted smoke/discovery. |
| Mistral | `mistral-small-latest` + JSON-mode | 5 | 22/30, 73.3% | 1 | EU/provider sammenligning og research. |
| Featherless | `Qwen/Qwen3-8B` | 5 | 22/30, 73.3% | 0 | Research; må forbedre intent/action. |

## Credential/runtime-anbefaling

API-nøkler skal samles som entity-scoped credentials, ikke scaffold-lokale
env-vars:

```text
Entity identity
  -> SecretCredentialCell / AI-provider credential policy
  -> CredentialVaultService + SecureCredentialStore
  -> Keychain/scoped secret provider
  -> AgentD provider.invoke / credential.authorizeUse
  -> external provider
```

Minimum credential metadata per provider:

- `providerID`: `featherless`, `nanogpt`, `mistral`
- `credentialLabel`
- `secretRef`, ikke raw key
- `ownerIdentityDomain`
- `allowedPurposeRefs`
- `allowedScaffolds`
- `allowedDataClasses`: foreløpig `synthetic`, `public`
- `blockedDataClasses`: credential secrets, private contact info, sponsor leads
  without consent, health, payment, children
- `maxMonthlySpendNOK`
- `requiresUserApproval`
- `dpaStatus`
- `sourceURLs`

## Neste test

1. Roter nøkler når SecretCredentialCell/AgentD-rute er klar.
2. Registrer Featherless, NanoGPT og Mistral som entity-scoped credentials.
3. Kjør representativ 8-case for:
   - Featherless `google/gemma-4-E2B-it` + JSON-mode
   - Mistral `mistral-small-latest` + JSON-mode
   - NanoGPT `openai/gpt-4.1-nano` + JSON-mode
4. Legg til post-normalisering for `needsClarification` og actionKeypath når
   modellens intensjon er riktig men schema-felt er feil.
5. Kjør safety/sponsor-cases før noen hosted route kan vurderes for mer enn
   syntetiske/offentlige data.

