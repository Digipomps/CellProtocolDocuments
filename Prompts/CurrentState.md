# Current State

Use this file as the short, durable handoff for active Codex and assistant work in this repo.
Keep it concise. Replace stale bullets instead of growing an unbounded log.

## Goal

- Maintain a reliable project-local checkpoint for work in `CellProtocolDocuments`.

## Active Focus

- Phase 1 of Explore-first skeleton/cell authoring has started. The working
  standard is `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`; tools live
  in `Tools/Explore/`.
- Fast path for testing entity extension from `Co-Pilot Chat`: owner-scoped
  capability discovery is implemented in `CellScaffold` as
  `chatHub.state.entityExtension` / `chatHub.entityExtension.scan`, while the
  deeper ContactEndpoint, registry, proof-chain, wakeup, and retention work
  remains documented for hardening. Real runtime smoke on 2026-05-13 returned
  `200` for both the entity-extension read and scan HTTP adapters on port 9089.
- Keep the scaffold/repo boundary decision visible: `CellScaffold` is a
  reference/workbench scaffold, while simulator and domain-specific DiMy
  surfaces should be extraction candidates once their interfaces stabilize.
- Establish the local prompt overlay expected by `Prompts/SystemPrompt-Codex.md`.
- Preserve enough state to survive context compression and session restarts.
- Keep the repo-local checkpointing flow aligned with the installed global `context-compression` skill.

## Stable References

- `Prompts/CoreContext.md`
- `Prompts/SystemPrompt-Codex.md`
- `Prompts/SystemPrompts.md`
- `DEVELOPERS.md`

## Files Read Recently

- `Book/11_Developer_Guide_Cell.md`
- `Book/12_Skeleton_Spec.md`
- `Book/13_Agent_Instructions.md`
- `CellProtocol/Docs/Cell_Contract_Testing_Architecture.md`
- `Prompts/SystemPrompt-Codex.md`
- `Prompts/SystemPrompts.md`
- `DEVELOPERS.md`
- `Book/21_Contact_Endpoint_Cell.md`

## Files Changed Recently

- `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`
- `Tools/Explore/explore_contract_audit.py`
- `Tools/Explore/skeleton_explore_validator.py`
- `Book/11_Developer_Guide_Cell.md`
- `Book/12_Skeleton_Spec.md`
- `Book/13_Agent_Instructions.md`
- `Prompts/CoreContext.md`
- `Book/21_Contact_Endpoint_Cell.md`
- `Book/07_Scaffold_Runtime.md`
- `.codex/skills/context-checkpointing/SKILL.md`
- `Prompts/CurrentState.md`
- `Prompts/Architecture.md`
- `Prompts/CONTRIBUTING.md`

## Decisions

- Production skeletons should bind only to complete Explore contracts. Missing
  or `unknown` contracts are Cell work, not UI polish.
- Phase 1 uses static tooling first: audit Swift source for implicit contracts
  and validate skeleton bindings against exported Explore manifests before
  runtime preview.
- `Co-Pilot Chat` can expose an owner-scoped entity-extension map as a first
  test surface, but it must remain grant-checked, click-before-side-effect,
  explicitly discoverable, and non-correlating across domains.
- Treat `CellScaffold` as a reference/workbench scaffold. Extract
  `UserSimulationScaffold` after real bridgehead integration and API/metrics
  stabilization; extract DiMy conference/SMI/miniting surfaces when they need
  deployment without the full workbench payload.
- Use `Prompts/CurrentState.md` as the main checkpoint file for active work.
- Keep architecture and process knowledge in separate prompt overlay files to reduce drift.
- Prefer short structured summaries over freeform narrative.
- Install the global `context-compression` skill in `~/.codex/skills/context-compression` for future Codex sessions.

## Open Questions

- How much of the entity-extension snapshot contract should move down into
  `CellProtocol` before real remote device/cloud enumeration starts.
- Whether Porthole browser automation can be made reliable enough to verify the
  protected `Co-Pilot Chat` `Tilgang` panel without manual login.
- Whether the current checkpoint template should later grow a dedicated `Files Created` or `Deliverables` section.

## Next Steps

1. Run the Explore audit against `../CellProtocol`, capture the report, and use
   it to prioritize contract backfill.
2. Validate representative CellConfiguration skeletons once matching
   ExploreManifest/ExploreContractCatalog exports are available.
3. Hardening for entity extension: scalable registry/index, proof-chain
   extraction to `CellProtocol`, wake/persist lifecycle, and real device/cloud
   provider adapters.
4. Revisit simulator repo extraction when `UserSimulationScaffold` has passed
   real `/bridgehead` integration and its coordinator/worker API, metrics,
   sharding, and JSONL artifacts have stabilized.
5. Verify that the new prompt overlay files are coherent and easy to maintain.
6. Update this file whenever a new task materially changes repo state.
7. Expand the template only if future work shows a clear missing section.

## Last Updated

- 2026-05-28 by Codex
