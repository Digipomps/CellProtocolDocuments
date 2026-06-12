
# Chapter 06 — CellResolver

The CellResolver is the enforcement and coordination authority within the HAVEN
runtime. It ensures that all interaction with a Cell follows CellProtocol
correctly, safely, and deterministically.

## 1. Core Responsibilities

The Resolver enforces every rule in the ecosystem:

- identity validation  
- contract and capability enforcement  
- condition evaluation  
- subscription supervision  
- flow ordering and integrity  
- replay correctness  
- storage integration  
- transport supervision  

Nothing bypasses the Resolver.

## 2. Lifecycle Management

The Resolver manages the full Cell lifecycle:

- **Instantiation** — the Cell is created and initial state is loaded.  
- **Activation** — the Cell becomes available for Absorb and Meddle.  
- **Running** — Emit, Absorb, Meddle operate normally.  
- **Suspension** — temporarily paused due to error or admin action.  
- **Termination** — Cell is safely shut down; state is persisted.

Lifecycle transitions are deterministic and logged in flow history.

## 3. Identity and Contract Enforcement

For every inbound action (Absorb or Meddle), the Resolver validates:

- signature correctness  
- identity exists and belongs to correct domain  
- contract exists for that identity  
- contract grants the requested capability  
- all conditions are satisfied  
- any required purpose is declared  
- any required evidence is included  
- group approvals (optional) are valid  

If any check fails, the call is rejected.

This guarantees that all state changes and data access happen only with proper
authorization.

## 4. Flow Supervision

The Resolver monitors every FlowElement:

- sequence numbers must increment correctly  
- producer identity must match the Cell  
- signatures must be valid  
- metadata must be well-formed  
- transport envelope must be intact  

If an error occurs:

- subscription may be paused  
- replay may be triggered  
- contracts may be revoked  
- Cell may be suspended  

Flow supervision ensures that distributed systems remain stable and auditable.

## 5. Replay Engine Integration

The Resolver coordinates replay:

- loads flow history  
- replays FlowElements in exact order  
- restores state deterministically  

Replay is used for:

- debugging  
- crash recovery  
- evidence generation  
- offline synchronization  
- compliance auditing  

Replay guarantees that distributed behavior can always be reproduced.

## 6. Storage Integration

Resolver cooperates with the storage engine to:

- persist Cell state  
- persist FlowElement history  
- retrieve previous versions  
- support deterministic reloading  

The storage layer must preserve ordering and atomicity.

## 7. Error Handling and Supervisors

Resolver acts as a supervisor:

- detects anomalies  
- isolates failing components  
- reroutes or terminates subscriptions  
- triggers fallback strategies  

Cells never crash the system; Resolver contains all faults.

## 8. Remote Host Routing (`cell://<host>/<CellName>`)

Resolver now supports explicit routing from remote `cell://` references to
WebSocket bridge endpoints.

Use case:

- input: `cell://example.org/LoginCell`
- resolved bridge endpoint: `ws(s)://example.org/<websocketEndpoint>/LoginCell`

Registration API:

```swift
let resolver = CellResolver.sharedInstance
resolver.registerRemoteCellHost(
    "example.org",
    route: RemoteCellHostRoute(
        websocketEndpoint: "bridgehead",
        schemePreference: .automatic
    )
)
```

Route model:

- `RemoteCellHostRoute.websocketEndpoint`  
  Path prefix used before `<CellName>` (default: `bridgehead`)
- `RemoteCellHostRoute.schemePreference`  
  - `.automatic`: selects `ws` in debug/dev mode and `wss` in production mode
  - `.ws`: forces `ws` (still blocked by production policy)
  - `.wss`: forces `wss`

Lifecycle helpers:

- `registerRemoteCellHost(_:, route:)`
- `unregisterRemoteCellHost(_:)`
- `remoteCellHostRoutesSnapshot()`

If a remote `cell://host/...` reference is used without registration, resolver
throws `missingRemoteCellHostRegistration`.

## 9. Resolver-Level WebSocket Security Policy

Resolver now enforces a global WebSocket security policy via `CellBase`:

```swift
CellBase.webSocketSecurityPolicy = .developmentOnlyInsecureAllowed
// or
CellBase.webSocketSecurityPolicy = .requireTLS
```

Behavior:

- In development mode, insecure `ws://` can be allowed for local iteration.
- In production mode (`.requireTLS`), insecure `ws://` is rejected.
- Rejections throw `insecureWebSocketNotAllowed(endpoint:)`.

This enforcement applies both to direct `ws://...` endpoints and to
`cell://host/...` references that resolve to WebSocket URLs.

## 10. Summary

The CellResolver is the “law keeper” of HAVEN:

- approves or rejects all interactions  
- enforces all contracts and capabilities  
- protects flows, identity, and state  
- keeps the system deterministic  
- orchestrates lifecycle, replay, and error handling  
- enforces transport security policy for WebSocket endpoints  
- resolves remote host routes from `cell://host/...` to `ws(s)://...`

Without the Resolver, trust in distributed computation would not be possible.
