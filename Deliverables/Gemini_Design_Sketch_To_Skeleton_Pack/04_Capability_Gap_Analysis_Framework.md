# Capability Gap Analysis Framework

Use this rubric when deciding whether a design can be shown well enough with current Skeleton UI.

## Rating Scale

- `native`
  - directly supported and likely to look intentional
- `approximate`
  - structurally possible, but with visible compromise
- `unsupported`
  - cannot be represented honestly without extensions or custom work

## Categories To Check

### Layout

Ask:

- Is the screen mostly linear, sectional, stacked, or grid-based?
- Does it depend on per-stack spacing or custom alignment not present in the JSON contract?
- Does it require absolute positioning or anchored overlays?

Current strengths:

- `VStack`, `HStack`, `ZStack`, `Grid`, `ScrollView`, `Section`

Known gaps:

- no explicit stack `spacing`
- no explicit stack `alignment`
- no absolute positioning
- no row/column span in `Grid`

### Data Binding

Ask:

- Is the screen mainly static copy, form-bound state, or feed-bound state?
- Can bindings be expressed with `url`, `keypath`, `sourceKeypath`, `targetKeypath`, `List`, or `Reference`?

Current strengths:

- text lookup via `url`
- row-local lookup via `keypath`
- list/reference templating
- `TextField`, `TextArea`, `Toggle`

Known gaps:

- no first-class computed binding expressions
- no direct templating language for `Button.payload`

### Interaction

Ask:

- Does the design require simple submit/select/toggle behavior, or gesture-heavy interactions?
- Does it rely on drag, swipe actions, reorder, hover, or multi-step app-shell navigation?

Current strengths:

- button action
- toggle state
- list selection
- list activation
- text input submit/persist

Known gaps:

- no drag/drop
- no swipe actions
- no reorder controls
- no modal/tab/navigation primitives in Skeleton itself
- button visual styling is comparatively limited

### Visual Styling

Ask:

- Is the design mostly typography, color, border, shadow, and spacing?
- Or does it depend on gradients, blur, glass, masks, corner-specific radii, advanced strokes, or token-driven theme systems?

Current strengths:

- foreground/background color
- corner radius
- shadow
- border
- typography controls
- `styleRole` / `styleClasses` metadata

Known gaps:

- no gradients
- no blur/material
- no masks
- no dashed strokes
- no corner-specific radius
- no built-in badge/chip primitive
- no strong button-label theming contract in generic modifiers

### Media

Ask:

- Does the design use asset images only, or remote images/avatars?

Current strengths:

- asset images by `name`
- resize and fit flags

Known gaps:

- `Image.url` exists in the model but is not currently loaded by the newer Swift renderer

### Rich Text

Ask:

- Is display text plain or formatted markdown?
- Is editable rich text required?

Current strengths:

- `Text` can render Markdown when `styleRole` is `"markdown"`

Known gaps:

- no rich text editor
- `TextArea` is plain editable text, not a structured rich text surface

### Responsiveness

Ask:

- Does the design rely on breakpoint-specific structure changes?
- Can `Grid` with adaptive columns approximate it?

Current strengths:

- adaptive grid columns
- scroll containers

Known gaps:

- no explicit breakpoint system
- no conditional layout rules in JSON

## Known Runtime Reality, Grounded In Code

These points should influence the verdict:

- `TextArea` is real and tested.
- `List` selection and activation are real in the current Swift UI.
- `Text.styleRole = "markdown"` has special behavior in the current Swift UI.
- `Image.url` is a model-level capability, but not a current-renderer capability.
- `HStack` / `VStack` are still rigid compared to modern design-tool auto-layout.

## Practical Verdict Guidance

Use `direct` when:

- the sketch is card-, list-, form-, or grid-like
- spacing compromises are acceptable
- visuals rely mostly on text, color, border, radius, shadow

Use `approximate` when:

- the structure maps, but the design depends on nuanced spacing, overlay positioning, or advanced polish

Use `requires_extension` when:

- remote image fidelity is central
- navigation containers are central
- glassmorphism / gradients / blur are central
- motion or gesture systems are central
- charting or timeline visuals are central

## Recommended Minimal Extensions To Consider

If Gemini concludes `requires_extension`, these are the most likely high-value additions:

- stack spacing in JSON
- stack alignment in JSON
- remote image loading for `Image.url`
- a `Badge` / `Chip` element
- a simple `NavigationLink` / route action contract
- a gradient background primitive
- a lightweight overlay/alignment primitive
