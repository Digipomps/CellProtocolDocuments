# Chapter 29 - Claim Argument Model

Status: implemented v0 runtime model, draft chapter.

Last verified against code: 2026-07-03.

This chapter documents the runtime model for representing claims (påstander)
and the argument structure that supports or attacks them. It is the layer-1
data model for argument-graph tooling such as the DiMy investor-case artifact
and future claim-review workflows.

Implementation:

- `CellProtocol/Sources/CellBase/PurposeAndInterest/ClaimDefinition.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/ClaimComposition.swift`

Contract tests:

- `CellProtocol/Tests/CellBaseTests/ClaimDefinitionTests.swift`
- `CellProtocol/Tests/CellBaseTests/ClaimCompositionTests.swift`

## 1. Design Position

Claims are a sibling model family next to Purpose, Interest, and Goal — not a
new meaning bolted onto `Purpose`. Chapter 09 defines Purpose as declared
intent; a claim is an assertion about the world, so it gets its own
schema-versioned structures.

The model deliberately reuses proven patterns from the Purpose family:

- recursive composition follows the `PurposeComposition` shape
  (`allOf`/`anyOf`/`atLeast`), extended with argument polarity;
- testability reuses `GoalDefinition`/`GoalEvaluation` through an optional
  `goalID` link (metric, baseline, target, evidence sources);
- declared intent (`Formål`) needs no new structure: it is a `Purpose` plus a
  `GoalDefinition`, and claims can point to it through `purposeRef`.

Boundary rule: argument validity is evaluated by `ClaimComposition.evaluate`,
which is deterministic and pure. The `WeightedGraphRuntime` remains a
discovery/matching surface (Chapter 14) and must not be used to score
arguments.

## 2. Shared Vocabulary With Chapter 27

Raw wire values are identical to the text reliability analysis contract
(`Book/27_Text_Reliability_Analysis.md`), so extracted claim ledgers and
authored claim artifacts can exchange data without translation:

- `ClaimType`: `factual`, `causal`, `normative`, `predictive`, `statistical`,
  `project_capability`
- `ClaimStrength`: `assertive`, `moderated`, `speculative`
- `ClaimSourceAuditStatus`: `supported`, `partly_supported`, `contradicted`,
  `source_missing`, `not_found`, `not_checkable`, `text_only_not_audited`,
  `needs_external_source_audit`, `source_cue_without_anchor`

`ClaimDefinitionTests.testWireVocabularyMatchesTextReliabilityContract` locks
these values.

## 3. Structures

### 3.1 `ClaimDefinition` (`haven.claim-definition.v0`)

The atomic claim node:

- `claimID`, `statement`, `claimType`, `strength`
- `quote` — exact quote anchor when extracted from a source text (Chapter 27
  audit-anchor rule); authored claims may leave it nil
- `isInferred` — inferred warrants must be marked, never presented as author
  claims
- `sourceRefs`
- `purposeRef` — optional link to the declared Purpose (Formål) the claim
  belongs to
- `goalID` — optional link to a `GoalDefinition` that makes the claim testable
- `supports` — attached support nodes
- `composition` — optional `ClaimComposition` describing how sub-claims
  establish this claim
- `tags`

### 3.2 `ClaimSupportNode`

Support-node kinds mirror the argument-graph layer-1 node types (Norwegian
terms in parentheses): `evidence` (evidens), `assumption` (antakelse),
`qualifier` (kvalifikator), `counterargument` (motargument). Each node carries
`statement`, `sourceRefs`, `sourceAuditStatus`, and optional `confidence` in
`[0, 1]`.

### 3.3 `ClaimComposition`

Recursive expression with a `type` discriminator on the wire:

- `claim` — leaf reference (`claimRef`, optional `name`)
- `allOf` — linked premises; weakest link decides the score
- `anyOf` — convergent support; strongest alternative decides the score
- `atLeast` — quorum support (`requiredCount`, `children`)
- `countered` — a support expression under attack (`base`, `counters`)

