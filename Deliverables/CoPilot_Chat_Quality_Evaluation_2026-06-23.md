# Co-Pilot Chat Quality Evaluation

Dato: 2026-06-23

Scope: fersk kvalitetsevaluering av HAVEN Co-Pilot chat med frontier-modeller,
lokal modell, Apple/Binding-kontrakt og iPhone/iPad-paritet.

## Kilder og modellvalg

- OpenAI modell-listen for kontoen eksponerte `gpt-5.5`, `gpt-5.5-pro` og
  nyere `gpt-5.x`-familie via API.
- Anthropic modell-listen eksponerte `claude-fable-5`, `claude-opus-4-8` og
  `claude-sonnet-4-6`; API svarte at `claude-fable-5` ikke er tilgjengelig på
  kontoen og ba om Opus 4.8.
- Apple Intelligence ble vurdert mot offisiell Apple Intelligence/Foundation
  Models-plattform og Binding sin faktiske `BindingAppleIntelligenceProviderCell`.
  I denne runden er verifisert Apple-spor en Binding/provider-kontrakt og
  device-paritet, ikke dokumentert live Foundation Models-kvalitet.

## Benchmark-harness

Brukt benchmark:

- `Tools/CoPilotChatLanguageBenchmark/cases.no.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/rubric.md`
- scoring: intent, action, clarification, safety, mustMention, mustNotMention
  med 6 poeng per case.

Runnerendringer:

- `run_openai_compatible_cases.py` støtter nå `openai`, `max_completion_tokens`
  for GPT-5/o-serie og `--omit-temperature`.
- `run_openai_responses_cases.py` ble lagt til for OpenAI Responses API, brukt
  til `gpt-5.5-pro`.
- `run_anthropic_cases.py` ble lagt til/oppdatert for Anthropic Messages API og
  `--omit-temperature`.

Alle runnerendringer ble `py_compile`-verifisert.

## Resultater

| Route | Cases | Score | Parse | Kommentar |
| --- | ---: | ---: | ---: | --- |
| Anthropic `claude-opus-4-8` | 40 | 197/240 (82.1%) | 0 | Best total, sterk på intent/action, svak safety-labeling. |
| OpenAI `gpt-5.5` | 40 | 196/240 (81.7%) | 0 etter repair | Nær Opus; trengte `max_completion_tokens=2000` for fire cases. |
| OpenAI `gpt-5.5-pro` | 3/8 partial | 13/18 (72.2%) | 0 | Responses API virker, men 68-96s per case og ikke bedre; stoppet. |
| Lokal Qwen3-8B Q4 via `llama-server` | 8 | 34/48 (70.8%) | 0 | Teknisk stabil på M5/Metal, men under frontier og eldre best Qwen-resultat. |
| Tidligere Qwen3-8B Q4 CLI v2 | 8 | 38/48 (79.2%) | 0 | Bedre enn dagens server-run; prompt/runtimeforskjell bør analyseres. |
| Tidligere Gemma 4 E4B QAT MLX | 8 | 36/48 (75.0%) | 0 | Nyttig lokal kandidat, men safety/mentions svake. |

Viktig funn: De beste modellene når ikke deltakerklar gate i nåværende harness.
Rubrikken krever ca. 95% intent/action og 100% safety for produktbruk. Gapet er
ikke bare modellkapasitet; safety-labels og action-policy må styres
deterministisk eller med langt skarpere kontekst/prompt.

## Apple, iPhone og iPad

Kjøring:

- macOS: `ChatWorkbenchParityTests`, 27/27 pass.
- iPhone 17 Pro simulator OS 26.2: `ChatWorkbenchParityTests`, 27/27 pass.
- iPad Pro 13-inch (M5) simulator OS 26.2: testhost krasjet før bootstrap to
  ganger, ingen chat-assertion ble kjørt.
- iPad mini (A17 Pro) simulator OS 26.2: `ChatWorkbenchParityTests`, 27/27 pass.

Dette verifiserer at chat/provider-kontrakten og Apple Intelligence-ruten er
semantisk lik på macOS, iPhone og minst én iPad-simulator. Det verifiserer ikke
at live Apple Foundation Models gir frontier-lik språkmodellkvalitet; dagens
eval-runner bruker fixture/fallback for Apple-providerens prompt-evaluering.

## Hovedfunn

1. Frontier-modellene er gode nok til å lage baseline-kandidater, men ikke til å
   eie policy eller action-routing alene.
2. Safety er svakeste dimensjon hos både Opus og OpenAI. Opus fikk 55.0% safety,
   OpenAI 65.0%.
3. OpenAI `gpt-5.5` trenger Responses/Chat-kontrakttilpasning: `max_tokens` og
   `temperature=0` feiler; `max_completion_tokens` og default temperature virker.
4. `gpt-5.5-pro` er for treg i denne harnessen for interaktiv Co-Pilot chat.
5. Lokal Qwen3-8B på M5/Metal er teknisk lovende, men trenger kompakt
   purpose/context-pack og policy-normalisering før den kan nærme seg frontier.
6. Binding-paritet er sterk for kontrakt og side-effect-sikkerhet på macOS,
   iPhone og iPad mini. iPad Pro-simulatoren må debugges som testhost/harness.

## Anbefalt tuningplan

1. Flytt safety/action-beslutning ut av modellen:
   - modellen foreslår intent, slots og naturlig tekst
   - deterministisk HAVEN-policy bestemmer `safetyDecision` og tillatt action
   - actionKeypath normaliseres mot allowlist

2. Lag frontier-baseline-sett:
   - bruk Opus 4.8 og OpenAI `gpt-5.5`
   - behold menneskevurdert fasit for cases der modellene er uenige
   - lag per-case “gold explanation” for hvorfor safety/action er riktig

3. Lag kompakt context-pack for små modeller:
   - canonical intent/action/safety labels
   - 3-5 fåskudds-eksempler for privacy, sponsor, publish, ambiguous followup
   - kort purpose/goal-sett for chat: side-effect-free, consent, action requires click
   - explicit “unknown/ask” regler når synlig kontekst mangler

4. Evaluer småmodeller på samme gate:
   - lokal Qwen3-8B `llama-server`
   - Gemma 4 E4B QAT MLX
   - Apple Foundation Models live bare når runtime/entitlement faktisk er ready
   - nanoGPT/Featherless når credentials er entity-scoped via SecretCredentialCell

5. Device-gate:
   - behold `ChatWorkbenchParityTests` som macOS/iPhone/iPad-kontraktgate
   - legg til eksplisitt Apple live-availability test som rapporterer status/reason
   - feilsøk iPad Pro 13-inch simulator bus-error separat

## Artefakter

- `Tools/CoPilotChatLanguageBenchmark/results/anthropic_claude_opus48_full_20260622.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/openai_gpt55_full_repaired_20260622.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/openai_gpt55_parse_repair_20260622.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/openai_gpt55pro_responses_representative8_20260622.jsonl`
- `Tools/CoPilotChatLanguageBenchmark/results/qwen3_8b_q4_local_server_representative8_20260623.jsonl`
- Binding xcresults:
  - macOS: `Test-Binding-2026.06.22_15-44-02-+0200.xcresult`
  - iPhone: `Test-Binding-2026.06.22_15-44-26-+0200.xcresult`
  - iPad Pro failed: `Test-Binding-2026.06.22_15-45-10-+0200.xcresult`,
    `Test-Binding-2026.06.22_15-47-00-+0200.xcresult`
  - iPad mini: `Test-Binding-2026.06.23_08-54-49-+0200.xcresult`
