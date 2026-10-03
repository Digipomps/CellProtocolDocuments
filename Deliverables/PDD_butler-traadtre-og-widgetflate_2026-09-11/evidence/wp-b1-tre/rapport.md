Utgangspunkt: CellScaffold `pdd/skjelett-elementer-web` @ `f851df4990e6da595b8daec40d34f2d6df6b3d10` mot CellProtocol `d810720f4910c026fe61dd9fd167357a328f7476`.

Fixture før Tree: `Tests/AppTests/Fixtures/ButlerBuiltIn-pretree.json`, kanonisk skjelett-digest `1af1ca3a94310791f7f63eb384639c2b4065fb1f3efc8fb9a9b6695bd71b0bdb` (to fabrikkkall, like).

Endring: WP-B1 lagt på i PersonalCopilotCloudStore+HelperTree.swift, PersonalCopilotCells+HelperTree.swift, PersonalCopilotConfigurationFactory+HelperTree.swift, ButlerBuiltInConfigurationUpgrade.swift, PersonalCopilotHelperTreeReachabilityTests.swift, ButlerBuiltInConfigurationUpgradeTests.swift, PersonalCopilotHelperTreeTests.swift;  11 files changed, 13557 insertions(+), 31 deletions(-). Diff: `evidence/wp-b1-tre/change.patch`.

## Fokuserte tester

`swift test --disable-sandbox --filter 'PersonalCopilotHelperTree|ButlerBuiltInConfigurationUpgradeTests|ProductionSkeletonBindingIntegrityTests'`: exit 0; Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds

## CI-filteret (`ci/run-tests.sh`)

```text
TOTALT {'started': 2426, 'passed': 2413, 'skipped': 10, 'failed': 3}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NY -[AppTests.SkeletonElementParityMatrixTests testNamedRealConfigurationScenariosExistAndDecode]
NYE 1
```
KJENT = feilet også i WP-R4f-kjøringen mot samme CP (paritetsmatrisens revisjonssjekk). Rålogger: `evidence/wp-b1-tre/cs-ci/`.

