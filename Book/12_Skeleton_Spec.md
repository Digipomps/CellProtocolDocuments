# Chapter 12 — Skeleton Specification

This chapter defines the JSON encoding and element semantics for Skeleton UI, based on the current Swift implementation in:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`
- `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift`
- `CellScaffold/Public/js/skeleton-runtime.js`

Important:

- `SkeletonElementView.swift` is deprecated and should not be treated as the canonical Apple renderer anymore.
- The canonical model still lives in `SkeletonDescription.swift`. Web and Apple runtimes may tolerate extra shapes, but portable JSON should follow the model, not renderer-only shortcuts.
- Production skeletons must validate key bindings against Explore contracts
  before preview or commit. Use
  [Chapter 22 - Explore Contracts for Skeleton and Cell Authoring](22_Explore_Contracts_For_Skeleton_Authoring.md)
  and `Tools/Explore/skeleton_explore_validator.py` when a skeleton reads from
  or writes to a Cell.

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
- `motionHint` (String enum: `appear` | `expand` | `collapse` |
  `minimize` | `restore` | `replace` | `emphasize`)
- `motionSourceRole` (String)

Source:

- `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

Motion note:

- `motionHint` is semantic metadata, not renderer-owned keyframes. It tells
  Porthole/Binding why an element appeared or changed.
- `motionSourceRole` points to a semantic source such as `chat-composer`,
  `suggestion-card` or `minimized-helper-pill`.
- Renderers must respect reduced-motion preferences and may replace movement
  with fade/highlight or no animation.
- Motion must never be the only signal that a component appeared.

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

### 3.16 Visualization

`Visualization` is the generic skeleton element for renderer-owned visual surfaces. Maps use the existing element with `kind: "map"`; do not introduce product-specific map element names.

Portable map skeleton pattern:

```json
{
  "Visualization": {
    "kind": "map",
    "keypath": "spatial.state.map",
    "stateKeypath": "spatial.state.selection",
    "actionKeypath": "spatial.selectFeature"
  }
}
```

Fields:
- `kind` (String, required; `map` is the portable spatial map kind)
- `keypath` (String, optional, resolves the visualization data/spec from state)
- `stateKeypath` (String, optional, resolves current selection/state)
- `actionKeypath` (String, optional, fired only by explicit user interaction)
- `spec` (ValueType, optional inline spec)
- `modifiers` (optional)

`kind: "map"` expects a `MapVisualizationSpec`:

```json
{
  "coordinateSpace": "geospatial",
  "base": {
    "kind": "tiles",
    "urlTemplate": "https://tiles.example/{z}/{x}/{y}.png",
    "attribution": "Map data attribution"
  },
  "viewport": {
    "center": [10.7522, 59.9139],
    "zoom": 14
  },
  "fit": "fitFeatures",
  "features": [
    {
      "id": "artifact-oslo-1",
      "geometry": {
        "type": "point",
        "coordinates": [10.7522, 59.9139]
      },
      "label": "Coffee note",
      "selectable": true,
      "properties": {
        "schema": "haven.spatial.feature.v1",
        "featureId": "artifact-oslo-1",
        "kind": "artifact",
        "positionDisclosure": "coarse",
        "accuracyMeters": 250,
        "purposeRefs": ["personal.chat.assist.spatial-query"],
        "interestRefs": ["coffee"],
        "matchExplanation": {
          "summary": "Matched purpose and interest.",
          "matchedPurposeRefs": ["personal.chat.assist.spatial-query"],
          "matchedInterestRefs": ["coffee"],
          "score": 13
        },
        "contactEndpoint": {
          "endpointId": "contact-anna",
          "displayName": "Anna",
          "cellEndpoint": "cell:///ContactEndpoint"
        },
        "mediaRefs": [
          {
            "id": "image-1",
            "kind": "image",
            "cellEndpoint": "cell:///Media/image-1",
            "previewKeypath": "preview"
          },
          {
            "id": "anchor-1",
            "kind": "ar"
          }
        ],
        "visibility": "nearby",
        "expiresAt": "2026-05-29T12:00:00Z",
        "sourceCellEndpoint": "cell:///SpatialArtifact",
        "proofRefs": ["proof:publisher-consent"]
      }
    }
  ],
  "revision": "spatial-v1"
}
```

Map spec fields:
- `coordinateSpace`: `geospatial` or `planar`
- `base`: optional `tiles` or `image` base. Omit it when the host owns the provider/base-map policy.
- `viewport`: optional `center`, `zoom`, or `bounds`
- `fit`: `manual`, `fitBase`, or `fitFeatures`
- `features`: array of point/polyline/polygon features
- `revision`: optional stable revision string for renderer diffing

