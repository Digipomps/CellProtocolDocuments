# Conference Complete Porthole/Binding Design Guide

Date: 2026-05-06

Status: canonical design guide and acceptance contract. This document describes
the intended conference product experience and the portable UI contract for
Porthole and Binding. It is not a claim that every item is already implemented
on staging. Current staging gaps are listed explicitly in
`Porthole_Binding_GUI_Parity_Audit_2026-05-06.md`.

Visual companion guide: concrete colors, borders, radius, typography, status
styles, and Claude screenshot references live in
`HAVEN_Conference_CoPilot_Visual_Design_System_2026-05-06.md`. Treat that
document as the acceptance contract for the look and feel.

## Source Basis

This guide consolidates:

- Claude conference redesign direction and follow-up UX critique from April and
  May 2026.
- Current CellScaffold conference documentation in `Documentation/`.
- Current CellScaffold conference cells and shell factory.
- Porthole screenshots and tab-click captures from staging on 2026-05-06.
- Binding Personal Co-Pilot design system conventions where they affect
  Porthole parity.
- CellConfiguration skeleton authoring rules: use existing portable primitives,
  prefer `FileUpload` for new upload surfaces, and treat `styleRole` as
  progressive enhancement only.

Primary implementation references:

- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceParticipantShellCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceAgendaCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceAdminShellCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferencePublishedContentCell.swift`
- `Sources/App/Cells/ConferenceMVP/ConferencePublishedContentCatalog.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceEntityDiscoveryCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceProofChatLaunchCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceConciergeCell.swift`
- `Sources/App/Cells/ConferenceMVP/Skeleton/ConferenceShellConfigurationFactory.swift`
- `Public/js/skeleton-runtime.js`
- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

## Product Thesis

The conference is four rooms that share one published truth:

- Public is the invitation.
- Participant is the day workspace.
- Organizer is the control tower.
- Sponsor is the consent-gated follow-up pipeline.

The design must make boundaries visible without turning the product into legal
paperwork. A user should always understand:

- what they can do now
- why a recommendation or tool is shown
- who owns the data
- which action will mutate state
- which capability is unavailable on the current host

## Non-Negotiable Design Principles

1. Porthole first. The core flow must work as plain `Tabs`, `Section`, `List`,
   `Grid`, `VStack`, `HStack`, `Text`, `Button`, `Toggle`, `TextField`,
   `TextArea`, `Image`, and `FileUpload`.
2. Binding parity second, not last. Binding may provide native shell polish, but
   it must not be required for the core task.
3. No dead controls. Every button, text field, toggle, upload field, list
   selection, and reference must map to a real state path or action path.
4. No fake capability. Nearby, location access, proof chat, upload, sponsor lead
   access, and tool execution must only appear when the shell can support the
   action.
5. Suggestion-first assistant. Co-pilot/tool cards can draft and explain. They
   cannot send, invite, publish, unlock, mutate consent, or start projects
   without an explicit click.
6. Low text density. Keep copy short. Use explanation only for consent,
   disabled states, match reasons, ownership, and tool effects.
7. Use visual hierarchy, not card spam. Cards are for units of meaning; lists
   are for sequences; tabs are for sibling modes.
8. Debug output is not product UI. Action toasts such as "Kjorte
   shell.navigation.setActiveTab" must not appear in finished conference flows.

## Portable Visual System

### Shared Tone

The product should feel calm, efficient, and serious enough for professional
events without becoming a dense admin dashboard everywhere. Every surface should
have one dominant moment:

- Public: editorial hero and registration handoff.
- Participant: "Now / next" day cockpit.
- Organizer: operational status and risk.
- Sponsor: lead state and consent trail.

### Surface Tone

| Surface | Tone | Density | Accent intent |
| --- | --- | --- | --- |
| Public | Editorial, open, inviting | Low | CTA and featured program |
| Participant | Focused, personal, calm | Medium | next action and match confidence |
| Organizer | Operational, compact | High | status and risk |
| Sponsor | Compliance-first pipeline | Medium | unlock/reclaim state |

### Typography Roles

Use four semantic roles only:

- Display: hero titles, current session, KPI values.
- Headline: section titles, card titles, selected entity names.
- Body: descriptions, abstracts, chat/message bodies.
- Caption: metadata, time, provenance, status, match reason, consent summary.

If `styleRole` is ignored, the hierarchy must still be readable through
position and structure.

### Color And Status

Status must never depend on color alone. Always pair color with text:

- `Live`
- `Draft`
- `Pending`
- `Expired`
- `Proof ready`
- `Consent active`
- `Consent required`
- `Locked`
- `Reclaim required`

Recommended semantic palette:

- Public: warm amber/coral accent for registration and featured program.
- Participant: teal/calm blue accent for current session, saved sessions, and
  next actions.
- Organizer: operational blue accent for live/control actions.
- Sponsor: muted blue-grey accent with red reserved for reclaim/redaction.
- Shared status: green for allowed/live, amber for draft/pending, muted grey for
  unavailable/expired, red for error/reclaim, indigo for proof-ready.

### Binding Style Roles

Conference-specific Binding style roles may be used as progressive enhancement:

- `conference-hero`
- `conference-status-band`
- `conference-section-header`
- `conference-card`
- `conference-session-row`
- `conference-track-filter`
- `conference-person-row`
- `conference-nearby-row`
- `conference-tool-card`
- `conference-consent-card`
- `conference-kpi-card`
- `conference-lead-row`
- `conference-content-editor`
- `conference-diagnostic`

These roles are not a theme engine. If Binding ignores them, the skeleton must
still be usable.

## Navigation Contract

Top-level navigation is `Tabs` for every shell. Do not make side rails required
for primary navigation.

Public tabs:

- Home
- Program
- People
- Articles
- Facilities
- Register

Participant tabs:

- Today
- Agenda
- People
- Chats
- Meetings
- Profile

Organizer tabs:

- Overview
- Content
- Audience
- Live
- Insights
- Sponsors
- Simulation
- Operations

Sponsor tabs:

- Pipeline
- Consent
- Unlock
- Follow-up

Tabs must work in Porthole and Binding. Tab changes may be logged internally,
but action-result debug text must not be rendered as page content.

## Core Component Patterns

### Action Button

Every `Button` must have:

- short verb label
- mapped action keypath
- payload shape documented by the owning cell
- disabled reason if unavailable

Avoid vague labels such as "Continue" unless the next target is visually
obvious.

### Form Field

Every `TextField` and `TextArea` must have:

- label
- bound state keypath
- save/apply action or live editing contract
- validation/error display if the source cell can reject the value

### Upload Field

Use `FileUpload` for new portable upload surfaces. Legacy `AttachmentField`
may remain where already implemented. Upload surfaces must include:

- current preview/reference where available
- replace/remove actions where supported
- upload state
- URL/reference fallback if the host cannot upload
- alt text for public images

Do not show upload controls in public viewer surfaces.

### List With Selection

`List.selectionMode = multiple` is the correct portable pattern for track and
source filters. It must write selected ids to a documented state path.

`List.selectionMode = single` opens detail panels for sessions, people, chats,
meetings, leads, content items, and access requests.

### Tool Card

Tool cards are assistant proposals, not hidden commands. They must show:

- what will happen
- what data/capability is needed
- why it is suggested
- primary action
- dismiss action

No tool card may mutate state automatically.

### Consent Or Access Card

Use this when a user is being asked to grant access, location, sponsor capture,
organizer insight, or proof-backed visibility. Show:

- current state
- who gets access
- duration if time-boxed
- consequence
- revoke or do-not-share path

### Match Row

Match rows should show a compact reason:

- score, if meaningful
- purpose hits
- interest hits
- shared context
- source: recommended, shared relation, public profile, nearby

Full explanation belongs in detail, not every row.

## Public Surface

### Purpose

Public is a product landing surface. It must not feel like an internal
participant dashboard.

### Home

Structure:

- Hero with conference name, date, venue, and one primary CTA.
- Featured tracks.
- Featured people.
- Latest articles.
- Facilities summary.

Rules:

- No participant-private agenda.
- No consent controls.
- No internal cell/debug labels.
- Registration CTA must hand off to a real route/action or clearly mark the
  handoff.

### Program

Structure:

- Track list.
- Session list filtered by selected track.
- Session detail.

Rows:

- time
- title
- track
- speaker
- location

Public program rows are read-only. Saving belongs to participant agenda.

### People

Show published person slices only:

- image if public and available
- name
- title/company
- public bio or talk relation

No private match score or participant-specific proof readiness on the public
surface.

### Articles

Article list and detail must support:

- title
- subtitle/excerpt
- author
- hero image/reference if published
- body

Article editing belongs to Organizer Content, not public.

### Register

Registration must be a simple handoff. If the full registration cell is not
mounted, the UI should say "Register" and route/handoff, not pretend to submit
to a missing action.

Portable contract:

- Preferred action: `conferencePublicShell.registration.openRegistration`.
- If registration is external, use a `Button` with URL payload and a one-line
  disabled reason when the URL is not configured.
- If neither action nor URL exists, hide the submit-style control and show one
  short handoff message.

## Participant Surface

### Today

Today answers "what should I do now?"

Sections:

- Now
- Up next
- Suggestions
- People to meet
- Pending requests

Rules:

- Suggestions: maximum three by default.
- Every suggestion must be actionable or dismissible.
- Avoid welcome copy and long explanations.
- Show only current/next context; deep browsing belongs in Agenda and People.

### Agenda

Agenda must support all of this:

- multi-select tracks
- show selected/saved sessions
- show recommended sessions
- show all sessions
- save/unsave session
- open session detail
- open thread/poll when active

Portable structure:

- `Section "Tracks"` with multi-select `List`.
- Nested `Tabs`: `Selected`, `Recommended`, `All`.
- Detail section below selected row.

Acceptance:

- Multi-track selection updates the lists.
- Selected tab only shows saved sessions.
- Recommended tab includes concise reason.
- All tab respects focused tracks when selected.
- Toggle save/unsave points to real agenda action.

### People

People is one list with capability-gated sources:

- recommended
- shared relation
- public profile
- nearby only when supported

Rules:

- Web/staging must not show fake nearby as a normal participant feature.
- Diagnostic nearby workbenches may show unavailable scanner state, but should
  be labelled as diagnostics.
- Actions appear in detail, not every row, to keep rows clean.
- Proof chat action appears only when proof readiness is ready.
- Location lookup appears only when peer has explicitly granted access.

Implementation references:

- `ConferenceEntityDiscoveryCell` supplies discovery rows, nearby-merged rows,
  source labels, match summaries, and capability-gated source state.
- `ConferenceProofChatLaunchCell` supplies proof-readiness state and proof-chat
  start actions for selected candidates.

Detail actions:

- open profile
- send message
- request meeting
- start proof chat when ready
- request location access when supported
- send nearby invite when scanner can support it

Empty state:

- No matches: show one `Text` line and a `Button` to refresh discovery if that
  action exists. If refresh is unavailable, show only the text.

### Chats

Chats is a unified inbox:

- direct
- proof
- sessions
- group

Structure:

- thread tabs/filter
- thread list
- selected thread
- messages
- compose area
- suggested tools

Tool examples:

- save note
- start project
- draft meeting request
- request location access
- find nearby people
- draft follow-up

Every tool must be an explicit card with a real action keypath. Chat must not
silently execute tools from natural language.

### Meetings

Meetings lifecycle:

- suggested
- requested
- pending
- confirmed
- follow-up

Detail must show:

- counterparty
- purpose
- time/location
- agreement state if accepted
- shared follow-up thread
- accept/decline/reschedule/export actions when supported

If an action has no real keypath, hide the control. If it is temporarily
unavailable, show it disabled with a one-line reason.

Empty state:

- No meetings in the selected lifecycle tab: show one short `Text` line and a
  `Button` to open People if navigation/action support exists.

No calendar grid is required for MVP. Use lists.

### Profile And Privacy

Profile editor must support:

- profile image upload/reference fallback
- display name
- title/company
- bio
- purpose and interests
- per-field visibility where supported
- public preview

Privacy must show:

- consents
- active access
- visibility policies
- revoke actions where supported

Public profile viewer must never show upload/edit controls.

## Organizer Surface

### Overview

Overview is the control tower:

- status band
- KPI cards rendered as a small `Grid` of `Text` cards
- live operations
- alerts/suggestions
- topic intensity as text/`Grid` fallback

Rules:

- Avoid chart placeholders.
- Keep the first screen actionable.
- Show provenance where aggregate signals depend on consent.

### Content

Content is a compact CMS:

- Landing
- Tracks
- Sessions
- People
- Articles
- Facilities

Each tab should show a list and selected editor. Editor fields must be connected
to draft state/actions. Media fields use `FileUpload` or existing attachment
contract plus URL/reference fallback.

Acceptance:

- add/remove works where actions exist
- reorder appears only where action exists
- publish/discard actions are visible and real
- image fields do not appear if neither upload nor URL/reference is supported

### Audience And Access

Audience must distinguish:

- interesting cohort
- readable cohort
- access requested
- access approved
- access expired

Never show raw participant-private data to organizer.

### Live

Live supports:

- active sessions
- session thread moderation
- polls
- broadcasts

Every moderation and broadcast button must map to real actions. Live update is
expected through subscription or refresh; if subscription is missing, do not
pretend it is real-time.

### Insights

Insights show aggregate KPIs and provenance:

- consent coverage
- fallback/proxy usage
- topic signals
- trend text

No chart primitive is required. If charts are introduced later, they must be a
separate renderer decision.

### Sponsors

Organizer Sponsors is aggregate only:

- sponsor name
- lead counts
- consent-active counts
- handoff status
- retention/reclaim summary

No individual sponsor-owned lead details.

### Simulation And Operations

Simulation playback is read-only. Never show an "apply to live" button.

Operations may include diagnostics, but diagnostics should not leak into normal
participant/public flows.

## Sponsor Surface

Sponsor is a narrow pipeline, not a generic admin dashboard.

Tabs:

- Pipeline
- Consent
- Unlock
- Follow-up

Pipeline rows show:

- lead display name only when handoff allows it
- organization/role when allowed
- consent state
- unlock state
- reclaim state

Detail shows:

- consent trail
- agreement reference
- unlock/reclaim/redact controls
- follow-up draft

Sponsor must never see pre-handoff lead details. Independent sponsor login is a
separate implementation track; until then, UI must not imply more autonomy than
the current session supports.

Unauthenticated or missing sponsor context:

- Render one locked-state card explaining that sponsor access requires an
  approved sponsor session or organizer-gated preview.
- Hide pipeline rows, lead details, unlock buttons, and follow-up drafts.
- Do not show sample lead data.

## Nearby And Location

Nearby and location are high-value but high-risk.

Rules:

- Nearby scanner rows are host-capability gated.
- Web/staging normal user flows should be quiet when scanner is unavailable.
- Diagnostic workbench may show "scanner unavailable" explicitly.
- Nearby alone is not identity.
- Chat/proof/meeting actions require resolved identity and readiness.
- "Find where X is" requires explicit peer permission and should use coarse,
  time-boxed location state.

Actions by state:

| State | Allowed actions |
| --- | --- |
| Nearby, no identity | send scanner invite, request contact, export encounter |
| Nearby plus known identity | open profile, request meeting |
| Nearby plus chat-ready identity | send message |
| Nearby plus proof-ready identity | start proof chat |
| Location not shared | request access |
| Location shared | show allowed coarse location/proximity |

## Assistant And Tool UX

Participant assistant:

- save session
- refresh matches
- draft chat opener
- draft meeting request
- request location access
- find nearby people
- save note
- start project
- explain proof readiness

Organizer assistant:

- summarize operational risk
- draft broadcast
- explain KPI movement
- flag content gap
- propose simulation scenario

Sponsor assistant:

- explain actionable leads
- draft follow-up
- flag reclaim work
- summarize consent trail

Hard rule: no assistant action mutates state without explicit click.

## Data And Action Acceptance Checklist

For every surface before staging sign-off:

- Each tab opens correct content.
- Each list selection updates a real detail state.
- Each multi-select writes selected ids and affects the intended projection.
- Each button has a real action keypath and payload.
- Each text field writes to a real keypath and has save/apply behavior.
- Each upload field uses `FileUpload` or documented legacy attachment contract.
- Each reference endpoint resolves.
- Each unavailable action has a reason or is hidden.
- Each list has a short empty state with at most one suggested next action.
- Debug toasts are absent from final user-facing copy.
- Public/profile viewer surfaces do not show edit controls.
- Web does not fake nearby.
- Binding does not require CSS-only layout to be usable.

## Current Implementation Boundaries

Implemented or substantially present:

- Top-level tabbed conference shells.
- Participant agenda with focused tracks, selected/saved, recommended, and all.
- Admin content add/remove and published-content media state/actions.
- Concierge/tool-card baseline.
- Structured match explanation baseline.
- Coarse location-sharing baseline.
- Sponsor preview/pipeline baseline.

Still requiring follow-up:

- Public Porthole routing/config selection must reliably show Public, not
  Participant, when Public is requested.
- User-facing action-result debug text must be removed or moved to diagnostics.
- Profile viewer must not expose upload/edit controls.
- Normal web participant flows should not show "nearby unavailable" unless in a
  diagnostic workbench.
- Admin Content needs progressive disclosure to reduce density.
- Dynamic image rendering should consistently use the current portable upload
  contract and safe preview/reference fallback.
- Binding scanner host wiring must be verified end-to-end.
- Independent sponsor login remains separate.
- Charts/maps/video/timelines remain deferred.

## Definition Of Done

The conference redesign is "done enough" when:

- Porthole public, participant, organizer, sponsor, profile, chat, and nearby
  surfaces match the navigation/content contract above.
- Binding renders the same core flows without requiring web-only CSS.
- Screenshot and DOM captures show no wrong initial configuration, no dead
  controls, no debug action text, no fake capability UI, and no viewer edit
  controls.
- The staging revision is recorded with capture artifacts.
- Any remaining gaps are explicit tickets, not hidden assumptions.
