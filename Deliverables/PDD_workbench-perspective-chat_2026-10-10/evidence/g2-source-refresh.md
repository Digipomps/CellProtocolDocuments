# G2 source refresh — 2026-10-11

Bounded read-only observations from this Codex turn. GitHub heads were queried through the authenticated GitHub CLI; thread snapshots through Codex; target configuration through AgentD MCP. No model invoke, remote Workbench mutation, queue claim, product build/test, merge or deploy occurred. Old test numbers are not new evidence.

| Source | Observation |
|---|---|
| CellScaffold GitHub main | `9ff06f8446b6331da49272f5fd72b947b4092ece`, release metadata after GUI snapshot `7678b2c3d293978b5b179cdcada5e843f17c5b73` |
| Compared code paths | Empty `git diff --stat` between those SHAs for `Sources/App/Cells/WorkbenchHelper`, `Sources/App/Cells/WorkItems`, `Sources/App/Cells/PersonalCopilot`, `Public/js/skeleton-runtime.js`. This does not assert the whole repository is unchanged. |
| CellProtocol GitHub main | `b4100f5734bb0b3781600845a267e424e55c0989` |
| HAVENAgentD GitHub main | `a4f2db3f0a15f4446d3ee9a21ef98480ee0af878` |
| Agreement PR #314 | OPEN, draft, head `4d9d704881dfe79ceed7ee54f9bc32699ab159cd`, not merged |
| AgentD targets | Enabled; `remoteAccessVerified=false`; kjetil2-staging-work and kjetil2-staging-projects allow only state/query. Configuration does not prove live access. No new remote state call performed here. |
| CellScaffold Package.swift | Main lines 105–129: published CP exact `2026.9.7`; local override controlled by `CELLPROTOCOL_PUBLISHED_API=1`. Local override is development evidence only. |
| Thread «La PerspectiveCell reagere på Flow» | Snapshot: G1 approved, G2 plan awaiting approval, no implementation claimed. Separate owner; automatic reaction is dependency, not existing functionality. |
| Thread «Oppgrader agreement-verktøyene» | Snapshot references draft PR #314, earlier reported tests not rerun. Missing new-rights preflight/signing/onboarding must not be inferred complete. |
| Queue coordination note | HAVEN-Deploy/_losen-queue/KOORDINERING.md last-updated heading 2026-10-07. Names Losen queue coordination and Mac executor split; too old to certify today's lane/claims. No current acknowledgement obtained. |
| Existing primary checkouts | CS 364, CP 12, CPDocs 639, AgentD 28, Deploy 2919, Binding 81 status entries observed in this turn. Counts are transient inventory, not files owned by this task; do not mass-stage/clean. |
| Mac filesystem | `df -h .` reports 926 GiB size, 89 GiB available. No build capacity gate was run. No conclusion that build threshold passes. |

## Additional bounded source reads

- CellScaffold `Public/js/porthole-webo.js`, main lines 8390–8432: routed mount actions return through `runComponentSourceAction` before the ordinary `flushPendingFieldActions`. Top-level route supplies `onFieldInput` and payload hooks; this contradicts a claim that every host universally loses drafts.
- Same source lines 8920–8958, 9013–9024, 9067–9104: field storage/debounce, mount routing and root payload enrichment. Nested renderer export from approved GUI snapshot does not forward all parent input/payload hooks. Full production click path remains untested.
- CellScaffold `Sources/ScaffoldKit/ComponentActionContext.swift`: actual types are `ComponentActionMount` and `ComponentActionContext` with TaskLocal mount; comment says Meddle wire has no metadata slot.
- CellScaffold `Sources/App/Controllers/PortholeWebSessionSupport.swift`, main lines 3326–3385: local resolver requester, mount TaskLocal; nonlocal hosts and resolved BridgeBase rejected. Current SET `?? .null` is returned under `ok:true`; source code observation, not a runtime reproduction. A nil-confirmation regression case is required.
- CellProtocol `Sources/CellApple/Cells/Porthole/Utility Views/CellComponentSurfaceView.swift`, main first 130 lines: separate instance/local state, scoped native actions; missing handler produces a visible limitation. `Skeleton/Suggestion/SkeletonNativeRuntime.swift` exposes native action request/handler/scope. No `SkeletonComponentActionContext` symbol found on the inspected main.
- Book 05 explicitly distinguishes actual FlowElement fields from durable replay/signature expectations. Book 08/21 describe transport neutrality and protocol-native contact; those design descriptions are not evidence that all bridge features are implemented.

## Evidence limits

Plan metadata and source anchors were transcribed from tool outputs in the current turn; exact external receipts saved separately where available. This document is not a functional test log. Current remote login, actual model routes, write grants, provider costs, Chronicle query support, native mounted bridge round-trip, host capacity and live deployment remain unverified. Existing global PDD lesson-reference failures remain recorded in evidence/pdd-validation.txt.