Spatial feature payload:
- `MapVisualizationFeature.properties` may carry `schema: "haven.spatial.feature.v1"`.
- Required identity fields are `featureId`, `kind`, `positionDisclosure`, `purposeRefs`, `visibility`, and `expiresAt`.
- Optional context fields are `accuracyMeters`, `interestRefs`, `matchExplanation`, `contactEndpoint`, `mediaRefs`, `sourceCellEndpoint`, and `proofRefs`.
- `contactEndpoint` must be a safe `ContactEndpointCell` reference. Do not expose raw routes, push tokens, global user IDs, or private owner hashes.
- Media is represented as refs, not blobs. AR in v1 is either `mediaRefs[].kind = "ar"` or `kind = "arAnchor"` with a normal marker fallback.

Privacy defaults:
- Coarse, time-limited position is the default.
- Precise position requires an explicit grant.
- Spatial publication requires an explicit purpose and TTL.
- Expired or revoked features must not project into the map.
- Co-Pilot may query, explain, or draft; publish/revoke actions require an explicit user action.

Renderer notes:
- Web uses Leaflet for portable map rendering and should keep the base provider neutral. If `tile.openstreetmap.org` tiles are used, the host must follow OSMF tile policy for attribution, identifiable client behavior, caching, and no bulk/offline prefetch.
- Apple uses MapKit for geospatial maps and planar rendering for image/floor maps.
- Real AR camera overlays are a host capability, not part of the v1 skeleton map contract.

References for this contract:
- OSMF tile policy: https://operations.osmfoundation.org/policies/tiles/
- W3C Geolocation privacy guidance: https://www.w3.org/TR/geolocation/
- Leaflet layer/vector/GeoJSON reference: https://leafletjs.com/reference.html
- Apple MapKit reference: https://developer.apple.com/documentation/mapkit

`kind: "calendar"` expects a `CalendarVisualizationSpec` backed by canonical
HAVEN calendar data. Do not introduce a new `Calendar` skeleton element; the
portable renderer surface is still `Visualization`.

Portable calendar skeleton pattern:

```json
{
  "Visualization": {
    "kind": "calendar",
    "keypath": "calendar.state.visualization",
    "stateKeypath": "calendar.state.selectedOccurrenceID",
    "actionKeypath": "calendar.queryOccurrences"
  }
}
```

`CalendarVisualizationSpec` fields:
- `schema`: `haven.calendar.visualization.v1`
- `view`: `agenda`, `day`, `week`, `month`, or `timeline`
- `range`: object with `startAt` and `endAt`
- `timezone`: IANA timezone string or `UTC`
- `itemsKeypath`: keypath for expanded `CalendarOccurrence` rows, normally `calendar.occurrences`
- `selectionKeypath`: optional keypath for current occurrence selection
- `actionKeypath`: optional action keypath for explicit user requests
- `capabilities`: host capability flags, for example selection or import/export affordances
- `display`: renderer labels and empty-state text
- `fallback`: list/grid fallback metadata for renderers that do not support calendar layout
- `occurrences`: expanded occurrence rows for the requested range

Calendar data is a Cell contract, not renderer-owned state:
- Authoritative item data uses `haven.calendar.item.v1`.
- Collections use `haven.calendar.collection.v1`.
- Render rows use `haven.calendar.occurrence.v1`.
- Recurrence is stored close to iCalendar (`rrule`, `rdate`, `exdate`, `recurrenceId`), but renderers consume already-expanded occurrences for a concrete range.
- ICS import/export preserves the iCalendar identity and time semantics where possible; CalDAV and native EventKit-style calendars are adapters over the same canonical store, not new skeleton data models.

Renderer notes:
- Web/Porthole and Apple/Porthole render agenda/day/week/month/timeline as readable occurrence lists in v1.
- Unsupported renderers must show the `fallback` list/grid and a visible diagnostic rather than a blank surface.
- Drag/drop, complex recurrence editing, and native calendar permission prompts are host capabilities outside the v1 skeleton contract.

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
3. Collection grids are now data-bindable, `Picker` now exists as a first-class single-selection primitive, and `Visualization(kind: "map")` exists for portable map surfaces. Domain contracts still need to expose honest option lists, state snapshots, and spatial privacy rules; a renderer primitive alone does not create an honest workflow.
4. `Visualization(kind: "map")` supports marker/vector/image-map fallback today. AR camera overlays, provider-specific offline maps, and native device permission prompts remain host capabilities outside the v1 skeleton contract.
