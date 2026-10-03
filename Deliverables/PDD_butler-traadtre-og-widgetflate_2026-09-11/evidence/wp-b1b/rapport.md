Utgangspunkt: CellScaffold `f851df4990e6da595b8daec40d34f2d6df6b3d10` med WP-B1 ucommittet (10 filer, som wp-b1-tre etterlot), CellProtocol `d810720f4910c026fe61dd9fd167357a328f7476`.

Hvorfor en andre runde: første CI-kjøring (`evidence/wp-b1-tre/cs-ci/klassifisering.txt`) fant én ny feil, `testNamedRealConfigurationScenariosExistAndDecode` — «personal-invite-chat runtime catalog skeleton must pass portable decode». `SkeletonRuntimeDecoder` hadde en hviteliste uten Tree og ComponentSurface. Den brukes av `PortholeWebSessionSupport` og `VaporBrowserhead` for arbeidsskjeletter, preview og commit, så hullet ville også stoppet dem i produksjon.

Dekoder: allerede lagt på; ingen endring. Diff: `evidence/wp-b1b/dekoder.patch`.

## Fokuserte tester

`swift test --disable-sandbox --filter 'PersonalCopilotHelperTree|ButlerBuiltInConfigurationUpgradeTests|ProductionSkeletonBindingIntegrityTests|SkeletonRuntimeDecoderTests|SkeletonElementParityMatrixTests'`: exit 1; Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds

```text
FEILET SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin
FEILET SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
```
Kjente (revisjonssjekken i paritetsmatrisen, retter seg når CP er merget og pinnen løftet): SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips

## CI-filteret (`ci/run-tests.sh`)

```text
TOTALT {'started': 2429, 'passed': 2417, 'skipped': 10, 'failed': 2}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NYE 0
```
KJENT = feilet også i WP-R4f-kjøringen mot samme CP. Rålogger: `evidence/wp-b1b/cs-ci/`.

Commits på `pdd/skjelett-elementer-web` (lokale, ikke pushet): `8cf33c11783b8a90822164f889a7052f736ca658` runtime-dekoderen, `c0997b1763e8e08dc376dc132f6a6c19c8db4b33` hjelpertreet. Sporede endringer etter commit: 
