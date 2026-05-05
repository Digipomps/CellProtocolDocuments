# Chapter 12 — Skeleton Specification

This chapter defines the JSON encoding and element semantics for Skeleton UI, based on the current Swift implementation in:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
- `CellScaffold/Public/js/skeleton-runtime.js`

Important:

- `SkeletonElementView.swift` is deprecated and should not be treated as the canonical Apple renderer anymore.
- The canonical model still lives in `SkeletonDescription.swift`. Web and Apple runtimes may tolerate extra shapes, but portable JSON should follow the model, not renderer-only shortcuts.

## 1. Encoding Rule (All Elements)

Each element is encoded as a **single-key object** where the key is the element type and the value is that element’s payload.

Example:

```json
{
  "Text": { "text": "Hello" }
}
```

Lists of elements are encoded as arrays of these single-key objects:

```json
{
  "VStack": [
    { "Text": { "text": "Title" } },
    { "Image": { "name": "Logo" } }
  ]
}
```

## 2. Modifiers

Many elements accept `modifiers`. The available fields are:

- `padding` (Double)
- `maxWidthInfinity` (Bool)
- `maxHeightInfinity` (Bool)
- `width` (Double)
- `height` (Double)
- `hAlignment` ("leading" | "center" | "trailing")
- `vAlignment` ("top" | "center" | "bottom")
- `background` (hex color string, e.g. `#RRGGBB` or `#RRGGBBAA`)
- `cornerRadius` (Double)
- `shadowRadius` (Double)
- `shadowX` (Double)
- `shadowY` (Double)
- `shadowColor` (hex color string)
- `borderWidth` (Double)
- `borderColor` (hex color string)
- `opacity` (Double)
- `hidden` (Bool)
- `foregroundColor` (hex color string)
- `fontStyle` (String)
- `fontSize` (Double)
- `fontWeight` (String)
- `lineLimit` (Int)
- `multilineTextAlignment` (String)
- `minimumScaleFactor` (Double)
- `styleRole` (String)
- `styleClasses` (String array)

Source:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

## 3. Elements

### 3.1 Text

```json
{ "Text": { "text": "Hello", "modifiers": { "fontStyle": "title2" } } }
```

Fields:
- `text` (String, optional)
- `url` (String, optional, `cell://` URL)
- `keypath` (String, optional)
- `modifiers` (optional)

Behavior:
- If `keypath` is present and user data is provided, it is resolved from the user info object.
- If `url` is present, the cell is resolved and `get` is called.

### 3.2 TextField

```json
{ "TextField": { "placeholder": "Type...", "sourceKeypath": "profile.name" } }
```

Fields:
- `text` (String, optional)
- `sourceKeypath` (String, optional)
- `targetKeypath` (String, optional)
- `placeholder` (String, optional)
- `modifiers` (optional)

### 3.3 Image

```json
{ "Image": { "name": "AppIcon", "resizable": true, "scaledToFit": true } }
```

Fields:
- `url` (String, optional)
- `name` (String, optional)
- `type` (String, optional: png | jpeg | gif)
- `resizable` (Bool, optional)
- `scaledToFit` (Bool, optional)
- `padding` (Double, optional)
- `modifiers` (optional)

Renderer note:
- Web runtime can resolve `url` directly to `<img src=...>`.
- The canonical Apple renderer now supports remote `url` loading through `AsyncImage`, with local/system fallback when loading fails.

### 3.4 Spacer

```json
{ "Spacer": { "width": 8 } }
```

Fields:
- `width` (Double, optional)
- `modifiers` (optional)

### 3.5 HStack / VStack

```json
{ "HStack": [ { "Text": { "text": "A" } }, { "Text": { "text": "B" } } ] }
```

```json
{ "VStack": [ { "Text": { "text": "A" } }, { "Text": { "text": "B" } } ] }
```

```json
{
  "HStack": {
    "elements": [
      { "Text": { "text": "A" } },
      { "Text": { "text": "B" } }
    ],
    "spacing": 12,
    "modifiers": {
      "padding": 8
    }
  }
}
```

Fields:
- `elements` (array of `SkeletonElement`)
- `spacing` (Double, optional)
- `modifiers` (optional)

Encoding note:
- Bare array form is still valid and remains the compact encoding for simple stacks without `spacing` or `modifiers`.
- Object form with `elements` is the portable form when `spacing` or stack-level `modifiers` are used.

### 3.6 List

