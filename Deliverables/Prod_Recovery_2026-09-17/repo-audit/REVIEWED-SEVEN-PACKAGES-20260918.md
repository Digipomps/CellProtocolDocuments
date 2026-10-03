# Source decisions for seven conservative inventory leads

Measured main: `988eb9d7a4c1f968c59213eaf818f365b862f7bc`. These are INN decisions, not a claim that all live user stories are accepted. Original branches and dirty worktrees remain preserved.

## claude/f76-provision-root-repair-20260819

Head: `1b0f30a84d9de1db5481a7415cb3c0a14e7f5ce9`. Decision: **INN**, carried by HD-0100.
Root-owned vault mirror, provision-root repair and mutation-only strike charging are present in newer main implementations. Preserve newer descriptor/file protections; no wholesale old-script replacement.

Changed paths reviewed against newer integration: `scripts/cellscaffold-runtime-secrets.py`, `scripts/deploy-staging-atomic-v3.py`, `scripts/tests/test_cellscaffold_runtime_secrets.py`, `scripts/tests/test_deploy_staging_atomic_v3.py`

## codex/admin-transaction-20260918

Head: `975de19556d2085b53a428c09ecf43763de48fa9`. Decision: **INN**, carried by HD-0100.
The accepted integration matches except newer PR248 operator pacing/rollback changes; remaining application changes are newer Butler asynchronous branch-origin preservation and WorkItem durability regressions. Accepted runtime is in web release87256f9a; actual final admin promotion remains HD0100/0101.

Changed paths reviewed against newer integration: `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift`, `Sources/App/Cells/WorkItems/WorkItemCell.swift`, `Tests/AppTests/PersonalCopilotV1Tests.swift`, `Tests/AppTests/WorkItemCellTests.swift`, `playwright/butler-explicit-helper-placement.spec.js`, `scripts/production/haven_deploy_admin.py`, `scripts/tests/test_haven_deploy_admin.py`

## codex/entity-fabric-20260911

Head: `fe9b1449a99b3a8a516228d9f7f004156414babc`. Decision: **INN**, carried by HD-0100.
37 runtime/test files match; changed Porthole, configure and document-browser files retain newer integrated fixes. Server/native device acceptance is tracked separately; no claim of actual physical-device acceptance.

Changed paths reviewed against newer integration: `Public/js/porthole-webo.js`, `Sources/App/configure.swift`, `playwright/rich-document-live.spec.js`

## codex/nearby-identity-link-20260911

Head: `746e66ee3e1d84d2eadc86febf6817df22f9ce3f`. Decision: **INN**, carried by HD-0100.
Seven runtime/test files match and five retain newer owner-resolver, signed read-route and persistence protections. Existing source is accepted; physical nearby enrollment remains unverified.

Changed paths reviewed against newer integration: `Sources/App/Controllers/VaporIdentityLink.swift`, `Sources/App/Support/PersonEntityLinkEvidenceStore.swift`, `Sources/App/configure.swift`, `Tests/AppTests/PersonEntityLinkCompletionTests.swift`, `Tests/AppTests/PersonEntityLinkEvidenceStoreTests.swift`

## losen/verk-portefolje-20260916

Head: `ceccccae58576b408ec522a8a7ff6823893692e0`. Decision: **INN**, carried by HD-0100.
Eight runtime/test files match. Three changed files add the accepted data-preserving legacy /verk URL fix and its regression coverage. Preserve published legacy behavior.

Changed paths reviewed against newer integration: `Sources/App/Cells/Publication/PublicationCell.swift`, `Sources/App/Controllers/VaporPublication.swift`, `Tests/AppTests/PublicationCellTests.swift`

## pdd/butler-hjelpertre

Head: `022cc257fdeb3e4042bf7fa3d3fe07a61bde6f83`. Decision: **INN**, carried by HD-0100.
Seven runtime/test files match; four changed files contain newer model consent, asynchronous reply-placement and mobile composer fixes. The source is in web release87256f9a. Saved built-in configuration migration is HD0106; actual account UI acceptance remains open.

Changed paths reviewed against newer integration: `Public/css/porthole-webo.css`, `Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift`, `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift`, `Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift`

## pdd/corr-varsel-recipient-feed

Head: `5aef9a3cbeabe3f85d16769ce75ec276110375bc`. Decision: **INN**, carried by HD-0100.
Both runtime and regression test files are byte-identical to accepted main; only branch documentation differs. Keep existing recipient-scoped feed; no duplicate source integration.

No runtime/test divergence.
