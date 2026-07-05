#!/usr/bin/env python3
"""Extract real HAVEN graphs into a normalized edgelist format.

Produces one JSON per graph under Tools/ModelKnowledge/generated/graphs/:

    {
      "graphID": str,
      "kind": str,
      "directed": bool,
      "source": str,
      "nodes": [ {"id": str, "type": str}, ... ],
      "edges": [ {"u": str, "v": str, "type": str}, ... ]
    }

Content-blind: only structure and coarse types are kept, never node prose.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "Tools" / "ModelKnowledge" / "generated" / "graphs"


def write_graph(graph: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{graph['graphID']}.json"
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def extract_purpose_graph() -> dict:
    """Parse the Book 23 mermaid purpose tree into a directed graph."""
    text = (ROOT / "Book" / "23_Purpose_Knowledge_Base.md").read_text(encoding="utf-8")
    block = re.search(r"```mermaid(.*?)```", text, re.DOTALL)
    body = block.group(1) if block else ""

    # Map mermaid identifiers to purpose refs where a label is declared.
    label_re = re.compile(r'(\w+)\["purpose://([a-z0-9._-]+)')
    id_to_ref: dict[str, str] = {}
    for ident, ref in label_re.findall(body):
        id_to_ref[ident] = f"purpose://{ref}"

    edge_re = re.compile(r"(\w+)\s*-->\s*(\w+)")
    edges = []
    node_ids: set[str] = set()
    for src, dst in edge_re.findall(body):
        edges.append((src, dst))
        node_ids.add(src)
        node_ids.add(dst)

    def node_type(ident: str) -> str:
        ref = id_to_ref.get(ident, "")
        if ref == "purpose://root":
            return "root"
        # depth by dotted segments in the ref
        tail = ref.split("://", 1)[-1]
        return f"depth{tail.count('.') + 1}" if tail else "unknown"

    nodes = [{"id": id_to_ref.get(i, i), "type": node_type(i)} for i in sorted(node_ids)]
    edge_objs = [
        {"u": id_to_ref.get(s, s), "v": id_to_ref.get(d, d), "type": "parent-child"}
        for s, d in edges
    ]
    return {
        "graphID": "haven_purpose_graph",
        "kind": "purpose-tree",
        "directed": True,
        "source": "Book/23_Purpose_Knowledge_Base.md (mermaid)",
        "nodes": nodes,
        "edges": edge_objs,
    }


def extract_book_link_graph() -> dict:
    """Build the Book documentation cross-reference graph from markdown links."""
    book_dir = ROOT / "Book"
    files = sorted(p.name for p in book_dir.glob("*.md"))
    fileset = set(files)
    link_re = re.compile(r"\]\(([^)]+?\.md)(?:#[^)]*)?\)")
    edges = []
    for f in files:
        txt = (book_dir / f).read_text(encoding="utf-8")
        for target in link_re.findall(txt):
            name = target.split("/")[-1]
            if name in fileset and name != f:
                edges.append((f, name))

    def node_type(name: str) -> str:
        m = re.match(r"(\d+)_", name)
        if not m:
            return "meta"
        n = int(m.group(1))
        if n <= 8:
            return "core"
        if n <= 16:
            return "developer"
        return "extended"

    nodes = [{"id": f, "type": node_type(f)} for f in files]
    edge_objs = [{"u": u, "v": v, "type": "doc-link"} for u, v in edges]
    return {
        "graphID": "haven_book_link_graph",
        "kind": "documentation-link",
        "directed": True,
        "source": "Book/*.md (markdown cross-references)",
        "nodes": nodes,
        "edges": edge_objs,
    }


def extract_claim_source_graph() -> dict:
    """Bipartite claim<->source graph from a real candidate-claims corpus."""
    path = ROOT / "Tools" / "ConciergeKnowledge" / "sicilia_research" / "candidate_claims.jsonl"
    claims = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    nodes = []
    edges = []
    seen_sources: set[str] = set()
    for c in claims:
        cid = c["id"]
        nodes.append({"id": cid, "type": f"claim:{c.get('entity_kind', 'unknown')}"})
        for sid in c.get("source_ids", []):
            if sid not in seen_sources:
                seen_sources.add(sid)
                nodes.append({"id": sid, "type": "source"})
            edges.append({"u": cid, "v": sid, "type": "cites"})
        for tid in c.get("topic_ids", []):  # optional richer links if present
            edges.append({"u": cid, "v": tid, "type": "topic"})
    return {
        "graphID": "haven_claim_source_graph",
        "kind": "argument-claim",
        "directed": True,
        "source": "Tools/ConciergeKnowledge/sicilia_research/candidate_claims.jsonl",
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    for extractor in (extract_purpose_graph, extract_book_link_graph, extract_claim_source_graph):
        graph = extractor()
        out = write_graph(graph)
        print(f"{graph['graphID']}: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
