
# Chapter 07 — Scaffold and Runtime Model

Last verified against code: 2026-07-13.

The Scaffold is the execution environment that hosts Cells, Resolvers, storage,
identity vaults, and transport bridges. It functions like a minimal operating
system designed to host privacy-first distributed applications and make
deterministic behavior possible where Cells and runtime services satisfy a
declared contract.

For dated implementation evidence rather than architectural intent, see the
[HAVEN cross-repository robustness audit](../Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md).

## 1. Goals of the Scaffold

The Scaffold runtime aims to provide:

- **deterministic execution** for explicitly bounded, tested inputs and state
- **isolation** between Cells to ensure safety  
- **structured concurrency** with supervision  
- **local-first operation**, with optional networking  
- **replay support** where ordered durable history and replay semantics exist
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

### 2.4 Replay support
May reconstruct declared state when the runtime has a complete compatible
history and the Cell implements deterministic replay semantics.

### 2.5 Transport Bridges  
Provide network connectivity without owning Cell semantics.

Current first-party implementation evidence in this audit covers WebSocket and
local/in-process routing paths. QUIC, WebRTC, IPC, and offline bundles are
architectural targets or experiments until an owning implementation and
contract tests are identified; they must not be advertised as generally
supported transports.

### 2.6 Scheduling and concurrency
Coordinates tasks and Cell work. Swift actors, tasks, transports, and external
services do not provide a universal total order; any ordering or single-flight
claim must be explicit in the owning component.

### 2.7 Supervisors  
Monitor Cells, Bridges, and subscriptions for errors and anomalies.

## 3. Execution Model

Supported Scaffold paths should preserve these boundaries:

- outbound streams use Emit/FlowElement contracts
- externally callable state changes use explicit Meddle/action contracts
- protected external access uses Resolver/Cell authorization
- flows are recorded only when the configured runtime declares durable replay
- Cells should not share application state implicitly; explicit connections and
  process-global runtime services remain reviewable coupling points

### Deterministic Scheduling  
Given the same:

- inputs  
- state  
- flow history  

… a deterministic Cell and runtime path should produce the same declared
outcome. The claim excludes wall-clock input, randomness, external services,
unordered concurrency, missing history, and version drift unless those are
captured by the contract.

## 4. Storage, Snapshots, and Replay

### 4.1 Storage  
Storage backends that claim durable restart/replay must provide:

- atomic writes  
- ordered FlowElement persistence  
- safe startup and shutdown  

This section describes the Scaffold's own persistence duties. It is distinct
from the `s` position in a subject's `rwxs` Grant. `s` authorizes that subject
to retain received output; it does not configure the storage engine.
`ColdStorageCondition` is a third, separate concept that governs lifecycle
policy for persisting an inactive Cell.

Agreement Workbench follows the same boundary when authoring Grants. It emits
canonical four-character permissions, accepts legacy three-character input
without inferring Storage, and exposes `---s` and `r--s` as explicit retention
choices. Its user-facing guidance states that `S` permits persistent retention
of received output but does not authorize forwarding.

### 4.2 Snapshots  
Snapshots allow:

- fast startup  
- checkpointing for long-running systems  
- offline packaging for bundle sync  

A Scaffold may call `CellResolver.persistCellSnapshot(_:)` when a persistent
Cell reaches an application-defined checkpoint and waiting for eviction would
risk losing acknowledged application state. The call refuses non-persistent
Cells and reports whether the Resolver completed its selected local storage
write. The Scaffold must still authorize the triggering action and must not
interpret success as a remote replication, quorum, or crash-durability receipt.

### 4.3 Replay  
Replay is triggered for:

- debugging  
- crash recovery  
- offline sync  
- evidence generation  

A path may claim exact replay only when the same compatible inputs, state,
ordering, and deterministic handlers reproduce the declared result in a
regression gate.

### 4.4 Validated owner-private contact persistence

`EntityAnchorCell` has an additive, fail-closed contact persistence gate for
Apple and Vapor runtimes:

- reserved keypath family: `relations.validatedContacts.<relationID>`
- batch schema: `haven.entity-validated-contact-batch.v1`
- record schema: `haven.entity-validated-contact-record.v1`
- owner-signed `entity.batchPersist` authority commit is mandatory
- commit purpose is `purpose://access.audit.privacy`
- storage authorization is explicit and disclosure authorization must be false
- e-mail and E.164 telephone values, provenance, purpose refs, relation binding,
  size limits, and the closed record shape are validated before persistence
- generic direct writes and legacy batch schemas are denied for the reserved
  keypath family
- `entityContactSchema` exposes value-free schema metadata to the owner

The gate returns the normal signed Entity authority receipt and supports
read-after-write plus storage reload verification in the CellScaffold helper
path. The current receipt still declares `local_authority_only`; it is not proof
of distributed quorum or remote replication.

