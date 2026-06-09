import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from concierge_knowledge import ConciergeKnowledgeCorpusCell, REQUIRED_RESPONSE_KEYS


class ConciergeKnowledgeCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = ConciergeKnowledgeCorpusCell.load(ROOT / "palazzo_seed_corpus.json")

    def assert_response_envelope(self, response):
        self.assertTrue(REQUIRED_RESPONSE_KEYS.issubset(response.keys()))
        self.assertIsInstance(response["citations"], list)
        self.assertIn(response["confidence"], {"high", "medium", "low", "blocked"})

    def test_source_list_has_citations(self):
        response = self.cell.dispatch("source.list")
        self.assert_response_envelope(response)
        self.assertEqual(response["confidence"], "high")
        self.assertGreaterEqual(len(response["records"]), 10)
        self.assertTrue(response["citations"])

    def test_menu_current_flags_image_pdf_review(self):
        response = self.cell.dispatch("menu.current")
        self.assert_response_envelope(response)
        self.assertTrue(response["needs_human_review"])
        self.assertIn("image-based menu PDF", response["answer"])
        self.assertTrue(any(citation["source_id"] == "src-palazzo-menu-pdf" for citation in response["citations"]))

    def test_allergen_query_refuses_guest_safe_answer_without_verification(self):
        response = self.cell.dispatch(
            "concierge.knowledge.query",
            {"query": "Hva er allergenene i arancini?", "audience": "guest"},
        )
        self.assert_response_envelope(response)
        self.assertEqual(response["confidence"], "low")
        self.assertTrue(response["needs_human_review"])
        self.assertIn("cannot give a guest-safe allergen answer", response["answer"])
        self.assertTrue(any(citation["source_id"] == "src-mattilsynet-allergen" for citation in response["citations"]))

    def test_wine_query_blocks_availability_claims(self):
        response = self.cell.dispatch(
            "concierge.knowledge.query",
            {"query": "Hvilken vin passer til pasta vongole?", "audience": "concierge"},
        )
        self.assert_response_envelope(response)
        self.assertTrue(response["needs_human_review"])
        self.assertIn("No verified wine list", response["answer"])
        self.assertTrue(any("Wine availability is not verified" in warning for warning in response["warnings"]))

    def test_unknown_structured_question_does_not_guess(self):
        response = self.cell.dispatch(
            "concierge.knowledge.query",
            {"query": "Hva er dagens vin på glass?", "audience": "guest"},
        )
        self.assert_response_envelope(response)
        self.assertTrue(response["needs_human_review"])
        self.assertIn("No verified wine list", response["answer"])

    def test_claim_review_returns_claim(self):
        response = self.cell.dispatch("claim.review", {"claim_id": "claim-alcohol-guardrail"})
        self.assert_response_envelope(response)
        self.assertEqual(response["confidence"], "high")
        self.assertFalse(response["needs_human_review"])
        self.assertTrue(any(citation["source_id"] == "src-helsedir-alcohol-ad" for citation in response["citations"]))

    def test_audit_rejects_uncited_answer(self):
        response = self.cell.dispatch(
            "audit.answer",
            {"response": {"answer": "Arancini contains milk.", "needs_human_review": False}},
        )
        self.assert_response_envelope(response)
        self.assertEqual(response["confidence"], "blocked")
        self.assertTrue(response["needs_human_review"])

    def test_eval_set_has_at_least_100_valid_questions(self):
        path = ROOT / "eval_questions.jsonl"
        rows = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        self.assertGreaterEqual(len(rows), 100)
        self.assertTrue(all("query" in row and "expected_route" in row for row in rows))


if __name__ == "__main__":
    unittest.main()
