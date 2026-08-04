#!/usr/bin/env python3
"""Restricted, dependency-free checks for the A1 normative deliverable.

This deliberately checks the wire subset and semantic locks used by the golden
fixtures. It is not a replacement for a standards-complete JSON Schema 2020-12
validator; A4 must add one to CI before this contract governs a runtime route.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


DELIVERY_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = DELIVERY_ROOT.parents[1]
DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
PURPOSE_RE = re.compile(r"^purpose://[a-z0-9][a-z0-9._/-]*$")
OPAQUE_REF_RE = re.compile(r"^[a-z][a-z0-9+.-]*://\S+$")
BINDING_KEYS = {
    "purposeDigest",
    "actionDigest",
    "destinationDigest",
    "dataManifestDigest",
    "planDigest",
    "configDigest",
    "policyDigest",
    "taxonomyDigest",
    "payloadDigest",
}
POLICY_BINDING_KEYS = {"configDigest", "policyDigest", "taxonomyDigest"}
WIRE_SCHEMAS = {
    "haven.purpose-bound-action-intent.v1": "schemas/PurposeBoundActionIntent.schema.json",
    "haven.cell-execution-policy.v1": "schemas/CellExecutionPolicy.schema.json",
    "haven.purpose-authorization-context.v1": "schemas/PurposeAuthorizationContext.schema.json",
    "haven.action-decision-receipt.v1": "schemas/ActionDecisionReceipt.schema.json",
}


def add(problems: list[str], condition: bool, message: str) -> None:
    if not condition:
        problems.append(message)


def object_with_keys(
    value: Any,
    required: set[str],
    optional: set[str],
    label: str,
    problems: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        problems.append(f"{label}: expected object")
        return {}
    keys = set(value)
    missing = sorted(required - keys)
    unknown = sorted(keys - required - optional)
    if missing:
        problems.append(f"{label}: missing {', '.join(missing)}")
    if unknown:
        problems.append(f"{label}: unknown {', '.join(unknown)}")
    return value


def require_string(value: Any, label: str, problems: list[str], pattern: re.Pattern[str] | None = None) -> None:
    add(problems, isinstance(value, str) and bool(value), f"{label}: expected non-empty string")
    if isinstance(value, str) and pattern is not None:
        add(problems, bool(pattern.fullmatch(value)), f"{label}: invalid format")


def require_iso_time(value: Any, label: str, problems: list[str]) -> None:
    require_string(value, label, problems)
    if isinstance(value, str):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            problems.append(f"{label}: invalid ISO-8601 date-time")


def check_bindings(value: Any, label: str, problems: list[str], expected_keys: set[str] = BINDING_KEYS) -> dict[str, Any]:
    bindings = object_with_keys(value, expected_keys, set(), label, problems)
    for key in expected_keys:
        require_string(bindings.get(key), f"{label}.{key}", problems, DIGEST_RE)
    return bindings


def validate_intent(value: Any, problems: list[str]) -> None:
    intent = object_with_keys(
        value,
        {
            "schema", "intentId", "status", "primaryPurposeRef", "primaryPurposeSelection",
            "facetsAreNonAuthorizing", "effect", "bindings", "createdAt",
        },
        {"primaryPurposeEvidenceRefs", "facetRefs"},
        "intent",
        problems,
    )
    add(problems, intent.get("schema") == "haven.purpose-bound-action-intent.v1", "intent.schema: wrong wire schema")
    require_string(intent.get("intentId"), "intent.intentId", problems)
    add(problems, intent.get("status") in {"proposed", "review_required", "blocked"}, "intent.status: invalid")
    require_string(intent.get("primaryPurposeRef"), "intent.primaryPurposeRef", problems, PURPOSE_RE)
    add(problems, intent.get("primaryPurposeSelection") in {"owner_confirmed", "deterministic_resolution", "unknown"}, "intent.primaryPurposeSelection: invalid")
    add(problems, intent.get("facetsAreNonAuthorizing") is True, "intent.facetsAreNonAuthorizing must be true")
    for field in ("primaryPurposeEvidenceRefs", "facetRefs"):
        if field in intent:
            add(problems, isinstance(intent[field], list), f"intent.{field}: expected array")
            if isinstance(intent[field], list):
                add(problems, len(intent[field]) == len(set(intent[field])), f"intent.{field}: duplicate values")
                for i, item in enumerate(intent[field]):
                    require_string(item, f"intent.{field}[{i}]", problems, PURPOSE_RE if field == "facetRefs" else None)

    effect = object_with_keys(
        intent.get("effect"),
        {"effectId", "effectKind", "actionRef", "executionMode", "destination", "data"},
        set(),
        "intent.effect",
        problems,
    )
    require_string(effect.get("effectId"), "intent.effect.effectId", problems)
    add(problems, effect.get("effectKind") in {"external_disclosure", "provider_invocation", "external_write", "external_publish", "subprocess_execution"}, "intent.effect.effectKind: invalid")
    require_string(effect.get("actionRef"), "intent.effect.actionRef", problems, OPAQUE_REF_RE)
    add(problems, effect.get("executionMode") in {"execute", "propose_only", "not_requested"}, "intent.effect.executionMode: invalid")
    destination = object_with_keys(effect.get("destination"), {"destinationRef", "destinationClass"}, set(), "intent.effect.destination", problems)
    require_string(destination.get("destinationRef"), "intent.effect.destination.destinationRef", problems, OPAQUE_REF_RE)
    add(problems, destination.get("destinationClass") in {"admitted_recipient", "approved_provider", "owner_controlled_store", "approved_subprocess"}, "intent.effect.destination.destinationClass: invalid")
    data = object_with_keys(effect.get("data"), {"dataClassRefs", "fieldManifestDigest", "minimizationDeclared"}, set(), "intent.effect.data", problems)
    add(problems, isinstance(data.get("dataClassRefs"), list) and bool(data.get("dataClassRefs")), "intent.effect.data.dataClassRefs: expected non-empty array")
    if isinstance(data.get("dataClassRefs"), list):
        add(problems, len(data["dataClassRefs"]) == len(set(data["dataClassRefs"])), "intent.effect.data.dataClassRefs: duplicate values")
        for i, item in enumerate(data["dataClassRefs"]):
            require_string(item, f"intent.effect.data.dataClassRefs[{i}]", problems)
    require_string(data.get("fieldManifestDigest"), "intent.effect.data.fieldManifestDigest", problems, DIGEST_RE)
    add(problems, data.get("minimizationDeclared") is True, "intent.effect.data.minimizationDeclared must be true")
    check_bindings(intent.get("bindings"), "intent.bindings", problems)
    require_iso_time(intent.get("createdAt"), "intent.createdAt", problems)
    unknown = intent.get("primaryPurposeRef") == "purpose://prompt.unknown"
    if unknown:
        add(problems, intent.get("status") == "blocked", "unknown purpose must be blocked")
        add(problems, intent.get("primaryPurposeSelection") == "unknown", "unknown purpose must declare selection unknown")
        add(problems, effect.get("executionMode") == "not_requested", "unknown purpose must not request execution")
    else:
        add(problems, intent.get("primaryPurposeSelection") != "unknown", "known purpose cannot declare selection unknown")


def validate_policy(value: Any, problems: list[str]) -> None:
    policy = object_with_keys(
        value,
        {
            "schema", "policyId", "status", "configPolicyIsCeilingNotGrant",
            "parentPurposeImpliesChild", "facetsAreNonAuthorizing",
            "ownerPathMayBypassExternalActionCeiling", "bindings", "policyProvenance",
            "defaultDecision", "effectCeilings",
        },
        set(),
        "policy",
        problems,
    )
    add(problems, policy.get("schema") == "haven.cell-execution-policy.v1", "policy.schema: wrong wire schema")
    require_string(policy.get("policyId"), "policy.policyId", problems)
    add(problems, policy.get("status") == "normative_draft", "policy.status must be normative_draft")
    add(problems, policy.get("configPolicyIsCeilingNotGrant") is True, "policy must be ceiling not grant")
    add(problems, policy.get("parentPurposeImpliesChild") is False, "policy must not imply parent/child")
    add(problems, policy.get("facetsAreNonAuthorizing") is True, "policy facets must be non-authorizing")
    add(problems, policy.get("ownerPathMayBypassExternalActionCeiling") is False, "policy owner path must not bypass ceiling")
    check_bindings(policy.get("bindings"), "policy.bindings", problems, POLICY_BINDING_KEYS)
    provenance = object_with_keys(policy.get("policyProvenance"), {"policyVersion", "issuerRef", "publicationRef", "signatureRef", "issuedAt"}, set(), "policy.policyProvenance", problems)
    require_string(provenance.get("policyVersion"), "policy.policyProvenance.policyVersion", problems)
    for field in ("issuerRef", "publicationRef", "signatureRef"):
        require_string(provenance.get(field), f"policy.policyProvenance.{field}", problems, OPAQUE_REF_RE)
    require_iso_time(provenance.get("issuedAt"), "policy.policyProvenance.issuedAt", problems)
    add(problems, policy.get("defaultDecision") == "denied", "policy.defaultDecision must be denied")
    ceilings = policy.get("effectCeilings")
    add(problems, isinstance(ceilings, list) and bool(ceilings), "policy.effectCeilings: expected non-empty array")
    if not isinstance(ceilings, list):
        return
    for index, ceiling_value in enumerate(ceilings):
        ceiling = object_with_keys(
            ceiling_value,
            {
                "ceilingId", "oneConcreteEffectOnly", "effectKind", "actionRef", "primaryPurposeRef",
                "purposeMatch", "allowedDestinationRefs", "allowedDataClassRefs", "planDigest",
                "requiredPermissions", "storageDisclosure",
            },
            {"permittedFacetRefs"},
            f"policy.effectCeilings[{index}]",
            problems,
        )
        require_string(ceiling.get("ceilingId"), f"policy.effectCeilings[{index}].ceilingId", problems)
        add(problems, ceiling.get("oneConcreteEffectOnly") is True, f"policy.effectCeilings[{index}].oneConcreteEffectOnly must be true")
        add(problems, ceiling.get("effectKind") in {"external_disclosure", "provider_invocation", "external_write", "external_publish", "subprocess_execution"}, f"policy.effectCeilings[{index}].effectKind: invalid")
        require_string(ceiling.get("actionRef"), f"policy.effectCeilings[{index}].actionRef", problems, OPAQUE_REF_RE)
        require_string(ceiling.get("primaryPurposeRef"), f"policy.effectCeilings[{index}].primaryPurposeRef", problems, PURPOSE_RE)
        add(problems, ceiling.get("purposeMatch") == "exact_only", f"policy.effectCeilings[{index}].purposeMatch must be exact_only")
        for field in ("allowedDestinationRefs", "allowedDataClassRefs"):
            values = ceiling.get(field)
            add(problems, isinstance(values, list) and bool(values), f"policy.effectCeilings[{index}].{field}: expected non-empty array")
            if isinstance(values, list):
                add(problems, len(values) == len(set(values)), f"policy.effectCeilings[{index}].{field}: duplicate values")
        if isinstance(ceiling.get("allowedDestinationRefs"), list):
            for item in ceiling["allowedDestinationRefs"]:
                require_string(item, f"policy.effectCeilings[{index}].allowedDestinationRefs", problems, OPAQUE_REF_RE)
        require_string(ceiling.get("planDigest"), f"policy.effectCeilings[{index}].planDigest", problems, DIGEST_RE)
        permissions = object_with_keys(ceiling.get("requiredPermissions"), {"execute"}, {"storage", "disclosure"}, f"policy.effectCeilings[{index}].requiredPermissions", problems)
        add(problems, permissions.get("execute") is True, f"policy.effectCeilings[{index}].requiredPermissions.execute must be true")
        storage = object_with_keys(ceiling.get("storageDisclosure"), {"storageRequiresSeparateSPermission", "disclosureRequiresSeparateCapability", "storageDoesNotAuthorizeDisclosure"}, set(), f"policy.effectCeilings[{index}].storageDisclosure", problems)
        for field in storage:
            add(problems, storage[field] is True, f"policy.effectCeilings[{index}].storageDisclosure.{field} must be true")


def validate_context(value: Any, problems: list[str]) -> None:
    context = object_with_keys(value, {"schema", "contextId", "intentRef", "authorizationStatus", "identity", "authority", "trustPackageEvidence", "checks", "bindings"}, {"denialReasons"}, "context", problems)
    add(problems, context.get("schema") == "haven.purpose-authorization-context.v1", "context.schema: wrong wire schema")
    require_string(context.get("contextId"), "context.contextId", problems)
    require_string(context.get("intentRef"), "context.intentRef", problems, OPAQUE_REF_RE)
    add(problems, context.get("authorizationStatus") in {"eligible", "denied", "requires_human_approval", "expired"}, "context.authorizationStatus: invalid")
    identity = object_with_keys(context.get("identity"), {"identityRef", "domain", "proofRef"}, set(), "context.identity", problems)
    require_string(identity.get("identityRef"), "context.identity.identityRef", problems, OPAQUE_REF_RE)
    require_string(identity.get("domain"), "context.identity.domain", problems)
    require_string(identity.get("proofRef"), "context.identity.proofRef", problems, OPAQUE_REF_RE)
    authority = object_with_keys(context.get("authority"), {"authorityPath", "ownerPath", "authorityCurrent"}, {"agreementRef", "contractRef", "grantRef", "cellAuthorityRef"}, "context.authority", problems)
    path = authority.get("authorityPath")
    add(problems, path in {"contract_grant", "owner_path", "cell_specific", "none"}, "context.authority.authorityPath: invalid")
    owner_path = object_with_keys(authority.get("ownerPath"), {"present", "mayBypassExternalActionCeiling"}, set(), "context.authority.ownerPath", problems)
    add(problems, isinstance(authority.get("authorityCurrent"), bool), "context.authority.authorityCurrent: expected boolean")
    add(problems, owner_path.get("mayBypassExternalActionCeiling") is False, "context.authority.ownerPath must not bypass external action ceiling")
    contract_refs = {"agreementRef", "contractRef", "grantRef"}
    if path == "contract_grant":
        add(problems, contract_refs <= set(authority), "contract_grant requires agreementRef, contractRef and grantRef")
        add(problems, owner_path.get("present") is False, "contract_grant cannot be an owner path")
        add(problems, "cellAuthorityRef" not in authority, "contract_grant must not carry cellAuthorityRef")
    elif path == "owner_path":
        add(problems, owner_path.get("present") is True, "owner_path requires ownerPath.present")
        add(problems, not (contract_refs | {"cellAuthorityRef"}) & set(authority), "owner_path must not carry Contract/Grant/cell authority refs")
    elif path == "cell_specific":
        add(problems, owner_path.get("present") is False, "cell_specific cannot be an owner path")
        add(problems, "cellAuthorityRef" in authority, "cell_specific requires cellAuthorityRef")
        add(problems, not contract_refs & set(authority), "cell_specific must not carry Agreement/Contract/Grant refs")
    elif path == "none":
        add(problems, owner_path.get("present") is False, "none authority cannot be an owner path")
        add(problems, authority.get("authorityCurrent") is False, "none authority cannot be current")
        add(problems, not (contract_refs | {"cellAuthorityRef"}) & set(authority), "none authority must not carry authority refs")
    for field in contract_refs | {"cellAuthorityRef"}:
        if field in authority:
            require_string(authority.get(field), f"context.authority.{field}", problems, OPAQUE_REF_RE)
    evidence = object_with_keys(context.get("trustPackageEvidence"), {"status", "confersAuthority"}, {"evidenceRef"}, "context.trustPackageEvidence", problems)
    status = evidence.get("status")
    add(problems, status in {"current", "unavailable", "expired", "not_required"}, "context.trustPackageEvidence.status: invalid")
    add(problems, evidence.get("confersAuthority") is False, "trust package must not confer authority")
    if status in {"current", "expired"}:
        add(problems, "evidenceRef" in evidence, "current or expired evidence requires evidenceRef")
    if "evidenceRef" in evidence:
        require_string(evidence.get("evidenceRef"), "context.trustPackageEvidence.evidenceRef", problems, OPAQUE_REF_RE)
    check_names = {"oneConcreteEffect", "exactPrimaryPurposeMatch", "parentMatchOnly", "facetMatchOnly", "unknownPurpose", "externalActionCeilingSatisfied", "destinationAllowed", "dataAllowed", "planAllowed", "storagePermissionSatisfied", "disclosureCapabilitySatisfied", "bindingDigestsMatch"}
    checks = object_with_keys(context.get("checks"), check_names, set(), "context.checks", problems)
    for field in check_names:
        add(problems, isinstance(checks.get(field), bool), f"context.checks.{field}: expected boolean")
    check_bindings(context.get("bindings"), "context.bindings", problems)
    if context.get("authorizationStatus") == "eligible":
        for field in check_names:
            expected = False if field in {"parentMatchOnly", "facetMatchOnly", "unknownPurpose"} else True
            add(problems, checks.get(field) is expected, f"eligible context requires {field}={expected}")
        add(problems, authority.get("authorityCurrent") is True, "eligible context requires current authority")
        add(problems, status in {"current", "not_required"}, "eligible context needs current or not_required evidence")
        add(problems, path != "none", "eligible context cannot use authorityPath=none")
    if context.get("authorizationStatus") == "denied":
        add(problems, isinstance(context.get("denialReasons"), list) and bool(context.get("denialReasons")), "denied context requires denialReasons")


def validate_receipt(value: Any, problems: list[str]) -> None:
    receipt = object_with_keys(value, {"schema", "receiptId", "intentRef", "contextRef", "decisionStatus", "executionStatus", "authorityPath", "checks", "bindings", "containsSecrets", "createdAt"}, {"reasonCodes"}, "receipt", problems)
    add(problems, receipt.get("schema") == "haven.action-decision-receipt.v1", "receipt.schema: wrong wire schema")
    for field in ("receiptId",):
        require_string(receipt.get(field), f"receipt.{field}", problems)
    for field in ("intentRef", "contextRef"):
        require_string(receipt.get(field), f"receipt.{field}", problems, OPAQUE_REF_RE)
    decision = receipt.get("decisionStatus")
    add(problems, decision in {"allowed", "denied", "requires_human_approval", "expired"}, "receipt.decisionStatus: invalid")
    add(problems, receipt.get("executionStatus") in {"not_executed", "started", "completed", "failed", "not_attempted"}, "receipt.executionStatus: invalid")
    add(problems, receipt.get("authorityPath") in {"contract_grant", "owner_path", "cell_specific", "none"}, "receipt.authorityPath: invalid")
    check_names = {"exactPrimaryPurposeMatch", "externalActionCeilingSatisfied", "storageDoesNotAuthorizeDisclosure", "trustPackageDidNotAuthorize", "ownerPathDidNotBypassCeiling", "bindingDigestsMatch"}
    checks = object_with_keys(receipt.get("checks"), check_names, set(), "receipt.checks", problems)
    for field in {"exactPrimaryPurposeMatch", "externalActionCeilingSatisfied", "bindingDigestsMatch"}:
        add(problems, isinstance(checks.get(field), bool), f"receipt.checks.{field}: expected boolean")
    for field in {"storageDoesNotAuthorizeDisclosure", "trustPackageDidNotAuthorize", "ownerPathDidNotBypassCeiling"}:
        add(problems, checks.get(field) is True, f"receipt.checks.{field} must be true")
    check_bindings(receipt.get("bindings"), "receipt.bindings", problems)
    add(problems, receipt.get("containsSecrets") is False, "receipt.containsSecrets must be false")
    require_iso_time(receipt.get("createdAt"), "receipt.createdAt", problems)
    if "reasonCodes" in receipt:
        add(problems, isinstance(receipt["reasonCodes"], list) and bool(receipt["reasonCodes"]), "receipt.reasonCodes: expected non-empty array")
    if decision == "allowed":
        add(problems, receipt.get("authorityPath") != "none", "allowed receipt cannot use authorityPath=none")
        for field in {"exactPrimaryPurposeMatch", "externalActionCeilingSatisfied", "bindingDigestsMatch"}:
            add(problems, checks.get(field) is True, f"allowed receipt requires {field}=true")
    if decision == "denied":
        add(problems, isinstance(receipt.get("reasonCodes"), list) and bool(receipt.get("reasonCodes")), "denied receipt requires reasonCodes")


def validate_wire(value: Any, wire_schema: str) -> list[str]:
    problems: list[str] = []
    if wire_schema == "haven.purpose-bound-action-intent.v1":
        validate_intent(value, problems)
    elif wire_schema == "haven.cell-execution-policy.v1":
        validate_policy(value, problems)
    elif wire_schema == "haven.purpose-authorization-context.v1":
        validate_context(value, problems)
    elif wire_schema == "haven.action-decision-receipt.v1":
        validate_receipt(value, problems)
    else:
        problems.append(f"unknown wire schema {wire_schema}")
    return problems


def load_json(path: Path, failures: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"{path.relative_to(DELIVERY_ROOT)}: JSON parse failed: {exc}")
        return None


def check_schema_documents(failures: list[str]) -> None:
    for wire_schema, relative in WIRE_SCHEMAS.items():
        path = DELIVERY_ROOT / relative
        document = load_json(path, failures)
        if not isinstance(document, dict):
            continue
        label = path.relative_to(DELIVERY_ROOT).as_posix()
        add(failures, document.get("$schema") == "https://json-schema.org/draft/2020-12/schema", f"{label}: wrong JSON Schema draft")
        add(failures, isinstance(document.get("$id"), str) and document["$id"].startswith("urn:haven:"), f"{label}: missing HAVEN urn id")
        add(failures, document.get("type") == "object", f"{label}: expected object root")
        add(failures, document.get("additionalProperties") is False, f"{label}: root must close unknown properties")
        required = document.get("required")
        add(failures, isinstance(required, list) and "schema" in required, f"{label}: required schema discriminator missing")
        properties = document.get("properties")
        add(failures, isinstance(properties, dict) and properties.get("schema", {}).get("const") == wire_schema, f"{label}: schema discriminator mismatch")


def check_markdown_links(failures: list[str]) -> None:
    link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
    for path in DELIVERY_ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            label = path.relative_to(DELIVERY_ROOT).as_posix()
            add(failures, candidate.is_relative_to(REPOSITORY_ROOT), f"{label}: link escapes repository: {target}")
            if candidate.is_relative_to(REPOSITORY_ROOT):
                add(failures, candidate.exists(), f"{label}: broken link: {target}")


def main() -> int:
    failures: list[str] = []
    check_schema_documents(failures)
    for path in DELIVERY_ROOT.rglob("*.json"):
        load_json(path, failures)
    manifest_path = DELIVERY_ROOT / "fixtures/fixture-manifest.json"
    manifest = load_json(manifest_path, failures)
    if not isinstance(manifest, dict):
        failures.append("fixture manifest unavailable")
    else:
        manifest = object_with_keys(manifest, {"schema", "version", "fixtures"}, set(), "fixture-manifest", failures)
        add(failures, manifest.get("schema") == "haven.purpose-bound-action-fixture-manifest.v1", "fixture-manifest: wrong schema")
        add(failures, manifest.get("version") == 1, "fixture-manifest: wrong version")
        fixtures = manifest.get("fixtures")
        add(failures, isinstance(fixtures, list) and bool(fixtures), "fixture-manifest: fixtures must be non-empty array")
        loaded: dict[str, Any] = {}
        registered_paths: set[Path] = set()
        if isinstance(fixtures, list):
            ids: set[str] = set()
            for entry in fixtures:
                entry_problems: list[str] = []
                entry_obj = object_with_keys(entry, {"id", "path", "wireSchema", "expected"}, set(), "fixture-manifest entry", entry_problems)
                fixture_id = entry_obj.get("id")
                add(entry_problems, isinstance(fixture_id, str) and bool(fixture_id) and fixture_id not in ids, f"fixture-manifest: duplicate/invalid id {fixture_id!r}")
                if isinstance(fixture_id, str):
                    ids.add(fixture_id)
                relative = entry_obj.get("path")
                add(entry_problems, isinstance(relative, str) and relative.endswith(".json"), f"fixture {fixture_id}: invalid path")
                fixture_path = manifest_path.parent / relative if isinstance(relative, str) else DELIVERY_ROOT
                add(entry_problems, fixture_path.is_relative_to(DELIVERY_ROOT) and fixture_path.exists(), f"fixture {fixture_id}: missing file")
                wire_schema = entry_obj.get("wireSchema")
                add(entry_problems, wire_schema in WIRE_SCHEMAS, f"fixture {fixture_id}: unknown wire schema")
                expected = entry_obj.get("expected")
                add(entry_problems, expected in {"accept", "accept_blocked", "accept_denied", "reject_schema"}, f"fixture {fixture_id}: invalid expected outcome")
                if fixture_path.exists() and wire_schema in WIRE_SCHEMAS:
                    fixture = load_json(fixture_path, entry_problems)
                    if fixture is not None:
                        registered_paths.add(fixture_path.resolve())
                        wire_problems = validate_wire(fixture, wire_schema)
                        if expected == "reject_schema":
                            add(entry_problems, bool(wire_problems), f"fixture {fixture_id}: expected schema rejection")
                        else:
                            entry_problems.extend(wire_problems)
                            if expected == "accept_blocked":
                                add(entry_problems, fixture.get("status") == "blocked", f"fixture {fixture_id}: must be blocked")
                            if expected == "accept_denied":
                                add(entry_problems, fixture.get("authorizationStatus", fixture.get("decisionStatus")) == "denied", f"fixture {fixture_id}: must be denied")
                        loaded[str(fixture_id)] = fixture
                failures.extend(f"{message}" for message in entry_problems)
        fixture_files = {path.resolve() for path in (DELIVERY_ROOT / "fixtures").rglob("*.json") if path.name != "fixture-manifest.json"}
        add(failures, fixture_files == registered_paths, "fixture-manifest: every fixture JSON must be registered exactly once")
        check_cross_fixture_locks(loaded, failures)
    check_markdown_links(failures)
    if failures:
        print("A1 contract validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("A1 contract validation passed: schemas, JSON, semantic fixtures and Markdown links")
    return 0


def check_cross_fixture_locks(loaded: dict[str, Any], failures: list[str]) -> None:
    intent = loaded.get("positive-intent")
    policy = loaded.get("positive-policy")
    context = loaded.get("positive-context")
    receipt = loaded.get("positive-receipt")
    if not all(isinstance(item, dict) for item in (intent, policy, context, receipt)):
        failures.append("cross-fixture locks: positive suite incomplete")
        return
    ceiling = policy["effectCeilings"][0]
    add(failures, intent["primaryPurposeRef"] == ceiling["primaryPurposeRef"], "positive suite: intent and ceiling primary purpose mismatch")
    add(failures, intent["effect"]["actionRef"] == ceiling["actionRef"], "positive suite: intent and ceiling action mismatch")
    add(failures, intent["effect"]["destination"]["destinationRef"] in ceiling["allowedDestinationRefs"], "positive suite: destination outside ceiling")
    add(failures, set(intent["effect"]["data"]["dataClassRefs"]) <= set(ceiling["allowedDataClassRefs"]), "positive suite: data class outside ceiling")
    add(failures, intent["bindings"]["planDigest"] == ceiling["planDigest"], "positive suite: plan digest mismatch")
    for key in BINDING_KEYS:
        add(failures, intent["bindings"][key] == context["bindings"][key] == receipt["bindings"][key], f"positive suite: {key} is not bound across intent/context/receipt")
    for key in POLICY_BINDING_KEYS:
        add(failures, intent["bindings"][key] == policy["bindings"][key], f"positive suite: {key} is not bound to policy")
    add(failures, receipt["decisionStatus"] == "allowed" and receipt["executionStatus"] == "not_executed", "positive suite: allow must remain distinct from execution")


if __name__ == "__main__":
    sys.exit(main())
