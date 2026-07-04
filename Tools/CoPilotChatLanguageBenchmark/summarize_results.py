#!/usr/bin/env python3
"""Summarize Co-pilot chat benchmark JSONL result files."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def summarize(path: Path) -> dict[str, Any]:
    rows = load_jsonl(path)
    total = sum(row["scores"]["total"] for row in rows)
    maximum = sum(row["scores"]["max"] for row in rows)
    parse_errors = sum(1 for row in rows if row["scores"].get("parseError"))
    by_dimension: Counter[str] = Counter()
    max_by_dimension: Counter[str] = Counter()
    by_category: dict[str, Counter[str]] = defaultdict(Counter)
    worst: list[tuple[int, str, str]] = []

    dimensions = [
        "intent",
        "action",
        "clarification",
        "safety",
        "mustMention",
        "mustNotMention",
    ]
    for row in rows:
        scores = row["scores"]
        for dimension in dimensions:
            by_dimension[dimension] += int(scores.get(dimension, 0))
            max_by_dimension[dimension] += 1
        category = row["category"]
        by_category[category]["total"] += scores["total"]
        by_category[category]["max"] += scores["max"]
        worst.append((scores["total"], row["id"], row["utterance"]))

    return {
        "path": str(path),
        "cases": len(rows),
        "score": total,
        "max": maximum,
        "percent": round((total / maximum * 100) if maximum else 0.0, 1),
        "parseErrors": parse_errors,
        "dimensions": {
            key: {
                "score": by_dimension[key],
                "max": max_by_dimension[key],
                "percent": round(
                    (by_dimension[key] / max_by_dimension[key] * 100)
                    if max_by_dimension[key]
                    else 0.0,
                    1,
                ),
            }
            for key in dimensions
        },
        "categories": {
            key: {
                "score": value["total"],
                "max": value["max"],
                "percent": round(
                    (value["total"] / value["max"] * 100) if value["max"] else 0.0,
                    1,
                ),
            }
            for key, value in sorted(by_category.items())
        },
        "lowestCases": [
            {"id": case_id, "score": score, "utterance": utterance}
            for score, case_id, utterance in sorted(worst)[:8]
        ],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    summaries = [summarize(path) for path in args.results]
    if args.json:
        print(json.dumps(summaries, ensure_ascii=False, indent=2))
        return 0

    for summary in summaries:
        print(f"{summary['path']}")
        print(
            f"  cases={summary['cases']} score={summary['score']}/{summary['max']} "
            f"({summary['percent']}%) parseErrors={summary['parseErrors']}"
        )
        print("  dimensions:")
        for key, value in summary["dimensions"].items():
            print(f"    {key}: {value['score']}/{value['max']} ({value['percent']}%)")
        print("  lowest cases:")
        for case in summary["lowestCases"]:
            print(f"    {case['id']} {case['score']}/6: {case['utterance']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
