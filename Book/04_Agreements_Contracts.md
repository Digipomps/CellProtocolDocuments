
# Chapter 04 — Agreements and Contracts

Agreements and Contracts define HAVEN’s explicit capability-based authorization
model. Nothing in HAVEN is implicit: all authority must be granted through a
Contract, and every Contract must be justified and verifiable.

## 1. Agreements

An Agreement is a request from an Identity asking for specific capabilities.

It contains:

- requesting identity  
- list of requested capabilities  
- optional declared purpose  
- optional evidence (verifiable credentials, endorsements, proofs)  

Agreements express intent but *do not* grant access by themselves.

They are always evaluated by the Resolver.

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

Capabilities are never broad or implicit. They always map to concrete actions.

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

Evidence is local and contextual — *never global*.

## 5. ConnectState

During Absorb, Agreements are resolved into a ConnectState:

- **connected** — Contract accepted  
- **signContract(...)** — Contract exists but caller must approve it  
- **denied(reason)** — Contract cannot be issued  

ConnectState ensures clients always know exactly what is required.

## 6. Enforcement

Resolver enforces all Contracts:

- checks identity validity  
- checks capability permissions for Meddle and Absorb  
- verifies Conditions  
- rejects calls lacking permission  
- handles automatic revocation  

Automatic revocation occurs if:

- conditions fail  
- identity is revoked  
- contract expires  
- required group approvals are withdrawn  

## 7. Security Properties

The system guarantees:

- no authority without explicit Contract  
- all permission logic is transparent and auditable  
- contracts are identity-bound and domain-scoped  
- behavior is deterministic and replayable  

## 8. Summary

Agreements express what an identity *wants*.  
Contracts define what the Cell *allows*.  
Conditions and evidence determine *when* a Contract is valid.  
Resolver enforces everything deterministically.

This results in a safe, decentralized, privacy-preserving permission model.
