# Fabel end-to-end encryption assessment

**Date:** 2026-07-21

**Authoritative task:** `019f84b5-2cfe-70a0-9154-c753f1611165`

**Assessment status:** **Codex/static portion review-ready; required Fabel
portion externally blocked**

**Implementation status:** analysis only; no E2EE implementation exists as a
result of this work

**Production decision:** **NO-GO for claiming current chat E2EE, forward
secrecy, or absolute irreversibility**

## 1. Executive decision

The proposition **“once E2EE is enabled it cannot be disabled” is rejected as
an absolute statement**. It is neither a complete security property nor a
credible guarantee against authorized endpoints: an endpoint that can decrypt
can export, copy, re-encrypt or disclose plaintext. Backups and recovery keys
can deliberately preserve future decryption. Existing plaintext does not
become encrypted merely because future writes change policy.

A narrower policy can be made meaningful and testable:

> Once a protected content epoch is committed for a declared Cell/entity and
> device participant set, every new protected write in that epoch must remain
> message-level E2EE; no server, old client, rollback or ordinary configuration
> change may accept a plaintext or weaker-suite write. A different protection
> policy requires a new, visibly distinct epoch or entity plus an explicit
> migration decision. Historical plaintext and exports remain separately
> classified.

This is **scoped monotonic protection**, not absolute impossibility of disabling
encryption. It is the strongest defensible interpretation of the hypothesis.

The current repository does not satisfy even that narrower claim:

1. `ChatCell` explicitly reports `encryptionEnabled=false` and
   `bootstrapOnly=true`; its normal send flow remains unencrypted.
2. Ordinary messages are appended to and encoded from plaintext
   `chatMessageHistory`. The optional encrypted record is a companion archive,
   not the source of truth.
3. `crypto.requestRekey` advances an envelope-generation checkpoint and
   invalidates prepared drafts; it does not rotate or erase cryptographic keys.
4. `haven.chat.message.v1` declares `supportsForwardSecrecy=true`, but it wraps
   each content key to a long-lived recipient X25519 key and stores the sender's
   ephemeral public key. Later compromise of that recipient private key can
   reconstruct the wrapping key and decrypt recorded historical envelopes.
   RFC 9180 explicitly excludes recipient-compromise forward secrecy for this
   construction.
5. persisted-Cell encryption is host-held encryption at rest with transparent
   legacy plaintext decode. TLS/WSS is transport/session encryption. Neither is
   E2EE against the host or delivery service.

The immediate safe action is documentation and claim correction, followed by a
separate product decision and protocol design. Do not patch the existing
envelope incrementally and call it E2EE.

## 2. Evidence and snapshot boundary

### 2.1 Repositories inspected

| Repository | Snapshot | State | Use in this assessment |
| --- | --- | --- | --- |
| `CellProtocolDocuments` | detached HEAD `52539f7c0769d5783345d4be73c08617cb6b6630` | clean before this report | canonical documentation contracts and this deliverable |
| `CellProtocol` | local HEAD `61ffc8990afd34a601231e332e423b905e04535f` | read-only; unrelated dirty `Package.swift` and `haven-browser-recovery-cp/`; eight commits behind observed `origin/main` `7974030` | current crypto, chat, storage, backup and identity code |

The eight observed upstream commits concern DeviceIngress/persistence-vault
work; static inspection did not identify a newer E2EE chat design. This is not
a claim about uninspected private or future code.

### 2.2 Evidence grades

| Evidence | Grade | Result |
| --- | --- | --- |
| Repository contracts and source at the pinned snapshots | inspected | sufficient to reject current E2EE and FS claims |
| Official primary standards/specifications | inspected | supports the layer, lifecycle, FS/PCS and metadata analysis below |
| Fabel/Claude assessment | **missing** | externally blocked; no Fabel opinion is attributed anywhere in this report |
| Executable tests/builds | **not run** | blocked by the authoritative hard-disk coordination gate |
| Independent cryptographic review | not performed | mandatory future exit gate |

Static source evidence is enough to reject an overclaim. It is not enough to
certify a secure implementation.

### 2.3 Defensive cybersecurity purpose and boundary

This assessment is defensive work on Kjetil/Digipomps-owned HAVEN and
CellProtocol frameworks, intended to expose cryptographic and authorization
contradictions and define evidence needed for production readiness. That
purpose supports rigorous negative-gate analysis on authorized isolated targets;
it does not authorize access to third-party systems, live user data, secrets,
identity/APNS/recovery operations, staging/production, deployment or cleanup.
Any future passing gate would be evidence only for its exact contained scope,
not proof that the framework is universally secure.

## 3. Purpose, goals and claim analysis

### 3.1 Purposes

- `purpose://access.audit.privacy`: make the confidentiality boundary and
  unavoidable leakage auditable.
- `purpose://human-agency`: preserve explicit owner choices for participants,
  devices, export, backup and recovery without representing recoverability as
  server-blind E2EE when it is not.
- `purpose://test.acceptance`: replace ambiguous adjectives with falsifiable
  security and operational gates.

### 3.2 Measurable goals

