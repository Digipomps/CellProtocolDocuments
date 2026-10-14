
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
- -> `wss://example.org/bridgehead/LoginCell` (prod)
- -> `ws://example.org/bridgehead/LoginCell` (dev, when allowed)

Registration:

```swift
resolver.registerRemoteCellHost(
    "example.org",
    route: RemoteCellHostRoute(
        websocketEndpoint: "bridgehead",
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

### 9.1 Verify resource admission and EOF retirement separately

Owning and joining Tasks at stop does not establish bounded resource use while
running. Before copying callback payloads or creating per-frame Tasks, reserve
both record count and retained bytes per connection and across the service.
Keep reservations for executing work until it actually returns; cancellation
alone is not a release. Include HTTP handlers, upgrade continuations and tiny
pipe records when examining neighbouring queues. Check caller concurrency
limits before treating a per-run bound as a service-wide bound.

Use actual callbacks with held consumers, mixed text/binary, exact quota and
quota-plus-one, then verify release, another connection and restart. Remove each
per-peer and shared count/byte guard separately. Removing the retention defer is
a separate control: it can make a nominally bounded queue unbounded again.

EOF, resolver unregistration, subscription cancellation and deallocation are
different observations. Track weak references and producer cancellation, and
hold already admitted outgoing work while testing terminal stop. A pipe peer
may close stdout while staying alive; merely removing its readability callback
can leave a pending RPC forever. Initiate owned retirement independently of a
suspended consumer, drain accepted terminal bytes, and join admitted callbacks.
Do not let that callback join its own lifetime scope.

Local evidence from D235 (2026-10-12): physical WebSocket quota tests, five
independent frame-control removals, HTTP/tiny-record negative probes, and a
synthetic Codex peer that closes stdout while remaining alive. See
`HAVEN-Deploy/_handoff/ARBEIDSBENK/D235-ASTRA-FUNN-RETTET-22.md` from the HAVEN root.
These are local repair/test results, not installation evidence. The D235 local
candidate adds terminal retirement in BridgeBase, where feed Tasks are actually
created. Its focused physical feed/EOF and pending-proof tests pass; the final
port and review status is recorded in the handoff above. A transport-only stop
guard cannot establish ownership of work created before the transport call.

Retire the command registry as well as subscriptions. A pending command can
retain a requester whose proof vault points back to the bridge. A TTL does not
bound the number or bytes admitted during that interval, and a stream entry may
be deliberately exempt from expiry. Test count and byte limits independently,
capacity reuse after removal, and rejection of late registrations after EOF.

Admission refusal must also complete the caller's observable result. Returning
no Task while leaving a Future or publisher pending is a lifecycle leak even
when memory admission is bounded. If proof request or timer registration fails,
stop before sending the challenge. D235 exercised saturated callbacks, EOF,
normal connect and refused proof timers before and after these repairs. For
privacy checks with competing stdout-EOF and process-exit diagnoses, select
each terminal path deterministically and attest the selected branch; mutating
only the other branch can produce a false green control-removal result.

For an authorized local repair of a dependency, keep its exact commit in the
consumer manifest and lockfile. D235 verified a process-local Git URL rewrite
(`GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0=url.file://<owned-checkout>.insteadOf`,
`GIT_CONFIG_VALUE_0=<original-origin>`) through the bounded SwiftPM runner. This
lets Git resolve the unpublished commit from an owned checkout without changing
persistent Git configuration or pushing a ref. Record the dependency commit,
source hashes and resolution fixture; this is local test provenance, not proof
that the commit is published or available to another installer. Restore local
path mutation fixtures byte-for-byte before final pinned verification.

The shared SwiftPM cache can retain test bundles from a dependency's standalone
test run. D235 W22-r2 had all seven expected AgentD bundles plus three CP bundles;
the unchanged strict runner rejected that inventory before starting its first
full regression. This is a fixture failure, not failed product assertions or a
completed full test run. Preserve the actual inventory and failing receipt.
An isolated product view was verified with inert fixtures to expose exactly the
declared package bundles while retaining library links, and to reject missing
or unexplained bundles. The subsequent authorized D235B W22B port verified actual
compiled execution through this view: the unchanged strict runner ran exactly
seven declared package bundles, 425 test functions in each of three rounds, with
identical names and multiplicities and all W21 functions preserved (one explicit
signature migration to a parameterized stderr test). Only the three declared CP
bundles were excluded. The outer candidate-bound footer and queue receipt were
both terminal green; both source trees remained byte-identical and clean.
Evidence: `HAVEN-Deploy/_handoff/ARBEIDSBENK/D235-W22B-VERIFIED.json` and
`HAVEN-Deploy/_handoff/ARBEIDSBENK/D235-W22B-EVIDENCE/auxiliary/products-selection.json`.
Do not delete shared cache products or weaken completeness checks to make the
inventory appear green. Inert selection proof and real compiled execution are
separate obligations; retain both, together with the original failing receipt.

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
