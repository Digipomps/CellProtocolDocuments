
# Chapter 05 — Flows and Stream Lifecycle

Flows are the primary communication mechanism in HAVEN. Every Cell exposes a
single outbound event stream via the Emit interface. Flows define all observable
behavior and must be deterministic, ordered, and replayable.

## 1. FlowElements

A FlowElement contains:

- sequence number  
- type identifier  
- payload  
- producer identity  
- timestamp or logical clock  
- metadata  

Properties:

- immutable  
- strictly ordered  
- cryptographically signed  
- domain-scoped  

FlowElements form the full history of how a Cell behaves over time.

## 2. Stream Lifecycle

A subscription to a Cell’s flow follows this lifecycle:

### 2.1 Discovery  
The subscriber inspects metadata via Explore to understand available actions and
flow schemas.

### 2.2 Negotiation  
The subscriber sends an Agreement through Absorb, requesting access.

### 2.3 Attachment  
Resolver validates the Agreement, evaluates Conditions, and issues a Contract.
If successful, the subscriber becomes attached to the Emit stream.

### 2.4 Streaming  
The subscriber receives FlowElements in strict sequence order.

### 2.5 Supervision  
Resolver monitors the flow for:

- signature validity  
- sequence gaps  
- domain mismatches  
- contract expiration  
- transport inconsistencies  

### 2.6 Termination  
A subscription ends when:

- the subscriber disconnects  
- a contract is revoked  
- conditions fail  
- errors require shutdown  

## 3. Replay

Replay is a first-class property.

Every stream can be replayed deterministically for:

- recovery  
- debugging  
- auditing  
- offline synchronization  
- simulation and testing  

Replay always produces the exact same sequence as the original run.

Replay ensures full transparency and makes distributed systems easier to reason
about.

## 4. Transport Independence

Flows must behave identically across any transport:

- WebSocket  
- QUIC  
- WebRTC  
- IPC  
- offline bundles  

Transport must not influence:

- ordering  
- delivery semantics  
- signature validation  
- identity behavior  

Envelopes guarantee that FlowElements remain intact across all transports.

## 5. Flow Graphs

Cells can be combined into graphs:

- linear pipelines  
- branching trees  
- DAGs  
- meshes  
- hybrid topologies  

The Scaffold runtime coordinates execution across these graphs.

Flows enable rich, composable distributed systems without requiring shared state.

## 6. Summary

Flows provide:

- a deterministic event backbone  
- replayable behavior  
- strict ordering  
- transparent auditing  
- transport independence  

They form the observable history and functional output of every Cell, making
HAVEN predictable, inspectable, and resilient.