| Goal | Baseline | Target/evidence | Status |
| --- | --- | --- | --- |
| G1: determine present confidentiality boundary | encryption features use overlapping terminology | layer-by-layer code inventory with pinned snapshots | satisfied for static review |
| G2: adjudicate irreversibility claim | absolute, unscoped hypothesis | scoped proposition with counterexamples and product choices | satisfied for decision review |
| G3: assess FS/PCS and lifecycle | suite boolean and advisory generation counter | primary-standard definitions plus compromise/deletion gates | present design contradicted |
| G4: obtain independent Fabel view | no readable result | preserve readable Fabel response and audit agreements/disagreements | **externally blocked** |
| G5: certify behavior | no end-to-end test evidence | future deterministic negative/positive tests and operational drills | blocked/not started |

### 3.3 Root claim ledger

| ID | Type | Claim | Strength | Adjudication |
| --- | --- | --- | --- | --- |
| C1 | product hypothesis | Once E2EE is enabled it cannot be disabled. | absolute | **contradicted** unless narrowed by scope, epoch, write class and adversary |
| C2 | counterclaim | Protection can be monotonic for new writes in a committed Cell/entity epoch. | conditional | **supported as a design option**, not implemented |
| C3 | present-state claim | HAVEN Chat currently provides E2EE. | universal/current | **contradicted** by `ChatCell` |
| C4 | cryptographic claim | `haven.chat.message.v1` provides forward secrecy. | universal | **contradicted** for recipient-key compromise by construction and RFC 9180 |
| C5 | storage claim | Persisted-Cell encryption or WSS/TLS establishes E2EE. | equivalence | **contradicted**; these protect different boundaries |
| C6 | recovery claim | Key erasure can make all historical content unrecoverable. | absolute | **open and generally unprovable** without verified deletion of every key/plaintext copy, including backups and offline devices |

No composition of C1, C3, C4 or C5 may support public or production copy.

## 4. Threat model

### 4.1 Assets

- message bodies, attachments, drafts and structured Cell state;
- content keys, epoch secrets, identity/key-agreement keys and skipped-message
  keys;
- participant and device membership, group/entity IDs, timestamps, traffic
  patterns and ciphertext lengths;
- plaintext caches, previews, indexes, logs, Flow payloads, exports and AI
  prompts/results;
- backup manifests, encrypted fragments, recovery keys and restore state;
- authorization policy, membership commits, downgrade state and audit evidence.

### 4.2 Trust boundaries

| Boundary | Required assumption for E2EE |
| --- | --- |
| End-user device/client | trusted while processing plaintext; hardened local storage and key deletion still required |
| Cell/Resolver host | **not an endpoint** if the claim is E2EE against HAVEN servers; must receive only ciphertext and declared metadata |
| Delivery/bridge/transport service | untrusted for content; may delay, drop, duplicate and observe metadata |
| Persistent server storage | untrusted for content; host-held at-rest keys do not change this classification |
| Identity/key directory | may be malicious or stale; authenticated device-key changes and consistency evidence required |
| Backup/export target | separate trust and retention policy; recovery authority is decryption authority |
| Search/AI provider | untrusted unless explicitly made an endpoint for a narrow disclosed purpose |

The current `crypto.openEnvelope` Cell action can return plaintext through the
trusted host. If that action runs on a server, the server is a decryption
endpoint and the product is not E2EE against that server. Placement is a
security property, not a deployment detail.

### 4.3 Adversaries in scope

- passive network observer despite TLS metadata protection limits;
- compromised or malicious delivery service/server/storage operator;
- malicious member or a member/device removed from the protected participant
  set;
- attacker who later obtains a long-lived recipient or recovery private key;
- attacker who temporarily compromises session/epoch state and then loses
  access;
- stolen, restored, rolled-back or long-offline device;
- malicious/stale server device list or key-directory response;
- old or modified client attempting suite/policy downgrade or plaintext writes;
- forensic recovery of keys/plaintext from caches, logs, crash reports or
  backups;
- metadata observer correlating identities, membership, timing, size and
  activity.

### 4.4 Explicit non-guarantees

E2EE cannot by itself prevent an authorized recipient from copying plaintext,
protect an actively compromised endpoint that reads current plaintext, ensure
availability against a blocking server, hide all traffic metadata, or make an
exported plaintext copy disappear. Those require separate controls and honest
product language.

## 5. Encryption layers are not interchangeable

