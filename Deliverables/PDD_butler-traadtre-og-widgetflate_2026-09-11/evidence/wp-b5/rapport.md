Utgangspunkt: CellScaffold `pdd/skjelett-elementer-web` @ `5e8feb1ca9f26bfb6e0b5ef887e492653e0c8666` (WP-B4), CellProtocol `1b92d01a030bac424e5172c875753a1dcfe41752`.

Fixture før arbeidsflaten: `Tests/AppTests/Fixtures/ButlerBuiltIn-prewb.json`, kanonisk skjelett-digest `8cadf2b642cf3294620e79725278df6e9f066d086a50e4b5567e303b05c3a9b8` (to fabrikkkall, like).

Endring: OK: WP-B5 lagt paa (12 filer endret, 6 nye/erstattet);  21 files changed, 12399 insertions(+), 246 deletions(-). Diff: `evidence/wp-b5/change.patch`.

## Fokuserte tester

`swift test --disable-sandbox --filter 'PersonalCopilotHelperTree|PersonalCopilotWorkbench|ButlerBuiltInConfigurationUpgradeTests|PersonalCopilotV1Tests|PersonalCopilotWidgetCanvasTests|SkeletonRuntimeDecoderTests|SkeletonElementParityMatrixTests|SkeletonRuntimeSourceTests|PortholeWebPayloadTests|ChatPurposeResourceRouterTests|SkeletonStyleParityCSSDriftTests|PortholeConfigurationLoadingTests.testBootstrapUsesChatWorkbenchAsDefaultWhenCurrentConfigurationHasNoSkeleton'`: exit 1; Executed 9 tests, with 0 failures (0 unexpected) in 0.763 (0.763) seconds

```text
FEILET SkeletonElementParityMatrixTests/testMatrixRevisionMatchesPackagePin
FEILET SkeletonElementParityMatrixTests/testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips
FEILET SkeletonRuntimeSourceTests/testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning
FEILET SkeletonRuntimeSourceTests/testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis
```

## Nettleserspecer uten server (butler-chat-starter med ny dump, paritet, katalog, korpus)

exit 0 —   19 passed (13.3s) 

```text
✓   1 playwright/butler-chat-starter.spec.js:158:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › tom samtale viser startforslag, ikke en tom rute (1.1s)
✓   2 playwright/butler-chat-starter.spec.js:184:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag holder seg lesbart på mobilbredde (816ms)
✓   3 playwright/butler-chat-starter.spec.js:209:3 › Butler Chat: startforslag, hjelpelinje og Butler-svar › startforslag forsvinner når samtalen er i gang, og Butler-svaret får egen stil (945ms)
✓   4 playwright/skeleton-element-catalog.spec.js:51:3 › Skeleton element catalog › renders and operates the baseline SkeletonElement corpus on desktop and mobile (1.7s)
✓   5 playwright/skeleton-element-catalog.spec.js:174:3 › Skeleton element catalog › WP-R2 Tree: every key, cell confirmation, disclosure isolation, ID focus and ARIA (634ms)
✓   6 playwright/skeleton-element-catalog.spec.js:254:3 › Skeleton element catalog › WP-R2 Tree: focus scrolls to a visible node and survives reordered data (431ms)
✓   7 playwright/skeleton-element-catalog.spec.js:269:3 › Skeleton element catalog › WP-R2 ComponentSurface: exact R1c two-instance oracle and separate action metadata (595ms)
✓   8 playwright/skeleton-element-catalog.spec.js:294:3 › Skeleton element catalog › WP-R2 ComponentSurface: revision remount keeps instance, draft, focus and scroll (248ms)
✓   9 playwright/skeleton-element-catalog.spec.js:320:3 › Skeleton element catalog › WP-R2 M7: declared grid column, first match, capabilities and stable controls (327ms)
✓  10 playwright/skeleton-element-catalog.spec.js:351:3 › Skeleton element catalog › WP-R2 M7: fixed panel narrows, undeclared container inherits, condition and height gate (365ms)
✓  11 playwright/skeleton-element-catalog.spec.js:363:3 › Skeleton element catalog › WP-R2 M1–M6 M9 M10 R1 R7 R8: computed styles and accessible plain control (1.1s)
✓  12 playwright/skeleton-element-catalog.spec.js:404:3 › Skeleton element catalog › WP-R2 M8/R4: real drag dims source and host, marks every accepting target, cancels and drops (806ms)
✓  13 playwright/skeleton-element-catalog.spec.js:445:3 › Skeleton element catalog › WP-R2 M8 hover/focusVisible and invalid ComponentSurface diagnostic (940ms)
✓  14 playwright/skeleton-native-parity.spec.js:53:3 › WP-B4 web/native layout parity › Spacer takes the free space; a Spacer with width stays fixed (283ms)
✓  15 playwright/skeleton-native-parity.spec.js:70:3 › WP-B4 web/native layout parity › stacks fill a column; their own alignment places content, not the stack (236ms)
✓  16 playwright/skeleton-native-parity.spec.js:93:3 › WP-B4 web/native layout parity › maxWidthInfinity fills a column, maxHeightInfinity fills a row, also after a layout variant flips the axis (281ms)
✓  17 playwright/skeleton-native-parity.spec.js:117:3 › WP-B4 web/native layout parity › TextArea modifiers form one box; the field inside has no border of its own (268ms)
✓  18 playwright/skeleton-native-parity.spec.js:138:3 › WP-B4 web/native layout parity › skeleton colors win over the product-view chat log colors (245ms)
✓  19 playwright/skeleton-real-configuration-corpus.spec.js:49:3 › Named real CellConfiguration/Skeleton corpus › renders every named checked-in skeleton artifact without generic fallback (1.5s)
```

```text
```

## CI-filteret

```text
TOTALT {'started': 2435, 'passed': 2423, 'skipped': 10, 'failed': 2}
SIGNAL 0
AVBRUTT 0
KJENT -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
KJENT -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
NYE 0
```

## T-P1 hjelpertreet i arbeidsflaten

```text
  ✓  1 playwright/butler-helper-tree-purpose.spec.js:30:1 › helper tree: selecting a node scopes the log and counters (A2) (7.0s)
  1 passed (7.4s)
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

Skjermbilder: `evidence/wp-b5/bilder/`.

Endringen står ucommittet i web-worktreen (diff `evidence/wp-b5/final.patch`, sha256 d0413014e60d0fe47f5cd98ac0573f6d9e7bec99091b262bddf00dc4a8cd3b84). Commit er en egen jobb etter gjennomsyn av bildene.
