# TESTRESULT — W1 partial foundation

All product test refs remain blocked/not-run. This file does not claim W1 or G3 acceptance.
Source hashes, queue and capacity observations: evidence/w1-preflight-20261012.json.
Scope and source findings: W1_FOUNDATION.md.

## events
Blocked: 17 new consumer XCTest methods drafted (13 internal journal/commit and 4 real EntityAnchor Flow probes), zero executed. Eight additional runtime tests are drafted in the isolated CellProtocol candidate, also unrun.
No live Cell/Flow, storage restart/crash, outbox or host reconciliation evidence.
The earlier six Cell integration test drafts were withdrawn with the unsafe snapshot adapter.

## build
Blocked: queue window remains closed behind d237/w23. Cleanup increased disk space; a fresh projected 10 percent capacity check is still required inside the admitted job. The prepared job is outside the inbox and has not run.
No Swift invocation, no CI.

## regression
Blocked: not run. Existing tests are unchanged.

## contract-fixtures
Blocked: internal draft is not the full public contract. No actual Explore/codec fixture proof.

## auth
Blocked: callback denial tests are drafts. Actual requester, forged identity,
delegated feed grant, retention revocation and runtime isolation remain unproved.

## dataflow
Blocked: production journal/admission/outbox adapter is not installed.

## static-source-preflight
Literal guard exited 0, including its six self-check messages; 19 existing
over-limit literals remain covered by baseline. No new over-limit source literal.
Tracked diff --check exited 0. New-file no-index whitespace inspection produced no
diagnostics; exit 1 represents added-file differences. These are not compilation tests.

## other-plan-tests
W2–W7, GUI parity/reachability/load-time, models, history, actions and production
end-to-end evidence remain not-run. Prior document-only checks retain their existing
scope; the global PDD validator's five prior lesson-reference failures are not cleared.

## entity-boundary-source-review
See W1_ENTITY_BOUNDARY.md. The pinned-runtime source audit found the legacy batch conflict bypass; two consumer rejection methods are expected to expose it. A separate candidate protects both runtimes before trace/snapshot write. No executed failing or passing product result is claimed. Script syntax/input-only checks passed; they do not compile Swift.

## W1 første lokale test 2026-10-12

Maskinelt opptalt: 17 testmetoder, 15 pass, 2 fail og 4 assertions. Alle 13 WorkbenchSessionJournalTests pass. De to forventede legacy-journal-conflict-probene feilet på CellProtocol 2026.9.7. Exit 1. Se W1_TEST_RESULT_20261012.md og evidence/w1-first-test-result-20261012.json. Ingen rerun.