| Layer/surface | What the repository does | Who can decrypt/observe | E2EE conclusion |
| --- | --- | --- | --- |
| TLS/WSS bridge transport | production guidance requires a secure channel and preserves application payloads | both TLS endpoints; traffic observer still sees timing/size and connection metadata | session/transport protection only |
| Persisted-Cell encryption | `CELLENC1` ChaChaPoly envelope; per-Cell key derived from process/config master key plus owner/Cell IDs; non-envelope data decodes as legacy plaintext | process/host holding the master key | server/host encryption at rest, not E2EE |
| `ContentCryptoEnvelopeUtility` | fresh content key; ChaChaPoly payload; one ephemeral X25519 wrap per identity recipient; sender signature | any host with recipient long-term private key; current action can return plaintext | useful envelope primitive, not a complete session/group E2EE protocol |
| `ChatCell` normal send | appends plaintext `ChatMessage` to Codable history, exposes it through state/messages and Flow/event paths | trusted Cell host and authorized requesters | explicitly not E2EE |
| encrypted chat companion | optional draft/sent envelope record in addition to plaintext history | same host plus envelope recipients | cannot repair plaintext primary path |
| user-owned backup | signed envelope to owner/recovery identities; opaque recipient IDs but identifying manifest fields remain | holders of long-lived recovery keys | encrypted recoverable backup; explicitly no FS |
| FileCrypto | direct symmetric ChaChaPoly-style file envelope and credential contract | raw credential holder and whichever runtime handles it | generic file encryption, not identity/session E2EE |

TLS 1.3 can provide forward secrecy for a connection when the right handshake
mode is used, but it does not provide post-compromise security after a traffic
secret is exposed; a fresh handshake is required. That still does not stop a
TLS server endpoint from seeing application plaintext. Message-level E2EE has
to be independent of the delivery transport.

## 6. Current repository findings

### 6.1 Chat plaintext is authoritative

In `Sources/CellBase/Cells/Chat/ChatCell.swift`:

- `ChatEncryptedPersistenceMode` defaults to `draftCacheOnly`; its own summary
  says sent history is stored as normal plaintext.
- `sendMessage` and `sendComposedMessage` create a `ChatMessage` and call
  `storeMessage`, which appends it to `chatMessageHistory`.
- `chatMessageHistory` is encoded with the Cell and returned in `messages` and
  `state`; message content/previews also enter status/event surfaces.
- `draftAndSentArchive` calls the ciphertext an encrypted **companion**.
- clearing encrypted messages only empties the companion dictionary, not
  plaintext history or external copies.
- crypto state says normal send is still unencrypted and returns
  `encryptionEnabled=false`, `bootstrapOnly=true`.

Result: the content-crypto path is a bootstrap/preview facility. It must not be
represented as a production E2EE send path.

### 6.2 “Rekey” is an advisory checkpoint

`crypto.requestRekey` compares a membership fingerprint, increments
`currentEnvelopeGeneration` if it changed, records a checkpoint and invalidates
prepared drafts. It does not generate a fresh participant/device group secret,
rotate identity key-agreement keys, update recipients through a committed
protocol transition, or erase obsolete secret material.

Result: it is useful policy bookkeeping, but it is not cryptographic rotation,
revocation, removal or PCS healing.

### 6.3 The forward-secrecy flag is wrong for recipient compromise

For each recipient the envelope code:

1. obtains the recipient's long-lived X25519 public key;
2. creates a fresh sender ephemeral X25519 private key;
3. derives a wrapping key from the ephemeral/private-to-recipient/public shared
   secret;
4. stores the ephemeral public key beside the wrapped content key;
5. opens later with the recipient's long-lived private key and the recorded
   ephemeral public key.

Therefore an attacker who records an envelope and later obtains the recipient's
long-lived private key can recompute the same shared secret and unwrap the old
content key. The limited sender-side property is forward secrecy against later
compromise of sender **long-term** state only if the actual ephemeral private
value has been erased. Later recovery of that ephemeral private value, combined
with the recipient public key, also reconstructs the wrap secret; ephemeral
randomness does not protect against compromise of itself. RFC 9180 §9.7.4
documents the matching HPKE security limit. The direct X25519 derivation in the
HAVEN source establishes the repository conclusion; this is not a claim that
the custom envelope conforms to HPKE.

The `supportsForwardSecrecy=true` suite field and its positive test are unsafe
until renamed to a precise one-sided property or replaced by a protocol that
actually meets the declared FS threat model.

### 6.4 At-rest encryption accepts historical plaintext

`CellPersistenceCrypto.decodeFromStorage` returns bytes unchanged when the
`CELLENC1` magic is absent. `encodeForStorage` returns plaintext when the write
option does not require encryption. Apple and Vapor filesystem backends honor
the options, while the base storage protocol's default options overload simply
delegates to the legacy store method unless a backend overrides it.

Result: encrypted-at-rest policy requires backend conformance and explicit
migration/inventory. It cannot establish that all existing records are
encrypted, and it remains host-decryptable in any case.

### 6.5 Authorization is necessary but distinct

HAVEN identity is domain-scoped, and Resolver Contract/Grant/owner proof is the
authorization boundary; a UUID or domain label is not authority. RWXS `S`
expresses retention/store authorization. It does not cryptographically prevent
copying, forwarding or later plaintext disclosure.

E2EE must compose with Resolver authorization, not replace it and not be
inferred from it. A removed capability can stop future authorized resolution,
but it cannot revoke ciphertext already decryptable with a retained key.

### 6.6 Documentation drift exists

