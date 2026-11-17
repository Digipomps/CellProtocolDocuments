
# Chapter 04 — Agreements and Contracts

Last verified against code: 2026-09-09.

The scaffold-administrator verification below applies to section 13 on
CellScaffold branch `pdd/scaffold-admin-delegering`, worktree
`CellScaffold/_wt-sad-20260909`; it is not a staging deployment claim.

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

## 8. Signature and time semantics

The production owner-archive path uses `Contract.ownerSignedSnapshot(...)`.
This is deliberately an **issuer-signed, subject-bound** snapshot:

- the Contract issuer signs the exact Agreement bytes;
- the Contract subject and storage domain are bound into the signature;
- the current owner-archive path requires issuer, subject, EntityAnchor owner,
  and signing-key control to resolve to the same owner;
- a descriptive `counterparty` is not a counterparty signature.

The UI and APIs must not describe this as bilateral or multiparty signing.
Those semantics require a different contract format with explicit signatures
from every required party.

Cryptographic authenticity and current authorization are separate questions:

- `verifyCryptographicSignature` and `verifyHistoricalBinding` establish that
  an immutable historical Contract was signed and remains bound to the
  expected issuer, subject, and domain;
- `verifySignature` and `verifyAuthorizationBinding` additionally require the
  Contract to be temporally active now;
- `temporalStatus` reports `active`, `not_yet_valid`, `expired`, or
  `structurally_invalid`.

An expired authentic Contract therefore remains visible in history, but it
must not authorize current access.

<!-- purposeRef: purpose://candidate.tillitspakke-agentflaate.signert-kvittering -->
`ActionDecisionReceipt` and the `EffectReceipt` model
(`haven.effect-receipt.v0`) support optional `ReceiptSignature` metadata:
`signerRef`, `algorithm`, base64 `value`, and `signedAt`. Their `signed(by:)`
methods use the existing `Identity.sign` vault path over compact, sorted JSON
with UTC timestamps and the signature field omitted. `verify(against:)` uses
the caller-pinned public Identity and returns `valid`, `invalid`, or `unsigned`;
legacy decision JSON without a signature still decodes. Supported algorithms
are P256-ECDSA-SHA256 and Ed25519, selected from the identity's public key.
`signedAt` must equal the signed receipt's canonical `createdAt`: it is a
declared issuance time, not an independently witnessed signing time. Changed
binding digests invalidate verification. An authentic receipt grants no rights.

`EffectReceipt` contains host-only destination metadata, method, received byte
count, actual credential-use flag, decision/execution status, optional reason
code, and ceiling/package digest bindings. It has no URL, headers, credential
alias or response-body field; its codec rejects paths and queries in the host.
WebFetch and PurposeBoundAIGateway now issue signed receipts with owner-only append-only stores; see [Chapter 36](36_Agent_Trust_Package.md) for bindings, fleet audit, and implementation limits.

## 9. Signed Agreement Entity commit

`signedAgreementEntity.commit` is the production admission boundary for an
owner-signed Contract in `EntityAnchorCell` (Apple and Vapor runtimes). It:

1. verifies owner/key control and the active owner/subject/domain binding;
2. verifies every required TrustedIssuer evaluation receipt;
3. computes the Contract hash and immutable record-content hash;
4. rejects conflicting content for an existing Contract UUID;
5. writes the immutable record and signed persistence receipt together using
   a serialized, atomic file replacement;
6. reloads the entity file from disk and verifies record and receipt hashes
   before returning `persisted`.

The persistence receipt binds the EntityAnchor owner, record ID, entity
keypath, Contract hash, record hash, timestamp, and persistence semantics. A
successful generic `set`, a renderer status string, or a local Workbench save
is not equivalent to this receipt.

## 10. Verifiable Credential evaluation receipts

A `ProvedClaimCondition` is only a requirement declaration. It is not evidence
that a Verifiable Credential has been validated.

