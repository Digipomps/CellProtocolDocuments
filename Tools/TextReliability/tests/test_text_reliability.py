import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import text_reliability as tr


class TextReliabilityTests(unittest.TestCase):
    def test_claims_are_exactly_anchored(self):
        text = "Dette vil redusere kostnaden med 20 prosent. Derfor bør piloten starte."
        inputs = [
            {
                "input_id": "manual-1",
                "title": "Manual",
                "text": text,
                "metadata": {},
            }
        ]
        analysis = tr.analyze(inputs)
        self.assertGreaterEqual(len(analysis["claim_ledger"]), 2)
        for claim in analysis["claim_ledger"]:
            self.assertEqual(text[claim["char_start"] : claim["char_end"]], claim["quote"])
            self.assertFalse(claim["is_inferred"])

    def test_missing_sources_are_not_claimed_supported(self):
        text = "Prosjektet vil redusere ventetiden med 40 prosent."
        analysis = tr.analyze([
            {"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}
        ])
        statuses = {check["status"] for check in analysis["source_checks"]}
        self.assertEqual(statuses, {"source_missing"})
        ratings = {item["dimension"]: item["rating"] for item in analysis["reliability_dimensions"]}
        self.assertEqual(ratings["source_grounding"], "weak")

    def test_url_sources_are_not_checkable_until_audited(self):
        text = "Ifølge https://example.com/report har tiltaket redusert ventetiden med 25 prosent."
        analysis = tr.analyze([
            {"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}
        ])
        self.assertEqual(analysis["source_checks"][0]["status"], "not_checkable")
        self.assertEqual(analysis["source_checks"][0]["source_audit_status"], "needs_external_source_audit")
        self.assertEqual(analysis["claim_ledger"][0]["source_audit_status"], "needs_external_source_audit")
        self.assertEqual(analysis["claim_ledger"][0]["source_refs"][0]["kind"], "url")

    def test_markdown_tables_are_parsed_as_structure_and_row_claims(self):
        text = """# Analyse

| Påstand | Belegg |
| --- | --- |
| Eksporten skal øke 50 prosent. | https://example.com/export |
| Produktiviteten bør øke 0,5 prosentpoeng. | Må kildeauditeres |
"""
        analysis = tr.analyze([
            {"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}
        ])
        self.assertEqual(len(analysis["markdown_structure"]["tables"]), 1)
        table_claims = [claim for claim in analysis["claim_ledger"] if claim.get("origin") == "markdown_table_row"]
        self.assertEqual(len(table_claims), 2)
        quotes = [claim["quote"] for claim in table_claims]
        self.assertFalse(any("---" in quote for quote in quotes))
        for claim in table_claims:
            self.assertEqual(text[claim["char_start"] : claim["char_end"]], claim["quote"])

    def test_claim_clusters_source_matrix_and_argument_graph_are_emitted(self):
        text = "# Kort svar\n\nDerfor bør tiltaket starte. Belegget mangler foreløpig."
        analysis = tr.analyze([
            {"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}
        ])
        self.assertGreaterEqual(len(analysis["claim_clusters"]), 1)
        self.assertEqual(len(analysis["claim_source_matrix"]), len(analysis["claim_ledger"]))
        self.assertIn("argument_graph", analysis)
        self.assertIn("mermaid", analysis["argument_graph"])

    def test_productivity_model_uses_compound_delta(self):
        text = "Produktivitetsbidrag i Fastlands-BNP bør modelleres."
        analysis = tr.analyze(
            [{"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}],
            policy={
                "productivity_model": {
                    "base_gdp_bn": 4423,
                    "years": 10,
                    "productivity_deltas_pp": [0.3, 0.5],
                    "fiscal_gap_share_pct": 6.2,
                }
            },
        )
        model = analysis["quantitative_models"][0]
        self.assertEqual(model["base_gdp_bn"], 4423)
        self.assertEqual(model["fiscal_gap_equivalent_bn"], 274.226)
        scenario_by_delta = {scenario["delta_pp"]: scenario for scenario in model["scenarios"]}
        self.assertAlmostEqual(scenario_by_delta[0.3]["additional_level_bn"], 134.496, places=3)
        self.assertAlmostEqual(scenario_by_delta[0.5]["additional_level_bn"], 226.193, places=3)

    def test_rhetoric_detection_flags_certainty_pressure(self):
        text = "Alle vet at dagens politikk aldri fungerer. Derfor må kommunen bytte strategi."
        analysis = tr.analyze([
            {"input_id": "manual-1", "title": "Manual", "text": text, "metadata": {}}
        ])
        types = {finding["rhetoric_type"] for finding in analysis["rhetoric_findings"]}
        self.assertIn("certainty_inflation", types)

    def test_add2entity_capture_produces_sidecar_without_entity_mutation(self):
        capture = json.loads((ROOT / "fixtures" / "add2entity_capture.json").read_text(encoding="utf-8"))
        inputs = [tr.input_from_add2entity_capture(capture)]
        analysis = tr.analyze(inputs, add2entity_capture=capture)
        self.assertIn("add2entity_sidecar", analysis)
        sidecar = analysis["add2entity_sidecar"]
        self.assertEqual(sidecar["schema"], tr.ADD2ENTITY_SIDECAR_SCHEMA)
        self.assertFalse(sidecar["mutatesEntity"])
        self.assertEqual(sidecar["captureID"], capture["captureID"])
        self.assertEqual(sidecar["target"]["projectID"], "project-demo")


if __name__ == "__main__":
    unittest.main()
