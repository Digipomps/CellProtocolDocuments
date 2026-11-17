# Butler / CellScaffold production recovery audit

Read-only audit 2026-09-17. Baseline `origin/main` = `b4a2779a5122d56ecdd9c9475fe772790bfd180c`, confirmed by root's subsequent fetch. Source tree inspected without modifying source, refs, or deployments. No runtime/build/browser success is claimed here. The handoff was treated as historical evidence and checked against source.

## Immediate integration recommendation

1. Integrate `pdd/butler-hjelpertre` at `022cc257fdeb3e4042bf7fa3d3fe07a61bde6f83` after running the exact candidate's tests. This clean worktree already incorporates baseline main and widget work. It adds the actual missing **Tråder** button, expandable helper hierarchy, node/subtree scopes and retained message provenance. This is the shortest concrete path to the requested thread GUI.
2. Do not reapply `pdd/butler-widgetflate`: its net diff has exactly the same stable patch-id as main commit `b4a2779a`; source and widget tests are also byte-identical. Widget branch ancestry alone misleadingly reports two unique commits because main used squash.
3. Include the small expired-session recovery `0115e4945d…` (`codex/porthole-session-recovery-20260910`) if it remains absent after root integration. It is four files, fixes expired Porthole sessions, and includes route and JS-source regressions. The admin-delegation branch already carries its equivalent `f3f6f67f`; do not import both.
4. Recover the dirty Butler provider registry/cache bundle separately (files below). It addresses registrations disappearing on restart. Preserve discovery's **opt-in** default; unconditionally enabling discovery would undo documented avoidance of slow/unavailable Cell lookups.
5. Do not merge old aggregate salvage branches wholesale. Apply the concrete missing packages listed below against main; all old histories also contain superseded deployment and identity implementations. Every dirty source file is inventoried, so leaving a package pending is visible rather than losing it.

## What helper tree actually implements

Worktree: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellscaffold-butler-hjelpertre`.

Branch-only non-merge commits: `d14c0362` model/UI; `74c6dc43` test-support reachability copy; `3385391e` Swift type-check fix; `68b6d91d` rail layout; `147ff38b` SkeletonCondition enum access; `cde7871e` visibility and semantic assertions. `f6bbb2a8` and `022cc257` are main integration merges.

The 12-file net diff is 1,537 insertions / 4 deletions. Core files:

- `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore+HelperTree.swift`: validated tree model, migration from helperRows, collapse state, selected node, subtree filtering, stable chronological message projection, unique row counts.
- `Sources/App/Cells/PersonalCopilot/PersonalCopilotCells+HelperTree.swift`: requester-authorized read and action contracts (`selectNode`, `setExpanded`, `setScopeMode`, `open`, `close`) and change flow.
- `Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory+HelperTree.swift`: existing skeleton elements, 288px rail, empty List gating, explicit `Tråder` open button and scope controls.
- `PersonalCopilotCloudStore.swift`: optional persisted helperTree and message nodeID; widget projection first, tree projection second; migration of legacy messages to Butler root.
- `PersonalCopilotConfigurationFactory.swift`: header, branch chips, rail wrapping retained alongside widgets.
- `Public/css/porthole-webo.css`: remaining-width desktop layout and compact overlay; no hidden desktop-only feature.
- `Tests/AppTests/PersonalCopilotHelperTreeTests.swift`, `PersonalCopilotHelperTreeReachabilityTests.swift`, fixture and support audit; both test classes in `ci/test-filter.txt`.

Critical limits, independently visible in code:

- This is A1/A2/A5, **not A3/A4**. `selectNode` changes `scope.nodeID`; it does not choose `activeHelper` or route a request through ancestors. Existing tests intentionally preserve independent legacy helper selection. Header copy “skriver til: X” can therefore imply stronger routing than implemented. Root should either implement tested routing or make that copy accurately describe scope.
- No public create/reparent action or dynamic new-helper suggestion exists. `upsert` is model support and test usage, not a reachable product operation.
- All existing helperRows become direct children of Butler; root begins collapsed and rail begins closed. Acceptance must explicitly open **Tråder** and expand Butler before deciding the tree is absent.
- An async provider response reads the *current* selected node when `appendProviderInvocationLog` runs (`CloudStore.swift:9582–9609`). If the user changes scope while a provider request is pending, a reply can be attributed to the later scope. Capture the originating node before await and test changing scope during an in-flight response if provider chat is part of the release acceptance.
- Projection retains only the preexisting bounded message history; this branch does not make chat history unlimited.

## Widget capability already on main

`PersonalCopilotCloudStore+WidgetCanvas.swift` and `PersonalCopilotConfigurationFactory+WidgetCanvas.swift` implement source-card pin/drop, unique instance identity, unpin, full-surface selection, requester isolation, persisted selections, invalid/tampered drop refusal. `PersonalCopilotWidgetCanvasTests` covers these via real Cell actions and fresh store reload.

The code explicitly sets `programRows` and `statRows` to empty arrays and renders the footer “lagret kort, uten løpende oppdatering”. Live source binding (B2), purpose-derived cross-Porthole propagation (B2c), and complete full-surface content (B3) were never delivered in this slice. Widget persistence is in requester/thread `personal-copilot-cloud.json`, **not** the user's source-backed CellConfiguration. `Documentation/Operations/butler-widgetflate/CONTRACT.md:69–100` names this gap. Shipping main plus helper-tree must not be described as completion of the whole approved PDD.

## Dirty runtime packages to integrate deliberately

Primary dirty checkout: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`, HEAD `942965ca` on `pdd/tillitspakke-agentflaate`. Its HEAD is an older aggregate; use patches and new files, not copies of whole modified files over current main.