`trustedIssuers.evaluateSigned` returns a short-lived signed receipt only after
the concrete `cell:///TrustedIssuers` authority evaluates the credential. The
receipt binds:

- credential hash;
- issuer-policy hash and context;
- exact Agreement-condition hash;
- required credential type and subject-claim path;
- requester/subject binding result;
- revocation/status result;
- verifier endpoint, verifier signing identity, evaluation time, and expiry.

Consumers must pin the verifier to the owner of the resolved
`cell:///TrustedIssuers` cell. They must reject an otherwise valid receipt from
an attacker-selected verifier and must not reuse a receipt for another
condition. Raw credential JSON is write-only input in Agreement Workbench and
is not returned in state, persisted in the Workbench snapshot, or copied into
the signed record; the signed receipt is the durable evidence projection.

## 11. Agreement Workbench provenance contract

Agreement Workbench and Entity Studio expose three distinct layers:

| Layer | Mutability | Authority |
| --- | --- | --- |
| Agreement template | Immutable start point | No access authority |
| Draft/local snapshot | Editable or restorable as a new draft | No signature or entity-persistence claim |
| Verified signed entity record | Immutable, read-only projection from EntityAnchor | Backed by Contract verification and a signed read-after-write receipt |

Restoring history always creates a new draft. Entity Studio never trusts
editable `recordState`, `signatureValidationState`, or
`isCryptographicallySigned` values; only records re-read and verified from
EntityAnchor may appear in the verified projection.

The full surface, compact helper component, and Co-Pilot chat helper read the
same Agreement Workbench state. Chat may prefill the AI prompt, but generation,
VC evaluation, signing, and storage remain separate explicit user actions.

Production CellConfigurations reference `AgreementWorkbench`, `EntityStudio`,
`TrustedIssuers`, and `EntityAnchor` explicitly. Their published GET/SET
keypaths have typed Explore contracts so strict-mode renderers and agents can
verify the operation boundary before invocation.

## 12. Summary

Agreements express what an identity *wants*.  
Contracts define what the Cell *allows*.  
Conditions and evidence determine *when* a Contract is valid.  
Supported resolver/Cell boundaries enforce the implemented policy. Conditions,
expiry, proof freshness, revocation, and concurrent admission each require
their own regression evidence.

This is intended to provide a decentralized, privacy-preserving permission
model; each concrete access path still needs positive and negative proof.

## 13. Scaffold administrator and single-hop mandates

