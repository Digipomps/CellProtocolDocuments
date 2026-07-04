# Chapter 19 - Chat Workbench As Central Interface

Date: 2026-05-07

This chapter documents the intended central chat architecture for
CellProtocol/HAVEN, grounded in the implementation currently present in
CellScaffold, CellProtocol, Binding-adjacent Apple cells, HAVENAgentD and Sprout
bridge contracts.

## 1. Product Role

Chat is the primary human interface for CellProtocol. It must be:

- compact enough to embed in other surfaces
- rich enough to become a full-screen workbench
- capable of discovering tools through natural language
- governed by Purpose/Interest matching and the requester's local Perspective
- safe by default: no hidden side effects, no global AI provider, no data leaks

The user writes naturally in a composer. The system translates the draft into
Purpose/Interest candidates, ranks available tools and providers, and presents
one or more helper cards. A helper card may fill draft data, but it never sends,
invites, queries a RAG, calls an AI provider, creates a module, wakes a device or
executes an agent action without an explicit user click and the relevant
CellProtocol grants.

## 2. Implemented Ground Truth

### 2.1 Chat foundation

Generic CellProtocol chat exists in:

- `CellProtocol/Sources/CellBase/Cells/Chat/ChatCell.swift`
- `CellProtocol/Sources/CellBase/Cells/Chat/ChatPresentation.swift`
- `CellProtocol/Sources/CellBase/Cells/Chat/ChatInvitationProofUtility.swift`

It has a real invitation and audience model, including invitation artifacts,
participant records, composed messages and presentation helpers.

Personal Co-Pilot chat exists in CellScaffold:

- `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCells.swift`
- `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift`
- `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift`

The `PersonalChatHubCell` currently exposes:

- composer: `setComposer`, `sendComposedMessage`, `clearComposer`
- assistant: `assistant.analyzeDraft`, `assistant.acceptSuggestion`,
  `assistant.dismissSuggestion`, `assistant.queryResource`
- provider routing: `assistant.provider.register`,
  `assistant.provider.recommend`
- invite: `invite`, `acceptInvite`, `declineInvite`,
  `assistant.setCandidateQuery`, `assistant.selectCandidate`
- poll: `poll.setQuestion`, `poll.setOptions`, `poll.create`, `poll.vote`,
  `poll.close`
- workbench helpers: `todo.*`, `project.*`, `reminder.*`, `meeting.*`
- agent review: `agent.review.*`
- moderation: `reportMessage`, `blockUser`, `unblockUser`
- UI state: `ui.setActiveTab`, `ui.setActiveMoreTab`,
  `ui.setActiveHelper`, `ui.openSuggestedHelper`,
  `ui.openComponentSurface`, `ui.minimizeComponentSurface`,
  `ui.restoreComponentSurface`, `ui.dismissComponentSurface`,
  `ui.pinComponentSurface`, `ui.setShowAdvanced`, `ui.setLearningEnabled`
- absorbed chat UI state: `absorbChat`, `releaseAbsorbedChat`,
  `setActiveAbsorbedChat`, `setCombinedChatView`
- idea capture helper: `idea.title`, `idea.content`, `idea.capture`

`ui.openSuggestedHelper` is intentionally side-effect free. It maps the current
suggestion to a helper tab without accepting the suggestion or creating a
learning event. It now also opens a chat-local component surface record so the
renderer can animate the helper into the active surface area.

`ui.openComponentSurface` is also side-effect free. It may never save an idea,
send an invite, create a poll, query RAG or enqueue an agent action.

### 2.2 Purpose and Perspective

The requester's local Purpose/Interest context is handled by `PerspectiveCell`:

- `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift`
- `CellProtocolDocuments/Book/14_Perspective_Runtime_Matching.md`

Implemented reads:

- `advertisedPurpose`
- `activePurpose`
- `perspective.state`

Implemented writes/queries:

- `addPurpose`
- `matchPurpose`
- `perspective.query.activePurposes`
- `perspective.query.interestsFromActivePurposes`
- `perspective.query.match`

Portable responses include `portablePurposeRef`, `portableInterestRef`, weights,
and supporting purposes. These are the right shape for cross-runtime matching.

### 2.3 Resource router

`ChatPurposeResourceRouter` matches a draft against:

- visible `CellConfiguration` metadata
- authenticated RAG case metadata
- safe HAVENAgentD action capability metadata