`Book/08_Bridging_Transport.md` makes broad statements about immutable,
ordered, cryptographically verifiable envelopes and transport-independent
identical behavior. `Book/06_CellResolver.md` under “Flow Supervision” and
`Book/05_Flows_Lifecycle.md` under “What the current contract does not prove”
more carefully state that generic FlowElement does not universally guarantee
signatures, timestamps, global sequence, durable history or replay. Those
narrower evidence contracts should control until the transport chapter is
corrected.

## 7. Required scope model

“Encryption enabled” is not a sufficient state variable. Every policy and
ciphertext must bind at least this tuple:

```text
ProtectionScope = {
  entityOrCellID,
  contentClass,
  protectionEpoch,
  participantDeviceSetHash,
  identityDomain,
  authorizationContextHash,
  policyCommitRef,
  protocolVersion,
  cipherSuite,
  writeVersion
}
```

The participant unit must be a **device/client key**, not merely an Identity
UUID. An identity with three devices implies three independently removable
cryptographic clients (or another explicit, equally strong device-key model).

`authorizationContextHash` must authenticate the selected authorization path
and its exact resource/action scope: verified owner proof, an exact signed
Contract/Grant/capability, or a deliberately narrow named cell-specific policy.
It must bind the requester identity UUID and signing-key fingerprint, domain,
keypath/action and RWXS permission plus applicable purpose, conditions,
validity/revocation reference. `policyCommitRef` must bind the canonical
protection/membership policy version or commit that authorized the epoch. A
signed domain binding supplies context but grants no authority; consent, an
identity label or possession of a decryption key is also insufficient by
itself.

### 7.1 Existing versus new writes

| Data class | Enabling protected epoch must do | Disabling/migration semantics |
| --- | --- | --- |
| New protected writes | encrypt on an authorized endpoint before host/delivery boundary; reject plaintext or wrong epoch/suite | cannot silently weaken within the same epoch |
| Existing plaintext | inventory and visibly label; explicitly migrate/re-encrypt or leave as historical plaintext | policy change must not imply retroactive protection |
| Existing ciphertext | preserve original scope/epoch and keys according to retention policy | moving plaintext to a weaker scope is a new explicit export/migration |
| Local caches/indexes | classify and encrypt/delete under endpoint policy | no hidden plaintext shadow after epoch activation |
| Backups | independently declare recipients, lifetime, exact authority path and restore behavior | recovery authority and loss risks remain visible |
| Exports | require exact owner/Contract/cell-specific authority, explicit user action, provenance and destination warning | exported plaintext is outside the old cryptographic guarantee |

### 7.2 Monotonic policy state

A defensible state machine is:

```text
unclassified -> planned -> protected(epoch N) -> archived/destroyed
                         \-> export/migration(new explicit scope)
```

There is no `protected(epoch N) -> plaintext(epoch N)` transition. Starting a
new plaintext entity/epoch may be a product choice, but must not rewrite the
historical claim or be accepted as an in-place downgrade.

## 8. Security invariants

These invariants are mandatory if HAVEN chooses scoped E2EE.

1. **Endpoint invariant:** protected content is encrypted before it crosses the
   declared client endpoint boundary; a HAVEN delivery/resolver server never
   receives its plaintext or content-decryption key.
2. **Scope invariant:** authenticated associated data binds the complete
   ProtectionScope, including entity/Cell, content class, epoch, device set,
   identity domain, authorization-context hash, policy/commit reference,
   version and suite.
3. **Monotonic-write invariant:** after epoch commitment, plaintext,
   legacy-suite and wrong-epoch writes fail closed on every current and stale
   client/server path.
4. **Device membership invariant:** every sending client encrypts for the
   authenticated current device set, including the sender's other approved
   devices; identity membership alone is insufficient.
5. **Committed-removal invariant:** a removal/rotation becomes effective only
   through one canonical ordered commit. No new application message is sent
   under the old secrets after that commit.
6. **Forward-secrecy invariant:** compromise at time T of a current recipient
   long-term/session private state cannot decrypt messages whose deletion
   schedule completed before T. A boolean declaration is not evidence.
7. **PCS invariant:** after compromise and a completed honest fresh-key update,
   an attacker lacking the new secret cannot decrypt subsequent messages.
   Generating an update locally is not healing until peers process the canonical
   transition.
8. **Deletion invariant:** obsolete epoch/private/message/skipped keys are
   deleted on a defined schedule. A bounded key-copy authority inventory covers
   active and old/offline devices, vault persistence, caches, crash/swap state,
   backups, recovery escrow, restores and exports. Every copy source has a
   named authority/owner, retention limit, destruction mechanism and recorded
   sanitization result; partial or failed sanitization narrows the claim.
   Retention for out-of-order messages is bounded by count/time.
9. **Offline invariant:** offline devices have explicit maximum age and
   catch-up rules; devices that do not update within policy are evicted or
   require a fresh authenticated rejoin.
10. **No-plaintext-shadow invariant:** protected content never enters Cell JSON,
    Flow events, previews, logs, telemetry, indexes, crash reports or companion
    archives as plaintext outside the endpoint.
11. **Downgrade/rollback invariant:** protocol version, suite, epoch, device-set
    state and monotonic counters are authenticated and rollback-detectable; an
    old client cannot make weaker data canonical.
