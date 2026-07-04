#!/usr/bin/env python3
"""Query the lightweight model-knowledge corpus with lexical scoring."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = ROOT / "Tools" / "ModelKnowledge" / "generated" / "model_knowledge_corpus.jsonl"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w./:-]+", text.lower())


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def score(query_terms: Counter[str], record: dict, document_frequency: Counter[str], total_docs: int) -> float:
    tokens = tokenize(" ".join([record.get("title", ""), record.get("heading", ""), " ".join(record.get("tags", [])), record["text"]]))
    counts = Counter(tokens)
    total = 0.0
    for term, query_count in query_terms.items():
        tf = counts.get(term, 0)
        if not tf:
            continue
        idf = math.log((1 + total_docs) / (1 + document_frequency[term])) + 1
        total += (1 + math.log(tf)) * idf * query_count
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=DEFAULT_CORPUS, type=Path)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    records = load_jsonl(args.corpus)
    query_terms = Counter(tokenize(args.query))
    document_frequency: Counter[str] = Counter()
    for record in records:
        document_frequency.update(set(tokenize(record["text"])))

    ranked = sorted(
        ((score(query_terms, record, document_frequency, len(records)), record) for record in records),
        key=lambda item: item[0],
        reverse=True,
    )
    for rank, (value, record) in enumerate(ranked[: args.top], start=1):
        preview = re.sub(r"\s+", " ", record["text"])[:400]
        print(f"{rank}. score={value:.3f} {record['sourcePath']} :: {record['heading']}")
        print(f"   tags={', '.join(record.get('tags', []))}")
        print(f"   {preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
