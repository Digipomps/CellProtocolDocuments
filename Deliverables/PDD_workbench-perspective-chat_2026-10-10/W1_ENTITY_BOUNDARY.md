# W1 — cleanup and Entity journal boundary, 2026-10-12

Status: Mac and server cleanup completed through the deploy queue and independently checked. Source candidates remain unrun; G2 is approved and G3 pending.
The immutable PLAN.md/plan.json and approval evidence are unchanged.

## Completed cleanup

Claude's deploy queue removed only `release-2026.10.4/.build/arm64-apple-macosx`
in job `z40-rydd-release-build`; candidate size was 7,679,604 KiB (7.32 GiB).
The receipt ended LEVERT/EXIT=0 at 07:32Z. Independent filesystem inspection
confirmed that product directory absent and `.build/checkouts`,
`.build/repositories`, Sources, Package.swift and .git present. Free space was
105.67 GiB at 07:35Z; concurrent work means this is not 7.32 GiB net df growth.
At 07:57Z, free space was 104.14 GiB. Every build still needs a fresh capacity
check with 10 percent projected floor and 10 GiB reserve.

Read-only host inspection at 07:45Z found 45.38 GiB free on root and 40.62 GiB
on the Docker volume. No server files, images, volumes or containers were
deleted in this session. The ops inventory was incomplete due to permission
denials. Docker's reclaimable number does not establish release safety; old
image candidates still require reconciliation against all container image IDs,
reserved releases and rollback evidence. Preserve archived project evidence,
models and active worktrees/caches. No broad prune was performed.

## Pinned runtime finding and bounded correction

CellScaffold pins CellProtocol 2026.9.7, peeled commit
`b4100f5734bb0b3781600845a267e424e55c0989`; remote main matched at inspection.
Both EntityAnchor implementations replay the authority journal for ordinary
saveKeypathStorage and reject a candidate that conflicts with signed history.
The legacy batch branch (`commitRequest == nil`) bypassed that comparison:
it could acknowledge a changed snapshot while restart would replay the older
signed value. This is source evidence, not yet an executed failure.

An isolated branch `codex/workbench-entity-journal-20261012` based on that commit
adds the same canonical replay comparison before trace append/snapshot write
in CellApple and CellVapor. The existing authority gate is already held; calling
saveKeypathStorage from inside it would re-enter the gate. No wire/JSON change,
new authority policy, migration or journal deletion is introduced. The existing
error `legacy_write_conflicts_with_committed_keypath` is reused. This preserves
an existing invariant; it does not certify every other writer or multi-process
concurrency. The dirty primary CellProtocol checkout was preserved.

Eight new, unrun CellBaseTests methods cover signed receipt/restart/retry,
unrelated legacy writes, conflicting leaf writes and conflicting parent
replacement on Apple and Vapor. Rejected batches must also leave persisted
snapshot and journal bytes unchanged. Existing tests and package pins are
unchanged. Independent source review caught a module/type name collision in
the new test; existing AppleEntityAnchorCell/VaporEntityAnchorCell aliases are
now used. Review completion is recorded separately; none of this is compile
or runtime acceptance.

## Consumer proof prepared, not queued

The existing two internal Workbench types and 13 journal/commit tests are joined
by four synthetic real-EntityAnchor Flow probes. The 17-method consumer job is
frozen by manifest in `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-20261012`.
Two rejection methods are predicted to fail against the pinned release.
This baseline remains unchanged by the separate runtime correction.

The job defaults to input inspection, requires the actual ÅPENT marker and no
foreign running jobs, checks inputs/HEAD/branch, performs a fresh capacity gate,
uses two Swift jobs and the managed runner, and records a one-shot attempt.
Syntax and input-only execution passed on the Mac with unset locale and
`en_US.UTF-8`; this does not prove every negative script path. No Swift, CI,
push, PR, queue submit, staging or prod operation has occurred for these changes.
The `.job.hold` is outside every inbox. Independent review of the 17-test
fixture/job found no P1/P2 issue within source-only scope.

Claude's d237/w23 work still owns the build window; y6 is responsible for opening
it after that work. Do not submit before the marker is ÅPENT. Then back up and
append the required confirmation in `_losen-queue/KOORDINERING.md` and submit
exactly the prepared job to inbox-g2. A red result stops the affected chain under
PLAN.md; no automatic rerun or candidate build. The separate CP candidate needs
its own coordinated focused and regression proof before integration.

## Remaining storage and product boundaries

