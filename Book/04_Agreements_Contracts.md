
# Chapter 04 — Agreements and Contracts

Agreements and Contracts define HAVEN’s explicit capability-based authorization
model. Nothing in HAVEN is implicit: all authority must be granted through a
verified authorization path. A Contract/Grant is the ordinary delegated path;
verified owner proof and deliberately narrow cell-specific policy are also
implemented paths. None may be inferred from a cookie, renderer, transport, or
unverified identity label.

Current strict-admission, TrustedIssuer, and remaining public-publication
evidence is recorded in the
[HAVEN cross-repository robustness audit](../Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md).

## 1. Agreements

An Agreement is a request from an Identity asking for specific capabilities.

It contains:

- requesting identity  
- list of requested capabilities  
- optional declared purpose  
- optional evidence (verifiable credentials, endorsements, proofs)  

Agreements express intent but *do not* grant access by themselves.

Supported `GeneralCell`/Resolver admission evaluates them before issuing or
using a Contract. Constructing an Agreement value alone performs no evaluation.

## 2. Contracts

A Contract is the Cell’s explicit authorization decision.

A Contract defines:

- which capabilities are granted  
- to which identity  
- under which conditions  
- for how long  
- with what domain restrictions  

Examples of capabilities:

- `flow.read`  
- `flow.write`  
- `state.write`  
- `action.invoke:addItem`  
- `purpose.execute:moderation`

Capabilities should be as narrow and concrete as the supported keypath/action
contract permits. Root or wildcard-like grants are broader and require explicit
review; a capability name alone does not prove least privilege.

## 3. Conditions

Conditions restrict when a Contract is valid. Examples:

- a verifiable credential is required  
- an endorsement is required  
- time-based or expiry conditions  
- domain must match  
- group approval threshold must be met  
- caller must declare a matching Purpose  

Conditions may be evaluated:

- at contract creation time  
- at contract usage time  
- continuously by the Resolver during subscription

## 4. Evidence

Evidence supports Conditions.

Examples:

- verifiable credentials  
- endorsements signed by trusted individuals  
- group approvals  
- proof-of-action via replayable flows  
- institution-issued credentials  

Issuers may be:

- organisations  
- communities  
- peers  
- individuals trusted in that domain  

Evidence should be scoped to the relevant context. Reusing an issuer,
identifier, or credential across contexts can create global correlation and is
not prevented by the evidence type alone.

## 5. ConnectState

During Absorb, Agreements are resolved into a ConnectState:

- **connected** — Contract accepted  
- **signContract(...)** — Contract exists but caller must approve it  
- **denied(reason)** — Contract cannot be issued  

ConnectState communicates the implemented admission result. Clients still need
typed diagnostics and retry/expiry handling; it is not proof that every policy
can be automatically resolved.

## 6. Enforcement

The supported Resolver/Cell access path enforces Contracts by:

- checking identity/proof validity
- checking capability permissions for Meddle and Absorb
- verifying implemented Conditions
- rejecting calls lacking permission
- rejecting expired or otherwise invalid authorization at use time

Authorization must be denied when the implemented use-time checks establish
that:

- conditions fail  
- identity is revoked  
- contract expires  
- required group approvals are withdrawn  

## 7. Security properties and proof boundary

For a supported and tested access path:

- no authority is accepted without verified owner proof, a valid
  Contract/Grant, or an explicit cell-specific decision
- the authorization decision records its path and reason
- signed Contracts bind the declared identity/proof material and scope
- replay/determinism are separate lifecycle and storage properties, not
  automatic consequences of having a Contract

## 8. Summary

Agreements express what an identity *wants*.  
Contracts define what the Cell *allows*.  
Conditions and evidence determine *when* a Contract is valid.  
Supported resolver/Cell boundaries enforce the implemented policy. Conditions,
expiry, proof freshness, revocation, and concurrent admission each require
their own regression evidence.

This is intended to provide a decentralized, privacy-preserving permission
model; each concrete access path still needs positive and negative proof.