12. **Backup invariant:** backup/export recipients and lifetimes are separate
   from live-chat membership. A recovery key is decryption authority and must
   never be counted as FS. Backup, restore and export each require an exact
   current owner-proof, Contract/Grant or deliberately narrow cell-specific
   authority path; recipient key possession alone is not authorization.
13. **Search/AI invariant:** server search or AI cannot receive protected
   plaintext by default. Client-side computation or a separately authorized,
   purpose-limited disclosure is required and recorded with domain, authority
   path, policy/commit, retention and revocation context.
14. **Metadata invariant:** exposed fields are enumerated and budgeted. Padding,
    batching or privacy transport may reduce leakage, but E2EE is not described
    as metadata anonymity.
15. **Authorization invariant:** cryptographic membership and exactly one
    audited Resolver path must both pass: verified owner proof, exact signed
    Contract/Grant/capability, or deliberately narrow cell-specific policy.
    Identity/domain/key binding, resource/action, purpose/conditions,
    freshness/expiry and revocation are checked where applicable. Missing or
    forged proof, UUID/key mismatch, wrong domain, stale/expired/revoked proof
    or capability, and unauthorized device add/remove/rejoin are denied without
    partial plaintext, key, membership, epoch or other state mutation.
16. **Error invariant:** parse, authentication, membership and decryption errors
    discard the candidate message and state changes; no plaintext fallback.

## 9. Multi-device, offline, removal and compromise

The current identity-recipient list has no complete multi-device session model.
A production design needs per-device keys, authenticated device-list updates,
sender-copy behavior, concurrent session resolution, delayed-message retention
and orphaned-session handling.

Signal's Sesame specification is useful evidence for the shape of this
problem: it encrypts to every recipient device and the sender's other devices,
tracks active/inactive sessions, handles add/delete and rollback/backup, and
bounds stale-session deletion around maximum latency. It also states that
device compromise requires replacement of the device and compromised identity
key plus correspondent notification. Sesame is a design reference, not a
library selection or proof that HAVEN implements those properties.

For groups, MLS provides a more direct standards-track model: membership
changes create ordered epochs; removal/update commits carry fresh path
material; old key material must be deleted; delayed-message key retention is
bounded; offline members that do not update eventually need eviction. PCS only
begins when group members process the relevant commit.

## 10. Backup, export, recovery and key erasure

Availability and irrecoverability pull in opposite directions:

- retaining a recovery private key enables decryption of historical backups;
- deleting every key copy may make ciphertext permanently unrecoverable;
- an offline device or old backup that retains a key defeats a universal
  erasure claim;
- removing a participant from future writes does not revoke their already-held
  plaintext or historical decryption key;
- rewrapping future content cannot remove old wrapped keys from copied
  ciphertext;
- key erasure is only credible after every authoritative key copy, recovery
  escrow, cache and backup is within a verified sanitization boundary.

NIST SP 800-57 treats keys as lifecycle objects with explicit states,
cryptoperiods, retention and destruction rather than a toggle. NIST SP 800-88
Rev. 2 defines cryptographic erase as sanitizing the media-encryption key so
recovery of decrypted target data becomes infeasible for the stated effort.
That is a bounded sanitization claim, not proof that no plaintext or key copy
exists anywhere.

Accordingly, an erasure result must name the complete key-copy authority set
inside its claimed boundary and exercise every source: active and offline
devices, vault/keychain or server-vault persistence, memory-derived crash/swap
state, backup and recovery escrow, restored snapshots and exported copies. The
evidence records retention/destruction schedules, attempted sanitization and
every failed, unavailable or partial result. An uninspected external copy makes
the broader erasure claim unproven; it is not silently treated as absent.

The current backup suite correctly sets `supportsForwardSecrecy=false`; its
long-lived recovery recipients are intentional. The signed manifest still
exposes at least owner UUID, signing-key fingerprint, dataset/version identifiers,
timestamps, commitments and fragment counts. Opaque recipient key IDs reduce
one form of stable-recipient leakage but do not make the backup anonymous.

## 11. Server search, AI and metadata

### 11.1 Search and AI choices

Opaque server-blind content removes ordinary server plaintext search,
moderation and AI inference. A decision must choose among:

- **client-side search/AI:** strongest alignment with server-blind E2EE; higher
  client resource, sync and index-management cost;
- **explicit derived disclosure:** client creates a narrowly scoped index,
  summary or prompt for a stated purpose; leakage and retention must be modeled
  as a separate data product;
- **trusted server/provider endpoint:** enables conventional compute, but the
  server/provider can see disclosed plaintext and must not be excluded from the
  E2EE endpoint set in product language;
- **specialized confidential/searchable computation:** requires a separate
  threat model, mature construction and audit; it is not assumed by this
  assessment.

Silent server decryption “for AI” is a downgrade, not an E2EE feature.

### 11.2 Metadata budget

