# Porthole/Binding GUI Parity Audit

Date: 2026-05-06

Status: current evidence and implementation backlog for conference and Personal
Co-Pilot design parity.

## Evidence Captured

Staging build:

- URL: `https://staging.haven.digipomps.org`
- Health revision observed: `e6f51360bd58c4d29f8dc935afe7cf31f40ed0f7`
- Build timestamp observed: `2026-05-05T15:42:35Z`

Porthole screenshot artifacts:

- Archived screenshots:
  `CellProtocolDocuments/Artifacts/Porthole_Conference_2026-05-06/screenshots`
- Archived tab-click captures:
  `CellProtocolDocuments/Artifacts/Porthole_Conference_2026-05-06/tab-clicks`
- Capture origin:
  `/tmp/haven-conference-claude-exchange/porthole-screenshots/2026-05-06T07-19-35-019Z`
- Capture origin:
  `/tmp/haven-conference-claude-exchange/porthole-tab-clicks/2026-05-06T07-19-34-738Z`

The audit is based on screenshots, text extracts, and tab-click captures. It is
not a full XCTest/Playwright pass.

## Executive Finding

The conference redesign is partially present on staging, but it is not yet in
full compliance with the Claude/Porthole design direction. The biggest issue is
not missing decoration. It is product correctness: some requested surfaces load
the wrong content, debug action text appears in the user experience, and a few
controls appear where they should be hidden.

Personal Co-Pilot has several strong implementation documents, but before this
pass it did not have one complete canonical design guide equivalent to the
conference guide.

Follow-up visual-design update: Claude's `Invite Chat` response was confirmed
to be a textual UX proposal, not a graphic design proposal. A human-visible
visual interpretation has now been added under
`Personal_CoPilot_Invite_Chat_Visual_Design_Guide_2026-05-06.md` with rendered
PNG artifacts.

## Conference Status

### Working Or Substantially Present

- Participant Agenda has focused tracks and tabs for selected, recommended, and
  all session views.
- Participant People shows match/recommendation style rows and nearby-related
  state.
- Participant Chats show assistant/tool-card style UX with explicit action
  framing.
- Organizer Content includes published-content editing and media upload/reference
  controls.
- Organizer Live, Audience, Insights, Sponsors, Simulation, and Operations have
  concrete content.
- Sponsor Pipeline, Consent, Unlock, and Follow-up tabs exist.
- Profile editor has image upload/reference style controls.

### P0/P1 Gaps

1. Public surface mismatch. Latest Porthole capture for the expected Public
   surface showed `Conference Participant Portal Dashboard` text instead of the
   Public surface. The manifest indicated the expected configuration was not
   seen. This blocks design acceptance for Public.
2. Action-result debug text leaks into product UI. Several tab captures include
   text like `Kjorte conferenceParticipantShell.navigation.setActiveTab` or
   equivalent admin navigation action text. This is visual noise and should be
   moved to diagnostics or removed from user-facing content.
3. Public profile viewer appears to expose upload/edit controls. Viewer surfaces
   must not show `Choose file` or edit controls.
4. Nearby unavailable copy appears in normal user-facing flows. Diagnostic
   workbenches may show scanner unavailable, but ordinary web/staging People
   should quietly hide nearby source when unsupported.
5. Organizer Content is too dense for the design goal. It is functional, but it
   currently risks becoming a long CMS/debug surface rather than a clean control
   workflow.

### P2 Gaps

- Organizer Overview is sparse compared to the intended control tower.
- Participant Meetings capture appears to repeat Chat/tool-card content in one
  tab-click run. Reproduction step: open Participant shell, click Meetings,
  confirm the body shows the meetings lifecycle list rather than Chat/tool-card
  content, then capture URL, screenshot, and text extract. File a bug if the
  mismatch persists.
- Some profile copy still feels fixture-like rather than final product copy.
- Media preview behavior should be made consistent with the current portable
  upload contract.
- Binding scanner/radar host wiring still needs end-to-end proof.

## Personal Co-Pilot Status

No Personal Co-Pilot Porthole capture set was produced in this audit pass. This
section is a design-gap pre-assessment, not an evidence-based staging audit.
Evidence capture is the first required next step for Personal Co-Pilot parity.

### Working Or Documented

- Chat assistant V1 has a concrete suggestion-first contract.
- Intent handling is deterministic and testable without external AI.
- Provider routing is cell-scoped.
- Purpose/interest refs and confidence tiers are documented.
- Binding has phase 1 design-system style roles and shell direction.
- `Invite Chat` now has a visual reference guide and rendered PNG artifacts
  based on Claude's textual UX proposal plus the canonical HAVEN visual tokens.

### Gaps

1. No single complete design guide existed before this pass. The new
   `Personal_CoPilot_V1_Complete_Design_Guide_2026-05-06.md` is the canonical
   guide.
2. `Invite Chat` now has a visual target, but staging/Porthole still needs to
   be captured and compared against it.
3. Porthole screenshot coverage for all Personal Co-Pilot surfaces still needs
   to be captured and attached to acceptance.
4. Binding phone/iPad/macOS parity needs visual verification.
5. Vault, Workflow, Directory, Matches, and Privacy need clean product-surface
   acceptance, not only implementation contracts.
6. Scanner/location flows require capability and consent verification.

## Required Fix Sequence

### Conference

1. Fix Public Porthole selection/routing so requesting Public reliably renders
   Public.
2. Remove or hide action-result debug text from normal Porthole surfaces.
3. Ensure public profile viewer uses viewer skeleton only; upload/edit controls
   are editor-only.
4. Make nearby source quiet on unsupported web/staging normal flows; keep
   explicit unavailable text only in diagnostics/workbench.
5. Reduce Organizer Content density through tabs/selection/detail grouping and
   shorter labels.
6. Re-capture Porthole screenshots and DOM for Public, Participant Today,
   Agenda, People, Chats, Meetings, Profile, Organizer tabs, Sponsor tabs,
   Profile viewer/editor, and Nearby Radar.
7. Run Binding parity tests for participant/public/admin/sponsor/chat/profile
   and nearby radar.

### Personal Co-Pilot

1. Identify canonical CellConfiguration names for Home/Profile/Directory/Matches
   /Chat/Vault/Workflow/Privacy.
2. Capture Porthole screenshots and DOM for each.
3. Verify Binding phone/iPad/macOS render paths.
4. Compare each surface to
   `Personal_CoPilot_V1_Complete_Design_Guide_2026-05-06.md`,
   `HAVEN_Conference_CoPilot_Visual_Design_System_2026-05-06.md`, and the
   Invite Chat visual guide where relevant.
5. File implementation gaps for any dead buttons, unbound fields, or capability
   UI shown without support.

## Clean UX Acceptance Checklist

Use the authoritative checklist in
`Conference_Complete_Porthole_Binding_Design_Guide_2026-05-06.md` under
`Data And Action Acceptance Checklist`. This audit should record pass/fail
evidence against that checklist rather than maintaining a divergent copy.

## Documentation Produced In This Pass

- `Conference_Complete_Porthole_Binding_Design_Guide_2026-05-06.md`
- `Personal_CoPilot_V1_Complete_Design_Guide_2026-05-06.md`
- `HAVEN_Conference_CoPilot_Visual_Design_System_2026-05-06.md`
- `Personal_CoPilot_Invite_Chat_Visual_Design_Guide_2026-05-06.md`
- `Porthole_Binding_GUI_Parity_Audit_2026-05-06.md`

These documents should be treated as the current design and acceptance baseline.
