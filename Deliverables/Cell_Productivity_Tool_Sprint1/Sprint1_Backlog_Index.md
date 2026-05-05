# Sprint 1 Backlog Index - Cell-Based Productivity Tool

## Objective
Coordinate Sprint 1 execution across runtime, desktop UX, server bridge, and entitlement layers for an Obsidian-like cell product with AI orchestration.

## Project Backlog Documents
1. Core runtime: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Docs/Sprint1_Cell_Productivity_Backlog.md`
2. Desktop UX: `/Users/kjetil/Build/Digipomps/HAVEN/Binding/Documentation/Sprint1_Cell_Productivity_Backlog.md`
3. Server/runtime bridge: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Documentation/Sprint1_Cell_Productivity_Backlog.md`
4. Entitlement and metering: `/Users/kjetil/Build/Digipomps/HAVEN/DiMyMicropayments/docs/iterations/ITERATION-16-sprint1-cell-productivity-backlog.md`

## Cross-Project Milestones

### Milestone M1: Contract Foundations (Week 1)
- CP-01, CP-02, DM-01 complete.
- Exit criteria: vault and entitlement contracts stable and versioned.

### Milestone M2: Orchestration + Bridge (Week 2)
- CP-03, CP-04, CS-01, CS-03, DM-02, DM-03 complete.
- Exit criteria: end-to-end orchestrated AI request can be authorized and executed.

### Milestone M3: UX + Mindmap + Hardening (Week 3)
- BD-01, BD-02, BD-03, CS-02, CS-04, CS-05, CP-05 complete.
- Exit criteria: primary user flow works and is test-covered.

### Milestone M4: Auditability and Sprint Closure (Week 4)
- BD-04, BD-05, DM-04, DM-05 complete.
- Exit criteria: policy surfaces and audit exports are ready for pilot users.

## Sprint 1 Critical Path
1. CP-01 -> CP-03 -> CS-03 -> BD-04
2. CP-01 -> CP-02 -> CS-02 -> BD-03
3. DM-01 -> DM-03 -> CP-03

## Risk Flags
1. Contract drift between Binding and Scaffold catalog/query behavior.
2. Non-deterministic matching/routing outputs causing flaky tests.
3. Entitlement policy ambiguity between subscription and BYOK.

## Tracking Recommendation
- Mirror each issue as a ticket in the active tracker with matching IDs (`CP-*`, `BD-*`, `CS-*`, `DM-*`).
- Keep acceptance criteria unchanged so test completion can close tickets automatically.
