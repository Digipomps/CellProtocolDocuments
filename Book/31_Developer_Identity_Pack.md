# Chapter 31 - Developer Identity Pack

Status: draft contract and fixture.

Last updated: 2026-07-06.

This chapter defines the developer/staging identity package used to exercise
normal CellProtocol identity behavior. It is not a shared login account and it
is not a private-key export. The package gives developers a stable set of
simulated entities, domain-scoped identity public descriptors, vault
references, and public-safe contact endpoints so services can be tested with
realistic owners, members, invitations, grants, and denial paths.

## 1. Security Rules

The package follows the identity model in Chapter 03:

- an Entity may have many Identities;
- every Identity belongs to exactly one `identityDomain`;
- the same Identity UUID must not be reused across domains;
- private key material remains inside an `IdentityVault`;
- the checked-in package contains public descriptors, vault references, and
  endpoint refs only;
- no endpoint ref may include route refs, push tokens, device ids, stable owner
  hashes, or raw private transport state.

Access follows Chapters 04 and 06:

- owner access requires owner proof through the correct vault;
- non-owner access is denied unless a Resolver-accepted Contract grants the
  exact capability;
- an Agreement request alone is not access;
- endpoint ids, profile ids, contact refs, QR payloads, or deep links are not
  authority;
- ContactEndpoint requests are signed, expiring, purpose-bound requests that
  create owner-reviewable tickets, not read access to another entity.

## 2. Files

- `Book/developer_identity_pack_contract_v0.json`
  Machine-readable contract for the package.
- `Tools/DeveloperIdentityPack/fixtures/developer_identity_pack.v0.json`
  Current simulated entities and identity descriptors.
- `Tools/DeveloperIdentityPack/validate_identity_pack.py`
  Deterministic validator for the fixture and future packs.
- `Tools/DeveloperIdentityPack/tests/test_validate_identity_pack.py`
  Negative and positive validation tests.
- `Tools/DeveloperIdentityPack/generate_invite_relations.py`
  Projects the pack into owner-local `EntityAnchor` invite seed mutations.
- `Tools/DeveloperIdentityPack/generated/developer_invite_relations.v0.json`
  Generated seed for `relations.people`, `relations.entities`,
  `relations.identities`, `relations.chatInvites`, and
  `entityRepresentation.chatInviteProfile`.
- `Tools/DeveloperIdentityPack/tests/test_generate_invite_relations.py`
  Tests for the invite relation projection and private-data guardrails.
- `Tools/DeveloperIdentityPack/resolve_invite_command.py`
  Local fixture resolver for `inviter <name>` commands against the generated
  seed.

## 3. Current Fixture Shape

The fixture contains:

- five simulated entities;
- at least one Identity for every domain listed on each entity;
- one home vault reference per simulated entity, plus a service vault for the
  staging agent;
- public-safe `ContactEndpoint` descriptors for chat invitations and contact
  requests;
- `EntityRepresentation`-compatible objects with empty relationship arrays for
  current Swift decoding compatibility;
- an extension block that carries identity refs, contact endpoint refs, and
  chat-invite matching metadata without pretending those fields are already
  encoded by `EntityRepresentation`.

The extension block is deliberately named separately:

```json
{
  "entityRepresentation": {
    "name": "Eira Solheim",
    "types": [],
    "subTypes": [],
    "parts": [],
    "partOf": [],
    "purposes": [],
    "interests": [],
    "entities": [],
    "states": [],
    "agreementRefs": []
  },
  "entityRepresentationExtensions": {
    "schema": "haven.entityRepresentation.simulated.v0",
    "identityRefs": [],
    "contactEndpointRefs": [],
    "chatInviteProfile": {}
  }
}
```

This avoids documenting non-current Swift behavior as if it were already part
of the core `EntityRepresentation` encoder. Runtime code can still project the
extension data into `EntityAnchorData` roots such as
`person.contact.endpoints`, `relations.people`, and
`entityRepresentation.chatInviteProfile`.

## 4. Invite Relation Seed

The generated invite seed turns the package into the owner-local shape that
current CellScaffold Personal Co-Pilot already reads:

```bash
python3 Tools/DeveloperIdentityPack/generate_invite_relations.py --write
```

The default requester is `entity:dev-sim:eira`, so the generated invite
candidates are:

- Jonas Berg
- Mina Aas
- Noor Haddad

The generated file is:

```text
Tools/DeveloperIdentityPack/generated/developer_invite_relations.v0.json
```

It contains direct owner-local mutations for:

- `relations.people[+]`
- `relations.entities.<entityID>`
- `relations.identities.<identityID>`
- `relations.chatInvites`
- `entityRepresentation.chatInviteProfile`

