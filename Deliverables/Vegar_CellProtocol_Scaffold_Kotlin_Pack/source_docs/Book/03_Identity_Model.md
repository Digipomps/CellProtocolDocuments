
# Chapter 03 — Identity Model

Identity in HAVEN is domain scoped, cryptographically anchored and privacy preserving.
The core principles are:

- Entities (people, organisations, devices) are never exposed directly.
- Identities are operational handles tied to a specific domain.
- There is no global identifier and no automatic cross-domain linkage.
- Identity is always explicit and always cryptographic.

## 1. Entity vs Identity

**Entity**  
A conceptual real-world actor (person, organisation, device).  
Entities are *never transmitted* and are *never stored* in Cells.

**Identity**  
A digital, domain-scoped operational representation used in all protocol interactions.  
An Identity contains:

- UUIDv4
- Public key
- Domain string
- Optional metadata (non-sensitive)

An Entity may have many Identities across different domains.

## 2. Domain Scoping

Identity is always scoped to a single domain, such as:

- domain:personal:notes
- domain:team:projectX
- domain:community:aid
- domain:device:local

This prevents cross-context tracking and removes the idea of a global account.

Cells may restrict access to specific domains and treat others as foreign.

## 3. Identity Vault

Private keys never leave the vault.  
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

Cells and Resolvers only see public keys and signatures, never private keys.

## 4. Identity in Absorb and Meddle

Every Absorb and Meddle call includes:

- identity UUID  
- identity public key  
- signature for the call  
- domain  
- optional purpose  
- optional evidence

Resolver checks:

- signature validity  
- domain compatibility  
- contract existence  
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

The identity model ensures:

- no global identifier  
- domain isolation  
- minimal metadata  
- no automatic linking across domains  
- no behavioural inference  
- no scoring or reputation  

Identity exists to support correct capability checking, not to identify people.

## 7. Summary

Identity in HAVEN is:

- cryptographic  
- explicit  
- domain-scoped  
- privacy preserving  
- minimal and stable  

This model provides a safe foundation for capabilities, trust, and decentralised cooperation.
