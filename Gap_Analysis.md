# CellProtocol Documentation Gap Analysis

This report compares the existing conceptual documentation in `CellProtocolDocuments/Book` to the actual Swift implementation in `CellProtocol`. It identifies gaps that prevent developers and code agents from implementing cells and skeleton-based UIs reliably.

## 1) Coverage Summary (Updated)

The conceptual book covers the major areas and now distinguishes design intent
from implementation evidence:

- Protocol intent, conditional invariants, and evidence boundaries are documented.
- Core interfaces, identity, agreements, flows, resolver, scaffold, transport, and purpose are explained.

Previously missing **implementation-level guidance** and **agent instructions** have now been added. The docs now connect concepts to Swift APIs, runtime defaults, and serialization formats, and include a runnable Quickstart and Skeleton spec.

## 2) Developer-Facing Documentation Status

### 2.1 Quickstart / "Hello Cell" — Addressed
Now covered in:
- `CellProtocolDocuments/Book/10_Quickstart.md`

Relevant code:
- `CellProtocol/Sources/CellBase/Cells/CellBase.swift`
- `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/AppInitializer.swift`
- `CellProtocol/Sources/CellApple/IdentityVault.swift`

### 2.2 "How to implement a Cell" — Addressed
Now covered in:
- `CellProtocolDocuments/Book/11_Developer_Guide_Cell.md`

Relevant code:
- `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`
- `CellProtocol/Sources/CellBase/Protocols/CellProtocol.swift`
- `CellProtocol/Sources/CellBase/Agreement/Agreement.swift`
- `CellProtocol/Sources/CellBase/Agreement/ConnectContext.swift`

### 2.3 Skeleton UI specification — Addressed
Now covered in:
- `CellProtocolDocuments/Book/12_Skeleton_Spec.md`

Relevant code:
- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonElementView.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonDescriptions.swift`

## 3) Agent Instructions — Addressed

Agent workflow is now defined in:
- `CellProtocolDocuments/Book/13_Agent_Instructions.md`

## 4) Conceptual Documentation Gaps (Remaining)

The core concepts are covered, but still missing:

- A stable “developer API map” listing the key types and modules.
- Full production coverage for machine-readable Explore contracts. Phase 1 is
  now documented in `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`, with
  audit and skeleton validation tools under `Tools/Explore/`, but legacy cells
  still need backfilled explicit `registerExploreContract(...)` entries.
- Integration patterns between `CellApple` and `CellVapor` (mobile vs server scaffolds).
- A consolidated runtime lifecycle diagram (init → resolve → usage → persistence).
- A machine-readable support matrix showing which concrete Cells/runtimes
  implement and test deterministic execution, durable ordered history, exact
  replay, process restart, remote acknowledgement, and fault containment.
- A resolver-boundary map that distinguishes protected resolver/`GeneralCell`
  entry points from internal direct calls and records the accepted authority
  path (owner proof, Contract/Grant, or cell-specific policy) for each public
  surface.

## 5) Specific Correctness/Interoperability Issues (Status)

- **Object wrapper mismatch** — Resolved in code and documented in Skeleton spec.  
  `SkeletonObject` now decodes wrapped and unwrapped forms, and encodes wrapped.  
  Code: `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