At minimum, current or likely surfaces expose some combination of IP/network
origin, sender/recipient routing, identity or opaque key identifiers, group or
Cell identifiers, epoch/generation, timestamps, suite/algorithm, ciphertext
length, message frequency, membership changes, backup owner/dataset/version and
availability behavior.

RFC 9420 protects application content but documents remaining MLS-visible
fields and inference from group ID, epoch, frequency, membership and ciphertext
length. RFC 9750 separately recommends TLS/QUIC for transport metadata and
at-rest protection for server-persisted metadata. Neither turns message E2EE
into anonymity.

## 12. Decision options

| Option | Description | Benefit | Cost/risk | Decision |
| --- | --- | --- | --- | --- |
| A. Continuous online service-decryption endpoint | keep WSS/TLS and at-rest protection while a HAVEN service continuously receives plaintext or holds content-decryption/private recipient keys for authorized live operations | ordinary server search/AI/moderation and support remain available | service compromise exposes content; continuous authority, disclosure, retention, revocation and incident boundary; not server-blind E2EE | viable only if the service is named as an endpoint and every purpose is authorized/audited |
| B. Offline recovery/escrow endpoint | live delivery remains server-blind, but a separately governed trustee/device holds recovery authority that is unavailable to ordinary service and activated only for an authorized restore | owner-directed restore can remain possible | does not enable ordinary server search/AI; retained historical authority weakens FS/erasure; activation, export, rotation and compromise need separate controls | viable only with restore-specific authority and explicit non-blind wording when activated |
| C. Scoped monotonic E2EE epochs | per-device membership, committed epochs, vetted ratcheting protocol, client-side plaintext, explicit backup/export | defensible server-blind E2EE for declared content/new writes; supports removal, FS/PCS if correctly built | substantial client, sync, recovery, search/AI and operations work | **recommended product-design candidate** |
| D. Permanent Cell/entity “burn fuse” | once protected, entity can never create a plaintext successor or export within product | strong product constraint and simple headline | cannot stop endpoint disclosure; severe recovery/migration/agency cost; brittle forever-claim | **reject for now** |

Option A and Option B require distinct gates. The online service needs
operation-specific authority, continuous disclosure/retention audit, service-key
rotation/revocation and a service-compromise incident plan. Offline recovery
needs restore-specific authority, demonstrable unavailability during ordinary
service, activation/export audit, trustee/key revocation and a recovery-compromise
plan. Both are decryption endpoints when active; neither is server-blind against
itself, and an offline trustee does not make live server AI/search possible.

For Option C, choose protocol topology before code:

- MLS is the standards-track candidate for asynchronous groups and explicit
  membership epochs.
- A Double Ratchet plus a Sesame-like device/session manager is a candidate for
  pairwise or fan-out messaging.
- The current one-shot static-recipient envelope can remain useful for
  recoverable packages, but cannot inherit ratcheting FS/PCS claims.

Use an established, reviewed implementation where possible. Protocol selection
still requires compatibility, platform, licensing, lifecycle and independent
review; this report does not select a library.

## 13. Falsifiable acceptance gates

All gates below are **future gates; none was executed in this disk-gated static
task**.

