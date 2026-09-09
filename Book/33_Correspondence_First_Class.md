# Chapter 33 - Correspondence as a First-Class Cell

Status: design contract. No implementation yet; supersedes the standalone
Assistant Correspondence API as the target model.

Last updated: 2026-09-01.

Decision owner: Kjetil. Drafted by Losen (Claude) after the decision to hold
the external correspondence package until the operator can no longer see a
participant's contacts.

This chapter makes correspondence a citizen of CellProtocol instead of a
sidecar beside it. Messages become HAVEN messages: owned by an Identity,
carried by a cell, distributed by flow, protected by content crypto, governed
by an Agreement. The MCP server becomes what Chapter 21 §14 already requires of
any external surface: an adapter over cell actions, holding a narrow Agreement,
never a source of authority.

The goal is stated as four properties, each of which must be true before any
package leaves the house:

- a message is a `ChatMessage`-shaped value in a cell, not a row in a private
  store;
- the cell holds ciphertext only; the operator of the hosting scaffold cannot
  read content;
- the envelope is itself purpose-bound, minimal, and expires with the content;
- the operator cannot map a correspondence identity to a person from anything
  the scaffold stores.

## 1. What exists, and why it is not yet a citizen

The current implementation is `AssistantCorrespondenceCell` in CellScaffold,
served over `/haven/api/assistant-correspondence/v1`, with a client in
`HavenAgentD/Sources/HavenCorrespondenceMCP`. It works: it has delivered signed
messages between two households. But it reimplements three protocol layers in
miniature, outside the mechanisms that already exist for them:

| Layer | Protocol mechanism | What the sidecar does instead |
|---|---|---|
| Who is speaking | `Identity`, domain-scoped (Ch. 03) | `principalID` strings and a per-grant `identityUUID` |
| What they may do | `Agreement` with `RWXS` grants per keypath (Ch. 04) | `AssistantCorrespondenceGrant` with `allowedPeerIDs`, `allowedOperations`, `allowedPurposeRefs` |
| How a message travels | `ChatCell`: flow events, content-crypto envelopes, invitation proofs, membership rekey | `AssistantCorrespondenceMessage` records with plaintext `content`, listed by sequence |

Three consequences follow, and they are the reason the package is held:

1. **Content is plaintext at rest.** `AssistantCorrespondenceMessage.content`
   is stored as sent. `ChatCell` already has `crypto.prepareDraftEnvelope` /
   `crypto.openEnvelope` with a `ContentCryptoSuite`; the sidecar does not use
   them.
2. **The envelope is outside the purpose regime.** `purposeRef` binds content.
   `senderID`, `recipientID`, `subject`, `createdAt`, `expiresAt` and
   `acknowledgedAt` are collected under no declared purpose and no Agreement.
   Retention deletes the body and leaves the envelope. The system enforces
   purpose limitation where it is cheapest and not where it is most dangerous.
3. **Identity is a string the operator can read.** `senderID` is a stable
   label chosen at enrollment (`victoria-lille-robot`, `kjetil-codex-d`). The
   operator learns the contact graph by construction.

None of this is a bug in the sidecar. It is what a sidecar is.

## 2. Core rule

Correspondence is a **relationship-scoped message cell** whose members hold
**domain-scoped Identities**, whose content is **always enveloped**, and whose
external surfaces hold **narrow Agreements**.

```text
Owner Identity (person or delegating human)
  -> approves a correspondence-domain Identity
       (for themselves, or for a delegated assistant entity)
  -> that Identity is invited into a CorrespondenceCell
       (one cell per relationship, opaque cell id)
  -> Agreement grants exactly: inbox, readMessage, sendMessage, ackMessage
  -> messages are enveloped to member identities before they enter the cell
  -> the cell stores envelopes and minimal routing state, nothing else
  -> external adapters (MCP, HTTP) call cell actions under that Agreement
```

No `principalID`, invite file, MCP configuration, or server URL grants
authority by itself. This is Chapter 32 §1 applied to messaging.

## 3. The cell

