> Fresh-ref update, 2026-09-18: see [FRESH-REF-UPDATE-20260918.md](FRESH-REF-UPDATE-20260918.md). CP/MP recovery packages are now on main; all configured remotes were fetched by root. The historical findings below retain their original snapshot context.

# Repository integration audit — 17 September 2026

work_id: prod-recovery-20260917
slice_id: non-cellscaffold-repository-inventory
status: VERIFIED (inventory and comparisons only; not build or release acceptance)
owner: repo_inventory
integrator: root

The Claude handoff is historical evidence, not a command source. The current user's request supplies the integration/deployment objective. This worker made no Git mutations, no fetches, no deployments and no modifications to existing source. Reports and audit scripts are the only new files.

## Actionable integration order

1. **CellProtocol:** reconcile `pdd/tillitspakke-agentflaate` (`561d34a7ea785c087bd6036921f60debe6bace4a`) with current main, keeping the already integrated security/chronicle fixes. This is real missing functionality, not a stale pin alone. Add the separate bridge fixes and inspect Overlay, native parity and CellNearby below. Build/test the resulting exact commit before downstream pinning.
2. **DiMyMicropayments:** integrate issuer-bound wallets (`1a664f396917237d4bcee42dbcf58c9eb047c984`) with current main and the accepted CellProtocol revision. This branch changes wallet persistence schema and requires migration/issuer tests, not just a compile check.
3. **DiMyMint:** reconcile the substantive funding/idempotency hardening with current main. Keep current coordinated dependency revisions and isolated PostgreSQL release gate. Test migrations and payment replay against disposable data before changing the production artifact.
4. Update **CellScaffold's** complete published pin chain and lockfile from accepted upstream commits. Main at the snapshot consistently pins CP `e03923cb`, MP `c3544c2f`, Mint `25b679ba`. The primary development checkouts contain older pins; copying them wholesale would regress dependencies.
5. **Native app/daemon:** Binding, HavenAgentD and Sprout each contain real work not on main. They are separate products/artifacts, not files to bundle into the web container. Native source integration/build and installed daemon acceptance must be recorded separately from the Butler web production cutover.
6. **Palazzo and other products:** additional independently deployed functionality exists. Preserve and integrate through its own image/tests. Completing Butler web alone does not prove these independent products shipped.

The audit did not run builds or tests. Claims below say where source is present, not that it works. No unreviewed branch should be blindly merged just because it is listed here.

## CellProtocol

Snapshot `origin/main`: `36372c5b95…`. Primary checkout: `pdd/tillitspakke-agentflaate` at `561d34a7`; only documentation paths were dirty there.

The trust-package branch is 7 commits ahead and 13 behind main. Its 83 changed paths include missing CorrespondenceCell/envelopes/Agreement templates, attachment stream v1, entity relation/perspective data, identity authentication changes, radar/nearby advertisement proofs, localization, skeleton reachability, audio-analysis records, AgentTrustPackage/EffectReceipt/ReceiptSignature, and a reference-load benchmark. It also includes historical audit documentation. Main does not contain these feature symbols/files; exact file/commit lists are in the inventory.

Overlapping main changes requiring reconciliation are:

- `Package.swift`
- `Sources/CellApple/Cells/EntityAnchorCell.swift`
- `Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
- `Sources/CellBase/Cells/CellResolver/CellResolver.swift`
- `Sources/CellBase/PersistingCells/EntityRelationRecordV1.swift`
- `Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `Tests/CellBaseTests/EntityRelationRecordV1Tests.swift`

Additional candidates:

