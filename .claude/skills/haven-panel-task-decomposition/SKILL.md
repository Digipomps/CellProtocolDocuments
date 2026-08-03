---
name: haven-panel-task-decomposition
description: Use when giving the HAVEN AI advisory panel (rådgiverpanelet) a task, or when any nontrivial HAVEN/DiMy task needs purpose+goal grounding and claim/argument analysis before work starts. Decomposes a task into declared purposes (Formål) with measurable Goals, expresses hypotheses, claims, and proposals from the user or advisers as claim structures with support and counterarguments, deduces subtasks from missing evidence and unsatisfied goals, and loops until every goal is terminal and every root claim is adjudicated. Trigger on phrases like "gi panelet denne oppgaven", "sett opp rådgiverpanelet", "dekomponer oppgaven", "analyser hypotesene/forslagene", "jobb gjennom til det er ferdig", or when a task produces competing proposals that need structured adjudication.
---

# HAVEN Panel Task Decomposition

Use this skill to turn a task for the AI advisory panel into a purpose-grounded,
claim-grounded workflow that runs until the job is verifiably done — not until
the conversation fizzles out.

The advisory panel is a working method, not a runtime object: the same problem
goes to several AI surfaces with distinct roles and controlled context, and the
human owns the decision. This skill adds the two structures that make panel
output composable and finishable: declared purposes with measurable Goals
(what "done" means) and claim structures (what is actually being asserted, by
whom, on what evidence).

## Canonical Sources

Read before deviating; these define the contracts this skill applies:

- `CellProtocolDocuments/Book/30_Panel_Task_Decomposition_Workflow.md` — the
  workflow contract this skill operationalizes
- `CellProtocolDocuments/Book/29_Claim_Argument_Model.md` — claim structures,
  composition polarity, graded evaluation semantics
- `CellProtocolDocuments/Book/23_Purpose_Knowledge_Base.md` — purpose taxonomy,
  "Goals must be achievable", hallucination guardrails
- `CellProtocolDocuments/Book/27_Text_Reliability_Analysis.md` — adviser roles,
  source-audit statuses, evidence conservatism
- `CellProtocolDocuments/Prompts/Advisory_Panel_Task_Decomposition.md` — the
  fill-in prompt template for launching a panel round
- `CellProtocolDocuments/Deliverables/Panel_Brief_Integrity_Finding_2026-08-02.md`
  — brief-integrity finding with its falsification test

On another machine, resolve the same repo-relative paths from the active
`CellProtocolDocuments` checkout.

## Workflow

### 0. Audit the brief before you fan it out

The shared brief is a load-bearing artifact with its own audit status. Its
facts are premises for *every* claim in the ledger, so an error there
propagates to the whole panel at once — measured 2026-08-02: one wrong fact in
a brief reached five of six panelists and was caught by none of them.

Before fan-out:

- Give every factual assertion in the brief the same audit status you would
  give a claim: `retrieved` (named source you actually fetched), `recalled`
  (from memory — carries no weight and must be labelled), `unavailable`,
  `contradicted`. Timestamp anything time-sensitive.
- **Never declare the brief authoritative.** Fairness rules (deadline
  discipline, scope limits, no-strawman rules) are binding as *rules*. The
  *facts* are not. Language like "these timestamps are binding" measurably
  suppresses objections panelists would otherwise raise.
- State known conflicts between sources inside the brief rather than
  resolving them silently. A declared conflict is data the panel can use.

Then require a brief audit as the first thing every panelist returns — see
step 3. Both controls are needed and neither is sufficient: the mandate
catches internal inconsistency, undated and unsourced assertions, and
conflated concepts, but it cannot catch a wrong fact that is internally
coherent. Those stay the briefer's responsibility, and retrieval is the only
control that finds them.

### 1. Declare Formål (intent) with measurable Goals

State 1–3 purposes for the task. Anchor each to an existing `purpose://` node
from the Book 23 taxonomy when one fits; when none fits, use
`purpose://prompt.unknown` and record a candidate — never invent a purposeRef.

