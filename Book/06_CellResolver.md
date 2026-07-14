
# Chapter 06 — CellResolver

The CellResolver is a principal routing, enforcement, and coordination boundary
within the HAVEN runtime. It can resolve Cells and bridges and apply the
implemented identity, Agreement, Grant, proof, lifecycle, and transport checks
at resolver-mediated entry points. It is not evidence that every internal call,
Cell implementation, storage backend, or remote peer is safe or deterministic.
Current test counts, published SHAs, and unresolved boundaries are recorded in
the
[HAVEN cross-repository robustness audit](../Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md).

## 1. Core Responsibilities

Current resolver responsibilities include:

- identity validation  
- contract and capability enforcement  
- condition evaluation  
- subscription supervision  
- selected flow connection and lifecycle coordination
- selected storage/load integration
- transport supervision  

Production hosts should route protected external access through the supported
Resolver/Cell authorization boundary. Internal direct calls and app-specific
adapters still require review; a renderer or transport must not become an
authorization bypass.

## 2. Lifecycle Management

The runtime implements parts of this lifecycle through Resolver registration,
Cell readiness, access, persistence, and connection mutation:

- **Instantiation** — the Cell is created and initial state is loaded.  
- **Activation** — the Cell becomes available for Absorb and Meddle.  
- **Running** — Emit, Absorb, Meddle operate normally.  
- **Connection mutation** — supported subscriptions may be paused, resumed, or
  detached through requester-aware operations.
- **Release** — local resources may be cancelled; persistence and remote
  acknowledgement are separate contracts.

Only transitions exposed by the selected runtime APIs are observable. Generic
CellProtocol does not promise that every transition is durably logged or
replayable; callers that need completion must use the waitable APIs and test
the relevant host/transport path.

## 3. Identity and Contract Enforcement

For supported resolver-mediated protected actions, authorization may validate:

- signature correctness  
- identity/proof consistency and required domain binding
- verified owner proof, Contract/Grant, or explicit cell-specific policy
- contract grants the requested capability  
- implemented conditions are satisfied
- any required purpose is declared  
- any required evidence is included  
- group approvals (optional) are valid  

If no accepted authorization path succeeds, the call must be rejected with a
typed decision.

This supports authorization at the audited boundary. It does not make internal
direct calls, unregistered hosts, or application fallback automatically safe.

## 4. Flow Supervision

Generic `FlowElement` does not itself guarantee a signature, timestamp, global
sequence, durable history, or replay. A concrete flow/transport policy may
validate:

- declared local ordering/sequence constraints
- producer or requester identity/proof where the contract requires it
- signatures where the selected wire contract carries them
- metadata must be well-formed  
- transport envelope must be intact  

If an error occurs:

- subscription may be paused  
- replay may be triggered  
- contracts may be revoked  
- Cell may be suspended  

Those responses are implementation choices. They require contract tests and do
not establish universal distributed stability or auditability.

## 5. Replay Engine Integration

Where a Cell/runtime implements replay, the Resolver may help coordinate:

- loads flow history  
- replays FlowElements in exact order  
- applying the Cell's declared replay semantics

Replay is used for:

- debugging  
- crash recovery  
- evidence generation  
- offline synchronization  
- compliance auditing  

Exact reproduction is **NOT PROVEN** by having a flow stream. It requires a
complete durable history, stable ordering, deterministic handlers, compatible
state/schema versions, and a tested replay contract.

## 6. Storage Integration

Resolver can cooperate with storage implementations to:

- persist Cell state  
- persist FlowElement history when configured
- retrieve previous versions  
- support reloading under a declared storage contract

Any claim of durable ordering, crash atomicity, or process-restart restoration
must be established by that storage backend's tests.

## 7. Error Handling and Supervisors

Resolver and hosts can act as supervisors:

- detects anomalies  
- isolates failing components  
- reroutes or terminates subscriptions  
- triggers fallback strategies  

Fault containment is a goal, not a universal guarantee. In-process Cells can
still trap, exhaust resources, block executors, or corrupt shared state; hosts
need isolation, bounds, cancellation, and failure-path tests proportional to
risk.

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

The CellResolver is a central enforcement boundary for supported HAVEN paths:

- approves or rejects resolver-mediated interactions
- enforces implemented contracts, grants, proofs, and cell-specific policies
- coordinates selected lifecycle and error handling
- enforces transport security policy for WebSocket endpoints  
- resolves remote host routes from `cell://host/...` to `ws(s)://...`

It is necessary infrastructure for the current runtime, but trust still depends
on the Cell, vault, proof, policy, storage, bridge, and host honoring the same
tested contract.
