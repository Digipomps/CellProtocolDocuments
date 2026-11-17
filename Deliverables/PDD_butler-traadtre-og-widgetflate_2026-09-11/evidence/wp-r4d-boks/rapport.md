Diagnose: `STATUS: REGRESJON — 21 av 21 krasjer bare med WP-R; SkeletonModifiers 736 → 1312 byte, chatHubSkeletonBody-ramme 270624 → 456128 byte`

Utgangspunkt: CellProtocol `pdd/skjelett-elementer` @ `c81a39799c3f664d77afa5f5de131ddac70f3c9c`, ren worktree.

Endring: boksa 70 felt i SkeletonDescription.swift;  2 files changed, 500 insertions(+). Full diff: `evidence/wp-r4d-boks/change.patch`.

## CellProtocol

- `swift build --disable-sandbox`: exit 0.
- `swift test --disable-sandbox --filter SkeletonModifiersStorageTests`: exit 0; 	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
- Elementstørrelser etter boksing (byte): SkeletonAutocomplete 105; SkeletonButton 144; SkeletonCellReference 136; SkeletonComponentMount 64; SkeletonComponentSurface 64; SkeletonDivider 24; SkeletonGrid 80; SkeletonHStack 48; SkeletonImage 96; SkeletonList 240; SkeletonNavigationBar 48; SkeletonNavigationBarItem 160; SkeletonObject 32; SkeletonPicker 152; SkeletonScrollView 48; SkeletonSection 48; SkeletonSpacer 40; SkeletonTabPanel 32; SkeletonTabs 112; SkeletonText 72; SkeletonTextArea 144; SkeletonTextField 200; SkeletonToggle 57; SkeletonTree 248; SkeletonUnsupported 64; SkeletonVStack 48; SkeletonVisualization 96; SkeletonZStack 32; 
- `swift test --disable-sandbox --jobs 4` (hele suiten): exit 0; 	 Executed 1218 tests, with 1 test skipped and 0 failures (0 unexpected) in 135.516 (135.575) seconds; feilet/avbrutt: 0.

Nye feil som bare skjer med boksen: 0.

Commit: `d810720f4910c026fe61dd9fd167357a328f7476` på `pdd/skjelett-elementer` (lokal, ikke pushet).

CP-worktree etter commit (sporede filer): ren.

## CellScaffold CI-filter mot den boksa kandidaten

Bolker med logg: 30; bolker med feil/avbrudd/signal: 1. Teststatus: {'started': 2424, 'passed': 2412, 'skipped': 10, 'failed': 2}.
Avbrutte tester: 0. Nye krasjrapporter med `Thread stack size exceeded`: 0.
De 21 testene som krasjet i WP-R4 og nå består: 21.
WP-R4 til sammenligning: {'started': 1232, 'passed': 1205, 'failed': 2, 'skipped': 4}, avbrutt 21.

Feilede tester:

- `-[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]`
- `-[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]`

## Stackramme fra prologen (debug, arm64), byte

| Funksjon | main e3ae9fc0 | WP-R før boks | WP-R med boks |
|---|---:|---:|---:|
| `_$s3App35PersonalCopilotConfigurationFactoryO19chatHubSkeletonBody33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ` | 270624 | 456128 | 30272 |
| `_$s3App8ChatCellC17chatConfiguration0C4Base0cE0VyFZ` | 83216 | 145408 | <8K |
| `_$s3App35PersonalCopilotConfigurationFactoryO21pagePublisherSkeleton33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ` | 61200 | 104976 | <8K |
| `_$s3App24ConfigurationCatalogCellC014havenWorkbenchB00D4Base0dB0VyFZ` | 63072 | 104528 | 9568 |
| `_$s3App25PortholeWebSessionSupportO36adminAccessRequirementOverlaySection33_8E217E960C5926DEA0180D2904CBDA92LL8CellBase15SkeletonElementOyFZ` | 55856 | 98480 | <8K |
| `_$s3App35ConferenceShellConfigurationFactoryO17makeAdminSkeleton33_9271A8077B345B1E070A97728968B307LL8CellBase0H6VStackVyFZ` | 61280 | 96992 | 14928 |
| `_$s3App25PortholeWebSessionSupportO38paymentAccessRequirementOverlaySection33_8E217E960C5926DEA0180D2904CBDA92LL8CellBase15SkeletonElementOy` | 52816 | 93136 | <8K |
| `_$s3App29EntityAnchorKeypathDescriptorV10v1Keypaths_WZ` | 92592 | 92592 | 92592 |
| `_$s3App24ConfigurationCatalogCellC017ideaTaskWorkspaceB00D4Base0dB0VyFZ` | 55680 | 91408 | 9504 |
| `_$s3App24ConfigurationCatalogCellC24scaffoldPurposeTemplates33_7B04337C317E4335B1BF7625E15E695DLLSayAC08ScaffoldF8TemplateAELLVGyFZ` | 89024 | 89024 | 89024 |
| `_$s3App8ChatCellC08embeddedB13Configuration0C4Base0cE0VyFZ` | 48624 | 84336 | <8K |
| `_$s3App24ConfigurationCatalogCellC19retintClaudeVisuals33_7B04337C317E4335B1BF7625E15E695DLL2in10styleClass5depth0D4Base15SkeletonElementOAK` | 46736 | 81296 | <8K |
| `_$s3App35PersonalCopilotConfigurationFactoryO19chatHubSkeletonBody33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ10helperTabsL_` | 41968 | 73072 | <8K |
| `ltmp0` | 44992 | 71488 | 10848 |
| `_$s8CellBase25SkeletonReachabilityAuditO9modifiers33_5C574E1BFEB9D538488820799BE198CBLL2ofAA0C9ModifiersVSgAA0C7ElementO_tFZ` | 37504 | 71088 | <8K |

Rålogger: `evidence/wp-r4d-boks/cs-ci/` (swift-ci.log, ci-chunks/bolk-*.log, summary.json); kommandoer: `tools/ci-commands.jsonl`.

Web-worktree: `f851df4990e6da595b8daec40d34f2d6df6b3d10`; status etter kjøring (Package.resolved gjenopprettet): ren.