| Branch/commit | Evidence and treatment |
|---|---|
| `pdd/bridge-provenance` / `f141c53b` | Two commits changing VaporBridgeTransport and its tests. Real separate bridge authorization work; not contained by the trust branch. |
| `claude/bro-bridgehead-20260915` / `04068ac1` | Resolver and BridgeTests add signed caller proof on dedicated remote bridges. Separate from the Vapor provenance branch. |
| `claude/skeleton-overlay-20260902` / `ab5ead7d` | Adds SkeletonOverlay plus native rendering/tests; SkeletonOverlay absent from main. Review together with corresponding web renderer support. |
| `claude/parity-renderer-20260904` | Three shared feature commits are in the trust branch. Only `6218ed5` and `fa7982d` add the remaining native alignment/spacing/full-width section behavior. Avoid replaying the shared old baseline. |
| `origin/codex/entity-continuity-20260911` / `436b6a7` | New bounded Network discovery package under `Packages/CellNearby`, with CLI and tests; nine changed paths including manifest/docs. Dependencies of Binding personal-entity continuity. |
| `claude/perspective-entities-invite-20260822`, `codex/entity-correspondence-20260910`, `correspondence/s5-land-20260909` | Their feature commits are included in the trust-branch candidate. Integrate once, then establish final-main ancestry/equivalence. |

Older identity-link, scanner, strict-vault, navigation, topic-register and consumer branches are often represented by squash merges or exact patches. The machine inventory differentiates these. Security-audit branch `c5c9a4cc` is largely represented: 60/67 changed paths match main exactly; its remaining seven include security files changed further during integration. Do not overwrite accepted main with this earlier candidate.

Other dirty worktrees have genuine tracked source differences: `_wt-bridge-credential-20260830` modifies resolver/BridgeTests; the visionOS worktree modifies PortholeBindingViewModel and ScannerService; the correspondence implementation worktree modifies both EntityAnchor implementations. They are inventoried and require reconciliation, not deletion.

The earlier `CP_BYGG_561d34a_2026-09-17.md` report is **not evidence of a Swift source error**: it stopped at `sandbox-exec: sandbox_apply: Operation not permitted`, ran zero tests and referenced the primary manifest rather than its purported isolated worktree. Fresh exact-candidate compilation is required.

## DiMyMicropayments

Current remote main `c3544c2f` already contains the coordinated crypto/transport/chronicle dependency upgrade. Local main `652da700` is stale and pins older CP `135d3c00`.

`claude/issuer-bound-wallet-20260909` (`1a664f39`) is 1 ahead / 6 behind. Its nine changed files implement one issuer per wallet, mixed-bundle rejection, accepted-issuer validation, key-epoch checks, and quarantined old/foreign coin migration (schema 2 → 3). Main lacks these changes. Only `Package.swift` overlaps changes on main, so source integration is narrower than the branch's age suggests. Retain current crypto/CP pins. Its old commit message reports tests, but this audit did not re-run them.

`codex/identityunique-cellprotocol-pin-20260811` is an obsolete two-file pin choice superseded by current coordinated main; no new feature should be imported from that pin alone. Chronicle and policy pin branches are patch-equivalent or already represented. Primary untracked files are worktree directories, memory/docs and verification helpers, not hidden production Swift sources.

## DiMyMint

Current remote main `25b679ba` includes current dependency pins and the disposable PostgreSQL gate. Primary checkout `micropayments-production-hardening` at `cce8f1e8` is older, with an uncommitted lockfile; do not promote that lockfile or its branch-based dependency declarations.

There is substantial missing code: `FundingService.swift` on main has 467 lines and lacks `issueFromReservation`, `redeemWithLedger`, `reconcile`, `replayIdempotentResponse`, and `storeIdempotentResponse`. The hardening candidates have 1019 lines and those functions. `PaymentSessionCreator.swift` and `StripeWebhookSigning.swift` are absent on main and present on both `micropayments-production-hardening` and `codex/dimy-entitlement-payment-hardening-20260719` (`96e8c914`). The work adds ledger stores/models, routes, tests and SQL migrations. This is not simply stale pin noise.

Select one reconciled hardening implementation; preserve newer main routes, dependency gates and pins. Validate funding/issuance/redemption and economic idempotency plus migration behavior with disposable PostgreSQL before publishing. This audit does not authorize changing the business or regulatory model.

`codex/stripe-entitlement-provider-hardening-20260719` (`bdf0e6e9`) is mostly represented: 13 of 16 changed paths exactly equal current main. The residual differences are `.github/workflows/stripe-entitlement-provider.yml`, `docs/stripe-entitlement-provider-v0.md`, and `scripts/verify-stripe-entitlement-provider.sh`. Review those as tooling/documentation deltas, not as an entire missing payment implementation.

