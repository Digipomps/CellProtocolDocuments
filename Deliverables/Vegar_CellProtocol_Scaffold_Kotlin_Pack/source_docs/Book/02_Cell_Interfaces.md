
# Chapter 02 — Cell Interfaces

This chapter explains the four required interfaces and the optional fifth
interface that every HAVEN Cell may implement:

- Emit
- Absorb
- Meddle
- Explore
- GroupProtocol (optional)

Together they describe the complete operational surface of a Cell.

## 1. Emit

Emit is the outbound, append only event stream. It:

- produces FlowElements in strict sequence order
- guarantees type correctness
- is replayable
- is the only channel for observable behaviour

Emit must never mutate state and must not rely on transport. It simply hands
FlowElements to the Resolver and bridge layer.

## 2. Absorb

Absorb is the ingress for subscription requests. It is responsible for:

- collecting identity, requested capabilities and optional purpose
- checking contracts and conditions
- returning a clear ConnectState

Absorb does not grant authority directly. It asks the Resolver to evaluate
contracts. If accepted, the subscriber is attached to the Emit stream.

## 3. Meddle

Meddle is a catalogue of explicit actions that may change state. Each action:

- has a name
- has a typed argument schema
- has a required capability
- may have additional conditions

The Cell implements the actual state change logic, but the Resolver ensures that
only authorised Meddle calls reach the Cell.

## 4. Explore

Explore describes the Cell in a machine readable way. Typical fields include:

- list of Meddle actions and their schemas
- list of FlowElement types produced by Emit
- domain and version information
- labels and human oriented descriptions
- declared purposes and interests

Explore has no side effects and never exposes private state. It is essential
for tooling, documentation and graph visualisation.

## 5. GroupProtocol (optional)

GroupProtocol is used when decisions require more than one identity. It may
implement:

- threshold signatures
- quorum voting
- multi party endorsements

It follows the same determinism rules as the core and never bypasses the
Resolver.

## 6. Interface separation

The interfaces never overlap:

- Emit: output only
- Absorb: access negotiation only
- Meddle: state change only
- Explore: description only
- GroupProtocol: group decision only

This strict separation makes reasoning about a Cell safe and predictable.
