#!/usr/bin/env python3
"""Local reference analyzer for argument, rhetoric and source grounding.

The v1 tool is intentionally conservative. It anchors findings in exact input
text, uses deterministic heuristics, and does not fetch external sources or call
language models. Source verification can be layered on later by a source-auditor
agent using the same JSON contract.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ANALYSIS_SCHEMA = "haven.text_reliability.analysis.v1"
INPUT_SET_SCHEMA = "haven.text_reliability.input_set.v1"
ADD2ENTITY_CAPTURE_SCHEMA = "haven.add2entity.webpage-capture.v1"
ADD2ENTITY_SIDECAR_SCHEMA = "haven.text_reliability.add2entity_sidecar.v1"

URL_RE = re.compile(r"https?://[^\s\]\)\}\>,]+")
SENTENCE_RE = re.compile(r"\S.*?(?:(?<=[.!?])(?=\s+)|$)", re.MULTILINE | re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
FENCE_RE = re.compile(r"^\s*```")

CLAIM_TYPE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("statistical", re.compile(r"\b\d+(?:[,.]\d+)?\s*(?:%|prosent|percent|million|billion|mrd|mill|nok|kr)\b", re.I)),
    ("causal", re.compile(r"\b(fordi|derfor|fører til|forer til|causes?|because|leads? to|due to)\b", re.I)),
    ("normative", re.compile(r"\b(bør|bor|må|ma|skal|should|must|ought|necessary|nødvendig|nodvendig)\b", re.I)),
    ("predictive", re.compile(r"\b(vil|kommer til|innen|by \d{4}|will|expected|forecast|forventer|sannsynlig)\b", re.I)),
    ("project_capability", re.compile(r"\b(implementert|prototype|kan hente|kan analysere|supports?|built|deployed|capability|feature)\b", re.I)),
]

MODERATED_RE = re.compile(r"\b(kan|could|may|might|mulig|possible|sannsynlig|likely|indicates?|tyder på|tyder pa)\b", re.I)
SPECULATIVE_RE = re.compile(r"\b(kanskje|maybe|perhaps|possibly|kan komme til|hypothesis|hypotese)\b", re.I)

RHETORIC_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("certainty_inflation", re.compile(r"\b(alle vet|alltid|aldri|ingen tvil|undeniable|obvious|everyone knows|never|always)\b", re.I), "may overstate certainty"),
    ("false_dichotomy", re.compile(r"\b(enten\b.+\beller|either\b.+\bor)\b", re.I), "presents a binary choice"),
    ("authority_appeal", re.compile(r"\b(ifølge|ifolge|according to|ekspert|expert|forskere|researchers)\b", re.I), "appeals to an authority or source"),
    ("anecdotal_evidence", re.compile(r"\b(jeg opplevde|i experienced|one example|anecdote|historien viser)\b", re.I), "uses an anecdotal basis"),
    ("loaded_language", re.compile(r"\b(katastrofe|skandale|absurd|håpløs|haplos|revolusjonerende|broken|disaster|corrupt)\b", re.I), "uses loaded wording"),
    ("contrast", re.compile(r"\b(men|derimot|however|whereas|instead|i motsetning)\b", re.I), "builds a contrast"),
    ("framing", re.compile(r"\b(egentlig handler dette om|the real issue is|rammen er|framed as)\b", re.I), "frames the issue explicitly"),
]

CONCLUSION_RE = re.compile(r"\b(derfor|konklusjon|av den grunn|bør|bor|må|ma|should|must|therefore|hence)\b", re.I)
SOURCE_CUE_RE = re.compile(r"\b(ifølge|ifolge|source|kilde|rapport|study|studie|according to)\b", re.I)
DEFAULT_PRODUCTIVITY_DELTAS_PP = [0.3, 0.5, 1.0]


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def parse_number(value: str | int | float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    normalized = str(value).strip().replace("\u00a0", " ").replace(" ", "")
    if not normalized:
        return None
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    else:
        normalized = normalized.replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def line_spans(text: str) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    offset = 0
    for line_number, raw_line in enumerate(text.splitlines(keepends=True), start=1):
        line = raw_line.rstrip("\r\n")
        spans.append(
            {
                "line_number": line_number,
                "line": line,
                "char_start": offset,
                "char_end": offset + len(line),
                "raw_char_end": offset + len(raw_line),
            }
        )
        offset += len(raw_line)
    return spans


def span_overlaps(start: int, end: int, spans: list[dict[str, Any]]) -> bool:
    return any(start < span["char_end"] and end > span["char_start"] for span in spans)


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def section_id_for_position(sections: list[dict[str, Any]], position: int) -> str | None:
    current: dict[str, Any] | None = None
    for section in sections:
        if section["char_start"] <= position:
            current = section
        else:
            break
    return current["section_id"] if current else None


def extract_markdown_structure(inputs: list[dict[str, Any]]) -> dict[str, Any]:
    sections: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    structural_spans: list[dict[str, Any]] = []
    code_fence_spans: list[dict[str, Any]] = []

    for input_item in inputs:
        spans = line_spans(input_item["text"])
        in_fence = False
        fence_start: dict[str, Any] | None = None
        section_stack: list[dict[str, Any]] = []
        input_sections: list[dict[str, Any]] = []

        for span in spans:
            line = span["line"]
            if FENCE_RE.match(line):
                if in_fence and fence_start is not None:
                    code_fence_spans.append(
                        {
                            "input_id": input_item["input_id"],
                            "char_start": fence_start["char_start"],
                            "char_end": span["raw_char_end"],
                            "line_start": fence_start["line_number"],
                            "line_end": span["line_number"],
                            "kind": "code_fence",
                        }
                    )
                    in_fence = False
                    fence_start = None
                else:
                    in_fence = True
                    fence_start = span
                structural_spans.append(
                    {
                        "input_id": input_item["input_id"],
                        "char_start": span["char_start"],
                        "char_end": span["raw_char_end"],
                        "kind": "code_fence_marker",
                    }
                )
                continue
            if in_fence:
                continue
            heading = HEADING_RE.match(line)
            if not heading:
                continue
            level = len(heading.group(1))
            title = heading.group(2).strip()
            while section_stack and section_stack[-1]["level"] >= level:
                section_stack.pop()
            parent_section_id = section_stack[-1]["section_id"] if section_stack else None
            section = {
                "section_id": f"section-{len(sections) + 1:04d}",
                "input_id": input_item["input_id"],
                "level": level,
                "title": title,
                "parent_section_id": parent_section_id,
                "char_start": span["char_start"],
                "char_end": span["char_end"],
                "line_start": span["line_number"],
            }
            sections.append(section)
            input_sections.append(section)
            section_stack.append(section)
            structural_spans.append(
                {
                    "input_id": input_item["input_id"],
                    "char_start": span["char_start"],
                    "char_end": span["raw_char_end"],
                    "kind": "heading",
                }
            )

        for index, section in enumerate(input_sections):
            next_section = input_sections[index + 1] if index + 1 < len(input_sections) else None
            section["char_end"] = next_section["char_start"] if next_section else len(input_item["text"])

        index = 0
        while index < len(spans):
            span = spans[index]
            if span_overlaps(span["char_start"], span["char_end"], code_fence_spans):
                index += 1
                continue
            if not is_table_row(span["line"]):
                index += 1
                continue
            if index + 1 >= len(spans) or not TABLE_SEPARATOR_RE.match(spans[index + 1]["line"]):
                index += 1
                continue
            headers = split_table_row(span["line"])
            table_start = span["char_start"]
            table_end = spans[index + 1]["raw_char_end"]
            row_spans: list[dict[str, Any]] = []
            cursor = index + 2
            while cursor < len(spans) and is_table_row(spans[cursor]["line"]):
                if TABLE_SEPARATOR_RE.match(spans[cursor]["line"]):
                    cursor += 1
                    continue
                row_spans.append(spans[cursor])
                table_end = spans[cursor]["raw_char_end"]
                cursor += 1
            rows = [
                {
                    "row_index": row_index,
                    "cells": split_table_row(row_span["line"]),
                    "quote": row_span["line"],
                    "char_start": row_span["char_start"],
                    "char_end": row_span["char_end"],
                    "line_number": row_span["line_number"],
                }
                for row_index, row_span in enumerate(row_spans, start=1)
            ]
            table = {
                "table_id": f"table-{len(tables) + 1:04d}",
                "input_id": input_item["input_id"],
                "section_id": section_id_for_position(input_sections, table_start),
                "headers": headers,
                "rows": rows,
                "char_start": table_start,
                "char_end": table_end,
                "line_start": span["line_number"],
                "line_end": spans[cursor - 1]["line_number"] if cursor > index else span["line_number"],
            }
            tables.append(table)
            structural_spans.append(
                {
                    "input_id": input_item["input_id"],
                    "char_start": table_start,
                    "char_end": table_end,
                    "kind": "markdown_table",
                }
            )
            index = cursor

    structural_spans.extend(code_fence_spans)
    return {
        "schema": "haven.text_reliability.markdown_structure.v1",
        "sections": sections,
        "tables": tables,
        "structural_spans": structural_spans,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def load_input_set(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    data = load_json(path)
    if data.get("schema") == ADD2ENTITY_CAPTURE_SCHEMA:
        return [input_from_add2entity_capture(data)], data
    if data.get("schema") != INPUT_SET_SCHEMA:
        raise ValueError(f"{path}: unsupported schema {data.get('schema')!r}")
    inputs = data.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        raise ValueError(f"{path}: inputs must be a non-empty list")
    return [normalize_input(item, index) for index, item in enumerate(inputs, start=1)], None


def input_from_text_file(path: Path, title: str | None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    return normalize_input(
        {
            "input_id": f"text-file:{path.name}:{stable_hash(text)}",
            "title": title or path.name,
            "text": text,
            "metadata": {
                "source_kind": "text_file",
                "path": str(path),
            },
        },
        1,
    )


def input_from_add2entity_capture(capture: dict[str, Any]) -> dict[str, Any]:
    if capture.get("schema") != ADD2ENTITY_CAPTURE_SCHEMA:
        raise ValueError(f"unsupported Add2Entity capture schema {capture.get('schema')!r}")
    content = capture.get("content")
    if not isinstance(content, dict) or not str(content.get("text", "")).strip():
        raise ValueError("Add2Entity capture requires content.text")
    capture_id = str(capture.get("captureID", "")).strip()
    if not capture_id:
        raise ValueError("Add2Entity capture requires captureID")
    metadata = {
        "source_kind": "add2entity_capture",
        "schema": capture.get("schema"),
        "captureID": capture_id,
        "capturedAt": capture.get("capturedAt"),
        "url": capture.get("url"),
        "canonicalURL": capture.get("canonicalURL"),
        "siteName": capture.get("siteName"),
        "author": capture.get("author"),
        "publishedTime": capture.get("publishedTime"),
        "language": capture.get("language"),
        "description": capture.get("description"),
        "target": capture.get("target"),
        "rag": capture.get("rag"),
        "mutatesEntity": False,
    }
    return normalize_input(
        {
            "input_id": f"add2entity:{capture_id}",
            "title": str(capture.get("title") or capture_id),
            "text": content["text"],
            "metadata": {key: value for key, value in metadata.items() if value is not None},
        },
        1,
    )


def normalize_input(raw: dict[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError(f"input {index}: expected object")
    text = str(raw.get("text", "")).strip()
    if not text:
        raise ValueError(f"input {index}: text is required")
    input_id = str(raw.get("input_id") or f"input-{index}")
    return {
        "input_id": input_id,
        "title": str(raw.get("title") or input_id),
        "text": text,
        "metadata": raw.get("metadata") if isinstance(raw.get("metadata"), dict) else {},
    }


def sentence_spans(text: str) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    for match in SENTENCE_RE.finditer(text):
        quote = match.group(0).strip()
        if not quote:
            continue
        leading = len(match.group(0)) - len(match.group(0).lstrip())
        start = match.start() + leading
        end = start + len(quote)
        spans.append({"quote": quote, "char_start": start, "char_end": end})
    return spans


def classify_claim_type(sentence: str) -> str:
    for claim_type, pattern in CLAIM_TYPE_PATTERNS:
        if pattern.search(sentence):
            return claim_type
    return "factual"


def classify_strength(sentence: str) -> str:
    if SPECULATIVE_RE.search(sentence):
        return "speculative"
    if MODERATED_RE.search(sentence):
        return "moderated"
    return "assertive"


def extract_source_refs(sentence: str, base_start: int = 0) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for index, match in enumerate(URL_RE.finditer(sentence), start=1):
        refs.append(
            {
                "source_ref_id": f"source-url-{index}",
                "kind": "url",
                "value": match.group(0),
                "quote": match.group(0),
                "char_start": base_start + match.start(),
                "char_end": base_start + match.end(),
            }
        )
    if SOURCE_CUE_RE.search(sentence) and not refs:
        refs.append(
            {
                "source_ref_id": "source-cue-1",
                "kind": "source_cue",
                "value": SOURCE_CUE_RE.search(sentence).group(0),
                "quote": sentence,
                "char_start": base_start,
                "char_end": base_start + len(sentence),
            }
        )
    return refs


def extract_claims(inputs: list[dict[str, Any]], markdown_structure: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    markdown_structure = markdown_structure or extract_markdown_structure(inputs)
    claims: list[dict[str, Any]] = []
    structural_spans_by_input: dict[str, list[dict[str, Any]]] = {}
    sections_by_input: dict[str, list[dict[str, Any]]] = {}
    for span in markdown_structure.get("structural_spans", []):
        structural_spans_by_input.setdefault(span["input_id"], []).append(span)
    for section in markdown_structure.get("sections", []):
        sections_by_input.setdefault(section["input_id"], []).append(section)

    for input_item in inputs:
        original_text = input_item["text"]
        scan_chars = list(original_text)
        for structural_span in structural_spans_by_input.get(input_item["input_id"], []):
            for index in range(structural_span["char_start"], min(structural_span["char_end"], len(scan_chars))):
                scan_chars[index] = " "
        scan_text = "".join(scan_chars)
        for sentence_index, span in enumerate(sentence_spans(scan_text), start=1):
            quote = original_text[span["char_start"] : span["char_end"]]
            if HEADING_RE.match(quote) or TABLE_SEPARATOR_RE.match(quote):
                continue
            if len(quote.split()) < 4:
                continue
            claim_type = classify_claim_type(quote)
            claim_id = f"claim-{len(claims) + 1:04d}"
            source_refs = extract_source_refs(quote, span["char_start"])
            claims.append(
                {
                    "claim_id": claim_id,
                    "input_id": input_item["input_id"],
                    "sentence_index": sentence_index,
                    "quote": quote,
                    "char_start": span["char_start"],
                    "char_end": span["char_end"],
                    "claim_type": claim_type,
                    "strength": classify_strength(quote),
                    "source_refs": source_refs,
                    "section_id": section_id_for_position(sections_by_input.get(input_item["input_id"], []), span["char_start"]),
                    "origin": "sentence",
                    "is_inferred": False,
                }
            )

    for table in markdown_structure.get("tables", []):
        for row in table.get("rows", []):
            quote = row["quote"]
            if len(" ".join(row.get("cells", [])).split()) < 4:
                continue
            claim_text = " ".join(row.get("cells", []))
            claim_id = f"claim-{len(claims) + 1:04d}"
            claims.append(
                {
                    "claim_id": claim_id,
                    "input_id": table["input_id"],
                    "sentence_index": None,
                    "quote": quote,
                    "char_start": row["char_start"],
                    "char_end": row["char_end"],
                    "claim_type": classify_claim_type(claim_text),
                    "strength": classify_strength(claim_text),
                    "source_refs": extract_source_refs(quote, row["char_start"]),
                    "section_id": table.get("section_id"),
                    "origin": "markdown_table_row",
                    "table_id": table["table_id"],
                    "table_row_index": row["row_index"],
                    "table_headers": table.get("headers", []),
                    "table_cells": row.get("cells", []),
                    "is_inferred": False,
                }
            )
    return claims


def build_argument_map(claims: list[dict[str, Any]]) -> dict[str, Any]:
    conclusions = [claim["claim_id"] for claim in claims if CONCLUSION_RE.search(claim["quote"])]
    premises = [claim["claim_id"] for claim in claims if claim["claim_id"] not in conclusions]
    inferred_links: list[dict[str, Any]] = []
    if conclusions and premises:
        for conclusion in conclusions[:3]:
            inferred_links.append(
                {
                    "from_claim_ids": premises[:3],
                    "to_claim_id": conclusion,
                    "relation": "supports_or_contextualizes",
                    "is_inferred": True,
                    "basis": "Heuristic v1 relation: nearby non-conclusion claims may function as premises.",
                }
            )
    return {
        "schema": "haven.text_reliability.argument_map.v1",
        "explicit_conclusion_claim_ids": conclusions,
        "explicit_premise_claim_ids": premises,
        "inferred_links": inferred_links,
        "limitations": [
            "Deterministic v1 uses sentence-level cues; model or human review is needed for deep argument reconstruction."
        ],
    }


def source_ref_domains(source_refs: list[dict[str, Any]]) -> list[str]:
    domains: list[str] = []
    for ref in source_refs:
        if ref.get("kind") != "url":
            continue
        parsed = urlparse(str(ref.get("value", "")))
        if parsed.netloc:
            domains.append(parsed.netloc.lower())
    return domains


def domain_allowed(domain: str, allowed_domains: list[str]) -> bool:
    normalized = domain.lower()
    return any(normalized == allowed.lower() or normalized.endswith(f".{allowed.lower()}") for allowed in allowed_domains)


def source_domain_status(source_refs: list[dict[str, Any]], allowed_domains: list[str]) -> str:
    domains = source_ref_domains(source_refs)
    if not domains:
        return "not_applicable"
    if not allowed_domains:
        return "not_restricted"
    return "allowed" if all(domain_allowed(domain, allowed_domains) for domain in domains) else "outside_allowed_domains"


def build_source_audits(claims: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    source_mode = policy.get("source_mode", "verifying")
    allowed_domains = [str(domain) for domain in policy.get("allowed_domains", [])]
    audits: list[dict[str, Any]] = []
    for claim in claims:
        source_refs = claim.get("source_refs", [])
        has_url = any(ref.get("kind") == "url" for ref in source_refs)
        has_source_cue = any(ref.get("kind") == "source_cue" for ref in source_refs)
        domain_status = source_domain_status(source_refs, allowed_domains)
        if source_mode == "text_only":
            check_status = "not_checkable"
            audit_status = "text_only_not_audited"
            evidence_grade = "not_audited_by_policy"
            reason = "text_only_policy_no_external_source_check"
            source_audit_required = False
        elif has_url:
            check_status = "not_checkable"
            audit_status = "needs_external_source_audit"
            evidence_grade = "source_named_unverified"
            reason = "local_v1_does_not_fetch_or_verify_sources"
            source_audit_required = True
        elif has_source_cue:
            check_status = "source_missing"
            audit_status = "source_cue_without_anchor"
            evidence_grade = "source_named_but_not_anchorable"
            reason = "source_cue_found_without_url_or_retrievable_anchor"
            source_audit_required = True
        else:
            check_status = "source_missing"
            audit_status = "source_missing"
            evidence_grade = "no_source_anchor"
            reason = "no_source_reference_found_near_claim"
            source_audit_required = True
        audits.append(
            {
                "source_audit_id": f"source-audit-{len(audits) + 1:04d}",
                "claim_id": claim["claim_id"],
                "status": check_status,
                "source_audit_status": audit_status,
                "source_audit_required": source_audit_required,
                "source_mode": source_mode,
                "source_refs": source_refs,
                "source_ref_count": len(source_refs),
                "source_domains": source_ref_domains(source_refs),
                "domain_status": domain_status,
                "evidence_grade": evidence_grade,
                "reason": reason,
                "checked_at": utc_now_iso(),
                "checked_by": "deterministic_source_auditor_v1",
            }
        )
    return audits


def source_checks_from_audits(source_audits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for audit in source_audits:
        checks.append(
            {
                "check_id": f"source-check-{len(checks) + 1:04d}",
                "claim_id": audit["claim_id"],
                "status": audit["status"],
                "source_refs": audit["source_refs"],
                "source_audit_id": audit["source_audit_id"],
                "source_audit_status": audit["source_audit_status"],
                "source_audit_required": audit["source_audit_required"],
                "reason": audit["reason"],
                "checked_at": audit["checked_at"],
                "checked_by": audit["checked_by"],
            }
        )
    return checks


def annotate_claims_with_source_audits(claims: list[dict[str, Any]], source_audits: list[dict[str, Any]]) -> None:
    audits_by_claim = {audit["claim_id"]: audit for audit in source_audits}
    for claim in claims:
        audit = audits_by_claim.get(claim["claim_id"])
        if audit is None:
            continue
        claim["source_audit_id"] = audit["source_audit_id"]
        claim["source_check_status"] = audit["status"]
        claim["source_audit_status"] = audit["source_audit_status"]
        claim["source_audit_required"] = audit["source_audit_required"]
        claim["evidence_grade"] = audit["evidence_grade"]


def count_values(items: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def section_title_lookup(markdown_structure: dict[str, Any]) -> dict[str, str]:
    return {section["section_id"]: section["title"] for section in markdown_structure.get("sections", [])}


def build_claim_clusters(
    claims: list[dict[str, Any]],
    markdown_structure: dict[str, Any],
    source_audits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    section_titles = section_title_lookup(markdown_structure)
    audits_by_claim = {audit["claim_id"]: audit for audit in source_audits}
    grouped: dict[str, list[dict[str, Any]]] = {}
    key_order: list[str] = []
    for claim in claims:
        key = claim.get("section_id") or f"input-root:{claim['input_id']}"
        if key not in grouped:
            grouped[key] = []
            key_order.append(key)
        grouped[key].append(claim)

    clusters: list[dict[str, Any]] = []
    for key in key_order:
        cluster_claims = grouped[key]
        cluster_id = f"cluster-{len(clusters) + 1:04d}"
        for claim in cluster_claims:
            claim["claim_cluster_id"] = cluster_id
        statuses = [
            audits_by_claim[claim["claim_id"]]["source_audit_status"]
            for claim in cluster_claims
            if claim["claim_id"] in audits_by_claim
        ]
        check_statuses = [
            audits_by_claim[claim["claim_id"]]["status"]
            for claim in cluster_claims
            if claim["claim_id"] in audits_by_claim
        ]
        representative_claims = [
            {
                "claim_id": claim["claim_id"],
                "quote": claim["quote"],
            }
            for claim in cluster_claims[:3]
        ]
        title = section_titles.get(key, "Unsectioned input")
        clusters.append(
            {
                "cluster_id": cluster_id,
                "cluster_key": key,
                "title": title,
                "claim_ids": [claim["claim_id"] for claim in cluster_claims],
                "claim_count": len(cluster_claims),
                "claim_type_counts": count_values([claim["claim_type"] for claim in cluster_claims]),
                "origin_counts": count_values([claim.get("origin", "unknown") for claim in cluster_claims]),
                "source_audit_status_counts": count_values(statuses),
                "source_check_status_counts": count_values(check_statuses),
                "representative_claims": representative_claims,
            }
        )
    return clusters


def build_claim_source_matrix(
    claims: list[dict[str, Any]],
    source_audits: list[dict[str, Any]],
    markdown_structure: dict[str, Any],
) -> list[dict[str, Any]]:
    audits_by_claim = {audit["claim_id"]: audit for audit in source_audits}
    section_titles = section_title_lookup(markdown_structure)
    matrix: list[dict[str, Any]] = []
    for claim in claims:
        audit = audits_by_claim.get(claim["claim_id"], {})
        matrix.append(
            {
                "claim_id": claim["claim_id"],
                "claim_cluster_id": claim.get("claim_cluster_id"),
                "section_id": claim.get("section_id"),
                "section_title": section_titles.get(claim.get("section_id"), "Unsectioned input"),
                "origin": claim.get("origin"),
                "claim_type": claim["claim_type"],
                "strength": claim["strength"],
                "quote": claim["quote"],
                "source_check_status": audit.get("status"),
                "source_audit_status": audit.get("source_audit_status"),
                "evidence_grade": audit.get("evidence_grade"),
                "source_audit_required": audit.get("source_audit_required"),
                "source_refs": audit.get("source_refs", []),
                "source_domains": audit.get("source_domains", []),
                "domain_status": audit.get("domain_status"),
                "reason": audit.get("reason"),
            }
        )
    return matrix


def mermaid_label(value: str, limit: int = 80) -> str:
    compact = re.sub(r"\s+", " ", value).strip().replace('"', "'")
    if len(compact) > limit:
        compact = f"{compact[: limit - 3]}..."
    return compact


def render_argument_mermaid(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
    lines = ["flowchart TD"]
    visible_nodes = nodes[:12]
    visible_ids = {node["node_id"] for node in visible_nodes}
    for node in visible_nodes:
        lines.append(f'    {node["node_id"]}["{mermaid_label(node["label"])}"]')
    for edge in edges:
        if edge["from_node_id"] in visible_ids and edge["to_node_id"] in visible_ids:
            label = mermaid_label(edge["relation"], 32)
            lines.append(f'    {edge["from_node_id"]} -- "{label}" --> {edge["to_node_id"]}')
    if len(nodes) > len(visible_nodes):
        lines.append(f'    omitted["... {len(nodes) - len(visible_nodes)} more cluster node(s) omitted"]')
    return "\n".join(lines)


def build_argument_graph(
    claims: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    argument_map: dict[str, Any],
) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = [
        {
            "node_id": f"n{index:03d}",
            "kind": "claim_cluster",
            "cluster_id": cluster["cluster_id"],
            "label": f"{cluster['title']} ({cluster['claim_count']} claim(s))",
            "claim_ids": cluster["claim_ids"],
        }
        for index, cluster in enumerate(clusters, start=1)
    ]
    node_by_cluster = {node["cluster_id"]: node for node in nodes}
    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    edges: list[dict[str, Any]] = []

    for index in range(len(nodes) - 1):
        edges.append(
            {
                "edge_id": f"edge-{len(edges) + 1:04d}",
                "from_node_id": nodes[index]["node_id"],
                "to_node_id": nodes[index + 1]["node_id"],
                "relation": "develops",
                "is_inferred": True,
                "basis": "Section order in the submitted text.",
            }
        )

    for link in argument_map.get("inferred_links", []):
        target = claim_by_id.get(link["to_claim_id"])
        if not target:
            continue
        target_node = node_by_cluster.get(target.get("claim_cluster_id"))
        if not target_node:
            continue
        for source_claim_id in link.get("from_claim_ids", []):
            source = claim_by_id.get(source_claim_id)
            if not source:
                continue
            source_node = node_by_cluster.get(source.get("claim_cluster_id"))
            if not source_node or source_node["node_id"] == target_node["node_id"]:
                continue
            edges.append(
                {
                    "edge_id": f"edge-{len(edges) + 1:04d}",
                    "from_node_id": source_node["node_id"],
                    "to_node_id": target_node["node_id"],
                    "relation": link.get("relation", "supports_or_contextualizes"),
                    "is_inferred": True,
                    "basis": link.get("basis", "Inferred from argument_map."),
                    "source_claim_id": source_claim_id,
                    "target_claim_id": target["claim_id"],
                }
            )

    return {
        "schema": "haven.text_reliability.argument_graph.v1",
        "nodes": nodes,
        "edges": edges,
        "mermaid": render_argument_mermaid(nodes, edges),
        "limitations": [
            "Deterministic graph uses section order and heuristic links; a reasoning model or human adjudicator should refine warrants.",
        ],
    }


def extract_rhetoric(inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for input_item in inputs:
        for span in sentence_spans(input_item["text"]):
            quote = span["quote"]
            for rhetoric_type, pattern, note in RHETORIC_PATTERNS:
                if pattern.search(quote):
                    findings.append(
                        {
                            "finding_id": f"rhetoric-{len(findings) + 1:04d}",
                            "input_id": input_item["input_id"],
                            "rhetoric_type": rhetoric_type,
                            "quote": quote,
                            "char_start": span["char_start"],
                            "char_end": span["char_end"],
                            "evidence_role": "presentation_or_pressure",
                            "substitutes_for_evidence": rhetoric_type in {"certainty_inflation", "false_dichotomy", "loaded_language"},
                            "note": note,
                        }
                    )
    return findings


def build_source_checks(claims: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    source_mode = policy.get("source_mode", "verifying")
    checks: list[dict[str, Any]] = []
    for claim in claims:
        if claim["source_refs"]:
            status = "not_checkable"
            reason = "local_v1_does_not_fetch_or_verify_sources"
        elif source_mode == "text_only":
            status = "not_checkable"
            reason = "text_only_policy_no_external_source_check"
        else:
            status = "source_missing"
            reason = "no_source_reference_found_near_claim"
        checks.append(
            {
                "check_id": f"source-check-{len(checks) + 1:04d}",
                "claim_id": claim["claim_id"],
                "status": status,
                "source_refs": claim["source_refs"],
                "reason": reason,
                "checked_at": utc_now_iso(),
                "checked_by": "deterministic_local_v1",
            }
        )
    return checks


def count_status(source_checks: list[dict[str, Any]], status: str) -> int:
    return sum(1 for check in source_checks if check["status"] == status)


def dimension(name: str, rating: str, reason: str) -> dict[str, str]:
    return {"dimension": name, "rating": rating, "reason": reason}


def build_reliability_dimensions(
    claims: list[dict[str, Any]],
    rhetoric: list[dict[str, Any]],
    source_checks: list[dict[str, Any]],
    argument_map: dict[str, Any],
) -> list[dict[str, str]]:
    missing = count_status(source_checks, "source_missing")
    not_checkable = count_status(source_checks, "not_checkable")
    supported = count_status(source_checks, "supported") + count_status(source_checks, "partly_supported")
    high_pressure = sum(1 for item in rhetoric if item["substitutes_for_evidence"])

    if not claims:
        source_rating = "unassessable"
        source_reason = "No claims were extracted."
    elif supported > 0 and missing == 0:
        source_rating = "strong"
        source_reason = "Extracted claims have checked support."
    elif not_checkable > 0 and missing == 0:
        source_rating = "unassessable"
        source_reason = "Source references exist, but the local v1 tool did not verify them."
    else:
        source_rating = "weak"
        source_reason = f"{missing} claim(s) lack nearby source references."

    logical_rating = "mixed" if argument_map["inferred_links"] else "unassessable"
    logical_reason = "Heuristic argument links found." if argument_map["inferred_links"] else "No explicit premise/conclusion pattern found."

    rhetoric_rating = "high_pressure" if high_pressure >= 2 else "moderate" if high_pressure == 1 else "low"
    rhetoric_reason = f"{high_pressure} rhetoric finding(s) may substitute for evidence."

    uncertainty_rating = "weak" if missing or not_checkable else "mixed"
    uncertainty_reason = "Unverified or missing source support remains." if (missing or not_checkable) else "No obvious unresolved source-status placeholders."

    return [
        dimension("source_grounding", source_rating, source_reason),
        dimension("logical_coherence", logical_rating, logical_reason),
        dimension("transparency", "mixed", "The local tool exposes quote spans and source-status limitations."),
        dimension("rhetorical_pressure", rhetoric_rating, rhetoric_reason),
        dimension("uncertainty_handling", uncertainty_rating, uncertainty_reason),
        dimension("fact_checkability", "mixed" if claims else "unassessable", "Claims are sentence anchored; external verification is a separate step."),
    ]


def build_input_summary(inputs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "input_count": len(inputs),
        "inputs": [
            {
                "input_id": item["input_id"],
                "title": item["title"],
                "characters": len(item["text"]),
                "word_count": len(item["text"].split()),
                "metadata": item["metadata"],
            }
            for item in inputs
        ],
    }


def combined_input_text(inputs: list[dict[str, Any]]) -> str:
    return "\n\n".join(str(item.get("text", "")) for item in inputs)


def unique_numbers(values: list[float]) -> list[float]:
    unique: list[float] = []
    for value in values:
        if all(abs(value - existing) > 0.0001 for existing in unique):
            unique.append(value)
    return unique


def extract_productivity_model_inputs(text: str) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    base_match = re.search(r"=\s*ca\.?\s*([\d\s,.]+)\s*mrd", text, re.I)
    if base_match:
        extracted["base_gdp_bn"] = parse_number(base_match.group(1))

    deficit_match = re.search(
        r"underskudd\s+til\s+([\d\s,.]+)\s*mrd.*?tilsvarende\s+([\d\s,.]+)\s*prosent",
        text,
        re.I | re.S,
    )
    if deficit_match:
        structural_deficit_bn = parse_number(deficit_match.group(1))
        structural_deficit_share_pct = parse_number(deficit_match.group(2))
        extracted["structural_deficit_bn"] = structural_deficit_bn
        extracted["structural_deficit_share_pct"] = structural_deficit_share_pct
        if extracted.get("base_gdp_bn") is None and structural_deficit_bn is not None and structural_deficit_share_pct:
            extracted["base_gdp_bn"] = structural_deficit_bn / (structural_deficit_share_pct / 100)

    fiscal_gap_match = re.search(r"inndekningsbehovet.*?([\d\s,.]+)\s*prosent", text, re.I | re.S)
    if fiscal_gap_match:
        extracted["fiscal_gap_share_pct"] = parse_number(fiscal_gap_match.group(1))

    deltas: list[float] = []
    for match in re.finditer(r"(\d+(?:[,.]\d+)?)(?:\s*-\s*(\d+(?:[,.]\d+)?))?\s*prosentpoeng", text, re.I):
        first = parse_number(match.group(1))
        second = parse_number(match.group(2))
        if first is not None:
            deltas.append(first)
        if second is not None:
            deltas.append(second)
    if deltas:
        extracted["productivity_deltas_pp"] = unique_numbers(deltas)
    return extracted


def productivity_policy(policy: dict[str, Any]) -> dict[str, Any]:
    candidate = policy.get("productivity_model")
    return candidate if isinstance(candidate, dict) else {}


def build_quantitative_models(inputs: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    text = combined_input_text(inputs)
    model_policy = productivity_policy(policy)
    extracted = extract_productivity_model_inputs(text)
    base_gdp_bn = parse_number(model_policy.get("base_gdp_bn")) or extracted.get("base_gdp_bn")
    has_productivity_context = bool(re.search(r"produktivit|productivit|Fastlands-BNP|mainland GDP", text, re.I))
    if base_gdp_bn is None or not has_productivity_context:
        return []

    years = int(parse_number(model_policy.get("years")) or 10)
    base_growth_pct = parse_number(model_policy.get("base_growth_pct")) or 0.0
    policy_deltas = model_policy.get("productivity_deltas_pp")
    deltas = []
    if isinstance(policy_deltas, list):
        deltas = [value for value in (parse_number(item) for item in policy_deltas) if value is not None]
    elif policy_deltas is not None:
        parsed_delta = parse_number(policy_deltas)
        if parsed_delta is not None:
            deltas = [parsed_delta]
    if not deltas:
        deltas = extracted.get("productivity_deltas_pp") or DEFAULT_PRODUCTIVITY_DELTAS_PP
    deltas = unique_numbers([float(delta) for delta in deltas])

    base_growth = base_growth_pct / 100
    scenarios: list[dict[str, Any]] = []
    for delta_pp in deltas:
        delta = delta_pp / 100
        baseline_level_bn = base_gdp_bn * ((1 + base_growth) ** years)
        improved_level_bn = base_gdp_bn * ((1 + base_growth + delta) ** years)
        additional_level_bn = improved_level_bn - baseline_level_bn
        simple_approximation_bn = base_gdp_bn * delta * years
        scenarios.append(
            {
                "delta_pp": round(delta_pp, 6),
                "years": years,
                "base_growth_pct": round(base_growth_pct, 6),
                "baseline_level_bn": round(baseline_level_bn, 3),
                "improved_level_bn": round(improved_level_bn, 3),
                "additional_level_bn": round(additional_level_bn, 3),
                "simple_approximation_bn": round(simple_approximation_bn, 3),
                "compound_formula": "base_gdp_bn * ((1 + base_growth + delta) ** years - (1 + base_growth) ** years)",
            }
        )

    fiscal_gap_share_pct = parse_number(model_policy.get("fiscal_gap_share_pct")) or extracted.get("fiscal_gap_share_pct")
    fiscal_gap_equivalent_bn = None
    if fiscal_gap_share_pct is not None:
        fiscal_gap_equivalent_bn = round(base_gdp_bn * (fiscal_gap_share_pct / 100), 3)

    return [
        {
            "schema": "haven.text_reliability.quantitative_model.v1",
            "model_id": "productivity-compound-level-effect",
            "kind": "productivity_compound_level_effect",
            "status": "calculated",
            "base_gdp_bn": round(base_gdp_bn, 3),
            "base_gdp_source": "policy" if model_policy.get("base_gdp_bn") is not None else "text_extraction",
            "years": years,
            "base_growth_pct": round(base_growth_pct, 6),
            "fiscal_gap_share_pct": round(fiscal_gap_share_pct, 6) if fiscal_gap_share_pct is not None else None,
            "fiscal_gap_equivalent_bn": fiscal_gap_equivalent_bn,
            "structural_deficit_bn": extracted.get("structural_deficit_bn"),
            "structural_deficit_share_pct": extracted.get("structural_deficit_share_pct"),
            "scenarios": scenarios,
            "limitations": [
                "This is a level-effect model, not a full macroeconomic forecast.",
                "It does not attribute causality to innovation without a separate empirical model.",
                "Base GDP, growth and fiscal-gap values should be source-audited before high-stakes use.",
            ],
        }
    ]


def build_add2entity_sidecar(capture: dict[str, Any] | None, analysis_id: str, analysis: dict[str, Any]) -> dict[str, Any] | None:
    if capture is None:
        return None
    target = capture.get("target") if isinstance(capture.get("target"), dict) else {}
    summary = {
        "claimCount": len(analysis["claim_ledger"]),
        "sourceMissingCount": count_status(analysis["source_checks"], "source_missing"),
        "notCheckableCount": count_status(analysis["source_checks"], "not_checkable"),
        "rhetoricFindingCount": len(analysis["rhetoric_findings"]),
    }
    return {
        "schema": ADD2ENTITY_SIDECAR_SCHEMA,
        "captureID": capture.get("captureID"),
        "analysisSchema": ANALYSIS_SCHEMA,
        "analysisID": analysis_id,
        "mutatesEntity": False,
        "target": {
            "kind": target.get("kind"),
            "projectID": target.get("projectID"),
            "cellEndpoint": target.get("cellEndpoint"),
        },
        "rag": capture.get("rag"),
        "summary": summary,
    }


def analyze(inputs: list[dict[str, Any]], policy: dict[str, Any] | None = None, add2entity_capture: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = {
        "source_mode": "verifying",
        "language": "auto",
        "jurisdiction": None,
        "high_stakes": False,
        "human_review_required": True,
        "allowed_domains": [],
        "productivity_model": {},
        **(policy or {}),
    }
    markdown_structure = extract_markdown_structure(inputs)
    claims = extract_claims(inputs, markdown_structure)
    argument_map = build_argument_map(claims)
    source_audits = build_source_audits(claims, policy)
    annotate_claims_with_source_audits(claims, source_audits)
    source_checks = source_checks_from_audits(source_audits)
    claim_clusters = build_claim_clusters(claims, markdown_structure, source_audits)
    claim_source_matrix = build_claim_source_matrix(claims, source_audits, markdown_structure)
    argument_graph = build_argument_graph(claims, claim_clusters, argument_map)
    rhetoric = extract_rhetoric(inputs)
    quantitative_models = build_quantitative_models(inputs, policy)
    analysis_id = f"analysis-{stable_hash(json.dumps(build_input_summary(inputs), sort_keys=True))}"
    analysis: dict[str, Any] = {
        "schema": ANALYSIS_SCHEMA,
        "analysis_id": analysis_id,
        "generated_at": utc_now_iso(),
        "policy": policy,
        "input_summary": build_input_summary(inputs),
        "markdown_structure": markdown_structure,
        "claim_ledger": claims,
        "claim_clusters": claim_clusters,
        "claim_source_matrix": claim_source_matrix,
        "argument_map": argument_map,
        "argument_graph": argument_graph,
        "rhetoric_findings": rhetoric,
        "source_audits": source_audits,
        "source_checks": source_checks,
        "contrary_evidence": [],
        "quantitative_models": quantitative_models,
        "reliability_dimensions": build_reliability_dimensions(claims, rhetoric, source_checks, argument_map),
        "uncertainties": [
            "The local v1 tool does not verify external sources.",
            "Deep argument reconstruction requires model or human review.",
            "Quantitative productivity models are sizing models unless a source-auditor validates inputs and an empirical model validates attribution.",
        ],
        "audit_log": [
            {"step": "intake", "status": "completed", "detail": "Normalized inputs and metadata."},
            {"step": "markdown_structure", "status": "completed", "detail": "Parsed headings, tables and code fences before claim extraction."},
            {"step": "quote_anchoring", "status": "completed", "detail": "Claims and rhetoric findings use exact input spans."},
            {"step": "source_auditor", "status": "limited", "detail": "Classified per-claim source audit status without web or RAG fetching."},
            {"step": "claim_clustering", "status": "completed", "detail": "Grouped claims by markdown section for review and RAG routing."},
            {"step": "argument_graph", "status": "completed", "detail": "Built deterministic graph nodes, edges and Mermaid source from clusters and heuristic links."},
            {"step": "quantitative_model", "status": "completed" if quantitative_models else "skipped", "detail": "Built productivity sizing model when inputs were available."},
            {"step": "adjudication", "status": "limited", "detail": "Deterministic dimensions are preliminary and require review for high-stakes use."},
        ],
    }
    sidecar = build_add2entity_sidecar(add2entity_capture, analysis_id, analysis)
    if sidecar is not None:
        analysis["add2entity_sidecar"] = sidecar
    return analysis


def markdown_cell(value: Any, limit: int = 140) -> str:
    if isinstance(value, list):
        rendered = ", ".join(str(item) for item in value)
    elif value is None:
        rendered = ""
    else:
        rendered = str(value)
    rendered = re.sub(r"\s+", " ", rendered).strip()
    if len(rendered) > limit:
        rendered = f"{rendered[: limit - 3]}..."
    return rendered.replace("|", "\\|")


def render_report(analysis: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Text Reliability Analysis Report")
    lines.append("")
    lines.append(f"- Schema: `{analysis['schema']}`")
    lines.append(f"- Analysis ID: `{analysis['analysis_id']}`")
    lines.append(f"- Generated at: `{analysis['generated_at']}`")
    lines.append(f"- Source mode: `{analysis['policy']['source_mode']}`")
    lines.append("")
    lines.append("## Inputs")
    for item in analysis["input_summary"]["inputs"]:
        lines.append(f"- `{item['input_id']}`: {item['title']} ({item['word_count']} words)")
    lines.append("")
    lines.append("## Markdown Structure")
    structure = analysis.get("markdown_structure", {})
    lines.append(f"- Sections: `{len(structure.get('sections', []))}`")
    lines.append(f"- Tables: `{len(structure.get('tables', []))}`")
    lines.append("")
    lines.append("## Claims")
    for claim in analysis["claim_ledger"]:
        cluster = claim.get("claim_cluster_id", "unclustered")
        source_status = claim.get("source_audit_status", "unknown")
        lines.append(
            f"- `{claim['claim_id']}` `{cluster}` `{claim['claim_type']}` `{claim['strength']}` "
            f"`{source_status}`: \"{claim['quote']}\""
        )
    lines.append("")
    lines.append("## Claim Clusters")
    if analysis.get("claim_clusters"):
        lines.append("| Cluster | Title | Claims | Source audit statuses | Representative claims |")
        lines.append("| --- | --- | ---: | --- | --- |")
        for cluster in analysis["claim_clusters"]:
            status_summary = ", ".join(f"{key}:{value}" for key, value in cluster["source_audit_status_counts"].items())
            reps = " / ".join(item["claim_id"] for item in cluster["representative_claims"])
            lines.append(
                f"| `{cluster['cluster_id']}` | {markdown_cell(cluster['title'])} | {cluster['claim_count']} | "
                f"{markdown_cell(status_summary)} | {markdown_cell(reps)} |"
            )
    else:
        lines.append("- No claim clusters.")
    lines.append("")
    lines.append("## Claim Source Matrix")
    if analysis.get("claim_source_matrix"):
        lines.append("| Claim | Cluster | Section | Type | Audit status | Evidence grade | Sources | Quote |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in analysis["claim_source_matrix"]:
            refs = [ref.get("value") or ref.get("quote") for ref in row.get("source_refs", [])]
            lines.append(
                f"| `{row['claim_id']}` | `{row.get('claim_cluster_id') or ''}` | {markdown_cell(row.get('section_title'))} | "
                f"{markdown_cell(row.get('claim_type'))} | `{markdown_cell(row.get('source_audit_status'))}` | "
                f"{markdown_cell(row.get('evidence_grade'))} | {markdown_cell(refs, 90)} | {markdown_cell(row.get('quote'), 120)} |"
            )
    else:
        lines.append("- No claim-source rows.")
    lines.append("")
    lines.append("## Source Checks")
    for check in analysis["source_checks"]:
        lines.append(
            f"- `{check['claim_id']}`: `{check['status']}` / `{check.get('source_audit_status')}` - {check['reason']}"
        )
    lines.append("")
    lines.append("## Argument Graph")
    graph = analysis.get("argument_graph", {})
    if graph:
        lines.append(f"- Nodes: `{len(graph.get('nodes', []))}`")
        lines.append(f"- Edges: `{len(graph.get('edges', []))}`")
        lines.append("")
        lines.append("```mermaid")
        lines.append(graph.get("mermaid", "flowchart TD"))
        lines.append("```")
    else:
        lines.append("- No argument graph.")
    lines.append("")
    lines.append("## Quantitative Models")
    if analysis.get("quantitative_models"):
        for model in analysis["quantitative_models"]:
            lines.append(f"### {model['model_id']}")
            lines.append("")
            lines.append(f"- Kind: `{model['kind']}`")
            lines.append(f"- Base GDP (bn): `{model['base_gdp_bn']}`")
            lines.append(f"- Years: `{model['years']}`")
            lines.append(f"- Base growth pct: `{model['base_growth_pct']}`")
            if model.get("fiscal_gap_equivalent_bn") is not None:
                lines.append(f"- Fiscal gap equivalent (bn): `{model['fiscal_gap_equivalent_bn']}`")
            lines.append("")
            lines.append("| Delta pp | Additional level bn | Baseline level bn | Improved level bn |")
            lines.append("| ---: | ---: | ---: | ---: |")
            for scenario in model.get("scenarios", []):
                lines.append(
                    f"| {scenario['delta_pp']} | {scenario['additional_level_bn']} | "
                    f"{scenario['baseline_level_bn']} | {scenario['improved_level_bn']} |"
                )
    else:
        lines.append("- No quantitative model inputs found.")
    lines.append("")
    lines.append("## Rhetoric")
    if analysis["rhetoric_findings"]:
        for finding in analysis["rhetoric_findings"]:
            lines.append(f"- `{finding['rhetoric_type']}`: \"{finding['quote']}\"")
    else:
        lines.append("- No heuristic rhetoric findings.")
    lines.append("")
    lines.append("## Reliability Dimensions")
    for item in analysis["reliability_dimensions"]:
        lines.append(f"- `{item['dimension']}`: `{item['rating']}` - {item['reason']}")
    lines.append("")
    lines.append("## Boundaries")
    for uncertainty in analysis["uncertainties"]:
        lines.append(f"- {uncertainty}")
    lines.append("")
    return "\n".join(lines)


def parse_cli_float(value: str) -> float:
    parsed = parse_number(value)
    if parsed is None:
        raise argparse.ArgumentTypeError(f"expected numeric value, got {value!r}")
    return parsed


def parse_policy_args(args: argparse.Namespace) -> dict[str, Any]:
    productivity_model = {
        "base_gdp_bn": args.base_gdp_bn,
        "base_growth_pct": args.base_growth_pct,
        "years": args.model_years,
        "productivity_deltas_pp": args.productivity_delta_pp or [],
        "fiscal_gap_share_pct": args.fiscal_gap_share_pct,
    }
    productivity_model = {key: value for key, value in productivity_model.items() if value not in (None, [])}
    return {
        "source_mode": args.source_mode,
        "language": args.language,
        "jurisdiction": args.jurisdiction,
        "high_stakes": args.high_stakes,
        "human_review_required": args.human_review_required or args.high_stakes,
        "allowed_domains": args.allowed_domain or [],
        "productivity_model": productivity_model,
    }


def write_outputs(analysis: dict[str, Any], out_json: Path | None, out_md: Path | None) -> None:
    encoded = json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True)
    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(f"{encoded}\n", encoding="utf-8")
    else:
        print(encoded)
    if out_md:
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_report(analysis), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze text reliability with local deterministic v1 heuristics.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text-file", type=Path, help="Plain text file to analyze.")
    source.add_argument("--input-json", type=Path, help="haven.text_reliability.input_set.v1 JSON file.")
    source.add_argument("--add2entity-capture", type=Path, help="haven.add2entity.webpage-capture.v1 JSON file.")
    parser.add_argument("--title", help="Title for --text-file input.")
    parser.add_argument("--source-mode", choices=["text_only", "verifying", "investigative"], default="verifying")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--jurisdiction")
    parser.add_argument("--high-stakes", action="store_true")
    parser.add_argument("--human-review-required", action="store_true")
    parser.add_argument("--allowed-domain", action="append")
    parser.add_argument("--base-gdp-bn", type=parse_cli_float, help="Base GDP/production level in billions for productivity scenarios.")
    parser.add_argument("--base-growth-pct", type=parse_cli_float, help="Baseline annual growth rate in percent for productivity scenarios.")
    parser.add_argument("--productivity-delta-pp", type=parse_cli_float, action="append", help="Additional annual productivity growth in percentage points. Repeat for multiple scenarios.")
    parser.add_argument("--model-years", type=int, help="Number of years for productivity scenarios.")
    parser.add_argument("--fiscal-gap-share-pct", type=parse_cli_float, help="Fiscal gap share of base GDP in percent.")
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-md", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    add2entity_capture = None
    try:
        if args.text_file:
            inputs = [input_from_text_file(args.text_file, args.title)]
        elif args.add2entity_capture:
            add2entity_capture = load_json(args.add2entity_capture)
            inputs = [input_from_add2entity_capture(add2entity_capture)]
        else:
            inputs, add2entity_capture = load_input_set(args.input_json)
        analysis = analyze(inputs, parse_policy_args(args), add2entity_capture=add2entity_capture)
        write_outputs(analysis, args.out_json, args.out_md)
        return 0
    except Exception as error:  # noqa: BLE001 - CLI should print concise user-facing errors.
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
