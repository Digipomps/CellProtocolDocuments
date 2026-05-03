# Attachment Surface Thread Prompt (CellProtocol)

Use this prompt when implementing shared attachment functionality in `CellProtocol` so the same `CellConfiguration.skeleton` can render a working attachment surface in every renderer.

## Goal

Add a renderer-agnostic skeleton contract for file and image attachment that supports both drag-and-drop and an explicit attach dialog fallback.

The result must be usable by all projects that render skeleton:

- `CellScaffold` / Porthole / web
- `Binding`
- future renderers that only know the shared `CellProtocol` model

## Scope Boundary

This prompt is for shared protocol/model work in `CellProtocol`.

The output from this thread should be:

- shared skeleton types
- shared value/state/action payloads
- transport/encode/decode coverage
- one or more canonical examples/fixtures

The output from this thread should not be:

- web-only picker logic
- SwiftUI/AppKit/UIKit rendering details
- product-specific conference/profile editor workarounds

## Problem To Solve

Current product surfaces need an image/file field that feels like a real editor surface:

- users should be able to drop a file directly onto a visible target when the platform supports it
- users should always have a visible fallback action such as `Attach…` or `Choose file`
- renderers must not invent their own incompatible attachment contracts
- the cell/runtime contract must not expose raw local file paths as durable values

Today we can fake this with text fields and helper text, but we do not yet have a general attachment primitive or state contract in skeleton.

## Deliverable

Introduce a shared skeleton-level attachment surface contract that covers:

1. declarative rendering of an attachment field / drop target
2. attachment lifecycle state
3. authoring-time configuration such as accepted types and multiplicity
4. value transport in a renderer-independent shape
5. action hooks for pick, drop, remove, replace, retry, and preview/open

Do not implement this as a product-specific conference workaround.

## Execution Order

1. Define the shared skeleton surface and its naming.
2. Define the durable value contract.
3. Define the transient state contract.
4. Define the action payload contract.
5. Add encode/decode and round-trip tests.
6. Add one canonical example that renderer projects can consume.
7. Only after that should renderer repos implement platform behavior on top.

If the work uncovers uncertainty about naming or transport shape, resolve it here in `CellProtocol` rather than pushing ambiguity down into `CellScaffold` or `Binding`.

## Proposed Shape

You may rename the types if they fit existing naming rules better, but keep the semantics.

### New skeleton element

Add a dedicated element similar to:

```swift
struct SkeletonAttachmentField: Codable, Equatable {
    var title: String?
    var subtitle: String?
    var helperText: String?
    var valueKeypath: String?
    var stateKeypath: String?
    var actionKeypath: String?
    var acceptedContentTypes: [String]?
    var preferredKinds: [String]?
    var allowsMultiple: Bool?
    var isRequired: Bool?
    var supportsDrop: Bool?
    var previewStyle: String?
    var emptyTitle: String?
    var emptyMessage: String?
    var modifiers: SkeletonModifiers?
}
```

Expected semantics:

- `valueKeypath` points to the normalized attachment value or list of values
- `stateKeypath` points to transient UI/runtime state such as uploading or error
- `actionKeypath` is the command surface for pick/drop/remove/retry/open
- `acceptedContentTypes` uses MIME-like or UTType-like identifiers that renderers can map locally
- `supportsDrop` means "show a drop affordance when the renderer/platform can do it", not "drop is the only way"

### Shared value contract

The stored value should be renderer-independent and safe to persist.

Target shape:

```swift
struct AttachmentValue: Codable, Equatable {
    var id: String
    var kind: String
    var displayName: String?
    var mimeType: String?
    var byteSize: Int?
    var previewURL: String?
    var assetReference: String?
    var metadata: [String: CellValue]?
}
```

Rules:

- persisted values must refer to app-controlled assets/references, not raw local filesystem paths
- a renderer may use a temporary local file during selection/upload, but that must stay transient
- image-specific metadata such as dimensions may be added in `metadata`

### Shared transient state contract

Add a normalized state model for the editor surface, for example:

```swift
enum AttachmentTransferPhase: String, Codable {
    case idle
    case dragTargeted
    case picking
    case uploading
    case attached
    case failed
}

struct AttachmentFieldState: Codable, Equatable {
    var phase: AttachmentTransferPhase
    var progressFraction: Double?
    var errorMessage: String?
    var canOpen: Bool?
    var canReplace: Bool?
    var canRemove: Bool?
}
```

This state is what renderers should observe when deciding how to show progress, errors, preview affordances, and retry/remove controls.

### Shared action contract

Add a typed action payload so all renderers can send the same intent back into the cell:

```swift
enum AttachmentFieldActionKind: String, Codable {
    case pick
    case drop
    case remove
    case replace
    case retry
    case openPreview
}

struct AttachmentFieldAction: Codable, Equatable {
    var kind: AttachmentFieldActionKind
    var fieldID: String?
    var temporaryPayload: [String: CellValue]?
}
```

Rules:

- renderers send `pick` before opening their native picker when needed
- renderers send `drop` with transient payload metadata when a file is dropped
- cells remain authoritative for authorization, validation, persistence, and final asset binding
- protocol should make the renderer/cell boundary explicit enough that web and native do not need private side contracts

## UX Rules That Must Be Supported Everywhere

- Show a visible attachment affordance even when drag-and-drop is unavailable.
- Drop is an enhancement, not a requirement.
- Multiple attachments should be opt-in and explicit.
- Errors must be field-local and actionable.
- Remove/replace must be available near the current attachment preview.
- Keyboard and assistive-technology users must have a non-drag path.
- Empty state text must be authorable from skeleton, not hardcoded in one renderer.

## Non-Goals

- Do not build a conference-only image uploader.
- Do not hardcode a web-only `input[type=file]` contract into protocol.
- Do not define a Binding-only or CellScaffold-only payload shape in parallel.
- Do not persist raw local paths in `CellValue`.
- Do not bypass `Meddle.get/set` or existing cell authorization rules.

## Verification

At minimum:

- protocol encode/decode tests for the new skeleton element
- tests for action/value/state payload round-tripping
- one fixture/example showing:
  - empty attachment field
  - uploading state
  - attached image/file state

## Handoff Expectation

When this prompt is complete, a renderer thread should be able to say:

- "the shared attachment contract exists"
- "these are the exact `CellProtocol` types/payloads to consume"
- "we do not need to invent any renderer-local attachment model"

## Expected Outcome

After this lands, renderer projects should be able to implement the same attachment field without inventing their own model, and product surfaces like profile editors can expose a real `drop here / attach…` workflow instead of helper text that leads nowhere.
