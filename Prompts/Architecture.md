# Architecture

Stable project-local overlay for how this repository is organized.

## Purpose

- `CellProtocolDocuments` is the documentation and prompt workspace for HAVEN / CellProtocol.
- Shared assistant context lives in `Prompts/CoreContext.md`.
- Project-local operational state lives in `Prompts/*.md` in this repo.

## Repository Layout

- `Prompts/`: shared wrappers and project-local overlays used by Codex and other assistants.
- `Book/`: canonical documentation chapters and doc tree for the platform.
- `Deliverables/`: dated research packs, generated artifacts, and one-off outputs.
- Repository-root `.graffle` and `.json` files: working diagrams and exports.
- `DEVELOPERS.md` and `README-CellProtocol.md`: entry points for humans and assistants.

## Prompt Layering

1. `Prompts/CoreContext.md` contains shared canonical concepts.
2. `Prompts/SystemPrompt-Codex.md` is a thin shared wrapper.
3. `Prompts/CurrentState.md` holds active checkpoint state.
4. `Prompts/Architecture.md` holds stable repo structure and invariants.
5. `Prompts/CONTRIBUTING.md` holds durable working rules for edits.

## Change Guidance

- Update `Prompts/CurrentState.md` for temporary or task-specific state.
- Update `Prompts/Architecture.md` only when repo structure or durable workflow assumptions change.
- Prefer one canonical file per topic; avoid duplicate truths across `Book/`, `Prompts/`, and `Deliverables/`.
