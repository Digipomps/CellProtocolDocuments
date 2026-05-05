# Normative CellConfiguration And Skeleton JSON

This document is the wire-format contract Gemini should follow.

## 1. Universal Encoding Rules

- Every `SkeletonElement` is encoded as a single-key object.
- The key is the element type.
- The value is that element's payload.

Example:

```json
{
  "Text": {
    "text": "Hello"
  }
}
```

- `HStack` and `VStack` are special: their payload is a raw array of single-key objects.

Example:

```json
{
  "VStack": [
    { "Text": { "text": "Title" } },
    { "Divider": {} },
    { "Text": { "text": "Body" } }
  ]
}
```

## 2. `CellConfiguration` Shape

Top-level fields:

- `name`: required string
- `uuid`: optional string
- `description`: optional string
- `discovery`: optional object
- `cellReferences`: optional array
- `skeleton`: optional `SkeletonElement`

`discovery` fields:

- `sourceCellEndpoint`: optional string
- `sourceCellName`: optional string
- `purpose`: optional string
- `purposeDescription`: optional string
- `interests`: optional string array
- `menuSlots`: optional string array

`cellReferences` item fields:

- `endpoint`: required string
- `subscribeFeed`: required bool
- `label`: required string
- `subscriptions`: optional array of nested `CellReference`
- `setKeysAndValues`: optional array of key/value commands

Notes:

- Keep `cellReferences` simple unless the screen really depends on startup commands.
- For design-to-skeleton work, Gemini may output only the `skeleton` root if `cellReferences` are unknown.

## 3. Modifier Fields

Supported `modifiers` fields:

- `padding`: number
- `maxWidthInfinity`: bool
- `maxHeightInfinity`: bool
- `width`: number
- `height`: number
- `hAlignment`: `"leading" | "center" | "trailing"`
- `vAlignment`: `"top" | "center" | "bottom"`
- `background`: hex color string
- `cornerRadius`: number
- `shadowRadius`: number
- `shadowX`: number
- `shadowY`: number
- `shadowColor`: hex color string
- `borderWidth`: number
- `borderColor`: hex color string
- `opacity`: number
- `hidden`: bool
- `foregroundColor`: hex color string
- `fontStyle`: string such as `title2`, `headline`, `body`, `caption`
- `fontSize`: number
- `fontWeight`: string such as `regular`, `medium`, `semibold`, `bold`
- `lineLimit`: integer
- `multilineTextAlignment`: `"leading" | "center" | "trailing"`
- `minimumScaleFactor`: number
- `styleRole`: string
- `styleClasses`: string array

Special runtime behavior:

- `Text.modifiers.styleRole = "markdown"` enables Markdown rendering in the current Swift renderer.

## 4. Elements

### 4.1 `Text`

Shape:

```json
{
  "Text": {
    "text": "Hello",
    "url": "cell:///Porthole/example.title",
    "keypath": "title",
    "modifiers": {}
  }
}
```

Fields:

- `text`: optional string
- `url`: optional string
- `keypath`: optional string
- `modifiers`: optional object

Rules:

- Use `text` for static copy.
- Use `keypath` mainly when the element receives row-local data, typically inside `List` or `Reference`.
- Use `url` for top-level remote lookup.
- Current Swift behavior prefers row-local `keypath` resolution, then `text`, then `url`.

### 4.2 `TextField`

Shape:

```json
{
  "TextField": {
    "text": "Optional initial text",
    "sourceKeypath": "profile.name",
    "targetKeypath": "profile.name.set",
    "placeholder": "Name",
    "modifiers": {}
  }
}
```

Fields:

- `text`: optional string
- `sourceKeypath`: optional string
- `targetKeypath`: optional string
- `placeholder`: optional string
- `modifiers`: optional object

Rules:

- Use for single-line input.
- Current Swift renderer writes to `targetKeypath` on submit, not on every keystroke.

### 4.3 `TextArea`

Shape:

```json
{
  "TextArea": {
    "text": "Optional initial text",
    "sourceKeypath": "chat.editorDraft",
    "targetKeypath": "chat.editorDraft.set",
    "placeholder": "Write message",
    "minLines": 4,
    "maxLines": 10,
    "submitOnEnter": false,
    "modifiers": {}
  }
}
```

Fields:

- `text`: optional string
- `sourceKeypath`: optional string
- `targetKeypath`: optional string
- `placeholder`: optional string
- `minLines`: optional integer
- `maxLines`: optional integer
- `submitOnEnter`: optional bool
- `modifiers`: optional object

