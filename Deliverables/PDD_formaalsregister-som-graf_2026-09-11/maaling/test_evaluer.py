"""Hand-computable measurement cases; no build or external dependencies."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import evaluer as e
from purpose_judgments import judge, validate_record


def lesson(ref, date="2026-09-01", source=""):
    return {"lessonRef": "lesson."+ref, "date": date, "source": source,
            "symptom": "en konkret feil med lesbar forklaring", "cause": "årsak",
            "prevention": "første avsnitt\n\nandre avsnitt", "tags": [], "purposeRefs": []}


def corpus():
    data = {"schema": "haven.matching-corpus.v1", "files": {},
            "lessons": [lesson("a"), lesson("b", "2026-09-02"), lesson("c")],
            "packages": {"packages": []}, "tasks": [
                {"taskRef": "PDD_test_2026-09-03", "date": "2026-09-03", "query": "intensjon",
                 "legacyQuery": "intensjon med senere tekst", "section4": "", "section5": "test.local",
                 "tags": [], "surfaces": []}]}
    data["snapshotHash"] = e.digest(data)
    return data


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.lessons = corpus()["lessons"]

    def test_known_metrics_and_short_output(self):
        s = e.score(["lesson.c", "lesson.a", "lesson.b"],
                    {"lesson.a": True, "lesson.b": True, "lesson.c": False}, self.lessons, 2)
        self.assertEqual((s["p_lo"], s["p_hi"], s["recall_known"], s["mrr_lo"]), (.5, .5, .5, .5))
        self.assertEqual((s["paragraphs"], s["noise_lo"], s["noise_hi"]), (6, 3, 3))
        s = e.score(["lesson.a"], {"lesson.a": True}, self.lessons, 2)
        self.assertEqual(s["p_hi"], .5)  # Missing slots do not improve precision.

    def test_unjudged_is_not_negative(self):
        s = e.score(["lesson.c", "lesson.a"], {"lesson.a": True}, self.lessons, 2)
        self.assertEqual((s["p_lo"], s["p_hi"], s["mrr_lo"], s["mrr_hi"]), (.5, 1, .5, 1))
        self.assertFalse(s["catalogue_judged"])

    def test_no_positive_is_not_zero_recall(self):
        s = e.score([], {}, self.lessons, 10)
        self.assertIsNone(s["recall_known"])
        self.assertEqual(s["p_lo"], 0)
        self.assertEqual(s["paragraphs"], 0)
        s = e.score(["lesson.a"], {x["lessonRef"]: False for x in self.lessons}, self.lessons, 1)
        self.assertEqual((s["mrr_lo"], s["mrr_hi"]), (0, 0))

    def test_mrr_distinguishes_budget_and_full_rank(self):
        s = e.score(["lesson.c", "lesson.a"], {"lesson.a": True}, self.lessons, 1)
        self.assertEqual((s["mrr_known"], s["mrr_at_k_known"]), (.5, 0))

    def test_paired_permutation_exact_and_zero(self):
        self.assertEqual(e.paired_stats([1]*4, 100)["p"], .125)
        self.assertEqual(e.paired_stats([1]*5, 100)["p"], .0625)
        self.assertEqual(e.paired_stats([1]*6, 100)["p"], .03125)
        self.assertEqual(e.paired_stats([0]*19, 100)["p"], 1)
        self.assertEqual(e.paired_stats([1, -1], 100)["p"], 1)
        self.assertIsNone(e.paired_stats([], 100)["ci95"])

    def test_same_task_denominator_for_all_candidates(self):
        d = corpus()
        report = e.evaluate({"a": lambda *_: [], "b": lambda *_: ["lesson.a"]}, d,
                            {d["tasks"][0]["taskRef"]: {"lesson.a": True}}, iterations=100)
        self.assertEqual(report["summaries"]["a"]["n_positive"], 1)
        self.assertEqual(report["summaries"]["b"]["n_positive"], 1)
        self.assertEqual(report["paired"][0]["n"], 1)


class EvidenceTests(unittest.TestCase):
    def test_section_does_not_leak_lookup_into_query(self):
        text = "## 0. Intensjon\nquery\n## 1. Tree\nno\n## 4. Lessons\n## auto heading\nyes\n## 5. Tests\nno"
        self.assertEqual(e.section(text, 0), "query")
        self.assertIn("yes", e.section(text, 4))
        self.assertNotIn("Tests", e.section(text, 4))

    def test_source_boundaries_and_auto_citations(self):
        d = corpus(); task = d["tasks"][0]
        d["lessons"][0]["source"] = "Deliverables/"+task["taskRef"]+"/STATUS.md"
        d["lessons"][1]["source"] = "Deliverables/"+task["taskRef"]+"-other/STATUS.md"
        task["section4"] = "## Lærdommer du må lese før dekomponering\nlesson.b lesson.missing"
        r = e.retrospective(d)
        self.assertEqual(len(r["unknownSection4Refs"]), 1)
        self.assertEqual(e.truth_labels(d, "source")[task["taskRef"]], {"lesson.a": True})
        self.assertEqual(e.truth_labels(d, "curated")[task["taskRef"]], {"lesson.a": True})

    def test_overlap_is_evidence_only(self):
        l = lesson("x")
        self.assertEqual(e.overlap(l, l["symptom"]+" "+l["prevention"]), 1)
        self.assertEqual(e.overlap(l, "helt annerledes"), 0)

    def test_date_filter_excludes_same_day_and_later(self):
        d = corpus(); d["lessons"][0]["date"] = "2026-09-03"
        d["lessons"][1]["date"] = "2026-09-04"
        self.assertEqual([l["lessonRef"] for l in e.available_lessons(d, d["tasks"][0], True)], ["lesson.c"])

    def test_hash_and_subset(self):
        d = corpus(); e.validate_snapshot(d)
        short = e.subset(d, ["lesson.c"])
        e.validate_snapshot(short)
        self.assertEqual(len(short["lessons"]), 2)
        self.assertNotEqual(short["snapshotHash"], d["snapshotHash"])
        d["lessons"][0]["symptom"] = "modified"
        with self.assertRaises(ValueError):
            e.validate_snapshot(d)

    def test_function_contract_and_isolation(self):
        d = corpus()
        def fn(query, lessons, context):
            self.assertEqual(query, "intensjon")
            self.assertNotIn("source", lessons[0])
            self.assertNotIn("taskRef", context)
            context["tags"].append("mutation")
            return ["lesson.a"]
        e.run_matcher(fn, d, d["tasks"][0])
        self.assertEqual(d["tasks"][0]["tags"], [])
        for output in (["lesson.a", "lesson.a"], ["lesson.unknown"], [1]):
            with self.assertRaises(ValueError):
                e.run_matcher(lambda *_: output, d, d["tasks"][0])


class HumanTests(unittest.TestCase):
    def record(self):
        d = corpus()
        r = e.pool(d, d["tasks"][0]["taskRef"], {"x": lambda *_: ["lesson.a", "lesson.b"]}, 2, 1)
        r["presented"] = ["lesson.a", "lesson.b"]
        return d, r

    def test_schema_rejects_missing_boolean_ambiguous_enforcement_and_ref(self):
        _, r = self.record()
        for row in [
            {"lessonRef": "lesson.a", "relevant": None, "repeatOf": None},
            {"lessonRef": "lesson.a", "relevant": True, "repeatOf": None},
            {"lessonRef": "lesson.a", "relevant": True, "repeatOf": None, "preventedBy": "test.local", "unenforced": {"reason": "why"}},
            {"lessonRef": "lesson.a", "relevant": True, "repeatOf": None, "unenforced": {"reason": " "}},
            {"lessonRef": "lesson.a", "relevant": True, "repeatOf": None, "preventedBy": "test.unknown"},
            {"lessonRef": "lesson.a", "relevant": False, "repeatOf": "lesson.b"},
        ]:
            r["judgments"] = [row]
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_record(r)

    def test_interactive_resume_boolean_false_and_repeat(self):
        d, r = self.record()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            task = Path(temp)/r["taskRef"]; task.mkdir()
            run = Path(temp)/"run.json"; e.write_json(run, r)
            answers = iter(["1 ?2", "-", "u:mangler-test"])
            self.assertEqual(judge(task, run, input_fn=lambda _: next(answers)), 0)
            stored = e.read_json(task/"MATCHING_FASIT.json")
            self.assertEqual(len(stored["judgments"]), 1)
            answers = iter(["-", "1=lesson.a"])
            self.assertEqual(judge(task, input_fn=lambda _: next(answers)), 0)
            stored = validate_record(e.read_json(task/"MATCHING_FASIT.json"))
            self.assertEqual(stored["judgments"][1], {"lessonRef": "lesson.b", "relevant": False, "repeatOf": "lesson.a"})
            truth = e.truth_labels(d, "human", [task/"MATCHING_FASIT.json"])
            self.assertEqual(truth[r["taskRef"]], {"lesson.a": True, "lesson.b": False})

    def test_abort_does_not_create_human_labels(self):
        _, r = self.record()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            task = Path(temp)/r["taskRef"]; task.mkdir()
            run = Path(temp)/"run.json"; e.write_json(run, r)
            def eof(_):
                raise EOFError
            self.assertEqual(judge(task, run, input_fn=eof), 1)
            self.assertFalse((task/"MATCHING_FASIT.json").exists())

    def test_real_cli_subcommand(self):
        _, r = self.record()
        with tempfile.TemporaryDirectory() as temp:
            task = Path(temp)/r["taskRef"]; task.mkdir()
            run = Path(temp)/"run.json"; e.write_json(run, r)
            result = subprocess.run([sys.executable, str(e.REPO/"Tools/PurposePackages/purpose_dev.py"),
                                     "judge", str(task), "--run", str(run)], input="1\n-\n1=test.local\n",
                                    text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr+result.stdout)
            self.assertEqual(e.read_json(task/"MATCHING_FASIT.json")["judgments"][0]["preventedBy"], "test.local")

    def test_snapshot_mismatch_rejected(self):
        d, r = self.record(); r["corpusHash"] = "0"*64
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"r.json"; e.write_json(path, r)
            with self.assertRaises(ValueError):
                e.truth_labels(d, "human", [path])

    def test_empty_or_fully_unjudged_runs_do_not_drop_hard_tasks(self):
        d, r = self.record()
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
            task = Path(temp)/r["taskRef"]; task.mkdir()
            path = Path(temp)/"r.json"; e.write_json(path, r)
            self.assertEqual(e.truth_labels(d, "human", [path]), {r["taskRef"]: {}})
            r["presented"] = []; r["rankings"] = {"x": []}; e.write_json(path, r)
            self.assertEqual(judge(task, path), 0)
            self.assertTrue((task/"MATCHING_FASIT.json").exists())

    def test_new_tasks_do_not_invalidate_old_judgments_but_query_edits_do(self):
        d, r = self.record()
        r["judgments"] = [{"lessonRef": "lesson.a", "relevant": False, "repeatOf": None}]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"r.json"; e.write_json(path, r)
            added = copy.deepcopy(d["tasks"][0]); added["taskRef"] = "PDD_other_2026-09-03"
            d["tasks"].append(added); d["snapshotHash"] = "a"*64
            self.assertEqual(len(e.truth_labels(d, "human", [path])), 1)
            d["tasks"][0]["query"] = "new intent"
            with self.assertRaises(ValueError):
                e.truth_labels(d, "human", [path])


class ExistingMatcherTests(unittest.TestCase):
    def test_adapter_matches_original_spike_on_frozen_inputs(self):
        data = e.read_json(e.HERE/"korpus_44.json")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/"Book").mkdir()
            e.write_json(root/"Book/haven_lessons_register_v0.json", {"lessons": data["lessons"]})
            for task in data["tasks"]:
                folder = root/"Deliverables"/task["taskRef"]; folder.mkdir(parents=True)
                (folder/"FORMAALSSPEC.md").write_text("## 0. Intensjon\n"+task["legacyQuery"])
            # Run the unmodified original script with the frozen corpus.
            code = "import runpy,json; d=runpy.run_path("+repr(str(e.HERE/"spike_tfidf_baseline.py"))+"); print(json.dumps({name:[r for _,r in sorted(((d['cos'](qv,v),r) for r,v in d['V'].items()),reverse=True)] for name,qv in d['q']}))"
            run = subprocess.run([sys.executable, "-c", code], cwd=root, capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            expected = json.loads(run.stdout.splitlines()[-1])
            for task in data["tasks"]:
                self.assertEqual(e.run_matcher(e.tfidf_matcher, data, task, legacy=True), expected[task["taskRef"]])


if __name__ == "__main__":
    unittest.main()