| Package | Existing dirty source and tests | Integration dependency / decision |
|---|---|---|
| Butler provider persistence and discovery cache | `Sources/App/Support/ChatScopedAIProviderRegistry.swift`; new `ChatAIGatewayDiscoveryCache.swift`; 20-line CloudStore opt-in discovery hunk; `ChatScopedAIProviderRegistryPersistenceTests`, `ChatAIGatewayDiscoveryCacheTests` | Candidate for inclusion. Uses Codable provider descriptors already present on main. Registry disk write is best-effort and does not report failures. Repeated registrations are not coordinated across processes; its comment promises more than the current cache actually guarantees. Test restart, clear and requester isolation. |
| Honest chat degradation feedback | `Public/js/porthole-webo.js` new `providerCanAnswerAsModel`, degradation banner and model-action timeout handling; `Public/css/porthole-webo.css` related additions | Candidate for inclusion with live model/non-model paths checked. The JS file also contains localization changes; split hunks and preserve current main's coalescing and helper/widget action updates. |
| Owner credentials | New `Sources/App/Cells/Credentials/OwnerScopedCredentialCell.swift`, `Support/OwnerScopedCredentialStore.swift`, `Support/CredentialSealing.swift`; `AIGatewaySupport.swift`; `WebKnowledgeCells.swift` adapter; `configure.swift` registrations; credential tests | Include as one dependency-complete bundle. Requires configured sealing master key to store actual credentials, not a generated/check-in secret. Existing ScopedCredentialAIGatewaySecretStore is in `WebKnowledgeCells.swift`, so importing only AIGatewaySupport creates missing initializer/type dependencies. |
| Remote Porthole configuration / bridgehead | New `Sources/ScaffoldKit/RemoteBridgeheadAccess.swift`; `AdminAuthenticatedVaporBridgeTransport.swift`; `PortholeWebPayloads.swift`; `PortholeWebSessionSupport.swift`; `configure.swift`; small catalog published-list change; remote tests + fixtures | Useful implemented remote lookup; checks explicit host:port and token allowlist and rebases owned references. Requires CP `RemoteCellHostRoute` APIs and compatible bridge endpoint. Retains Admin HMAC precedence. Do not combine blindly with the distinct defective default-on VaporCellBridge branch below. |
| Localization | New `Public/js/haven-localization.js` and NOTICES; JS runtime/porthole/chat/conference glue; Leaf script includes; `PortholeBootstrapProjection.swift`; localization Playwright tests | Requires CellProtocol skeleton localization API (`localizationRootKeypaths`) absent from old pins. Coordinate CP pin first. This is actual source, not generated noise. |
| Agent trust package / signed receipts / audits | Commit `1dbdee23` (19 files, WP2–7) plus current dirty AgentTrustPackage files, new `AgentTrustPackageAudit.swift`, `Sources/App/Cells/SignedCellReceiptStore.swift`, AIGateway/WebKnowledge receipt changes and receipt/audit/anti-purpose/E2E tests | Include coherent package, not isolated AIGateway hunks. Uses `@_spi(HAVENRuntime) import CellBase`, ActionDecisionReceipt signing and trust contracts; requires the corresponding CP implementation. Do not merge the 68-commit aggregate branch merely to get this one package. |
| Workbench board / detail / filter | `WorkItemCell.swift` schema v0.5, requester filter, relationships/activity/actions; `ConfigurationCatalogCell.swift` UI hunks; workbench CSS; `WorkItemCellTests`, `HavenWorkbenchConfigurationTests`, `ProductionSkeletonBindingIntegrityTests`; `scripts/workboard-smoke.js` | Candidate for inclusion, preserve all newer main catalog work. Tests should exercise filtered list, selection, status/priority actions and persistence. |
| Product Control durability | `VaporProductControl.swift` + new `VaporProductControlDurabilityTests.swift` | Candidate correctness fix: only acknowledge import after five Cell snapshots persist and reload identically. Requires resolver.persistCellSnapshot and typed store access. It is local durability, not distributed commit; code reports this accurately. |
| Palazzo runtime and branding | Corpus/service/controller dirty files and tests; full `Public/css/themes/palazzo/` assets, licenses/fonts; Concierge CSS and Gjestebrief CSS | Real package, include after its assertions and browser flow. `PalazzoConciergeRemoteService.swift` changes local bundled corpus/default/timeout behavior; do not silently treat branding as the entire change. |
| Runtime skeleton iteration | `scripts/skeleton-iterate.js`, new `scripts/tests/skeleton-iterate-configuration-keypath.test.js`, workflow docs | Candidate tooling improvement. Supports source configuration keypaths; no reason to transplant old runtime files along with it. |
| Host deployment tooling | dirty `scripts/production/haven-deploy`, `haven-deploy-sudoers`, `install.sh` | Root/deploy audit owns these; compare against current main before installation. Historical handoff says prefetch scripts are untracked, but both current untracked copies are byte-identical to main. |

