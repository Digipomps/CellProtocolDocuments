#!/usr/bin/env python3
"""Deterministic reference transformer for RAG prompt packages.

This is a local contract tool, not a model runner. It adapts a RAG source
package to a target model profile and emits a prompt package suitable for a
provider invocation boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PROMPT_PACKAGE_VERSION = 1
DEFAULT_MAX_CHARS_PER_CHUNK = 1800


MODEL_PROFILES: dict[str, dict[str, Any]] = {
    "qwen3-8b-q4": {
        "family": "qwen3",
        "language": "no",
        "format": "six_numbered_points",
        "maxWords": 550,
        "includeNoThink": True,
        "citationStyle": "path_lines",
        "tone": "compact_technical",
    },
    "qwen3-1.7b-q8": {
        "family": "qwen3",
        "language": "no",
        "format": "six_numbered_points",
        "maxWords": 420,
        "includeNoThink": True,
        "citationStyle": "path_lines",
        "tone": "compact_technical",
    },
    "gemma4-e2b-qat-mlx": {
        "family": "gemma4",
        "language": "no",
        "format": "six_numbered_points",
        "maxWords": 520,
        "includeNoThink": False,
        "citationStyle": "path_lines",
        "tone": "source_explicit",
    },
    "gemma4-e4b-qat-mlx": {
        "family": "gemma4",
        "language": "no",
        "format": "six_numbered_points",
        "maxWords": 520,
        "includeNoThink": False,
        "citationStyle": "path_lines",
        "tone": "source_explicit",
    },
    "default": {
        "family": "unknown",
        "language": "no",
        "format": "six_numbered_points",
        "maxWords": 500,
        "includeNoThink": False,
        "citationStyle": "path_lines",
        "tone": "compact_technical",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit(f"{path}: expected JSON object")
    return payload


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def truncate_text(text: str, max_chars: int) -> str:
    text = str(text or "").strip()
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 32)].rstrip() + "\n\n[truncated]"


def normalize_line(chunk: dict[str, Any], key: str, fallback: str = "") -> str:
    value = chunk.get(key, fallback)
    if value is None:
        return fallback
    return str(value)


def chunk_ref(chunk: dict[str, Any]) -> str:
    path = normalize_line(chunk, "path", "unknown")
    start = normalize_line(chunk, "lineStart", normalize_line(chunk, "line_start", "?"))
    end = normalize_line(chunk, "lineEnd", normalize_line(chunk, "line_end", "?"))
    return f"{path}:{start}-{end}"


def resolve_profile(request: dict[str, Any]) -> dict[str, Any]:
    target = request.get("targetModel", {})
    if not isinstance(target, dict):
        target = {}
    model_id = str(target.get("modelID", "default"))
    profile = dict(MODEL_PROFILES.get(model_id, MODEL_PROFILES["default"]))
    profile.update({key: value for key, value in target.items() if value not in (None, "")})

    answer_style = request.get("answerStyle", {})
    if isinstance(answer_style, dict):
        for key in ("language", "format", "maxWords"):
            if key in answer_style:
                profile[key] = answer_style[key]
    profile["modelID"] = model_id
    return profile


def source_chunks(request: dict[str, Any]) -> list[dict[str, Any]]:
    rag = request.get("rag", {})
    chunks = rag.get("chunks") if isinstance(rag, dict) else []
    if not isinstance(chunks, list):
        raise SystemExit("request.rag.chunks must be a list")
    normalized: list[dict[str, Any]] = []
    for chunk in chunks:
        if isinstance(chunk, dict):
            normalized.append(chunk)
    if not normalized:
        raise SystemExit("request.rag.chunks must contain at least one object chunk")
    return normalized


def build_ground_truth(chunks: list[dict[str, Any]], max_chars_per_chunk: int) -> str:
    blocks: list[str] = []
    for chunk in chunks:
        ref = chunk_ref(chunk)
        heading = normalize_line(chunk, "heading", "")
        text = truncate_text(normalize_line(chunk, "text", ""), max_chars_per_chunk)
        blocks.append("\n".join([f"### {ref}", f"Heading: {heading}", text]).strip())
    return "\n\n".join(blocks)


def coverage_warnings(request: dict[str, Any], chunks: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    rag = request.get("rag", {})
    if isinstance(rag, dict):
        supplied = rag.get("coverageWarnings", [])
        if isinstance(supplied, list):
            warnings.extend(str(item) for item in supplied)

    paths = {normalize_line(chunk, "path") for chunk in chunks}
    if len(paths) < 2:
        warnings.append("Only one canonical source path is present; citation diversity may be weak.")

    constraints = request.get("constraints", {})
    must_cover = constraints.get("mustCover", []) if isinstance(constraints, dict) else []
    haystack = " ".join(normalize_line(chunk, "text") for chunk in chunks).lower()
    iterable_must_cover = must_cover if isinstance(must_cover, list) else []
    for item in iterable_must_cover:
        terms = re.findall(r"[\w./:-]+", str(item).lower())
        if terms and not any(term in haystack for term in terms):
            warnings.append(f"Required topic may be under-covered by retrieved chunks: {item}")
    return sorted(set(warnings))


def quality_checks(request: dict[str, Any]) -> list[dict[str, Any]]:
    constraints = request.get("constraints", {})
    must_cover = constraints.get("mustCover", []) if isinstance(constraints, dict) else []
    forbidden = constraints.get("forbiddenClaims", []) if isinstance(constraints, dict) else []
    checks: list[dict[str, Any]] = [
        {
            "id": "uses_canonical_citations",
            "description": "Answer cites canonical source paths with line ranges.",
            "requiredPattern": "Book/.*\\.md:\\d+-\\d+"
        },
        {
            "id": "states_missing_ground_truth",
            "description": "Answer says when a requested fact is not present in ground truth.",
        },
    ]
    for index, item in enumerate(must_cover if isinstance(must_cover, list) else [], start=1):
        checks.append(
            {
                "id": f"covers_required_topic_{index}",
                "description": f"Answer covers required topic: {item}",
                "requiredTopic": str(item),
            }
        )
    for index, item in enumerate(forbidden if isinstance(forbidden, list) else [], start=1):
        checks.append(
            {
                "id": f"avoids_forbidden_claim_{index}",
                "description": f"Answer avoids unsupported claim area: {item}",
                "forbiddenTopic": str(item),
            }
        )
    return checks


def build_system_prompt(profile: dict[str, Any]) -> str:
    language = profile.get("language", "no")
    max_words = profile.get("maxWords", 500)
    lines = [
        "Du er en HAVEN dokumentasjonsassistent.",
        "Bruk bare GROUND TRUTH nedenfor som faktagrunnlag.",
        "Hvis noe ikke finnes i kildene, si at det mangler i grunnlaget.",
        f"Svar paa {language} for en utvikler eller en annen spraakmodell.",
        "Ikke finn opp elementtyper, runtime-egenskaper eller sikkerhetsregler.",
        "Inkluder korte kildehenvisninger med Book/..:linjer.",
        f"Hold svaret kompakt og komplett: 6 nummererte punkter, maks ca. {max_words} ord.",
    ]
    if profile.get("tone") == "source_explicit":
        lines.append("Prioriter presise kildehenvisninger fremfor flytende prosa.")
    return "\n".join(lines)


def build_user_prompt(request: dict[str, Any], profile: dict[str, Any], ground_truth: str) -> str:
    constraints = request.get("constraints", {})
    must_cover = constraints.get("mustCover", []) if isinstance(constraints, dict) else []
    question = str(request.get("question", "")).strip()
    lines: list[str] = []
    if profile.get("includeNoThink"):
        lines.append("/no_think")
        lines.append("")
    lines.extend(
        [
            "GROUND TRUTH:",
            ground_truth,
            "",
            "OPPGAVE:",
            question,
            "",
            "Maa dekke:",
        ]
    )
    iterable_must_cover = must_cover if isinstance(must_cover, list) else []
    for item in iterable_must_cover:
        lines.append(f"- {item}")
    lines.extend(
        [
            "Bruk minst en kildehenvisning fra hver relevante kanoniske kilde.",
            "Ikke bruk kunnskap utenfor GROUND TRUTH.",
        ]
    )
    return "\n".join(lines).strip()


def transform(request: dict[str, Any], max_chars_per_chunk: int = DEFAULT_MAX_CHARS_PER_CHUNK) -> dict[str, Any]:
    profile = resolve_profile(request)
    chunks = source_chunks(request)
    ground_truth = build_ground_truth(chunks, max_chars_per_chunk)
    system_prompt = build_system_prompt(profile)
    user_prompt = build_user_prompt(request, profile, ground_truth)
    warnings = coverage_warnings(request, chunks)
    source_refs = [chunk_ref(chunk) for chunk in chunks]
    constraints = request.get("constraints", {})
    data_class = "internal_non_sensitive"
    if isinstance(constraints, dict) and constraints.get("dataClass"):
        data_class = str(constraints["dataClass"])

    prompt_material = {
        "systemPrompt": system_prompt,
        "userPrompt": user_prompt,
        "targetModel": profile,
        "sourceChunkRefs": source_refs,
    }
    return {
        "status": "ready" if not warnings else "ready_with_warnings",
        "promptPackageVersion": PROMPT_PACKAGE_VERSION,
        "targetModel": {
            "modelID": profile.get("modelID", "default"),
            "family": profile.get("family", "unknown"),
            "providerID": profile.get("providerID"),
            "route": profile.get("route"),
        },
        "systemPrompt": system_prompt,
        "userPrompt": user_prompt,
        "citationPolicy": {
            "required": True,
            "minimumSources": min(2, len(set(ref.split(":", 1)[0] for ref in source_refs))),
            "canonicalPathsOnly": True,
            "style": profile.get("citationStyle", "path_lines"),
        },
        "qualityChecks": quality_checks(request),
        "promptManifest": {
            "promptHash": sha256_text(canonical_json(prompt_material)),
            "sourceChunkRefs": source_refs,
            "dataClass": data_class,
            "retentionClass": "hash_only",
            "transformerVersion": "rag-prompt-transformer-v0",
        },
        "warnings": warnings,
    }


def sample_request() -> dict[str, Any]:
    return {
        "question": "Forklar hvordan CellProtocol Skeleton virker.",
        "purposeRef": "purpose://docs.rag.answer-with-citations",
        "targetModel": {
            "modelID": "qwen3-8b-q4",
            "providerID": "haven-local-m5",
            "route": "local-gguf",
            "family": "qwen3",
        },
        "answerStyle": {
            "language": "norsk",
            "format": "six_numbered_points",
            "maxWords": 550,
        },
        "rag": {
            "query": "CellProtocol Skeleton Explore owner access",
            "chunks": [
                {
                    "path": "Book/12_Skeleton_Spec.md",
                    "heading": "1. Encoding Rule (All Elements)",
                    "lineStart": 37,
                    "lineEnd": 59,
                    "text": "Each element is encoded as a single-key object where the key is the element type and the value is that element's payload.",
                    "score": 18.2,
                },
                {
                    "path": "Book/22_Explore_Contracts_For_Skeleton_Authoring.md",
                    "heading": "Skeleton Binding Rules",
                    "lineStart": 165,
                    "lineEnd": 221,
                    "text": "Skeleton authoring must validate every remote binding before preview or commit. Text.keypath matches get; Button.keypath with payload matches set.",
                    "score": 16.8,
                },
            ],
            "coverageWarnings": [],
        },
        "constraints": {
            "dataClass": "internal_non_sensitive",
            "mustCover": [
                "single-key JSON encoding",
                "Explore validation",
                "owner/entity access",
            ],
            "forbiddenClaims": [
                "unsupported Skeleton element types",
                "uncited implementation claims",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="RAG source package JSON.")
    parser.add_argument("--out", type=Path, help="Output prompt package JSON.")
    parser.add_argument("--sample", action="store_true", help="Use built-in sample request.")
    parser.add_argument("--max-chars-per-chunk", type=int, default=DEFAULT_MAX_CHARS_PER_CHUNK)
    args = parser.parse_args()

    if args.sample:
        request = sample_request()
    elif args.input:
        request = load_json(args.input)
    else:
        raise SystemExit("Provide --input or --sample.")

    package = transform(request, max_chars_per_chunk=args.max_chars_per_chunk)
    text = json.dumps(package, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
