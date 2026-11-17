STATUS: REGRESJON — 21 av 21 krasjer bare med WP-R; SkeletonModifiers 736 → 1312 byte, chatHubSkeletonBody-ramme 270624 → 456128 byte

# WP-R4b — stackdiagnose (fullført av skript etter Codex-kvotestopp)

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-r4b-maal.sh`. Codex-jobben `wp-r4b-stackdiagnose-20260919` stoppet 07:34Z på brukskvoten etter å ha målt main-oppsettet; resten er målt av skriptet i de samme worktreene. Revisjoner: `evidence/wp-r4b-stackdiagnose/maal-heads.txt`.

## 1. MemoryLayout (size, byte)

| Type | CP 533b42d5 (main-pin) | CP c81a3979 (WP-R) |
|---|---:|---:|
| `SkeletonAutocomplete` | 105 | 105 |
| `SkeletonButton` | 872 | 1448 |
| `SkeletonCellReference` | 1592 | 2744 |
| `SkeletonComponentSurface` | — | 1368 |
| `SkeletonDivider` | 752 | 1328 |
| `SkeletonGrid` | 808 | 1384 |
| `SkeletonHStack` | 776 | 1352 |
| `SkeletonImage` | 824 | 1400 |
| `SkeletonInteractionStyles` | — | 185 |
| `SkeletonLayoutVariant` | — | 272 |
| `SkeletonList` | 1696 | 2848 |
| `SkeletonModifiers` | 736 | 1312 |
| `SkeletonModifiers?` | 736 | 1312 |
| `SkeletonNavigationBar` | 776 | 1352 |
| `SkeletonNavigationBarItem` | 888 | 1464 |
| `SkeletonObject` | 760 | 1336 |
| `SkeletonPicker` | 880 | 1456 |
| `SkeletonPresentation` | 112 | 112 |
| `SkeletonScrollView` | 776 | 1352 |
| `SkeletonSection` | 776 | 1352 |
| `SkeletonSpacer` | 768 | 1344 |
| `SkeletonTabPanel` | 760 | 1336 |
| `SkeletonTabs` | 840 | 1416 |
| `SkeletonText` | 800 | 1376 |
| `SkeletonTextArea` | 872 | 1448 |
| `SkeletonTextField` | 928 | 1504 |
| `SkeletonToggle` | 785 | 1361 |
| `SkeletonTree` | — | 5464 |
| `SkeletonUnsupported` | 792 | 1368 |
| `SkeletonVStack` | 776 | 1352 |
| `SkeletonVisualization` | 824 | 1400 |
| `SkeletonZStack` | 760 | 1336 |

Rålogger: `evidence/wp-r4b-stackdiagnose/layout-main.log`, `layout-wpr.log`.

## 2. Stackramme fra prologen (debug, arm64), byte

| Funksjon | main e3ae9fc0 | WP-R f851df49 |
|---|---:|---:|
| `_$s3App35PersonalCopilotConfigurationFactoryO19chatHubSkeletonBody33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ` | 270624 | 456128 |
| `_$s3App8ChatCellC17chatConfiguration0C4Base0cE0VyFZ` | 83216 | 145408 |
| `_$s3App35PersonalCopilotConfigurationFactoryO21pagePublisherSkeleton33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ` | 61200 | 104976 |
| `_$s3App24ConfigurationCatalogCellC014havenWorkbenchB00D4Base0dB0VyFZ` | 63072 | 104528 |
| `_$s3App25PortholeWebSessionSupportO36adminAccessRequirementOverlaySection33_8E217E960C5926DEA0180D2904CBDA92LL8CellBase15SkeletonElementOyFZ` | 55856 | 98480 |
| `_$s3App35ConferenceShellConfigurationFactoryO17makeAdminSkeleton33_9271A8077B345B1E070A97728968B307LL8CellBase0H6VStackVyFZ` | 61280 | 96992 |
| `_$s3App25PortholeWebSessionSupportO38paymentAccessRequirementOverlaySection33_8E217E960C5926DEA0180D2904CBDA92LL8CellBase15SkeletonElementOy` | 52816 | 93136 |
| `_$s3App29EntityAnchorKeypathDescriptorV10v1Keypaths_WZ` | 92592 | 92592 |
| `_$s3App24ConfigurationCatalogCellC017ideaTaskWorkspaceB00D4Base0dB0VyFZ` | 55680 | 91408 |
| `_$s3App24ConfigurationCatalogCellC24scaffoldPurposeTemplates33_7B04337C317E4335B1BF7625E15E695DLLSayAC08ScaffoldF8TemplateAELLVGyFZ` | 89024 | 89024 |
| `_$s3App8ChatCellC08embeddedB13Configuration0C4Base0cE0VyFZ` | 48624 | 84336 |
| `_$s3App24ConfigurationCatalogCellC19retintClaudeVisuals33_7B04337C317E4335B1BF7625E15E695DLL2in10styleClass5depth0D4Base15SkeletonElementOAK` | 46736 | 81296 |
| `_$s3App35PersonalCopilotConfigurationFactoryO19chatHubSkeletonBody33_2014C9383BDE91BC5D70D4F2CF546DC6LL8CellBase0H7ElementOyFZ10helperTabsL_` | 41968 | 73072 |
| `ltmp0` | 44992 | 71488 |
| `_$s8CellBase25SkeletonReachabilityAuditO9modifiers33_5C574E1BFEB9D538488820799BE198CBLL2ofAA0C9ModifiersVSgAA0C7ElementO_tFZ` | 37504 | 71088 |
| `_$s3App24ConfigurationCatalogCellC19retintClaudeVisuals33_7B04337C317E4335B1BF7625E15E695DLL2in10styleClass5depth0D4Base15SkeletonElementOAK` | — | 8240 |

Rådata: `frames-main.json`, `frames-wpr.json` (alle funksjoner ≥ 8 KiB i App og CellBase).

## 3. CI-filteret på uendret main

Exit 1. Bolker med logg: 29. Teststatus: {'started': 2411, 'passed': 2396, 'skipped': 10, 'failed': 5}. Avbrutte tester totalt: 0. Nye xctest-krasjrapporter fra main-bygget: 0, av dem `Thread stack size exceeded`: 0.

Til sammenligning WP-R4: {'started': 1232, 'passed': 1205, 'failed': 2, 'skipped': 4}, avbrutt 21.

## 4. De 21 krasjtestene fra WP-R4 kjørt på main

| Test | På main |
|---|---|
| `-[AppTests.PortholeWebSessionPersonaTests testBootstrapConfigurationListsAreLightweightSummaries]` | bestått |
| `-[AppTests.PortholeIdentityContinuityRoutesTests testCoPilotChatLoadsWhileUnprovenHistoricalAuxiliariesRemainUntouched]` | bestått |
| `-[AppTests.AdminCopilotWorkspaceConfigurationTests testAdminOperationsWorkspaceBootstrapHydratesNodeFleetDashboard]` | bestått |
| `-[AppTests.ChatPurposeResourceRouterTests testScaffoldEntityAtlasDedupeRuntimeDuplicateByEndpointAndName]` | bestått |
| `-[AppTests.ConfigurationCatalogCellTests testCatalogContractsExposeSharedContractShapeAndParityFixtures]` | bestått |
| `-[AppTests.ArendalsukaConfigurationPublisherCellTests testPortholeCommitRuntimePersistsOfficialSkeletonAcrossFreshSession]` | bestått |
| `-[AppTests.ConferenceShellCellsTests testPortholeSessionDetailPreparesLiveThreadForSelectedPreviewSession]` | bestått |
| `-[AppTests.PortholeMenuFallbackTests testDefaultCatalogBuildsOnceWithinRequestScope]` | bestått |
| `-[AppTests.PurposeCellTests testPalazzoFixtureDecodesLosslesslyIntoPurposeModelAndConfigurationIsPublished]` | bestått |
| `-[AppTests.CellConfigurationStudioImportTests testDecodedStudioInstallsPrivateImportRuntimeBindingBeforeStateRead]` | bestått |
| `-[AppTests.ButlerSignalMatcherTests testAnalysePromptNowReachesTheAdvisoryReportHelper]` | bestått |
| `-[AppTests.ConferenceConfigurationCatalogTests testConferenceCatalogConfigurationsLoadAsWorkspaces]` | bestått |
| `-[AppTests.ConfigurationCatalogCellTests testCatalogBootstrapsRAGGatewayEntryAndExposesMenuConfiguration]` | bestått |
| `-[AppTests.ExecutablePurposeGroundingCellTests testAdvisoryPanelPromptWithoutSubjectReportsMissingContext]` | bestått |
| `-[AppTests.OrchestratorPersistenceTests testLegacyPortholeSnapshotRecoversConfigurationFromSidecar]` | bestått |
| `-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound]` | bestått |
| `-[AppTests.SwarmIdentityAdmissionCellTests testAdminObserverCatalogIncludesSwarmAdmissionOnlyForProvedRequester]` | bestått |
| `-[AppTests.PersonalCopilotHelperTreeTests testPromptSubmitRecordsSelectedNodeThroughProductionAppendPath]` | bestått |
| `-[AppTests.PersonalCopilotWidgetCanvasTests testCancelWithoutDropLeavesTheCellAndDiskUnchanged]` | bestått |
| `-[AppTests.PortholeWebRemoteConfigurationTests testBuiltInAdminNavigationResolvesLocalFactoryBeforeRemoteExportAdmission]` | bestått |
| `-[AppTests.ButlerBuiltInConfigurationUpgradeTests testNormalBootstrapAndSameSurfaceLoadPersistThreadControls]` | bestått |

Rålogger: `evidence/wp-r4b-stackdiagnose/baseline/` (swift-ci.log, ci-chunks/bolk-*.log, crash-reports.json); kommandoer: `baseline-tools/ci-commands.jsonl`.

## Merk om basislinjen

Basislinjen er CellScaffold `e3ae9fc0` **pluss** den mekaniske `App.ChatCell`-kvalifiseringen fra WP-R4 (`f851df49`) i `ConferenceEntityDiscoveryCellTests.swift` og `ConferenceShellCellsTests.swift`. Uten den kompilerer ikke AppTests på macOS/Swift 6.4: første forsøk (`baseline-attempt3-chatcell-kompilerte-ikke/`) feilet i alle 29 bolker med `ambiguous use of 'ChatCell'`, fordi CellBase også på main-pinnen 533b42d5 har en offentlig `ChatCell`. Kontroll av at diffen bare er kvalifisering: `basis2-chatcell-kontroll.txt` (endrede linjer: 11 fjernet, 11 lagt til; bare App.-kvalifisering: True). Endringen ligger bare i den detached worktreen `_worktrees/wp-r4b/scaffold-main`, uten commit.
