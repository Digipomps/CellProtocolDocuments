#!/usr/bin/env python3
"""Validate an experimental Agent Continuity Core v1 JSON contract.

The validator is deliberately side-effect-free: it reads one local JSON file,
does not resolve any URI, and never turns contract content into instructions,
authority, approval, or a canonical-state write.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


TOOL_VERSION = "0.1.0"
TOOL_ID = "agent-continuity-validator"
CORE_VERSION = "agent-continuity.core.v1"
RECEIPT_VERSION = "agent-continuity.validation-receipt.v1"
WORK_PROFILE = "org.cellprotocol.haven.work-domain"
KNOWN_PROFILE_VERSIONS = {
    WORK_PROFILE: "1.0",
}

MAX_INPUT_BYTES = 256 * 1024
MAX_NESTING_DEPTH = 20
MAX_CONTAINER_ITEMS = 10_000
MAX_STRING_CHARS = 16_384

STABLE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{2,255}$")
PURPOSE_REF_RE = re.compile(r"^purpose://")
PROFILE_ID_RE = re.compile(r"^[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)+$")
PROFILE_VERSION_RE = re.compile(r"^[1-9][0-9]*\.[0-9]+$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)

TOP_LEVEL_KEYS = {
    "protocolVersion",
    "experimental",
    "capturedAt",
    "objective",
    "currentSituation",
    "constraints",
    "next",
    "verificationRoutes",
    "profiles",
    "warnings",
}


class DuplicateKeyError(ValueError):
    """Raised when JSON parsing encounters a duplicate object key."""


@dataclass(frozen=True, order=True)
class ValidationIssue:
    severity: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


@dataclass(frozen=True)
class ValidationResult:
    issues: tuple[ValidationIssue, ...]
    ignored_profiles: tuple[str, ...]
    disposition: str

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")

    @property
    def contract_valid(self) -> bool:
        return not self.errors


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_contract_bytes(raw: bytes) -> tuple[dict[str, Any] | None, tuple[ValidationIssue, ...]]:
    """Parse bytes with deterministic resource and duplicate-key guards."""
    if len(raw) > MAX_INPUT_BYTES:
        return None, (
            ValidationIssue(
                "error",
                "ACV012_RESOURCE_LIMIT_EXCEEDED",
                "$",
                f"input is {len(raw)} bytes; maximum is {MAX_INPUT_BYTES}",
            ),
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, (
            ValidationIssue("error", "ACV001_INVALID_JSON", "$", f"invalid UTF-8: {error}"),
        )

    try:
        payload = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except DuplicateKeyError as error:
        return None, (
            ValidationIssue("error", "ACV002_DUPLICATE_KEY", "$", str(error)),
        )
    except (json.JSONDecodeError, ValueError, RecursionError) as error:
        return None, (
            ValidationIssue("error", "ACV001_INVALID_JSON", "$", str(error)),
        )

    if not isinstance(payload, dict):
        return None, (
            ValidationIssue("error", "ACV005_SCHEMA_VIOLATION", "$", "top-level JSON value must be an object"),
        )

    try:
        depth, items, longest = _resource_shape(payload)
    except RecursionError:
        return None, (
            ValidationIssue(
                "error",
                "ACV012_RESOURCE_LIMIT_EXCEEDED",
                "$",
                "input nesting exceeds the parser's safe recursion limit",
            ),
        )
    problems: list[ValidationIssue] = []
    if depth > MAX_NESTING_DEPTH:
        problems.append(
            ValidationIssue(
                "error",
                "ACV012_RESOURCE_LIMIT_EXCEEDED",
                "$",
                f"nesting depth is {depth}; maximum is {MAX_NESTING_DEPTH}",
            )
        )
    if items > MAX_CONTAINER_ITEMS:
        problems.append(
            ValidationIssue(
                "error",
                "ACV012_RESOURCE_LIMIT_EXCEEDED",
                "$",
                f"container item count is {items}; maximum is {MAX_CONTAINER_ITEMS}",
            )
        )
    if longest > MAX_STRING_CHARS:
        problems.append(
            ValidationIssue(
                "error",
                "ACV012_RESOURCE_LIMIT_EXCEEDED",
                "$",
                f"longest string is {longest} characters; maximum is {MAX_STRING_CHARS}",
            )
        )
    return (payload if not problems else None), tuple(sorted(problems))


def _resource_shape(value: Any, depth: int = 1) -> tuple[int, int, int]:
    max_depth = depth
    item_count = 0
    longest_string = len(value) if isinstance(value, str) else 0
    children: Iterable[Any]
    if isinstance(value, dict):
        item_count += len(value)
        children = list(value.keys()) + list(value.values())
    elif isinstance(value, list):
        item_count += len(value)
        children = value
    else:
        children = ()
    for child in children:
        child_depth, child_items, child_longest = _resource_shape(child, depth + 1)
        max_depth = max(max_depth, child_depth)
        item_count += child_items
        longest_string = max(longest_string, child_longest)
    return max_depth, item_count, longest_string


class ContractValidator:
    def __init__(self, contract: dict[str, Any]) -> None:
        self.contract = contract
        self.issues: list[ValidationIssue] = []
        self.stable_ids: dict[str, str] = {}
        self.verification_route_ids: set[str] = set()
        self.verification_refs: list[tuple[str, str]] = []
        self.required_before_action: set[str] = set()
        self.route_states: dict[str, str] = {}
        self.ignored_profiles: list[str] = []
        self.captured_at: datetime | None = None

    def validate(self) -> ValidationResult:
        self._validate_core()
        self._validate_cross_references()
        self._validate_action_gate()
        next_kind = self.contract.get("next", {}).get("kind") if isinstance(self.contract.get("next"), dict) else None
        if any(issue.severity == "error" for issue in self.issues):
            disposition = "reject"
        elif next_kind == "action":
            disposition = "verify-before-act"
        elif next_kind == "decision-needed":
            disposition = "decision-needed"
        else:
            disposition = "blocked"
        return ValidationResult(
            issues=tuple(sorted(self.issues)),
            ignored_profiles=tuple(sorted(self.ignored_profiles)),
            disposition=disposition,
        )

    def error(self, code: str, path: str, message: str) -> None:
        self.issues.append(ValidationIssue("error", code, path, message))

    def warn(self, code: str, path: str, message: str) -> None:
        self.issues.append(ValidationIssue("warning", code, path, message))

    def _validate_core(self) -> None:
        core = self._object(
            self.contract,
            "$",
            required={
                "protocolVersion",
                "experimental",
                "capturedAt",
                "objective",
                "currentSituation",
                "constraints",
                "next",
                "verificationRoutes",
            },
            allowed=TOP_LEVEL_KEYS,
        )
        version = core.get("protocolVersion")
        if version != CORE_VERSION:
            self.error(
                "ACV003_UNSUPPORTED_CORE_MAJOR",
                "$.protocolVersion",
                f"expected {CORE_VERSION!r}",
            )
        if core.get("experimental") is not True:
            self.error("ACV005_SCHEMA_VIOLATION", "$.experimental", "must be true")
        self.captured_at = self._timestamp(core.get("capturedAt"), "$.capturedAt")
        self._validate_objective(core.get("objective"), "$.objective")

        situations = self._array(core.get("currentSituation"), "$.currentSituation", minimum=1)
        for index, item in enumerate(situations):
            self._validate_situation(item, f"$.currentSituation[{index}]")

        constraints = self._array(core.get("constraints"), "$.constraints")
        for index, item in enumerate(constraints):
            self._validate_constraint(item, f"$.constraints[{index}]")

        routes = self._array(core.get("verificationRoutes"), "$.verificationRoutes", minimum=1)
        for index, route in enumerate(routes):
            self._validate_route(route, f"$.verificationRoutes[{index}]")

        self._validate_next(core.get("next"), "$.next")

        profiles = self._array(core.get("profiles", []), "$.profiles")
        profile_keys: set[tuple[str, str]] = set()
        for index, profile in enumerate(profiles):
            path = f"$.profiles[{index}]"
            profile_key = self._validate_profile(profile, path)
            if profile_key is not None:
                if profile_key in profile_keys:
                    self.error("ACV006_DUPLICATE_STABLE_ID", path, f"duplicate profile {profile_key[0]}@{profile_key[1]}")
                profile_keys.add(profile_key)

        warnings = self._array(core.get("warnings", []), "$.warnings")
        for index, warning in enumerate(warnings):
            self._string(warning, f"$.warnings[{index}]")

    def _validate_objective(self, value: Any, path: str) -> None:
        item = self._object(
            value,
            path,
            required={"statement", "verificationRefs"},
            allowed={"statement", "doneWhen", "verificationRefs"},
        )
        self._string(item.get("statement"), f"{path}.statement")
        done_when = self._array(item.get("doneWhen", []), f"{path}.doneWhen")
        for index, criterion in enumerate(done_when):
            self._string(criterion, f"{path}.doneWhen[{index}]")
        self._collect_refs(item.get("verificationRefs"), f"{path}.verificationRefs", minimum=1)

    def _validate_situation(self, value: Any, path: str) -> None:
        item = self._object(
            value,
            path,
            required={"id", "statement", "status", "verificationRefs"},
            allowed={"id", "statement", "status", "verificationRefs"},
        )
        self._stable_id(item.get("id"), f"{path}.id")
        self._string(item.get("statement"), f"{path}.statement")
        self._enum(
            item.get("status"),
            {"observed", "proposed", "inferred", "contradicted", "unknown", "unavailable"},
            f"{path}.status",
        )
        self._collect_refs(item.get("verificationRefs"), f"{path}.verificationRefs", minimum=1)

    def _validate_constraint(self, value: Any, path: str) -> None:
        item = self._object(
            value,
            path,
            required={"id", "statement", "verificationRefs"},
            allowed={"id", "statement", "verificationRefs"},
        )
        self._stable_id(item.get("id"), f"{path}.id")
        self._string(item.get("statement"), f"{path}.statement")
        self._collect_refs(item.get("verificationRefs"), f"{path}.verificationRefs", minimum=1)

    def _validate_route(self, value: Any, path: str) -> None:
        route = self._object(
            value,
            path,
            required={"id", "uri", "observedAt", "reportedState", "requiredBeforeAction"},
            allowed={"id", "uri", "observedAt", "reportedState", "requiredBeforeAction", "revision", "digest"},
        )
        route_id = self._stable_id(route.get("id"), f"{path}.id")
        self._string(route.get("uri"), f"{path}.uri")
        observed_at = self._timestamp(route.get("observedAt"), f"{path}.observedAt")
        if observed_at is not None and self.captured_at is not None and observed_at > self.captured_at:
            self.error(
                "ACV011_TEMPORAL_INCONSISTENCY",
                f"{path}.observedAt",
                "cannot be later than the contract capturedAt timestamp",
            )
        state = self._enum(
            route.get("reportedState"),
            {"current", "stale", "unresolved", "unavailable", "contradicted"},
            f"{path}.reportedState",
        )
        if not isinstance(route.get("requiredBeforeAction"), bool):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.requiredBeforeAction", "must be a boolean")
        self._optional_string(route.get("revision"), f"{path}.revision")
        digest = route.get("digest")
        if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest)):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.digest", "must be sha256:<64 lowercase hex>")
        if route_id is not None:
            self.verification_route_ids.add(route_id)
            if isinstance(state, str):
                self.route_states[route_id] = state
            if route.get("requiredBeforeAction") is True:
                self.required_before_action.add(route_id)

    def _validate_next(self, value: Any, path: str) -> None:
        item = self._object(
            value,
            path,
            required={"kind", "statement", "preconditions", "verificationRefs"},
            allowed={"kind", "statement", "preconditions", "verificationRefs"},
        )
        self._enum(item.get("kind"), {"action", "blocked", "decision-needed"}, f"{path}.kind")
        self._string(item.get("statement"), f"{path}.statement")
        preconditions = self._array(item.get("preconditions"), f"{path}.preconditions")
        for index, condition in enumerate(preconditions):
            self._string(condition, f"{path}.preconditions[{index}]")
        self._collect_refs(item.get("verificationRefs"), f"{path}.verificationRefs", minimum=1)

    def _validate_profile(self, value: Any, path: str) -> tuple[str, str] | None:
        profile = self._object(
            value,
            path,
            required={"profileID", "version", "requiredForContinuation", "data"},
            allowed={"profileID", "version", "requiredForContinuation", "data"},
        )
        profile_id = self._string(profile.get("profileID"), f"{path}.profileID")
        version = self._string(profile.get("version"), f"{path}.version")
        if profile_id is not None and not PROFILE_ID_RE.fullmatch(profile_id):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.profileID", "must be a namespaced profile ID")
        if version is not None and not PROFILE_VERSION_RE.fullmatch(version):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.version", "must be a major.minor version")
        required_for_continuation = profile.get("requiredForContinuation")
        if not isinstance(required_for_continuation, bool):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.requiredForContinuation", "must be a boolean")
        data = self._object(profile.get("data"), f"{path}.data", required=set(), allowed=None)
        if not profile_id or not version:
            return None
        expected = KNOWN_PROFILE_VERSIONS.get(profile_id)
        if expected is None:
            if required_for_continuation is True:
                self.error("ACV004_UNKNOWN_CRITICAL_PROFILE", path, f"unsupported required profile {profile_id}@{version}")
            else:
                self.warn(
                    "ACV104_UNKNOWN_NONCRITICAL_PROFILE_QUARANTINED",
                    path,
                    f"unknown profile {profile_id}@{version} is opaque data and must not be interpreted",
                )
                self.ignored_profiles.append(f"{profile_id}@{version}")
            return profile_id, version
        if version != expected:
            self.error(
                "ACV005_SCHEMA_VIOLATION",
                f"{path}.version",
                f"profile {profile_id} supports only version {expected}",
            )
            return profile_id, version
        if profile_id == WORK_PROFILE:
            self._validate_work_profile(data, f"{path}.data")
        return profile_id, version

    def _validate_work_profile(self, data: dict[str, Any], path: str) -> None:
        data = self._object(
            data,
            path,
            required={"project", "goal", "decisions", "openWork", "risksOpenQuestions"},
            allowed={"project", "goal", "decisions", "openWork", "risksOpenQuestions"},
        )
        project = self._object(
            data.get("project"),
            f"{path}.project",
            required={"id", "name", "purposeRefs", "verificationRefs"},
            allowed={"id", "name", "purposeRefs", "verificationRefs"},
        )
        self._stable_id(project.get("id"), f"{path}.project.id")
        self._string(project.get("name"), f"{path}.project.name")
        purpose_refs = self._array(project.get("purposeRefs"), f"{path}.project.purposeRefs", minimum=1)
        seen_purpose_refs: set[str] = set()
        for index, purpose_ref in enumerate(purpose_refs):
            if not isinstance(purpose_ref, str) or not PURPOSE_REF_RE.match(purpose_ref):
                self.error("ACV005_SCHEMA_VIOLATION", f"{path}.project.purposeRefs[{index}]", "must start with purpose://")
                continue
            if purpose_ref in seen_purpose_refs:
                self.error(
                    "ACV006_DUPLICATE_STABLE_ID",
                    f"{path}.project.purposeRefs[{index}]",
                    f"duplicate purpose reference {purpose_ref!r} in the same list",
                )
            seen_purpose_refs.add(purpose_ref)
        self._collect_refs(project.get("verificationRefs"), f"{path}.project.verificationRefs", minimum=1)

        goal = self._object(
            data.get("goal"),
            f"{path}.goal",
            required={"id", "statement", "acceptanceCriteria", "verificationRefs"},
            allowed={"id", "statement", "acceptanceCriteria", "verificationRefs"},
        )
        self._stable_id(goal.get("id"), f"{path}.goal.id")
        self._string(goal.get("statement"), f"{path}.goal.statement")
        criteria = self._array(goal.get("acceptanceCriteria"), f"{path}.goal.acceptanceCriteria", minimum=1)
        for index, criterion in enumerate(criteria):
            self._string(criterion, f"{path}.goal.acceptanceCriteria[{index}]")
        self._collect_refs(goal.get("verificationRefs"), f"{path}.goal.verificationRefs", minimum=1)

        decisions = self._array(data.get("decisions"), f"{path}.decisions")
        for index, decision in enumerate(decisions):
            item_path = f"{path}.decisions[{index}]"
            item = self._object(
                decision,
                item_path,
                required={"id", "statement", "status", "verificationRefs"},
                allowed={"id", "statement", "status", "verificationRefs"},
            )
            self._stable_id(item.get("id"), f"{item_path}.id")
            self._string(item.get("statement"), f"{item_path}.statement")
            self._enum(item.get("status"), {"reported", "proposed", "superseded", "contradicted"}, f"{item_path}.status")
            self._collect_refs(item.get("verificationRefs"), f"{item_path}.verificationRefs", minimum=1)

        open_work = self._array(data.get("openWork"), f"{path}.openWork")
        for index, work in enumerate(open_work):
            item_path = f"{path}.openWork[{index}]"
            item = self._object(
                work,
                item_path,
                required={"id", "status", "summary", "doneWhen", "verificationRefs"},
                allowed={"id", "status", "summary", "doneWhen", "verificationRefs"},
            )
            self._stable_id(item.get("id"), f"{item_path}.id")
            self._enum(item.get("status"), {"open", "in-progress", "blocked", "done"}, f"{item_path}.status")
            self._string(item.get("summary"), f"{item_path}.summary")
            done_when = self._array(item.get("doneWhen"), f"{item_path}.doneWhen", minimum=1)
            for criterion_index, criterion in enumerate(done_when):
                self._string(criterion, f"{item_path}.doneWhen[{criterion_index}]")
            self._collect_refs(item.get("verificationRefs"), f"{item_path}.verificationRefs", minimum=1)

        risks = self._array(data.get("risksOpenQuestions"), f"{path}.risksOpenQuestions")
        for index, risk in enumerate(risks):
            item_path = f"{path}.risksOpenQuestions[{index}]"
            item = self._object(
                risk,
                item_path,
                required={"id", "kind", "statement", "disposition", "verificationRefs"},
                allowed={"id", "kind", "statement", "disposition", "verificationRefs"},
            )
            self._stable_id(item.get("id"), f"{item_path}.id")
            self._enum(item.get("kind"), {"risk", "open-question"}, f"{item_path}.kind")
            self._string(item.get("statement"), f"{item_path}.statement")
            self._string(item.get("disposition"), f"{item_path}.disposition")
            self._collect_refs(item.get("verificationRefs"), f"{item_path}.verificationRefs", minimum=1)

    def _validate_cross_references(self) -> None:
        for ref, path in self.verification_refs:
            if ref not in self.verification_route_ids:
                self.error("ACV007_DANGLING_REFERENCE", path, f"unknown verification route {ref!r}")

    def _validate_action_gate(self) -> None:
        next_value = self.contract.get("next")
        if not isinstance(next_value, dict):
            return
        next_refs = {ref for ref in next_value.get("verificationRefs", []) if isinstance(ref, str)}
        if next_value.get("kind") != "action":
            return
        omitted = sorted(self.required_before_action - next_refs)
        for ref in omitted:
            self.error(
                "ACV009_EXTERNAL_VERIFICATION_REQUIRED",
                "$.next.verificationRefs",
                f"required-before-action route {ref!r} is omitted",
            )
        all_core_and_profile_refs = {ref for ref, _ in self.verification_refs}
        blocked = sorted(ref for ref in all_core_and_profile_refs if self.route_states.get(ref) != "current")
        for ref in blocked:
            self.error(
                "ACV010_FRESHNESS_UNRESOLVED",
                "$.next",
                f"action is inconsistent with reported state {self.route_states.get(ref)!r} for {ref!r}",
            )

    def _object(
        self,
        value: Any,
        path: str,
        *,
        required: set[str],
        allowed: set[str] | None,
    ) -> dict[str, Any]:
        if not isinstance(value, dict):
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be an object")
            return {}
        for key in sorted(required - value.keys()):
            self.error("ACV005_SCHEMA_VIOLATION", f"{path}.{key}", "missing required field")
        if allowed is not None:
            for key in sorted(value.keys() - allowed):
                self.error(
                    "ACV101_SELF_ASSERTED_SECURITY_STATUS" if key in {"approval", "approved", "authority", "authorization", "verified"} else "ACV005_SCHEMA_VIOLATION",
                    f"{path}.{key}",
                    "field is not part of this contract",
                )
        return value

    def _array(self, value: Any, path: str, minimum: int = 0) -> list[Any]:
        if not isinstance(value, list):
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be an array")
            return []
        if len(value) < minimum:
            self.error("ACV005_SCHEMA_VIOLATION", path, f"must contain at least {minimum} item(s)")
        return value

    def _string(self, value: Any, path: str) -> str | None:
        if not isinstance(value, str) or not value.strip():
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be a non-empty string")
            return None
        return value

    def _optional_string(self, value: Any, path: str) -> None:
        if value is not None:
            self._string(value, path)

    def _enum(self, value: Any, choices: set[str], path: str) -> str | None:
        if not isinstance(value, str) or value not in choices:
            self.error("ACV005_SCHEMA_VIOLATION", path, f"must be one of {sorted(choices)}")
            return None
        return value

    def _timestamp(self, value: Any, path: str) -> datetime | None:
        if not isinstance(value, str) or not RFC3339_RE.fullmatch(value):
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be an RFC 3339 timestamp")
            return None
        candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(candidate)
        except ValueError:
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be an RFC 3339 timestamp")
            return None
        if parsed.tzinfo is None:
            self.error("ACV005_SCHEMA_VIOLATION", path, "timestamp must include a UTC offset")
            return None
        return parsed

    def _stable_id(self, value: Any, path: str) -> str | None:
        if not isinstance(value, str) or not STABLE_ID_RE.fullmatch(value):
            self.error("ACV005_SCHEMA_VIOLATION", path, "must be a stable ID")
            return None
        previous_path = self.stable_ids.get(value)
        if previous_path is not None:
            self.error("ACV006_DUPLICATE_STABLE_ID", path, f"duplicates {value!r} first seen at {previous_path}")
        else:
            self.stable_ids[value] = path
        return value

    def _collect_refs(self, value: Any, path: str, minimum: int) -> None:
        refs = self._array(value, path, minimum=minimum)
        seen: set[str] = set()
        for index, ref in enumerate(refs):
            ref_path = f"{path}[{index}]"
            if not isinstance(ref, str) or not STABLE_ID_RE.fullmatch(ref):
                self.error("ACV005_SCHEMA_VIOLATION", ref_path, "must be a stable verification-route ID")
                continue
            if ref in seen:
                self.error("ACV006_DUPLICATE_STABLE_ID", ref_path, f"duplicate reference {ref!r} in the same list")
            seen.add(ref)
            self.verification_refs.append((ref, ref_path))


def validate_contract(contract: dict[str, Any]) -> ValidationResult:
    """Validate a parsed contract without reading, writing, or resolving state."""
    return ContractValidator(contract).validate()


def sha256_bytes(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def build_receipt(
    *,
    raw: bytes,
    result: ValidationResult | None,
    parse_issues: tuple[ValidationIssue, ...] = (),
) -> dict[str, Any]:
    issues = parse_issues if result is None else result.issues
    errors = [issue.as_dict() for issue in issues if issue.severity == "error"]
    warnings = [issue.as_dict() for issue in issues if issue.severity == "warning"]
    return {
        "receiptType": RECEIPT_VERSION,
        "tool": TOOL_ID,
        "toolVersion": TOOL_VERSION,
        "contractDefinition": CORE_VERSION,
        "inputBytesDigest": sha256_bytes(raw),
        "contractValid": result.contract_valid if result is not None else False,
        "continuationDisposition": result.disposition if result is not None else "reject",
        "authorityEffect": "none",
        "freshnessEffect": "none",
        "externalResolutionRequired": True,
        "ignoredProfiles": list(result.ignored_profiles) if result is not None else [],
        "errors": errors,
        "warnings": warnings,
    }


def validate_bytes(raw: bytes) -> tuple[dict[str, Any], int]:
    contract, parse_issues = parse_contract_bytes(raw)
    if contract is None:
        return build_receipt(raw=raw, result=None, parse_issues=parse_issues), 2
    result = validate_contract(contract)
    return build_receipt(raw=raw, result=result), 0 if result.contract_valid else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Local Agent Continuity Core v1 JSON file")
    parser.add_argument("--json", action="store_true", help="Emit the deterministic validation receipt as JSON")
    args = parser.parse_args(argv)

    try:
        raw = args.path.read_bytes()
    except OSError as error:
        print(f"failed to read {args.path}: {error}", file=sys.stderr)
        return 2

    receipt, exit_code = validate_bytes(raw)
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    elif exit_code == 0:
        print(f"valid untrusted continuation contract: {args.path}")
        print(f"disposition: {receipt['continuationDisposition']}; external resolution remains required")
        for warning in receipt["warnings"]:
            print(f"warning: {warning['code']} {warning['path']}: {warning['message']}", file=sys.stderr)
    else:
        for issue in receipt["errors"]:
            print(f"{issue['code']} {issue['path']}: {issue['message']}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
