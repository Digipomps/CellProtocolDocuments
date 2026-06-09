#!/usr/bin/env python3
"""Review-first Sicilian food and wine research agent.

The agent is deliberately local and side-effect light. It validates candidate
source/claim JSONL files, applies concierge guardrails, and can emit a review
bundle that is suitable for human approval before any RAG or runtime ingestion.
It does not fetch the web or publish data.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = ROOT / "sicilia_research"
DEFAULT_SOURCES = DEFAULT_DATA_DIR / "candidate_sources.jsonl"
DEFAULT_CLAIMS = DEFAULT_DATA_DIR / "candidate_claims.jsonl"
DEFAULT_BUNDLE = DEFAULT_DATA_DIR / "sicilia_research_review_bundle.json"

REQUIRED_SOURCE_KEYS = {
    "id",
    "title",
    "url",
    "owner",
    "source_type",
    "status",
    "retrieval_method",
    "last_checked",
    "quality",
}

REQUIRED_CLAIM_KEYS = {
    "id",
    "topic",
    "entity_kind",
    "name",
    "claim",
    "source_ids",
    "last_verified",
    "confidence",
    "relevance",
    "palazzo_relevance",
    "guest_visibility",
    "verification_status",
    "needs_human_review",
}

ALCOHOL_TOPICS = {"wine", "alcohol_guardrail", "wine_pairing", "wine_region"}
PUBLISHABLE_CONFIDENCE = {"high"}
PUBLISHABLE_VERIFICATION = {"verified"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected object")
            rows.append(row)
    return rows


def today_iso() -> str:
    return dt.date.today().isoformat()


def source_index(sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for source in sources:
        source_id = str(source.get("id", ""))
        if source_id in index:
            raise ValueError(f"Duplicate source id: {source_id}")
        index[source_id] = source
    return index


def validate_sources(sources: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    for source in sources:
        source_id = str(source.get("id", ""))
        missing = sorted(REQUIRED_SOURCE_KEYS - source.keys())
        if missing:
            issues.append(f"source:{source_id}: missing keys {missing}")
        if not source_id:
            issues.append("source:<empty>: id is required")
        if source_id in seen:
            issues.append(f"source:{source_id}: duplicate id")
        seen.add(source_id)
        if not str(source.get("url", "")).startswith(("https://", "local://")):
            issues.append(f"source:{source_id}: url must be https:// or local://")
    return issues


def validate_claims(
    claims: list[dict[str, Any]],
    sources_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    for claim in claims:
        claim_id = str(claim.get("id", ""))
        missing = sorted(REQUIRED_CLAIM_KEYS - claim.keys())
        if missing:
            issues.append(f"claim:{claim_id}: missing keys {missing}")
        if not claim_id:
            issues.append("claim:<empty>: id is required")
        if claim_id in seen:
            issues.append(f"claim:{claim_id}: duplicate id")
        seen.add(claim_id)

        source_ids = claim.get("source_ids", [])
        if not isinstance(source_ids, list) or not source_ids:
            issues.append(f"claim:{claim_id}: source_ids must be a non-empty list")
        else:
            for source_id in source_ids:
                if source_id not in sources_by_id:
                    issues.append(f"claim:{claim_id}: unknown source_id {source_id}")

        topic = str(claim.get("topic", ""))
        if topic in ALCOHOL_TOPICS and not claim.get("alcohol_policy"):
            issues.append(f"claim:{claim_id}: alcohol topic requires alcohol_policy")

        if claim.get("palazzo_relevance") == "palazzo_direct" and not claim.get("palazzo_source_ids"):
            issues.append(f"claim:{claim_id}: palazzo_direct requires palazzo_source_ids")

        if claim.get("guest_visibility") == "public_guest" and not claim.get("citations_required", True):
            issues.append(f"claim:{claim_id}: public_guest claims must require citations")

    return issues


def is_publishable(claim: dict[str, Any]) -> bool:
    if claim.get("needs_human_review"):
        return False
    if claim.get("confidence") not in PUBLISHABLE_CONFIDENCE:
        return False
    if claim.get("verification_status") not in PUBLISHABLE_VERIFICATION:
        return False
    if claim.get("guest_visibility") != "public_guest":
        return False
    if claim.get("topic") in ALCOHOL_TOPICS:
        return claim.get("alcohol_policy") == "neutral_fact_only"
    return True


def build_bundle(
    sources: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> dict[str, Any]:
    publishable = [claim for claim in claims if is_publishable(claim)]
    review = [claim for claim in claims if claim not in publishable]
    by_topic = collections.Counter(str(claim.get("topic", "unknown")) for claim in claims)
    by_relevance = collections.Counter(str(claim.get("palazzo_relevance", "unknown")) for claim in claims)
    return {
        "schema": "haven.restaurant.sicilia_research_review_bundle.v1",
        "generated_at": today_iso(),
        "status": "review_required_before_ingest",
        "source_count": len(sources),
        "claim_count": len(claims),
        "publishable_claim_count": len(publishable),
        "review_claim_count": len(review),
        "topics": dict(sorted(by_topic.items())),
        "palazzo_relevance": dict(sorted(by_relevance.items())),
        "publishable_claim_ids": [claim["id"] for claim in publishable],
        "review_claim_ids": [claim["id"] for claim in review],
        "rag_candidate_chunks": build_rag_chunks(publishable),
        "sources": sources,
        "claims": claims,
        "ingest_policy": {
            "raw_page_storage": "do_not_store",
            "store_only": [
                "source metadata",
                "short evidence notes",
                "normalized claims",
                "citations",
                "verification status",
            ],
            "runtime_publish": "blocked_until_human_review",
        },
    }


def build_rag_chunks(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for claim in claims:
        chunks.append(
            {
                "id": f"rag-{claim['id']}",
                "case_id": "palazzo_sicilia_supplement",
                "source_claim_id": claim["id"],
                "title": claim["name"],
                "text": claim["claim"],
                "tags": [
                    "restaurant-concierge",
                    "sicilia",
                    str(claim.get("topic", "knowledge")),
                    str(claim.get("palazzo_relevance", "restaurant_general")),
                ],
                "source_ids": claim["source_ids"],
                "audience": claim.get("guest_visibility", "staff_review"),
            }
        )
    return chunks


def command_validate(args: argparse.Namespace) -> int:
    sources = load_jsonl(Path(args.sources))
    claims = load_jsonl(Path(args.claims))
    issues = validate_sources(sources)
    issues.extend(validate_claims(claims, source_index(sources)))
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "sources": len(sources),
                "claims": len(claims),
                "publishable_claims": sum(1 for claim in claims if is_publishable(claim)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def command_bundle(args: argparse.Namespace) -> int:
    sources = load_jsonl(Path(args.sources))
    claims = load_jsonl(Path(args.claims))
    issues = validate_sources(sources)
    issues.extend(validate_claims(claims, source_index(sources)))
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    bundle = build_bundle(sources, claims)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(str(output))
    return 0


def command_publishable(args: argparse.Namespace) -> int:
    claims = load_jsonl(Path(args.claims))
    for claim in claims:
        if is_publishable(claim):
            print(json.dumps(claim, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(func=command_validate)
    parser.add_argument("--sources", default=str(DEFAULT_SOURCES))
    parser.add_argument("--claims", default=str(DEFAULT_CLAIMS))

    subparsers = parser.add_subparsers(dest="command")
    validate = subparsers.add_parser("validate", help="Validate source and claim JSONL")
    validate.add_argument("--sources", default=str(DEFAULT_SOURCES))
    validate.add_argument("--claims", default=str(DEFAULT_CLAIMS))
    validate.set_defaults(func=command_validate)

    bundle = subparsers.add_parser("bundle", help="Build review bundle JSON")
    bundle.add_argument("--sources", default=str(DEFAULT_SOURCES))
    bundle.add_argument("--claims", default=str(DEFAULT_CLAIMS))
    bundle.add_argument("--output", default=str(DEFAULT_BUNDLE))
    bundle.set_defaults(func=command_bundle)

    publishable = subparsers.add_parser("publishable", help="Print claims that pass local publishability checks")
    publishable.add_argument("--claims", default=str(DEFAULT_CLAIMS))
    publishable.set_defaults(func=command_publishable)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
