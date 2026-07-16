# Chapter 01 — CellProtocol Core

This chapter describes the conceptual foundations of CellProtocol: the problem
it addresses, its design invariants, and its boundaries. Concrete interfaces
(how to program against the protocol) are covered in the next chapter.

> **Design versus implementation:** determinism, replay, auditability, privacy,
> and transport-independent semantics are goals and conditional properties,
> not blanket guarantees of every current Cell, host, bridge, or storage
> backend. A supported path may claim them only when its state, ordering,
> authorization, persistence, and replay contracts are implemented and tested.
> See the dated
> [HAVEN cross-repository robustness audit](../Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md)
> for the current evidence map and explicit `NOT PROVEN` boundaries.

## What CellProtocol is
CellProtocol is a minimal, privacy-first model intended to make deterministic
state and event behavior possible. It provides a common language for how small,
separate units (Cells) should:
- represent and change state
- express outbound streaming behavior as events (flows)
- manage access and trust explicitly
- be reproducible (replay) and auditable
- operate independently of transport and networking

## The problem it solves
Modern distributed apps often suffer from:
- hidden state and unpredictable behavior
- implicit access and “magic” APIs
- global identity and cross-domain tracking
- lack of verifiability and audit

CellProtocol addresses this by:
- making supported observable behavior explicit as state, actions, and flows
- requiring an explicit authorization path for protected access
- using domain-scoped identity (no global IDs)
- making supported mutation traceable, with replay only where history is stored
- separating semantics from transport (run locally, P2P, or via bridges)

## Core design principles
1. Minimal surface: as small as possible, sufficiently expressive.
2. Determinism: same input + same history ⇒ same outcome.
3. Capability security: no authority, including persistent retention, without
   explicit capability.
4. Domain-scoped identity: no cross-domain tracking.
5. Transport independence: semantics do not change with networking.
6. Replay first: behavior that claims replay support must record enough ordered
   information to reproduce and audit the declared result.
7. Transparency: no hidden APIs or implicit side effects.

## Required invariants and evidence boundary

- Explicit protected access: supported public boundaries must resolve authority
  through verified owner proof, a valid Contract/Grant, or an explicit
  cell-specific policy. A renderer, cookie, or transport is not authority.
- Conditional predictability: the same declared inputs, state, ordered history,
  and deterministic implementation should yield the same declared result.
- Conditional replay: a flow is replayable only when the producer/runtime
  records sufficient ordered events and the consumer defines replay semantics.
- Privacy by construction and policy: domain-scoped identities reduce global
  linkage, but deployments must still prevent identifier reuse, metadata leaks,
  and unauthorized data sharing.
- Wire portability: encoded contracts can be shared across runtimes; equivalent
  lifecycle, storage, security, and renderer behavior requires separate parity
  evidence.

## Non-goals (boundaries)
- No implicit access or “god mode”.
- No global account/ID that follows you across domains.
- No hidden side channels for mutation or communication.
- No semantics in the transport layer (bridges move bytes, not rules).

## Conceptual execution model
- Supported streaming behavior is expressed as ordered `FlowElement` values;
  state reads and explicit actions are separate interfaces.
- Protected state changes must be justified by an implemented authorization
  path at the supported access boundary.
- Authorization decisions should produce inspectable decision evidence.
- Cells are composable: they can be connected, but are isolated by default.

(Detailed interfaces for publishing events, subscribing, mutating state, and introspecting are covered in the next chapter.)

## Identity, contracts, and trust
- Identity is cryptographic and domain-scoped. An identity applies within a domain, not across domains.
- Protected access is granted through verified owner proof, explicit
  Contracts/Grants, or a deliberately narrow cell-specific policy. Absence of
  every accepted path means denial.
- Compact Grants use the canonical four-position `rwxs` form: read, write,
  execute, and Storage/retention. Storage permission is evidence of authority
  to retain output; it is not technical copy prevention or permission to
  forward it.
- Trust can be anchored in Purpose and Interests, and extended with evidence/attestations when relevant.

## Replay and audit
- A runtime may store an ordered stream and replay it when the Cell defines how
  those events reconstruct its declared state.
- Replay can support debugging, evidence, and synchronization; generic
  `FlowElement` alone does not provide durable storage, signatures, global
  sequencing, or exact state reconstruction.

## Transport and operation
- The protocol is not bound to a specific network. Bridges carry events without changing semantics.
- The system operates locally, offline, P2P, or via periodic synchronization.

## Composition and modularity
- Cells are small, self-contained modules that can be composed into larger systems.
- A Resolver enforces the implemented identity, proof, Agreement, Grant, and
  cell-specific policy checks at supported resolver-mediated boundaries.
- A Scaffold/Runtime can provide storage, replay, and supervision without changing the protocol’s semantics.

## Expected reader outcome
After this chapter, you should understand:
- why CellProtocol exists
- which problems it solves
- which invariants it targets and what evidence their claims require
- how it differs from traditional, API-centric models

In the next chapter (02_Cell_Interfaces) we will look at the concrete interfaces and how to use them in code.

## Related documentation
- [02_Cell_Interfaces.md](02_Cell_Interfaces.md) — Concrete interfaces (Emit, Absorb, Meddle, Explore, GroupProtocol)
- [03_Identity_Model.md](03_Identity_Model.md) — Cryptographic, domain-scoped identity
- [04_Agreements_Contracts.md](04_Agreements_Contracts.md) — Capability-based contracts and grants
- [05_Flows_Lifecycle.md](05_Flows_Lifecycle.md) — Event model, ordering, and replay lifecycle
- [06_CellResolver.md](06_CellResolver.md) — Resolver enforcement, connection, and capability checks
- [07_Scaffold_Runtime.md](07_Scaffold_Runtime.md) — Runtime environment, storage, replay, and supervision
- [10_Quickstart.md](10_Quickstart.md) — Minimal runnable setup
- [11_Developer_Guide_Cell.md](11_Developer_Guide_Cell.md) — Step-by-step cell implementation
- [12_Skeleton_Spec.md](12_Skeleton_Spec.md) — Skeleton UI JSON specification
- [13_Agent_Instructions.md](13_Agent_Instructions.md) — Agent workflow and checklist
- [README-CellProtocol.md](../README-CellProtocol.md) — Full documentation index