Rules:

- Use for multi-line input.
- Current Swift renderer debounces persistence to `targetKeypath`.
- `submitOnEnter: true` switches enter-key behavior toward submit.

### 4.4 `Image`

Shape:

```json
{
  "Image": {
    "name": "hero_art",
    "url": "https://example.invalid/hero.png",
    "type": "png",
    "resizable": true,
    "scaledToFit": true,
    "padding": 8,
    "modifiers": {}
  }
}
```

Fields:

- `url`: optional string
- `name`: optional string
- `type`: optional string
- `resizable`: optional bool
- `scaledToFit`: optional bool
- `padding`: optional number
- `modifiers`: optional object

Rules:

- Put `resizable` and `scaledToFit` on `Image`, not inside `modifiers`.
- Current Swift renderer uses `name`, `resizable`, `scaledToFit`, and `padding`.
- `url` and `type` exist in the model but are not currently rendered as remote images in the newer Swift renderer.

### 4.5 `Spacer`

Shape:

```json
{
  "Spacer": {
    "width": 8,
    "modifiers": {}
  }
}
```

Fields:

- `width`: optional number
- `modifiers`: optional object

### 4.6 `HStack`

Shape:

```json
{
  "HStack": [
    { "Text": { "text": "A" } },
    { "Spacer": { "width": 8 } },
    { "Text": { "text": "B" } }
  ]
}
```

Rules:

- Payload is an array only.
- Do not emit `elements`, `spacing`, or `alignment` for `HStack`.
- Even though the Swift type has a `modifiers` property, the current wire format does not encode it.
- Current Swift renderer uses fixed spacing and centered alignment for stacks.

### 4.7 `VStack`

Shape:

```json
{
  "VStack": [
    { "Text": { "text": "Title" } },
    { "Text": { "text": "Body" } }
  ]
}
```

Rules:

- Same constraints as `HStack`.
- No stack-level `modifiers`, `spacing`, or `alignment` in the current JSON contract.

### 4.8 `List`

Shape:

```json
{
  "List": {
    "topic": "agreements",
    "keypath": "cell:///Porthole/agreements",
    "filterTypes": ["event"],
    "selectionMode": "multiple",
    "selectionValueKeypath": "agreementId",
    "selectionStateKeypath": "workbench.selection.set",
    "selectionActionKeypath": "workbench.selection.preview",
    "activationActionKeypath": "workbench.selection.open",
    "selectionPayloadMode": "selected_ids",
    "allowsEmptySelection": false,
    "elements": [],
    "flowElementSkeleton": {
      "VStack": [
        { "Text": { "keypath": "title" } }
      ]
    },
    "modifiers": {}
  }
}
```

Fields:

- `topic`: optional string
- `keypath`: optional string
- `filterTypes`: optional string array
- `selectionMode`: optional `"none" | "single" | "multiple"`
- `selectionValueKeypath`: optional string
- `selectionStateKeypath`: optional string
- `selectionActionKeypath`: optional string
- `activationActionKeypath`: optional string
- `selectionPayloadMode`: optional `"item" | "item_id" | "selected_items" | "selected_ids"`
- `allowsEmptySelection`: optional bool
- `elements`: optional array of inline values
- `flowElementSkeleton`: optional wrapped `VStack`
- `modifiers`: optional object

Rules:

- Use `flowElementSkeleton` for row templating.
- If `selectionPayloadMode` is `item_id` or `selected_ids`, `selectionValueKeypath` is required.
- Current Swift renderer supports visual selection and selection/activation writes through `CellListView`.

### 4.9 `Object`

Shape:

```json
{
  "Object": {
    "elements": {
      "title": { "Text": { "text": "Hello" } },
      "value": { "Text": { "text": "42" } }
    },
    "modifiers": {}
  }
}
```

Fields:

- `elements`: required object mapping string keys to `SkeletonElement`
- `modifiers`: optional object

Rules:

- Always emit wrapped `Object`.
- Decoder still accepts the legacy unwrapped form, but Gemini must not generate it.

### 4.10 `Reference`

Shape:

```json
{
  "Reference": {
    "topic": "purposes",
    "keypath": "cell:///Porthole/purposes",
    "filterTypes": ["event"],
    "flowElementSkeleton": {
      "VStack": [
        { "Text": { "keypath": "title" } }
      ]
    },
    "scaledToFit": false,
    "padding": 8,
    "modifiers": {}
  }
}
```

Fields:

- `topic`: required string
- `keypath`: required string
- `filterTypes`: optional string array
- `flowElementSkeleton`: optional wrapped `VStack`
- `scaledToFit`: optional bool
- `padding`: optional number
- `modifiers`: optional object

### 4.11 `Button`

Shape:

```json
{
  "Button": {
    "keypath": "chat.submitDraft",
    "label": "Send",
    "url": "cell:///Porthole",
    "payload": {
      "draftId": "draft-1",
      "urgent": true
    },
    "modifiers": {}
  }
}
```

Fields:

- `keypath`: required string
- `label`: required string
- `url`: optional string
- `payload`: optional JSON value
- `modifiers`: optional object

Rules:

- `payload` is natural JSON because it is encoded as `ValueType`.
- If `payload` is present, current runtime performs a `set`.
- If `payload` is absent, current runtime performs a `get`.
- Be conservative with visual button styling. In the current Swift renderer, generic modifiers do not provide the same rich text-color control on `Button` that `Text` gets.

### 4.12 `Divider`

Shape:

```json
{
  "Divider": {
    "modifiers": {}
  }
}
```

Fields:

- `modifiers`: optional object

### 4.13 `ScrollView`

Shape:

```json
{
  "ScrollView": {
    "axis": "vertical",
    "elements": [
      { "Text": { "text": "Row 1" } },
      { "Text": { "text": "Row 2" } }
    ],
    "modifiers": {}
  }
}
```

Fields:

- `axis`: optional `"vertical"` or `"horizontal"`
- `elements`: required array of `SkeletonElement`
- `modifiers`: optional object

### 4.14 `Section`

Shape:

```json
{
  "Section": {
    "header": { "Text": { "text": "Header" } },
    "footer": { "Text": { "text": "Footer" } },
    "content": [
      { "TextField": { "placeholder": "Name" } }
    ],
    "modifiers": {}
  }
}
```

Fields:

- `header`: optional `SkeletonElement`
- `footer`: optional `SkeletonElement`
- `content`: required array of `SkeletonElement`
- `modifiers`: optional object

### 4.15 `ZStack`

Shape:

```json
{
  "ZStack": {
    "elements": [
      { "Image": { "name": "background" } },
      { "Text": { "text": "Overlay" } }
    ],
    "modifiers": {}
  }
}
```

Fields:

- `elements`: required array of `SkeletonElement`
- `modifiers`: optional object

Rules:

- Order matters: earlier elements are behind later elements.

### 4.16 `Grid`

Shape:

```json
{
  "Grid": {
    "columns": [
      { "type": "adaptive", "min": 120, "max": 200 }
    ],
    "spacing": 12,
    "elements": [
      { "Text": { "text": "A" } },
      { "Text": { "text": "B" } }
    ],
    "modifiers": {}
  }
}
```

Fields:

- `columns`: required array of grid column objects
- `spacing`: optional number
- `elements`: required array of `SkeletonElement`
- `modifiers`: optional object

Grid column object:

- `type`: required `"fixed" | "flexible" | "adaptive"`
- `value`: optional number, used with `fixed`
- `min`: optional number, used with `flexible` or `adaptive`
- `max`: optional number, used with `flexible` or `adaptive`

Rules:

- No row/column span support in current JSON contract.
- Current Swift renderer maps this to `LazyVGrid`.

### 4.17 `Toggle`

Shape:

```json
{
  "Toggle": {
    "label": "Enabled",
    "keypath": "settings.enabled",
    "isOn": true,
    "modifiers": {}
  }
}
```

Fields:

- `label`: required string
- `keypath`: required string
- `isOn`: required bool
- `modifiers`: optional object

Rules:

- Current Swift renderer binds toggle changes to the runtime via `set`.

## 5. Canonical Caveats

- Emit canonical `flowElementSkeleton`.
- Emit wrapped `Object`.
- Do not emit legacy keys unless you are intentionally testing backward compatibility.
- Prefer omitting runtime-generated `id` fields.
- Prefer natural JSON for `Button.payload`.
- Keep `Text.keypath` for row-local or user-info-bound data. Use `url` for top-level remote text.

## 6. Things Gemini Must Not Invent

Do not invent any of these unless the renderer is extended first:

- `spacing` on `HStack` / `VStack`
- `alignment` on `HStack` / `VStack`
- gradients, blur, material, masks, or corner-specific radius fields
- absolute positioning or anchored overlays
- tabs, sheets, navigation stacks, charts, badges, or chips as first-class Skeleton elements
- remote image behavior that the current Swift renderer does not implement