It returns metadata and scores only. It must not return local file contents,
raw Entity values, script source, shell commands, shortcut bodies or private
folder listings.

### 2.4 Cell-scoped AI provider router

`ChatScopedAIProviderRouter` ranks providers that are visible in the current
chat/cell scope:

- `local_rules`
- `apple_intelligence`
- `subscription`
- `api_gateway`
- `rag_gateway`
- `agent_bridge`
- `custom`

There is no global AI-provider catalog. A provider can be recommended only when
it is declared in the chat scope or resolved through the requester's local cell
scope. Recommendation is not invocation.

The default safety/cost preference is:

1. deterministic local rules
2. Apple Intelligence / Foundation Models on device
3. explicit RAG or owner-scoped local/remote provider
4. subscription/API model only after explicit escalation
5. AgentD bridge only as signed review request, not direct execution

Apple's Foundation Models framework is on-device and supports text generation,
structured generation and tool calling. Apple documents that it requires Apple
Intelligence to be enabled on the device. See:

- https://developer.apple.com/documentation/FoundationModels
- https://developer.apple.com/documentation/FoundationModels/LanguageModelSession
- https://developer.apple.com/apple-intelligence/whats-new/

## 3. Universal Chat Workbench Modes

### 3.1 Full-screen

Use when chat is the main task surface.

Structure:

- context bar: active cell scope, active purpose summary, privacy/provider status
- tabs: `Samtale`, `Aktivt`, `Mer`
- `Samtale`: message stream, suggestion stripe, composer
- `Aktivt`: invites, polls, tasks, projects, reminders, meetings,
  agent review requests and other created modules
- `Mer`: tools, AI/provider visibility, moderation, privacy, advanced/debug

### 3.2 Embedded compact

Use inside another CellConfiguration.

Structure:

- recent messages or last system event
- one-line composer
- one compact suggestion chip
- "Open full chat" action or reference

Embedded mode should not show full helper panels, provider lists, raw debug,
advanced purpose scores or unrelated tools. It is a portal into the full chat,
not a miniature control tower.

### 3.3 Conference context

Use when the chat is embedded in, or launched from, the conference runtime.

The chat should detect conference scope through visible cells and metadata, not
through hardcoded global state. Relevant existing cells include:

- `ConferenceUIRouterCell`
- `ConferenceOnboardingCell`
- `ConferenceSchedulingCell`
- `ConferenceConnectionHubCell`
- `ConferenceRecommendationCell`
- `ConferenceEntityDiscoveryCell`
- `ConferenceChatLaunchCell`
- `ConferenceProofChatLaunchCell`
- `ConferenceSessionThreadCell`
- `ConferenceSessionPollingCell`
- `ConferenceBroadcastStudioCell`
- `ConferencePublishedContentCell`
- sponsor/admin/participant/public shells

Conference helper cards must be role-gated and grant-gated.

## 4. Matching Pipeline

Recommended V1 pipeline:

1. User writes a draft.
2. User clicks `assistant.analyzeDraft`, or the renderer calls it only where the
   product has explicitly accepted that behavior.
3. The chat reads:
   - current draft
   - visible chat state
   - visible CellConfiguration metadata
   - accessible RAG case metadata
   - safe AgentD capability metadata
   - Perspective portable refs and weights
4. `ChatPurposeResourceRouter` returns ranked resource matches.
5. `ChatScopedAIProviderRouter` returns a provider recommendation.
6. The assistant shows a suggestion stripe or helper card.
7. User clicks an explicit action.
8. The target cell validates grants and input again server-side.

The pipeline must not:

- mutate active Perspective state silently
- query RAG silently
- call a remote provider silently
- enqueue AgentD intents silently
- expose raw Entity values, local paths or source code in autocomplete

## 5. Conference Capabilities From Chat

The chat should surface conference functionality as helper cards. Examples:

### Agenda

Prompt examples:

- "Hva skjer etter lunsj?"
- "Vis neste sesjon"
- "Legg privacy talken i agendaen min"

Implementation route:

- match against conference agenda/scheduling configuration metadata
- use `ConferenceUIRouterCell.navigate` to open the agenda/scheduling screen
- use explicit scheduling actions only after confirmation

### People matching and start chat

Prompt examples:

- "Hvem jobber med agent governance?"
- "Finn folk med privacy-interesser"
- "Start chat med Sara og Jonas"

Implementation route:

- match against `ConferenceRecommendationCell` and
  `ConferenceEntityDiscoveryCell`
