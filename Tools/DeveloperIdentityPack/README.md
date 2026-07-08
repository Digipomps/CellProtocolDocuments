# Developer Identity Pack

This tool validates developer/staging identity packs for CellProtocol.

The pack is intentionally public-descriptor only:

- no private keys;
- no seed material;
- no route refs or push tokens;
- no reused identity UUID across domains;
- no non-owner access without an exact explicit grant.

Run:

```bash
python3 Tools/DeveloperIdentityPack/validate_identity_pack.py \
  Tools/DeveloperIdentityPack/fixtures/developer_identity_pack.v0.json
```

Generate the owner-local invite seed used by Personal Co-Pilot and EntityAnchor:

```bash
python3 Tools/DeveloperIdentityPack/generate_invite_relations.py --write
```

This writes:

```text
Tools/DeveloperIdentityPack/generated/developer_invite_relations.v0.json
```

The generated seed projects simulated people from the identity pack into
`cell:///EntityAnchor` owner-local keypaths:

- `relations.people`
- `relations.entities`
- `relations.identities`
- `relations.chatInvites`
- `entityRepresentation.chatInviteProfile`

With those mutations applied by the owner, existing Personal Co-Pilot invite
matching can resolve commands such as `inviter Jonas`, `inviter Mina`, and
`inviter Noor` to a `profileID` and public-safe `contactEndpoint` descriptor.
The simulated relation also carries `simulation.responsePolicy` so a test
harness can produce a scoped, relevant reply. The seed does not contain private
keys, route refs, push tokens, or authority grants.

Resolve a generated invite command locally:

```bash
python3 Tools/DeveloperIdentityPack/resolve_invite_command.py \
  "inviter Jonas" \
  --message "Kan du sjekke endpoint og sikkerhet?"
```

The resolver prints the matched `profileID`, public-safe `contactEndpoint`
descriptor, message payload, and simulated reply policy. This is a fixture
resolver for tests; live sending still goes through CellScaffold/Personal
Co-Pilot and the ContactEndpoint/Resolver policy.

Tests:

```bash
python3 -m unittest \
  Tools.DeveloperIdentityPack.tests.test_validate_identity_pack \
  Tools.DeveloperIdentityPack.tests.test_generate_invite_relations
```
