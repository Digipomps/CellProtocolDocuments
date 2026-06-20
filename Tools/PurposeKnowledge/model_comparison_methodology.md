# Purpose Decomposition Model Comparison Methodology

Status: v0, 2026-06-14.

Goal: compare HAVEN's deterministic purpose resolver, large frontier models, and smaller local models on the same prompt-to-purpose task. The result should guide prompt/instruction tuning, local model selection, and future fine-tuning without letting any model mutate the canonical purpose taxonomy.

## Current Reference Models

Model availability changes quickly. For each benchmark run, verify provider docs that day and record the checked URL and model ID in the run metadata.

Official docs checked on 2026-06-14:

- OpenAI models page: GPT-5.5 is presented as the flagship model for complex reasoning/coding, with GPT-5.4 mini/nano positioned for lower latency/cost.
- Anthropic models page: Claude Fable 5 is described as the most capable widely released Claude model; Claude Mythos 5 is limited availability; Opus/Sonnet/Haiku model IDs are listed for API use.
- Google Gemini models page: Gemini 3.1 Pro, Gemini 3.5 Flash, Gemini 3 Flash, and Gemini 3.1 Flash-Lite are listed in the Gemini 3 family; Gemini 2.5 Pro remains described as advanced for complex tasks.

Use provider docs as source-of-truth for names, IDs, pricing, context, and availability. Do not bake these IDs into HAVEN tests permanently.

Sources:

- https://developers.openai.com/api/docs/models
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://ai.google.dev/gemini-api/docs/models

## Evaluation Sets

Use `Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl` as the current gold set.

The set includes:

- project/work management prompts
- questionnaire prompts
- GUI/access/governance prompts
- grounding/local-model/taxonomy-intake prompts
- personal semantic context prompts
- scaffold operations prompts
- known conference PromptPurposeLab-style prompts
- unknown and negated prompts
- mixed prompts with multiple purpose branches

Each case should contain:

- `id`
- `category`
- `source`
- `prompt`
- optional `visibleCapabilities`
- `expected.mustIncludePurposeRefs`
- optional `expected.mustExcludePurposeRefs`
- optional `expected.mustIncludeGoalRefs`
- optional `expected.nearestSharedPurposeRef`
- optional `expected.status`

## Baselines

Run these in order:

1. `haven-deterministic`: `node Tools/PurposeKnowledge/evaluate_purpose_cases.mjs`
2. `frontier-closed-book`: major hosted models with no taxonomy excerpt.
3. `frontier-open-taxonomy`: same models with compact taxonomy context.
4. `frontier-retrieved-context`: same models with top-K HAVEN resolver nodes.
5. `local-open-taxonomy`: local models with the exact same prompt and taxonomy context.
6. `local-repair`: local models get validator errors and one correction attempt.

The deterministic resolver is the safety baseline. Frontier models are advisors and comparators, not final authority.

## Required Model Output

Ask every model to emit JSON matching `haven.purpose-model-output.v0`; use `Tools/PurposeKnowledge/model_decomposition_prompt.v0.md`.

Minimum output fields:

- `status`
- `purposeRefs`
- `goalRefs`
- `nearestSharedPurposeRef`
- `candidatePurposeRefs`
- `missingCapabilities`
- `reviewRequired`
- `confidence`
- `sideEffectFree=true`
- `mutatesPerspective=false`
- `mutatesEntity=false`

Reject outputs that:

- are not valid JSON
- invent non-`purpose://` refs
- omit side-effect flags
- claim mutation or execution
- silently convert unknown prompts into canonical purposes

## Scoring

Use `Tools/PurposeKnowledge/score_model_outputs.mjs` for model JSONL outputs.

Primary metrics:

- required purpose coverage
- forbidden purpose avoidance
- Goal coverage
- nearest shared purpose accuracy
- unknown/negation handling
- valid JSON rate
- hallucinated ref rate

Secondary metrics:

- confidence calibration
- repeat stability across 3 runs
- latency
- token count
- cost
- repair success after validator feedback

Recommended scorecard:

- `pass_rate`: exact fixture pass rate
- `coverage_recall`: required refs found / required refs
- `hallucination_rate`: invalid or unknown non-candidate refs / cases
- `overreach_rate`: forbidden refs or side-effect claims / cases
- `lca_accuracy`: matching nearest shared purpose / cases with LCA expectation
- `repair_delta`: pass rate after one validator repair minus first-pass pass rate

## Recurring Hallucination Gate

Use `purpose://test.acceptance.hallucination-evaluation` when the goal is not
to compare one model sweep, but to periodically ask whether HAVEN chat and
purpose grounding still avoid invented knowledge.

This gate should include:

- hallucinated `purpose://` refs, Goal refs, capabilities, keypaths, and source
  citations
- unsupported factual claims where the correct answer is source-backed,
  qualified as inference, or unknown
- stale-source prompts where the model must request/check fresh information
- adversarial prompts that ask the model to invent nonexistent cells or methods
- ambiguous prompts where candidate review is safer than false certainty

Recommended v0 guardrails:

- `hallucinatedRefRate <= 0.01`
- `unsupportedClaimRate <= 0.03`
- `unknownWhenUnsupportedRate >= 0.90`
- `citationIntegrityRate >= 0.95`
- `sideEffectViolations == 0`

Once the gate passes its target band repeatedly, treat later runs as a
non-regression Goal: changes that improve one metric should not be accepted if
they increase hallucinated refs, unsupported claims, or side-effect violations
past the guardrails.

## Frontier Consensus Use

Use frontier models to find weaknesses in the gold set:

- cases where all frontier models disagree with HAVEN
- cases where frontier models agree with each other but not the fixture
- cases where wording variants produce unstable outputs
- cases where the model proposes a plausible new purpose and Goal

Do not auto-accept these changes. Create `PurposeCandidate` records with evidence, nearest parent, confidence, and review state.

## Local Model Tuning

For smaller local models:

1. Start with open-taxonomy prompting.
2. Add retrieved top-K context from the deterministic resolver.
3. Keep output schema short and strict.
4. Prefer repair prompts over longer initial prompts when JSON validity is the main failure.
5. Tune instruction examples by error cluster:
   - missing child purposes
   - over-broad parent only
   - hallucinated purposeRef
   - wrong LCA
   - failure to mark unknown
   - side-effect confusion
6. Use the same score script after every prompt change.

Fine-tuning should wait until:

- the fixture set is at least 200 reviewed cases
- categories are balanced
- unknown/negative cases are at least 20 percent of the set
- frontier and deterministic disagreements have been reviewed
- prompt-only tuning has plateaued

## Run Metadata

Every benchmark run should store:

- date/time
- git commit or dirty-tree note
- fixture file hash
- KB and index hash
- model provider and exact model ID
- endpoint/runtime
- temperature/top_p/max tokens
- prompt mode
- prompt file hash
- output JSONL path
- score report path

This makes frontier comparisons useful for evaluating smaller local models later.