- show people matches as normalized metadata rows
- call `ConferenceChatLaunchCell` only after the user clicks start chat

### Meeting request

Prompt examples:

- "Sett opp kaffe med Maria i morgen"
- "Foreslaa et møte etter keynote"

Implementation route:

- V1 uses text fields for time/place
- dispatch to scheduling/meeting request actions through conference cells
- V2 should use `DateTimePicker` when that primitive exists

### Session thread and poll

Prompt examples:

- "Aapne sesjonstråden"
- "Lag en poll om neste steg"

Implementation route:

- match `ConferenceSessionThreadCell` and `ConferenceSessionPollingCell`
- helper card opens thread or poll draft
- poll side effects require explicit create/vote/reveal clicks

### Broadcast and device wake

Prompt examples:

- "Send paaminnelse til alle om middag kl 18"
- "Vekk deltakerne for keynote"

Implementation route:

- admin/organizer role only
- match `ConferenceBroadcastStudioCell` and notification policy cells
- show delivery/wake consequences in plain language
- require explicit confirmation before sending

### Public content edit

Prompt examples:

- "Oppdater programteksten"
- "Endre sponsor-info"

Implementation route:

- organizer/admin grants only
- match `ConferencePublishedContentCell`
- use published-content setter actions
- use `FileUpload` only where the target surface supports attachment state

### Sponsor follow-up

Prompt examples:

- "Vis sponsorleads med samtykke"
- "Del min kontaktinfo med sponsor X"

Implementation route:

- sponsor scope and consent-bound data only
- locked participants remain locked
- explicit consent before any share/unlock

## 6. Apple Intelligence Integration Pattern

Apple Intelligence should be a cell-scoped provider, not a global fallback.

V1 Apple-provider responsibilities:

- classify draft intent
- map natural language to Purpose/Interest candidates
- extract structured helper-card fields
- rank already-authorized metadata candidates
- summarize why a helper is recommended in user language

Apple Intelligence should not:

- read other users' drafts
- read native contacts/calendar/files without explicit capability consent
- bypass CellProtocol grants
- execute tools directly
- silently escalate to remote API

Runtime availability must be checked separately from compile-time
`canImport(FoundationModels)`. If Apple Intelligence is unavailable, the chat
falls back to deterministic local rules and shows that richer interpretation may
require enabling Apple Intelligence or explicitly choosing another provider.

## 7. Skeleton Support

Supported now:

- `Text`
- `TextField`
- `TextArea`
- `Image`
- `Spacer`
- `HStack`
- `VStack`
- `ZStack`
- `List`
- `Object`
- `Reference`
- `Button`
- `Grid`
- `ScrollView`
- `Section`
- `Divider`
- `Picker`
- `Toggle`
- `Tabs`
- `FileUpload`

V1 can build:

- full-screen tabs
- compact embedded chat
- inline helper cards
- semantic motion through `motionHint` and `motionSourceRole`
- minimerbare component surfaces for helpers
- provider recommendation panel
- active module lists
- Ideas/Vault capture helper through `personal.chat.assist.idea.capture`
- absorbed chat references with source badges and grant checks
- conference helper cards
- RAG query button
- AgentD review-request helper

V2 candidates:

- `Sheet` for confirmation and detail panels
- sticky composer / sticky section
- `DateTimePicker`
- `ComponentSlot`
- safer dynamic conditional visibility
- richer attachment preview around `FileUpload`

## 8. Documentation Map

CellProtocolDocuments should document protocol-facing contracts:

- this chapter: central chat workbench architecture
- `PerspectiveCell` keypaths and portable matching
- `PersonalChatHubCell` state/actions
- `ChatPurposeResourceRouter`
- `ChatScopedAIProviderRouter`
- `AppleIntelligenceCell`
- `AgentD` signed review bridge
- conference integration pattern
- skeleton primitives and V1/V2 limits

DiMyDocuments should document product/commercial use:

- what the user sees
- how commercial cells may appear as tools
- payment/regulatory guardrails
- AI provider transparency
- privacy and consent language

## 9. Non-Negotiables

- No global AI provider.
- No hidden RAG query.
- No hidden remote model call.
- No hidden AgentD action.
- No raw shell, AppleScript or shortcut body from chat.
- No local file paths, file contents or Entity values in autocomplete.
- No fake buttons.
- No raw debug fields in default UI.
- Every visible helper must either be actionable or clearly explain what input
  is missing.
- Every side effect must be grant-checked by the target cell.
