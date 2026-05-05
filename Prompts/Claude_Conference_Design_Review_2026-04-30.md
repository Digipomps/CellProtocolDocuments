# Claude Prompt · Conference Design Review · 2026-04-30

You are reviewing a cross-platform conference product that currently exists in
two runtimes:

- `Binding`: native Apple host for conference and Porthole surfaces
- `CellScaffold`: browser/server host for the same conference concepts

The attached screenshots are fresh captures from both runtimes.

Important reading note for the `CellScaffold` browser captures:

- `route-viewports/` show a web preview wrapper around the actual surface
- `surface-viewports/` are scrolled down to the actual conference surface and
  should be treated as the more canonical skeleton GUI

If there is tension between those two, prioritize the actual surface viewport.

Your job is not to redesign one screen in isolation. Your job is to propose a
much better, more coherent product-wide visual and interaction system for the
conference experience while respecting the fact that these surfaces are backed
by real `CellConfiguration` + skeleton-rendered UI and real state/action
contracts.

## Important constraints

- Do not propose fake one-off marketing mockups that ignore the existing
  product structure.
- Do not flatten everything into a single giant dashboard.
- Preserve the split between:
  - public surface
  - participant portal
  - participant chat / workbench
  - organizer control tower
  - AI assistant workspace
  - identity-link / setup flow
  - participant public profile / public profile editor
- Assume the same design language should work across web and native host
  surfaces.
- Assume some surfaces are long-lived control surfaces, not just static pages.
- Respect that access, identity, consent, and agreement boundaries are core to
  the product. Do not solve complexity by hiding those boundaries completely.

## What I want from you

1. Diagnose the current design problems across the screenshots.
2. Propose one strong, holistic visual direction for the conference product.
3. Explain how that direction should adapt across:
   - public storytelling surface
   - participant productivity surfaces
   - organizer/control-tower surfaces
   - AI / setup / utility workspaces
4. Suggest a coherent design system:
   - typography
   - spacing
   - color system
   - card language
   - navigation model
   - hierarchy
   - iconography / status treatment
   - data-density strategy
   - treatment of trust / consent / proof / access states
5. Call out which current patterns should be kept, which should be changed,
   and which should be removed entirely.
6. Give concrete redesign ideas for each captured surface.
7. Suggest how to make the whole product feel:
   - more beautiful
   - more intentional
   - calmer
   - more premium
   - more “conference-grade”
   - more obviously part of one family
8. End with a prioritized rollout plan:
   - highest-impact global changes first
   - then surface-specific changes
   - then small polish passes

## Output format

Please structure the answer as:

1. Overall diagnosis
2. Proposed design direction
3. Cross-surface system
4. Surface-by-surface recommendations
5. Component / pattern recommendations
6. Rollout plan

## Extra request

Be opinionated. Do not stay generic. If the current design language is too
safe, too flat, too repetitive, too dev-tool-like, or too fragmented, say so
clearly and propose a bolder alternative that still fits the architecture.
