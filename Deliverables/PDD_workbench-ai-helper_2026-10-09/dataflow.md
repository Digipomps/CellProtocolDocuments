# Dataflyt — AI-hjelper i Developer Workbench

Skrevet 2026-10-09. Kanter som er nye i denne PDD-en er merket **ny**.

```
Developer Workbench (skjelett)
  │  helper.ask {setId, text, context}            ny
  ▼
WorkbenchHelper ──grounding.analyze──► ExecutablePurposeGrounding ──(forslag)──► AIGateway
  │   ◄──GroundedActionPlan──────────┘
  │  sjekk: target.actionKeypath ∈ set.allowedActions          ny
  ├──grounding.verify / grounding.dryRun──► ExecutablePurposeGrounding
  ├──select {ids}──► WorkItem   (markering i listen)
  │
  │  helper.accept {proposalId}   (eierens klikk)              ny
  ├──setStatus {id, status} × N──► WorkItem   (requester = eieren, tilgang sjekkes per kall)
  │  helper.undo {proposalId}                                  ny
  ├──setStatus {id, forrige status} × N──► WorkItem
  │
  └──helper.handoff {conversation, surface}──► PersonalChatHub (Butler)   ny, fase 2
```

| Kant | Fra | Til | Endepunkt / keypath | Kontrakt |
|---|---|---|---|---|
| 1 | Developer Workbench | WorkbenchHelper | `helper.ask` | ny, `contract/` (WP1) |
| 2 | WorkbenchHelper | ExecutablePurposeGrounding | `grounding.analyze` | `ExecutablePurposeGroundingCell.swift:18`, `:129` |
| 3 | WorkbenchHelper | ExecutablePurposeGrounding | `grounding.verify`, `grounding.dryRun` | `ExecutablePurposeGroundingCell.swift:149`, `:153` |
| 4 | WorkbenchHelper | WorkItem | `select` | `WorkItemCell.swift:919` |
| 5 | WorkbenchHelper | WorkItem | `setStatus` | `WorkItemCell.swift:929` |
| 6 | Developer Workbench | WorkbenchHelper | `helper.accept`, `helper.undo` | ny (WP6) |
| 7 | Developer Workbench | WorkbenchHelper | `sets`, `set.select`, `set.save`, `set.diff`, `set.revert` | ny, `contract/workbench-ai-helper-instruction-set.v0.schema.json` |
| 8 | WorkbenchHelper | PersonalChatHub | handoff | ny, fase 2 (F2) |