Once the owner applies those mutations to `cell:///EntityAnchor`,
Personal Co-Pilot can resolve prompts such as:

```text
inviter Jonas
inviter Mina
inviter Noor
```

to a relation `profileID`, target domain identity UUID, and public-safe
`ContactEndpoint` descriptor. Each relation also contains
`simulation.responsePolicy` and `simulation.rolePrompt`, so a test harness can
produce a relevant simulated reply after the invite is accepted.

For local fixture verification without a running scaffold:

```bash
python3 Tools/DeveloperIdentityPack/resolve_invite_command.py \
  "inviter Jonas" \
  --message "Kan du sjekke endpoint og sikkerhet?"
```

The resolver returns the matched `profileID`, public-safe contact endpoint,
message payload, and a simulated reply body. It intentionally reports that the
lookup itself grants no authority; live sending still belongs to
CellScaffold/Personal Co-Pilot and ContactEndpoint/Resolver policy.

Security boundary:

- the seed is owner-local social/contact metadata;
- names and profile ids are lookup hints, not proof or authority;
- endpoint ids are routing hints, not permission grants;
- private keys remain in `IdentityVault`;
- private delivery routes, push tokens, owner hashes, and proof bodies remain
  outside the seed;
- non-owner reads still require a Resolver-accepted Contract with exact
  capability.

CellScaffold also exposes an Entity Studio action named
`entityStudio.seedChatInviteCandidatesToEntityAnchor` that writes a built-in
demo version of this same `relations.people` shape into the active owner's
`EntityAnchor`.

## 5. Interaction Cells

The default interaction surface is `ContactEndpointCell`:

- endpoint cell: `cell://staging.haven.digipomps.org/ContactEndpoint`
- local fallback: `cell:///ContactEndpoint`
- accepted topics:
  - `contact.request`
  - `contact.message`
  - `chat.invitation`
- required action:
  - `contact.request.submit`

The endpoint descriptor is a routing and policy hint. It does not grant contact
access by itself. A requester still needs a signed request, accepted purpose,
fresh expiry, nonce, and whatever Contract/capability the endpoint policy
requires. Owner response, private routes, push delivery, and bridge wakeup
state remain inside the owning cell/vault boundary.

## 6. Dev Usage

Use the fixture when a service needs to test:

1. Owner access to private entity state.
2. A member identity with an explicit grant.
3. A non-owner identity without a grant.
4. Wrong-domain identities.
5. Wrong-vault signing attempts.
6. Chat invitation and contact request flows.
7. Revocation or expired capability behavior.

Do not use the fixture to bypass Resolver checks. If a test passes because it
injects an entity ref or endpoint id directly into a privileged path, the test
is proving the wrong thing.

## 7. Validation

Run:

```bash
python3 Tools/DeveloperIdentityPack/validate_identity_pack.py \
  Tools/DeveloperIdentityPack/fixtures/developer_identity_pack.v0.json
```

The validator rejects:

- forbidden secret-bearing keys;
- duplicated identity UUIDs;
- reused identity domains on one entity;
- identities without an `IdentityVault` home reference;
- exported key material;
- broad or wildcard grants;
- contact endpoint descriptors with private route material;
- missing owner-only default access policy.

For test coverage:

```bash
python3 -m unittest \
  Tools.DeveloperIdentityPack.tests.test_validate_identity_pack \
  Tools.DeveloperIdentityPack.tests.test_generate_invite_relations
```

The invite seed can also be regenerated and validated in one pass:

```bash
python3 Tools/DeveloperIdentityPack/generate_invite_relations.py --write
```

## 8. Current Limits

This package is a checked-in contract and seed fixture. It does not create
actual identities in a running `IdentityVault` by itself. Runtime provisioning
should use the existing `IdentityVault` implementations and should write only
public descriptors back to the package shape. The next runtime step is a small
provisioning command that creates the missing domain identities inside the
selected staging vault and emits a matching public descriptor file.

The generated invite seed does not currently apply itself to a running
CellScaffold. It is a deterministic set of owner-local mutations. A runtime
tool, Entity Studio action, or test harness must apply those mutations as the
owner before `inviter <name>` can resolve the generated people in a live chat
surface.

Cross-scaffold access to the same owner entity data is defined separately in
[Chapter 32 - Cross-Scaffold Entity Enrollment](32_Cross_Scaffold_Entity_Enrollment.md).
The identity pack can provide public descriptors and test data for that flow,
but enrollment authority still comes from signed owner approval, active
scaffold links, exact capabilities, and Resolver enforcement.