Do **not** import dirty `Package.resolved` as-is: it deletes CellProtocol, DiMyMicropayments and DiMyMint remote pins, consistent with local-path development overrides. Re-resolve a deliberate remote package closure instead.

Exact already-integrated dirty files (byte comparison against baseline main): `scripts/deploy-admin-staging.sh`, `scripts/production/haven-ghcr-prefetch`, `scripts/production/haven-ghcr-prefetch-production`, `playwright/palazzo-envelope.spec.js`, `playwright/surface-load-ladder.spec.js`. These require no reimplementation.

## Other dirty worktrees with actual source

- `/Users/kjetil/.codex/worktrees/29a7/CellScaffold`: EntityPurposeLibrarySetup cell, setup contract/commit verification, PerspectiveLibraryProjection, Perspective/Spatial runtime bindings, Butler routing-context boundary changes, registration and tests. Seven modified tracked files plus untracked source/tests/docs. The change intentionally prevents a missing/denied Perspective read or library token from authorizing automatic external-model invocation. Integrate with CP Entity/Purpose work; it is not duplicated by the primary dirty checkout. Reported only as source-reviewed, not built.
- `/Users/kjetil/Build/Digipomps/HAVEN/DiMyMint/CellScaffold-session-recovery`: current `codex/scaffold-admin-staging-20260911` branch plus dirty ScaffoldAdministratorProvisioner, runtime support, registry/mandate/admin workspace UI, configure/main and tests/script. This is completion on top of admin-delegation, not interchangeable with plain branch HEAD.
- `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-bridge-identity-20260830`: dirty routes + untracked VaporCellBridge; historical version of bridge restoration. Compare with `ec437501`, do not combine two routes.
- `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-projection-20260830`: dirty ancestor-keypath Porthole projection and tests. Main already contains evolved ancestor projection; determine any test-only delta, not blind replacement. Its branch's original ancestor support was integrated historically.
- `_wt-butler-baseline-20260908` contains only untracked usefulness test/corpus. Other dirty worktrees contain reports/logs, not production source. Full list is in INVENTORY.md and worktrees.json.

## Other concrete branch packages