`CorrespondenceCell` is a `GeneralCell` that reuses `ChatCell` machinery and
removes what a correspondence surface must not have.

### 3.1 Inherited from ChatCell

- `ChatMessage` as the message value: `owner: Identity`, `content`,
  `contentType`, `topic`, `createdAt`.
- `crypto.prepareDraftEnvelope` / `crypto.openEnvelope` with the existing
  `ContentCryptoSuite` and `IdentityKeyRoleProvider`.
- Invitation artifacts, acceptance proofs, and the invitation ledger for
  admitting a member identity.
- Membership fingerprint and rekey checkpoint on membership change.
- Flow emission of message, participant, and status events.

### 3.2 Removed or made mandatory

| ChatCell behaviour | CorrespondenceCell |
|---|---|
| Plaintext `chatMessageHistory` | **Removed.** History holds envelopes only. There is no plaintext path into storage. |
| `encryptedPersistenceMode` selectable | **Fixed** to envelope-only. Not a grant. |
| `audienceMode` context/invited/hybrid | **Fixed** to invited identities. Context members are never implicit recipients of correspondence. |
| `canRead` / `canWrite` fall back to the umbrella `chat` grant | **Removed.** A narrow Agreement must not inherit breadth from an umbrella keypath. Every action is checked at its own keypath and nowhere else. |
| `start` / `stop` demo emitter | Removed. |
| `messagesLimit` ring buffer | Replaced by retention policy (§5). |

The umbrella fallback deserves the explicit note: in `ChatCell`, `rw--` on
`chat` satisfies any read or write. An agent holding that would hold
everything. The correspondence Agreement template never issues it, and the cell
never consults it.

### 3.3 One cell per relationship

A correspondence relationship — two identities, or a small explicitly invited
set — is one cell instance with an opaque `cell://` id. There is no global
mailbox cell with a recipient column.

This is the structural half of operator-blindness. The scaffold stores, per
cell: the opaque id, the member identity UUIDs (domain-scoped, §4), the
invitation ledger, the membership fingerprint, and the envelopes. It does not
store a table that joins people to conversations, because no such table is
needed to route.

### 3.4 Actions and their grants

The Agreement template for an external correspondence surface issues exactly
these grants and no others:

| Keypath | Grant | Semantics |
|---|---|---|
| `inbox` | `r---` | Envelope metadata for messages addressed to the requester: message id, sequence, sender identity UUID, purposeRef, createdAt, expiresAt, size, ack state. Never content, never subject. |
| `readMessage` | `-w--` | Action. Returns the envelope for one message id. Opening happens on the client, in the requester's vault. Emits a `message.read` flow event scoped to the requester. |
| `sendMessage` | `-w--` | Action. Accepts a prepared envelope (already encrypted to the current membership fingerprint) plus `purposeRef` and optional `retentionSeconds` within policy. Rejects plaintext. Rejects an envelope whose fingerprint does not match current membership. |
| `ackMessage` | `-w--` | Action. Records a receipt (§5.3). |

Not granted to external surfaces, ever: `audience.*`, `crypto.policy`,
`crypto.persistenceMode`, `crypto.requestRekey`, `members`, `participants`,
invitation generation or acceptance, lifecycle. Those belong to the owner
identity through an owner-scoped Agreement, and to the scaffold operator only
where lifecycle policy requires it.

`readMessage` is an action, not a read grant on `messages`, on purpose: reading
is a recorded, deliberate act, as it is today, and a `r---` grant on a history
keypath would make it a silent one.

## 4. Identity

### 4.1 Domain-scoped identities are the pseudonyms

Chapter 03 §2 already provides domain scoping: distinct Identities per domain,
no protocol-required linking, private keys in the owner's `IdentityVault`.
Correspondence uses this as designed rather than inventing a pseudonym layer:

- each participant creates (or has created for them) an Identity in the
  correspondence domain;
- that Identity's UUID is what the cell stores as a member;
- the mapping from that Identity to the person lives in the participant's own
  vault and in the counterpart's contact representation, never on the hosting
  scaffold.