```json
{
  "List": {
    "topic": "feed.topic",
    "keypath": "cell:///Porthole/feed",
    "filterTypes": ["event"],
    "selectionMode": "single",
    "selectionValueKeypath": "agreementId",
    "selectionStateKeypath": "workbench.selection.set",
    "activationActionKeypath": "workbench.selection.open",
    "selectionPayloadMode": "item_id",
    "elements": [],
    "modifiers": { "padding": 8 }
  }
}
```

Fields:
- `topic` (String, optional)
- `keypath` (String, optional)
- `filterTypes` (String array, optional)
- `selectionMode` (String, optional: `none` | `single` | `multiple`)
- `selectionValueKeypath` (String, optional, row-relative keypath used to derive stable selected values)
- `selectionStateKeypath` (String, optional, explicit `set` target for publishing the current selection snapshot)
- `selectionActionKeypath` (String, optional, explicit `set` target fired on user selection change)
- `activationActionKeypath` (String, optional, explicit `set` target fired on explicit row activation)
- `selectionPayloadMode` (String, optional: `item` | `item_id` | `selected_items` | `selected_ids`)
- `allowsEmptySelection` (Bool, optional)
- `elements` (ValueTypeList, optional)
- `flowElementSkeleton` (VStack, optional)
- `modifiers` (optional)

Note: `flowElementSkeleton` is the canonical spelling in code.

Behavior:
- If no selection fields are present, `List` behaves as a read-only/render-only list like before.
- Renderers may keep local visual selection state, but must not invent hidden remote writes.
- `selectionStateKeypath`, `selectionActionKeypath`, and `activationActionKeypath` may only trigger because of explicit user interaction.
- They must not trigger on initial render, decode, refresh, or because a row disappeared from the backing dataset.
- Selection is distinct from activation:
  - selection updates selection state
  - activation performs an explicit action
- Multi-select payload order must follow source list order, not click order.
- If `selectionPayloadMode` is `item_id` or `selected_ids`, `selectionValueKeypath` is required.

Deterministic selection payload contract:

Single-select example:

```json
{
  "selectionMode": "single",
  "trigger": "select",
  "selectedIndex": 2,
  "selected": "agreement-123"
}
```

Multi-select example:

```json
{
  "selectionMode": "multiple",
  "trigger": "select",
  "selectedIndices": [1, 3, 4],
  "selected": ["agreement-101", "agreement-204", "agreement-205"]
}
```

Activation example:

```json
{
  "selectionMode": "single",
  "trigger": "activate",
  "selectedIndex": 2,
  "selected": "agreement-123"
}
```

### 3.6a Picker

```json
{
  "Picker": {
    "label": "Velg spor",
    "placeholder": "Velg et spor",
    "keypath": "conferencePublishedContent.state.program.tracks",
    "optionLabelKeypath": "title",
    "selectionValueKeypath": "id",
    "selectionStateKeypath": "contentPublishing.selectDraftTrack",
    "selectionActionKeypath": "contentPublishing.selectDraftTrack",
    "selectionPayloadMode": "item_id",
    "allowsEmptySelection": false
  }
}
```

Fields:
- `label` (String, optional)
- `placeholder` (String, optional)
- `keypath` (String, optional)
- `elements` (ValueTypeList, optional)
- `optionLabelKeypath` (String, optional)
- `selectionValueKeypath` (String, optional, required for `item_id` / `selected_ids`)
- `selectionStateKeypath` (String, optional)
- `selectionActionKeypath` (String, optional)
- `selectionPayloadMode` (`item` | `item_id` | `selected_items` | `selected_ids`, optional)
- `allowsEmptySelection` (Bool, optional)
- `modifiers` (optional)

Notes:
- `Picker` is intentionally a thin single-selection primitive over the same payload contract as `List`.
- The payload shape on selection is the same canonical object used by list single-selection:
  - `selectionMode`
  - `trigger`
  - `selectedIndex`
  - `selected`
- Apple renders `Picker` as a native menu-style picker.
- Web renders `Picker` as a native `<select>` and uses the same `selectionActionKeypath` / `selectionStateKeypath` flow as list selection.

### 3.7 Object

```json
{
  "Object": {
    "elements": {
      "title": { "Text": { "text": "Hello" } },
      "value": { "Text": { "text": "42" } }
    }
  }
}
```

Fields:
- `elements` (map of string → SkeletonElement)
- `modifiers` (optional)

Encoding now uses the wrapped `{ "Object": ... }` form. Decoding also accepts legacy unwrapped objects that contain `elements` at the top level.

### 3.8 Reference

