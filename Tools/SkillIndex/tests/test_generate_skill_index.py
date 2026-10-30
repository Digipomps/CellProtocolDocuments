from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generate_skill_index as gen


def make_skill(root: Path, name: str, description: str, body: str = "Innhold.\n", extra: dict | None = None):
    directory = root / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n{body}", encoding="utf-8")
    for rel, text in (extra or {}).items():
        target = directory / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


class IndexTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.a = self.tmp / "a"
        self.b = self.tmp / "b"

    def tearDown(self):
        self._tmp.cleanup()

    def build(self):
        return gen.build({"a": self.a, "b": self.b}, 8000)

    def test_drift_single_scope_and_counts(self):
        make_skill(self.a, "same", "Samme tekst. Mer.")
        make_skill(self.b, "same", "Samme tekst. Mer.")
        make_skill(self.a, "drifty", "Versjon en.")
        make_skill(self.b, "drifty", "Versjon to.")
        make_skill(self.a, "alone", "Bare her.")
        index = self.build()
        by_name = {s["name"]: s for s in index["skills"]}
        self.assertFalse(by_name["same"]["drift"])
        self.assertTrue(by_name["drifty"]["drift"])
        self.assertEqual(by_name["alone"]["scopes"], ["a"])
        self.assertEqual(index["counts"]["unique_names"], 3)
        self.assertEqual(index["counts"]["with_drift"], 1)
        self.assertEqual(index["counts"]["single_scope"], 1)

    def test_purpose_is_first_sentence_and_lengths_counted(self):
        make_skill(self.a, "x", "Første setning. Andre setning som er lengre.")
        entry = self.build()["skills"][0]
        self.assertEqual(entry["purpose"], "Første setning.")
        self.assertEqual(entry["desc_len"], len("Første setning. Andre setning som er lengre."))

    def test_problems_are_reported(self):
        make_skill(self.a, "ok", "Fin.")
        (self.a / "nofile").mkdir()
        bad = self.a / "badname"
        bad.mkdir()
        (bad / "SKILL.md").write_text("---\nname: annet\ndescription: x\n---\n", encoding="utf-8")
        nofront = self.a / "nofront"
        nofront.mkdir()
        (nofront / "SKILL.md").write_text("Ingen frontmatter.\n", encoding="utf-8")
        problems = {s["name"]: s["problems"] for s in self.build()["skills"]}
        self.assertEqual(problems["ok"], [])
        self.assertIn("mangler SKILL.md (a)", problems["nofile"])
        self.assertTrue(any("er ikke mappenavnet" in p for p in problems["badname"]))
        self.assertIn("mangler frontmatter (a)", problems["nofront"])

    def test_hardcoded_user_paths_and_references_counted(self):
        make_skill(self.a, "paths", "Beskrivelse.", body="Se /Users/noen/GitHub/x og /Users/noen/y.\n", extra={"references/r.md": "r"})
        entry = self.build()["skills"][0]
        self.assertEqual(entry["hardcoded_user_paths"], 2)
        self.assertEqual(entry["references"], 1)

    def test_combined_listing_counts_duplicates_twice(self):
        roots = {"user": self.a, "ws-x": self.b}
        make_skill(self.a, "dup", "Femten tegn..")
        make_skill(self.b, "dup", "Femten tegn..")
        index = gen.build(roots, 8000)
        self.assertEqual(index["listing_if_combined"]["user+ws-x"], 2 * len("Femten tegn.."))

    def test_overlap_finds_similar_descriptions(self):
        make_skill(self.a, "one", "Reviewing golden fixtures parity determinism policy cellprotocol runtime.")
        make_skill(self.a, "two", "Porting golden fixtures parity determinism policy cellprotocol runtime language.")
        make_skill(self.a, "far", "Baking sourdough bread recipes kitchen flour.")
        pairs = [(o["a"], o["b"]) for o in self.build()["overlap_candidates"]]
        self.assertIn(("one", "two"), pairs)
        self.assertFalse(any("far" in p for p in pairs))

    def test_output_is_deterministic_and_check_detects_drift(self):
        make_skill(self.a, "x", "Beskrivelse.")
        out = self.tmp / "out"
        self.assertEqual(gen.main(["--no-defaults", "--root", f"a={self.a}", "--out", str(out)]), 0)
        self.assertEqual(gen.main(["--no-defaults", "--root", f"a={self.a}", "--check", str(out)]), 0)
        make_skill(self.a, "y", "Ny skill.")
        self.assertEqual(gen.main(["--no-defaults", "--root", f"a={self.a}", "--check", str(out)]), 1)

    def test_skill_files_are_never_modified(self):
        make_skill(self.a, "x", "Beskrivelse.")
        before = (self.a / "x/SKILL.md").read_bytes()
        gen.main(["--no-defaults", "--root", f"a={self.a}", "--out", str(self.tmp / "out")])
        self.assertEqual((self.a / "x/SKILL.md").read_bytes(), before)

    def test_no_absolute_home_paths_in_output(self):
        make_skill(self.a, "x", "Beskrivelse.")
        index = self.build()
        text = json.dumps(index)
        self.assertNotIn(str(gen.HOME) + "/GitHub", text)


if __name__ == "__main__":
    unittest.main()