| Branch / commits | Recommendation |
|---|---|
| `codex/butler-20260903-helper-drag-placement-v2`, `5c5271d5` | Actual extra helper-drag placement (1,115 additions / 25 deletions in 10 files), absent action names on main. Integrate the one unique commit semantically with new WidgetCanvas/helper tree. It uses distinct `butler-helper-list`/helper-surface drop semantics and includes its own JS contract and Playwright tests. Whole branch merge would also import stale unrelated Arendalsuka/AgentRun history. |
| `codex/butler-explicit-helper-placement-v1`, `38a08add` | Older precursor. Main already has explicit helper click behavior and evolving tests. Use current v2/main behavior; review residual tests rather than overwriting CloudStore with this WIP snapshot. |
| `codex/butler-20260903-project-prompt-shelf`, `e1ccd7f8`, `65a96078`, `e9722f3e` | Real new private prompt shelf, three commits, 1,352 source lines and 482 test lines. `ProjectPromptShelfRegistration.swift` explicitly is **not called by configure.swift**, so cherry-picking alone does not expose functionality. Needs deliberate startup registration and product path validation before calling deployed. |
| `codex/developer-workbench-dependency-projection-p1`, `a3e402a0` | Real dependency projection/Workbench surface (1,535 additions), isolated source/test files plus WorkItem/catalog hooks. Integrate with board package after confirming no overlapping newer dependency projection. |
| `codex/async-app-test-20260912`, `acceb5d5` | Test-only async XCTVapor overload migration over 32 test files plus codemod tests. Useful when all-target compilation trips overload selection. Apply specific proven fixes against current tests, then run script tests; not required runtime feature. |
| `pdd/scaffold-admin-delegering` / `codex/scaffold-admin-staging-20260911` | Coherent missing administrator registry, signed mandate and authority tests; newer branch includes session recovery. Merge the newer package plus reviewed dirty completion, not both histories. |
| `pdd/tillitspakke-agentflaate` | Extract `1dbdee23` and follow-up dirty package; most other commits are preserved historical aggregate work. |
| `claude/arendalsuka-publisher-bootstrap-20260909`, `13f4440b` | Already present: full reverse-apply check succeeds against baseline main. No new merge required. |
| `losen/verk-portefolje-20260916`, `pdd/corr-varsel-recipient-feed`, `codex/entity-fabric-20260911`, `entity-link-integration`, `origin/codex/nearby-identity-link-20260911` | Root has independent open-PR / cross-repo review. Local refs differ from freshly fetched remote heads, especially correspondence and publication. Do not take stale local heads as release targets. |

## Bridge restoration defects requiring correction

`claude/bro-bridgehead-20260915` at `ec437501` adds `VaporCellBridge.swift` and route wiring, enabled by default.

1. `shouldUpgrade` calls `provenCaller`, whose `identityProvenCaller` **consumes** the replay challenge. The WebSocket handler calls `provenCaller` a second time for the same request. With signingChallengeReplayStore enabled, the second call rejects the legitimately authenticated connection as `replayed`. Cache a verified caller in request-local state or otherwise consume once. Add a real identity-proof handshake test through both callbacks.
2. `caller.identity` is only used in a log message. `bridgeConfig` and resolver registration receive the publisher identity. This code does not visibly bind the authenticated caller to command execution despite its comments. Root must trace BridgeBase's current principal enforcement and prove it with a negative test before exposing the route; this is a source-evident missing binding, not a verified exploit claim.
3. There are no branch-added tests for either path. Default-on remote admission changes need positive, replay, wrong identity and unauthorized target tests with the coordinated CP transport.

## Exact acceptance and existing test entrypoints

Host builds must follow the worktree AGENTS.md bounded runner and capacity gate. Do not invoke raw Swift builds or invent scratch directories. Relevant command shape:

```sh
scripts/check_build_capacity.sh
ci/check-value-literals.sh
scripts/run_swift_bounded.sh test --filter 'PersonalCopilotHelperTreeTests|PersonalCopilotHelperTreeReachabilityTests|PersonalCopilotWidgetCanvasTests|PersonalCopilotV1Tests|ButlerSignalMatcherTests|ButlerLatencyCachingTests'
```

Run full configured CI after focused gates; a passing old branch run is not a result for the final candidate. If the bounded script is absent in the actual checkout, root must use the documented managed build path instead of silently bypassing its safeguards.

Live browser entry: `/browserhead/webo?configurationName=Co-Pilot%20Chat&configurationEndpoint=cell%3A%2F%2F%2FPersonalChatHub` on the target. Existing `playwright/butler-explicit-helper-placement.spec.js` uses `PORTHOLE_CHAT_BASE_URL`, `PORTHOLE_CHAT_USERNAME`, `PORTHOLE_CHAT_PASSWORD`; it creates a disposable user when none is supplied and clears that user's history/surfaces. Never point its clearing setup at a real user's conversation. Desktop 1280×900 and compact 375×812 are both covered. The starter test is a **static fixture render**, not live acceptance.

