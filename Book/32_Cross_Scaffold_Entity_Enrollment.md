# Chapter 32 - Cross-Scaffold Entity Enrollment

Status: draft contract and implementation map.

Last updated: 2026-07-08.

This chapter defines how one owner can reach the same private entity data from
multiple scaffolds without reusing one Identity everywhere, copying private
keys, or making a hosted scaffold an implicit authority.

The goal is simple:

- the owner can use the same `EntityAnchor` and `EntityRepresentation` data
  from every scaffold they have explicitly enrolled;
- each scaffold uses its own domain-scoped Identity;
- private key material remains in the relevant `IdentityVault`;
- all access remains Resolver-enforced and capability-scoped;
- canonical entity data lives in the selected home scaffold unless the owner
  explicitly approves another placement or cache policy.

## 1. Core Rule

An enrolled scaffold is not the entity and is not the owner. It is a
capability-bearing runtime identity that the owner has approved for a bounded
purpose.

The protocol boundary is:

```text
Owner Identity in owner IdentityVault
  -> approves scaffold enrollment
  -> EntityScaffoldEnrollment records active scaffold link
  -> Resolver grants exact entity-data capabilities
  -> enrolled scaffold reads/writes EntityAnchor through that grant
```

No `cell://` reference, endpoint URL, QR payload, scaffold name, or copied
profile id grants authority by itself.

## 2. Canonical Data Placement

Entity data should have one canonical home:

- `cell:///EntityAnchor` for owner-private entity data;
- `entityRepresentation` for the durable current representation;
- `relations`, `agreements`, `purposes`, and `chronicle` for related private
  and contractual state;
- `EntityScaffoldEnrollment` for active scaffold links.

Other scaffolds may keep indexes, local UI state, or encrypted caches, but
those are not the source of truth unless the owner explicitly changes the home
policy.

## 3. Home Scaffold Selection

The default home scaffold should be the most available scaffold that still
fits the owner's declared cost and privacy policy.

Selection inputs:

- `ownerChoice`: explicit owner override, if present;
- `availabilityTier`: local-only, LAN, private cloud, hosted staging, swarm;
- `estimatedMonthlyCostNOK`;
- `maxMonthlyCostNOK`;
- `dataSensitivity`: synthetic, public, private, sensitive;
- `region` and hosting boundary;
- `backupPolicy`;
- `transportPolicy`: local, VPN/LAN, TLS remote bridge, offline bundle;
- `ownerPresenceRequiredForWrites`.

Default decision:

1. Prefer an explicit owner choice.
2. Otherwise choose the highest-availability candidate whose estimated cost is
   within `maxMonthlyCostNOK` and whose hosting boundary is allowed for the data
   sensitivity.
3. If no hosted candidate is acceptable, keep the canonical home local and
   expose only enrolled remote access or encrypted snapshots.
4. If cost is unknown, treat the placement as requiring owner confirmation.

This lets a developer use a hosted CellScaffold or swarm-backed scaffold for
staging when it is useful, without silently turning that host into the owner's
global data home.

## 4. Enrollment Flow

The enrollment flow extends the existing CellScaffold
`EntityScaffoldEnrollment` pattern:

1. The candidate scaffold creates or selects its own domain-scoped Identity in
   its own `IdentityVault`.
2. The candidate sends an `EntityScaffoldEnrollmentRequest` to the owner's
   enrollment cell. The request includes scaffold public metadata, requested
   capabilities, target `entityAnchorReference`, audience, origin, expiry, and
   nonce.
3. The request is signed by the scaffold Identity. The home scaffold verifies
   the signature before storing a pending enrollment.
4. The owner approves a subset of requested capabilities with a fresh owner
   proof. The approval carries a replay-protected `jti`.
5. The enrollment cell returns an activation challenge.
6. The candidate scaffold signs the challenge and completes activation.
7. The enrollment cell records an active `EntityScaffoldLinkRecord`.
8. The Resolver uses the active link and capability set when the enrolled
   scaffold calls entity data keypaths.

The existing request -> approval -> activation challenge -> active link shape
is the right model. The missing runtime layer is the grant-backed entity data
proxy that turns an active link into remote `EntityAnchor` read/write access.

## 5. Capabilities

Capabilities must be narrow and explicit. Examples:

