# Chapter 14 — Perspective Runtime Matching (Phase 0 + 1)

This chapter documents implemented runtime behavior for `Perspective`,
`PerspectiveCell`, and weighted matching in CellProtocol.

Scope:

- Phase 0: correctness fixes needed for deterministic matching and decoding
- Phase 1: stable query/matching API exposed through `GeneralCell` intercepts
- cross-runtime reference portability (`portableRefs-v1`)

## 1. Runtime intent

Chapter 09 defines conceptual semantics for `Purpose` and `Interest`.
This chapter defines the concrete request/response contract applications can use
through `Meddle.get/set`.

## 2. Implemented Phase 0 fixes

### 2.1 `Signal` collector persistence

`Signal.init(...)` now assigns `collector`, enabling `hit(...)` to record matched refs.

### 2.2 Typed reference lookup in `Weight<T>`

`Weight.node` resolves by node type:

- `Interest` -> `findInterestByReference`
- `Purpose` -> `findPurposeByReference`
- `EntityRepresentation` -> `findENtityRepresentationByReference`

Decoder `userInfo["context"]` is restored into `Weight.context`.

### 2.3 Facilitator compatibility keys

Encoding/decoding supports both:

- `entityRepresentationsFacilitator` (canonical)
- `entityFacilitator` (legacy alias)

### 2.4 `Interest.entities` decode/encode type fix

`Interest.entities` is decoded/encoded as `[Weight<EntityRepresentation>]`.

### 2.5 `Perspective.addInterest(...)` index fix

`interestNameReferences` is now updated correctly.

### 2.6 `Perspective.updateEntityRepresentation(...)` target fix

Entity updates now target entity refs and entity-typed relations.

### 2.7 Active set query/upsert support in `Perspective`

Implemented helpers:

- `getActivePurposes(minWeight:limit:)`
- `getActiveInterests(minWeight:limit:)`
- `getActiveEntities(minWeight:limit:)`
- `upsertActivePurpose(...)`
- `upsertActiveInterest(...)`

### 2.8 `EntityRepresentation.agreementRefs` for cross-scaffold agreement discovery

`EntityRepresentation` now has canonical support for:

- `agreementRefs: [AgreementReference]`

`AgreementReference` is intentionally lightweight. It is the stable bridge from
an entity representation to a separate signed-agreement store.

Recommended fields:

- `id`
- `label`
- `counterparty`
- `purpose`
- `dataPointer`
- `recordState`
- `savedAt`
- `savedAtText`
- `recordKeypath`
- `sourceEntityKeypath`

Design rule:

- keep full signed agreements outside `EntityRepresentation`
- expose only lightweight references in `EntityRepresentation.agreementRefs`
- let applications resolve the full record through `recordKeypath`

This keeps social/entity context light while still allowing deterministic lookup
of the agreement that explains why access exists.

### 2.9 Canonical signed-agreement entity projection

CellProtocol now includes:

- `SignedAgreementRecord`
- `SignedAgreementEntity`

`SignedAgreementEntity` is the canonical "full record" side of the model.

Recommended projection pattern:

1. Store the full signed agreement as `SignedAgreementRecord` in a dedicated
   signed-agreement entity.
2. Derive lightweight `AgreementReference`s from that entity.
3. Copy those refs into `EntityRepresentation.agreementRefs`.

This produces a stable two-layer model:

- full audit/history in the signed-agreement entity
- lightweight relationship/navigation data in `EntityRepresentation`

## 3. Implemented Phase 1 API in `PerspectiveCell`

All external behavior is exposed via intercepts.

### 3.1 GET keys

- `advertisedPurpose`
- `activePurpose` (legacy convenience snapshot)
- `perspective.state`

### 3.2 SET keys

- `addPurpose` (upsert one or more active purposes, then persist)
- `matchPurpose` (legacy alias for matching query)
- `perspective.query.activePurposes`
- `perspective.query.interestsFromActivePurposes`
- `perspective.query.match`

## 4. Query contracts

## 4.1 `perspective.query.activePurposes`

Request fields:

- `minPurposeWeight: Double` (default `0.0`)
- `limit: Int` (default `50`)
- `includeInterests: Bool` (default `true`)
- `referenceMode: "local" | "portable" | "both"` (default `"both"`)

Response fields:

- `purposes: [Object]`
- `count: Int`
- `minPurposeWeight: Double`
- `referenceMode: String`
- `referenceStrategy: "portableRefs-v1"`

Purpose item fields:

- `purposeName`
- `purposeWeight`
- refs by `referenceMode`:
  - `purposeRef` (local)
  - `portablePurposeRef` (portable)
- optional `interests` list with weighted interest entries

## 4.2 `perspective.query.interestsFromActivePurposes`

Request fields:

- `minPurposeWeight: Double`
- `minInterestWeight: Double`
- `limit: Int`
- `referenceMode`

Response fields:

- `interests: [Object]`
- `count`
- thresholds (`minPurposeWeight`, `minInterestWeight`)
- `referenceMode`
- `referenceStrategy: "portableRefs-v1"`

Aggregated interest weight:

- per active purpose/interest edge: `combinedWeight = purposeWeight * interestWeight`
- per interest key: keep max `combinedWeight`

Each interest includes `supportingPurposes` with weights for explainability.

## 4.3 `perspective.query.match`

Request fields:

- `minPurposeWeight: Double`
- `minInterestWeight: Double`
- `minMatchScore: Double`
- `limit: Int`
- `allowViaInterests: Bool`
- `referenceMode`
- target list accepted via:
  - `targetPurposes`
  - `targetActivePurposes`
  - `targetPerspective.purposes`
  - `targetPerspective.activePurposes`

Response fields:

- `directPurposeHits`
- `viaInterestHits`
- `allHits`
- `count`
- `referenceMode`
- `referenceStrategy: "portableRefs-v1"`

Scoring:

- direct route: `min(sourcePurposeWeight, targetPurposeWeight)`
- via-interest route:
  `min(sourcePurposeWeight, targetPurposeWeight) * min(sourceInterestWeight, targetInterestWeight)`

## 5. Cross-runtime references (`portableRefs-v1`)

Local refs are often runtime-local and may differ across devices/scaffolds.
To match between local and remote Perspectives, API responses can include:

- `portablePurposeRef` (`purpose://<slug>`)
- `portableInterestRef` (`interest://<slug>`)

Slug strategy (current implementation):

- if ref has `scheme://value`, slugify `value`
- otherwise slugify node name
- lowercase + ASCII-like normalized tokens

This allows deterministic matching even when local reference namespaces differ.

## 6. Local -> remote interoperability pattern

1. Local runtime calls `perspective.query.activePurposes` with `referenceMode = "both"`.
2. Local runtime sends returned purpose payload to remote runtime.
3. Remote runtime calls `perspective.query.match` with `targetPurposes` set to payload.
4. Remote runtime returns weighted hits (`directPurposeHits`, `viaInterestHits`).

## 7. GeneralCell implementation rules

For `GeneralCell` subclasses exposing Perspective behavior:

- use intercepts only (`addInterceptForGet` / `addInterceptForSet`)
- keep payloads explicit (`ValueType.object`, numeric weights, named route)
- keep scoring deterministic and explainable
- include refs + weights needed for downstream matching/ranking

## 8. Not yet included (Phase 2+)

The following are intentionally out of Phase 1 and should be treated as next steps:

- queue-based signal propagation runtime using TTL/hops
- multi-hop signal aggregation as first-class response type
- credibility/evidence blending from `EntityRepresentation` social context
