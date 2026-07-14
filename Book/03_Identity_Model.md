
# Chapter 03 — Identity Model

Identity in HAVEN is designed to be domain scoped, cryptographically anchored,
and privacy preserving. Those properties depend on the selected vault, proof,
policy, and deployment path; a UUID or domain label alone grants no authority.
The core principles are:

- Protocol authorization uses operational Identities rather than treating a
  real-world Entity as authority.
- Identities are operational handles tied to a specific domain.
- There is no global identifier and no automatic cross-domain linkage.
- Protected interactions require explicit cryptographic identity control or
  another explicitly implemented policy proof.

The dated positive/negative evidence and remaining cross-runtime gaps are
tracked in the
[HAVEN cross-repository robustness audit](../Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md).

## 1. Entity vs Identity

**Entity**  
A conceptual real-world actor (person, organisation, device).  
The protocol does not use an Entity object as a bearer credential. Applications
may still store or transmit entity-related records, so their schemas and access
policies require an ordinary privacy review.

**Identity**  
A digital operational representation used in protected protocol interactions;
its domain/context binding comes from the vault and signed request evidence.
An Identity contains:

- UUIDv4
- Public signing key and optional key-agreement key
- Optional metadata (non-sensitive)

The runtime `Identity` object deliberately does not contain a mutable domain
string. The identity vault owns the canonical mapping between an identity and
the context in which it was created. An Entity may have many Identities across
different domains.

## 2. Domain Scoping

Vault-created identities should be scoped to one context/domain, such as:

- domain:personal:notes
- domain:team:projectX
- domain:community:aid
- domain:device:local

This reduces cross-context tracking when applications use distinct identities.
Reusing a UUID, signing key, or correlatable metadata across domains can still
create linkage; the type system cannot prevent that deployment choice.

Cells may restrict access to specific domains and treat others as foreign.

### 2.1 Canonical Runtime Domain Binding

`IdentityVaultProtocol.identityDomainBinding(for:)` exposes the vault's
canonical mapping as `IdentityDomainBinding` when the vault can prove that the
requested UUID and signing-key fingerprint match exactly one stored identity
context.

The binding has these fields:

- `schema`: `cellprotocol.identity.domain-binding.v1`
- `bindingKind`: `vault_context`
- `domain`: the canonical vault context
- `identityUUID`: the bound identity
- `signingKeyFingerprint`: the bound public signing key
- `grantsAuthority`: always `false`

The binding must be included inside the requester's canonical signed payload.
The recipient verifies the outer request signature and checks that the binding
matches the embedded identity UUID and signing-key fingerprint. A domain-policy
request fails closed when the binding is absent, ambiguous, malformed, or does
not match the signed identity.

This is signed context evidence, not a capability, organization-membership
credential, or third-party attestation. A remote recipient cannot infer more
trust from the domain string than the requester's identity and explicit proof
chain provide. Resolver grants, Agreements, Contracts, and capabilities remain
the only authorization path. A legacy vault may return `nil`; traffic to an
endpoint without domain policy remains backward compatible.

## 3. Identity Vault

Conforming production vaults must not expose private keys.
The vault is responsible for:

- creating new key pairs  
- signing messages  
- safe rotation of keys  
- revocation support  
- generating key material from cryptographically secure OS entropy sources  
  (`SecRandomCopyBytes` on Apple platforms, `/dev/urandom` on Linux)

Security requirement:

- non-cryptographic generators (for example `String.random` / `Int.random`) must
  never be used for keys, IVs, nonces, or seed material.

Cells and Resolvers should receive public identity material and signatures, not
private keys. Legacy or test storage that embeds key material is not evidence
of this production invariant and should be migrated or rejected.

## 4. Identity in Absorb and Meddle

Protected Absorb and Meddle requests carry a requester Identity and, where the
selected policy requires it, signed proof and contextual evidence such as:

- identity UUID  
- identity public key  
- signature/proof for the call
- optional vault-context domain binding when required by policy
- optional purpose  
- optional evidence

The supported resolver/Cell access path checks the subset required by policy:

- signature validity  
- domain-binding consistency and endpoint domain policy, when active
- owner proof, Contract/Grant, or an explicit cell-specific policy path
- capability permissions  
- required conditions  

If any of these fail, the call is rejected.

## 5. Verifiable Evidence

Contracts may require evidence such as:

- verifiable credentials  
- endorsements  
- multi-party approvals  
- domain-scoped statements  

Evidence can be issued by:

- institutions  
- organisations  
- peers  
- trusted individuals  
- communities  

Issuer does *not* need to be central or governmental.

## 6. Privacy Properties

The identity model supports:

- avoiding a required global identifier
- domain isolation when distinct identities and policies are used
- minimal metadata  
- no protocol-required automatic linking across domains
- avoiding behavioural inference, scoring, or reputation in the identity
  mechanism itself; applications can still violate these goals and must be
  audited separately

Identity exists to support correct capability checking, not to identify people.

## 7. Summary

Identity in HAVEN is intended to be:

- cryptographic  
- explicit  
- domain-scoped  
- privacy preserving  
- minimal and stable  

When the vault, proof, authorization, domain-separation, and metadata policies
are correctly implemented and tested, this model can provide a privacy-aware
foundation for capabilities and decentralized cooperation. The Identity type
alone does not prove those properties.