| ID | Test/evidence | Pass condition | Falsifier |
| --- | --- | --- | --- |
| A1 | endpoint-boundary capture | delivery/resolver/storage sees no protected plaintext or content key | plaintext/key appears outside declared client endpoint |
| A2 | persistence and artifact scan | protected body absent from Cell JSON, Flow/event payloads, previews, logs, telemetry, indexes, crash data and server backups | any recoverable plaintext shadow |
| A3 | plaintext downgrade attempt | every protected-epoch path rejects plaintext/legacy/wrong-suite writes without state mutation | any path accepts or canonicalizes weaker data |
| A4 | rollback test | restored client/server state cannot lower epoch/version/device-set policy | old state produces canonical protected write |
| A5 | recipient-key compromise at T | after the deletion window, current recipient long-term/private state cannot open pre-T messages | recorded old message decrypts, as the current envelope would |
| A6 | PCS healing | attacker with state at T cannot decrypt messages after all peers process an honest fresh-key commit | attacker decrypts indefinitely after completed healing |
| A7 | device removal | after canonical removal commit, removed device cannot decrypt any new application message | removed device decrypts post-commit content |
| A8 | concurrent membership update | all honest clients converge on one epoch or fail visibly; forks are bounded and erased | divergent epochs silently accept writes |
| A9 | offline/out-of-order | messages inside declared window decrypt; keys outside count/time limit are deleted and late messages fail visibly | unlimited old-key retention or silent loss/fallback |
| A10 | add/new device | historical access matches explicit policy; new device cannot gain undeclared history | new device receives historical keys unintentionally |
| A11 | key-directory attack | substituted/stale device keys trigger authenticated warning/failure and consistency evidence | malicious directory silently inserts endpoint |
| A12 | backup/restore | declared recipients can restore exactly declared scope; nonrecipients cannot; restore cannot roll live epoch backward | unauthorized restore or live downgrade |
| A13 | key-loss drill | loss behavior matches chosen recovery promise with no hidden service key | undeclared recovery path or unexpected permanent loss |
| A14 | export test | plaintext export requires explicit action, provenance and destination warning; no export mutates epoch claim | implicit/background plaintext export |
| A15 | search/AI test | server receives only approved ciphertext/metadata or separately authorized, purpose-bound derived disclosure through an accepted owner/Contract/cell-specific path | protected plaintext reaches server/provider silently or by consent/key-possession alone |
| A16 | metadata measurement | observed routing/header/size/timing fields match a reviewed budget and privacy copy | undeclared stable identifier/content-derived field |
| A17 | interoperability vectors | independent clients agree on canonical encoding, epochs, membership, signatures and error behavior | implementation-specific acceptance divergence |
| A18 | fuzz/error atomicity | malformed/replayed/duplicated/truncated inputs fail closed with no partial state/plaintext | crash, fallback or partial epoch mutation |
| A19 | authorization allow matrix | correct-domain requests succeed only through a verified owner proof, exact current Contract/Grant/capability, or named narrow cell-specific policy, bound to the exact identity/key, resource/action, purpose/conditions, device set and policy commit | a valid declared path is rejected without contract reason, or a broader/different path is accepted |
| A20 | authorization deny/atomicity matrix | missing/forged proof, UUID/key mismatch, wrong domain, stale/expired/revoked proof or capability, unauthorized device add/remove/rejoin, and consent/key-possession-only requests are denied across content, backup/restore/export and derived AI/search disclosure with no partial plaintext/key/epoch/membership/state mutation | any denied case reveals plaintext, mutates state, or succeeds through fallback |
| A21 | key-copy inventory and sanitization | bounded inventory names active/offline devices, vault persistence, crash/swap, backup, escrow, restore and export copies; each has authority, retention/destruction schedule and exercised sanitization result, with failed/partial/unavailable results retained and the conclusion limited to the verified boundary | an authoritative copy source is omitted, a declared-destroyed key remains recoverable, or an external copy is assumed absent |
| A22 | online-service/offline-recovery separation | online service decryption is purpose-authorized and continuously audited; offline recovery material is unavailable during ordinary service and every activation/export/revocation is restore-authorized and audited; product wording names each active endpoint | offline material enables ordinary service/AI, an online endpoint is called server-blind, or recovery disclosure/activation is unlogged |

Gate A5 intentionally fails the current `haven.chat.message.v1` construction.
That failure is a useful regression test for any replacement.

## 14. Operational gates

1. Kjetil records the protected scope/domain, participant/device model, accepted
   owner/Contract/cell-specific authority paths, online-service versus offline
   recovery endpoints, search/AI choice, metadata budget and migration policy.
2. Security design maps every invariant to an owner, protocol mechanism,
   persisted state, authority/policy commit, complete key-copy inventory and
   deletion/sanitization schedule.
3. Current false/ambiguous FS and E2EE claims are removed or made explicitly
   bootstrap-only before broader use.
4. A vetted protocol and implementation strategy pass independent cryptographic
   design review before integration.
5. Deterministic vectors and all A1–A22 gates pass in isolated environments.
6. Cross-platform clients pass multi-device, offline, rollback, concurrent
   update, removal and restore trials.
7. Operations complete device-loss, key-compromise, recovery-key loss,
   online-service compromise, offline-trustee activation/compromise,
   failed-sanitization, malicious-directory, metadata-leak and downgrade
   incident drills.
8. A staged trial proves observability without collecting protected content and
   proves support can diagnose failures without service decryption keys.
9. Privacy, authority/denial, backup/recovery, AI/search, export and endpoint
   wording match measured behavior.
10. Only after independent review and staged evidence may a production owner
    decide deployment and public wording. This task owns neither.

Hard-disk coordination currently blocks all builds, dependency resolution and
tests. No gate may be marked passing by inference.

## 15. Disagreement and uncertainty ledger

| Topic | Statement A | Statement B/evidence | Resolution |
| --- | --- | --- | --- |
| Fabel assessment | task requires readable Fabel analysis | Fabel CLI returned only a usage-credit error; collaboration surfaces expose no Codex-to-Fabel assessor | **pending/external block; no Fabel view invented** |
| Present chat encryption | suite/policy/envelope bootstrap exists | `ChatCell` says disabled/bootstrap-only and normal send persists plaintext | current E2EE claim rejected |
| Forward secrecy | `chatMessageV1.supportsForwardSecrecy=true` | static recipient private key plus recorded ephemeral public key opens old wraps; RFC 9180 excludes recipient-compromise FS | suite flag contradicted/release-blocking |
| Rekey/removal | generation and membership checkpoint say “rekeyed” | no key rotation, committed device epoch or secret erasure occurs | treat as advisory bookkeeping only |
| At-rest encryption | encrypted Cell envelope is enabled by lifecycle policy | host holds master key; legacy plaintext passes through; base storage default may ignore options | do not call E2EE; audit backends/migration separately |
| Transport evidence | Book 08 describes universally ordered/verifiable envelopes | Book 06 limits generic Flow evidence guarantees | narrower Book 06 contract controls; docs need reconciliation |
| Irreversibility | encryption must never be disabled | endpoint/export/recovery and existing plaintext are unavoidable counterexamples | adopt scoped monotonic write policy only if chosen |
| Recovery vs erasure | user recovery should remain possible | retained recovery keys defeat absolute historical key erasure/FS | explicit product tradeoff; no universal claim |
| Server AI/search | desirable product capability | server-blind ciphertext is unavailable to ordinary server compute | choose client-side or separately disclosed endpoint; never silent downgrade |

