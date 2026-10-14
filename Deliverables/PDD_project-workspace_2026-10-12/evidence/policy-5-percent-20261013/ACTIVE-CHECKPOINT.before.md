# Active continuation checkpoint — 2026-10-13T15:54:56.867156+00:00

## Current authorization and actual state

Kjetil: «Jeg godkjenner testrettelsen og én ny lokal baseline på 116 tester. Ved grønt kjører du de allerede godkjente 8+17 testene og fortsetter med prosjektflaten. Ingen CI eller deploy.»

The exact approved stale access-banner test patch is APPLIED. No product edits have been made. The corrected test requires request/recheck and absence of obsolete approve; security behavior remains unchanged. `git diff --check` passed. R1 non-Swift preflight passed in no-locale and nb_NO.UTF-8; queue envelope uses blank first line = HAVEN root. These checks do not claim XCTest success.

At this checkpoint R1 and CP8→CS17 have no attempt-started/result. Queue owner recorded the next exclusive reservation at 15:49:55Z; d245-agentd-bro-w26-regresjon and w-d245-reproduce-r2 still occupy the queue. The reservation also requests coordination with Sprout builds outside the queue. Do not preempt another job, clear a lease, or start competing Swift. Read fresh state; this paragraph is a timestamped observation.

A thread heartbeat `fortsett-prosjektflaten-etter-lokale-tester` is ACTIVE every ten minutes. It checks these result files briefly, stays quiet on unchanged state, and resumes this task on actionable progress. Queue owner, not the heartbeat, controls admission and activation. Pause the heartbeat when work is taken up after green, on red after documenting the failure, or when user action is the sole remaining dependency.

## Exact inputs

Find managed source paths with `git -C CellScaffold worktree list --porcelain` from HAVEN root; do not use this chat's old default worktree.

- Project branch `codex/project-workspace-20261013`, base `3a6680446e55fc1644afb368ac2bf48dd0720e30`. Only dirty file: `Tests/AppTests/PortholeConfigurationLoadingTests.swift`, SHA256 `2c8c40cc0ec35d3e9fbc249583e053e91638ef610f0b363c5cc8dc725c2efc70`. Applied patch is `evidence/proposed-access-banner-test-20261013.patch`, SHA256 `93a4e5a61625f974eb4242975f8e2aecaab42d27ebc3aae8bf5eccb293fd45f1`.
- R1 packet: `HAVEN-Deploy/_handoff/ARBEIDSBENK/PROJECT-WORKSPACE-BASELINE-R1-20261013`, jobID `project-workspace-baseline-r1-20261013`, manifest `c2d85e1999b8bdd6fd4abe7121879426fff34f15d7ece11a07ced8e2aa60f73b`. AUTHORIZATION binds current user approval. 112 prior methods + four existing AdminAccessBannerTests = 116 exact unique methods. Published CP `b4100f5734bb0b3781600845a267e424e55c0989` (2026.9.7). Helpers inherited from reviewed packet; driver permits only the one exact dirty test file and rechecks authorization/hash.
- Prior failed packet `PROJECT-WORKSPACE-BASELINE-20261013` remains immutable, 111 passed / 1 stale-test failure at 15:13:02Z. Never rerun it or mix its receipts into R1.
- Next packet: `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CONTINUE-20261013`, jobID `g2-w1-entity-continue-20261013`, manifest `9c481f32f273cd928a09eca02fd54073f2091fb591589ed78e220af4524ce469`. AUTHORIZATION exists. CP candidate branch `codex/workbench-entity-journal-20261012`, base b4100f57; consumer branch `codex/workbench-perspective-chat-20261012`, base 9ff06f84. Its own manifest freezes all source inputs. Do not change either until its tests complete. Owner must fix only activated queue-envelope first line to blank; frozen `.job.hold` stays unchanged.

Both jobs use fresh owner admission, bounded managed caches, two Swift jobs, 40 GiB / 10 percent after 10 GiB reserve, report-only cache collection, and one attempt. No direct Swift, new scratch tree, whole-cache deletion, CI or deploy. No automatic repeat after red.

## Observe and continue

1. Read only both `result.json` / attempt markers initially. If no terminal change, inspect latest relevant `_losen-queue/KOORDINERING.md` paragraph only as needed. Owner Claude thread is “Deploy prosjekt køadministrasjon” in HAVEN-Deploy, current project thread, not the migrated archived chat. User explicitly authorizes coordination. Verified UI message sent 15:49 local tool timestamp 17:49 CEST; owner replied that it would verify and activate when free.
2. For green R1, require status passed / exitCode0, all 116 exact starts and terminals once, unchanged pins, actual remote CP workspace entry, source postcheck and queue `.done`. Then owner activates unchanged CP8→CS17 with fresh admission.
3. For green next packet, require eight CP and seventeen CS methods, actual CS filesystem dependency pointing to frozen CP candidate, preserved before/after pin evidence and exact restored pins, both source postchecks, terminal receipts. Do not infer consumer success from CP success.
4. On either red, stop dependent chain, preserve raw evidence and diagnose specific failure. No new test attempt or additional committed-test change without Kjetil's word. Do not present an empty log or missing terminal as green.
5. After both green, update `TESTRESULT.md` and `STATUS.md` with actual hashes/counts; pause the waiting heartbeat and immediately resume approved product implementation in the project branch. The GUI/P1–P6 plan is approved G2; no new approval gate is required merely to implement it. The current instruction still excludes CI/deploy.

