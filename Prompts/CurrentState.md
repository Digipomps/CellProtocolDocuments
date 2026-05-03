# Current State

Use this file as the short, durable handoff for active Codex and assistant work in this repo.
Keep it concise. Replace stale bullets instead of growing an unbounded log.

## Goal

- Maintain a reliable project-local checkpoint for work in `CellProtocolDocuments`.

## Active Focus

- Establish the local prompt overlay expected by `Prompts/SystemPrompt-Codex.md`.
- Preserve enough state to survive context compression and session restarts.
- Keep the repo-local checkpointing flow aligned with the installed global `context-compression` skill.

## Stable References

- `Prompts/CoreContext.md`
- `Prompts/SystemPrompt-Codex.md`
- `Prompts/SystemPrompts.md`
- `DEVELOPERS.md`

## Files Read Recently

- `Prompts/SystemPrompt-Codex.md`
- `Prompts/SystemPrompts.md`
- `DEVELOPERS.md`

## Files Changed Recently

- `.codex/skills/context-checkpointing/SKILL.md`
- `Prompts/CurrentState.md`
- `Prompts/Architecture.md`
- `Prompts/CONTRIBUTING.md`

## Decisions

- Use `Prompts/CurrentState.md` as the main checkpoint file for active work.
- Keep architecture and process knowledge in separate prompt overlay files to reduce drift.
- Prefer short structured summaries over freeform narrative.
- Install the global `context-compression` skill in `~/.codex/skills/context-compression` for future Codex sessions.

## Open Questions

- Whether the current checkpoint template should later grow a dedicated `Files Created` or `Deliverables` section.

## Next Steps

1. Verify that the new prompt overlay files are coherent and easy to maintain.
2. Update this file whenever a new task materially changes repo state.
3. Expand the template only if future work shows a clear missing section.

## Last Updated

- 2026-04-30 by Codex
