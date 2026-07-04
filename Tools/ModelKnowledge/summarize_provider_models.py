#!/usr/bin/env python3
"""Summarize fetched provider model lists into a HAVEN candidate shortlist."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IN_DIR = ROOT / "Tools" / "ModelKnowledge" / "generated"

CANDIDATE_RULES = [
    {
        "ruleID": "gemma4-small-multimodal",
        "contains": ["gemma-4-e2b", "gemma-4-e4b", "gemma-4-e4b-it", "gemma-4-26b-a4b", "gemma-4-31b"],
        "purposeRefs": [
            "purpose://conference.co-pilot.multimodal-qa",
            "purpose://personal.ai.private-draft",
        ],
        "reason": "Gemma 4 family is already part of the local M5/MLX test path and useful for multimodal comparison.",
        "priority": 10,
    },
    {
        "ruleID": "qwen3-text",
        "contains": ["qwen/qwen3-8b", "qwen/qwen3-14b", "qwen/qwen3.5-9b", "qwen/qwen3.5-2b"],
        "purposeRefs": [
            "purpose://conference.co-pilot.participant-guidance",
            "purpose://model.provider-discovery",
        ],
        "reason": "Qwen local text models are current HAVEN Co-pilot baseline candidates.",
        "priority": 9,
    },
    {
        "ruleID": "qwen3-vl",
        "contains": ["qwen3-vl-8b", "qwen3-vl-30b"],
        "purposeRefs": [
            "purpose://conference.co-pilot.multimodal-qa",
        ],
        "reason": "Qwen VL variants are relevant for screenshot/poster multimodal QA.",
        "priority": 9,
    },
    {
        "ruleID": "embedding",
        "contains": ["embedding", "bge-m3"],
        "purposeRefs": [
            "purpose://docs.rag.answer-with-citations",
        ],
        "reason": "Embedding models are candidates for the dedicated model-knowledge and Book/docs RAG.",
        "priority": 8,
    },
    {
        "ruleID": "small-helper",
        "contains": ["tinyllama", "phi-3-mini", "qwen3-0.6b", "qwen2.5-0.5b", "gemma-3-1b", "gemma-3-4b"],
        "purposeRefs": [
            "purpose://privacy.pii-preflight",
            "purpose://conference.co-pilot.model-evaluation",
        ],
        "reason": "Very small models are useful as helper/preflight candidates if benchmarked carefully.",
        "priority": 6,
    },
    {
        "ruleID": "agentic-coding",
        "contains": ["qwen3-coder", "kimi-k2", "deepseek-v3", "deepseek-v4", "glm-5"],
        "purposeRefs": [
            "purpose://developer.protocol-code-reasoning",
            "purpose://model.provider-discovery",
        ],
        "reason": "Large hosted models are useful for synthetic agent/coding bake-offs before any sensitive routing.",
        "priority": 5,
    },
    {
        "ruleID": "mistral-hosted",
        "contains": ["mistral-small", "mistral-medium", "mistral-large", "ministral", "open-mistral", "devstral", "codestral"],
        "purposeRefs": [
            "purpose://conference.co-pilot.participant-guidance",
            "purpose://developer.protocol-code-reasoning",
            "purpose://model.provider-discovery",
        ],
        "reason": "Mistral hosted models are useful for EU/provider comparison, coding and Norwegian Co-pilot benchmark sweeps.",
        "priority": 7,
    },
]

EXCLUDED_MODEL_TERMS = [
    "abliterated",
    "amoral",
    "darkidol",
    "daredevil",
    "gaslight",
    "heresy",
    "heretic",
    "uncensored",
    "unfiltered",
    "unshackled",
]


def latest_snapshots(in_dir: Path) -> list[Path]:
    by_provider: dict[str, Path] = {}
    for path in sorted(in_dir.glob("*_models_*.json")):
        provider = path.name.split("_models_", 1)[0]
        by_provider[provider] = path
    return sorted(by_provider.values())


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def model_id(record: dict[str, Any]) -> str:
    return str(record.get("modelID") or record.get("id") or "")


def raw_value(record: dict[str, Any], key: str) -> Any:
    raw = record.get("raw")
    if isinstance(raw, dict) and key in raw:
        return raw[key]
    return record.get(key)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def matching_rules(model: str) -> list[dict[str, Any]]:
    lowered = normalized(model)
    if any(term in lowered for term in EXCLUDED_MODEL_TERMS):
        return []
    matches: list[dict[str, Any]] = []
    for rule in CANDIDATE_RULES:
        if any(term in lowered for term in rule["contains"]):
            matches.append(rule)
    return matches


def summarize(snapshots: list[Path], max_per_rule: int) -> dict[str, Any]:
    providers = []
    candidates_by_rule: dict[str, list[dict[str, Any]]] = defaultdict(list)
    counts_by_provider_rule: dict[tuple[str, str], int] = defaultdict(int)
    seen: set[tuple[str, str, str]] = set()

    for snapshot in snapshots:
        payload = load_json(snapshot)
        provider_id = str(payload.get("providerID") or snapshot.name.split("_models_", 1)[0])
        models = payload.get("models") if isinstance(payload.get("models"), list) else []
        providers.append(
            {
                "providerID": provider_id,
                "snapshotPath": str(snapshot),
                "fetchedAt": payload.get("fetchedAt"),
                "modelCount": payload.get("modelCount", len(models)),
            }
        )
        for record in models:
            if not isinstance(record, dict):
                continue
            mid = model_id(record)
            if not mid:
                continue
            for rule in matching_rules(mid):
                key = (provider_id, rule["ruleID"], mid)
                provider_rule_key = (provider_id, rule["ruleID"])
                if key in seen or counts_by_provider_rule[provider_rule_key] >= max_per_rule:
                    continue
                seen.add(key)
                counts_by_provider_rule[provider_rule_key] += 1
                candidates_by_rule[rule["ruleID"]].append(
                    {
                        "providerID": provider_id,
                        "modelID": mid,
                        "ruleID": rule["ruleID"],
                        "priority": rule["priority"],
                        "purposeRefs": rule["purposeRefs"],
                        "reason": rule["reason"],
                        "contextLength": raw_value(record, "context_length"),
                        "concurrencyCost": raw_value(record, "concurrency_cost"),
                        "ownedBy": raw_value(record, "owned_by") or record.get("ownedBy"),
                        "isGated": raw_value(record, "is_gated"),
                    }
                )

    candidates = [
        candidate
        for rule_id in sorted(candidates_by_rule)
        for candidate in candidates_by_rule[rule_id]
    ]
    candidates.sort(key=lambda item: (-int(item["priority"]), item["providerID"], item["modelID"].lower()))
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return {
        "schema": "haven.model-provider-candidate-summary.v0",
        "generatedAt": timestamp,
        "source": "Tools/ModelKnowledge/generated/*_models_*.json",
        "providers": providers,
        "rules": [
            {
                "ruleID": rule["ruleID"],
                "priority": rule["priority"],
                "purposeRefs": rule["purposeRefs"],
                "reason": rule["reason"],
            }
            for rule in CANDIDATE_RULES
        ],
        "excludedModelTerms": EXCLUDED_MODEL_TERMS,
        "candidateCount": len(candidates),
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", default=DEFAULT_IN_DIR, type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--max-per-rule", type=int, default=25)
    args = parser.parse_args(argv)

    snapshots = latest_snapshots(args.in_dir)
    if not snapshots:
        raise SystemExit(f"No provider model snapshots found in {args.in_dir}")
    summary = summarize(snapshots, args.max_per_rule)
    out = args.out or (args.in_dir / f"provider_model_candidates_{summary['generatedAt']}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {summary['candidateCount']} candidates to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
