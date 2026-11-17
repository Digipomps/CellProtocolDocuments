# Trust approval gate failure — read-only diagnosis

Source reviewed at candidate `/private/tmp/haven-prod-20260917/CellScaffold`; failing evidence is `logs/swift-gates.log`, batch 28, around lines 73581–73585. No test/build or code change was performed by this auditor.

The first failure is `approval_commit_invalid` in `AgentTrustPackageCell.approve`, after calling `signedAgreementEntity.commit`. Subsequent `package_not_approved`, missing history, audit and model-effect errors are consequences. The source fixtures already create real proof-capable test identities, bind their default vault, and register real CellVapor EntityAnchor instances. Weakening owner/signature checks or giving a blanket test authorization is not appropriate.

`Sources/ScaffoldTestKit/IsolatedCellTestCase.swift:42` resets `CellBase.persistedCellMasterKey = nil` for every test. The four trust fixtures construct `CellVapor.EntityAnchorCell` directly, without the host's key-first storage initialization. In CP `Sources/CellVapor/Cells/EntityAnchorCell.swift:644–664`, first-load storage initialization catches a write failure and retains it in `persistenceFailureReason`. A later signed agreement commit then cannot persist. The approval wrapper reduces this commit error to `approval_commit_invalid`.

The existing passing regression `AgreementWorkbenchCellTests.testOwnerSigningPersistsThroughEntityAnchorAndProjectsOnlyVerifiedRecord` explicitly sets `CellBase.persistedCellMasterKey = Data(repeating: 0x7e, count: 32)` before constructing the anchor, with the comment that direct EntityAnchor construction needs the same key-first setup as a host. This is the applicable fixture pattern.

Smallest correction: provide a known 32-byte **test-only** persistence key before constructing any anchor in these fixtures, preserving the base's per-test reset and teardown:

- `AgentTrustPackageApprovalTests.swift`, fixture anchor at line 46.
- `AgentTrustPackageAuditTests.swift`, fixture anchor at line 58.
- `AgentTrustPackageE2ETests.swift`, fixture anchor at line 53.
- `AgentTrustPackageAntiPurposeTests.swift`, fixture anchor at line 61.

Prefer placement in each fixture before anchor construction, or an async setup that calls the base first. No production default key, encryption bypass, signature relaxation or commit-success override is needed. Existing owner-denial, tamper, revocation and failed-persistence tests must retain their expectations.

Root should first rerun the single signed snapshot approval test, then these four suites. If approval remains invalid, split the response diagnostic into `commit.status`/`commit.error`, receipt verification and snapshot-equality results without logging keys or complete records. This audit establishes the missing fixture key by source; the corrected execution result remains to be observed by root.

Separate failures in the same batch refer to external CPD fixture paths; root is handling their repository-local relocation. They do not explain the initial approval denial.
