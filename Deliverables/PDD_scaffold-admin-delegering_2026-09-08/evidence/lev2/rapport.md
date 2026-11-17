Ledig disk: 115 GiB.
origin/main: `77a922bc301a0ea7586a6b3677a87c2b1e0f73f7`.

Endringer mot origin/main:
```text
 M Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift
 M Sources/App/Support/ScaffoldAdministratorProvisioner.swift
 M Tests/AppTests/ScaffoldAdministratorProvisionerTests.swift
 M ci/test-filter.txt
?? Tests/AppTests/GuidedOnboardingFailureReasonTests.swift
?? scripts/provision-scaffold-administrator-production.sh
 .../PersonalCopilotCloudStore.swift                | 111 ++++++++++++++-
 .../Support/ScaffoldAdministratorProvisioner.swift |  56 +++++++-
 .../ScaffoldAdministratorProvisionerTests.swift    | 157 ++++++++++++++++++++-
 ci/test-filter.txt                                 |   1 +
 4 files changed, 310 insertions(+), 15 deletions(-)
```
- test-suite-coverage: OK (testsuiter:      336 | kjøres:      316 | unntatt:       21)
- bygg: OK (362s)
- fokuserte tester (`ScaffoldAdministratorProvisionerTests|ScaffoldAdministratorRegistryTests|ScaffoldMandateTests|ScaffoldRoleIsNotAuthorityTests|GuidedOnboardingFailureReasonTests|GuidedOnboardingCellTests|PersonalChatHubAccountCompatibilityTests`): exit 0, 48 bestått
- CI-filter: exit 0; {'started': 2442, 'passed': 2432, 'skipped': 10}; nye feil/avbrudd: 0
```text
TOTALT {'started': 2442, 'passed': 2432, 'skipped': 10}
SIGNAL 0
AVBRUTT 0
NYE 0
```
- commit: `78e8e52f8b5a85bf59b82b9a6a7f5fe7953a67f3`
- push: `origin/claude/scaffold-admin-prod-og-onboarding-20260923`
- PR: https://github.com/Digipomps/CellScaffold/pull/255
