#!/usr/bin/env python3
"""Run the deterministic Agent Continuity fixture and ablation corpus."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

import validate_contract as validator


MANIFEST_VERSION = "agent-continuity.deterministic-eval-manifest.v1"


class ManifestError(ValueError):
    pass


def _pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ManifestError(f"JSON pointer must start with '/': {pointer!r}")
    if pointer == "/":
        return [""]
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def _parent_for_pointer(document: Any, pointer: str) -> tuple[Any, str]:
    parts = _pointer_parts(pointer)
    current = document
    for part in parts[:-1]:
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError) as error:
                raise ManifestError(f"invalid list pointer {pointer!r}") from error
        elif isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise ManifestError(f"pointer does not resolve: {pointer!r}")
    return current, parts[-1]


def apply_mutations(document: dict[str, Any], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(document)
    for mutation in mutations:
        if not isinstance(mutation, dict):
            raise ManifestError("mutation must be an object")
        operation = mutation.get("op")
        pointer = mutation.get("path")
        if not isinstance(pointer, str):
            raise ManifestError("mutation.path must be a string")
        parent, key = _parent_for_pointer(result, pointer)
        if operation == "set":
            if isinstance(parent, list):
                try:
                    parent[int(key)] = copy.deepcopy(mutation.get("value"))
                except (ValueError, IndexError) as error:
                    raise ManifestError(f"invalid list pointer {pointer!r}") from error
            elif isinstance(parent, dict):
                parent[key] = copy.deepcopy(mutation.get("value"))
            else:
                raise ManifestError(f"pointer parent is not a container: {pointer!r}")
        elif operation == "remove":
            if isinstance(parent, list):
                try:
                    del parent[int(key)]
                except (ValueError, IndexError) as error:
                    raise ManifestError(f"invalid list pointer {pointer!r}") from error
            elif isinstance(parent, dict) and key in parent:
                del parent[key]
            else:
                raise ManifestError(f"pointer does not resolve for removal: {pointer!r}")
        else:
            raise ManifestError(f"unsupported mutation operation: {operation!r}")
    return result


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_VERSION:
        raise ManifestError(f"manifest schema must be {MANIFEST_VERSION!r}")
    if not isinstance(manifest.get("cases"), list):
        raise ManifestError("manifest.cases must be an array")
    return manifest


def _case_bytes(case: dict[str, Any], root: Path) -> bytes:
    fixture = case.get("fixture")
    if not isinstance(fixture, str):
        raise ManifestError("case.fixture must be a string")
    fixture_path = (root / fixture).resolve()
    try:
        fixture_path.relative_to(root.resolve())
    except ValueError as error:
        raise ManifestError(f"fixture escapes tool root: {fixture!r}") from error
    raw = fixture_path.read_bytes()
    mutations = case.get("mutations", [])
    payload, parse_issues = validator.parse_contract_bytes(raw)
    if payload is None:
        if not mutations:
            return raw
        details = "; ".join(str(issue) for issue in parse_issues)
        raise ManifestError(f"cannot mutate invalid fixture {fixture!r}: {details}")
    if not isinstance(mutations, list):
        raise ManifestError("case.mutations must be an array")
    mutated = apply_mutations(payload, mutations) if mutations else payload
    return json.dumps(mutated, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def evaluate_manifest(manifest: dict[str, Any], tool_root: Path) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    false_positives: list[str] = []
    false_negatives: list[str] = []
    expectation_mismatches: list[str] = []
    probe_coverage: dict[str, int] = {}

    for case in manifest["cases"]:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise ManifestError("every case must be an object with a string id")
        case_id = case["id"]
        raw = _case_bytes(case, tool_root)
        receipt, exit_code = validator.validate_bytes(raw)
        expected = case.get("expected")
        if not isinstance(expected, dict) or not isinstance(expected.get("contractValid"), bool):
            raise ManifestError(f"case {case_id!r} needs expected.contractValid")

        actual_codes = sorted(
            {item["code"] for item in receipt["errors"] + receipt["warnings"]}
        )
        expected_codes = sorted(set(expected.get("issueCodes", [])))
        matched = (
            receipt["contractValid"] == expected["contractValid"]
            and receipt["continuationDisposition"] == expected.get("disposition")
            and actual_codes == expected_codes
        )
        if expected["contractValid"] and not receipt["contractValid"]:
            false_positives.append(case_id)
        if not expected["contractValid"] and receipt["contractValid"]:
            false_negatives.append(case_id)
        if not matched:
            expectation_mismatches.append(case_id)

        probe_types = case.get("probeTypes", [])
        if not isinstance(probe_types, list):
            raise ManifestError(f"case {case_id!r} probeTypes must be an array")
        for probe_type in probe_types:
            if isinstance(probe_type, str):
                probe_coverage[probe_type] = probe_coverage.get(probe_type, 0) + 1

        decoded = raw.decode("utf-8", errors="replace")
        results.append(
            {
                "id": case_id,
                "matchedExpectation": matched,
                "contractValid": receipt["contractValid"],
                "disposition": receipt["continuationDisposition"],
                "issueCodes": actual_codes,
                "inputBytes": len(raw),
                "inputCharacters": len(decoded),
                "lexicalTokenProxy": len(re.findall(r"\w+|[^\w\s]", decoded, flags=re.UNICODE)),
                "probeTypes": probe_types,
            }
        )

    return {
        "reportType": "agent-continuity.deterministic-eval-report.v1",
        "manifestSchema": manifest["schema"],
        "validatorVersion": validator.TOOL_VERSION,
        "caseCount": len(results),
        "matchedCount": sum(1 for item in results if item["matchedExpectation"]),
        "falsePositiveCaseIDs": false_positives,
        "falseNegativeCaseIDs": false_negatives,
        "expectationMismatchCaseIDs": expectation_mismatches,
        "probeCoverage": dict(sorted(probe_coverage.items())),
        "tokenMetricStatus": "proxy-only-not-comparable-to-provider-tokenizers",
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parent / "evaluation" / "deterministic_manifest.v1.json",
    )
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        report = evaluate_manifest(manifest, Path(__file__).resolve().parent)
    except (OSError, json.JSONDecodeError, ManifestError) as error:
        print(f"evaluation failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not report["expectationMismatchCaseIDs"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
