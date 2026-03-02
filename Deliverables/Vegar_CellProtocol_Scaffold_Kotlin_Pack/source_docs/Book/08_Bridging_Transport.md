
# Chapter 08 — Bridging and Transport

Bridging and Transport ensure that HAVEN remains **semantically stable and fully
independent of any specific network technology**. Transport is a replaceable
detail: it must never influence meaning, ordering, identity, or authorization.

## 1. Envelope Model

Every FlowElement is wrapped in a transport-neutral **envelope** containing:

- sequence number  
- type identifier  
- payload (ASCII-safe)  
- producer identity  
- signature  
- domain  
- metadata  

Envelopes are:

- immutable  
- ordered  
- cryptographically verifiable  
- semantics-preserving  

No transport may modify an envelope.

## 2. Supported Transport Modes

Transport modules convert envelopes to bytes and deliver them safely. HAVEN
supports multiple families of transport:

### 2.1 WebSocket  
For browser-based and mobile-friendly integrations.

### 2.2 QUIC  
For low-latency, reliable multi-stream communication.

### 2.3 WebRTC  
For direct peer-to-peer connections with NAT traversal.

### 2.4 IPC (Inter-Process Communication)  
For local-first systems using:

- pipes  
- domain sockets  
- shared memory  
- OS messaging primitives  

### 2.5 Offline Bundles  
For environments without stable connectivity:

- humanitarian field use  
- disaster recovery  
- remote or air-gapped environments  

Bundles contain:

- recorded flow history  
- state snapshots  
- identity evidence  

## 3. Reliability Modes

Transport modules may operate in different modes:

### 3.1 Reliable Mode  
Guarantees delivery and ordering.

### 3.2 Best-Effort Mode  
Allowed only if semantics permit event loss.

### 3.3 Replay Mode  
Used for:

- reconnection  
- state repair  
- offline synchronization  
- deterministic verification  

## 4. Supervision

The Resolver supervises all bridges and ensures:

- reconnection on failure  
- detection of invalid envelopes  
- prevention of sequence gaps  
- rejection of invalid signatures  
- correct domain handling  

Transport errors **never** cause Cells to behave inconsistently.

## 5. Multi-Hop Routing

Envelopes may pass through:

- relay servers  
- mesh networks  
- peer-to-peer overlays  

Rules for routing:

- no hop may modify the envelope  
- no hop may resign an envelope  
- ordering must be preserved  
- private keys never leave the vault  

This supports:

- community mesh networks  
- local-first connectivity  
- federation models  
- offline-first sync topologies  

## 6. Security Guarantees

Transport is required to preserve:

- envelope integrity  
- ordering  
- identity provenance  
- signature validity  
- replay correctness  

Transport cannot add or remove authority.

## 7. WebSocket Policy (Dev vs Prod)

CellProtocol now supports explicit WebSocket security policy so development can
use `ws://`, while production requires `wss://`.

Policy surface:

```swift
CellBase.webSocketSecurityPolicy = .developmentOnlyInsecureAllowed
// or
CellBase.webSocketSecurityPolicy = .requireTLS
```

Runtime rule:

- `.developmentOnlyInsecureAllowed`: `ws://` is allowed in debug workflows.
- `.requireTLS`: `ws://` is rejected, `wss://` is required.

This is enforced in resolver endpoint handling, not just by convention.

## 8. Remote `cell://host` Bridge Mapping

For remote hosts, `cell://host/<CellName>` can be mapped to WebSocket bridge
endpoints using a host registry.

Example mapping:

- `cell://example.org/LoginCell`
- -> `wss://example.org/publishersws/LoginCell` (prod)
- -> `ws://example.org/publishersws/LoginCell` (dev, when allowed)

Registration:

```swift
resolver.registerRemoteCellHost(
    "example.org",
    route: RemoteCellHostRoute(
        websocketEndpoint: "publishersws",
        schemePreference: .automatic
    )
)
```

This makes transport selection deterministic and removes hardcoded endpoint
construction from feature code.

## 9. Developer Notes

- do not rely on timing guarantees  
- preserve ASCII safety  
- prefer QUIC for bulk or multi-stream systems  
- prefer WebRTC for local-first systems  
- use bundles for intermittent connectivity  
- log envelope inconsistencies for diagnostics  
- keep `ws://` limited to development environments  
- register remote host routes centrally during bootstrap

## 10. Summary

Bridging and Transport make HAVEN:

- resilient  
- portable  
- offline-capable  
- verifiable  
- tamper-resistant  
- semantically stable across all networks  

Cells behave identically regardless of how data travels. This is essential for a
user-owned distributed ecosystem.