- EntityAnchor signs and writes its journal before snapshot completion. A failed
  snapshot acknowledgement can therefore follow a journal write. Recovery must
  distinguish unknown from rejected and reconcile the original mutation; a
  signed receipt alone is not disk readback or power-loss proof.
- Inherited Flow grants can authorize a non-owner feed. A Helper owner gate does
  not by itself protect private values emitted by the underlying EntityAnchor.
  A real granted-feed rejection test is still required.
- EntityAuthorityJournalEntry retains full mutation payloads in its hash chain.
  Replacing a snapshot or writing a tombstone does not erase old chat text.
  No selective payload purge/compaction contract was found in the inspected
  runtime. Do not store real chat text in this path on the assumption it can
  later be purged by changing the snapshot. Encryption is not selective erasure.
- The user has been asked for retention of new private chat text. No answer has
  been recorded. Idea TTL is not a chat retention policy.
- W2 owner inventory remains blocked: AgentD targets returned Transport closed;
  the native Mac UI was locked at the latest observation. Neither was bypassed.
- The production adapter/outbox, actual owner and retention binding, replay
  catch-up, perspective/model/embedding/history/actions and end-to-end release
  proof remain outstanding. The existing WorkbenchHelper runtime is unchanged.

Source hashes and observations: `evidence/w1-cleanup-and-entity-guard-20261012.json`.
Earlier observations in W1_FOUNDATION.md and its evidence file are historical.

## Follow-up after 08:04Z

Native Claude became accessible again. The live queue coordinator acknowledged
receipt of the held test job and the request to reconcile five exact old server
image candidates; it is checking container IDs and release reservations. This
is not a cleanup completion receipt.

Chrome showed a cached Developer Workbench view with 77 cards and kjetil2 label.
Closing the detail dialog and selecting Prosjekter redirected to login. The
cached view is not a fresh owner inventory or proof that data is currently
readable. No export, migration or new private chat write occurred. The user
was asked to sign in again. Retention and login requests were recorded as
pointer-only entries in `HAVEN-Deploy/_handoff/GODKJENNINGER/forespoersler.json`;
they do not grant authority or claim a live Workbench sync.

Learning L-2026-10-12-en-signert-entity-journal-beviser-ikke-at-alle was applied
and synced to cellprotocol-distributed-entity-data. Canonical, local Codex and
Claude SKILL.md hashes match. Desktop stores and upload ZIP were generated; an
already uploaded Cowork plugin has not been updated. The global learning check
remains red on seven pre-existing open and 31 applied-but-unsynced entries; this
session's learning is not among them. No rerun or claim that the global gate is
green.

## Server cleanup completed and independently checked, 08:10Z

Claude's x41 removed the five exact old image candidates using docker rmi
without force or prune, after checking all 32 container Image IDs and reserved
release SHAs. The queue receipt reports no active host claims. It also discloses
that reading extra deploy-receipt SHAs produced no additional matches, probably
due to ops permissions; do not claim those receipt directories were fully read.

A separate Codex read via the normal ops SSH wrapper found all five image IDs
absent, 32 containers/22 running unchanged, and the same prod/staging/rollback
container image IDs. Docker volume free space: 42,596,332 KiB before,
62,649,880 KiB after (40.62 → 59.75 GiB, about 19.12 GiB net). Root free space
remains about 45.38 GiB. Image metadata sizes are not summed as net disk gain.
Receipt: HAVEN-Deploy/_handoff/OPPRYDDING/VERT-RMI-KANDIDATER-20261012.md.
No claim of new deploy or full service acceptance follows from this metadata.

The queue owner was asked to activate exactly the held 17-test job only after
y6 opens the window, fresh admission and the required backed-up coordination
entry. It must stop on drift/failure and may not run the CP candidate, push or
deploy. At this record, acceptance/submit has not yet been confirmed.

## Activation handoff accepted, 08:11Z

The live Claude chat “Deploy prosjekt køadministrasjon” explicitly accepted
activation of the single held test job. It inspected the script and will not
use a separate waiting queue job, which would violate the foreign-job guard.
It will copy the job only when the window is ÅPENT, only finishing y6 remains,
inbox-w/inbox-d are empty, fresh capacity permits it and KOORDINERING is backed
up and updated. First planned check is 09:30Z. Receipt for submit/result will
appear there; at this handoff the job is still not submitted. No edit to the
frozen source/script, no retry, candidate build, push, CI or deploy is included.

For the next Codex turn: read the queue receipt and attempt marker first; never
submit a duplicate. A red probe stops the chain under PLAN.md until Kjetil
authorizes the concrete next run. The separate CP patch is review-ready source,
not tested. Login and private-chat retention questions remain unanswered.
