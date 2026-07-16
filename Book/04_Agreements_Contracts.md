
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
- persistent retention requires `S`; it is never inferred from read access
- Storage authority never implies forwarding or redistribution authority
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
