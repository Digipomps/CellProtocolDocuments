# Chapter 13 — Agent Instructions (Cells + Skeleton UI)

This chapter provides explicit instructions for code agents that implement new Cells and Skeleton UI definitions in the HAVEN ecosystem.

## 1. Mandatory Reading

Before making changes, read:

- [10_Quickstart.md](10_Quickstart.md)
- [11_Developer_Guide_Cell.md](11_Developer_Guide_Cell.md)
- [12_Skeleton_Spec.md](12_Skeleton_Spec.md)

## 2. Input Contract

Agents must confirm:

- the required behavior of the cell  
- which keys it exposes (`get` and `set`)  
- expected flow outputs and topics  
- identity domain and persistency  
- required UI layout (skeleton)

If any of these are ambiguous, ask for clarification before implementing.

## 3. Implementation Steps

1. Locate or create a Cell subclass.  
   - Prefer `GeneralCell` for standard cells.
2. Implement `get` and `set` intercepts.  
   - Use `addInterceptForGet` and `addInterceptForSet`.
3. Register schema entries for the keys you expose.  
   - `addInterceptForSet` registers schema automatically.  
   - If a key is read-only, register its schema explicitly.
4. Emit events using `FlowElement` and `pushFlowElement(...)`.
5. Register the cell with the resolver.  
   - Add to your scaffold or initializer (e.g. `AppInitializer`).
6. Define a `CellConfiguration` describing dependencies and initial setup.
7. Build a `SkeletonElement` tree for UI rendering.
8. Provide a JSON sample for the configuration and skeleton.

## 4. Output Requirements

Agents should deliver:

- Swift implementation of the cell  
- updated resolver registration  
- a `CellConfiguration` sample  
- a `SkeletonElement` JSON sample  
- brief usage notes or a minimal Quickstart update if needed

## 5. Validation Checklist

The output is acceptable only if:

- the cell resolves by name via `CellResolver`  
- at least one `get` and `set` key is functional  
- at least one `FlowElement` can be emitted  
- a skeleton JSON sample is provided and valid per spec  
- the configuration references correct endpoints and labels

## 6. Known Encoding Caveats

Current implementation details that affect agent output:

- `SkeletonObject` decoding expects a wrapper key `"Object"`, while encoding does not include it.  
  Agents should generate JSON using the wrapper to be safe.
- Some stored JSON may still use the legacy key `flowELementSkeleton`.  
  Use `flowElementSkeleton` for new output, and consider backward compatibility if needed.

## 7. Minimal Template

Use this as a starting point when creating new cells:

```swift
public actor ExampleCell: GeneralCell {
    public override init(owner: Identity) async throws {
        try await super.init(owner: owner)
        await addInterceptForGet(requester: owner, key: "example.state") { _, _ in
            return .string("ready")
        }
        await addInterceptForSet(requester: owner, key: "example.set") { _, _, _ in
            return .string("ok")
        }
    }
}
```

## 8. Where to Look in Code

- `GeneralCell` implementation  
  `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`

- `CellResolver` registration  
  `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift`

- `SkeletonElement` encoding  
  `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift`

- Default runtime bootstrapping  
  `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/AppInitializer.swift`

## 9. PerspectiveCell Pattern (Required for Weighted Matching)

When implementing a `GeneralCell` subclass that exposes `Perspective` functionality:

- Expose read snapshots via `GET` intercepts (for example `perspective.state`).
- Expose parameterized matching/query operations via `SET` intercepts:
  - `perspective.query.activePurposes`
  - `perspective.query.interestsFromActivePurposes`
  - `perspective.query.match`
- Return explicit weighted payloads only. Do not infer hidden features or implicit scores.
- Keep scoring deterministic and documented:
  - direct purpose route
  - via-interest route
- Include enough data for downstream ranking and explainability:
  - source/target purpose refs and weights
  - interest refs and weights when route is via-interest
  - route type and final match score

Reference contract for cross-device/scaffold matching:

- Support `referenceMode` (`local`, `portable`, `both`) in query payloads.
- Include `referenceStrategy` in responses.
- Use portable refs for interoperability when local refs differ across runtimes.

See Chapter 14 for the runtime contract and request/response fields:

- [14_Perspective_Runtime_Matching.md](14_Perspective_Runtime_Matching.md)

## 10. Documentation Placement Policy

Agents must place documentation based on ownership and portability:

- Core protocol/runtime behavior required for CellProtocol/HAVEN interoperability:
  - document in `CellProtocolDocuments` (this repo).
- App, product, or commercial behavior built on top of CellProtocol/HAVEN:
  - document in app/vendor repositories (for example DiMy repos).

If a doc starts in an app repo but describes shared protocol behavior, promote it to
`CellProtocolDocuments` and leave a short pointer in the app repo.