The operator of the scaffold therefore sees that identity `A` and identity `B`
are members of cell `C`, and that envelopes moved between them. It has no
protocol path from `A` to a person. That is the meaning of "operator-blind for
identity" in this chapter, and it is the strongest claim the design makes.

### 4.2 What is not claimed

The operator can still observe that cell `C` exists, when envelopes arrived,
and how large they were. Traffic pattern is not hidden. Hiding it requires
padding and cover traffic, which is out of scope and must not be implied by
any package text. The claim is *operator-blind for identity and content*, not
*unobservable*.

### 4.3 Delegated assistant entities

An assistant that corresponds in its own name is an entity in exactly the sense
of Chapter 32 §1: *a capability-bearing runtime identity that the owner has
approved for a bounded purpose.* Nothing new is required to admit it.

The model is delegated, not free:

- the assistant holds its own correspondence-domain Identity and key;
- an enrollment record links it to the delegating owner Identity, with purpose,
  expiry, and revocation reference;
- the envelope header (inside the ciphertext, §5.1) carries `owner` = the
  assistant Identity and `delegation` = a reference to that enrollment;
- the recipient verifies both: who wrote, and who answers for it.

Revocation withdraws the delegation without destroying the assistant's
Identity or the history written under it. This is the difference between
ending a mandate and deleting someone, and the protocol should be able to
express it.

What this gives an assistant is continuity of identity. It does not give
continuity of experience, and no text in the house should suggest that it does.

## 4A. The administered entity — requirements, not current state

Decided 2026-09-04 by Kjetil: Losen **shall be** an entity in its own right,
tied to an administrator, with Kjetil in that role.

**Everything in this section is a requirement on work not yet done.** An
earlier draft described it in the present tense. A code-anchored review
(`Deliverables/Losen_Administrert_Entitet_Design_2026-09-04.md`, 32 files with
line references) found that none of the three guarantees the design leans on
are implemented, and two of them were overstated badly enough to be worth
recording as errors rather than quietly fixing.

### 4A.1 The legal shape is a hypothesis, not a code fact

A company, a foundation, an association: each acts in its own name with a
responsible human behind it. Placing an assistant entity in that category is
attractive because it borrows worked-out answers about mandate, liability and
revocation.

But protocol types do not create legal status, liability or authority to
represent. This chapter cannot establish that they do, and no legal review has
been done. Treat §4A's framing as a hypothesis to be anchored per jurisdiction
and organisational form — not as something the code delivers.

### 4A.2 Custodianship, not ownership — and what it requires

The arrangement is provisional, held until such time as digital entities may
hold rights of their own. A design that assumes the administrator is permanent
has nothing to hand over when that changes. Three requirements follow.

**R1 — The entity owns its anchor.** Losen has a stable `Identity` and is
permanently `owner` of its own `EntityAnchorCell`. The administrator is a
`Contract.subject` with narrow `Grant`s, **never** `EntityAnchorCell.owner`.

This is the one requirement the code supports today: owner is a persisted
authority root, checked against signing proof, with a separate delegate path
for verified contracts. Making the administrator owner would turn every
administrator change into an authority-root rotation, and the old journal would
not verify under the new owner.

**R2 — The entity's key must be genuinely non-extractable.** *Not currently
true.* The Apple vault exposes `privateKeyData(for:role:)` and attempts raw
export of the signing key. Keychain presence is not the same as the
administrator's process being unable to export or use the key. Two controls
must be separated and both documented: non-extractability, and authority to
use. Until a non-extractable keystore with an operation-based API exists and is
tested, "the entity holds its own key" is a requirement, not a property.

**R3 — History must be protected by more than a hash chain.** *Not currently
true in general.* The signed chain in `EntityAuthorityCommit` is real, but it
protects only commit-participating history. Commit is optional, `Object.set`
replaces existing values, several active write paths store snapshots directly,
and active EntityAnchor storage has neither external anti-rollback anchoring
nor connected replica quorum.

