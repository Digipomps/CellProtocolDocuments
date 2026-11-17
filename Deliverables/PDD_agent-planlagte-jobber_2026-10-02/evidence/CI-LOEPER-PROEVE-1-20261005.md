== proev-ci-loeper: 2026-10-05T19:37:05Z ==
ok  arbeidstreet står på 653fb87a0a0b43658af427f28b0e4a4c6f5f58a8
-- endret eller usporet i arbeidstreet (det som er bygget, er bygget fra dette):
    M Docs/ScheduledEvents.md
    M Sources/HavenAgentRuntime/ScheduledEventService.swift
    M Sources/HavenMacAutomation/BoundedProcessRunner.swift
    M Tests/HavenAgentRuntimeTests/ScheduledEventScheduleTests.swift
    M Tests/HavenMacAutomationTests/BoundedProcessRunnerTests.swift
-- løperen hentes fra origin/codex/file-provenance-20261002, som står på 5cf353118b1004320ca90d9ec4ffce8db250e4c6
   siste endring av de to filene der: 5dc229f 2026-10-03 13:39:10 +0200 Bound CI phases and stream compiled Swift Testing output
ok  Scripts/run_ci_phase.py: sha256 ee19cff20977782015d3583412a664f2733a41b0b6fb05de6f558953e22ba372
ok  Scripts/run_prebuilt_tests.py: sha256 f99b0ad804aa5d0c9744cf844c95952827928bdaa5de619008accbeec3174076
-- testbuntene som er bygget:
   .build/debug/HavenAgentCellRuntimeTests.xctest
   .build/debug/HavenAgentCellsTests.xctest
   .build/debug/HavenAgentDMCPTests.xctest
   .build/debug/HavenAgentMenuCoreTests.xctest
   .build/debug/HavenAgentRuntimeTests.xctest
   .build/debug/HavenCorrespondenceMCPTests.xctest
   .build/debug/HavenMacAutomationTests.xctest
-- verktøykjeden: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swift, swift-driver version: 1.168.6 Apple Swift version 6.4 (swiftlang-6.4.0.34.1 clang-2100.3.34.1)
-- kjører testfasen (grense 120 sekunder). Hele utskriften: HAVEN-Deploy/_handoff/PLANLAGTE-JOBBER/maal/CI-LOEPER-PROEVE-20261005T193705Z.log
   løperen ga kode 0 etter 28 sekunder
-- 1051 linjer utskrift, 7 bunter
   􁁛 Test run with 7 tests in 1 suite passed after 0.300 seconds.
   􁁛 Test run with 31 tests in 4 suites passed after 2.346 seconds.
   􁁛 Test run with 25 tests in 2 suites passed after 0.685 seconds.
   􁁛 Test run with 53 tests in 11 suites passed after 0.012 seconds.
   􁁛 Test run with 244 tests in 37 suites passed after 17.369 seconds.
   􁁛 Test run with 18 tests in 2 suites passed after 0.217 seconds.
   􁁛 Test run with 20 tests in 2 suites passed after 6.222 seconds.
   i alt 398 tester
   CI phase finished in 27.8s, exit 0
-- suitene og testene som er nye eller endret i PR #30:
   􁁛 Suite CronScheduleTests passed after 0.994 seconds.
   􁁛 Suite ScheduledEventScheduleTests passed after 8.112 seconds.
   􁁛 Suite ScheduledEventServiceTests passed after 0.012 seconds.
   􁁛 Suite BoundedProcessRunnerTests passed after 6.219 seconds.
   􁁛 Test aServiceThatIsLetGoOfWithoutStopTakesItsWorkerWithIt() passed after 0.069 seconds.
   􁁛 Test aRoundAskedForWhileAnotherRunsWaitsForItAndThenLooksAtTheClockItself() passed after 0.423 seconds.
   􁁛 Test startingAWorkerAgainWhileItsCommandRunsLeavesTheRunAlone() passed after 0.113 seconds.
   􁁛 Test aChangeGivesUpWhenSomeoneElseHoldsTheStateFilesLockAndGoesThroughWhenItIsFree() passed after 0.307 seconds.
-- ingen linjer med feil
-- testene som tok ett sekund eller mer:
     2.36 s  aCommandThatHangsOrFloodsIsStoppedAndTheNextEventStillRuns
     2.34 s  lifecycleControllerReconnectsAfterIngressDisconnect
     2.27 s  aCommandThatIgnoresTheRequestToStopIsRemovedAfterTheGracePeriod
     1.79 s  lifecycleControllerCapsOversizedRenewalLeadTimeAgainstShortContracts
     1.73 s  aCommandThatRunsPastTheTimeLimitIsStoppedWithEverythingItStarted
     1.30 s  theSignOfLifeCanBeHeldBack
     1.17 s  approvedToolCellNotifyWritesMarkerEmitsResultAndCleansUp
     1.06 s  timeoutProducesBlockedOutcomeAndStopsProcess
TESTFASEN ER GRØNN med løperen fra origin/codex/file-provenance-20261002, på denne Macens verktøykjede. CI bruker Xcode 26.3, og én samlet bunt.
