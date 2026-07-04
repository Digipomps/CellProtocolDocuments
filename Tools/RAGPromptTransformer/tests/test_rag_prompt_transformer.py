import json
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Tools" / "RAGPromptTransformer"))

import rag_prompt_transformer as transformer  # noqa: E402


FIXTURE = ROOT / "Tools" / "RAGPromptTransformer" / "fixtures" / "skeleton_rag_source_package.json"


class RAGPromptTransformerTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_transforms_rag_package_to_prompt_package(self):
        package = transformer.transform(self.load_fixture())

        self.assertIn(package["status"], {"ready", "ready_with_warnings"})
        self.assertEqual(package["promptPackageVersion"], 1)
        self.assertIn("GROUND TRUTH", package["userPrompt"])
        self.assertIn("Book/12_Skeleton_Spec.md:37-59", package["userPrompt"])
        self.assertIn("Book/22_Explore_Contracts_For_Skeleton_Authoring.md:251-301", package["userPrompt"])
        self.assertTrue(package["citationPolicy"]["required"])
        self.assertEqual(package["promptManifest"]["retentionClass"], "hash_only")
        self.assertRegex(package["promptManifest"]["promptHash"], r"^sha256:[0-9a-f]{64}$")

    def test_qwen_profile_adds_no_think(self):
        package = transformer.transform(self.load_fixture())

        self.assertTrue(package["userPrompt"].startswith("/no_think"))
        self.assertEqual(package["targetModel"]["family"], "qwen3")

    def test_gemma_profile_does_not_add_no_think(self):
        request = self.load_fixture()
        request["targetModel"]["modelID"] = "gemma4-e2b-qat-mlx"
        request["targetModel"]["family"] = "gemma4"

        package = transformer.transform(request)

        self.assertFalse(package["userPrompt"].startswith("/no_think"))
        self.assertEqual(package["targetModel"]["family"], "gemma4")

    def test_missing_topic_becomes_warning(self):
        request = self.load_fixture()
        request["constraints"]["mustCover"].append("calendar recurrence expansion")

        package = transformer.transform(request)

        self.assertIn("calendar recurrence expansion", " ".join(package["warnings"]))


if __name__ == "__main__":
    unittest.main()