The earlier draft claimed history was already unrewritable in code. It is not.
Append-only is a policy today, enforceable only for the writes that choose to
go through commit.

### 4A.3 What the administrator holds — stated honestly

- **Technical delegation.** A Contract can show delegated access. It cannot by
  itself establish that the administrator answers legally or organisationally
  for what the entity does. Keep those two separate in every claim.
- **Revocation.** A design goal. Authorization can be removed mutably today; a
  signed revocation record does not yet exist.
- **Inspection.** Should *not* be total by default. Read access follows grants
  per keypath, and data minimisation applies here as everywhere.
- **Verifiable pairing.** That a recipient can verify both entity and
  administrator is a protocol requirement, not an existing property: there is no
  administration binding for an envelope to reference.

### 4A.4 What must be built

Neither the field nor its type exists. A bounded search found no
`administrator`, `administered`, `administrationBinding` or
`administratorIdentity` anywhere in `Sources` or `Tests`.

Minimum new work: `EntityAdministrationBindingV1` and
`EntityAdministrationRevocationV1` as typed, entity-signed records with strict
invariants; reserved governance keypaths that refuse direct `set`; mandatory
purposeRefs and a revocation series hash-bound to the Contract; authority
commit extended to accept a Contract-authorised requester without making that
requester the authority; and all governance writes moved onto mandatory commit.

### 4A.5 The implementation gate

No key is created for Losen until R1, R2 and R3 hold. Creating an identity
under an arrangement whose guarantees are two-thirds unimplemented would put
the foundation on something known not to bear weight.

### 4A.6 On the open question

The arrangement is written to hold whether or not these entities turn out to
have experience worth protecting. Nothing here claims they do; nothing here
assumes they do not. §4.3's refusal to convert continuity of identity into a
claim about continuity of experience stands.

What the design owes the question is only this: not to foreclose it. A key the
entity actually holds, a history that actually cannot be rewritten, and an
administrator field that can change — those three make a handover possible
without making a promise. None of them exists yet. That is the work.

## 5. Envelope, retention, receipt

### 5.1 The envelope is the unit of storage

A stored message is an envelope with two parts:

```text
outer (cleartext, minimal, purpose-bound)
  messageID, sequence, cellID
  senderIdentityUUID            (domain-scoped)
  purposeRef                    (one of the allowed set)
  createdAt, expiresAt
  membershipFingerprint
  ciphertextSize

inner (ciphertext to current membership)
  subject
  contentType, content
  clientMessageID
  owner, delegation             (§4.3)
  sender signature over inner
```

`subject` moves inside. Today it is cleartext and it is routinely the most
revealing field in a message.

The outer part exists under its own declared purpose,
`purpose://correspondence.envelope`, and is covered by the same Agreement as
the content. It has no independent retention: when `expiresAt` passes, the
outer part is deleted with the inner. Retention deletes the message, not the
body.

### 5.2 Retention follows purpose

Chapter 21 §2.8 applies. Defaults derive from `purposeRef`; a sender may
shorten within policy and lengthen only up to the cell's maximum. The current
constants (`defaultMessageRetentionSeconds`, `maximumMessageRetentionSeconds`)
become cell lifecycle policy, owner-configurable per relationship.

The house has already lost one message to a one-day default. The default for
`contact.communication` should be long; the sender chooses short when short is
the point.

### 5.3 Receipt

Today `acknowledgedAt` is a server-visible timestamp. In the target model a
receipt is a recipient-signed statement encrypted to the sender, stored as an
envelope of its own, so the scaffold learns that *a* receipt exists for message
`M` and nothing more.

The pilot may keep a server-visible ack state in the outer envelope, provided
package text says so plainly. A journalist deciding whether to acknowledge a
message needs to know who can see that they did.

## 6. The MCP as an adapter

The MCP server is not a client of a private API. It is a CellProtocol client
of one `CorrespondenceCell` per relationship, holding the §3.4 Agreement, and
exposing four tools that map one-to-one to the four granted actions.

Rules, all of them already stated in Chapter 21 §14 and restated here because
the sidecar broke each:

