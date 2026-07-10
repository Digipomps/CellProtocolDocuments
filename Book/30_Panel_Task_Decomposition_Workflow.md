# Chapter 30 - Panel Task Decomposition Workflow

Status: draft workflow contract, v0.

Last updated: 2026-07-04.

This chapter defines how a task given to the AI advisory panel is decomposed
with the two structures HAVEN already has: declared purposes with measurable
Goals (Chapters 09 and 23) and claim/argument structures (Chapter 29). The
goal is that panel work is finishable and auditable: intent is explicit,
assertions are structured, subtasks are deduced from evaluation gaps rather
than improvised, and "done" is a documented evaluation state.

Related sources:

- `Book/09_Purpose_Interests.md` — Purpose as declared intent, Goals
- `Book/23_Purpose_Knowledge_Base.md` — purpose taxonomy and guardrails
- `Book/27_Text_Reliability_Analysis.md` — adviser roles and evidence rules
- `Book/29_Claim_Argument_Model.md` — claim structures and evaluation
- `Deliverables/AI_Agent_Advisory_Panel_Report_Jorn_Erik_2026-06-15.md` —
  the panel as a working method
- `Prompts/Advisory_Panel_Task_Decomposition.md` — fill-in launch template
- Skill: `.claude/skills/haven-panel-task-decomposition/SKILL.md`

## 1. Why Both Structures

A panel task has two failure modes that map to two different missing
structures.

Without declared purpose and Goals, the panel produces plausible analysis
with no termination condition: nobody can say when the task is finished or
whether the outcome satisfied the intent. The Formål layer fixes this: intent
is declared ex ante, and each purpose carries a Goal with metric, target, and
a testable status.

Without claim structure, adviser output degrades into prose opinions that
cannot be compared, audited, or attacked precisely. The claim layer fixes
this: hypotheses, claims, and proposals from the user or advisers become
typed claim nodes with support, assumptions, qualifiers, and counterarguments
with explicit polarity.

The boundary between the layers is the Chapter 09/29 boundary: a purpose
declares intent, a claim asserts something about the world. Claims link to
the Formål they serve through `purposeRef`; testable claims link to a
GoalDefinition through `goalID`.

## 2. Workflow Contract

### Phase 1 - Formål

Declare 1-3 purposes for the task, anchored to existing `purpose://` nodes
where possible. Unknown intent resolves to `purpose://prompt.unknown` with
candidate intake; refs are never invented. Every purpose gets a
`haven.goal-definition.v1` Goal. An intent that cannot name an observable
Goal is returned to the task owner for sharpening before panel work starts.

### Phase 2 - Claim Ledger

Load-bearing hypotheses, claims, and proposals become
`haven.claim-definition.v0` nodes with claim type, strength, quote anchors
for extracted claims, and `isInferred` marking for panel-inferred premises.
Each root claim gets a composition: `allOf` linked premises, `anyOf`
alternatives, `atLeast` quorum, `countered` with `rebuts`/`undercuts`.

Where a claim leans on a recognizable inference type — expert opinion,
cause to effect, analogy, practical reasoning, argument from consequences —
attach an argumentation scheme (Book 29 section 6). Its critical questions
seed the gap set the skeptic and source auditor work through, so the panel
does not have to reinvent what a given kind of argument must survive.

### Phase 3 - Role Mandates

The Chapter 27 adviser roles get artifact responsibilities:

| Role | Produces |
| --- | --- |
| Text-internal analyst | normalized claim ledger |
| Source auditor | support records with honest audit statuses |
| Skeptic | counters as `rebuts`/`undercuts` compositions |
| Steelman/fairness reviewer | strengthened bases; strawman check on counters |
| Domain expert | domain evidence, surfaced hidden assumptions |
| Final adjudicator | Chapter 29 evaluations; conclusions from anchors only |

Surfaces keep their panel roles from the working method (Codex repo-grounded
implementation, Claude long-horizon critique, local models for deterministic
checks, and so on). The panel is not a voting machine; disagreement between
roles is signal.

### Phase 4 - Subtask Deduction Loop

Next work items are deduced from evaluation artifacts, not invented:

- Goal evaluation `missing`/`blockers` → evidence or unblocking subtasks
- Claim evaluation `missingClaimRefs`/`blockingReason` → source-audit or
  premise-support subtasks
- Contradicted root claims → revise proposal or log the drop decision
- New adviser proposals → new claims (back to Phase 2)
- Unexamined scheme critical questions (Book 29 section 6) → targeted
  subtasks; challenged critical questions → undercuts on the claim

Every subtask carries its parent `purposeRef` so all work traces to declared
intent. The loop repeats until every Goal is terminal (satisfied, missed,
blocked, cancelled) and every root claim is adjudicated or explicitly logged
open with reason and owner.

### Phase 5 - Handoff

A dated deliverable records: Formål block, goal table with final statuses,
claim graph summary, decision log, open items. The human task owner makes
the decisions; the panel makes assumptions, gaps, risk, and alternatives
visible.

## 3. Minimal Example

Task: "Should the DiMy investor-case MVP include the market module?"

Formål: `purpose://value-and-commons` (candidate), Goal: decision documented
with adjudicated claim basis within the sprint, status testable as
satisfied/blocked.

Root claim (normative, moderated): "The MVP should ship layers 1+2+7 without
the market module."

```json
{
  "type": "countered",
  "base": {
    "type": "allOf",
    "children": [
      { "type": "claim", "claimRef": "claim.mvp.cold-start-needs-founder-side" },
      { "type": "claim", "claimRef": "claim.mvp.market-module-needs-external-data" }
    ]
  },
  "counters": [
    {
      "role": "rebuts",
      "composition": { "type": "claim", "claimRef": "claim.mvp.investors-reject-caseless-numbers" }
    }
  ]
}
```

The source auditor grades the premises, the skeptic owns the rebuttal, the
adjudicator evaluates. If `claim.mvp.market-module-needs-external-data` comes
back `needs_external_source_audit`, the deduced subtask is that audit — not a
new round of opinions. When the root claim is adjudicated and the Goal is
satisfied, the task is done and the handoff records the decision.

## 4. Current Limitations

- This is a prompt/skill workflow contract. No runtime object orchestrates
  it; agents apply the JSON contracts manually and a human owns decisions.
- Goal and claim evaluation is computed by whoever holds the adjudicator
  role, following Chapter 29 and Chapter 09 semantics by hand or with local
  scripts. The Swift implementations in CellProtocol are the normative
  semantics but are not yet exposed as a Cell or CLI for panel use.
- Artifacts live as fenced JSON in notes and deliverables. RAG indexing,
  Perspective persistence, and signing are future work.
- The workflow does not replace `haven-claim-review` for public-facing
  claims or the payment/regulatory guardrails where those apply.
