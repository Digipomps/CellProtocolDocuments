import copy
import json
import unittest
from pathlib import Path

from Tools.DeveloperIdentityPack.validate_identity_pack import validate_package


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "Tools" / "DeveloperIdentityPack" / "fixtures" / "developer_identity_pack.v0.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class DeveloperIdentityPackValidationTests(unittest.TestCase):
    def test_fixture_is_valid(self):
        self.assertEqual(validate_package(load_fixture()), [])

    def test_duplicate_identity_domain_on_entity_is_rejected(self):
        package = load_fixture()
        package["entities"][0]["identities"][1]["identityDomain"] = package["entities"][0]["identities"][0]["identityDomain"]

        issues = validate_package(package)

        self.assertTrue(any("exactly one identity" in issue.message for issue in issues))

    def test_forbidden_secret_field_is_rejected(self):
        package = load_fixture()
        package["entities"][0]["identities"][0]["seed"] = "do-not-store-this"

        issues = validate_package(package)

        self.assertTrue(any("forbidden secret" in issue.message for issue in issues))

    def test_contact_endpoint_route_refs_are_rejected(self):
        package = load_fixture()
        package["entities"][0]["entityRepresentationExtensions"]["contactEndpointRefs"][0]["routeRefs"] = []

        issues = validate_package(package)

        self.assertTrue(any("forbidden secret or private-route key" in issue.message for issue in issues))

    def test_broad_capability_is_rejected(self):
        package = load_fixture()
        package["explicitGrantExamples"][0]["capabilities"].append("state.*")

        issues = validate_package(package)

        self.assertTrue(any("broad capability" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()

