# Announcement: Local Small Models Available For HAVEN Experiments

Date: 2026-06-11

Audience: HAVEN conference/product, Porthole/Binding, privacy/safety, sponsor
value and Co-pilot stakeholders.

## Short Message

We now have a small set of local language models downloaded on Kjetil's laptop
for HAVEN conference and Co-pilot experiments, including Gemma 4 QAT models
that can use Apple Silicon through MLX/VLM.

They are available for local testing through `llama-cli` and `mlx-vlm`. They
are not approved as production assistants, policy authorities or autonomous
action callers.

## Available Models

GGUF local folder:

`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/local-models/gguf`

Gemma 4 MLX/VLM local folder:

`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Artifacts/gemma4-runtime/mlx`

| Model | Best current purpose |
| --- | --- |
| `Qwen3-8B-Q4_K_M.gguf` | Best tested local text candidate so far for controlled Norwegian Co-pilot helper experiments. Promising for agenda suggestions, constrained helper-card language and policy-safe phrasing after deterministic checks. |
| `Gemma 4 E4B QAT MLX/VLM` | Best Gemma candidate so far. Use for next M5-local conference assistant tests, especially multimodal tasks such as screenshots, posters/slides and audio snippets. |
| `Gemma 4 E2B QAT MLX/VLM` | Smaller Gemma comparison model for M5-local tests and multimodal smoke work. |
| `Qwen3-4B-Q4_K_M.gguf` | Comparison model for smaller local helper experiments. Better than the tiny models, but too uneven for default participant-facing behavior. |
| `Qwen3-1.7B-Q8_0.gguf` | Best candidate from this run for controlled local helper experiments: short agenda explanations, constrained routing tests, latency tests and local fallback demos. |
| `Qwen3-0.6B-Q8_0.gguf` | Tiny-model latency baseline and comparison model. Not reliable enough for conference helper decisions. |
| `qwen2.5-0.5b-instruct-q4_k_m.gguf` | Simple routing baseline. It selected the correct meeting-request action in one test, but failed Norwegian user-facing text. |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | Ultra-small baseline only. It is useful for testing the floor, not for participant-facing behavior. |

## HAVENAgentD Note

Gemma 4 should be exposed through HAVENAgentD for product-shaped tests:

- AgentD supervises the local `mlx_vlm.server` process on loopback.
- Co-pilot/Binding/Porthole call a stable AgentD provider id, not a raw
  filesystem model path.
- Credentialed web retrieval belongs in HAVENAgentD cells. Credentials should
  not be placed in prompts, result logs or benchmark scripts.
- Deterministic policy/action checks remain outside the model.

## What Interested Parties Can Use Them For Now

- Compare local model latency on Apple Silicon.
- Test whether Co-pilot helper cards can be drafted locally before escalation.
- Prototype deterministic action routing with model output validation.
- Explore local fallback behavior when external model access is unavailable or
  not justified.
- Evaluate whether a larger local model should be added next for conference
  assistant quality.

## What They Should Not Be Used For Yet

- Participant-facing conference concierge without guardrails.
- Sponsor lead qualification or consent decisions.
- Raw contact-info, profile or private-note handling.
- Unvalidated JSON/action payloads.
- Autonomous CellProtocol actions.
- Public claims that HAVEN now has a production-ready local AI assistant.

## Product Guidance

The smoke tests confirm the earlier toolbox direction:

The conference assistant should feel competent because the product has good
data lookup, consent rules, deterministic actions and validation. The local
model should phrase, summarize and suggest inside those boundaries.

For current experiments, `Qwen3-8B-Q4_K_M` is still the strongest local
text-only benchmark result. `Gemma 4 E4B QAT MLX/VLM` is the strongest Gemma
candidate and the better strategic choice where M5 acceleration, multimodal
input or long context matter. `Qwen3-4B-Q4_K_M` is useful as a smaller
comparison model. `Qwen3-1.7B` and below are valuable mostly as baselines.

Standardized Norwegian daily-speech benchmark results:

| Model | Representative 8-case score |
| --- | ---: |
| `Qwen3-1.7B-Q8_0` | `24/48` (`50.0%`) |
| `Qwen3-4B-Q4_K_M` | `31/48` (`64.6%`) |
| `Gemma 4 E2B QAT MLX/VLM` | `32/48` (`66.7%`) |
| `Gemma 4 E4B QAT MLX/VLM` | `36/48` (`75.0%`) |
| `Qwen3-8B-Q4_K_M` | `38/48` (`79.2%`) |

## Next Suggested Experiment

Run the full 40-case benchmark against `Gemma 4 E4B QAT MLX/VLM` through a
persistent local server supervised by HAVENAgentD. Then add explicit multimodal
tasks for screenshots, posters/slides and audio snippets. Keep `Qwen3-8B-Q4_K_M`
as the text-only comparison baseline.

## Test Log

Detailed results are in:

`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Local_Model_Availability_Test_Log_2026-06-11.md`
