
# Chapter 02 — Cell Interfaces

This chapter explains four principal interfaces and an optional group
interface that a HAVEN Cell may implement as needed:

- Emit
- Absorb
- Meddle
- Explore
- GroupProtocol (optional)

Together with lifecycle/readiness and persistence contracts, they describe the
portable operational surface of a Cell. Not every Cell implements every
interface.

## 1. Emit

Emit is the outbound publisher interface. A concrete implementation can expose
an event stream that:

- produces typed `FlowElement` values in the producer's observed order
- can participate in replay when a runtime records sufficient history
- is the outbound streaming channel; state reads and action responses remain
  observable through their own contracts

An Emit implementation should not make transport own event semantics. Emitting
an event does not by itself prove that no state changed, that the event was
persisted, signed, globally sequenced, or remotely acknowledged.

## 2. Absorb

Absorb is the ingress for subscription requests. It is responsible for:

- collecting identity, requested capabilities and optional purpose
- checking contracts and conditions
- returning a clear ConnectState

Absorb does not grant authority merely because a request exists. Supported
implementations evaluate owner proof, Agreement/Contract/Grant, conditions, or
a narrow cell-specific policy before attaching a subscriber.

## 3. Meddle

The core Meddle surface provides generic explicit `get`/`set` operations. A
production Cell can use keypaths/intercepts as named actions and should publish
an Explore contract that declares, where applicable:

- operation name and kind
- argument/result schema
- required access/capability
- additional conditions

The Cell implements the actual state change logic. Resolver-mediated and
`GeneralCell` access paths enforce authorization; internal direct method calls
must not be presented as proof that every possible call site is mediated.

## 4. Explore

Explore describes the Cell in a machine readable way. Typical fields include:

- list of Meddle actions and their schemas
- list of FlowElement types produced by Emit
- domain and version information
- labels and human oriented descriptions
- declared purposes and interests

Explore is required to be side-effect-free and to avoid private state. That is
an authoring and validation contract; exposing an Explore implementation is not
automatic proof that its content is complete or privacy-safe.

For skeleton and generated Cell authoring, Explore contracts must describe the
operation shape, not only the key name. See
[Chapter 22 - Explore Contracts for Skeleton and Cell Authoring](22_Explore_Contracts_For_Skeleton_Authoring.md).

## 5. GroupProtocol (optional)

GroupProtocol is used when decisions require more than one identity. It may
implement:

- threshold signatures
- quorum voting
- multi party endorsements

It must use the same explicit authorization boundaries and may claim
determinism only for a defined, tested decision contract.

## 6. Interface separation

The interfaces have distinct responsibilities even when one Cell implements
several of them:

- Emit: output only
- Absorb: access negotiation only
- Meddle: explicit get/set/action access
- Explore: description only
- GroupProtocol: group decision only

Keeping these responsibilities explicit makes a Cell easier to reason about;
it does not replace readiness, authorization, persistence, and replay tests.
