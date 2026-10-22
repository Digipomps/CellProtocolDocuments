"""purpose_dev.py tree/treediff: FORMAALSSPEC §1 → tree.json for PurposeReview, og tilbake."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import purpose_tree as pt

SPEC = """# Formålsspesifikasjon — eksempel

## 0. Intensjon

Tekst.

## 1. Formålstre

Rot og forankring: roten festes under `purpose://human-agency` i Book 23.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| **ex.root** `purpose://candidate.eksempel.root` | **Roten** | purpose://human-agency (felles lesing) | Fem har lest | T-R | candidate |
| **ex.read** | **Alle har boken** | ex.root | Hver kan åpne boken | T-A | candidate |
| ex.read.share `…read.share-link` | Deles med lenke | ex.read | Lenken virker | T-A1 | candidate |
| ex.read.mark | Merke avsnitt | ex.read | Et merket avsnitt kan
| siteres | T-A2 | candidate |
| test.read.mark | ex.read.mark | Testrad som har havnet her | TESTRESULT.md | venter |

| Test | purposeRef | Hva |
|---|---|---|
| test.read.share | purpose://candidate.eksempel.read.share-link | Playwright |

## 2. Avgrensning
"""


def make_pdd(root, spec=SPEC, status="- G1: godkjent 2026-10-20\n- G1-GUI: venter\n"):
    taskdir = os.path.join(root, "PDD_eksempel_2026-10-22")
    os.makedirs(taskdir)
    Path(taskdir, "FORMAALSSPEC.md").write_text(spec, encoding="utf-8")
    Path(taskdir, "STATUS.md").write_text(status, encoding="utf-8")
    return taskdir


class PurposeTreeTests(unittest.TestCase):
    def test_section_one_becomes_a_valid_review_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            tree, notes = pt.parse_spec_with_notes(make_pdd(tmp))
        self.assertEqual(tree["id"], "eksempel-2026-10-22")
        self.assertEqual(tree["pdd"], "PDD_eksempel_2026-10-22")
        self.assertEqual(tree["gate"], "G1-GUI")
        self.assertEqual(tree["title"], "eksempel")
        self.assertEqual(tree["anchorRef"], "purpose://human-agency")
        self.assertEqual(tree["anchorNote"], "felles lesing")
        self.assertEqual(tree["rootRef"], "purpose://candidate.eksempel.root")
        refs = {n["code"]: n["ref"] for n in tree["nodes"]}
        self.assertEqual(refs, {
            "ex.root": "purpose://candidate.eksempel.root",
            "ex.read": "purpose://candidate.eksempel.read",
            "ex.read.share": "purpose://candidate.eksempel.read.share-link",
            "ex.read.mark": "purpose://candidate.eksempel.read.mark",
        })
        mark = next(n for n in tree["nodes"] if n["code"] == "ex.read.mark")
        self.assertEqual(mark["parentRef"], "purpose://candidate.eksempel.read")
        self.assertEqual(mark["outcome"], "Et merket avsnitt kan siteres")
        self.assertEqual(mark["verifier"], "T-A2")
        self.assertEqual(mark["status"], "candidate")
        self.assertEqual(notes, ["hoppet over testraden «test.read.mark» i formålstabellen"])
        self.assertNotIn("skippedRows", tree)
        self.assertIsNone(pt.validation_problem(tree))

    def test_validation_matches_the_cell(self):
        node = lambda ref, parent: {"ref": ref, "parentRef": parent, "title": ref}
        base = {"id": "t", "title": "T", "rootRef": "purpose://r"}
        cases = [
            [node("purpose://r", None), node("purpose://a", "purpose://missing")],
            [node("purpose://r", None), node("purpose://r", None)],
            [node("purpose://r", None), node("purpose://a", "purpose://b"), node("purpose://b", "purpose://a")],
            [node("r", None)],
        ]
        for nodes in cases:
            self.assertIsNotNone(pt.validation_problem(dict(base, nodes=nodes)), nodes)
        self.assertIsNone(pt.validation_problem(dict(base, nodes=[node("purpose://r", None), node("purpose://a", "purpose://r")])))

    def test_two_roots_are_refused(self):
        spec = SPEC.replace("| ex.read.mark | Merke avsnitt | ex.read |", "| ex.read.mark | Merke avsnitt | — |")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                pt.parse_spec(make_pdd(tmp, spec))

    def test_write_tree_and_diff_against_a_workbench_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            taskdir = make_pdd(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(pt.write_tree(taskdir), 0)
            path = Path(taskdir, "formaalsside", "tree.json")
            tree = json.loads(path.read_text(encoding="utf-8"))
            # Slik Workbench gir det tilbake etter redigering: én endret, én fjernet, én lagt til.
            tree["revision"] = 3
            tree["nodes"] = [n for n in tree["nodes"] if n["code"] != "ex.read.mark"]
            tree["nodes"][1]["title"] = "Alle har boken på telefonen"
            tree["nodes"].append({"ref": "purpose://candidate.eksempel-2026-10-22.boken-kan-lanes-ut",
                                  "parentRef": "purpose://candidate.eksempel.read", "title": "Boken kan lånes ut",
                                  "status": "candidate"})
            exported = Path(tmp, "export.json")
            exported.write_text(json.dumps({"selected": {"id": tree["id"], "revision": 3, "tree": tree}}), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(pt.diff_command(taskdir, str(exported)), 0)
        text = out.getvalue()
        self.assertIn("Revisjon i Workbench: 3", text)
        self.assertIn("## Lagt til", text)
        self.assertIn("boken-kan-lanes-ut", text)
        self.assertIn("## Fjernet", text)
        self.assertIn("purpose://candidate.eksempel.read.mark", text)
        self.assertIn('title: "Alle har boken" → "Alle har boken på telefonen"', text)

    def test_unchanged_export_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            taskdir = make_pdd(tmp)
            tree = pt.parse_spec(taskdir)
            self.assertIn("Ingen endringer", pt.render_diff(tree, tree))


if __name__ == "__main__":
    unittest.main()
