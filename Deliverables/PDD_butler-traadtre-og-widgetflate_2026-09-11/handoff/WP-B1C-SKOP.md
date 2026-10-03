STATUS: LEVERT — commit d38151d7faad0793edd211b3115f043eb1de7f87 på pdd/skjelett-elementer-web — avklaringskort og hjelpelinje følger skopet; T-P1 skjerpet og grønn; CI uten nye feil

# WP-B1c — avklaringskortet og hjelpelinja følger skopet

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-b1c.sh` 2026-09-19T12:58:10Z. Bevis: `evidence/wp-b1c/`.

Utgangspunkt: CellScaffold `ee04f722993658382864ad05463877b75e742db3`, CellProtocol `d810720f4910c026fe61dd9fd167357a328f7476`. Diagnose: `evidence/wp-b1-diag.md`.

Endring: WP-B1c lagt på i PersonalCopilotCloudStore+HelperTree.swift, PersonalCopilotCells+HelperTree.swift, PersonalCopilotConfigurationFactory.swift, PersonalCopilotHelperTreeTests.swift; T-P1-speccen måler nå også avklaringskortet og hjelpelinja. Diff: `evidence/wp-b1c/change.patch`.

## Fokuserte tester

`swift test --disable-sandbox --filter 'PersonalCopilotHelperTree|ButlerBuiltInConfigurationUpgradeTests|SkeletonRuntimeDecoderTests|SkeletonElementParityMatrixTests'`: exit 1; Executed 8 tests, with 0 failures (0 unexpected) in 0.197 (0.197) seconds

```text
FEILET SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin
FEILET SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
```

## CI-filteret

```text
TOTALT {'started': 2430, 'passed': 2418, 'skipped': 10, 'failed': 2}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NYE 0
```

## T-P1 (skjerpet)

```text
  ✓  1 playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2) (8.2s)
  1 passed (8.6s)
```

```json
{
    "baseURL": "http://127.0.0.1:9192",
    "rootRows": 2,
    "rootClarificationCards": 1,
    "rootHelpLines": 1,
    "rootInitiallyExpanded": false,
    "childCount": 16,
    "childID": "helper-invite",
    "childComposerTarget": "skriver til: Inviter",
    "childRows": 0,
    "childClarificationCards": 0,
    "childHelpLines": 0,
    "rootRowsAfterReturn": 2,
    "childrenAfterCollapse": 0
}
```

Skjermbilder: `evidence/wp-b1c/bilder/`.

Commit: `d38151d7faad0793edd211b3115f043eb1de7f87` på `pdd/skjelett-elementer-web` (lokal). Sporede endringer etter commit: 
