#!/usr/bin/env python3
"""Build a lightweight JSONL corpus for model/provider knowledge.

This is an interim RAG seed. It avoids dependencies and does not create
embeddings. The output is safe to commit because it contains only selected
source text and metadata, never API keys.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "Tools" / "ModelKnowledge" / "model_knowledge_sources.json"
DEFAULT_OUT = ROOT / "Tools" / "ModelKnowledge" / "generated" / "model_knowledge_corpus.jsonl"


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def markdown_chunks(text: str, max_chars: int) -> list[tuple[str, str]]:
    lines = clean_text(text).splitlines()
    chunks: list[tuple[str, str]] = []
    heading = "Document"
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        body = "\n".join(current).strip()
        if body:
            chunks.extend(split_large(heading, body, max_chars))
        current = []

    for line in lines:
        if line.startswith("#"):
            flush()
            heading = line.lstrip("#").strip() or heading
            current.append(line)
        else:
            current.append(line)
    flush()
    return chunks


def split_large(heading: str, text: str, max_chars: int) -> list[tuple[str, str]]:
    if len(text) <= max_chars:
        return [(heading, text)]
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if current and current_len + len(paragraph) + 2 > max_chars:
            chunks.append((heading, "\n\n".join(current)))
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph) + 2
    if current:
        chunks.append((heading, "\n\n".join(current)))
    return chunks


def json_chunks(text: str, max_chars: int) -> list[tuple[str, str]]:
    parsed = json.loads(text)
    pretty = json.dumps(parsed, ensure_ascii=False, indent=2)
    return split_large("JSON catalog", pretty, max_chars)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build(manifest: dict[str, Any], max_chars: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for source in manifest["sources"]:
        source_path = ROOT / source["path"]
        text = source_path.read_text(encoding="utf-8")
        chunks = json_chunks(text, max_chars) if source_path.suffix == ".json" else markdown_chunks(text, max_chars)
        for index, (heading, chunk_text) in enumerate(chunks, start=1):
            normalized = clean_text(chunk_text)
            records.append(
                {
                    "corpus": "model-knowledge",
                    "sourceID": source["id"],
                    "sourcePath": source["path"],
                    "title": source["title"],
                    "heading": heading,
                    "tags": source.get("tags", []),
                    "chunkID": f"{source['id']}#{index:03d}",
                    "sha256": sha256(normalized),
                    "text": normalized,
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, type=Path)
    parser.add_argument("--out", default=DEFAULT_OUT, type=Path)
    parser.add_argument("--max-chars", type=int, default=2200)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    records = build(manifest, args.max_chars)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} chunks to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
