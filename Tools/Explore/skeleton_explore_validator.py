#!/usr/bin/env python3
"""Validate skeleton key bindings against Explore manifests.

The validator is intentionally conservative. It accepts exported
ExploreManifest, ExploreContractCatalog, raw operation arrays, or a small
manifest index file. It cannot prove runtime authorization or data freshness;
it checks whether the declared skeleton bindings have a matching public
contract.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCALAR_TYPES = {"string", "integer", "number", "float", "bool", "boolean"}
DISPLAY_TYPES = SCALAR_TYPES | {"object", "list", "array", "unknown"}
LIST_TYPES = {"list", "array"}
OBJECT_TYPES = {"object"}
OWNER_ACCESS_PURPOSE_REF = "purpose://skeleton.owner-entity-access"
OWNER_ACCESS_TERMS = {
    "co-pilot",
    "copilot",
    "chat",
    "chathub",
    "entity",
    "entityanchor",
    "entityextension",
    "owner",
    "ownentity",
    "egen entitet",
    "min entitet",
    "mi entitet",
    "eier-entitet",
    "eierentitet",
    "assistent",
}


@dataclass
class Operation:
    endpoint: str
    key: str
    method: str
    input_schema: Any
    return_schema: Any
    input_type: str
    return_type: str
    summary: str | None


@dataclass
class Binding:
    path: str
    element: str
    role: str
    endpoint: str
    key: str
    method: str
    expected_types: list[str]
    raw_value: str


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str
    element: str
    role: str
    endpoint: str
    key: str
    method: str


@dataclass
class OwnerAccessAffordance:
    path: str
    element: str
    reason: str
    value: str


def canonical_type(type_name: str | None) -> str:
    if not type_name:
        return "unknown"
    value = type_name.strip().lower()
    mapping = {
        "bool": "bool",
        "boolean": "bool",
        "int": "integer",
        "integer": "integer",
        "number": "number",
        "float": "float",
        "double": "float",
        "text": "string",
        "string": "string",
        "array": "list",
        "list": "list",
        "dictionary": "object",
        "map": "object",
        "object": "object",
        "null": "null",
        "none": "null",
        "oneof": "oneOf",
    }
    return mapping.get(value, value or "unknown")


def schema_type(schema: Any) -> str:
    if schema is None:
        return "null"
    if isinstance(schema, str):
        return canonical_type(schema)
    if isinstance(schema, dict):
        if "oneOf" in schema:
            return "oneOf"
        return canonical_type(schema.get("type") or "object")
    if isinstance(schema, list):
        return "list"
    return "unknown"


def one_of_types(schema: Any) -> set[str]:
    if isinstance(schema, dict) and isinstance(schema.get("oneOf"), list):
        return {schema_type(option) for option in schema["oneOf"]}
    return {schema_type(schema)}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def operations_from_manifest(endpoint: str, manifest: Any) -> list[Operation]:
    if isinstance(manifest, dict):
        raw_operations = manifest.get("operations") or manifest.get("records") or manifest.get("keys")
    elif isinstance(manifest, list):
        raw_operations = manifest
    else:
        raw_operations = None

    operations: list[Operation] = []
    if not isinstance(raw_operations, list):
        return operations

    for item in raw_operations:
        if not isinstance(item, dict):
            continue
        contract = item.get("contract") if isinstance(item.get("contract"), dict) else item
        key = item.get("key") or contract.get("key")
        method = item.get("method") or contract.get("method")
        if not key or not method:
            continue
        input_schema = contract.get("input")
        return_schema = contract.get("returns")
        operations.append(
            Operation(
                endpoint=endpoint,
                key=str(key),
                method=str(method),
                input_schema=input_schema,
                return_schema=return_schema,
                input_type=canonical_type(item.get("inputType") or schema_type(input_schema)),
                return_type=canonical_type(item.get("returnType") or schema_type(return_schema)),
                summary=item.get("summary") or contract.get("summary"),
            )
        )
    return operations


def load_operation_index(args: argparse.Namespace) -> dict[str, list[Operation]]:
    by_endpoint: dict[str, list[Operation]] = {}

    def add(endpoint: str, manifest: Any) -> None:
        by_endpoint.setdefault(normalize_endpoint(endpoint), []).extend(
            operations_from_manifest(normalize_endpoint(endpoint), manifest)
        )

    if args.manifest:
        add(args.default_endpoint, load_json(args.manifest))

    for item in args.contract or []:
        if "=" not in item:
            raise SystemExit(f"--contract expects ENDPOINT=PATH, got {item!r}")
        endpoint, path = item.split("=", 1)
        add(endpoint, load_json(Path(path)))

    if args.manifest_index:
        index = load_json(args.manifest_index)
        if isinstance(index, dict) and isinstance(index.get("manifests"), list):
            for entry in index["manifests"]:
                if not isinstance(entry, dict):
                    continue
                endpoint = entry.get("endpoint") or args.default_endpoint
                if "path" in entry:
                    add(endpoint, load_json(Path(entry["path"])))
                elif "manifest" in entry:
                    add(endpoint, entry["manifest"])
        elif isinstance(index, dict):
            for endpoint, manifest in index.items():
                add(endpoint, manifest)

    return by_endpoint


def normalize_endpoint(endpoint: str) -> str:
    if endpoint.startswith("cell://"):
        parsed = urlparse(endpoint)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc:
            if parts:
                return f"cell://{parsed.netloc}/{parts[0]}"
            return f"cell://{parsed.netloc}"
        if parts:
            return f"cell:///{parts[0]}"
    return endpoint.rstrip("/")


def resolve_keypath(raw: str, references: dict[str, str], default_endpoint: str) -> tuple[str, str]:
    raw = raw.strip()
    if raw.startswith("cell://"):
        parsed = urlparse(raw)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc:
            endpoint = f"cell://{parsed.netloc}/{parts[0]}" if parts else f"cell://{parsed.netloc}"
            key_parts = parts[1:]
        else:
            endpoint = f"cell:///{parts[0]}" if parts else normalize_endpoint(default_endpoint)
            key_parts = parts[1:]
        return normalize_endpoint(endpoint), ".".join(key_parts)

    root = raw.split(".", 1)[0]
    if root in references and "." in raw:
        return normalize_endpoint(references[root]), raw.split(".", 1)[1]
    return normalize_endpoint(default_endpoint), raw


def extract_configuration_root(config: Any) -> tuple[Any, dict[str, str], str | None]:
    references: dict[str, str] = {}
    discovery_endpoint = None
    if isinstance(config, dict):
        discovery = config.get("discovery")
        if isinstance(discovery, dict):
            discovery_endpoint = discovery.get("sourceCellEndpoint")
        for ref in config.get("cellReferences") or []:
            if isinstance(ref, dict) and ref.get("label") and ref.get("endpoint"):
                references[str(ref["label"])] = str(ref["endpoint"])
        if "skeleton" in config:
            return config["skeleton"], references, discovery_endpoint
    return config, references, discovery_endpoint


def collect_bindings(
    node: Any,
    path: str,
    references: dict[str, str],
    default_endpoint: str,
    bindings: list[Binding],
) -> None:
    if isinstance(node, list):
        for index, item in enumerate(node):
            collect_bindings(item, f"{path}[{index}]", references, default_endpoint, bindings)
        return

    if not isinstance(node, dict):
        return

    if len(node) == 1:
        element, payload = next(iter(node.items()))
        collect_element_bindings(element, payload, path, references, default_endpoint, bindings)
        return

    for key, value in node.items():
            collect_bindings(value, f"{path}.{key}", references, default_endpoint, bindings)


def normalize_affordance_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("_", "").replace("-", "")


def contains_owner_access_term(value: Any) -> bool:
    normalized = normalize_affordance_text(value)
    if not normalized:
        return False
    compact_terms = {normalize_affordance_text(term) for term in OWNER_ACCESS_TERMS}
    return any(term and term in normalized for term in compact_terms)


def collect_owner_access_affordances(
    node: Any,
    path: str,
    affordances: list[OwnerAccessAffordance],
) -> None:
    if isinstance(node, list):
        for index, item in enumerate(node):
            collect_owner_access_affordances(item, f"{path}[{index}]", affordances)
        return

    if not isinstance(node, dict):
        return

    if len(node) == 1:
        element, payload = next(iter(node.items()))
        collect_owner_access_element(element, payload, path, affordances)
        return

    for key, value in node.items():
        collect_owner_access_affordances(value, f"{path}.{key}", affordances)


def collect_owner_access_element(
    element: str,
    payload: Any,
    path: str,
    affordances: list[OwnerAccessAffordance],
) -> None:
    if isinstance(payload, list):
        for index, child in enumerate(payload):
            collect_owner_access_affordances(child, f"{path}.{element}[{index}]", affordances)
        return
    if not isinstance(payload, dict):
        return

    modifiers = payload.get("modifiers")
    if isinstance(modifiers, dict) and modifiers.get("hidden") is True:
        return

    candidate_fields: list[tuple[str, Any]] = []
    if element == "Button":
        candidate_fields = [
            ("label", payload.get("label")),
            ("keypath", payload.get("keypath")),
            ("url", payload.get("url")),
            ("payload", payload.get("payload")),
        ]
    elif element in {"TextArea", "TextField"}:
        candidate_fields = [
            ("placeholder", payload.get("placeholder")),
            ("sourceKeypath", payload.get("sourceKeypath")),
            ("targetKeypath", payload.get("targetKeypath")),
        ]
    elif element == "Reference":
        candidate_fields = [
            ("keypath", payload.get("keypath")),
            ("topic", payload.get("topic")),
        ]
    elif element in {"List", "Grid", "Picker", "Tabs"}:
        candidate_fields = [
            ("keypath", payload.get("keypath")),
            ("tabsKeypath", payload.get("tabsKeypath")),
            ("selectionActionKeypath", payload.get("selectionActionKeypath")),
            ("activationActionKeypath", payload.get("activationActionKeypath")),
        ]

    for field, value in candidate_fields:
        if contains_owner_access_term(value):
            affordances.append(
                OwnerAccessAffordance(
                    path=f"{path}.{element}.{field}",
                    element=element,
                    reason=field,
                    value=str(value),
                )
            )
            break

    for child_key in ("elements", "content", "header", "footer", "flowElementSkeleton", "itemSkeleton"):
        if child_key in payload:
            collect_owner_access_affordances(payload[child_key], f"{path}.{element}.{child_key}", affordances)

    if element == "Tabs":
        for index, panel in enumerate(payload.get("panels") or []):
            if isinstance(panel, dict):
                collect_owner_access_affordances(panel.get("content") or [], f"{path}.Tabs.panels[{index}].content", affordances)


def validate_owner_access(required: bool, affordances: list[OwnerAccessAffordance]) -> list[Finding]:
    if not required or affordances:
        return []
    return [
        Finding(
            severity="error",
            code="missing_owner_entity_access",
            message=(
                "Production skeleton must include a visible owner-entity or Co-Pilot access affordance "
                "so generated UI cannot lock the user away from their own entity."
            ),
            path="$.skeleton",
            element="CellConfiguration",
            role="ownerAccess",
            endpoint="",
            key=OWNER_ACCESS_PURPOSE_REF,
            method="interface",
        )
    ]


def add_binding(
    bindings: list[Binding],
    path: str,
    element: str,
    role: str,
    raw_value: Any,
    method: str,
    expected_types: set[str],
    references: dict[str, str],
    default_endpoint: str,
) -> None:
    if not isinstance(raw_value, str) or not raw_value.strip():
        return
    endpoint, key = resolve_keypath(raw_value, references, default_endpoint)
    if not key:
        return
    bindings.append(
        Binding(
            path=path,
            element=element,
            role=role,
            endpoint=endpoint,
            key=key,
            method=method,
            expected_types=sorted(canonical_type(item) for item in expected_types),
            raw_value=raw_value,
        )
    )


def collect_element_bindings(
    element: str,
    payload: Any,
    path: str,
    references: dict[str, str],
    default_endpoint: str,
    bindings: list[Binding],
) -> None:
    if isinstance(payload, list):
        for index, child in enumerate(payload):
            collect_bindings(child, f"{path}.{element}[{index}]", references, default_endpoint, bindings)
        return
    if not isinstance(payload, dict):
        return

    collect_modifier_bindings(payload.get("modifiers"), f"{path}.{element}.modifiers", references, default_endpoint, bindings)

    if element == "Text":
        add_binding(bindings, path, element, "display", payload.get("keypath") or payload.get("url"), "get", DISPLAY_TYPES, references, default_endpoint)
    elif element in {"TextField", "TextArea"}:
        add_binding(bindings, path, element, "source", payload.get("sourceKeypath"), "get", SCALAR_TYPES, references, default_endpoint)
        add_binding(bindings, path, element, "target", payload.get("targetKeypath"), "set", SCALAR_TYPES | {"unknown"}, references, default_endpoint)
        autocomplete = payload.get("autocomplete")
        if isinstance(autocomplete, dict):
            add_binding(bindings, path, element, "autocomplete.query", autocomplete.get("queryActionKeypath"), "set", {"object", "string", "unknown"}, references, default_endpoint)
            add_binding(bindings, path, element, "autocomplete.suggestions", autocomplete.get("suggestionsKeypath"), "get", LIST_TYPES, references, default_endpoint)
            add_binding(bindings, path, element, "autocomplete.selection", autocomplete.get("selectionActionKeypath"), "set", {"object", "string", "unknown"}, references, default_endpoint)
    elif element in {"List", "Grid", "Picker"}:
        add_binding(bindings, path, element, "items", payload.get("keypath"), "get", LIST_TYPES, references, default_endpoint)
        add_binding(bindings, path, element, "selectionState", payload.get("selectionStateKeypath"), "set", {"object", "list", "string", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "selectionAction", payload.get("selectionActionKeypath"), "set", {"object", "list", "string", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "activationAction", payload.get("activationActionKeypath"), "set", {"object", "string", "unknown"}, references, default_endpoint)
        for child_key in ("flowElementSkeleton", "itemSkeleton"):
            if child_key in payload:
                collect_bindings(payload[child_key], f"{path}.{element}.{child_key}", references, default_endpoint, bindings)
    elif element == "Reference":
        add_binding(bindings, path, element, "reference", payload.get("keypath"), "get", LIST_TYPES | {"object", "unknown"}, references, default_endpoint)
        if "flowElementSkeleton" in payload:
            collect_bindings(payload["flowElementSkeleton"], f"{path}.Reference.flowElementSkeleton", references, default_endpoint, bindings)
    elif element == "Button":
        method = "set" if "payload" in payload else "get"
        role = "action" if method == "set" else "readAction"
        endpoint = payload.get("url") or default_endpoint
        raw = payload.get("keypath")
        if isinstance(raw, str):
            resolved_endpoint, key = resolve_keypath(raw, references, endpoint)
            bindings.append(
                Binding(path=path, element=element, role=role, endpoint=resolved_endpoint, key=key, method=method, expected_types=["unknown"], raw_value=raw)
            )
    elif element in {"FileUpload", "AttachmentField"}:
        add_binding(bindings, path, element, "value", payload.get("valueKeypath") or payload.get("sourceKeypath"), "get", {"object", "list", "string", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "state", payload.get("stateKeypath"), "get", {"object", "string", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "action", payload.get("actionKeypath") or payload.get("targetKeypath"), "set", {"object", "list", "data", "unknown"}, references, default_endpoint)
    elif element == "Toggle":
        add_binding(bindings, path, element, "toggle", payload.get("keypath"), "set", {"bool", "boolean"}, references, default_endpoint)
    elif element == "Tabs":
        add_binding(bindings, path, element, "tabs", payload.get("tabsKeypath"), "get", LIST_TYPES, references, default_endpoint)
        add_binding(bindings, path, element, "activeTabState", payload.get("activeTabStateKeypath"), "set", {"string", "object", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "selectionAction", payload.get("selectionActionKeypath"), "set", {"string", "object", "unknown"}, references, default_endpoint)
        for index, panel in enumerate(payload.get("panels") or []):
            if isinstance(panel, dict):
                collect_bindings(panel.get("content") or [], f"{path}.Tabs.panels[{index}].content", references, default_endpoint, bindings)
    elif element == "Visualization":
        add_binding(bindings, path, element, "data", payload.get("keypath"), "get", {"object", "list", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "state", payload.get("stateKeypath"), "get", {"object", "list", "unknown"}, references, default_endpoint)
        add_binding(bindings, path, element, "action", payload.get("actionKeypath"), "set", {"object", "unknown"}, references, default_endpoint)

    for child_key in ("elements", "content", "header", "footer"):
        if child_key in payload:
            collect_bindings(payload[child_key], f"{path}.{element}.{child_key}", references, default_endpoint, bindings)


def collect_modifier_bindings(
    modifiers: Any,
    path: str,
    references: dict[str, str],
    default_endpoint: str,
    bindings: list[Binding],
) -> None:
    if not isinstance(modifiers, dict):
        return
    visibility = modifiers.get("visibility")
    if isinstance(visibility, dict):
        when = visibility.get("when")
        collect_visibility_condition_bindings(when, f"{path}.visibility.when", references, default_endpoint, bindings)

    presentation = modifiers.get("presentation")
    if isinstance(presentation, dict):
        add_binding(
            bindings,
            path,
            "Presentation",
            "openState",
            presentation.get("openStateKeypath"),
            "get",
            DISPLAY_TYPES | {"null"},
            references,
            default_endpoint,
        )
        add_binding(
            bindings,
            path,
            "Presentation",
            "closeAction",
            presentation.get("closeActionKeypath"),
            "set",
            {"object", "unknown", "null"},
            references,
            default_endpoint,
        )


def collect_visibility_condition_bindings(
    condition: Any,
    path: str,
    references: dict[str, str],
    default_endpoint: str,
    bindings: list[Binding],
) -> None:
    if not isinstance(condition, dict):
        return

    scope = str(condition.get("scope") or "root")
    raw_keypath = condition.get("keypath")
    if scope == "root" and isinstance(raw_keypath, str) and raw_keypath.strip():
        add_binding(
            bindings,
            path,
            "Visibility",
            "condition",
            raw_keypath,
            "get",
            DISPLAY_TYPES | {"null"},
            references,
            default_endpoint,
        )

    for key in ("allOf", "anyOf"):
        children = condition.get(key)
        if isinstance(children, list):
            for index, child in enumerate(children):
                collect_visibility_condition_bindings(child, f"{path}.{key}[{index}]", references, default_endpoint, bindings)

    if isinstance(condition.get("not"), dict):
        collect_visibility_condition_bindings(condition["not"], f"{path}.not", references, default_endpoint, bindings)


def find_operation(
    operations_by_endpoint: dict[str, list[Operation]],
    endpoint: str,
    key: str,
    method: str,
) -> tuple[Operation | None, bool]:
    operations = operations_by_endpoint.get(endpoint, [])
    for operation in operations:
        if operation.key == key and operation.method == method:
            return operation, False

    prefixes = sorted(
        [
            operation
            for operation in operations
            if operation.method == method and (key.startswith(operation.key + ".") or key.startswith(operation.key + "["))
        ],
        key=lambda op: len(op.key),
        reverse=True,
    )
    if prefixes:
        return prefixes[0], True
    return None, False


def compatible(operation: Operation, binding: Binding) -> tuple[bool, str]:
    schema = operation.return_schema if binding.method == "get" else operation.input_schema
    actual_types = one_of_types(schema)
    if not actual_types:
        actual_types = {operation.return_type if binding.method == "get" else operation.input_type}
    actual_types = {canonical_type(item) for item in actual_types}
    expected = {canonical_type(item) for item in binding.expected_types}
    if "unknown" in actual_types or "unknown" in expected:
        return True, "unknown-compatible"
    if actual_types & expected:
        return True, ",".join(sorted(actual_types))
    if binding.element == "Text" and actual_types <= {"object", "list"}:
        return True, "display-stringified"
    return False, ",".join(sorted(actual_types))


def validate(bindings: list[Binding], operations_by_endpoint: dict[str, list[Operation]]) -> list[Finding]:
    findings: list[Finding] = []
    for binding in bindings:
        operation, used_parent = find_operation(operations_by_endpoint, binding.endpoint, binding.key, binding.method)
        if operation is None:
            findings.append(
                Finding(
                    severity="error",
                    code="missing_explore_contract",
                    message="Skeleton binding references a key/method with no matching Explore operation.",
                    path=binding.path,
                    element=binding.element,
                    role=binding.role,
                    endpoint=binding.endpoint,
                    key=binding.key,
                    method=binding.method,
                )
            )
            continue
        ok, actual = compatible(operation, binding)
        if not ok:
            findings.append(
                Finding(
                    severity="error",
                    code="type_mismatch",
                    message=f"Expected {binding.expected_types}, Explore declares {actual}.",
                    path=binding.path,
                    element=binding.element,
                    role=binding.role,
                    endpoint=binding.endpoint,
                    key=binding.key,
                    method=binding.method,
                )
            )
        elif used_parent:
            findings.append(
                Finding(
                    severity="warn",
                    code="parent_contract_used",
                    message=f"Matched parent contract `{operation.key}`. Add child schema if this nested path is stable.",
                    path=binding.path,
                    element=binding.element,
                    role=binding.role,
                    endpoint=binding.endpoint,
                    key=binding.key,
                    method=binding.method,
                )
            )
    return findings


def render_markdown(
    config_path: Path,
    bindings: list[Binding],
    findings: list[Finding],
    owner_access_affordances: list[OwnerAccessAffordance],
    require_owner_access: bool,
) -> str:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    lines = [
        "# Skeleton Explore Validation",
        "",
        f"Configuration: `{config_path}`",
        "",
        "## Summary",
        "",
        f"- Bindings checked: {len(bindings)}",
        f"- Owner/entity access required: {str(require_owner_access).lower()}",
        f"- Owner/entity access affordances: {len(owner_access_affordances)}",
        f"- Findings: {len(findings)}",
        f"- Errors: {counts.get('error', 0)}",
        f"- Warnings: {counts.get('warn', 0)}",
        "",
        "## Owner/Entity Access",
        "",
    ]
    if not owner_access_affordances:
        lines.append("No owner/entity access affordance found in the skeleton.")
    else:
        for affordance in owner_access_affordances:
            lines.append(
                f"- `{affordance.path}` {affordance.element}/{affordance.reason}: `{affordance.value}`"
            )
    lines.extend([
        "",
        "## Bindings",
        "",
    ])
    if not bindings:
        lines.append("No skeleton bindings found.")
    else:
        for binding in bindings:
            lines.append(
                f"- `{binding.path}` {binding.element}/{binding.role}: `{binding.method}` `{binding.endpoint}` `{binding.key}`"
            )
    lines.extend(["", "## Findings", ""])
    if not findings:
        lines.append("No findings.")
    else:
        for finding in findings:
            lines.extend(
                [
                    f"### {finding.severity.upper()} {finding.code}",
                    "",
                    f"- Path: `{finding.path}`",
                    f"- Element/role: `{finding.element}` / `{finding.role}`",
                    f"- Operation: `{finding.method}` `{finding.endpoint}` `{finding.key}`",
                    f"- Message: {finding.message}",
                    "",
                ]
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, help="Manifest for the default endpoint.")
    parser.add_argument("--contract", action="append", help="ENDPOINT=PATH mapping. May be repeated.")
    parser.add_argument("--manifest-index", type=Path)
    parser.add_argument("--default-endpoint", default="cell:///Porthole")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-error", action="store_true")
    parser.add_argument(
        "--require-owner-access",
        action="store_true",
        help="Require a visible owner-entity / Co-Pilot affordance in the skeleton.",
    )
    args = parser.parse_args()

    config = load_json(args.configuration)
    skeleton, references, discovery_endpoint = extract_configuration_root(config)
    default_endpoint = normalize_endpoint(discovery_endpoint or args.default_endpoint)
    operations_by_endpoint = load_operation_index(args)

    bindings: list[Binding] = []
    collect_bindings(skeleton, "$.skeleton", references, default_endpoint, bindings)
    owner_access_affordances: list[OwnerAccessAffordance] = []
    collect_owner_access_affordances(skeleton, "$.skeleton", owner_access_affordances)
    findings = validate(bindings, operations_by_endpoint)
    findings.extend(validate_owner_access(args.require_owner_access, owner_access_affordances))

    report = {
        "configuration": str(args.configuration),
        "defaultEndpoint": default_endpoint,
        "references": references,
        "bindings": [asdict(binding) for binding in bindings],
        "ownerAccess": {
            "required": args.require_owner_access,
            "purposeRef": OWNER_ACCESS_PURPOSE_REF,
            "affordances": [asdict(affordance) for affordance in owner_access_affordances],
        },
        "findings": [asdict(finding) for finding in findings],
        "summary": {
            "bindings": len(bindings),
            "ownerAccessAffordances": len(owner_access_affordances),
            "errors": sum(1 for finding in findings if finding.severity == "error"),
            "warnings": sum(1 for finding in findings if finding.severity == "warn"),
        },
    }

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(
            render_markdown(args.configuration, bindings, findings, owner_access_affordances, args.require_owner_access),
            encoding="utf-8",
        )

    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    if args.fail_on_error and report["summary"]["errors"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
