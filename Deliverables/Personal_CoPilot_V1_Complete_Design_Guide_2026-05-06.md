# Personal Co-Pilot V1 Complete Porthole/Binding Design Guide

Date: 2026-05-06

Status: canonical design guide for Personal Co-Pilot V1. This document
consolidates the current chat assistant contract, cloud-cell notes, Binding
design system, and runtime/Porthole acceptance rules into one product guide.

Visual companion guide: concrete colors, borders, radius, typography, status
styles, and Claude screenshot references live in
`HAVEN_Conference_CoPilot_Visual_Design_System_2026-05-06.md`. Treat that
document as the acceptance contract for the look and feel.

Invite Chat visual companion:
`Personal_CoPilot_Invite_Chat_Visual_Design_Guide_2026-05-06.md` contains the
human-visible reference mockup and exact visual rules for the chat/tool surface.

## Source Basis

This guide consolidates:

- `Documentation/PersonalCopilotV1_ChatAssistant.md`
- `Documentation/PersonalCopilotV1_CloudCells.md`
- `Documentation/PersonalCopilotV1_PurposeEvaluationAndPlan.md`
- `Binding/Documentation/PersonalCopilotDesignSystem.md`
- `Binding/Documentation/BindingPersonalCopilot_DesignPrompt.md`
- Current CellConfiguration skeleton rules and Porthole constraints.

## Product Thesis

Personal Co-Pilot is a private, consent-first workspace that helps a person
publish a useful public presence, discover relevant people, chat with tools,
capture ideas, and coordinate work without turning private context into a
platform feed.

The product must feel like a calm personal operating layer, not a dashboard of
everything the system knows.

## Non-Negotiable Principles

1. Local-first trust. Private context stays private unless explicitly published
   or shared.
2. Suggestion-first assistant. The assistant proposes, drafts, and explains. It
   does not mutate state without a click.
3. Purpose-interest weighting must be explainable. Scores are not enough.
4. No hidden global provider magic. AI providers are scoped to the cell,
   requester, and visible capability.
5. Porthole portability. Every core flow must work with existing skeleton
   primitives.
6. Binding enhancement. Native Binding may add navigation, inspector, scanner,
   Apple Intelligence, and permission context, but it must not hide broken
   portable surfaces.
7. Low text density. Copy exists for trust, consent, disabled states, and next
   action clarity.
8. No App Store-hostile surprises. Permissions, user-generated content,
   moderation, and agent actions must be explicit.

## Visual Direction

Personal Co-Pilot should feel lighter than the conference organizer cockpit.

Tone:

- calm
- personal
- focused
- trustworthy
- slightly editorial, not enterprise-heavy

Recommended palette:

- warm neutral base
- restrained purple/indigo brand accent
- green only for active/allowed
- amber for needs review
- red only for risk/block/revoke

Use color only as support. Every state needs a text label.

Typography roles:

- Display: personal hero and primary next action.
- Headline: section and card titles.
- Body: profile, notes, messages, drafts.
- Caption: provenance, privacy, timestamps, match reasons.

Binding style roles may include:

- `personal-hero`
- `personal-card`
- `personal-badge`
- `personal-action-row`
- `personal-draft-composer`
- `personal-match-card`
- `personal-chat-item`
- `personal-message-bubble`
- `personal-consent-prompt`
- `personal-publish-confirmation`
- `personal-audit-row`
- `personal-scanner-result`
- `personal-workflow-step`

These are progressive enhancement. The Layer 0 skeleton must still be usable
without them.

## Navigation Model

Phone Binding shell:

- Home
- Matches
- Chat
- Vault
- Profile

iPad/macOS Binding shell:

- Personal
- Network
- Workspace
- Governance

Porthole canonical tabs:

- Home
- Profile
- Directory
- Matches
- Chat
- Vault
- Workflow
- Privacy

Native shell navigation may group these, but the portable surfaces should stay
addressable and testable.

Shell mapping:

| Porthole canonical tab | Phone Binding | iPad/macOS Binding |
| --- | --- | --- |
| Home | Home | Personal |
| Profile | Profile | Personal |
| Directory | Matches | Network |
| Matches | Matches | Network |
| Chat | Chat | Network |
| Vault | Vault | Workspace |
| Workflow | Vault | Workspace |
| Privacy | Profile | Governance |

If a shell collapses multiple canonical tabs into one native destination, the
canonical surface must still be reachable inside that destination and covered by
Porthole smoke tests.

## Core Component Patterns

### Personal Hero

Purpose: orient the user and show one next action.

Contents:

- display name or workspace label
- compact status
- primary next action
- privacy state if relevant

Avoid generic greetings.

### Publish Card

Used when the user edits public profile or public artifacts.

Contents:

- what will be public
- audience
- preview
- publish button
- unpublish/revoke path where supported

Never publish automatically.