Required live story for the release candidate:

1. Verify `/health/build` exact candidate SHA; authenticate a dedicated synthetic tester through the real browser route. Observe Co-Pilot Chat active and **Samtale** selected, composer visible, no critical errors.
2. Click **Tråder**, expand Butler, verify real migrated helper rows. Select a child; verify title, selected style, counts and scope; post a normal message from composer; see user and substantive response rows, correct origin chip.
3. Switch **Bare denne** / **Undertre** and back to Butler. Assert exact expected message sets and counts, no vanished history; after every action assert parent Samtale remains selected. Open/close rail on both widths and ensure composer remains usable with no horizontal overflow.
4. Create one helper result via a real prompt (existing regression uses “jeg har en ide jeg maa skrive ned: privat mappe for prosjektideer”); verify it stays in conversation until explicit open. Open **Lagre idé** as a helper without executing the domain save. Drag its source card to widget canvas; verify exactly one pin, duplicate drop remains one, cancel produces no pin. Unpin removes it.
5. Refresh/re-authenticate the same synthetic identity and verify node/scope/pin selections survive. Test server restart against staging before promoting the same immutable image to production. Assert requester B cannot see or mutate requester A's cards.
6. If a provider is used, verify a real model response and accurate degraded state when unavailable; change scope during delayed response to test provenance. A local-rule answer alone is not proof that provider chat works.
7. Capture before/after screenshots, action responses, console/page errors and selected-state DOM assertions. Widget live-data acceptance must remain failed until actual source changes propagate; no amount of pin/screenshot evidence substitutes for it.

Existing browser command shape (dedicated synthetic account only):

```sh
PORTHOLE_CHAT_BASE_URL=https://staging.haven.digipomps.org npx playwright test --config=playwright.config.js playwright/butler-explicit-helper-placement.spec.js playwright/butler-chat-mobile.spec.js
```

No current live test in the helper-tree branch drives Tråder/select/scope end-to-end. Add that test; Swift reachability cannot establish that projection/action/bootstrap UI update actually works.

## Evidence and limits

- `INVENTORY.md`: every 455 original ref and every dirty existing worktree path.
- `branches-classified.json`: ancestor, individual patch equivalence, whole-branch squash match and exact SHAs.
- `recent-commit-reverse-check.json`: non-mutating reverse checks for recent candidate patches against clean baseline main; a failed check is inconclusive when later edits changed context.
- `dirty-vs-main.json`: byte-comparison inventory of dirty primary checkout source/runtime files.
- `worktree-instructions.json`: exact AGENTS.md read from inspected worktrees.
- `dirty-main.patch`: primary checkout's preexisting tracked work delta, saved without changing it.

38 refs with apparent git-cherry additions were positively classified as already squashed into main. Examples: never-create-kept-binding → `7989c2dd`, security-consumer → `e10e93ea`, rich-document → `649255bb`, publication-cell → `83f0e364`, admin-leaf-theme → `5a29a207`, porthole-a11y → `ae268f388`, studio-copy → `9771ea07`, widgetflate → `b4a2779a`. Do not report these as missing functionality.

Remaining historical refs are inventoried, **not all semantically adjudicated or blanket rejected**. Local/remote refs include preserved disaster-recovery experiments and outdated integration branches; absence of ancestry/patch equivalence alone cannot establish a safe feature to ship. Root must finish decisions for genuinely missing packages and run the final candidate's build, tests, staging and production stories before claiming the user's “ALT” objective complete.

## Primary committed lineage follow-up

A direct `git diff origin/main HEAD -- Sources Tests Public Resources` confirmed that only the 12 AgentTrustPackage-related source/test files are new in primary HEAD. NativeLocalModelBridge, GraphStore, LiveInteraction and ConferenceLiveInteractionIntegration are byte-identical to main. Main already includes invitation landing and bridge multiplex with later security/correctness fixes. Primary HEAD would regress invitation bearer digest/retention, resolved bridge publisher UUID, bridge ready state and max-frame handling. In particular, primary AdminAuthenticatedVaporBridgeTransport retains an extra description Task that current main removed to avoid a duplicate-description race/crash. The dirty bridgehead admission hunks must be merged into current main while retaining these main safeguards. This supports cherry-picking only `1dbdee23` as the committed primary runtime prerequisite before applying reviewed dirty deltas.
