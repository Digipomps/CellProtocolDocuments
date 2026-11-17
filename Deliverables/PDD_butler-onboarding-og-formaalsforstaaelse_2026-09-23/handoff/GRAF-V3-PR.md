STATUS: LEVERT — PR åpnet, venter på CI

# Formålsgraf v3 — PR

Skrevet av `HAVEN-Deploy/_handoff/BUTLER-MAALING/graf/wp-butler-graf-pr.sh` 2026-09-24T02:37:23Z. Bevis: `evidence/graf-pr/`.

Ledig disk: 98 GiB.
origin/main: `03fc0eff`.
```text
M  Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift
M  Sources/App/Support/ChatPurposeResourceRouter.swift
 M ci/test-filter.txt
?? Tests/AppTests/ButlerGrafRoutingTests.swift
```
- test-suite-coverage: OK (testsuiter:      337 | kjøres:      317 | unntatt:       21)
- bygg: OK (191s)
- fokuserte tester (`ButlerGrafRoutingTests|PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests|PersonalCopilotV1Tests|GuidedOnboardingCellTests|PersonalChatHubAccountCompatibilityTests`): exit 0, 195 bestått, derav 3 i ButlerGrafRoutingTests
- commit: `b928a27e` på `claude/butler-graf-v3-20260924`
- PR: https://github.com/Digipomps/CellScaffold/pull/257
