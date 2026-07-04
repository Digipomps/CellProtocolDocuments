---
name: cellprotocol-docs-and-rag-maintenance
description: Use when updating, auditing, reorganizing, or generating CellProtocol documentation, Book chapters, machine-readable catalogs, agent entrypoints, read-only Docs MCP surfaces, RAG/discovery indexes, RAG prompt transformer contracts, gap analysis, handoff notes, or context-preservation summaries for HAVEN/CellProtocol and companion repositories.
---

# CellProtocol Docs And RAG Maintenance

Use this skill when the durable knowledge layer needs to change, especially
when code behavior, agent workflows, or cross-repo contracts have changed.

## Core Rules

- Documentation must match current code and current known limitations.
- Do not document planned behavior as implemented behavior.
- Do not commit documentation for a behavior change before the implementing code
  is committed. If updating both in one workflow, commit code first, verify it
  landed, then commit docs.
- Keep protocol/runtime behavior in `CellProtocolDocuments`; keep app/product
  behavior in the owning app repo unless it is shared protocol contract.
- Update machine-readable catalogs when user-facing Book structure changes.
- Write for future agents: clear entrypoints, exact paths, and current limits.
- Preserve enough context for recovery before long work risks context loss.
- Keep the docs MCP boundary clear: `Tools/HavenDocsMCP` is read-only lookup
  and static reading-path prompts. Model-adaptive prompt packaging belongs in
  RAG or `RAGPromptTransformerCell`, not in the MCP adapter.
- When Explore contract behavior, skeleton binding rules, or agent authoring
  workflows change, update `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`
  and keep `Tools/Explore/` usage examples current.

## Installation And Portability

- Keep this `SKILL.md` as the single source for Codex, Claude Code, and Claude
  Desktop variants.
- Install for Codex at
  `~/.codex/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md`.
- Install for Claude Code at
  `~/.claude/skills/cellprotocol-docs-and-rag-maintenance/SKILL.md`, or as a
  project skill under `<CellProtocolDocuments>/.claude/skills/`.
- Package Claude Desktop uploads as one ZIP containing a single folder named
  `cellprotocol-docs-and-rag-maintenance` with `SKILL.md` at that folder root.
  Claude Desktop rejects lowercase `skill.md` packages.
- Treat absolute `/Users/kjetil/...` paths below as local anchors. On another
  machine, resolve the same repo-relative paths from the active
  `CellProtocolDocuments` checkout before deciding that a file is missing.

## Read First

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/README-CellProtocol.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/00_Book_Home.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/book_catalog.json`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/15_Documentation_Discovery_and_RAG.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/16_Book_Reference_Workspace.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/17_Documentation_Workbench_Landing_and_Development_Plan.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/22_Explore_Contracts_For_Skeleton_Authoring.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/28_RAG_Prompt_Transformer_Cell.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/HavenDocsMCP/README.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/RAGPromptTransformer/README.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Gap_Analysis.md`

If code behavior changed, inspect the actual source before editing docs.

## Placement Rules

- Core protocol contracts: `CellProtocolDocuments/Book`.
- Read-only local docs lookup adapter: `Tools/HavenDocsMCP`.
- Model-adaptive RAG prompt package contract:
  `Book/28_RAG_Prompt_Transformer_Cell.md` plus
  `Book/rag_prompt_transformer_cell_contract_v0.json`.
- Deterministic reference transformer and fixtures:
  `Tools/RAGPromptTransformer`.
- Current implementation caveats: relevant Book chapter plus `Gap_Analysis.md`
  if the gap is unresolved.
- Agent workflow: `Book/13_Agent_Instructions.md` or a focused skill.
- App/scaffold behavior: app repo docs, with a pointer from CellProtocol docs
  only if it illustrates shared protocol use.
- Temporary handoff: `Prompts/CurrentState.md` or a dated deliverable when the
  content is project-state rather than canonical spec.

## Required Workflow

1. Identify what changed: code, contract, limitation, workflow, or product docs.
2. Find the authoritative source and compare before editing.
3. Update the smallest doc set that future agents will actually read.
4. Update `book_catalog.json` when Book chapter inventory or metadata changes.
5. Add "current limitation" language when behavior is partial.
6. Avoid marketing claims unless `haven-claim-review` is also applicable.
7. Validate links/paths and run any local catalog checks if present.

## RAG Hygiene

- Prefer stable headings and concise summaries.
- Put exact file paths near operational instructions.
- Keep examples minimal and schema-valid.
- Split large docs by task area instead of creating giant catch-all chapters.
- Include negative boundaries: what is not supported and what requires approval.
- For shared use with colleagues, prefer each developer running the read-only
  Docs MCP locally from their own checkout. Use a shared LAN/VPN service only
  when the hosting, auth, freshness, and source-revision boundary is explicit.
- RAG source packages should preserve canonical citations, retrieval warnings,
  and prompt manifest hashes before provider invocation.

## Completion Checklist

- Docs align with current code or clearly state planned/gap status.
- Book index/catalog updated if needed.
- Agent entrypoint remains easy to find.
- No stale cross-repo paths were introduced.
- Any uncertainty is explicitly called out.
