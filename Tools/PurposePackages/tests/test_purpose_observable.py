"""PDD formaal-som-gui-test, blad observable-goal: ordlisten er lukket og argumentene sjekkes."""
import json
from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from purpose_observable import VOCABULARY, validate_observable, validate_observables, describe
import purpose_dev


class ObservableVocabulary(unittest.TestCase):
    def test_vocabulary_is_the_six_words_kjetil_approved(self):
        self.assertEqual(sorted(VOCABULARY), sorted(["opensTab", "dispatches", "showsState", "insertsWidget", "navigatesTo", "changesState"]))

    def test_every_word_accepts_its_required_arguments(self):
        samples = {
            "opensTab": {"tab": "verktoy"},
            "dispatches": {"actionKeypath": "gameHelper.ask", "payloadShape": {"text": "string"}},
            "showsState": {"keypath": "gameHelper.helper.state.message"},
            "insertsWidget": {"widgetKind": "gamePreview"},
            "navigatesTo": {"configuration": "Spillverksted"},
            "changesState": {"keypath": "project.state.versions", "equals": "1"},
        }
        for kind, args in samples.items():
            with self.subTest(kind=kind):
                self.assertEqual(validate_observable({"kind": kind, **args}), [])

    def test_unknown_word_is_rejected(self):
        errors = validate_observable({"kind": "clicksButton", "label": "x"})
        self.assertEqual(len(errors), 1)
        self.assertIn("ukjent kind 'clicksButton'", errors[0])

    def test_missing_or_blank_required_argument_is_rejected(self):
        self.assertTrue(validate_observable({"kind": "opensTab"}))
        self.assertTrue(validate_observable({"kind": "opensTab", "tab": "  "}))
        self.assertTrue(validate_observable({"kind": "changesState", "keypath": ""}))

    def test_unknown_argument_is_rejected(self):
        errors = validate_observable({"kind": "opensTab", "tab": "verktoy", "selector": "#x"})
        self.assertEqual(len(errors), 1)
        self.assertIn("kjenner ikke argumentet 'selector'", errors[0])

    def test_payload_shape_types_are_closed(self):
        ok = validate_observable({"kind": "dispatches", "actionKeypath": "a.b", "payloadShape": {"text": "string", "n": "integer"}})
        self.assertEqual(ok, [])
        bad = validate_observable({"kind": "dispatches", "actionKeypath": "a.b", "payloadShape": {"text": "varchar"}})
        self.assertEqual(len(bad), 1)
        self.assertIn("ukjent type 'varchar'", bad[0])
        self.assertTrue(validate_observable({"kind": "dispatches", "actionKeypath": "a.b", "payloadShape": {}}))

    def test_observable_field_must_be_a_non_empty_list(self):
        self.assertEqual(validate_observables({}, "n"), [])
        self.assertTrue(validate_observables({"observable": []}, "n"))
        self.assertTrue(validate_observables({"observable": {"kind": "opensTab", "tab": "x"}}, "n"))
        self.assertEqual(validate_observables({"observable": [{"kind": "opensTab", "tab": "x"}]}, "n"), [])

    def test_describe_is_one_readable_line(self):
        self.assertEqual(describe({"kind": "opensTab", "tab": "verktoy"}), "opensTab(tab='verktoy')")


class ValidatorReadsObservable(unittest.TestCase):
    def test_validate_reports_observable_errors_in_packages_and_book(self):
        kb = {"nodes": [
            {"purposeRef": "purpose://t", "parentRef": None, "goal": {}},
            {"purposeRef": "purpose://t.a", "parentRef": "purpose://t", "observable": [{"kind": "flies"}]},
        ]}
        pk = {"packages": [{
            "packageRef": "pkg.t", "title": "t", "summary": "t", "status": "active", "triggers": {},
            "requiredArtifacts": [], "lessonRefs": [],
            "purposes": [{
                "purposeRef": "purpose://t.p", "parentRef": "purpose://t",
                "goal": {"goalRef": "g", "lifecycle": "c", "outcome": "o", "successSignals": ["s"], "verifier": "v"},
                "observable": [{"kind": "opensTab", "tab": "x"}],
                "derivedTests": [{"testRef": "test.t", "kind": "command", "description": "d", "how": "h", "evidence": "e",
                                  "observable": [{"kind": "showsState"}]}],
            }],
        }]}
        errors = purpose_dev.observable_errors(kb, pk)
        joined = "\n".join(errors)
        self.assertIn("purpose://t.a/observable[0]: ukjent kind 'flies'", joined)
        self.assertIn("pkg.t/purpose://t.p/test.t/observable[0]: showsState krever 'keypath'", joined)
        self.assertEqual(len(errors), 2, joined)

    def test_real_book_and_packages_validate(self):
        kb, pk, _ = purpose_dev.load_all()
        self.assertEqual(purpose_dev.observable_errors(kb, pk), [])


if __name__ == "__main__":
    unittest.main()