## Product work to resume

Read `PLAN.md` with `evidence/g2-approval-20261013.json`; historical plan header predates approval. GUI references and original spec are frozen. `evidence/p1-independent-source-read-20261013.md` and `evidence/p1-view-lifecycle-20261013.md` are source-audit requirements, not implementation.

First actual slice: isolated authorized project context and direct dashboard opening. Keep legacy select for legacy consumers. New explicit workspace route uses portfolioUUID/projectID/viewInstanceID/mountID and must never mutate shared selectedProjectID. Server-side scoped read, not client-filtered broad private state. Project record and source version must be read atomically from ProjectPortfolioCell's queue. Recheck authority after awaited source operations; revoke clears labels/counts/search/graph and fences late results.

Per-view runtime needs an explicit role before initialization: ordinary Orchestrator init attaches the owner's native model callback; save writes a sidecar even when persistancy is ephemeral. Preserve the required identity-host initializer for AccountContinuityPortholeCell; transient views must neither attach the shared native model channel nor read/write its sidecar/resolver snapshot. Reserve view construction before await, bind proof-bearing requester/session/view/mount, invalidate on logout/expiry/replacement without destroying active HTTP state on ordinary WS reconnect. Native identity-host behavior must remain covered.

Main files: `CellScaffold/Sources/App/Cells/SimpleProjectManager/OrchestratorCell.swift`, `Sources/App/Cells/interface/WebCellEmbeddings.swift`, `Sources/App/Controllers/VaporWebSessions.swift`, `Sources/App/Controllers/VaporBrowserhead.swift`, `Sources/App/Controllers/PortholeWebSessionSupport.swift`, `Sources/App/Cells/WorkItems/ProjectPortfolioCell.swift`, `Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift`, `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift`, Porthole JS and shared workbench styles. All paths after the first are relative to CellScaffold.

Browser route restoration carries project IDs but creates a fresh view ID per page load, including duplicate tabs. Both project Open routes go to actual catalog Skeleton dashboard; new-project intake has its own explicit entry. Stable configuration UUID and project scope in back/refresh. New project isolation/authorization/lifecycle/open test files may be written; do not edit other committed tests. Object/list ValueType assertions compare canonical sorted JSON. Test real catalog Skeleton and signed nonowner agreements.

P2 must use Flow/invalidation and snapshot resync on gaps, no fullscan timer. Existing mutation topic is haven.project-portfolio.mutations. Reader grants may lack eventsSince; use authorized snapshot fallback, not policy widening. Unknown counts remain unknown. P5 requires AgentD owner integration; last 14:01Z snapshot showed expired Porthole bridge, not live recovery. Do not claim queue control merely because a command is stored or helper journal tests pass. P6 extends actual web/native network renderer and Binding parity, not a separate mock app.

Mandatory learning capture at the end of command/edit sessions. Existing queue-envelope and transient-host lessons have already been applied/synced; do not duplicate narrative as learning.

## 2026-10-13T15:57:55.087155+00:00 — capacity blocks admission before any test attempt

A capacity-only invocation with the frozen 40 GiB / 10 percent / 10 GiB reserve policy returned 75: 90.8 GiB free (9 percent), 80.8 GiB (8 percent) after reserve. No Swift or attempt-started. See evidence/baseline-r1-capacity-20261013.json. Queue owner was already measuring cleanup candidates, and the exact measurement was sent and visibly read back in the Claude thread at 17:56 CEST. Codex has not deleted anything or started a competing cleanup. The older general five-percent policy in the health skill does not alter this approved project's frozen PLAN/AGENTS ten-percent policy. Capacity must pass afresh before admission; preflight blockage does not spend the approved XCTest attempt.

Independent reader r1_receipt_review checked the applied patch, exact 116-method set, source/script hashes, minimal driver delta, preserved safeguards, untouched CP manifest and ACTIVE heartbeat. No blocking findings; no XCTest was run. Its later queue snapshot had d245, inv12 and x49 running; the earlier queue listing is historical. This new capacity note was appended after that initial review.

Independent final note check: r1_receipt_review found only a wording clarification: the percentage floor fails (8 percent after reserve); the absolute 40 GiB floor passes. Final status wording was corrected accordingly. No source, frozen script, manifest or test result changed.
