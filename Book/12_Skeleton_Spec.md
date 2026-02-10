# Chapter 12 — Skeleton Specification

This chapter defines the JSON encoding and element semantics for Skeleton UI, based on the current Swift implementation in:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonElementView.swift`

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

Source:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

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

Fields:
- array of `SkeletonElement`

### 3.6 List

```json
{
  "List": {
    "topic": "feed.topic",
    "keypath": "cell:///Porthole/feed",
    "filterTypes": ["event"],
    "elements": [],
    "modifiers": { "padding": 8 }
  }
}
```

Fields:
- `topic` (String, optional)
- `keypath` (String, optional)
- `filterTypes` (String array, optional)
- `elements` (ValueTypeList, optional)
- `flowElementSkeleton` (VStack, optional)
- `modifiers` (optional)

Note: `flowElementSkeleton` is the canonical spelling in code.

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
    "elements": [
      { "Text": { "text": "A" } },
      { "Text": { "text": "B" } }
    ]
  }
}
```

Fields:
- `columns` (array of `{ type, value?, min?, max? }`)
- `spacing` (Double, optional)
- `elements` (array of SkeletonElement)
- `modifiers` (optional)

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

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonElementView.swift`

## 5. Encoding Caveats

The current implementation has two interoperability risks:

1. **Object wrapper mismatch**: encoding vs decoding differs for `Object`.  
2. **Legacy key spelling**: some stored JSON may still use `flowELementSkeleton`.  

If you are generating JSON manually or with agents, use the names shown in this spec to be consistent with decoding.