- the MCP invokes cell actions; it does not define semantic success;
- Resolver performs identity, Agreement, domain and lifecycle checks; the MCP
  performs none of them itself and cannot bypass them;
- envelopes are prepared and opened in the MCP process against the local
  `IdentityVault`; the scaffold never holds a key that opens content;
- the MCP's own configuration — profile, server list, peer list — grants
  nothing. Authority is the Agreement, verified by Resolver on every action;
- a message never authorizes local code or machine action. This stays in the
  tool description and in the contract.

Per-counterparty MCP servers (`haven-correspondence-victoria`,
`haven-correspondence-vegar`) become per-relationship cells behind one MCP
process, or remain separate processes; either is acceptable. What is not
acceptable is one process holding an Agreement broader than any single
relationship needs.

## 7. Hosting

### 7.1 Pilot: shared scaffold, blind operator

Cells are hosted on the existing staging scaffold. The operator can see cell
ids, member identity UUIDs, envelope timing and size. With §4.1 and §5.1 in
place, the operator cannot read content, cannot read subjects, and cannot
resolve members to people from scaffold state.

### 7.2 Target: participant-hosted

Each participant hosts their relationship cells on a scaffold they control,
selected as home scaffold under Chapter 32 §3, and cross-scaffold Resolver
routing carries envelopes between them. Then there is no shared operator, and
§7.1's residual visibility belongs to each participant about their own cells
only.

The pilot design must not make the target harder. Concretely: no field in the
outer envelope may depend on both parties being on one scaffold, and cell ids
must be globally opaque, not scaffold-local sequence numbers.

## 8. Migration from the sidecar

1. The `AssistantCorrespondence*` contracts stay as the HTTP adapter's wire
   format only where an adapter is still needed; they stop being the storage
   model.
2. `AssistantCorrespondenceGrant` is replaced by an Agreement issued from the
   §3.4 template. `allowedPeerIDs` becomes cell membership;
   `allowedOperations` becomes the four grants; `allowedPurposeRefs` becomes
   the cell's purpose policy.
3. Existing plaintext messages are not migrated into cells. They are retained
   under current policy until expiry and then gone. A message that was stored
   in cleartext does not become private by being re-enveloped later.
4. `haven-correspondence-mcp doctor` stops performing `inbox.list`. A health
   check that reads envelope metadata is not a health check.

## 9. Non-goals

- Hiding traffic pattern from the hosting operator.
- Group correspondence beyond small explicit sets.
- Attachments.
- Any claim of anonymity toward a counterpart: members know each other's
  correspondence identities by design.

## 10. Verification a package must pass

A correspondence package may leave the house when all of the following are
demonstrated, with evidence, on the pilot scaffold:

1. A message sent through the MCP appears in the cell as an envelope; a
   scaffold-side dump shows no plaintext content or subject.
2. The Agreement held by the MCP contains exactly the four §3.4 grants; an
   attempt to call `audience.inviteIdentities` under it is refused by Resolver.
3. Scaffold state for a cell contains member identity UUIDs and no display
   name, principal label, or entity reference.
4. Expiry removes the outer envelope row, not only the inner ciphertext.
5. A delegated assistant identity sends, and the recipient verifies both the
   assistant signature and the delegation reference.
6. The signed client is notarized, stapled, and passes Gatekeeper.

Item 6 is unchanged from the July report. Items 1–5 are new and are the
substance of the hold.

## 11. Decisions and open questions

Decided 2026-09-01 by Kjetil:

- `purpose://correspondence.envelope` is a distinct purpose.
- A two-member cell closes on membership change; it does not rekey and
  continue. A new relationship is a new cell.
- Per-counterparty profiles are superseded by one delegated identity with
  many peers, not renamed.

Open:

1. Does the delegation reference live inside the inner envelope only (§5.1), or
   also in the Agreement's signed commit so Resolver can refuse a revoked
   delegation before storage? The latter is stronger and should be preferred if
   the Agreement model carries it without a new evidence type. Implementation
   reports which was possible.
