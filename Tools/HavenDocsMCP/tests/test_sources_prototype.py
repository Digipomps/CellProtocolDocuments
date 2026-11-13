"""Tester for forslaget om ekstra kilder, implementation_status og ferskhet (prototype).

Bruker midlertidige git-repoer; rører aldri CellProtocol eller andre ekte repoer.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import haven_docs_mcp as mcp
import haven_docs_sources as sources


def run_git(cwd, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class SourcesFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.upstream = self.tmp / "upstream"
        write(self.upstream / "Docs/spec.md", "# Spec\n\nDette er beskrevet.\n")
        run_git(self.tmp, "init", "-b", "main", str(self.upstream))
        run_git(self.upstream, "add", ".")
        run_git(self.upstream, "commit", "-m", "first")
        self.clone = self.tmp / "clone"
        run_git(self.tmp, "clone", str(self.upstream), str(self.clone))
        sources._freshness_cache.clear()
        sources._provenance_cache.clear()

    def tearDown(self):
        self._tmp.cleanup()

    def config(self, **overrides):
        source = {
            "id": "fx",
            "repo": "clone",
            "root": str(self.clone),
            "group": "fixture",
            "include": ["Docs/**/*.md", "Docs/**/*.schema.json"],
        }
        return {
            "sources": [source],
            "exclude_global": ["**/haven-correspondence/**", "**/*.eml"],
            "status_overrides": overrides.get("status_overrides", []),
        }


class DiscoveryTests(SourcesFixture):
    def test_correspondence_and_index_false_stay_out(self):
        write(self.clone / "Docs/haven-correspondence/message.md", "# Melding\n\nFra Kjetil.\n")
        write(self.clone / "Docs/mail.eml", "From: x")
        write(self.clone / "Docs/private.md", "---\nindex: false\n---\n# Privat\n")
        write(self.clone / "Docs/ok.md", "# OK\n\ntekst\n")
        docs, reports = sources.discover_docs(self.config(), ROOT)
        paths = {doc["path"] for doc in docs}
        self.assertIn("Docs/ok.md", paths)
        self.assertNotIn("Docs/haven-correspondence/message.md", paths)
        self.assertNotIn("Docs/private.md", paths)
        self.assertEqual(reports[0]["skipped"].get("index=false"), 1)

    def test_missing_root_is_reported_not_silent(self):
        config = self.config()
        config["sources"][0]["root"] = str(self.tmp / "finnes-ikke")
        docs, reports = sources.discover_docs(config, ROOT)
        self.assertEqual(docs, [])
        self.assertIn("error", reports[0])

    def test_frontmatter_beats_override_and_invalid_becomes_unknown(self):
        write(self.clone / "Docs/a.md", "---\nimplementation_status: implemented\nstatus_basis: code-verified\n---\n# A\n")
        write(self.clone / "Docs/b.md", "---\nimplementation_status: ferdig\n---\n# B\n")
        overrides = [{"source": "fx", "paths": ["Docs/a.md", "Docs/spec.md"], "implementation_status": "decided", "status_basis": "doc-self-declared"}]
        docs, _ = sources.discover_docs(self.config(status_overrides=overrides), ROOT)
        by_path = {doc["path"]: doc for doc in docs}
        self.assertEqual(by_path["Docs/a.md"]["implementation_status"], "implemented")
        self.assertEqual(by_path["Docs/a.md"]["status_basis"], "code-verified")
        self.assertEqual(by_path["Docs/b.md"]["implementation_status"], "unknown")
        self.assertEqual(by_path["Docs/spec.md"]["implementation_status"], "decided")


class IndexTests(SourcesFixture):
    def test_default_index_is_unchanged_by_prototype(self):
        index = mcp.DocsIndex(with_sources=False)
        self.assertEqual(index.source_ids, set())
        result = index.search("Documentation Discovery", max_results=2)
        self.assertNotIn("freshness", result)

    def test_external_doc_search_carries_label_provenance_and_freshness(self):
        write(self.clone / "Docs/model.schema.json", json.dumps({"title": "Modell v2", "type": "object"}))
        run_git(self.clone, "add", ".")
        run_git(self.clone, "commit", "-m", "schema")
        overrides = [{"source": "fx", "paths": ["Docs/model.schema.json"], "implementation_status": "decided", "status_basis": "doc-self-declared"}]
        index = mcp.DocsIndex(with_sources=True, sources_config=self.config(status_overrides=overrides))
        result = index.search("Modell v2", source="fx")
        first = result["results"][0]
        self.assertEqual(first["citation"]["implementation_status"], "decided")
        self.assertEqual(first["citation"]["source"], "fx")
        self.assertEqual(len(first["provenance"]["commit"]), 40)
        self.assertFalse(first["provenance"]["dirty"])
        self.assertEqual(result["freshness"][0]["behind"], 0)
        self.assertIn("[decided]", mcp.format_search_text(result))
        self.assertIn("Ferskhet:", mcp.format_search_text(result))
        # Fil uten overskrifter (JSON-skjema) må kunne finnes.
        self.assertEqual(first["citation"]["path"], "Docs/model.schema.json")

    def test_filter_on_implementation_status(self):
        write(self.clone / "Docs/plan.md", "---\nimplementation_status: proposal\n---\n# Plan\n\nforslag om tokens\n")
        index = mcp.DocsIndex(with_sources=True, sources_config=self.config())
        hits = index.search("tokens", implementation_status="proposal")
        self.assertEqual(hits["result_count"], 1)
        self.assertEqual(index.search("tokens", implementation_status="implemented")["result_count"], 0)

    def test_resource_uri_roundtrip_for_external_source(self):
        index = mcp.DocsIndex(with_sources=True, sources_config=self.config())
        doc = index.resolve_doc("fx/Docs/spec.md")
        self.assertEqual(doc.uri, "haven-docs://fx/Docs/spec.md")
        read = index.read_resource(doc.uri)
        self.assertIn("Dette er beskrevet", read["contents"][0]["text"])

    def test_section_marker_overrides_and_is_inherited(self):
        write(
            self.clone / "Docs/mix.md",
            "---\nimplementation_status: implemented\n---\n# Mix\n\n## Virker\n\nok\n\n"
            "## Besluttet\n<!-- haven:implementation_status=decided -->\n\ntekst\n\n### Detalj\n\nmer\n\n## Etter\n\nigjen\n",
        )
        index = mcp.DocsIndex(with_sources=True, sources_config=self.config())
        doc = index.resolve_doc("fx/Docs/mix.md")
        status = {s.heading: s.effective_implementation_status for s in index.sections(doc) if s.level}
        self.assertEqual(status["Virker"], "implemented")
        self.assertEqual(status["Besluttet"], "decided")
        self.assertEqual(status["Detalj"], "decided")
        self.assertEqual(status["Etter"], "implemented")

    def test_lint_flags_implemented_label_with_not_implemented_text(self):
        write(self.clone / "Docs/c.md", "---\nimplementation_status: implemented\n---\n# C\n\nDette er ikke implementert ennå.\n")
        index = mcp.DocsIndex(with_sources=True, sources_config=self.config())
        report = sources.lint(index)
        self.assertEqual(report["conflicts_label_says_implemented_text_says_not"][0]["doc_id"], "fx/Docs/c.md")


class FreshnessTests(SourcesFixture):
    def test_behind_after_fetch_and_unfetched_commits_via_remote_check(self):
        write(self.upstream / "Docs/new.md", "# Ny\n")
        run_git(self.upstream, "add", ".")
        run_git(self.upstream, "commit", "-m", "second")

        # Før fetch ser klonen ingenting; --check-remote avslører det uten å endre klonen.
        local_only = sources.freshness(self.clone, label="fx")
        self.assertEqual(local_only["behind"], 0)
        checked = sources.freshness(self.clone, label="fx", check_remote=True)
        self.assertTrue(checked["remote_has_unfetched_commits"])
        self.assertTrue(any("ikke er hentet" in w for w in checked["warnings"]))
        self.assertIn("ikke er hentet", checked["summary"])

        run_git(self.clone, "fetch")
        sources._freshness_cache.clear()
        after = sources.freshness(self.clone, label="fx")
        self.assertEqual(after["behind"], 1)
        self.assertIn("1 commits bak origin/main", after["summary"])

    def test_branch_other_than_main_is_called_out(self):
        run_git(self.clone, "checkout", "-b", "feature/x")
        info = sources.freshness(self.clone, label="fx")
        self.assertTrue(any("feature/x" in w for w in info["warnings"]))

    def test_dirty_file_is_flagged_in_provenance(self):
        write(self.clone / "Docs/spec.md", "# Spec\n\nendret lokalt\n")
        self.assertTrue(sources.provenance(self.clone, "Docs/spec.md")["dirty"])


if __name__ == "__main__":
    unittest.main()
