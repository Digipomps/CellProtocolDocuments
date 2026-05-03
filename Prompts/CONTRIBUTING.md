# Contributing

Operational rules for Codex and humans working in this repo.

## Documentation Policy

- Update documentation in the same change set as functional changes when relevant.
- For contract or endpoint changes, update both user-facing and agent-facing docs.
- Document legacy compatibility explicitly when it still matters.
- Prefer repo-relative markdown paths; avoid absolute local paths in repository docs.

## Context Preservation

- Read `Prompts/CurrentState.md` at the start of substantial work or after a long gap.
- Update `Prompts/CurrentState.md` after important findings, file edits, or decision changes.
- Keep checkpoints short, structured, and factual.
- Summarize external research in your own words; store only the facts needed to resume work.
- Before expected context compression, ensure `Goal`, `Files Changed Recently`, `Decisions`, and `Next Steps` are current.

## RAG-Friendly Writing

- Give each document a clear purpose, scope, and audience near the top.
- Include concrete file names, paths, keypaths, or endpoint names as list items when relevant.
- Keep a stable canonical path per topic to avoid duplicate truths.
- When describing a contract or interface, include `Last verified against code` with a date when possible.

## Deliverables

- Put generated research packs and one-off outputs under `Deliverables/`.
- Use descriptive names, ideally with dates for time-specific artifacts.