### Match Card

Contents:

- person/entity name
- title/company or role
- match reason
- relation state
- available actions

Keep row compact. Full match explanation belongs in detail.

### Chat Tool Card

Contents:

- tool title
- what it will do
- required capability/permission
- suggested because
- primary action
- dismiss

Tool cards can represent:

- invite person
- create poll
- create todo
- start project
- set reminder
- draft meeting
- request location
- query resource
- agent review request

Every tool action must map to a real action keypath.

### Consent Prompt

Contents:

- current state
- who gets access
- duration/scope
- consequence
- approve/reject/revoke actions

Use this for publishing, location, scanner identity handoff, AI provider use,
agent actions, and external sharing.

### Vault Note

Contents:

- title
- body
- source context
- owner/private state
- link to chat/thread/project if created from conversation

### Audit Row

Contents:

- event
- actor
- scope
- timestamp
- result

Audit rows should be readable, not raw logs.

## Surface Specs

### Home

Purpose: personal cockpit.

Sections:

- Next action
- Recent conversations
- Active drafts
- Matches worth reviewing
- Privacy/status summary

Rules:

- No dense dashboards.
- No global feed.
- No more than three suggestions by default.

Acceptance:

- Primary next-action `Button` maps to a real action or is hidden.
- Recent conversations list opens the selected thread.
- Active draft rows open the draft or show a disabled reason.
- Match rows open the same detail contract used by Matches.
- Empty state: one `Text` line and one optional `Button` to Profile or Matches.

### Profile

Purpose: private profile editing and public profile publishing.

Sections:

- Identity and display fields.
- Public profile preview.
- Profile image upload/reference fallback.
- Purpose and interests.
- Field visibility.
- Publish/revoke controls.

Acceptance:

- Viewer surfaces do not show edit/upload controls.
- Publish action is explicit.
- Purpose and interest changes are saved through real actions.
- Public preview uses only public fields.

### Directory

Purpose: browse public people/entities available to the user.

Sections:

- source filters
- public people/entities list
- selected detail
- relation actions

Rules:

- Directory cannot show private match explanations unless the requester has
  access to those signals.
- Nearby source appears only with capability.

Acceptance:

- Source filter list writes selected source ids.
- Directory list selection opens selected public entity detail.
- Relation buttons are hidden unless the action keypath exists.
- Nearby filter/rows are hidden when scanner capability is absent.
- Empty state: one `Text` line and optional refresh/search action if supported.

### Matches

Purpose: explainable purpose-interest recommendations.

Sections:

- filter/source selection
- recommended people/entities
- match explanation detail
- relation/action area

Acceptance:

- each match has compact "why"
- full explanation can be expanded
- action availability follows identity/proof/consent readiness

Allowed match actions:

| Readiness state | Allowed actions |
| --- | --- |
| Public profile only | open profile |
| Match explained, no relation | open profile, request contact/meeting if supported |
| Connected/relation active | open profile, send message, request meeting |
| Proof-ready | open profile, start proof chat |
| Location shared | show allowed coarse proximity/location |

Empty state:

- No recommendations: show one `Text` line and optional refresh action if the
  match cell supports it.

### Chat

Purpose: safe conversation plus explicit tools.

Sections:

- thread list
- selected thread
- messages
- compose
- assistant/tool cards
- participants/proof state where relevant

Supported V1 intents:

- invite person
- create poll
- todo
- project
- reminder
- meeting video intent
- schedule meeting
- agent action review
- moderation/report

Hard gates:

- blocked users cannot be suggested or invited
- moderation override does not execute assistant side effects
- provider use requires provider visibility/registration
- agent action requires review/signature path

Portable meeting video rendering:

- V1 renders meeting-video intent as `Text` explanation plus a `Button` with an
  external URL or provider action payload.
- No in-app video primitive is required or promised.
- If no provider URL/action exists, hide the action and keep the draft as text.

Acceptance:

- Compose `TextArea` writes to the draft state path.
- Send button maps to a real chat send action or is hidden.
- Tool cards have primary and dismiss actions.
- Poll/todo/project/reminder/meeting fields are visible only when their action
  surface exists.
- Blocked/moderated participants cannot be suggested.
- Empty state: no threads shows one `Text` line and an optional new-chat action.

### Vault

Purpose: private memory, ideas, notes, and workbench artifacts.

Sections:

- notes
- todos
- project drafts
- reminders
- links back to source chats

Rules:

- Private by default.
- Sharing/publishing uses consent prompt.
- Chat-created artifacts show source context.

Acceptance:

- Notes/todos/project draft lists open selected detail.
- Create buttons map to real actions or are hidden.
- Share/publish controls require consent prompt.
- Source chat references resolve or are omitted.
- Empty state: one `Text` line and optional create-note action if supported.

### Workflow

Purpose: lightweight workflow/project actions, not a full canvas in V1.

