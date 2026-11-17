# Remaining CellProtocol dirty source — 18 September 2026

Comparison baseline is the integrated CellProtocol source used by the accepted recovery release. Exact source hashes and full diffs are retained in cp-dirty-current-comparison-20260918.json. Original worktrees were only read. No native build of these remaining drafts is claimed.

## Sources/CellBase/Cells/CellResolver/CellPersistedDataLifecycleDecision.swift

Source: `/Users/kjetil/.codex/worktrees/443a/CellProtocol`

UNWIRED_LIFECYCLE_DRAFT; preserve without activation. TTL decision store and entitlement-verifier types exist only in the new file; no runtime call sites or tests found. Activation affects retention/deletion and cannot be claimed implemented by copying isolated types.

## Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/PortholeBindingViewModel.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/visionos-20260916/CellProtocol`

NATIVE_DIAGNOSTIC_DRAFT; not ready as-is. New backside/pulse diagnostic UI is absent. refreshBackside selects/creates a private identity instead of consuming the active requester; requires current-owner integration and native permission/reload tests. Not a web Butler dependency.

## Sources/CellApple/EntityRadar/ScannerService.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/visionos-20260916/CellProtocol`

SMALL_PORTABILITY_FIX_CANDIDATE; native validation pending. Only removes unused UIImpactFeedbackGenerator stored property unavailable on visionOS. No new authority or product behavior. Native compiler currently blocked by Xcode27 license.

## Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/PortholeBackside.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/visionos-20260916/CellProtocol`

NATIVE_DIAGNOSTIC_DRAFT; not ready as-is. New backside/pulse diagnostic UI is absent. refreshBackside selects/creates a private identity instead of consuming the active requester; requires current-owner integration and native permission/reload tests. Not a web Butler dependency.

## Sources/CellBase/Cells/CellResolver/CellResolver.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-bridge-credential-20260830`

DO_NOT_MERGE_WHOLE_FILE; signed-caller draft requires paired server/replay tests. Compared with integrated source it removes master-key loading, owner binding and current scoped-signing negative tests, and restores payload logging. The novel signed-caller query additions are the already recorded unready paired package.

## Tests/CellBaseTests/BridgeTests.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-bridge-credential-20260830`

DO_NOT_MERGE_WHOLE_FILE; signed-caller draft requires paired server/replay tests. Compared with integrated source it removes master-key loading, owner binding and current scoped-signing negative tests, and restores payload logging. The novel signed-caller query additions are the already recorded unready paired package.

## Sources/CellApple/Cells/EntityAnchorCell.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol`

EXTRACT_AND_VERIFY_SEPARATELY; unready as-is. Record/store/schema additions are genuinely absent. Old EntityAnchor copies also remove current encryption, identity-link restoration/revocation/fresh-auth policy and relation validation. Wholesale copying would regress these. No matching record/store tests found in the preserved worktree Tests. Requires extraction onto current encrypted persistence with real tests.

## Sources/CellVapor/Cells/EntityAnchorCell.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol`

EXTRACT_AND_VERIFY_SEPARATELY; unready as-is. Record/store/schema additions are genuinely absent. Old EntityAnchor copies also remove current encryption, identity-link restoration/revocation/fresh-auth policy and relation validation. Wholesale copying would regress these. No matching record/store tests found in the preserved worktree Tests. Requires extraction onto current encrypted persistence with real tests.

## Sources/CellBase/Cells/Correspondence/EntityCorrespondenceRecordV1.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol`

EXTRACT_AND_VERIFY_SEPARATELY; unready as-is. Record/store/schema additions are genuinely absent. Old EntityAnchor copies also remove current encryption, identity-link restoration/revocation/fresh-auth policy and relation validation. Wholesale copying would regress these. No matching record/store tests found in the preserved worktree Tests. Requires extraction onto current encrypted persistence with real tests.

## Sources/CellBase/Cells/Correspondence/EntityCorrespondenceSchemasV1.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol`

EXTRACT_AND_VERIFY_SEPARATELY; unready as-is. Record/store/schema additions are genuinely absent. Old EntityAnchor copies also remove current encryption, identity-link restoration/revocation/fresh-auth policy and relation validation. Wholesale copying would regress these. No matching record/store tests found in the preserved worktree Tests. Requires extraction onto current encrypted persistence with real tests.

## Sources/CellBase/Cells/Correspondence/EntityCorrespondenceStoreV1.swift

Source: `/Users/kjetil/Build/Digipomps/HAVEN/sprout/implementation/entity-correspondence/CellProtocol`

EXTRACT_AND_VERIFY_SEPARATELY; unready as-is. Record/store/schema additions are genuinely absent. Old EntityAnchor copies also remove current encryption, identity-link restoration/revocation/fresh-auth policy and relation validation. Wholesale copying would regress these. No matching record/store tests found in the preserved worktree Tests. Requires extraction onto current encrypted persistence with real tests.

## Additional pure-Python checks

UniverseSimulation preserved loop-detector WIP: 19 synthetic tests passed. CellProtocolDocuments PurposePackages WIP: 29 tests passed. Skeleton-localization binding test: 1 passed. These are developer/research tools, not components to install into the web container. Their publication/research-archive closure remains separate. System git/Swift are presently blocked by the new Xcode27 license; no agreement was accepted by the agent.