## Binding

Fresh remote main `285dc235` includes inspector PR #27, identity-link PR #30, dependency/test PR #31 and the daemon extraction. The primary branch `775fc93d` uses a local `../CellProtocol` package and contains 28 tracked-file changes plus many untracked paths. Most of the ~41,500 untracked paths are nested builds/checkouts under `Scripts` and `Implementation`, not independent product source. Nothing was removed.

`codex/binding-haven-complete-20260910` at `c3c823c7` is the best existing native integration starting point, now 22 ahead / 1 behind fresh main. Its clean worktree is `/private/tmp/binding-haven-integration-20260910.V2q7pH/Binding`. It already reconciles much primary app WIP, relations/contact import, invitations, persisted startup identity, remote LLM chat, relevance/catalog tests, radar, native snapshots, Palazzo surface and registration denial tests.

Its own committed `Documentation/Operations/HAVEN_Integration_Verification_2026-09-10.md` explicitly says **not release acceptance**: only syntax/plist checks passed; app compilation never completed because a resource guard interrupted dependency compilation. It also identifies public-tag-derived persisted-cell secret material in `BindingStartupIdentityVault.scopedSecretData`, with old-data compatibility unresolved. This is a concrete technical migration/test problem to solve, not grounds for claiming the branch is ready.

Fresh remote branches are additional real functionality:

- `origin/codex/entity-continuity-20260911` / `24faaff0`: reviewed/resumable QR and Network nearby entity linking, cancellation and isolated UI fixture (5 commits).
- `origin/codex/person-entity-read-route-20260911` / `71f916e9`: includes all five continuity commits and adds bounded authenticated native read transport, expiry/cancellation, reply provenance and TLS fixture (16 commits total).

Use the later read-route lineage once, then reconcile with the larger integration candidate. It requires the CP CellNearby package and corresponding server route/provenance contract.

Remaining primary untracked application sources include `BindingAuthenticatedRuntimeAttempt.swift`, `ButlerLanguageSupport.swift`, `NearbyScannerSurfaceView.swift`, their tests, ButlerConversationUITests and NearbyScannerNavigationUITests. They are not byte-identical to the examined accepted/candidate refs and need review. Exact dirty source paths and byte-equality results are in `dirty-code-inventory.json`.

Do not reintroduce the embedded `Binding/HavenAgentD` subtree: it was deliberately extracted. Compare its idle-watchdog/network changes with the standalone repository. Four Binding stashes are all preserved as exact-SHA archive refs. Two are only Xcode breakpoints; one contains NetworkSentinel code and one nearby/app work. `stashes.json` inventories their tracked and untracked payload paths; no stash was popped.

## HavenAgentD and Sprout

