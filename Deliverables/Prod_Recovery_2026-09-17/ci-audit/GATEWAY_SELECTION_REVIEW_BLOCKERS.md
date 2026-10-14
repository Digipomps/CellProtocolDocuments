# Gateway/model selection review — blocking findings

Read-only review of the uncommitted candidate at `/private/tmp/haven-prod-20260917/CellScaffold`, 2026-09-18. No code, Git, build or test mutations. Line numbers identify the reviewed snapshot. Root's planned strict credential removal and recipient-display changes are excluded.

## 1. Interactive chooser is bound to policy-filtered recommendations

`Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1907` creates the interactive list with `chatHub.state.assistant.assistantProviders`; its selection action is `chatHub.assistant.provider.select`. The new unfiltered choices field exists at `PersonalCopilotCloudStore.swift:11408`, but only the old passive list (`PersonalCopilotConfigurationFactory.swift:1386`) was changed to consume it.

`recommendChatAssistantProvider` applies `enforceProviderPolicyBeforeRanking: true` (`PersonalCopilotCloudStore.swift:6532`); the filter requires a bound valid trust packet even without consent (`:9654`, `PersonalAIProviderPolicy.swift:288`). Newly discovered gateway descriptors do not carry `trustPacketRef`. Selection is what binds the matching profile packet (`PersonalCopilotCloudStore.swift:6597`). Therefore ordinary new gateway setup cannot appear in the actual interactive chooser, including when the matching packet already exists in the profile.

Minimal fix: change the interactive list's keypath to `chatHub.state.assistant.providerChoices`. Preserve invoke-time policy enforcement.

Regression: find the skeleton list by its `selectionActionKeypath` and require the choices keypath; a declared ready external gateway with no consent must be visible/selectable while invoke remains blocked.

## 2. Gateway descriptor can relabel remote execution as local and bypass consent

`PersonalCopilotCloudStore.swift:6762–6776` binds the configured route's hash and model, but does not bind its processing classification. `assistant.provider.register` accepts the caller's descriptor (`:6485`), and selection retains it. The later policy gate trusts that descriptor (`:6806`). `PersonalAIProviderPolicy.swift:254–258` permits `processingClass == .local && requiresNetwork == false` without checking the profile, trust packet or consent.

Thus the same bound provider ID/model for a real configured `openai` remote route can be registered with local classification and selected; typed routing still invokes the remote gateway with its stored owner key. The new `testNormalSendUsesSelectedGatewayRouteAndDoesNotFallBackWhenItChanges` deliberately exercises this classification override for a synthetic provider. Production discovery itself classifies every AIGateway descriptor as external (`ChatScopedAIProviderRouter.swift:295–329`), so this override is inconsistent with the authoritative route.

Minimal fix: reject non-external or non-network descriptors in the canonical gateway binding path, or replace policy-relevant descriptor fields from an authoritative current gateway descriptor before evaluation. Apply the same invariant if a gateway is reached through the local-agent fallback. Do not weaken the policy for the test double.

Regression: a valid remote gateway draft plus a local-spoofed descriptor and no external consent must produce zero provider calls. Exercise successful synthetic routing using the actual external profile/trust/consent fixture.

## 3. A consumed single-use consent becomes reusable after receipt eviction

The new confirm action issues `useScope: singleUse` and the UI promises one sending. Used consent IDs are derived exclusively from `provider_call_authorized` entries in the display receipt list (`PersonalCopilotCloudStore.swift:6801–6804`). Every rejected reuse also appends to that list (`:6816`), and it keeps only 200 entries (`:9770–9774`). The selected consent ID remains in UI state.

Concrete sequence within its 15-minute validity: one authorized send, 200 blocked attempts using that consent, then another attempt. The authorization receipt has been evicted, so the final attempt is authorized again. This is an existing ledger limitation exposed by the new one-send UI contract.

Minimal fix: persist consumed single-use consent IDs independently of bounded display receipts, or durably revoke/consume that consent before dispatch. Do not remove consumption evidence merely because display history is trimmed; also fail closed if persisting consumption fails.

Regression: one authorized call followed by more than 200 blocked reuses must still yield exactly one provider call; repeat after rehydrating state. Existing negative single-reuse coverage does not exercise eviction.
