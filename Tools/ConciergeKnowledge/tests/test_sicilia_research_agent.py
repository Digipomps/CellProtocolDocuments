import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sicilia_research_agent as agent


class SiciliaResearchAgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = agent.load_jsonl(agent.DEFAULT_SOURCES)
        cls.claims = agent.load_jsonl(agent.DEFAULT_CLAIMS)
        cls.sources_by_id = agent.source_index(cls.sources)

    def test_seed_files_validate(self):
        issues = agent.validate_sources(self.sources)
        issues.extend(agent.validate_claims(self.claims, self.sources_by_id))
        self.assertEqual(issues, [])

    def test_alcohol_claims_carry_policy(self):
        alcohol_claims = [claim for claim in self.claims if claim["topic"] in agent.ALCOHOL_TOPICS]
        self.assertGreaterEqual(len(alcohol_claims), 4)
        self.assertTrue(all(claim.get("alcohol_policy") for claim in alcohol_claims))

    def test_publishable_claims_exclude_single_source_food_context(self):
        publishable = [claim["id"] for claim in self.claims if agent.is_publishable(claim)]
        self.assertIn("claim-cerasuolo-blend", publishable)
        self.assertNotIn("claim-sicily-presidia-examples", publishable)
        self.assertNotIn("claim-palazzo-wine-availability-boundary", publishable)

    def test_review_bundle_has_rag_candidates_only_for_publishable_claims(self):
        bundle = agent.build_bundle(self.sources, self.claims)
        self.assertEqual(bundle["status"], "review_required_before_ingest")
        self.assertEqual(bundle["claim_count"], len(self.claims))
        self.assertEqual(bundle["publishable_claim_count"], len(bundle["rag_candidate_chunks"]))
        self.assertTrue(all(chunk["case_id"] == "palazzo_sicilia_supplement" for chunk in bundle["rag_candidate_chunks"]))

    def test_bundle_is_json_serializable(self):
        encoded = json.dumps(agent.build_bundle(self.sources, self.claims), sort_keys=True)
        self.assertIn("palazzo_sicilia_supplement", encoded)


if __name__ == "__main__":
    unittest.main()