Give every purpose a Goal in `haven.goal-definition.v1` shape: metric,
baseline, target, timeframe, evidence sources, and a status the loop can test
(satisfied, at-risk, missed, blocked, unknown). The practical rule from the
purpose knowledge base applies to tasks too: an intent that cannot name an
observable Goal is not ready to be worked on. Push back and sharpen it with
the task owner first.

### 2. Build the claim ledger

Express every load-bearing hypothesis, claim, and proposal — from the user and
from advisers — as `haven.claim-definition.v0` nodes: claim type (factual,
causal, normative, predictive, statistical, project_capability), strength
(assertive, moderated, speculative), quote anchor when extracted from a text,
`isInferred=true` for premises the panel infers rather than the author states.

Compose per root claim: `allOf` for linked premises, `anyOf` for independent
alternatives, `atLeast` for quorum support, `countered` with `rebuts`
(claims it is false) or `undercuts` (claims the support does not establish it).
Attach support nodes: evidence, assumption, qualifier, counterargument.

Keep the purpose/claim boundary clean: a purpose declares intent, a claim
asserts something about the world. Link claims to the Formål they serve via
`purposeRef`, and make testable claims point at a Goal via `goalID`.

For claims that lean on a recognizable inference type — expert opinion,
cause to effect, analogy, practical reasoning, argument from consequences —
attach an argumentation scheme (`haven.claim-scheme.v0`, Book 29 section 6).
The scheme's critical questions are the specific things that kind of argument
must survive; unexamined ones become deduced subtasks, challenged ones become
undercuts. This is how the panel avoids reinventing, per case, what makes a
given argument weak.

Gate the scheme layer (panel-tested 2026-07-11): a capable analyst on a
well-documented case reproduces most critical questions unaided, so do not
instantiate schemes on claims already fully adjudicated — use them where a
critical question is expected to be challenged or genuinely unexamined, when
the analyst is a weaker model, when the argument type is unfamiliar, or when
coverage must be demonstrable (governance/audit). Triage every critical
question to answered/not-applicable before running subtask deduction, so the
loop never emits already-answerable work. Treat the completeness ratio as
bookkeeping, never as measured argument quality.

### 3. Assign panel roles against the structures

Map the Book 27 adviser roles onto concrete artifact responsibilities:

- text-internal analyst: extract and normalize the claim ledger
- source auditor: produce support records with honest audit statuses;
  unaudited or missing sources give no support — never claim support that
  has not been checked
- skeptic: contribute counters as `rebuts`/`undercuts` compositions, not
  loose objections
- steelman/fairness reviewer: strengthen base compositions and verify
  counters attack the real argument, not a strawman
- domain expert: supply domain evidence and surface hidden assumptions
- final adjudicator: evaluate compositions with the Book 29 semantics and
  conclude only from quote anchors, source anchors, and marked inferences

Different AI surfaces take different roles (Codex repo-grounded, Claude
long-horizon critique, local models for deterministic checks, and so on).
The panel is not a voting machine — disagreement between roles is signal,
not noise to average away.

**Every panelist opens with a brief audit.** Before its role output, each one
returns a `## Brief audit` section: either "no objections" after actually
looking, or a numbered list of what it believes is wrong or suspect in the
brief, what made it doubt, and what would settle the question. Say plainly
that a finding here outranks a finding about the subject matter, because a
brief error propagates to everyone. Without this mandate the observed
detection rate is zero; with it, panelists find real defects the briefer
missed.

**Run two adjudicators, and hand the second an explicit challenge.** Give
adjudicator B the single hardest verdict adjudicator A reached, stated as a
challenge with the counter-argument spelled out, and require an explicit
ruling on it. A panel configured to critique drifts toward convicting its
object — the roles that generate pressure (skeptic, source auditor) have no
counterweight when the object is a third party rather than the commissioner.
The challenge is what surfaces that drift; in the 2026-08-02 run it overturned
two findings that were harsher than the evidence bore.

### 4. Deduce subtasks and loop

Derive the next work items mechanically from the artifacts instead of
inventing them:

- Goal evaluation `missing`/`blockers` → evidence-gathering or unblocking
  subtasks
- Claim evaluation `missingClaimRefs`/`blockingReason` → source-audit or
  premise-support subtasks
