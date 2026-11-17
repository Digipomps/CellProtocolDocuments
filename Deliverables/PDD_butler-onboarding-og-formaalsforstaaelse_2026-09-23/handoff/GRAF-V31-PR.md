STATUS: LEVERT — PR åpnet (ikke automatisk merget; Kjetil avgjør)

# Formålsgraf v3.1 — PR (møte/video respekterer nektelse)

Skrevet av `HAVEN-Deploy/_handoff/BUTLER-MAALING/graf/wp-butler-graf-pr.sh` 2026-09-24T07:53:23Z. Bevis: `evidence/graf-v31-pr/`.

Ledig disk: 90 GiB.
origin/main: `60e5a64d`.
```text
M  Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift
 M Tests/AppTests/ButlerGrafRoutingTests.swift
```
- test-suite-coverage: OK (testsuiter:      337 | kjøres:      317 | unntatt:       21)
- bygg: OK (360s)
- fokuserte tester (`ButlerGrafRoutingTests|PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests|PersonalCopilotV1Tests|GuidedOnboardingCellTests|PersonalChatHubAccountCompatibilityTests`): exit 0, 195 bestått, derav 3 i ButlerGrafRoutingTests
- commit: `eb225d21` på `claude/butler-graf-v3-1-20260924`
- PR: https://github.com/Digipomps/CellScaffold/pull/258
