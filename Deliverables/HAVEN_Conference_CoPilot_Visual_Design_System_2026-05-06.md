# HAVEN Conference and Co-Pilot Visual Design System

Date: 2026-05-06

Status: canonical visual design guide for the conference surfaces and Personal
Co-Pilot surfaces. This document complements the functional guides:

- `Conference_Complete_Porthole_Binding_Design_Guide_2026-05-06.md`
- `Personal_CoPilot_V1_Complete_Design_Guide_2026-05-06.md`
- `Porthole_Binding_GUI_Parity_Audit_2026-05-06.md`

This guide focuses on how the product should look: color, typography, borders,
radius, spacing, states, and cross-tab recognition. It is not a claim that
staging currently matches this system.

## Why This Guide Exists

The earlier design guides captured the interaction model, data boundaries, and
Porthole-safe component structure. They did not capture enough of Claude's
visual sketches because the relevant design information lived in screenshots,
not in Markdown. Copying the Claude conversation preserved text, but lost the
visual system: cream canvas, indigo hero, lavender selected states, amber admin
warnings, green sponsor consent, rounded bordered cards, and large calm
typography.

Those screenshots are now archived as source artifacts:

- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-27 kl. 11.40.42.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-27 kl. 11.41.21.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-27 kl. 11.41.44.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-27 kl. 11.42.11.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-27 kl. 11.42.55.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-28 kl. 13.38.03.png`
- `CellProtocolDocuments/Artifacts/Claude_Visual_Design_References_2026-05-06/screenshots/Skjermbilde 2026-04-28 kl. 15.51.18.png`

Current Porthole screenshots used for comparison are archived in:

- `CellProtocolDocuments/Artifacts/Porthole_Conference_2026-05-06/`

Generated human-visible visual references:

- `CellProtocolDocuments/Artifacts/Personal_CoPilot_Invite_Chat_Visual_2026-05-06/invite-chat-desktop-and-mobile.png`
- `CellProtocolDocuments/Artifacts/Personal_CoPilot_Invite_Chat_Visual_2026-05-06/invite-chat-mobile-crop.png`

Detailed guide:

- `Personal_CoPilot_Invite_Chat_Visual_Design_Guide_2026-05-06.md`

Source classification matters. The conference/public/participant/chat/admin/
sponsor/nearby references above are screenshot-derived Claude visual proposals.
The `Invite Chat` reference is different: Claude supplied a textual UX proposal
without a graphic sketch, so the visual artifact is a controlled interpretation
using this guide's tokens and the existing Claude visual language.

## Visual Thesis

The HAVEN conference and Co-Pilot products should not look like a generic dark
dashboard. The shared visual language is:

- warm paper canvas
- white or soft cream content surfaces
- dark ink typography
- indigo as the primary action and trust accent
- lavender as selected or recommended state
- amber for organizer caution and drafts
- green for consent, sponsor handoff, live, and allowed states
- blue for nearby/radar affordances
- red only for denial, revoke, reclaim, and destructive risk

The system should feel calm, tactile, legible, and precise. It should look like
a product workspace, not an internal admin debug screen.

## Layering Rule

The same skeleton must survive three rendering layers:

1. Semantic skeleton: `Tabs`, `Section`, `List`, `Grid`, `VStack`, `HStack`,
   `Text`, `Button`, `Toggle`, `TextField`, `TextArea`, `Image`, `FileUpload`.
2. Portable style roles: roles such as `conference-card`, `accent-indigo`,
   `status-live`, `surface-public`, `tool-card`.
3. Host styling: web CSS and Binding native style mapping.

Layer 1 and 2 may be ignored by a renderer. The flow must still work. But a
finished visual implementation must honor Layer 2 and 3 so that users recognize
the same product across tabs and hosts.

## Core Tokens

These are recommended canonical token names. Exact renderer syntax can differ,
but the values should stay visually close.

```css
:root {
  --haven-paper: #f7f5ef;
  --haven-paper-raised: #fbfaf6;
  --haven-surface: #ffffff;
  --haven-surface-muted: #f1efe7;
  --haven-ink: #171717;
  --haven-ink-soft: #35332f;
  --haven-muted: #77736b;
  --haven-border: #d9d5cb;
  --haven-border-strong: #bdb7ac;

  --haven-indigo: #5b4bc8;
  --haven-indigo-dark: #2d256a;
  --haven-indigo-soft: #efedff;
  --haven-indigo-border: #a79cff;

  --haven-amber: #b76a00;
  --haven-amber-soft: #fff1d6;
  --haven-amber-border: #f3bd63;

  --haven-green: #0b7a5a;
  --haven-green-soft: #ddf6ef;
  --haven-green-border: #65cfae;

  --haven-blue: #2f65b8;
  --haven-blue-soft: #dceaff;
  --haven-blue-border: #9dbcf2;

  --haven-red: #a62424;
  --haven-red-soft: #ffe8e8;
  --haven-red-border: #ee9999;
}
```

### Surface Accents

| Surface | Accent | Soft fill | Use |
|---|---:|---:|---|
| Public | Indigo dark | Indigo soft | Hero, register CTA, program selection |
| Participant | Indigo | Lavender | Selected agenda, recommendations, chat owner bubble |
| Chat/proof | Indigo | Lavender plus amber request row | Members, outgoing messages, invitations |
| Organizer | Amber plus indigo metrics | Amber soft | Drafts, broadcast caution, admin selected tab |
| Sponsor | Green | Green soft | Consent, handoff, actionable leads |
| Nearby/radar | Blue | Blue soft | Nearby nav, scan filters, signal actions |
| Personal Co-Pilot | Indigo with dark sidebar | Lavender | Trust surfaces, matches, tool consent |

## Typography

Use semantic type roles, not ad hoc sizes.

| Role | Web target | Binding target | Use |
|---|---:|---:|---|
| Display | 32px / 38px, 700 | largeTitle or title1 bold | Hero titles, main screen title |
| H1 | 28px / 34px, 700 | title1/title2 bold | Surface titles |
| H2 | 22px / 28px, 700 | title2/title3 semibold | Section titles and card titles |
| Body | 17px / 24px, 400 | body | Normal content and chat text |
| Body strong | 17px / 24px, 650 | body semibold | Row titles and important values |
| Caption | 14px / 20px, 500 | caption/headline small | Metadata, source, timestamps |
| Overline | 13px / 18px, 700, 0.08em tracking | caption2 uppercase | Section labels like "PROGRAMHØYDEPUNKTER" |
| Button | 17px / 22px, 700 | body semibold | All buttons |
| Metric | 34px / 40px, 700 | title1 bold | KPI numbers |

Rules:

- Do not use small dense dashboard text for primary tasks.
- Main cards need 20px or larger titles.
- Captions must be readable; never drop below 13px web equivalent.
- Use uppercase only for section labels and compact status, not paragraphs.

## Spacing

Use a compact but breathable scale:

| Token | Value | Use |
|---|---:|---|
| `space-1` | 4px | Tiny inline gaps |
| `space-2` | 8px | Badge and compact row gaps |
| `space-3` | 12px | Row internals |
| `space-4` | 16px | Card internals, list gaps |
| `space-5` | 24px | Section padding |
| `space-6` | 32px | Major card padding |
| `space-7` | 40px | Hero and page rhythm |

Cards in the Claude sketches generally use 24px to 32px internal padding.
Rows use 12px to 16px vertical rhythm. Current Porthole staging is too dense.

## Radius, Borders, and Elevation

| Element | Radius | Border |
|---|---:|---|
| Page shell card | 18px to 20px | 1px `--haven-border` |
| Standard card | 14px to 16px | 1px `--haven-border` |
| Selected card | 14px to 16px | 1.5px `--haven-indigo-border` |
| Button | 12px to 16px | 1px `--haven-border-strong` |
| Pill/chip | 999px | 1px current accent border |
| Avatar | 999px | none |
| Input | 12px to 14px | 1px `--haven-border-strong` |
| Proof/advanced panel | 16px | 1px dashed `--haven-border` |

Elevation should be subtle. Prefer visible borders over heavy shadows. If a
shadow is used, keep it low: `0 1px 2px rgba(23, 23, 23, 0.06)`.

## Page Canvas

The default conference canvas is `--haven-paper`, not dark navy. The Porthole
chrome may remain its own application chrome, but the skeleton content should
render on the warm paper canvas.

Required page structure:

- outer paper background
- content max width on desktop, generally 1080px to 1280px
- top tab strip or hero first
- sections separated by whitespace, not heavy dividers
- white cards with warm borders

## Tabs

Tabs are the primary cross-platform navigation pattern.

Visual:

- Tab container: `--haven-paper-raised`, 1px border, 14px radius.
- Height: 56px to 64px.
- Selected tab: soft accent fill plus accent border.
- Label: 17px semibold.
- Horizontal padding: 20px to 28px.
- No dense dark pill tabs in product surfaces.

Surface-specific selected states:

- Public and Participant: lavender/indigo selected tab.
- Organizer: amber selected tab.
- Sponsor: green selected tab.
- Nearby: blue selected tab.
- Personal Co-Pilot dark sidebar: selected item can be indigo icon/text and
  subtle dark panel highlight.

## Buttons

Button rules:

- Minimum height: 44px. Preferred: 52px for primary actions.
- Radius: 12px to 16px.
- Primary: filled indigo unless surface demands green sponsor action.
- Secondary: white/cream fill with strong warm border.
- Danger: red text/border, red soft fill only for confirmation/risk.
- Disabled: muted text, low contrast border, explicit reason nearby.
- Never show more than one primary action in the same small card.

Canonical button styles:

| Role | Fill | Text | Border |
|---|---|---|---|
| Primary | `--haven-indigo` | white | `--haven-indigo` |
| Primary dark hero | transparent or indigo dark | white | lavender/white alpha |
| Secondary | `--haven-surface` | `--haven-ink` | `--haven-border-strong` |
| Sponsor primary | `--haven-green` | white | `--haven-green` |
| Nearby primary | `--haven-blue-soft` | `--haven-blue` | none or blue border |
| Danger | white | `--haven-red` | `--haven-red-border` |

## Cards

Cards should be purposeful, not decorative. A card is appropriate when an item
has independent meaning or actions: session, person, KPI, lead, tool suggestion.

Default card:

- fill `--haven-surface`
- border `--haven-border`
- radius 16px
- padding 24px
- title H2/body strong
- captions muted

Selected/recommended card:

- fill `--haven-indigo-soft`
- border `--haven-indigo-border`
- selected badge with indigo text

Consent card:

- fill `--haven-green-soft`
- border `--haven-green-border`
- direct, compact text

Warning/draft card:

- fill `--haven-amber-soft`
- border `--haven-amber-border`

Locked card:

- fill `--haven-paper-raised`
- opacity visually muted, but keep text readable
- no hidden data preview

## Forms and Inputs

Inputs should feel like large, safe targets:

- height 44px to 52px for single-line fields
- radius 12px to 14px
- border `--haven-border-strong`
- fill `--haven-surface`
- placeholder muted but readable
- focus border indigo, blue for nearby, green for sponsor
- TextArea minimum height 96px

Upload fields:

- use `FileUpload` where supported
- preview image in a normal card above or beside upload controls
- never expose upload fields in public viewer surfaces
- provide URL/reference fallback if upload is not supported by that cell

## Status Pills

Status is always text plus optional color. Never color alone.

| Status | Fill | Text |
|---|---|---|
| Live | `--haven-green-soft` | `Live` |
| Active | `--haven-green-soft` | `Aktiv` |
| Draft | `--haven-amber-soft` | `Utkast` |
| Pending | `--haven-amber-soft` | `Venter` |
| Proof ready | `--haven-indigo-soft` | `Proof ready` |
| Selected | `--haven-indigo-soft` | `Valgt` |
| Recommended | `--haven-indigo-soft` | `Anbefalt` |
| Locked | `--haven-surface-muted` | `Låst` |
| Reclaim required | `--haven-red-soft` | `Reclaim required` |
| Nearby | `--haven-blue-soft` | `Nearby` |

Pill radius: 999px. Padding: 6px 12px. Font: caption semibold.

## Public Conference Surface

Source sketch: `Skjermbilde 2026-04-27 kl. 11.40.42.png`.

Visual target:

- Canvas: warm paper.
- Main shell: large white rounded card with thin warm border.
- Hero: dark indigo rectangle, radius 14px to 16px, generous padding.
- Hero title: display, white, strong line height.
- Hero meta: uppercase overline in lavender/white alpha.
- Hero subtitle: large body, lavender/white alpha.
- CTA buttons: large, two side by side on desktop. Primary register; secondary
  program.
- Program highlights: small white cards, 1px warm border, 16px radius.
- People: circular pastel avatars, initials visible, 64px diameter.
- Public empty/callout state: pale cream box, warm border, compact text.

Acceptance:

- The public surface must look like a conference product landing page, not an
  internal data dashboard.
- Hero CTA must be visible without scrolling on desktop and mobile.
- No dark dashboard background unless explicitly used inside the hero.

## Participant Portal

Source sketch: `Skjermbilde 2026-04-27 kl. 11.41.21.png`.

Visual target:

- Canvas: warm paper.
- Top tabs: cream segmented control, selected tab lavender fill and indigo
  border.
- Cards: white, warm border, 16px radius, 24px padding.
- Home cockpit: two-column on desktop, single-column on mobile.
- Agenda action tiles: large 44px to 52px buttons/cards.
- Selected agenda row: lavender fill, indigo border, selected pill on right.
- Recommendation rows: compact but readable, with `Anbefalt` pill and concise
  reason.
- Track filters: large square/rect buttons or cards, not tiny chips.
- People rows: circular avatars, name/body strong, muted purpose/company text,
  large `Chat` action.
- Empty agenda state: cream callout with direct instruction, no long paragraph.

Agenda tabs:

- `Valgte`, `Anbefalte`, `Alle` are visible as equal sibling modes.
- Multi-track selection sits above agenda tabs.
- Selected sessions are visually distinct from recommended sessions.

Acceptance:

- The participant surface must feel like a day workspace.
- Important actions must be large enough for touch.
- It should not require reading dense explanatory text to understand next step.

## Participant Chat and Proof

Source sketch: `Skjermbilde 2026-04-27 kl. 11.41.44.png`.

Visual target:

- Chat window card: white/cream, rounded 16px, warm border.
- Header: back action left, title/body strong center-left, info button right.
- Member strip: lavender fill, indigo text/avatars, invite button outline
  indigo.
- Invitation request row: amber soft fill, approve/deny buttons.
- Incoming bubbles: white, warm border, black text.
- Outgoing bubble: indigo fill, white text, right aligned.
- Composer: white, large bordered input with `Tøm` and `Send` buttons.
- Settings cards: white cards with large segmented policy choices.
- Proof advanced panel: dashed warm border, muted title, explanatory cream
  callout, explicit `Åpne Proof Chat` button.

Acceptance:

- Ordinary chat and proof chat must be visually related but not confused.
- Proof state is visible as a panel or badge, not hidden as metadata.
- Tool cards may appear in chat, but only as explicit suggestions with `Do it`
  and `Dismiss`.

## Organizer Control Tower

Source sketch: `Skjermbilde 2026-04-27 kl. 11.42.11.png`.

Visual target:

- Canvas: warm paper, not dark operations dashboard.
- Top tabs: cream container, selected admin mode amber fill and amber border.
- KPI cards: white cards, warm borders, large metric numbers.
- Metric colors: indigo for participants, green for published/active, amber
  for pending/draft.
- Access request rows: pale cream row background, circular initials avatar,
  approve/deny buttons.
- Live session card: lavender border, live green pill, indigo progress bar.
- Publishing card: table-like rows with warm dividers, status text green/amber
  muted.
- Broadcast studio: amber border, amber warning callout, large explicit action.
- Insights: text/table fallback, not fake charts.

Acceptance:

- Organizer can be denser than participant, but must remain calm and readable.
- Warnings and drafts use amber. Live uses green. Primary operational trust uses
  indigo.
- No chart/sparkline visuals unless renderer support exists.

## Sponsor Follow-Up

Source sketch: `Skjermbilde 2026-04-27 kl. 11.42.55.png`.

Visual target:

- Accent: green.
- Main pipeline card: white, green border, 16px radius.
- Consent notice: green soft fill, green border, concise statement.
- Actionable lead row: cream row fill, circular mint avatar, strong name,
  readable consent timestamp, large `Følg opp` button.
- Locked lead row: muted, lower visual emphasis, no hidden detail preview.
- Update/export actions: secondary buttons with warm borders.
- Consent/agreement stats: white card, table rows with dividers, green values
  for full consent, amber values for partial.

Acceptance:

- Sponsor must feel like consent/compliance follow-up, not sales CRM gloss.
- Locked/pre-handoff states are visible and honest.
- Sponsor never sees private lead detail before consent and handoff.

## Nearby and Radar

Source sketch: `Skjermbilde 2026-04-28 kl. 13.38.03.png`.

Visual target:

- Accent: blue.
- Responsive hierarchy:
  - phone: bottom tabs, composer/action at bottom
  - tablet: master-detail split
  - desktop: sidebar + list + detail
- Search/filter input: 44px high, warm border.
- Signal cards: cream/white cards, border, 12px to 14px radius.
- Selected signal: subtle cream fill or blue selected nav state.
- Tags: small outlined pills for purpose/interest/radius.
- Action buttons: blue soft fill for friendly contact, secondary report button.

Capability rule:

- On web/staging, do not show fake nearby rows or scanner controls when host
  capability is absent.
- In diagnostics/radar-specific surfaces, show capability state explicitly.

Acceptance:

- Nearby must look lightweight and local, not surveillance-like.
- Unknown nearby entities must not get chat/proof actions until identity and
  readiness are resolved.

## Personal Co-Pilot

Source sketch: `Skjermbilde 2026-04-28 kl. 15.51.18.png`.

Detailed `Invite Chat` visual guide:
`Personal_CoPilot_Invite_Chat_Visual_Design_Guide_2026-05-06.md`.

Visual target:

- Shell: macOS/Binding style with dark left sidebar and cream main canvas.
- Sidebar: near-black fill, white section titles, muted descriptions, selected
  item with indigo icon/text.
- Main canvas: warm paper.
- Hero/info panel: lavender fill, indigo border, 18px radius.
- Tag pills: outline pills with indigo, warm, or amber borders.
- Context panel: white card on right, large section labels, clear policy/source
  fields.
- Device/content preview: black device frame may be Binding-specific; Porthole
  can use a bordered card fallback.
- Buttons: indigo primary, secondary cream outline, amber/red for decline/risk.
- Warning bar: gray/amber surface, dismiss action right.

Acceptance:

- Personal Co-Pilot should feel like a private workspace.
- It may use a dark sidebar, but the content canvas remains warm/light.
- Consent and matching actions require explicit click and clear labels.

## Tool Cards

Tool cards are the visual language for co-pilot actions across conference and
Personal Co-Pilot.

Default tool card:

- white card with warm border
- optional small icon
- H2 title
- one body sentence explaining what will happen
- `Needs` row for required data/consent
- compact `Why` caption
- primary `Do it` button
- secondary `Dismiss` button

Visual states:

- Suggested only: standard white card.
- Requires consent: green or amber callout inside card.
- Blocked: muted card with reason and no primary mutation button.
- Dangerous/reclaim/destructive: red outline and explicit confirmation action.

Hard rule:

- Tool cards never auto-run, regardless of confidence score.

## Current Staging Mismatch

Reference current Porthole screenshot:

- `CellProtocolDocuments/Artifacts/Porthole_Conference_2026-05-06/tab-clicks/participant-agenda.png`

Observed mismatch:

| Area | Current staging/Porthole | Target visual system |
|---|---|---|
| Canvas | Dark navy/teal dashboard | Warm paper canvas |
| Cards | Dark translucent cards with cyan borders | White/cream cards with warm borders |
| Tabs | Dark pills | Cream segmented tabs with accent selected state |
| Typography | Dense small dashboard text | Larger product typography with clear hierarchy |
| Agenda | Many dense cards, low visual contrast | Large track selectors, clear selected/recommended/all modes |
| Status | Cyan/green dashboard accents | Semantic indigo, lavender, amber, green, blue |
| Public | Still reads as app surface in places | Editorial conference landing |
| Sponsor | Generic dark cards | Green consent pipeline |
| Nearby | Diagnostics/dark styling | Blue lightweight radar where supported |

Conclusion: the implemented staging surface does not yet match Claude's visual
design proposal. The structure is closer than before, but the visual system is
not implemented in Porthole/Binding parity.

## Porthole Implementation Contract

The visual guide can be implemented without new skeleton primitives if renderers
honor style roles/classes. Required work:

1. Add or align Porthole theme CSS for conference and Personal Co-Pilot
   surfaces.
2. Map existing skeleton `styleRole` and `styleClasses` to the tokens in this
   guide.
3. Ensure root surface roles exist, for example:
   - `surface-conference-public`
   - `surface-conference-participant`
   - `surface-conference-chat`
   - `surface-conference-organizer`
   - `surface-conference-sponsor`
   - `surface-nearby`
   - `surface-personal-copilot`
4. Ensure component roles exist:
   - `conference-card`
   - `hero-card`
   - `selected-card`
   - `recommended-card`
   - `consent-card`
   - `tool-card`
   - `kpi-card`
   - `status-pill`
   - `message-incoming`
   - `message-outgoing`
   - `proof-panel`
5. Do not depend on CSS-only layout for core UX. The skeleton still needs to be
   valid and usable as stacked sections.

## Binding Implementation Contract

Binding should use the same semantic roles, but may map them to native SwiftUI
styles:

- `--haven-paper` maps to a warm grouped background.
- Card borders map to rounded rectangle strokes.
- Buttons map to bordered/prominent styles with matching tint.
- Tabs map to segmented controls or native tab bars depending on host.
- Sidebar Personal Co-Pilot maps to a dark navigation rail.
- Unsupported web-only CSS must degrade to native readable defaults.

Binding acceptance must include screenshots for:

- conference participant Today
- participant Agenda
- participant Chat
- organizer Control Tower
- sponsor Pipeline
- nearby/radar
- Personal Co-Pilot Matches

## Accessibility

- Minimum touch target: 44px/44pt.
- Text contrast must pass WCAG AA against the chosen fill.
- Status must never rely on color alone.
- Focus state should use a 2px accent outline or native focus ring.
- Disabled controls must explain why in nearby text or status.
- Avatars need initials fallback when image is absent.

## Acceptance Checklist

A surface matches this guide only when all of these are true:

- It uses warm paper as the dominant canvas, except allowed dark sidebar/hero.
- It uses white/cream cards with warm borders.
- It uses semantic accent colors per surface.
- It uses large readable typography for titles, rows, and buttons.
- It avoids dense card spam and long explanatory copy.
- It keeps all primary actions visible and touch-size.
- It keeps selected/recommended/saved states visually distinct.
- It hides unsupported capability UI.
- It does not expose editor-only upload controls in public viewers.
- It has no debug action text or fake toasts in product copy.
- It remains usable when style roles are ignored.

## Next Implementation Order

1. Implement Porthole theme tokens and role mapping for conference surfaces.
2. Re-capture Porthole screenshots and compare against the archived Claude
   screenshots.
3. Implement Binding role mapping or native style parity for the same roles.
4. Re-capture Binding screenshots.
5. Only then refine skeleton layout if the remaining mismatch is structural.

The current problem is primarily styling parity, not missing skeleton
primitives.