```json
{
  "Reference": {
    "topic": "test",
    "keypath": "cell:///Porthole/eventTest",
    "flowElementSkeleton": {
      "VStack": [
        { "Text": { "text": "Item" } }
      ]
    }
  }
}
```

Fields:
- `topic` (String)
- `keypath` (String)
- `filterTypes` (String array, optional)
- `flowElementSkeleton` (VStack, optional)
- `scaledToFit` (Bool, optional)
- `padding` (Double, optional)
- `modifiers` (optional)

### 3.9 Button

```json
{
  "Button": {
    "keypath": "action.doThing",
    "label": "Run",
    "payload": { "string": "hello" }
  }
}
```

Fields:
- `keypath` (String)
- `label` (String)
- `url` (String, optional)
- `payload` (ValueType, optional)
- `modifiers` (optional)

Behavior:
- Executes `get` or `set` on the target cell depending on whether `payload` is set.

### 3.10 Divider

```json
{ "Divider": { } }
```

Fields:
- `modifiers` (optional)

### 3.11 ScrollView

```json
{
  "ScrollView": {
    "axis": "vertical",
    "elements": [ { "Text": { "text": "Item" } } ]
  }
}
```

Fields:
- `axis` (String, optional)
- `elements` (array of SkeletonElement)
- `modifiers` (optional)

### 3.12 Section

```json
{
  "Section": {
    "header": { "Text": { "text": "Header" } },
    "content": [ { "Text": { "text": "Row" } } ]
  }
}
```

Fields:
- `header` (SkeletonElement, optional)
- `footer` (SkeletonElement, optional)
- `content` (array of SkeletonElement)
- `modifiers` (optional)

Important:
- `content` is an array. A single wrapped element must still be encoded inside an array.

### 3.13 ZStack

```json
{
  "ZStack": {
    "elements": [
      { "Image": { "name": "Background" } },
      { "Text": { "text": "Overlay" } }
    ]
  }
}
```

Fields:
- `elements` (array of SkeletonElement)
- `modifiers` (optional)

### 3.14 Grid

```json
{
  "Grid": {
    "columns": [
      { "type": "adaptive", "min": 120, "max": 200 }
    ],
    "spacing": 8,
    "keypath": "conferenceParticipantShell.state.matches.recommendations",
    "itemSkeleton": {
      "Section": {
        "content": [
          { "Text": { "keypath": "title" } },
          { "Text": { "keypath": "detail" } }
        ]
      }
    }
  }
}
```

Fields:
- `columns` (array of `{ type, value?, min?, max? }`)
- `spacing` (Double, optional)
- `keypath` (String, optional)
- `itemSkeleton` (SkeletonElement, optional)
- `elements` (array of SkeletonElement, optional)
- `modifiers` (optional)

Behavior:
- `elements` is for static grids.
- `keypath + itemSkeleton` is the portable pattern for data-bound card grids.
- Grid keeps an internal `id` for SwiftUI identity, but the portable JSON form does not need to encode it.

### 3.15 Toggle

```json
{
  "Toggle": {
    "label": "Enabled",
    "keypath": "settings.enabled",
    "isOn": false
  }
}
```

Fields:
- `label` (String)
- `keypath` (String)
- `isOn` (Bool)
- `modifiers` (optional)

## 4. Keypath Rules

Many elements use `keypath` or `url`:

- `cell://` URLs are resolved through the `CellResolver`.
- Relative keypaths are often resolved as `cell:///Porthole/<keypath>` in the current UI.

See:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
- `CellScaffold/Public/js/skeleton-runtime.js`

## 5. Encoding Caveats

Current behavior:

1. `SkeletonObject` encodes with wrapped form `{ "Object": ... }`.
2. `SkeletonObject` decoding accepts both wrapped and legacy unwrapped object form.
3. New payloads should use canonical key `flowElementSkeleton`.

If you are generating JSON manually or with agents, emit canonical field names, wrapped `Object` format, and the names shown in this spec to stay consistent with decoding.

## 6. Current Practical Gaps

These are real, repo-confirmed limits as of March 2026:

1. `styleRole` / `styleClasses` exist in the model and web runtime, while Apple currently exposes them mainly as accessibility metadata rather than a full native theme mapping.
2. Skeleton still lacks first-class `Badge` / `Chip` and `Gauge` / `Progress` primitives, so metadata-heavy dashboards still rely on styled `Text` and custom cells.
3. Collection grids are now data-bindable, and `Picker` now exists as a first-class single-selection primitive. Domain contracts still need to expose honest option lists and state snapshots; a renderer primitive alone does not create an honest workflow.