- `entity.representation.read`
- `entity.representation.write`
- `entity.relations.read`
- `entity.relations.write.ownerApproved`
- `entity.invite.resolve`
- `entity.contactEndpoint.request`
- `entity.cache.read`
- `entity.cache.refresh`
- `entity.homePolicy.read`
- `entity.homePolicy.proposeChange`

Avoid wildcard grants such as `entity.*`. A scaffold that can render the
owner's public profile does not automatically get write access to private
relations, credentials, or contact endpoints.

## 6. Cache And Snapshot Rules

Cross-scaffold access needs caching for local UX, but caches must not become
authority.

Allowed cache behavior:

- encrypted local cache with expiry;
- snapshot hash, revision, and source home reference;
- read-only rendering while offline;
- queued writes marked `pendingOwnerHomeCommit`;
- explicit conflict handling on reconnect.

Forbidden cache behavior:

- raw private key material;
- copied owner Identity or signing material;
- treating a stale cache as proof of current capability;
- granting another scaffold access because one scaffold has a local cache;
- writing cached entity data to public profiles, logs, prompts, or skeletons.

## 7. Resolver Enforcement

Every entity data operation from a non-home scaffold must carry:

- requester scaffold Identity UUID;
- requester public key and signature;
- active enrollment link id;
- requested keypath and capability;
- purpose ref;
- target `entityAnchorReference`;
- freshness or replay guard where the action mutates state.

The Resolver denies access when:

- no active link exists;
- the link is revoked or expired;
- requested capability is not granted;
- purpose or audience does not match;
- signature is missing or invalid;
- request tries to escalate beyond the approved capability set;
- cache revision is presented as authority;
- cost or hosting policy requires owner confirmation.

## 8. Current Implementation Map

Current CellScaffold code already has a concrete enrollment cell:

- endpoint: `cell:///EntityScaffoldEnrollment`;
- get: `state`, `contracts`, `linkedScaffolds`, `pendingEnrollments`;
- set: `enrollment.begin`, `enrollment.approve`, `enrollment.complete`,
  `enrollment.revoke`, `enrollment.validate`;
- record shape: signed request, signed approval, activation proof, active link;
- tested denial paths: replayed approval, wrong audience, capability
  escalation, forged scaffold signature, expired request, foreign requester.

Current documents also define the developer identity pack and invite seed:

- simulated entities use one Identity per `identityDomain`;
- private keys remain vault-bound;
- invite/profile/contact descriptors are owner-local routing hints;
- generated invite relations target `EntityAnchor` owner-local keypaths.

Not implemented yet:

- a shared `EntityHomePolicy` cell or keypath;
- automatic home scaffold selection by cost/availability;
- a grant-backed remote `EntityAnchor` proxy for every enrolled scaffold;
- live sync of `entityRepresentation` across multiple CellScaffold instances;
- encrypted cache/snapshot conflict resolution.

## 9. Runtime Next Step

The next implementation slice should be in CellScaffold:

1. Add `EntityHomePolicy` state near `EntityScaffoldEnrollment`, or as a small
   sibling cell if that keeps policy clearer.
2. Add a read path that resolves the owner's canonical `entityAnchorReference`
   from an active scaffold link.
3. Add a write path that accepts only approved entity keypaths and records
   FlowElements for each remote write.
4. Add tests for:
   - owner can read entityRepresentation from two enrolled scaffolds;
   - non-enrolled scaffold is denied;
   - revoked scaffold is denied;
   - requested capability outside the approved subset is denied;
   - hosted placement is selected only within cost/privacy policy;
   - stale cache can render but cannot authorize writes.
5. Keep private key and secret material inside the relevant vault or
   SecretCredentialCell boundary.

## 10. Testing With Multiple CellScaffold Instances

For developer/staging tests, use the same canonical home scaffold and enroll
each test scaffold as a separate scaffold Identity:

```text
home scaffold
  cell:///EntityAnchor
  cell:///EntityScaffoldEnrollment

local scaffold A
  scaffold Identity domain: domain:scaffold:local-a
  active link: entity.representation.read, entity.invite.resolve

local scaffold B
  scaffold Identity domain: domain:scaffold:local-b
  active link: entity.representation.read, entity.relations.write.ownerApproved
```

This gives repeatable tests where each scaffold sees the same
`entityRepresentation`, while denial behavior still proves that access comes
from enrollment and capability grants rather than shared global identity.
