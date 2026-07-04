# Advisory Panel Task Decomposition Prompt (Shared)

Fill-in template for launching a panel round with purpose+claim grounding.
Contract: `Book/30_Panel_Task_Decomposition_Workflow.md`. Structures:
`Book/23_Purpose_Knowledge_Base.md` (purposes/Goals),
`Book/29_Claim_Argument_Model.md` (claims), `Book/27_Text_Reliability_Analysis.md`
(roles, evidence rules). Keep this template thin; put project state in the
project's `Prompts/CurrentState.md`.

---

## Task

- Task: <one paragraph, concrete>
- Task owner (human decision-maker): <name>
- Source basis: <files, RAG cases, URLs the panel may use>
- Constraints: <deadlines, regulatory guardrails, scope limits>

## Formål

For each purpose (1-3):

- purposeRef: <existing purpose:// ref, or purpose://prompt.unknown + candidate note>
- Intent: <one sentence>
- Goal (haven.goal-definition.v1): metric, baseline, target, timeframe,
  evidence sources
- Done means: <observable state the loop can test>

## Initial Claim Ledger

For each load-bearing hypothesis/claim/proposal (from user or advisers):

- claimID, statement, claimType (factual/causal/normative/predictive/
  statistical/project_capability), strength (assertive/moderated/speculative)
- quote anchor if extracted from a text; isInferred if the panel inferred it
- purposeRef it serves; goalID if testable
- Known support/assumptions/qualifiers/counterarguments

Root claim compositions in Book 29 JSON (allOf/anyOf/atLeast/countered).

## Role Assignments

| Role | Surface/agent | Mandate |
| --- | --- | --- |
| Text-internal analyst | <e.g. Claude> | claim ledger |
| Source auditor | <e.g. Codex + web tooling> | support records, honest statuses |
| Skeptic | <surface> | rebuts/undercuts counters |
| Steelman/fairness | <surface> | strengthen bases, strawman check |
| Domain expert | <surface or human> | domain evidence |
| Final adjudicator | <surface> | Book 29 evaluations, conclusions from anchors |

## Loop Protocol

1. Evaluate goals and root claims after each round.
2. Deduce subtasks only from `missing`/`blockers`/`missingClaimRefs`/
   `blockingReason`/contradicted claims; tag each with parent purposeRef.
3. Stop when all Goals are terminal and all root claims adjudicated or
   logged open with reason and owner.

## Handoff

Dated deliverable in `Deliverables/` (or owning repo): Formål block, goal
table with statuses, claim graph summary, decision log, open items. Human
owner signs the decision.

## Boundaries

No invented purpose:// refs. Unaudited sources give no support. Claims about
the case, never scores on people. Analysis is side-effect-free; publishing is
a separate explicit action; public claims go through haven-claim-review.
