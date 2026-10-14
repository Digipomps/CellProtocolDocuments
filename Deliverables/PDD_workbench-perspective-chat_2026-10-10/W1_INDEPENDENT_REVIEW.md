# W1 — independent source/document review, 2026-10-12

Reviewer: Codex agent workbench_spec_review. Read-only review in this session.
No compile, test, queue mutation, Git push or deployment was performed by the reviewer.

## Initial findings and disposition

- P2 private metadata on delegated feed: the preliminary runtime adapter was removed.
- P2 pending journal included in generic Cell encoding/autosave: the preliminary
  runtime adapter was removed. Existing WorkbenchHelperCell matches HEAD exactly.
- P2 command B could reconcile pending A using B's admission callback: changed
  commit boundary to return unknown(A) before readback/publication unless IDs match.
  A new test method covers that scenario; it has not been executed.

## Final bounded verdict (reviewer's response)

PASS within source/document scope. The commandID guard in
CellScaffold/Sources/App/Cells/WorkbenchHelper/WorkbenchSessionCommitBoundary.swift
returns unknown(A) before readback/publish for B. The new test draft checks this.
All three source hashes and byte counts match evidence/w1-preflight-20261012.json.
There are 13 test methods, consistently recorded in the documents. No new findings
in this bounded scope.

This is static review. No build, tests or product acceptance are established.
Learning sync was not reviewed. Live queue/GitHub/deploy observations were not
independently rechecked; saved observations and not-run statements are scoped logs.

## Remaining acceptance gaps

W1_FOUNDATION.md and TESTRESULT.md retain the incomplete production adapter,
outbox/restart delivery, wire contract, actual authorization/Flow, host reconciliation
and runtime tests. W1 and G3 remain incomplete. This review cannot authorize CI
before the local test gates or override queue, capacity and production holds.
