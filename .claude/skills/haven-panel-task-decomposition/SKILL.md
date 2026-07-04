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

On another machine, resolve the same repo-relative paths from the active
`CellProtocolDocuments` checkout.

## Workflow

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

### 4. Deduce subtasks and loop

Derive the next work items mechanically from the artifacts instead of
inventing them:

- Goal evaluation `missing`/`blockers` → evidence-gathering or unblocking
  subtasks
- Claim evaluation `missingClaimRefs`/`blockingReason` → source-audit or
  premise-support subtasks
- `contradicted` root claims → revise the proposal or record the decision to
  drop it
- New proposals from advisers → back to step 2 as new claims

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

- Every declared purpose has a testable Goal with a final terminal status.
- Every root claim has an adjudicated evaluation or a logged open-item entry.
- Counterarguments were sought (skeptic ran), not just accumulated support.
- Source-audit statuses are honest; nothing unaudited counts as support.
- The handoff deliverable exists, is dated, and names the human decision.
