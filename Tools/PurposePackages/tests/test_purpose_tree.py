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


def make_pdd(root, spec=SPEC, status="- G1: godkjent 2026-10-20\n- G1-GUI: venter\n", name="PDD_eksempel_2026-10-22"):
    taskdir = os.path.join(root, name)
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

    def test_a_purpose_without_parent_goes_under_its_ref_prefix_or_the_root(self):
        spec = SPEC.replace("| ex.read.mark | Merke avsnitt | ex.read |", "| ex.read.mark | Merke avsnitt | — |")
        spec = spec.replace("| **ex.read** | **Alle har boken** | ex.root |", "| **ex.read** | **Alle har boken** | — |")
        with tempfile.TemporaryDirectory() as tmp:
            tree, notes = pt.parse_spec_with_notes(make_pdd(tmp, spec), packages_path=os.devnull)
        by_ref = {n["ref"]: n for n in tree["nodes"]}
        self.assertEqual(tree["rootRef"], "purpose://candidate.eksempel.root")
        self.assertEqual(by_ref["purpose://candidate.eksempel.read"]["parentRef"], tree["rootRef"])
        self.assertEqual(by_ref["purpose://candidate.eksempel.read.mark"]["parentRef"],
                         "purpose://candidate.eksempel.read")
        self.assertTrue(any(n.startswith("ex.read:") and "under roten" in n for n in notes), notes)

    def test_headings_become_branches_when_a_table_has_no_parent_column(self):
        spec = """# Formålsspesifikasjon — nøkkel

## 1. Formålstre

### 1.0 Rot

| purposeRef | Tittel | Forelder |
|---|---|---|
| `purpose://candidate.nokkel.root` | Snever nøkkel | `purpose://access.audit.privacy` |

### 1.1 Gren 1 — Myndigheten er en celle

| purposeRef | Tittel | Goal (outcome) |
|---|---|---|
| `purpose://candidate.nokkel.grant-is-a-cell` | Grantene bor i en celle | Én celle |
| `purpose://candidate.nokkel.grant-is-owned` | Cellen er eid | Eid |
"""
        with tempfile.TemporaryDirectory() as tmp:
            tree, notes = pt.parse_spec_with_notes(make_pdd(tmp, spec, name="PDD_nokkel_2026-09-12"),
                                                   packages_path=os.devnull)
        by_ref = {n["ref"]: n for n in tree["nodes"]}
        branch = by_ref["purpose://candidate.nokkel.myndigheten-er-en-celle"]
        self.assertEqual(branch["title"], "Myndigheten er en celle")
        self.assertEqual(branch["parentRef"], tree["rootRef"])
        self.assertEqual(by_ref["purpose://candidate.nokkel.grant-is-owned"]["parentRef"], branch["ref"])
        self.assertEqual(tree["anchorRef"], "purpose://access.audit.privacy")
        self.assertIsNone(pt.validation_problem(tree))

    def test_parents_written_as_short_names_book23_refs_and_root_words(self):
        spec = """# Formålsspesifikasjon — kort

## §1 Formål med mål

| Kode | purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|---|
| R | `purpose://candidate.workbench-approvals.control` | Kontroll | — (under `purpose://human-agency`) | Styrer | T1 | candidate |
| A | `purpose://candidate.workbench-approvals.find` | Finn | control | Finner | T2 | candidate |
| B | `purpose://candidate.workbench-approvals.decide` | Avgjør | R | Avgjør | T3 | candidate |
| C | `purpose://candidate.workbench-approvals.privacy` | Personvern | purpose://access.audit.privacy | Ingen lekkasje | T4 | candidate |
| C | `purpose://candidate.workbench-approvals.privacy` | Dobbel rad | R | — | — | candidate |

## §1b Endringer

| purposeRef | Tittel | Forelder |
|---|---|---|
| purpose://candidate.workbench-approvals.ignored | Ikke med | R |
"""
        with tempfile.TemporaryDirectory() as tmp:
            tree, notes = pt.parse_spec_with_notes(make_pdd(tmp, spec, name="PDD_godkjenninger_2026-10-07"),
                                                   packages_path=os.devnull)
        by_ref = {n["ref"]: n for n in tree["nodes"]}
        root = "purpose://candidate.workbench-approvals.control"
        self.assertEqual(tree["rootRef"], root)
        self.assertEqual(tree["anchorRef"], "purpose://human-agency")
        self.assertEqual(by_ref["purpose://candidate.workbench-approvals.find"]["parentRef"], root)
        self.assertEqual(by_ref["purpose://candidate.workbench-approvals.decide"]["parentRef"], root)
        self.assertEqual(by_ref["purpose://candidate.workbench-approvals.privacy"]["parentRef"], root)
        self.assertIn("purpose://access.audit.privacy", by_ref["purpose://candidate.workbench-approvals.privacy"]["why"])
        self.assertNotIn("purpose://candidate.workbench-approvals.ignored", by_ref)
        self.assertEqual(len(tree["nodes"]), 4)
        self.assertTrue(any("access.audit.privacy" in n for n in notes), notes)
        self.assertTrue(any("mer enn én gang" in n for n in notes), notes)
        self.assertIsNone(pt.validation_problem(tree))

    def test_attached_packages_become_a_reused_branch_and_a_missing_root_is_made(self):
        registry = {"packages": [{"packageRef": "pkg.std.everything-works", "purposes": [
            {"purposeRef": "purpose://quality.build-and-regression", "title": "Bygger og bryter ingenting",
             "status": "candidate", "goal": {"outcome": "Alt bygger", "successSignals": ["0"], "verifier": "CI"}},
            {"purposeRef": "purpose://quality.work-is-visible", "title": "Arbeidet er synlig",
             "goal": {"outcome": "STATUS.md er ajour"}}]}]}
        spec = """# Formålsspesifikasjon — bibliotek

## 1. Formålstre

| purposeRef | Tittel | Forelder |
|---|---|---|
| purpose://quality.build-and-regression | Bygg | rot |
| purpose://candidate.bibliotek.restore | Gjenopprett | quality.build-and-regression |

## 4. Pakker

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke
    - purpose://quality.build-and-regression: Alt bygger.
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packages.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            tree, notes = pt.parse_spec_with_notes(make_pdd(tmp, spec, name="PDD_bibliotek_2026-10-07"),
                                                   packages_path=str(path))
        by_ref = {n["ref"]: n for n in tree["nodes"]}
        self.assertEqual(tree["rootRef"], "purpose://candidate.bibliotek.root")
        self.assertTrue(any("ingen rot" in n for n in notes), notes)
        self.assertEqual(by_ref["purpose://quality.build-and-regression"]["parentRef"], tree["rootRef"])
        self.assertEqual(by_ref["purpose://candidate.bibliotek.restore"]["parentRef"],
                         "purpose://quality.build-and-regression")
        branch = by_ref["purpose://candidate.bibliotek.pkg.std"]
        visible = by_ref["purpose://quality.work-is-visible"]
        self.assertEqual(visible["parentRef"], branch["ref"])
        self.assertEqual(visible["reused"], "purpose://quality.work-is-visible")
        self.assertEqual(visible["outcome"], "STATUS.md er ajour")
        self.assertIsNone(pt.validation_problem(tree))

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
