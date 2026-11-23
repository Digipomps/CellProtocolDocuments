import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import haven_docs_mcp as mcp


class HavenDocsMCPTests(unittest.TestCase):
    def setUp(self):
        self.index = mcp.DocsIndex()

    def test_catalog_loads_book_docs_and_entrypoints(self):
        ids = {doc.doc_id for doc in self.index.docs}
        self.assertIn("book-15-documentation-discovery-rag", ids)
        self.assertIn("book-16-reference-workspace", ids)
        self.assertIn("repo-readme-cellprotocol", ids)

    def test_resources_include_catalog_and_read_book_doc(self):
        resources = self.index.resources()
        uris = {resource["uri"] for resource in resources}
        self.assertIn("haven-docs://catalog/book", uris)

        result = self.index.read_resource("haven-docs://book/book-15-documentation-discovery-rag")
        self.assertEqual(result["contents"][0]["mimeType"], "text/markdown")
        self.assertIn("Documentation Discovery and RAG", result["contents"][0]["text"])

    def test_read_specific_heading_anchor(self):
        result = self.index.read_section(
            "book-16-reference-workspace",
            anchor="rag-integration-contract",
        )
        self.assertEqual(result["citation"]["heading"], "9. RAG Integration Contract")
        self.assertIn("Required RAG behavior", result["text"])

    def test_search_returns_canonical_citations(self):
        result = self.index.search("RAG citations canonical Book paths", max_results=5)
        self.assertGreater(result["result_count"], 0)
        first = result["results"][0]["citation"]
        self.assertIn("path", first)
        self.assertTrue(first["path"].startswith("Book/") or first["path"].endswith(".md"))

    def test_unknown_resource_scheme_is_rejected(self):
        with self.assertRaises(mcp.DocsError):
            self.index.read_resource("file:///etc/passwd")

    def test_mcp_initialize_and_tool_call(self):
        server = mcp.MCPServer()
        initialize = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test"}},
            }
        )
        self.assertEqual(initialize["result"]["protocolVersion"], "2025-11-25")
        self.assertIn("resources", initialize["result"]["capabilities"])

        listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tool_names = {tool["name"] for tool in listed["result"]["tools"]}
        self.assertIn("haven_docs_search", tool_names)

        called = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "haven_docs_search",
                    "arguments": {"query": "Explore contracts", "max_results": 3},
                },
            }
        )
        self.assertFalse(called["result"]["isError"])
        self.assertGreater(called["result"]["structuredContent"]["result_count"], 0)

    def test_term_bridge_counts_norwegian_and_english_as_one_concept(self):
        concepts = dict(mcp.query_concepts({"avtale", "agreement"}))
        self.assertEqual(len(concepts), 1)
        words = next(iter(concepts))
        self.assertIn("avtale", words)
        self.assertIn("agreements", words)

    def test_norwegian_query_finds_english_chapter(self):
        result = self.index.search("avtaler og kontrakter", max_results=3)
        paths = [item["citation"]["path"] for item in result["results"]]
        self.assertIn("Book/04_Agreements_Contracts.md", paths)

    def test_student_questions_top5_floor(self):
        # test.egen-agent.docs-norsk: 13/31 uten begrepsbro, 19/31 med (2026-11-23). Gulvet hindrer tilbakegang.
        cases = json.loads((ROOT / "tests" / "fixtures" / "student-questions.v1.json").read_text(encoding="utf-8"))["cases"]
        hits = total = 0
        for case in cases:
            expected = set(case.get("expectedSources") or [])
            if not expected:
                continue
            total += 1
            result = self.index.search(case["question"], max_results=5)
            if {item["citation"]["path"] for item in result["results"]} & expected:
                hits += 1
        self.assertEqual(total, 31)
        self.assertGreaterEqual(hits, 19)

    def test_client_configs_start_this_server(self):
        # test.egen-agent.docs-config (filsiden): Claude Code og Codex peker på samme skrivebeskyttede server.
        import tomllib
        repo = ROOT.parents[1]
        claude = json.loads((repo / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["haven-docs"]
        with open(repo / ".codex" / "config.toml", "rb") as handle:
            codex = tomllib.load(handle)["mcp_servers"]["haven-docs"]
        for config in (claude, codex):
            self.assertEqual(config["command"], "python3")
            self.assertTrue((repo / config["args"][0]).is_file())
        self.assertIn("haven-docs", (repo / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual((repo / "CLAUDE.md").read_text(encoding="utf-8").strip(), "@AGENTS.md")

    def test_stdio_smoke_line_delimited_json(self):
        request = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {"name": "haven_docs_list", "arguments": {"status": "active"}},
        }
        server = mcp.MCPServer()
        response = server.handle(json.loads(json.dumps(request)))
        self.assertEqual(response["id"], 10)
        self.assertFalse(response["result"]["isError"])
        self.assertGreater(response["result"]["structuredContent"]["count"], 0)


if __name__ == "__main__":
    unittest.main()