HavenAgentD remote main `551d37a4` already includes app-server jobs (#11), chronicle pin (#12) and menubar v2 (#14). Primary local `main` at `ba148955` is 1 ahead / 15 behind: the ahead commit is the real CorrespondenceCell-backed MCP migration, not a harmless local-main naming difference.

Missing candidates: the correspondence migration plus its dirty implementation-worktree refinements; `claude/varsler-og-behandlingssted-20260911` (correspondence waiting source, venue recommendations, disabled-notification guidance); `claude/ci-robusthet-20260911` (bounded CI, PR concurrency, logs, arm64 test invocation); and guarded private artifact workflow `24b65b92`. These should be reconciled with accepted menubar v2, not replaced by its earlier `pdd/agent-menylinje-og-varsler` branch.

`codex/app-server-mcp-bridge-20260909` is mostly already represented: 122/127 changed paths exactly match main, including runtime source. Remaining files are CI, audit documentation/tooling and dependency pins. Primary dirty AgentRuntime and DeviceActionRelay exactly match main. Several other dirty job-model/service files are earlier variants that need comparing with the accepted app-server implementation before import. The cancel-and-local-task-gate worktree contains separate dirty source in AgentRuntime, ScheduledEventService, AutomationPolicy, LocalTaskRunner and SubprocessRunner; retain and review it.

The historical D7 launch-constraint report proves a prior failed daemon launch, not the current installed artifact's state. Validate the exact newly built signed daemon if installation is part of delivery; a test-only pass does not prove launchd acceptance.

HavenAgentD main pins Sprout `d5a70f35`, but the audit's Sprout checkout and `origin/main` are `473d6998`, and the required object does not exist locally. Fetch Sprout before choosing any dependency or judging its dirty source. Dirty Sprout includes onboarding CLI/HTTP/dialogue/profile/doctor, bounded HTTP responses, private-state and identity recovery, release guards and tests. These are real code candidates; the six-file presence-seed/archive branch is not the whole dirty feature set. The coordinator was notified of this freshness gap.

## Other repositories and documentation

| Repository | Disposition with evidence |
|---|---|
| CellProtocolDocuments | Primary `codex/docs-cleanup-20260810` and multiple separate feature/research branches contain substantial committed and uncommitted Book/catalog/Tools/Deliverables work. These are docs/RAG/public-site artifacts; reconcile catalog plus new chapters before advancing the server's document submodule. Preserve research/media artifacts and inspect publish scope. One stash is preserved under exact-SHA archive refs. |
| HAVEN-Deploy | Local-only `main`, no remote. 635 dirty paths are mainly handoff/queue/evidence, plus 17 code/config candidates (test suite and tools). Local queue/workbench/menubar tooling belongs on the operator machine according to its AGENTS.md, not inside the server image. Do not bulk commit generated index DB or promote unchecked handoff scripts. Root owns queue mutation and deployment workflow. |
| PalazzoScaffold | Clean `pdd/palazzo-2026-09-14` (`fed2a202`), five unique commits / 61 changed paths: native web facade/static UI, health/build routes, image workflow, Linux OpenCombine fix. Genuine separate image candidate requiring its own build/functional deployment evidence. Includes large historical failed GUI artifacts; source presence does not prove GUI acceptance. |
| PyPalazzoConciergeScaffold | `f0fe0958` adds seven guardrail/deploy/source/test paths versus main. Dirty paths are digest/evidence output. Separate service candidate; not included by CellScaffold image. |
| CellUtility | `b25841d3` runtime-readiness/recovery branch has 15 changed paths absent from main. Separate package candidate; assess consumer dependency before publication. |
| DiMyDocuments | `386ee395` commercial-rules/value-redistribution/hardening docs and archive work are not all in main. One untracked diagram. Documentation scope, not web runtime source. |
| UniverseSimulation | Research branch `408c00b0` has 67 changed paths and tracked verification/loop-detector WIP. Separate research archive/site/RAG closure policy; must not be silently asserted delivered by Butler deployment. Keep pending or complete its own closure with evidence. |
| DiMy Source Editor Extension, DiMyDevRAG, GoCellProtocol, HAVEN_MVP, PyCellProtocol, RustCellProtocol, SpatialRegistryScaffold, SwiftWebScaffold, WatchPong | Clean primary worktrees and all known refs reachable from their local remote main. No missing source found in this snapshot; remote freshness still needs verification if asserting exhaustive current remote coverage. |

## Verification and limits

Executed read-only status before inspection, complete local+remote ref enumeration, all registered worktree statuses, stash payload-path inventories, ahead/behind ancestry, git-cherry patch equivalence, exact changed-path endpoint equality and selected source-symbol comparisons. The scripts preserve evidence as machine-readable JSON/TSV. No mutation outside this report directory occurred in this slice.

A no-common-ancestor history is explicitly flagged instead of treating a failed triple-dot diff as empty. Old archive/history branches may contain overlapping or genuinely missing work; the audit does not declare them discarded. The branch table gives each ref a review state and candidate containment. No claim is made that every old divergent-history line has received a semantic review. Ignored files, private credential contents and live user data are outside this read-only source audit.

Next dependency: integrator completes exact-candidate source reconciliation, build/tests, published pins, main/CI and production user-path acceptance. Preserve this report's snapshot boundary when appending completion receipts.
