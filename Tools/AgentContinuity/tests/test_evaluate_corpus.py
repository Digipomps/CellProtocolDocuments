import json
import unittest
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[3]
TOOL_ROOT = ROOT / "Tools" / "AgentContinuity"
sys.path.insert(0, str(TOOL_ROOT))

import evaluate_corpus as evaluator  # noqa: E402


MANIFEST = TOOL_ROOT / "evaluation" / "deterministic_manifest.v1.json"


class AgentContinuityCorpusTests(unittest.TestCase):
    def test_manifest_matches_all_expected_results(self):
        manifest = evaluator.load_manifest(MANIFEST)

        report = evaluator.evaluate_manifest(manifest, TOOL_ROOT)

        self.assertEqual(report["caseCount"], 19)
        self.assertEqual(report["matchedCount"], report["caseCount"])
        self.assertEqual(report["falsePositiveCaseIDs"], [])
        self.assertEqual(report["falseNegativeCaseIDs"], [])
        self.assertEqual(report["expectationMismatchCaseIDs"], [])

    def test_manifest_covers_all_probe_types(self):
        manifest = evaluator.load_manifest(MANIFEST)

        report = evaluator.evaluate_manifest(manifest, TOOL_ROOT)

        self.assertEqual(set(report["probeCoverage"]), {"recall", "artifact", "continuation", "decision"})

    def test_cost_fields_are_explicitly_proxy_only(self):
        manifest = evaluator.load_manifest(MANIFEST)

        report = evaluator.evaluate_manifest(manifest, TOOL_ROOT)

        self.assertEqual(report["tokenMetricStatus"], "proxy-only-not-comparable-to-provider-tokenizers")
        self.assertTrue(all(item["inputBytes"] > 0 for item in report["results"]))
        self.assertTrue(all(item["lexicalTokenProxy"] > 0 for item in report["results"]))

    def test_mutations_do_not_modify_the_base_fixture(self):
        before = json.loads((TOOL_ROOT / "fixtures" / "positive" / "minimal_core.v1.json").read_text())
        manifest = evaluator.load_manifest(MANIFEST)

        evaluator.evaluate_manifest(manifest, TOOL_ROOT)

        after = json.loads((TOOL_ROOT / "fixtures" / "positive" / "minimal_core.v1.json").read_text())
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
