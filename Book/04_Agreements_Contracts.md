
# Chapter 04 — Agreements and Contracts

Last verified against code: 2026-07-13.

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

### 2.1 Canonical `RWXS` permission form

A compact Grant permission is written as exactly four ordered positions:

| Position | Meaning | Authority granted |
| --- | --- | --- |
| `r` | Read | Read or receive the value/output at the granted keypath. |
| `w` | Write | Write or change the value/state at the granted keypath. |
| `x` | Execute | Invoke the granted operation. |
| `s` | Storage | Persist or retain received output beyond the active operation. |

A dash means that authority is absent. Examples:

- `r---`: read only; no persistent retention authority
- `r--s`: read and retain
- `---s`: retain output already received through a separate authorized path
- `rwxs`: all four permissions
- `----`: no permission and therefore never a successful request

The canonical form uses lowercase wire characters. `R`, `W`, `X`, and `S` may
be used as prose names, but are not accepted as permission-string characters.

### 2.2 What Storage permission proves

`S` is authorization evidence, not digital-rights-management technology. A
signed, identity-bound Contract containing an `S` Grant can prove that the
subject was allowed to retain the specified output under the Contract's
keypath, domain, conditions, purpose, and duration. The bare string `---s`
without that proof path is not evidence by itself.

A compliant consumer without `S` may perform the volatile processing needed
to complete the authorized operation, but must not keep a persistent copy.
Persistent copies include files, databases, durable caches, logs, backups,
training datasets, and equivalent retained representations. A Contract may
narrow this boundary further through Conditions.

CellProtocol cannot prevent a non-compliant or malicious recipient from
copying output after it has been revealed. The value of `S` is that authorized
retention is explicit and auditable, and unauthorized retention can be shown
as a Contract violation with consequences outside the copy mechanism itself.

### 2.3 Storage is not forwarding

`S` does not authorize disclosure, redistribution, publication, or forwarding.
Those actions need a separately defined capability and Contract path. Before
forwarding retained material, the sender must be able to show both:

1. authority to retain the source material; and
2. authority to disclose it to the intended recipient.

The recipient then needs its own applicable authority. A forwarded copy does
not inherit the sender's Contract automatically.

### 2.4 Compatibility and implementation boundary

New code and generated Explore contracts must emit four-character permissions.
The Swift runtime still decodes legacy three-character forms (`rwx`) and
legacy six-character group/other forms without granting Storage. Canonical
group/other input uses two four-character segments (eight characters total).
The persisted integer representation remains compatible: the existing
read/write/execute bits are unchanged and Storage is additive.

`S` is also distinct from `ColdStorageCondition`. `S` governs whether a
Contract subject may retain output. `ColdStorageCondition` governs how the
runtime may persist an inactive Cell as part of lifecycle policy.

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
- persistent retention requires `S`; it is never inferred from read access
- Storage authority never implies forwarding or redistribution authority
- behavior is deterministic and replayable  

## 8. Summary

Agreements express what an identity *wants*.  
Contracts define what the Cell *allows*.  
Conditions and evidence determine *when* a Contract is valid.  
Resolver enforces everything deterministically.

This results in a safe, decentralized, privacy-preserving permission model.
