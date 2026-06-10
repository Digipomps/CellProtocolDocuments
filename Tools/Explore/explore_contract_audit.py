#!/usr/bin/env python3
"""Audit Swift cells for missing or weak Explore contracts.

This is a source-level scanner. It does not try to compile Swift or prove
behavior. Its job is to make implicit contracts visible so humans can decide
what to backfill next.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


DEFAULT_SOURCE_DIRS = [
    "Sources/CellBase",
    "Sources/CellApple",
    "Sources/CellVapor",
]


@dataclass
class Call:
    name: str
    file: str
    line: int
    cell_type: str | None
    key: str | None
    raw_key: str | None
    method: str | None
    text: str


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    file: str
    line: int
    cell_type: str | None
    key: str | None
    method: str | None


def iter_swift_files(root: Path, source_dirs: list[str]) -> Iterable[Path]:
    for source_dir in source_dirs:
        candidate = root / source_dir
        if not candidate.exists():
            continue
        yield from sorted(candidate.rglob("*.swift"))


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def nearest_type_name(text: str, index: int) -> str | None:
    prefix = text[:index]
    # Prefer the nearest class/actor. Many Cell files contain helper structs near
    # registration code, and reporting those as the owning Cell makes the audit
    # harder to act on.
    matches = list(re.finditer(r"\b(?:open|public|internal|private|final)?\s*(?:actor|class)\s+([A-Za-z_][A-Za-z0-9_]*)", prefix))
    if not matches:
        matches = list(
            re.finditer(
                r"\b(?:open|public|internal|private|final)?\s*struct\s+([A-Za-z_][A-Za-z0-9_]*)",
                prefix,
            )
        )
    if not matches:
        return None
    return matches[-1].group(1)


def find_calls(text: str, names: Iterable[str]) -> list[tuple[str, int, int, str]]:
    results: list[tuple[str, int, int, str]] = []
    for name in names:
        pattern = re.compile(r"\b" + re.escape(name) + r"\s*\(")
        for match in pattern.finditer(text):
            open_paren = text.find("(", match.start())
            if open_paren == -1:
                continue
            end = find_matching_paren(text, open_paren)
            if end is None:
                continue
            results.append((name, match.start(), end + 1, text[match.start() : end + 1]))
    results.sort(key=lambda item: item[1])
    return results


def find_matching_paren(text: str, open_index: int) -> int | None:
    depth = 0
    in_string = False
    escaped = False
    i = open_index
    while i < len(text):
        char = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return None


def extract_argument(call_text: str, label: str) -> str | None:
    match = re.search(r"\b" + re.escape(label) + r"\s*:\s*", call_text)
    if not match:
        return None
    i = match.end()
    start = i
    depth = 0
    in_string = False
    escaped = False
    while i < len(call_text):
        char = call_text[i]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif char == "," and depth == 0:
                break
        i += 1
    return call_text[start:i].strip()


def normalize_key(raw: str | None) -> tuple[str | None, str | None]:
    if raw is None:
        return None, None
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        inner = raw[1:-1]
        if "\\(" not in inner:
            return inner, raw
    return None, raw


def extract_method(name: str, call_text: str) -> str | None:
    if name.endswith("ForGet") or name == "registerGet":
        return "get"
    if name.endswith("ForSet") or name == "registerSet":
        return "set"
    method_arg = extract_argument(call_text, "method")
    if method_arg:
        match = re.search(r"\.(get|set)\b", method_arg)
        if match:
            return match.group(1)
    return None


def parse_calls(path: Path, repo_root: Path) -> list[Call]:
    text = path.read_text(encoding="utf-8")
    names = [
        "addInterceptForGet",
        "addInterceptForSet",
        "registerExploreContract",
        "registerExploreSchema",
        "registerGet",
        "registerSet",
    ]
    parsed: list[Call] = []
    for name, start, _end, call_text in find_calls(text, names):
        raw_key_arg = extract_argument(call_text, "key")
        key, raw_key = normalize_key(raw_key_arg)
        parsed.append(
            Call(
                name=name,
                file=str(path.relative_to(repo_root)),
                line=line_number(text, start),
                cell_type=nearest_type_name(text, start),
                key=key,
                raw_key=raw_key,
                method=extract_method(name, call_text),
                text=call_text,
            )
        )
    return parsed


def contract_identity(call: Call) -> tuple[str | None, str | None, str | None]:
    return (call.key, call.raw_key, call.method)


def has_explicit_shape(call: Call) -> bool:
    if call.name == "registerExploreContract":
        if call.method == "set" and "input:" not in call.text:
            return False
        if "returns:" not in call.text:
            return False
        return "unknownSchema" not in call.text and 'type: "unknown"' not in call.text
    if call.name == "registerExploreSchema":
        return "returns" in call.text or "payload" in call.text or "input" in call.text
    if call.name == "registerGet":
        return "returns:" in call.text
    if call.name == "registerSet":
        return "input:" in call.text and "returns:" in call.text
    return False


def build_findings(calls: list[Call]) -> list[Finding]:
    explicit: set[tuple[str | None, str | None, str | None]] = set()
    weak_explicit: list[Call] = []
    intercepts: list[Call] = []

    for call in calls:
        if call.name in {"registerExploreContract", "registerExploreSchema", "registerGet", "registerSet"}:
            if has_explicit_shape(call):
                explicit.add(contract_identity(call))
            else:
                weak_explicit.append(call)
        if call.name in {"addInterceptForGet", "addInterceptForSet"}:
            intercepts.append(call)

    findings: list[Finding] = []

    for call in weak_explicit:
        findings.append(
            Finding(
                severity="warn",
                code="weak_explicit_contract",
                message=f"{call.name} advertises {call.method or 'unknown'} key without complete input/returns shape.",
                file=call.file,
                line=call.line,
                cell_type=call.cell_type,
                key=call.key or call.raw_key,
                method=call.method,
            )
        )

    for call in intercepts:
        identity = contract_identity(call)
        if identity in explicit:
            continue
        key_matches = [
            item
            for item in explicit
            if item[2] == call.method and (item[0] == call.key or item[1] == call.raw_key)
        ]
        if key_matches:
            continue
        severity = "error" if call.key else "warn"
        code = "implicit_intercept_contract" if call.key else "dynamic_key_needs_manual_review"
        findings.append(
            Finding(
                severity=severity,
                code=code,
                message=(
                    "Intercept registers a key before an explicit Explore contract. "
                    "It will fall back to default/unknown metadata unless strict mode rejects it."
                ),
                file=call.file,
                line=call.line,
                cell_type=call.cell_type,
                key=call.key or call.raw_key,
                method=call.method,
            )
        )

    return sorted(findings, key=lambda item: (item.file, item.line, item.code))


def render_markdown(repo_root: Path, calls: list[Call], findings: list[Finding]) -> str:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1

    lines = [
        "# Explore Contract Audit",
        "",
        f"Source root: `{repo_root}`",
        "",
        "## Summary",
        "",
        f"- Calls inspected: {len(calls)}",
        f"- Findings: {len(findings)}",
        f"- Errors: {counts.get('error', 0)}",
        f"- Warnings: {counts.get('warn', 0)}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"

    for finding in findings:
        location = f"{finding.file}:{finding.line}"
        key = finding.key or "(unknown key)"
        method = finding.method or "unknown"
        cell_type = finding.cell_type or "unknown type"
        lines.extend(
            [
                f"### {finding.severity.upper()} {finding.code}",
                "",
                f"- Location: `{location}`",
                f"- Cell/type: `{cell_type}`",
                f"- Key: `{key}`",
                f"- Method: `{method}`",
                f"- Message: {finding.message}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("../CellProtocol").resolve(),
        help="Path to the CellProtocol repository.",
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        default=[],
        help="Source directory relative to repo root. Defaults to CellBase, CellApple and CellVapor.",
    )
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    source_dirs = args.source_dir or DEFAULT_SOURCE_DIRS
    calls: list[Call] = []
    for swift_file in iter_swift_files(repo_root, source_dirs):
        calls.extend(parse_calls(swift_file, repo_root))

    findings = build_findings(calls)
    report = {
        "repoRoot": str(repo_root),
        "sourceDirs": source_dirs,
        "callsInspected": len(calls),
        "findings": [asdict(finding) for finding in findings],
        "summary": {
            "errors": sum(1 for finding in findings if finding.severity == "error"),
            "warnings": sum(1 for finding in findings if finding.severity == "warn"),
        },
    }

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(repo_root, calls, findings), encoding="utf-8")

    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    if args.fail_on_error and report["summary"]["errors"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
