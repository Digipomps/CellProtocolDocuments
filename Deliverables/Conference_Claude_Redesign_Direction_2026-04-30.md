# Conference Product Redesign Direction
_April 30 2026 · Based on handoff pack review_

---

## North Star

> **The architecture already knows what the system is. The design work is closing the gap between what the architecture understands and what the person using it experiences.**

The conference product's differentiating idea — shared relation state across organizer and participant, bounded by agreement and consent — should be *felt* in the UI, not just encoded in the data model. Every surface should make the user's position in that relation graph legible at a glance: who they are here, what's pending, what's shared with whom.

Principle hierarchy:
1. **Position before action.** Always orient the user (role, context, what's live) before asking them to do something.
2. **Shared reality is visible.** Threads, sessions, and handoffs that cross organizer/participant lines carry that crossing as a visual marker — not hidden in metadata.
3. **Infrastructure is invisible to participants.** Config, skeleton setup, model selection, and challenge state machine are operator concerns. Participants see none of this unless they explicitly go looking.

---

## Surface Model

Seven surfaces. Three persona tiers. Two cross-cutting layers.

### Tiers

| Tier | Surfaces | Shell weight |
|---|---|---|
| Public | Public landing, Profile viewer | Minimal — no auth chrome |
| Participant | Portal dashboard, Chat workbench, Profile editor, AI workspace | Persistent identity rail |
| Organizer | Control tower | Full admin chrome |

### Cross-cutting layers

**Identity layer** — Identity link / setup flow sits orthogonal to all tiers. It is not a surface participants visit repeatedly; it is a one-time bootstrap wizard. Design it as such: linear, one step visible at a time, exits into the Participant tier on completion.

**AI layer** — The AI workspace is not a standalone surface for participants. It is a mode that the portal dashboard and chat workbench can enter. Expose it as a contextual overlay / expanded input state, not a separate route. The operator-facing CellConfiguration and skeleton setup belongs in the Control Tower or a dedicated admin route, not in the participant AI surface.

### Surface contracts

**Public landing** — unauthenticated, read-only, drives two exits: registration and portal login. No session state.

**Profile viewer** — unauthenticated, renders only the participant-owned public slice. No edit affordances. Used by other participants and external visitors.

**Portal dashboard** — authenticated participant home. Owns: agenda state, people recommendations, meeting requests, chat threads index. Does not own: AI config, challenge/identity state, organizer-side data.

**Chat workbench** — activates on opening any thread. Context collapses to a rail; thread becomes full surface. Renders shared organizer/participant threads with role provenance on each node.

**Profile editor** — participant owns one slice of their profile per conference context. Edit surface is scoped strictly to that slice. Audience/privacy state is editable here and only here.

**AI workspace** — participant-facing mode only. Entry point is a compose area with context chips. No model selector, no baseURL input, no skeleton chooser visible to participants.

**Control tower** — organizer only. Three modes: Run (live ops, broadcasts, status board), Build (program, content, access, agenda), Review (insights, relation audit, KPIs, sponsor follow-up).

---

## Visual Language

### Shell vs surface

Binding's dev chrome (mode toggles, debug bar, library strip) currently renders at the same visual weight as the content it wraps. This must change.

- **Shell** (Binding chrome, nav rail, identity strip): low contrast, receded. Thin strokes, muted backgrounds. Feels like a browser frame.
- **Surface** (canonical content): full contrast, readable. This is where the product lives.

Use Scaffold's lighter canonical surface treatment as the product register. The shell's job is to disappear.

### Typographic scale

Current: compressed, mostly 13–14px, minimal weight differentiation. Replace with a four-stop ramp applied consistently:

| Role | Size | Weight | Use |
|---|---|---|---|
| Display | 20–22px | 500 | Section hero, surface title |
| Title | 17–18px | 500 | Card headers, tab labels |
| Body | 15px | 400 | Content, descriptions |
| Label | 13px | 400 | Meta, counts, badges |

No font-size below 13px in production surfaces.

### Hierarchy markers

- **Role badges** on thread nodes: small pill (Participant / Organizer / System), rendered inline, not in a tooltip.
- **Boundary rule** in shared threads: a horizontal rule with a label ("organizer-visible from here") where the shared zone starts — not hidden in metadata.
- **Status chips** on agenda items: session state (saved / confirmed / pending / conflict) as a chip on the card, not as a prose sentence.
- **Draft vs published** on profile: a single persistent indicator at the top of the editor surface — one source of truth for audience/privacy state, not duplicated in both header and body.

### What to remove

- Equal-weight twin CTAs (e.g. "Åpne AI-assistent" / "Åpne chatflate" as peers). Differentiate primary from secondary.
- Status report headers. Six count-numbers stacked in a portal header is a status dump, not a welcome screen.
- Config surfaces in participant-facing routes. Model selectors, API key inputs, baseURL fields — all behind operator/admin gates.
- Duplicated metadata. Audience/context state appears in both the profile viewer header and the Visible Focus section. Pick one location.

---

## Navigation / IA

### Participant portal tabs

Current: Today / Agenda / People / Chats / Meetings / Profile — six tabs, reasonable.

Proposed change: keep the six tabs but fix the Today tab. Today is the product's homepage and it is currently the weakest tab. It should render:
1. A single prioritised action card ("Your next step") — derived from agenda readiness, pending meetings, or unread threads.
2. The three-column status grid (Agenda / People / Meetings) as a secondary widget row, not as the hero.
3. An AI compose entry point as a bottom-anchored affordance, not a top-of-page button.

Remove the portal header status cluster (six count numbers). This data lives in the Today tab widgets. It does not need to live in the header.

### Control tower navigation

Current: eleven primary tabs (Overview / Story / Insights / Broadcasts / Access / Content / Audience / Live / Sponsors / Simulation / Operations).

Replace with three modes and sub-navigation within each:

- **Run** → Live status board, Broadcasts, Operations
- **Build** → Program, Content, Access, Audience, Sponsors
- **Review** → Insights, Story, Relation audit, Simulation / KPI recompute

Default entry point on load: Run. Organizers arriving mid-conference should land in the live view, not an overview tab.

### Identity link flow

Replace the current three-column document layout with a five-step wizard:

1. **Receive** — challenge arrives (QR / link / paste). One action: "Review challenge."
2. **Verify** — show what the challenge grants access to. One action: "Accept" or "Decline."
3. **Bind** — Binding matches challenge to identity. Status feedback: "Confirmed ✓" or error with recovery path.
4. **Complete profile** — prompt for the one required field (name or focus) if missing. Skippable.
5. **Enter portal** — transition directly into the Participant portal. No intermediate confirmation screen.

All state machine explanation and challenge format documentation moves to a collapsible help drawer on step 2.

### AI entry points

Remove the AI workspace as a top-level route for participants. Replace with two in-context entry points:

- **Portal dashboard**: a compose chip at the bottom of the Today tab, pre-populated with a context summary (n sessions saved, n people recommended, n follow-ups pending). Expanding it opens an AI panel inline.
- **Chat workbench**: an AI suggestion strip above the compose input in any thread, offering context-aware prompts ("Draft a follow-up to Ana based on your meeting notes").

The standalone AI workspace route remains for operators and power users. Gate it behind an explicit "Open AI workspace" action in the profile or settings, not in the main nav.

---

## Implementation Priorities

In dependency order — each item unblocks the ones below it.

### P0 — Foundation (do first, everything depends on this)

1. **Shell/surface visual separation.** Reduce Binding chrome contrast and weight. Define the two registers (shell vs surface) in the design token layer. Without this, every surface looks like a dev tool.
2. **Typographic scale.** Implement the four-stop ramp as design tokens. Apply to all surfaces in one pass before further UI work.
3. **Role badge and boundary rule components.** These are used in chat workbench, control tower, and shared thread views. Build them once as primitives.

### P1 — Portal (highest user-facing leverage)

4. **Today tab redesign.** Remove status cluster from header. Implement prioritised action card as hero. Move count widgets below fold.
5. **Portal header → collapsed identity rail.** Name, role, event name — nothing else in the header. All counts move to Today tab.
6. **Primary/secondary CTA differentiation.** Apply across all surfaces. Quick pass, high visual impact.

### P2 — Chat workbench

7. **Thread as full surface.** When inside a thread, portal header collapses to a breadcrumb rail. Thread timeline takes full width.
8. **Timeline thread UI.** Role badges on nodes. Boundary rule for shared zones. Meeting requests as rich cards inline.
9. **AI suggestion strip.** Inline above compose input. Context-aware, collapsible.

### P3 — Identity and onboarding

10. **Identity link wizard.** Replace document layout with five-step wizard. One step visible at a time. Help drawer for state machine docs.

### P4 — AI workspace

11. **Remove config from participant-facing AI surface.** Move model selector, skeleton chooser, API key input to admin/operator route.
12. **Context-first AI surface.** Context chips as pills above compose area. Last response visible. CellConfiguration drawer collapsed by default.

### P5 — Control tower

13. **Three-mode navigation.** Replace eleven-tab strip with Run / Build / Review. Default to Run.
14. **Organizer-as-participant thread view.** When organizer opens a participant thread, it renders in the same chrome as the participant sees, with organizer affordances as overlays.

### P6 — Profile surfaces

15. **Image drop zone.** Replace three-line "no profile image / choose file" pattern with a single drop target.
16. **Metadata deduplication.** Audience/privacy state in one location per surface. Audit viewer and editor for duplication.

---

## Risks

### Binding chrome is load-bearing in unexpected ways

The debug bar, mode toggles, and library strip in Binding are used actively during development and may have hooks that make them hard to visually recede without functional regressions. Treat the shell/surface separation as a theming/token problem, not a layout change — the chrome stays in place, it just gets a lower-contrast token set.

### Portal header status cluster may be used by other surfaces

The six-count header block (saved sessions / recommended sessions / pending requests / confirmed meetings / shared threads / persistence failures) appears to be a reused component across portal and control tower views. Removing it from the participant portal header requires verifying it is not the canonical source for these counts elsewhere in the product. Audit before removing.

### AI workspace config removal needs operator gate

Removing CellConfiguration from the participant-facing AI surface only works if there is a clear operator/admin route where it lives instead. If that route doesn't exist yet, build it before removing config from the participant surface — otherwise participants with edge cases (custom models, non-default skeleton) have no path to configure.

### Identity link wizard assumes linear challenge flow

The five-step wizard design assumes a single challenge token arriving at a known moment. If the system supports multiple concurrent challenges, partial challenges, or challenge expiry/retry flows, the wizard needs error and recovery states designed explicitly. The current document layout handles this by showing all state at once; the wizard hides it. Don't hide states that have no recovery path designed.

### Eleven-tab control tower nav may reflect real operational complexity

The eleven tabs may not be UI bloat — they may reflect eleven genuinely distinct organizer tasks that don't collapse cleanly. Before implementing the three-mode grouping, validate with an organizer that Run / Build / Review actually matches how they context-switch during a conference. If organizers jump between Insights and Live constantly, splitting them into different modes creates more friction than the current flat list.

### Norwegian copy and English structure

Several surfaces carry Norwegian UI copy (agenda labels, CTA text, status descriptions) alongside English structural labels. This is presumably a locale/i18n work-in-progress, not a design decision. But it means any component built with Norwegian copy as a layout assumption (character count, line length, button width) may break when English copy is substituted. Design and test component widths with both languages from the start.