This does not make the rest of legacy `EntityAnchorData` strictly validated,
does not authorize contact disclosure or message delivery, and does not yet
provide selective erasure of personal values from already committed authority
journal history. Do not claim complete Entity storage validation or deletion
support from this bounded gate.

### 4.5 Owner-private relation records and interaction events

Implemented in the security integration at CellProtocol `c85754c` (2026-09-10),
with equivalent Apple and Vapor EntityAnchor admission:

- `relations.records.<relationID>` stores `haven.entity-relation-record.v1`;
- `haven.entity-relation-batch.v1` uses the existing `entity.batchPersist`
  operation and owner-proof boundary; signed commit requests retain their
  journal/receipt contract, while unsigned legacy batches remain local writes;
- direct writes, whole-family replacement, selector aliases, unknown JSON
  fields, mismatched IDs and partial-record deletion are rejected;
- a null at exactly one relation ID deletes that record, not retained journal
  history or historical backups;
- `entityRelationSchema` is an owner-only, value-free metadata surface.

New interaction events use **`haven.relation-interaction-event.v2`**. Their
stored `id` matches `chronicle[id=relation-event-<relationID>-<eventID>]`, while
`eventID` retains the short logical ID exposed by Swift `event.id`. The former
feature-branch v1 shape put the short ID into the selector field, so subsequent
reads could miss the entry and append duplicates. V1 values remain readable and
re-encodable; new admission requires v2. There is no automatic migration of
existing feature-branch chronicle data.

An identical stored event may be retried. Different content or a different
relation/event binding at an occupied v1-style address is rejected, including
within one batch. This preserves the address format without silently overwriting
colliding hyphen-separated ID pairs. It does not make the local summary fold
`applying` a deduplicating distributed merge operation.

Ordinary owner history keeps its existing `chronicle[+]` object format,
including legacy objects without an ID. The compatibility correction at
[CellProtocol `d9aebaa`](https://github.com/Digipomps/CellProtocol/blob/d9aebaa32103cf84a33ce80630469dbaaa703e32/Docs/ChronicleAppendCompatibility-2026-09-10.md)
checks both the address and payload: ordinary appends cannot supply a reserved
`relation-event-` ID or declare a relation-interaction-event schema. An exact
ordinary `chronicle[id=...]` selector cannot carry a different ID in its value.
Multiple ordinary appends preserve batch order beside protected events; they
do not participate in the reserved event collision map. Root/index/descendant
replacement remains denied. No stored history is migrated. The final consumer
gate exposed the original overly broad append rejection; the correction and
subsequent consumer pin changes require their own passing test receipts.

Capture defaults to metadata. `off` admits no event; full content requires the
already stored owner policy `person.relations.interactionPolicy = "full"`.
Malformed settings disable capture. An event cannot authorize its own content,
and a simultaneous policy change does not grant authority to that same batch.
An owner setting does not establish third-party consent. Standing and evidence
references likewise do not themselves verify a credential or grant capability.

Relation records remain private data. The channel validator excludes obvious
raw addresses; it is not a universal scrubber for names, notes or other declared
fields. A reach plan proposes an action and does not authorize or send a message.

The shared [v2 JSON fixture](https://github.com/Digipomps/CellProtocol/blob/c85754c/Tests/CellBaseTests/Fixtures/EntityRelationEventV2.json)
and [integration/migration notes](https://github.com/Digipomps/CellProtocol/blob/c5c9a4c/Docs/EntityRelationSecurityParity-2026-09-10.md)
record the tested wire shape and current boundaries. Full local regression at
this source revision: 1082 tests, zero failures; final integration/CI evidence
is tracked in the source repository.

## 5. Transport Integration

Transport bridges may:

- serialize and wrap FlowElements into envelopes  
- preserve declared ordering metadata
- carry or verify signatures when required by the wire policy
- reconnect automatically when possible  
- handle multi-hop relaying  

Transport must not own Cell authorization or application semantics. Current
bridges still need parity, ordering, denial, reconnect, and remote-
acknowledgement tests; moving bytes alone does not prove semantic equivalence.

## 6. Local-First Operation

HAVEN systems often run:

- entirely offline  
- on local networks  
- in edge devices  
- with periodic sync to peers  

The Scaffold is optimized for these environments.

## 7. Supervision and Fault Management

The Scaffold should isolate failures with explicit bounds and supervision:

- a faulty Cell should not take down unrelated services
- bridge restart/backoff must be bounded and observable
- invalid flows should fail closed for the affected path
- contract violations must be denied; revocation propagation needs its own
  implementation and tests

Errors should produce typed, observable outcomes. Universal fault containment
or deterministic escalation is not currently proven.

## 8. Summary

The Scaffold aims to provide:

- a safe runtime for Cells  
- contract-bounded deterministic execution
- modular transport support  
- secure identity and contract enforcement  
- replay and auditability where the required history is captured
- local-first, privacy-preserving operation  

It is the foundation for running HAVEN applications across desktops, servers,
mobile devices, and constrained environments.