Last verified against code: 2026-09-09 — CellScaffold branch
`pdd/scaffold-admin-delegering`, worktree `CellScaffold/_wt-sad-20260909`.
Evidence: [PDD test results](../Deliverables/PDD_scaffold-admin-delegering_2026-09-08/TESTRESULT.md#auth)
and [acceptance boundaries](../Deliverables/PDD_scaffold-admin-delegering_2026-09-08/ACCEPT.md).
WP9 inspected source and existing results; it ran no new builds or tests.

`cell:///ScaffoldAdministratorRegistry` records one organization Entity reference
as administrator **per scaffold**. The scaffold owner registers it with verified
owner proof. Changing it requires the separate, audited
`administrator.transfer` action. Registration is an organizational attribution;
the Entity name is not a signing Identity and grants no Cell access. Public
`administrator.state` names the organization without a person's identity.
See [Chapter 07](07_Scaffold_Runtime.md#scaffold-administrator) for storage and
startup policy and [the registry contract](scaffold-administrator_v1.json).

For delegation through this model, the **mandate is the only authority-bearing
delegation artifact**. It uses the existing signed Agreement/Contract mechanism,
issued on the registered organization's behalf and bound to its recipient's
Identity and key. Existing verified owner-proof and Cell-specific Contract paths
remain separate authorization grounds. The five mandatory scope/lifetime fields
are:

| Field | Required meaning |
| --- | --- |
| `resourceRefs` | Explicit resources; use also checks the resolved Cell UUID. |
| `actionKeypaths` | Exact permitted actions; no wildcard expansion. |
| `purposeRef` | Exact purpose; `purpose://prompt.unknown` fails closed. |
| `validUntil` | Expiry; expired or excessive lifetime is rejected. |
| `revocationRef` | Reference bound to the retained central mandate record. |

Omitting any field is rejected; scope and lifetime are not filled with defaults.
The [mandate contract](scaffold-mandate_v1.json) also requires issuer, scaffold,
recipient, timestamps, signatures and explicit nullable `orgLinkRef`.

The chain is **one hop**. Issuance requires a separate scaffold-owner-signed
representative Contract bound to the organization, scaffold and current
registration/transfer receipt. A mandate is never accepted as that representative
proof. A `use` mandate requesting scaffold mandate issuance, orgLink issuance or
administrator actions is rejected. An `administrate` fixture may name
`mandate.issue` and support scaffold mandate inspection; this does not grant
onward issuance authority. Being scaffold owner alone also does not establish
authority to sign on the organization's behalf.

The required number of distinct verified signatures for `kind=administrate` is
read from registered `administrator.thresholdPolicy`. Its initial value is **1**,
with reason **«utviklingsfase, styreleder alene»**, dated
`2026-09-09T00:00:00Z`. It can be raised to 2 through the policy action without a
code change. Two signatures from the same Identity count once; `kind=use`
requires one verified representative signature. While the policy is below 2,
`runtimeAdvisories` includes `scaffold_administrator_threshold_below_two`, naming
the scaffold and reason. This is verified development policy, not evidence of
staging provisioning or a legal assessment of the signer's position.

Role labels `admin.observer`, `admin.operator`, `admin.nodeAgent` and
`admin.security` still grant **zero Cell authority** in this model.
`ScaffoldRoleIsNotAuthorityTests` protects that boundary: four role tests deny
`mandate.issue`, `administrator.register`, `administrator.transfer` and
`administrator.thresholdPolicy.set` with `agreement_or_proof_required`, just as
for an unrelated Identity. A fifth test guards increases above 48 matching
`requireAdminUser` lines and 33 `AdminRoleProfile` lines. The behavioral denials
are the authority proof; the counts are an additional review tripwire.

Mandate use checks the recipient's proof copy, signature, current administrator,
resource, action, purpose, expiry and revocation. `mandate.revoke` retains the
record and reason. `orgLink.issue` represents organizational affiliation as a
role Agreement with start, optional end and revocation; the role Agreement
alone grants no access. Revoking it invalidates dependent mandates while
retaining Entity data. Owners can inspect active mandates for their own Cells
via `mandate.list`; an unrelated requester is denied. Issuance and recorded use
retain `mandateID`, `issuerEntityRef`, `actingIdentityUUID`, reason and time in
private audit state. Public state and Flow receipts do not expose this identity
pair. See [revocation and audit evidence](../Deliverables/PDD_scaffold-admin-delegering_2026-09-08/TESTRESULT.md#revoke).

**Verified integration and remaining limits.** The green target-Cell test uses
`ArendalsukaConfigurationPublisher.resetEditableCellConfiguration` before and
after revocation. Source also connects `applyEditableCellConfiguration` to the
mandate check, but this evidence does not prove a completed publication through
that action. `publisherAccess.issue` is **not-implemented on this branch**;
fixture issuance for that key does not execute it. Other target-Cell integrations
are planned. Reading `administrator.history` with only an administrate mandate
is also **not-implemented**; the verified path requires owner proof or an
owner-authorized Agreement for that exact key. See
[Gap Analysis](../Gap_Analysis.md#scaffold-admin-delegering).

**Planned, not deployed:** WP10 staging provisioning, actual Digipomps/DiMy
entities and representative signing setup, and restoration of Vegar's publishing
access. No part of this PDD is running on staging yet. Organizational affiliation
has not been assessed by a lawyer. These tests establish the software form only.
