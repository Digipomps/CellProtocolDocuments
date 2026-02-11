# Chapter 11 — Developer Guide: Implementing a Cell

This chapter is a practical guide for building a new Cell in Swift that works with the current CellProtocol runtime. It assumes you already read the conceptual chapters.

## 1. Decide the Cell's Role

Before coding, define:

- **Purpose**: What problem does the cell solve?
- **Meddle surface**: Which explicit actions should change state?
- **Emit surface**: Which events should be observable?
- **Explore surface**: What metadata and schemas should be discoverable?
- **Identity domain**: Which domain should it operate in?

These map directly to CellProtocol interfaces in:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Protocols/CellProtocol.swift`

## 2. Create a Cell Class

The simplest and most common approach is to subclass `GeneralCell`.

```swift
import CellBase

public actor ExampleCell: GeneralCell {
    public override init(owner: Identity) async throws {
        try await super.init(owner: owner)
        try await setupIntercepts()
    }

    private func setupIntercepts() async throws {
        let owner = self.owner

        await addInterceptForGet(requester: owner, key: "example.state") { keypath, requester in
            return .string("ready")
        }

        await addInterceptForSet(requester: owner, key: "example.set") { keypath, value, requester in
            // Mutate state here, then return a ValueType response
            return .string("ok")
        }
    }
}
```

Relevant implementation:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`

Notes:

- `addInterceptForSet(...)` registers the key in the schema dictionary internally.
- `addInterceptForGet(...)` does **not** register schema by default.
- Only the owner (or pre-init hook) can set intercepts.

## 3. Define Schema and Descriptions

`GeneralCell` holds:

- `schemaDict` — key → schema
- `schemaDescriptionDict` — key → description

These are used by `Explore` calls. The current runtime only auto-registers schema on `addInterceptForSet`. If you want schema for read-only keys, register them explicitly.

## 4. Emit FlowElements

To publish observable behavior, push a `FlowElement` via `pushFlowElement`:

```swift
let msg = FlowElement(
    title: "example.event",
    content: .string("Hello"),
    properties: .init(type: .event, contentType: .string)
)
msg.topic = "example.topic"
msg.origin = self.uuid

pushFlowElement(msg, requester: owner)
```

Relevant code:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/FeedItem/FlowElement.swift`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`

## 5. Register the Cell with the Resolver

Cells are resolved by name using `CellResolver.addCellResolve(...)`.

```swift
let resolver = CellResolver.sharedInstance
try await resolver.addCellResolve(
    name: "Example",
    cellScope: .identityUnique,
    persistency: .persistant,
    identityDomain: "private",
    type: ExampleCell.self
)
```

Resolver implementation:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift`

## 6. Provide a CellConfiguration

A `CellConfiguration` describes:

- external cell references (`cellReferences`)
- subscriptions and initial `set` values
- optional UI skeleton

Structs:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift`

Minimal example:

```json
{
  "name": "Example Config",
  "cellReferences": [
    {
      "endpoint": "cell:///Example",
      "label": "example",
      "subscribeFeed": true,
      "subscriptions": [],
      "setKeysAndValues": [
        { "key": "example.set", "value": "hello" }
      ]
    }
  ],
  "skeleton": {
    "Text": { "text": "Hello from Example" }
  }
}
```

## 7. Add a Skeleton UI

Skeleton UI lets the client render a cell configuration without hardcoded views.

See:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/12_Skeleton_Spec.md`

## 8. Checklist (Minimal Done Definition)

- Cell compiles and can be resolved by name.
- `get` and `set` are wired through intercepts.
- At least one `FlowElement` can be emitted.
- A `CellConfiguration` exists with valid `cellReferences`.
- A Skeleton UI exists and renders in Porthole.

## 9. Recommended Next Steps

- Add `Explore` metadata and schema descriptions.
- Define meaningful `Agreement` and conditions.
- Add real tests in `Tests/`.

## 10. Troubleshooting

If `CellBaseTests` shows as “missing” in Xcode:

- Ensure the workspace includes the local `CellProtocol` folder (not only a remote package reference).
- In the workspace, add `CellProtocol` via “Add Files to…” and choose the folder, or verify the workspace file includes `group:../CellProtocol`.
- In the test plan, ensure the `CellBaseTests` entry uses `container:../CellProtocol`.

If Skeleton encoding/decoding fails:

- Run `SkeletonTests` and check the JSON fixtures under `Tests/CellBaseTests/Fixtures/`.
- Verify the fixture uses the correct casing for `flowElementSkeleton` and `SkeletonObject` encoding matches the wrapper format.