Each `ClaimCounter` has a `role`:

- `rebuts` — argues the claim itself is false
- `undercuts` — argues the support does not establish the claim

Example wire shape:

```json
{
  "type": "countered",
  "base": {
    "type": "allOf",
    "children": [
      { "type": "claim", "claimRef": "claim.market.segment-size" },
      { "type": "claim", "claimRef": "claim.market.price-point" }
    ]
  },
  "counters": [
    {
      "role": "rebuts",
      "composition": { "type": "claim", "claimRef": "claim.market.competitor-pricing" }
    }
  ]
}
```

## 4. Evaluation Semantics

`ClaimComposition.evaluate(in:)` takes a `ClaimCompositionEvaluationContext`
(`evaluatedAt`, `supportRecords`, `scorePolicy`) and returns a
`ClaimCompositionEvaluation` with `status`, `score` in `[0, 1]`, ref ledgers
(`supportedClaimRefs`, `contradictedClaimRefs`, `missingClaimRefs`),
`childResults`, and blocking info.

Leaf evaluation is graded, not binary:

- the newest `ClaimSupportRecord` with `checkedAt <= evaluatedAt` wins;
- `score = scorePolicy.score(for: sourceAuditStatus) * confidence`;
- the default `ClaimScorePolicy.conservative` gives `supported = 1.0`,
  `partly_supported = 0.5`, and everything unaudited, missing, or contradicted
  `0.0`. This enforces the Chapter 27 acceptance criterion that source support
  is not claimed unless a source-auditor step has checked it.

Statuses: `supported`, `partial`, `unsupported`, `contradicted`.

Composition rules:

- `allOf`: score is the minimum child score. A contradicted premise makes the
  parent `unsupported` with `blockingReason = "premiseContradicted"` — denying
  a premise does not prove the negated conclusion.
- `anyOf`: score is the maximum child score.
- `atLeast(k)`: score is the mean of the top `k` child scores.
- `countered`: `effective = max(0, base - maxRebutScore) * (1 - maxUndercutScore)`.
  A rebuttal at least as strong as the base support makes the claim
  `contradicted` (`rebuttalDominates`). Undercutting can eliminate support but
  never contradicts the claim itself.

Counter evaluations appear in `childResults` after the base result, but their
supported/missing ledgers are not merged into the parent: a claim that
supports a counterargument does not support the countered claim.

Determinism: evaluation is a pure function of the composition and the context.
Same inputs plus same records give the same result; the contract tests assert
this.

## 5. Relationship To Purpose, Goal, And Attestation

- A declared `Formål` is a `Purpose` with a `GoalDefinition`; its feasibility
  case is a claim tree whose root `ClaimDefinition.purposeRef` points at the
  purpose.
- A testable atomic claim links a `GoalDefinition` via `goalID`; a
  `GoalEvaluation` (Chapter 09 / `GoalDefinition.swift`) can then feed a
  `ClaimSupportRecord` for that claim.
- Endorsement-style attestations (Chapter 09, section 5) map onto support
  records produced by third parties; the claim model itself stays
  signature-agnostic and leaves signing/versioning to the identity layer.

## 6. Current Limitations

- No Cell surface yet: there is no ClaimCell, no Explore contract, and no
  skeleton rendering for claim graphs. The model is CellBase-only.
- Claims are not wired into `Perspective` persistence; storage and retrieval
  are the caller's responsibility.
- `partial` leaves appear in neither `supportedClaimRefs` nor
  `missingClaimRefs`; detail lives in `childResults`.
- Score aggregation is a fixed v0 policy (min/max/top-k mean, subtractive
  rebut, multiplicative undercut). Alternative aggregation needs a schema
  revision, not silent behavior change.
- No signing, versioning, or non-repudiation; that belongs to the identity /
  agreements layer when claim artifacts become shareable.
- `ClaimSupportRecord` production is manual or tool-driven; there is no
  automatic bridge from the Chapter 27 reference tool yet.
