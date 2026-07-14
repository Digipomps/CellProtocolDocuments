import os
import sys
import tempfile
import unittest
from pathlib import Path


EXPLORE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPLORE_DIR))

from explore_contract_audit import (  # noqa: E402
    CONTRACT_NAMES,
    HANDLER_NAMES,
    analyze_repo,
    build_findings,
    has_explicit_shape,
)


class ExploreContractAuditTests(unittest.TestCase):
    def audit(self, files: dict[str, str]):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for relative, contents in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        analysis = analyze_repo(root, ["Sources/CellBase"])
        return analysis, build_findings(analysis)

    @staticmethod
    def contract(key: str = '"state"', method: str = ".get") -> str:
        return f"""
        await registerExploreContract(
            requester: owner,
            key: {key},
            method: {method},
            input: .null,
            returns: ExploreContract.schema(type: \"string\")
        )
        """

    def test_complete_helper_called_before_handler_covers_it(self):
        source = f"""
        final class DemoCell {{
            func setup() async {{
                await registerContracts()
                await registerGet(key: \"state\", owner: owner) {{ _ in .null }}
            }}
            func registerContracts() async {{ {self.contract()} }}
        }}
        """
        _analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        self.assertEqual(findings, [])

    def test_unused_helper_does_not_cover_handler(self):
        source = f"""
        final class DemoCell {{
            func setup() async {{
                await registerGet(key: \"state\", owner: owner) {{ _ in .null }}
            }}
            func registerContracts() async {{ {self.contract()} }}
        }}
        """
        _analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        self.assertEqual([finding.code for finding in findings], ["implicit_handler_contract"])

    def test_helper_called_after_handler_does_not_cover_it(self):
        source = f"""
        final class DemoCell {{
            func setup() async {{
                await registerGet(key: \"state\", owner: owner) {{ _ in .null }}
                await registerContracts()
            }}
            func registerContracts() async {{ {self.contract()} }}
        }}
        """
        _analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        self.assertEqual([finding.code for finding in findings], ["implicit_handler_contract"])

    def test_literal_string_loop_expands_contracts_and_handlers(self):
        source = f"""
        final class DemoCell {{
            func setup() async {{
                await registerContracts()
                for key in [\"one\", \"two\"] {{
                    await registerGet(key: key, owner: owner) {{ _ in .null }}
                }}
            }}
            func registerContracts() async {{
                for key in [\"one\", \"two\"] {{ {self.contract(key="key")} }}
            }}
        }}
        """
        analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        handlers = [call for call in analysis.calls if call.name in HANDLER_NAMES]
        contracts = [call for call in analysis.calls if call.name in CONTRACT_NAMES and has_explicit_shape(call)]
        self.assertEqual([call.key for call in handlers], ["one", "two"])
        self.assertEqual([call.key for call in contracts], ["one", "two"])
        self.assertEqual(findings, [])

    def test_literal_tuple_loop_expands_key_component(self):
        source = f"""
        final class DemoCell {{
            func setup() async {{
                await registerContracts()
                for (key, ignored) in [(\"one\", \"a\"), (\"two\", \"b\")] {{
                    await registerSet(key: key, owner: owner) {{ _, _ in .null }}
                }}
            }}
            func registerContracts() async {{
                for (key, ignored) in [(\"one\", \"a\"), (\"two\", \"b\")] {{
                    {self.contract(key="key", method=".set")}
                }}
            }}
        }}
        """
        analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        handlers = [call for call in analysis.calls if call.name in HANDLER_NAMES]
        self.assertEqual([call.key for call in handlers], ["one", "two"])
        self.assertEqual(findings, [])

    def test_computed_loop_remains_manual_review(self):
        source = f"""
        final class DemoCell {{
            func setup(keys: [String]) async {{
                await registerContracts(keys: keys)
                for key in keys {{
                    await registerGet(key: key, owner: owner) {{ _ in .null }}
                }}
            }}
            func registerContracts(keys: [String]) async {{
                for key in keys {{ {self.contract(key="key")} }}
            }}
        }}
        """
        _analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        self.assertEqual([finding.code for finding in findings], ["dynamic_key_needs_manual_review"])

    def test_same_key_contract_does_not_cross_cell_scope(self):
        source = f"""
        final class CellA {{
            func publish() async {{ {self.contract()} }}
        }}
        final class CellB {{
            func setup() async {{
                await registerGet(key: \"state\", owner: owner) {{ _ in .null }}
            }}
        }}
        """
        _analysis, findings = self.audit({"Sources/CellBase/TwoCells.swift": source})
        self.assertEqual([finding.cell_type for finding in findings], ["CellB"])

    def test_unknown_type_fallback_is_isolated_by_file(self):
        files = {
            "Sources/CellBase/A.swift": f"func publish() async {{ {self.contract()} }}",
            "Sources/CellBase/B.swift": """
                func setup() async {
                    await registerGet(key: "state", owner: owner) { _ in .null }
                }
            """,
        }
        _analysis, findings = self.audit(files)
        self.assertEqual(len(findings), 1)
        self.assertTrue(findings[0].file.endswith("B.swift"))

    def test_framework_declarations_and_forwarder_are_ignored(self):
        source = """
        open class GeneralCell {
            func registerExploreContract(key: String) async {
                await registerExploreSchema(requester: owner, key: key, schema: [:])
            }
            func registerExploreSchema(requester: Identity, key: String, schema: Object) async {}
            func registerGet(key: String, owner: Identity) async {}
            func registerIntercept(key: String) async {
                await addInterceptForGet(requester: owner, key: key) { _, _ in .null }
            }
        }
        """
        analysis, findings = self.audit({"Sources/CellBase/GeneralCell.swift": source})
        self.assertEqual(analysis.calls, [])
        self.assertEqual(findings, [])

    def test_typed_registration_covers_its_own_handler(self):
        source = """
        final class DemoCell {
            func setup() async {
                await registerSet(
                    key: "run",
                    owner: owner,
                    input: ExploreContract.schema(type: "object"),
                    returns: ExploreContract.schema(type: "string")
                ) { _, _ in .null }
            }
        }
        """
        _analysis, findings = self.audit({"Sources/CellBase/Demo.swift": source})
        self.assertEqual(findings, [])

    @unittest.skipUnless(os.environ.get("CELLPROTOCOL_REPO"), "CELLPROTOCOL_REPO is not set")
    def test_live_chat_has_56_handlers_and_56_complete_contracts(self):
        root = Path(os.environ["CELLPROTOCOL_REPO"]).resolve()
        analysis = analyze_repo(root, ["Sources/CellBase/Cells/Chat"])
        findings = build_findings(analysis)
        handlers = [call for call in analysis.calls if call.name in HANDLER_NAMES]
        contracts = [call for call in analysis.calls if call.name in CONTRACT_NAMES and has_explicit_shape(call)]
        self.assertEqual(len(handlers), 56)
        self.assertEqual(len(contracts), 56)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
