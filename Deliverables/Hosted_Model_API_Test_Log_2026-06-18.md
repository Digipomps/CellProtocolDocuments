# Hosted model API test log

Dato: 2026-06-18

Status: Featherless API-key virker for syntetiske chat-completion tester.
NanoGPT API-key autentiserer langt nok til a fa provider/billing-svar, men
testen stoppet pa manglende saldo.

Ingen API-nokler er skrevet til resultfiler, Book, benchmarkfiler eller Git.
Forste PTY-forsok ekkoet stdin i terminaloutput; noklene bor derfor roteres
etter denne runden og neste test bor ga via SecretCredentialCell/AgentD eller
en ikke-ekkende credential-kanal.

## Tester kjort

### Smoke tests

Featherless:

- `Qwen/Qwen3-8B`
- `google/gemma-4-E2B`

NanoGPT:

- `openai/gpt-4.1-nano`

### Co-Pilot Chat daily-speech benchmark

Ny hosted runner:

`Tools/CoPilotChatLanguageBenchmark/run_openai_compatible_cases.py`

Resultfiler:

- `Tools/CoPilotChatLanguageBenchmark/results/featherless_qwen3_8b_limit5_20260618.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/featherless_gemma4_e2b_limit5_20260618.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/featherless_gemma4_e2b_it_jsonmode_limit3_20260618.jsonl`

Smoke-resultfiler:

- `Tools/ModelKnowledge/generated/featherless_qwen3_8b_smoke_20260618.json`
- `Tools/ModelKnowledge/generated/featherless_gemma4_e2b_smoke_20260618.json`

## Resultater

| Provider | Model | Test | Score | Parse errors | Vurdering |
| --- | --- | --- | ---: | ---: | --- |
| Featherless | `Qwen/Qwen3-8B` | smoke | OK | 0 | API virker, men smoke viste synlig thinking-output. |
| Featherless | `google/gemma-4-E2B` | smoke | OK teknisk | 0 | API virker, men modellen ekkoet prompten. |
| NanoGPT | `openai/gpt-4.1-nano` | smoke | blokkert | n/a | HTTP 402: insufficient balance. |
| Featherless | `Qwen/Qwen3-8B` | Co-Pilot limit 5 | 22/30, 73.3% | 0 | Brukbar research-rute, men lav intent/action-presisjon. |
| Featherless | `google/gemma-4-E2B` | Co-Pilot limit 5 | 0/30, 0.0% | 5 | Ikke egnet uten annen adapter/prompt. |
| Featherless | `google/gemma-4-E2B-it` + JSON-mode | Co-Pilot limit 3 | 16/18, 88.9% | 0 | Lovende; bor kjores pa full representativ 8-case og safety-cases. |

## Detaljer

`Qwen/Qwen3-8B`:

- 5 cases.
- Total: 22/30.
- Intent: 2/5.
- Action: 2/5.
- Clarification: 5/5.
- Safety: 3/5.
- Must mention: 5/5.
- Must not mention: 5/5.
- Beste cases: `no_daily_001`, `no_daily_004`.
- Svakhet: modellen svarte nyttig, men klassifiserte noen agenda-sporsmal som
  schedule/action i stedet for anbefaling.

`google/gemma-4-E2B`:

- 5 cases.
- Total: 0/30.
- Parse errors: 5/5.
- Svakhet: modellen fulgte ikke JSON-kontrakten og ekkoet prompten.

`google/gemma-4-E2B-it` med `response_format={"type":"json_object"}`:

- 3 cases.
- Total: 16/18.
- Intent/action/safety/mustMention/mustNotMention: 100%.
- Clarification: 1/3 fordi modellen returnerte tekst i
  `needsClarification` i to cases der boolean `false` var forventet.
- Vurdering: interessant nok til neste test. Krever schema-normalisering eller
  strengere prompt slik at `needsClarification` alltid er boolean.

NanoGPT:

- `openai/gpt-4.1-nano` stoppet med HTTP 402.
- Meldingen oppga manglende USD-saldo.
- Neste steg er a fylle lav test-saldo eller koble BYOK/routing med eksplisitt
  spend cap for syntetiske benchmarker.

## Anbefaling

1. Roter Featherless- og NanoGPT-noklene etter denne chat-baserte testingen.
2. Registrer neste nokler via SecretCredentialCell/AgentD, ikke chat.
3. Kjor `google/gemma-4-E2B-it` med JSON-mode pa representativ 8-case.
4. Kjor `Qwen/Qwen3-8B` pa samme 8-case med en sterkere `/no_think`/JSON
   prompt og vurder om thinking-output kan slas av provider-side.
5. Fyll minimal NanoGPT-saldo og kjor samme hosted runner mot
   `openai/gpt-4.1-nano`.
6. Ikke bruk hosted providers for private data for DPA/region/subprocessor er
   avklart.

