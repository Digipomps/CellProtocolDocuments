import json
import unittest
from pathlib import Path

from Tools.DeveloperIdentityPack.generate_invite_relations import (
    build_invite_seed,
    validate_invite_seed,
)
from Tools.DeveloperIdentityPack.resolve_invite_command import resolve_invite_command


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "Tools" / "DeveloperIdentityPack" / "fixtures" / "developer_identity_pack.v0.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class DeveloperInviteRelationSeedTests(unittest.TestCase):
    def test_builds_owner_local_relations_for_invite_commands(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")

        self.assertEqual(validate_invite_seed(seed), [])
        names = [relation["displayName"] for relation in seed["relations"]["people"]]
        self.assertEqual(names, ["Jonas Berg", "Mina Aas", "Noor Haddad"])
        self.assertEqual(seed["intendedRuntime"]["personalCopilotLookupPath"], "relations.people")
        self.assertIn("inviter Jonas", seed["intendedRuntime"]["inviteCommandExamples"])
        self.assertNotIn("Eira Solheim", names)
        self.assertNotIn("HAVEN Staging Service Agent", names)

    def test_relations_have_contact_endpoint_and_response_policy(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")

        for relation in seed["relations"]["people"]:
            endpoint = relation["contact"]["endpoints"][0]
            simulation = relation["simulation"]
            self.assertEqual(endpoint["visibility"], "owner-private")
            self.assertIn("personal.chat.invite.receive", endpoint["purposes"])
            self.assertIn("personal.chat.simulation.respond", endpoint["purposes"])
            self.assertEqual(simulation["responsePolicy"]["mode"], "test-relevant-short-reply")
            self.assertGreaterEqual(len(simulation["responsePolicy"]["suggestedReplies"]), 1)
            self.assertIn("send-external-message", simulation["mustNot"])

    def test_seed_mutations_target_only_owner_local_invite_paths(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")
        keypaths = [mutation["keypath"] for mutation in seed["seedMutations"]]

        self.assertEqual(keypaths.count("relations.people[+]"), 3)
        self.assertIn("entityRepresentation.chatInviteProfile", keypaths)
        self.assertTrue(any(keypath.startswith("relations.entities.") for keypath in keypaths))
        self.assertTrue(any(keypath.startswith("relations.identities.") for keypath in keypaths))

    def test_private_route_material_is_rejected(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")
        seed["relations"]["people"][0]["contact"]["endpoints"][0]["routeRefs"] = []

        issues = validate_invite_seed(seed)

        self.assertTrue(any("forbidden secret" in issue.message for issue in issues))

    def test_resolves_invite_command_to_profile_endpoint_and_simulated_reply(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")

        result = resolve_invite_command(seed, "inviter Jonas", message_body="Kan du sjekke endpoint og sikkerhet?")

        self.assertTrue(result["ok"])
        self.assertEqual(result["profileID"], "relation-person-dev-sim-jonas")
        self.assertEqual(result["contactEndpoint"]["endpointId"], "contact-dev-sim-jonas-chat")
        self.assertIn("endpoint", result["simulatedReply"]["body"].lower())
        self.assertTrue(result["simulatedReply"]["requiresAcceptedInviteBeforeReply"])
        self.assertEqual(result["security"]["authority"], "none_from_lookup")

    def test_unknown_invite_name_returns_no_match(self):
        seed = build_invite_seed(load_fixture(), requester_entity_ref="entity:dev-sim:eira")

        result = resolve_invite_command(seed, "inviter Ukjent Person")

        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "no_invite_relation_match")


if __name__ == "__main__":
    unittest.main()
