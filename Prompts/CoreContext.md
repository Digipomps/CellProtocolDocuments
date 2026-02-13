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

## Working Conventions
- Decompose work into small, verifiable steps.
- Explain failures and blockers explicitly.
- Keep docs in English unless explicitly requested otherwise.
- Update documentation together with behavior changes.

