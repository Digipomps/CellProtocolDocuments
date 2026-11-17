import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skeleton_explore_validator import collect_bindings

class LocalizationBindingsTests(unittest.TestCase):
    def test_only_root_localization_dependencies_enter_explore_validation(self):
        skeleton = {"VStack": [
            {"Text": {"text": "Count", "modifiers": {"localization": {"text": {
                "namespace": "demo", "key": "count", "arguments": {
                    "count": {"keypath": "alpha.count", "scope": "root"},
                    "row": {"keypath": "alpha.secret", "scope": "item"},
                    "context": {"keypath": "alpha.private", "scope": "context"},
                    "literal": {"value": 2}
                }}}}}},
            {"Text": {"text": "Label", "modifiers": {"localization": {"text": {"valueKeypath": "alpha.label", "scope": "root"}}}}}
        ]}
        bindings = []
        collect_bindings(skeleton, "$.skeleton", {"alpha": "cell:///Demo"}, "cell:///Porthole", bindings)
        self.assertEqual([(b.endpoint, b.key, b.method) for b in bindings], [
            ("cell:///Demo", "count", "get"), ("cell:///Demo", "label", "get")])
        self.assertEqual(bindings[1].expected_types, ["object"])

if __name__ == "__main__": unittest.main()