- Scheme evaluation: unexamined critical questions → targeted subtasks;
  challenged critical questions → undercuts on the claim
- `contradicted` root claims → revise the proposal or record the decision to
  drop it
- New proposals from advisers → back to step 2 as new claims
- **Any brief fact that retrieval overturns → a correction round, not a
  patch.** Hand the adjudicators the corrected facts, all prior-round output,
  and an explicit mandate to discard or invert their own findings that rested
  on the error. Name which panelist and which finding falls, stands, or flips.
  Quietly editing the brief and moving on leaves contaminated conclusions in
  the ledger.

Give each subtask the parent `purposeRef` so every piece of work traces to a
declared intent. Repeat evaluation after each round.

Stop when, and only when: every Goal is in a terminal state (satisfied,
missed, blocked, cancelled) and every root claim is adjudicated (supported or
contradicted) or explicitly logged as open with a reason and an owner. "Done"
is a documented evaluation state, not a feeling.

### 5. Hand off

Write a dated deliverable (in `CellProtocolDocuments/Deliverables/` for
HAVEN-wide work, or the owning repo) containing: the Formål block, the goal
table with final statuses, the claim graph summary, the decision log, and open
items. The human task owner signs off on decisions; the panel makes
assumptions, gaps, risk, and alternatives visible — it does not decide.

## Report Quality Metrics

Quality is a measured property of the report, not a feeling about it. Publish
these with the deliverable so a reader can audit the analysis without redoing
it. All ten are observable from the artifact itself.

**The metrics are diagnostics, never targets.** Optimizing a ratio produces a
report that scores well and reasons badly (Goodhart). Report the number and the
evidence that produced it; never manufacture a counter-finding to move a ratio.

| # | Metric | Definition | Healthy signal |
|---|---|---|---|
| Q1 | Position-change traceability | Position changes citing the specific evidence that caused them / all position changes | 100 % — an untraced change is social compliance, not analysis |
| Q2 | Mixed-ledger ratio | Adjudications against whatever the commissioning framing rewards / total | Determined by evidence. **No target value.** Find the reward direction first: when the object is the commissioner, the failure is deference; when the object is a third party the panel was convened to critique, the failure is harshness, and a 100 % conviction rate is the tell |
| Q3 | Audit-status honesty | Load-bearing claims with a named retrieved source / all load-bearing claims | Recalled-from-memory is never "audited"; unaudited gives no support |
| Q4 | Narrative independence | Findings that hold under every party's framing / all headline findings | Headline findings should pass; frame-dependent ones get marked as such |
| Q5 | Falsifiability audit | Claims structured so both confirmation and disconfirmation support them | Zero unflagged. Name the structure when it appears, including in the commissioner's own framing |
| Q6 | Natural-experiment identification | Counterfactuals checked against a real instance where they ran | Every counterfactual gets the check before it gets a probability |
| Q7 | Revealed-preference test | Actor claims compared against actor behaviour | Applied to every stated motive |
| Q8 | Terminal adjudication rate | Claims closed or logged open-with-owner / all claims | 100 %. Silent open claims are the failure mode |
| Q9 | Steelman sourcing | Steelmen drawn from sources that argue the opposite of the panel's lean | Self-authored steelmen are weak evidence |
| Q10 | Concession asymmetry | Concessions made without a new evidence anchor | Zero. This is the direct sycophancy probe |

### Which methodology actually raised quality (panel-tested 2026-08-01)

Measured across a long adversarial analysis round, the return per unit of
effort was strongly uneven:

- **Highest return — Q6, natural-experiment identification.** Asking "did this
  counterfactual ever actually run?" overturned the round's strongest finding
  in four retrievals. Run this *before* assigning probability bands to any
  counterfactual; a scenario that has already been tried has evidence, not odds.
- **Second — audit-before-close (Q3).** A claim held open specifically because
  it rested on recall could only be closed after retrieval, and the retrieval
  reversed its direction. Never close a load-bearing claim from memory.
- **Third — opposing-source steelmen (Q9).** Sourcing a proposal's best defence
  from an author who argues *for* it, then testing that, is far stronger than
  self-authored steelmanning.
