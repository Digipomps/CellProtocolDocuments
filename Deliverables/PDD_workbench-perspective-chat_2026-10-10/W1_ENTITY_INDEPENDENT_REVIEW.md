# W1 Entity dependency and candidate — independent source review

Date: 2026-10-12. Reviewer: Codex workbench_spec_review, read-only bounded passes.
Base: CellProtocol b4100f5734bb0b3781600845a267e424e55c0989 (2026.9.7).
No build or product test was executed by the reviewer.

## Dependency and consumer fixture

- Confirmed the legacy batch bypass in both EntityAnchor variants by source.
- Confirmed the minimal replay/canonical comparison belongs inside the existing
  authority gate before trace/snapshot writes; nested save would re-enter it.
- Inspected consumer Flow fixture: resolver binding, owner vault/signing,
  request correlation and receipt checks. No concrete P1/P2 found.
- Counted 13 internal + 4 dependency methods. Two rejection methods are expected
  to expose the pinned defect; this is not an executed result.
- Inspected the held one-shot job: marker/foreign-job/capacity guards, managed
  runner, jobs=2, exact inputs and queue layout. No P1/P2 within source scope.

## Runtime candidate and follow-up

Two seven-line guards in CellApple/CellVapor use canonical sorted JSON under the
existing gate. Entity is a Dictionary value; conflicting candidates are rejected
before publishing memory, appending trace or writing files.

P2 found before build: module/type ambiguity in CellApple.EntityAnchorCell and
CellVapor.EntityAnchorCell. The new test now uses existing test-target
AppleEntityAnchorCell/VaporEntityAnchorCell aliases, and os(macOS) for Vapor.
The reviewer reread the correction: no remaining P1/P2.

Two further test improvements were recommended and implemented: preserve,
install and restore MockCellResolver/debug flag; measure revision/head after
retry as well as the returned receipt. A final bounded reread confirmed both
and found no new concrete issue.

The eight new methods cover signed restart/retry, unrelated legacy writes,
conflicting leaf and parent on both runtimes; rejection compares disk bytes.
Fixture, signing and storage paths were assessed as plausible, not compiled.

## Limits

No runtime result, crash/lost-ack, feed-denial, retention/purge, migration, wider
regression or deployment claim. No queue window was opened by this review.
Current file and candidate patch hashes: evidence/w1-cleanup-and-entity-guard-20261012.json.