Sections:

- draft project
- tasks
- meeting intents
- agent review requests

No node/canvas workflow studio is required in V1. Use lists and forms.

Acceptance:

- Project/task/meeting/agent-review lists open selected detail.
- Forms write to real state keypaths.
- Create/execute buttons are hidden unless action keypaths exist.
- Agent execution always requires review/signature path.
- Empty state: one `Text` line and optional create-project action if supported.

### Privacy

Purpose: user control and audit.

Sections:

- published profile state
- active shares
- location permissions
- AI provider registrations
- agent action review history
- audit events

Acceptance:

- Active share rows open detail or show revoke action if supported.
- Provider rows show scope and can be revoked/disabled when the action exists.
- Audit rows are readable summaries, not raw JSON.
- Location permissions show scope/duration or are hidden.
- Empty state: one `Text` line for no active shares/audit events.

## Assistant Contract

Assistant read scope:

- current draft/composer
- selected thread and participants
- published profile/match metadata available to requester
- requester-scoped provider descriptors
- allowed resource metadata
- block/moderation state

Assistant must not read:

- private device capabilities unless granted
- global provider catalog
- private vault outside requester scope
- native contacts/calendar without explicit permission
- other users' private state

Confidence tiers:

- `>= 0.60`: render helper and explanation.
- `>= 0.72`: propose action.
- `>= 0.85`: prefill safe draft/helper data.

Side effects always require click.

Safe prefill means read-only preview copy, suggested titles, subject lines, and
non-sensitive helper fields. Recipients, body text that will be sent, consent
fields, provider invocation, and agent execution are never committed without an
explicit click.

Learning:

- accept writes scoped success event
- dismiss writes scoped failure event
- learning is requester/thread scoped unless explicitly designed otherwise

Learning acceptance:

- Accept/dismiss on a tool card must write a scoped event readable from the
  owning cell state.
- If weighting changes are not visible in the same session, document that as a
  deferred learning-feedback iteration rather than implying live adaptation.

## AI Provider Routing

Provider descriptors are local to the cell/requester scope:

- id
- kind
- title
- endpoint/source cell
- action keypath
- purpose refs
- interests
- availability
- privacy level
- execution scope
- requires approval
- requires network
- can invoke from chat
- score/reason

Recommendation is not invocation. Invoking a provider requires a separate
explicit action and policy check.

## Nearby, Scanner, And Location

Scanner capability is Binding/local-host specific.

Rules:

- Porthole web must not fake scanner availability.
- Scanner rows require capability-gated source.
- Nearby without identity cannot start normal chat/proof.
- Location lookup requires explicit peer permission.
- Location should be coarse and time-boxed unless a separate consent model
  says otherwise.

Personal Co-Pilot may use scanner results for:

- same-room discovery
- invite/contact request
- proof encounter export
- match enrichment after identity resolution

## Porthole/Binding Acceptance Matrix

For every Personal Co-Pilot surface:

- Porthole renders the portable skeleton with no page errors.
- Binding renders the same core content without relying on web CSS.
- All buttons point to real action keypaths.
- All text fields point to real state keypaths.
- All upload fields use `FileUpload` or documented legacy attachment contract.
- Capability-specific rows hide when unsupported.
- Disabled states explain why or are hidden.
- Assistant tool cards never auto-execute.
- Accept/dismiss writes a scoped learning event or is explicitly marked
  deferred.
- Viewer surfaces do not expose editor controls.
- Debug/action-result logs are not product copy.

## Current Implementation Boundaries

Known implemented or documented:

- `PersonalChatHubCell` chat assistant baseline.
- Deterministic V1 intent handling.
- Tool-card action surfaces for chat assistant intents.
- Provider registration/recommendation scope.
- Purpose/interest refs for assistant intents.
- Binding phase 1 design-system roles.
- Cloud-cell notes and runtime fixture routes.

Still requiring verification or implementation:

- A single staging/Porthole capture set for all Personal Co-Pilot surfaces.
- Runtime skeleton iteration for every Personal surface, not only chat.
- Binding visual parity across phone/iPad/macOS shells.
- Complete profile publish/revoke visual flow.
- Vault and workflow surfaces as clean product UI rather than raw workbench.
- Scanner and location flows with host capability and consent proof.
- App Store policy copy for provider/agent/native capability use.

## Definition Of Done

Personal Co-Pilot V1 design is complete enough when:

- this guide maps to actual CellConfiguration surfaces and screenshot artifacts
- Home/Profile/Directory/Matches/Chat/Vault/Workflow/Privacy all pass Porthole
  smoke checks
- Binding renders the same flows with native shell polish but no hidden broken
  skeletons
- assistant suggestions are explicit, scoped, and non-mutating until clicked
- public/private/published/shared states are visible in every relevant surface
- remaining gaps are tracked as implementation tickets