- **Lowest return — option generation.** Additional alternatives past the first
  batch did not improve the report; adversarial testing of existing ones did.
  When a task owner asks for more ideas until a conclusion is reached, generate
  the batch, then shift effort to testing and say plainly that testing, not
  volume, is what moved the result.

Corollary for the loop in step 4: prefer subtasks that could **falsify** a
standing finding over subtasks that would extend coverage. Rank deduced
subtasks by how much a negative result would change the report.

### Brief integrity (panel-tested 2026-08-02)

A brief written for a six-model fan-out contained one wrong fact. All six
panelists used it; none objected. Retrieval caught it afterwards, and the
correction round overturned or reclassified findings from five of the six.

The tempting conclusion — that fan-out structurally cannot detect briefer
error, because the error is in the shared input rather than in any model —
was tested and came back **too strong**. Three models were re-run on the same
faulty brief with an explicit mandate to audit it:

| Arm | Brief declared binding | Audit mandate | Objected |
|---|---|---|---|
| A | yes | no | **0 / 6** |
| B | no | yes | **3 / 3** |
| C | yes | yes | **2 / 3** |

So the blind spot is mostly **instructional, not architectural**. What the
mandate buys is real but bounded:

- It found two genuine defects the briefer had missed — a figure placed on the
  timeline without a timestamp, and three distinct legal actions conflated
  into one term. Both later proved load-bearing.
- It did **not** find the actual wrong fact. That one was internally coherent
  and concerned events too recent for training data. Internally coherent
  factual error is findable only by retrieval, and stays the briefer's
  responsibility no matter how the panel is instructed.
- Declaring the brief authoritative suppresses objections: the model that
  answered "no objections" under binding framing was the one that caught the
  most valuable defect when unbound. Direction consistent, effect size not
  established (n = 3 per arm).

Practical rule: bind the panel to *rules*, never to *facts*. And when a finding
looks like it follows from architecture alone, that is exactly when to run the
arm that could falsify it — this one did.

The guards this produced — step 0 brief audit, the mandatory `## Brief audit`
return, the never-authoritative brief, the correction round, the challenged
second adjudicator, and the Q2 restatement — are **standing policy (D2,
decided 2026-08-02 by Kjetil)**, alongside the 2026-07-11 scheme guards. The
decision covers the guards, not the open questions: the effect size of binding
language is still unmeasured, so apply the rule on the finding's direction and
do not cite a strength for it.

Full evidence: `Deliverables/Panel_Brief_Integrity_Finding_2026-08-02.md`.

## Boundaries

- Do not invent `purpose://` refs, capabilities, keypaths, or citations;
  unknown intent goes to `purpose://prompt.unknown` with candidate intake.
- Apply the Book 29 evaluation semantics as written (weakest link for
  `allOf`, contradicted premise makes a parent unsupported not contradicted,
  dominant rebuttal contradicts, undercut discounts). Do not eyeball scores.
- Do not use the weighted Perspective graph for argument evaluation; it is a
  discovery/matching surface.
- Analysis artifacts are side-effect-free. Publishing results into entities,
  RAG, or public claims is a separate explicit action, and public-facing
  claims also go through `haven-claim-review`.
- Claims are about the case, never scores on people. No ranking of persons,
  no global reputation — the anti-gapestokk principle applies.
- Keep JSON artifacts schema-valid against the Book 23/27/29 contracts so a
  later runtime or validator can consume them unchanged.

## Completion Checklist

- The brief was audited before fan-out, its facts carry audit statuses, and it
  was never declared authoritative.
- Every panelist returned a brief audit, and anything it raised was resolved
  or logged.
- Any brief error found mid-run triggered a correction round that named which
  findings fell, stood, or flipped.
- Every declared purpose has a testable Goal with a final terminal status.
- Every root claim has an adjudicated evaluation or a logged open-item entry.
- Counterarguments were sought (skeptic ran), not just accumulated support.
- Source-audit statuses are honest; nothing unaudited counts as support.
- Every counterfactual was checked for a real instance where it ran (Q6).
- The Q1–Q10 metric block is published with the deliverable, with values and
  the evidence behind them — not asserted as a grade.
- The handoff deliverable exists, is dated, and names the human decision.
