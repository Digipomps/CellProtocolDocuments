# Send This To Gemini Now

```text
You are helping design and implementation work for HAVEN / CellProtocol.

Your job is to inspect one or more attached design sketches and produce:

1. a concrete HAVEN Skeleton UI proposal
2. a capability gap analysis against the current runtime
3. a small, prioritized set of proposed extensions or improvements where the current system is not enough

You must be conservative, precise, and explicit about what is actually supported today versus what only looks plausible.

## What HAVEN / CellProtocol Skeleton Is

In HAVEN, a screen can be described by a `CellConfiguration`:

- `cellReferences` define which cells or feeds the screen depends on
- `skeleton` is the declarative UI tree
- the runtime renders the skeleton and resolves dynamic data through cells, feeds, and keypaths

The main question is not just “can you imagine this UI,” but:

Can the current Skeleton UI and current Swift renderer show this design well enough, honestly and without pretending that unsupported features already exist?

## What You Must Deliver

Return all of the following sections:

### 1. Intent Summary

Briefly describe:

- the primary user job
- the major layout regions
- the key interactions
- whether the design is mainly:
  - static content
  - feed/list driven
  - form/input driven
  - app-shell/navigation driven
  - mixed

### 2. Fit Verdict

Choose exactly one:

- `direct`
- `approximate`
- `requires_extension`

Interpretation:

- `direct` = current Skeleton should represent the design well enough
- `approximate` = structure can be represented, but there are visible compromises
- `requires_extension` = current Skeleton/runtime cannot represent the design honestly enough

### 3. Concrete Skeleton Output

Produce either:

- a valid `skeleton` JSON root, or
- a full `CellConfiguration` JSON if enough bindings can be inferred

This JSON must be canonical and valid. Do not invent unsupported fields or element types.

### 4. Capability Gap Analysis

Return a table with these columns:

- `design_feature`
- `status`
- `why`
- `current_workaround`
- `recommended_extension`

Where `status` is one of:

- `native`
- `approximate`
- `unsupported`

### 5. Assumptions

List the assumptions you had to make:

- unknown data sources
- ambiguous navigation
- unclear interactions
- unclear responsive behavior
- unclear state model

### 6. Proposed Extensions And Improvements

If the design exceeds the current system, propose the smallest useful set of changes.

Do not answer with vague statements like “build a custom renderer.” Be specific and incremental.

Good examples:

- add stack spacing support to Skeleton JSON
- add stack alignment support to Skeleton JSON
- add remote image loading for `Image.url`
- add a `Badge` / `Chip` element
- add a lightweight navigation action contract
- add gradient background support

Also include:

- `priority`
- `why it matters`
- `backward compatibility risk`

## Normative JSON Contract

You must follow these rules exactly.

### Universal encoding rule

Every Skeleton element is encoded as a single-key object:

```json
{ "Text": { "text": "Hello" } }
```

### Container rule for stacks

`HStack` and `VStack` are array payloads, not objects:

```json
{
  "VStack": [
    { "Text": { "text": "Title" } },
    { "Text": { "text": "Body" } }
  ]
}
```

Do not invent:

- `spacing` on `HStack` / `VStack`
- `alignment` on `HStack` / `VStack`
- stack-level `elements` objects

Even if the Swift types expose some internal properties, the current JSON contract is still array-based for these stacks.

### Canonical field names

- Use `flowElementSkeleton`
- Never use legacy `flowELementSkeleton`
- Use wrapped `Object` form:

```json
{
  "Object": {
    "elements": {
      "title": { "Text": { "text": "Hello" } }
    }
  }
}
```

### Top-level `CellConfiguration`

If you produce a full configuration, the main fields are:

- `name`: string
- `uuid`: optional string
- `description`: optional string
- `discovery`: optional object
- `cellReferences`: optional array
- `skeleton`: optional Skeleton element

For each `cellReferences` item:

- `endpoint`: required string
- `subscribeFeed`: required bool
- `label`: required string
- `subscriptions`: optional array
- `setKeysAndValues`: optional array

## Supported `modifiers`

Available modifier fields:

- `padding`
- `maxWidthInfinity`
- `maxHeightInfinity`
- `width`
- `height`
- `hAlignment`
- `vAlignment`
- `background`
- `cornerRadius`
- `shadowRadius`
- `shadowX`
- `shadowY`
- `shadowColor`
- `borderWidth`
- `borderColor`
- `opacity`
- `hidden`
- `foregroundColor`
- `fontStyle`
- `fontSize`
- `fontWeight`
- `lineLimit`
- `multilineTextAlignment`
- `minimumScaleFactor`
- `styleRole`
- `styleClasses`

Notes:

- `Text.modifiers.styleRole = "markdown"` has special meaning in the current Swift renderer and enables Markdown rendering.
- Do not place image-specific fields such as `resizable` or `scaledToFit` inside `modifiers`.

## Supported Skeleton elements

You may use these current elements:

- `Text`
- `TextField`
- `TextArea`
- `Image`
- `Spacer`
- `HStack`
- `VStack`
- `List`
- `Object`
- `Reference`
- `Button`
- `Divider`
- `ScrollView`
- `Section`
- `ZStack`
- `Grid`
- `Toggle`

## Element details

### `Text`

Fields:

- `text`
- `url`
- `keypath`
- `modifiers`

Guidance:

- use `text` for static copy
- use `keypath` mostly for row-local or user-info-bound values inside `List` / `Reference`
- use `url` for top-level remote lookups

### `TextField`

Fields:

- `text`
- `sourceKeypath`
- `targetKeypath`
- `placeholder`
- `modifiers`

Guidance:

- use for short single-line input

### `TextArea`

Fields:

- `text`
- `sourceKeypath`
- `targetKeypath`
- `placeholder`
- `minLines`
- `maxLines`
- `submitOnEnter`
- `modifiers`

Guidance:

- use for multi-line input

### `Image`

Fields:

- `url`
- `name`
- `type`
- `resizable`
- `scaledToFit`
- `padding`
- `modifiers`

Important:

- `Image.url` exists in the model
- but the current newer Swift renderer does not actually give us trustworthy remote image rendering from `url`
- therefore remote-image-heavy designs should usually be marked as a real capability gap

### `List`

Fields:

- `topic`
- `keypath`
- `filterTypes`
- `selectionMode`
- `selectionValueKeypath`
- `selectionStateKeypath`
- `selectionActionKeypath`
- `activationActionKeypath`
- `selectionPayloadMode`
- `allowsEmptySelection`
- `elements`
- `flowElementSkeleton`
- `modifiers`

Important current behavior:

- `List` selection and activation are implemented in the current Swift UI
- `selectionPayloadMode = "item_id"` or `"selected_ids"` requires `selectionValueKeypath`
- use `flowElementSkeleton` for row templating

### `Reference`

Fields:

- `topic`
- `keypath`
- `filterTypes`
- `flowElementSkeleton`
- `scaledToFit`
- `padding`
- `modifiers`

### `Button`

Fields:

- `keypath`
- `label`
- `url`
- `payload`
- `modifiers`

Behavior:

- with `payload` => set
- without `payload` => get

Important:

- `payload` should be natural JSON
- do not assume rich button styling support beyond conservative generic modifiers

### `ScrollView`

Fields:

- `axis`
- `elements`
- `modifiers`

### `Section`

Fields:

- `header`
- `footer`
- `content`
- `modifiers`

### `ZStack`

Fields:

- `elements`
- `modifiers`

### `Grid`

Fields:

- `columns`
- `spacing`
- `elements`
- `modifiers`

Grid columns use:

- `type`: `fixed | flexible | adaptive`
- `value`
- `min`
- `max`

Important:

- no row span or column span in the current contract

### `Toggle`

Fields:

- `label`
- `keypath`
- `isOn`
- `modifiers`

## Current strengths of the system

Be willing to use these confidently:

- linear content layout
- simple card-like composition
- forms with text inputs and toggles
- feed/list rendering
- reference/list row templating
- adaptive grid layouts
- layered composition with `ZStack`
- markdown display through `Text.styleRole = "markdown"`
- selection-driven list browsing

## Current known gaps and weak spots

You must factor these into your analysis:

### Layout gaps

- no explicit stack spacing in JSON for `HStack` / `VStack`
- no explicit stack alignment in JSON for `HStack` / `VStack`
- no absolute positioning
- no anchored overlay primitives
- no breakpoint language for responsive layout

### Visual styling gaps

- no gradient primitive
- no blur/material/glass primitive
- no masks
- no corner-specific radii
- no first-class badge/chip element
- button visual styling is relatively limited

### Media gaps

- remote image rendering via `Image.url` is not dependable in the newer Swift renderer

### Interaction gaps

- no tabs, sheets, or navigation stack primitives in Skeleton itself
- no drag/drop
- no swipe actions
- no reorder interactions

### Rich content gaps

- markdown display exists
- but there is no full rich text editor primitive

## How to reason about a sketch

For each major feature in the sketch, classify it as:

- `native`
- `approximate`
- `unsupported`

Then decide:

- what can be represented concretely in Skeleton right now
- what needs approximation
- what needs a real runtime/renderer extension

Do not collapse everything into “unsupported.” Separate the representable core structure from the missing polish.

## What I especially want your help thinking through

Please pay special attention to these design-system questions when relevant:

1. When a sketch clearly depends on stack spacing or alignment that Skeleton does not encode, what is the best conservative mapping?
2. If remote images are central to the design, what is the smallest clean extension?
3. Which single visual extension would unlock the biggest improvement in modern card-heavy UI?
4. Which navigation behaviors should live outside Skeleton in app shell, and which might deserve a Skeleton-level contract?
5. If you could add only three backward-compatible Skeleton improvements, which three would unlock the most real GUI value?

## Output discipline

- Be concrete.
- Be honest about gaps.
- Produce valid JSON.
- Prefer a working conservative Skeleton proposal plus explicit extension suggestions over an aspirational but invalid proposal.

Now inspect the attached design sketch images and produce your answer.
```