- **Legacy key spelling (`flowELementSkeleton`)** — Standardized to `flowElementSkeleton` in code and docs.  
  Backward compatibility is not required at this time.  
  Code: `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

- **README references docs not present in the code repo** — Addressed by updated README that points to `CellProtocolDocuments`.

- **Permission strings exposed four positions but implemented only `rwx`** —
  Resolved 2026-07-13. `Permission` now implements canonical `rwxs`, preserves
  the existing integer bits for legacy persisted data, adds Storage as an
  independent bit, emits four-character strings, and decodes legacy three- and
  six-character input without inferring Storage. Chapter 04 documents that
  Storage is retention evidence rather than copy prevention or forwarding
  authority.

## 6) Delivered Additions

The gaps were closed with these additions:

1. Quickstart (runnable setup + tests).  
2. Developer Guide (cell implementation workflow).  
3. Skeleton Spec (JSON encoding + examples).  
4. Agent Instructions (repeatable workflow).  
5. Troubleshooting (Xcode testplan + skeleton issues).

Files:
- `CellProtocolDocuments/Book/10_Quickstart.md`
- `CellProtocolDocuments/Book/11_Developer_Guide_Cell.md`
- `CellProtocolDocuments/Book/12_Skeleton_Spec.md`
- `CellProtocolDocuments/Book/13_Agent_Instructions.md`

## 7) Scaffold administrator and delegation — bounded status <a id="scaffold-admin-delegering"></a>

Last verified against code: 2026-09-09 — CellScaffold branch
`pdd/scaffold-admin-delegering`, worktree `CellScaffold/_wt-sad-20260909`.
Sources: `Sources/App/Cells/Admin/ScaffoldAdministratorRegistryCell.swift`,
`ScaffoldMandateCell.swift`, `ScaffoldMandateProofSupport.swift` and
`Sources/App/Cells/Arendalsuka/ArendalsukaConfigurationPublisherCell.swift`
within that worktree. This is source inspection reconciled with existing
[test evidence](Deliverables/PDD_scaffold-admin-delegering_2026-09-08/TESTRESULT.md#auth),
not a new test or staging run.

All 13 declared base operations (registry 3 GET + 3 SET; mandate 3 GET + 4 SET)
have real implementations. No operation is an unconditional empty handler.
The complete branch/no-op inventory is in
[ACCEPT.md#stubs](Deliverables/PDD_scaffold-admin-delegering_2026-09-08/ACCEPT.md#stubs).
The following limitations remain explicit:

| ID | Status | Boundary and missing work |
| --- | --- | --- |
| SAD-01 | `not-implemented` | `publisherAccess.issue` has no handler on this branch. A positive issuance fixture naming that key proves mandate shape/signing, not target execution. The green target action is `resetEditableCellConfiguration`; other target integrations are planned. Source wiring for `applyEditableCellConfiguration` is not an end-to-end publication result. |
| SAD-02 | `not-implemented` | Registry history does not recognize an administrate mandate by itself. `administrator.history` works through owner proof or the existing owner-authorized exact-key Agreement path. The broader mandate-only reader in the G2 draft remains planned. |
| SAD-03 | `not-implemented` | Explicit failure when a registry handler loses its weak `self` is missing: `administrator.state` and `administrator.thresholdPolicy` fall back to `.null`, `administrator.history` to `[]`, and all three SET handlers share `guard let self else { return .null }`. These are conditional no-op/fallback paths, not missing normal operations. No lifecycle test proving these paths unreachable or requiring a typed error is recorded. `ScaffoldMandateCell` throws `persistenceUnavailable` on lost `self`. |
| SAD-04 | planned / not executed | WP10, staging organization creation and representative provisioning are pending. Neither `entity:digipomps` nor `entity:dimy` is created there; Vegar's publishing access is not restored. No lawyer has assessed the organizational affiliation. |
| SAD-05 | verification limit | Several mandate Explore return schemas are generic object/list descriptions; prior computed-key source-audit warnings required manual review. This is not a complete remote schema/parity or generated-UI proof. |

Intentional idempotence is separate from SAD-03: registering the same organization,
revoking an already revoked mandate and revoking an already revoked orgLink return
the retained result without another mutation. The first two have explicit green
test assertions; the orgLink retry branch is source-inspected only. Namespace
GETs `mandate`, `orgLink` and bare `mandate.read` deny invalid/incomplete reads;
denial is not an empty success stub.

Acceptance measures **zero new failures**, not an all-green CellScaffold suite:
the existing report records 2150 tests, 90 failures and 29 unique failing tests,
against 2129 tests / 346–347 failures / 59 unique on main `e1f3e22f`.
No reduction in old failures is attributed to this PDD because environments differ.
