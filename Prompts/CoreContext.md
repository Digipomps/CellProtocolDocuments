# Core Context (Shared Canonical)

This file is the shared source of truth for architecture concepts and collaboration rules across projects in this workspace.

## Scope
- Applies to Binding and other projects using CellProtocol.
- Project-specific status and roadmap belongs in each project's local `Prompts/CurrentState.md`.

## Authoritative References
- `Book/10_Quickstart.md`
- `Book/11_Developer_Guide_Cell.md`
- `Book/12_Skeleton_Spec.md`
- `Book/13_Agent_Instructions.md`
- `Book/14_Perspective_Runtime_Matching.md`
- `Book/15_Documentation_Discovery_and_RAG.md`
- `Book/16_Book_Reference_Workspace.md`

## Core Concepts
- `CellConfiguration`: declarative configuration payload for cells and skeleton UI.
- `SkeletonElement`: declarative UI tree rendered by platform-specific renderers.
- `Meddle.get/set`: authoritative state and command interface for cells.
- `Emit.flow`: runtime publishing channel via `FlowElement`.
- `Perspective`: purpose/interest graph and matching context.

## Interface Constraints
- Expose state/behavior with interceptors (`addInterceptForGet`, `addInterceptForSet`).
- Enforce authorization per keypath inside the cell.
- Publish events and updates through flow topics, not ad-hoc side channels.

## Agreement and Contract Evolution Rules
- Authorization is capability-based and identity-bound. Do not model access control as static role labels.
- Agreement templates may be applied with explicit rollout behavior:
  - only for new connections, or
  - including re-evaluation of already connected identities.
- If re-evaluation makes a connection non-compliant, implementations may require renewed `signContract` or revoke access only when contract terms/conditions allow it.
- Agreement artifacts should be signable by all parties and retrievable for storage in each party-controlled entity context.
- Default connect behavior remains `ConnectState`-driven: if `signContract` is returned, user review/signing flow is expected.
- If a proposed solution may conflict with documented CellProtocol concepts, discuss with the user before implementation.

## Working Conventions
- Decompose work into small, verifiable steps.
- Explain failures and blockers explicitly.
- Keep docs in English unless explicitly requested otherwise.
- Update documentation together with behavior changes.