## 16. Required product decisions

Before implementation, Kjetil/product ownership must answer:

1. What exactly is protected: whole Cell, entity, field/content class, chat,
   attachment or an explicit combination?
2. Is the protection unit an epoch, immutable entity lifetime, or new-write
   policy? What happens to existing plaintext?
3. Are all devices independent cryptographic clients? How are device keys
   authenticated, added, removed and recovered?
4. Who is an allowed endpoint: only user devices, a HAVEN service, recovery
   trustee, organization administrator, or external AI provider?
5. Must future-device history sync be possible? If yes, which endpoint stores or
   re-encrypts historical secrets/content?
6. Is recovery preferable to cryptographic irrecoverability, and for which data
   classes? Who holds recovery authority?
7. Which search, moderation, preview and AI functions must survive, and what
   derived disclosure is acceptable?
8. Which metadata is acceptable to delivery, push, backup and analytics
   services, and for how long?
9. What offline duration and skipped-key retention window is acceptable before
   forced rejoin or message loss?
10. What exact product wording is desired: transport encryption, encryption at
    rest, recoverable client encryption, or server-blind E2EE with declared
    endpoints?

## 17. Fabel section — externally blocked

**Status: PENDING — EXTERNALLY BLOCKED. No readable Fabel assessment exists.**

The mandated collaboration workflow was used for a bounded Fabel request. The
only returned text was:

```text
Fable 5 requires usage credits. Run /usage-credits to continue or switch models with /model.
```

This is an access error, not an assessment, and receives no evidentiary credit.
Development-admin confirmed that the available `codex-local` and filesystem
MCPs are Claude-to-Codex/file exchange bridges, not a separate callable
Codex-to-Fabel assessment tool. `QUEUE.md` marks the exit gate externally
blocked. This worker did not retry, evade the credit gate, substitute another
model, or label Codex text as Fabel.

Kjetil subsequently reset the general model/token quota. One newly authorized,
bounded retry was made with model `fable`, no tools, safe mode and no session
persistence. It exited 1 with the same Fabel-specific usage-credit message and
no assessment text. The general quota reset therefore did not satisfy the
Fabel usage-credit gate. No further retry, `/usage-credits` action or model
substitution was attempted.

When a readable external Fabel response is supplied, preserve it verbatim or as
a clearly attributed attachment, then add a line-by-line agreement/disagreement
audit against the pinned repository and primary standards. Until then the
initiative cannot pass its first exit gate, even though the Codex/static portion
is review-ready.

## 18. Primary standards and specifications

Retrieved 2026-07-21; all are official primary publications/specifications.

- [RFC 9420 — Messaging Layer Security (MLS) Protocol](https://www.rfc-editor.org/rfc/rfc9420.html): message-level E2EE for asynchronous groups; epochs, removal, deletion schedules, FS/PCS, offline-member and delivery-service limits.
- [RFC 9750 — MLS Architecture](https://www.rfc-editor.org/rfc/rfc9750.html): transport independence, delivery/authentication architecture, metadata exposure and server metadata-at-rest guidance.
- [RFC 9180 — Hybrid Public Key Encryption](https://www.rfc-editor.org/rfc/rfc9180.html): §9.7.4 states that HPKE is not forward-secret against later recipient private-key compromise; also excludes application downgrade/replay and length hiding.
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html): connection protection, forward secrecy conditions, traffic analysis and lack of PCS after traffic-secret compromise.
- [NIST SP 800-57 Part 1 Rev. 5](https://doi.org/10.6028/NIST.SP.800-57pt1r5): key states, cryptoperiods, retention, compromise, archival and destruction lifecycle.
- [NIST SP 800-88 Rev. 2](https://doi.org/10.6028/NIST.SP.800-88r2): media sanitization and bounded cryptographic-erase definition.
- [Signal Double Ratchet specification](https://signal.org/docs/specifications/doubleratchet/): per-message ratchets, forward security, break-in recovery/PCS and secure-deletion assumptions for pairwise sessions.
- [Signal Sesame specification](https://signal.org/docs/specifications/sesame/): asynchronous multi-device session management, add/delete, rollback/backup, delayed messages, device compromise and stale-session deletion.

## 19. Final gate statement

The independent static evidence is sufficient for a **NO-GO** on current E2EE,
forward-secrecy and “cannot be disabled” claims. It is not a certification of a
replacement. The Codex portion is ready for review; the required Fabel portion
and all executable/operational evidence remain honestly blocked or pending.

No code, keys, secrets, build, dependency resolution, test, commit, push, PR,
merge, deployment, service restart or production/staging action occurred in
this assessment.
