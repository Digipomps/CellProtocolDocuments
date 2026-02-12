# Chapter 10 — Quickstart

This chapter provides a minimal, concrete setup for running CellProtocol in a Swift app. It is intentionally short, practical, and directly tied to the current Swift implementation.

## 1. Prerequisites

- Swift 5.8+
- macOS 13+ (or iOS 16+)
- The CellProtocol package in your workspace

The package exposes multiple libraries:

- `CellBase` (protocol core)
- `CellApple` (Apple runtime: IdentityVault + bridging + UI utilities)
- `CellVapor` (server runtime)

See `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Package.swift`.

## 2. Minimal Apple Runtime Setup

If you are building a macOS or iOS app, the fastest way to bootstrap is to use `AppInitializer`, which wires up:

- `CellBase.defaultIdentityVault`
- `CellBase.defaultCellResolver`
- default cell resolves
- storage and typed cell utilities
- default transports

Code:

```swift
import CellApple

@main
struct DemoApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .task {
                    await AppInitializer.initialize()
                }
        }
    }
}
```

`AppInitializer` lives in:

`/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/AppInitializer.swift`

It also sets transport defaults for security:

- registers both `ws` and `wss` transports
- allows insecure `ws://` only in debug/dev mode
- requires `wss://` in release mode
- supports default remote host mapping for `cell://<host>/<CellName>`

## 3. Manual Setup (No AppInitializer)

If you want full control, you can initialize the defaults directly:

```swift
import CellBase
import CellApple

func configureCellBase() async {
    let identityVault = IdentityVault.shared
    _ = await identityVault.initialize()
    CellBase.defaultIdentityVault = identityVault

    let resolver = CellResolver.sharedInstance
    CellBase.defaultCellResolver = resolver

    // Transport policy:
    // - debug/dev: ws can be allowed
    // - prod: require wss
    CellBase.webSocketSecurityPolicy = .developmentOnlyInsecureAllowed

    try? await resolver.registerTransport(AppleBridgeTransport.self, for: "ws")
    try? await resolver.registerTransport(AppleBridgeTransport.self, for: "wss")

    // Remote host mapping:
    // cell://example.org/LoginCell -> ws(s)://example.org/publishersws/LoginCell
    resolver.registerRemoteCellHost(
        "example.org",
        route: RemoteCellHostRoute(websocketEndpoint: "publishersws", schemePreference: .automatic)
    )

    // Optional but recommended: typed cell storage + document root
    CellBase.documentRootPath = "/path/to/documents"
    let tcUtility = TypedCellUtility(storage: FileSystemCellStorage())
    resolver.tcUtility = tcUtility
    CellBase.typedCellUtility = tcUtility
}
```

## 4. Create a Minimal Cell

The simplest approach is to subclass `GeneralCell` and add intercepts for `get` and `set`:

```swift
import CellBase

public actor EchoCell: GeneralCell {
    public override init(owner: Identity) async throws {
        try await super.init(owner: owner)

        await addInterceptForGet(requester: owner, key: "echo.value") { keypath, requester in
            return .string("Hello from EchoCell")
        }

        await addInterceptForSet(requester: owner, key: "echo.set") { keypath, value, requester in
            return .string("ok")
        }
    }
}
```

`GeneralCell` and intercepts are defined in:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`

## 5. Register the Cell

Cells are resolved by name through the `CellResolver`:

```swift
let resolver = CellResolver.sharedInstance
try await resolver.addCellResolve(
    name: "Echo",
    cellScope: .identityUnique,
    persistency: .persistant,
    identityDomain: "private",
    type: EchoCell.self
)
```

## 6. Resolve and Interact with the Cell

```swift
guard let vault = CellBase.defaultIdentityVault else { return }
let identity = await vault.identity(for: "private", makeNewIfNotFound: true)

let emitter = try await resolver.cellAtEndpoint(endpoint: "cell:///Echo", requester: identity)
let meddle = emitter as? Meddle

let value = try await meddle?.get(keypath: "echo.value", requester: identity)
```

## 7. Next Steps

Once you can resolve a cell and call `get`/`set`, you should:

- add `FlowElement` output via `pushFlowElement(...)`
- define `CellConfiguration` and a `SkeletonElement` UI
- document your cell via `Explore`

See:

- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/11_Developer_Guide_Cell.md`
- `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Book/12_Skeleton_Spec.md`

## 8. Running Skeleton Tests (Xcode)

Skeleton encoding/decoding tests live in the `CellBaseTests` target.

- Open the workspace you use for app development (for example `Binding.xcworkspace`).
- Ensure the workspace includes the local `CellProtocol` package folder (not just a remote reference).
- Select the `CellBaseTests` test target in the test plan.
- Run the `SkeletonTests` test suite.

If `CellBaseTests` shows as “missing”, verify these two entries match your local layout:

- `/Users/kjetil/Build/Digipomps/HAVEN/Binding/Binding.xcworkspace/contents.xcworkspacedata` includes `group:../CellProtocol`
- `/Users/kjetil/Build/Digipomps/HAVEN/Binding/Binding.xcodeproj/xcshareddata/xctestplans/Binding.xctestplan` uses `container:../CellProtocol`
