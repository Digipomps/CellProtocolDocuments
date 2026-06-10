
# Chapter 07 — Scaffold and Runtime Model

The Scaffold is the execution environment that hosts Cells, Resolvers, storage,
identity vaults, and transport bridges. It functions like a minimal operating
system designed specifically for deterministic, privacy-first distributed
applications within HAVEN.

## 1. Goals of the Scaffold

The Scaffold runtime aims to provide:

- **deterministic execution** across all devices and environments  
- **isolation** between Cells to ensure safety  
- **structured concurrency** with supervision  
- **local-first operation**, with optional networking  
- **full replayability** for debugging and audit  
- **modular extensibility** without affecting the protocol core  

The Scaffold is intentionally small, stable, and predictable.

## 1.1 Scaffold Boundaries and Repo Strategy

`CellScaffold` should be treated as a reference/workbench scaffold, not as the
long-term deployment unit for every HAVEN or DiMy surface.

Near-term, it is acceptable to incubate new runtime capabilities inside
`CellScaffold` while their interfaces are still changing. Once the seams are
clear, domain-specific or operationally-specific runtime surfaces should be
split into their own focused scaffolds.

Recommended boundary:

- `Digipomps/HAVEN` keeps open, reusable protocol/runtime work:
  CellProtocol, generic cells, diagnostics, reference scaffolds, documentation,
  and public examples.
- DiMy-specific products should move into separate scaffolds or repos, for
  example conference, SMI, miniting, or other commercial/domain-specific
  surfaces.
- The user simulation runtime should eventually become a minimal scaffold of
  its own, depending only on CellProtocol/CellBase, the needed transport/runtime
  libraries, and scenario/persona artifacts.

This avoids turning the reference scaffold into a monolith and makes it easier
to run, deploy, license, scale, and audit each surface independently.

Extraction should not happen too early. First let the implementation prove the
right shape inside the workbench scaffold, then extract when the boundary is
visible.

Trigger to revisit this decision:

- the user simulation scaffold has passed real bridgehead integration against a
  target scaffold
- the coordinator/worker API, metrics, sharding, and run-artifact format are
  stable enough that downstream users can depend on them
- at least one domain-specific DiMy surface needs deployment without the full
  CellScaffold workbench payload
- shared bootstrap concerns are clear enough to extract into a small
  `ScaffoldRuntime` or `CellScaffoldKit` layer instead of copying runtime setup
  across repos

When these conditions are met, prefer extracting the simulator first. It has a
clean operational purpose, a narrow dependency surface, and fewer product UI
concerns than conference or SMI scaffolds.

## 2. Major Components

### 2.1 Resolver  
The enforcement engine that validates identity, capabilities, conditions, and
flow integrity.

### 2.2 Storage Engine  
Responsible for:

- state persistence  
- FlowElement history  
- replay data  
- safe snapshots  

### 2.3 Identity Vault  
Manages private keys, rotation, signing, and local cryptographic operations.

Runtime hardening rule:

- all generated key/IV/nonce bytes must come from OS-backed CSPRNG sources
  (Apple: `SecRandomCopyBytes`, Linux: `/dev/urandom`)
- deterministic or convenience random APIs are not valid entropy sources for
  cryptographic material

### 2.4 Replay Engine  
Ensures state and events can always be reconstructed.

### 2.5 Transport Bridges  
Provide network connectivity without altering semantics.

Supported transports include:

- WebSocket  
- QUIC  
- WebRTC  
- IPC  
- offline bundles  

### 2.6 Scheduler  
Coordinates when Cells run, ensuring predictable order and deterministic state
changes.

### 2.7 Supervisors  
Monitor Cells, Bridges, and subscriptions for errors and anomalies.

## 3. Execution Model

The Scaffold enforces:

- all outward behavior goes through Emit  
- all state changes go through Meddle  
- all access is mediated by the Resolver  
- all flows are recorded for replay  
- all Cells operate independently unless explicitly connected  

### Deterministic Scheduling  
Given the same:

- inputs  
- state  
- flow history  

… the Scaffold guarantees the same outcome.

## 4. Storage, Snapshots, and Replay

### 4.1 Storage  
The storage layer ensures:

- atomic writes  
- ordered FlowElement persistence  
- safe startup and shutdown  

### 4.2 Snapshots  
Snapshots allow:

- fast startup  
- checkpointing for long-running systems  
- offline packaging for bundle sync  

### 4.3 Replay  
Replay is triggered for:

- debugging  
- crash recovery  
- offline sync  
- evidence generation  

Replay must produce identical results.

## 5. Transport Integration

Transport bridges:

- serialize and wrap FlowElements into envelopes  
- maintain ordering  
- verify signatures  
- reconnect automatically when possible  
- handle multi-hop relaying  

Transport never introduces semantic meaning.

## 6. Local-First Operation

HAVEN systems often run:

- entirely offline  
- on local networks  
- in edge devices  
- with periodic sync to peers  

The Scaffold is optimized for these environments.

## 7. Supervision and Fault Management

The Scaffold isolates failures:

- faulty Cells cannot crash others  
- failing Bridges are restarted  
- invalid flows cause safe termination  
- contract violations revoke capabilities  

Errors escalate deterministically, not chaotically.

## 8. Summary

The Scaffold provides:

- a safe runtime for Cells  
- deterministic execution  
- modular transport support  
- secure identity and contract enforcement  
- full replay and auditability  
- local-first, privacy-preserving operation  

It is the foundation for running HAVEN applications across desktops, servers,
mobile devices, and constrained environments.
