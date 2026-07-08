#!/usr/bin/env python3
"""Validate CellProtocol developer identity pack fixtures."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cellprotocol.developerIdentityPack.v0"
UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
DOMAIN_RE = re.compile(r"^domain:[a-z0-9][a-z0-9:._-]*$")
CELL_ENDPOINT_RE = re.compile(r"^cell://")

FORBIDDEN_KEYS = {
    "privateKey",
    "private_key",
    "privateSecureKey",
    "privateKeyBase64URL",
    "privateSeed",
    "seed",
    "mnemonic",
    "rawSecret",
    "secret",
    "routeRefs",
    "privateRoute",
    "rawRoute",
    "pushToken",
    "deviceToken",
    "apnsToken",
    "ownerIdentityUUIDHash",
    "stableOwnerHash",
}

BROAD_CAPABILITIES = {"*", "all", "admin", "root", "state.*", "flow.*", "cell.*"}
REQUIRED_ENTITY_REPRESENTATION_ARRAYS = {
    "types",
    "subTypes",
    "parts",
    "partOf",
    "purposes",
    "interests",
    "entities",
    "states",
    "agreementRefs",
}


class ValidationIssue:
    def __init__(self, path: str, message: str) -> None:
        self.path = path
        self.message = message

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")
    return data


def validate_package(package: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _check_forbidden_keys(package, "$", issues)
    _check_top_level(package, issues)

    domains = _identity_domains(package, issues)
    vault_refs = _vault_refs(package, issues)
    identity_uuid_domains: dict[str, str] = {}
    identity_refs: dict[str, dict[str, Any]] = {}

    for entity_index, entity in enumerate(_list(package.get("entities"))):
        path = f"$.entities[{entity_index}]"
        _check_entity(
            entity,
            path,
            domains,
            vault_refs,
            identity_uuid_domains,
            identity_refs,
            issues,
        )

    _check_explicit_grants(package.get("explicitGrantExamples", []), "$.explicitGrantExamples", identity_refs, issues)
    return issues


def assert_valid(package: dict[str, Any]) -> None:
    issues = validate_package(package)
    if issues:
        raise AssertionError("\n".join(str(issue) for issue in issues))


def _check_forbidden_keys(value: Any, path: str, issues: list[ValidationIssue]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_KEYS:
                issues.append(ValidationIssue(child_path, "forbidden secret or private-route key"))
            _check_forbidden_keys(child, child_path, issues)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _check_forbidden_keys(child, f"{path}[{index}]", issues)


def _check_top_level(package: dict[str, Any], issues: list[ValidationIssue]) -> None:
    if package.get("schema") != SCHEMA:
        issues.append(ValidationIssue("$.schema", f"expected {SCHEMA!r}"))
    if package.get("version") != 0:
        issues.append(ValidationIssue("$.version", "expected version 0"))
    for key in ["identityDomains", "vaults", "entities", "accessPolicy"]:
        if key not in package:
            issues.append(ValidationIssue(f"$.{key}", "missing required key"))

    policy = _dict(package.get("accessPolicy"))
    if policy.get("defaultNonOwnerAccess") != "denied":
        issues.append(ValidationIssue("$.accessPolicy.defaultNonOwnerAccess", "must be denied"))
    if policy.get("requiresExplicitGrant") is not True:
        issues.append(ValidationIssue("$.accessPolicy.requiresExplicitGrant", "must be true"))
    requirements = set(_list(policy.get("nonOwnerRequirements")))
    for required in ["resolverAcceptedContract", "exactCapability", "requesterSignature"]:
        if required not in requirements:
            issues.append(ValidationIssue("$.accessPolicy.nonOwnerRequirements", f"missing {required}"))


def _identity_domains(package: dict[str, Any], issues: list[ValidationIssue]) -> set[str]:
    domains: set[str] = set()
    for index, item in enumerate(_list(package.get("identityDomains"))):
        path = f"$.identityDomains[{index}]"
        domain = item.get("identityDomain") if isinstance(item, dict) else None
        if not isinstance(domain, str) or not DOMAIN_RE.match(domain):
            issues.append(ValidationIssue(path, "identityDomain must start with domain:"))
            continue
        if domain in domains:
            issues.append(ValidationIssue(path, f"duplicate identityDomain {domain}"))
        domains.add(domain)
    return domains


def _vault_refs(package: dict[str, Any], issues: list[ValidationIssue]) -> set[str]:
    refs: set[str] = set()
    for index, vault in enumerate(_list(package.get("vaults"))):
        path = f"$.vaults[{index}]"
        if not isinstance(vault, dict):
            issues.append(ValidationIssue(path, "vault must be an object"))
            continue
        ref = vault.get("vaultRef")
        if not isinstance(ref, str) or not ref.startswith("vault://"):
            issues.append(ValidationIssue(f"{path}.vaultRef", "must start with vault://"))
            continue
        refs.add(ref)
        if vault.get("kind") != "IdentityVault":
            issues.append(ValidationIssue(f"{path}.kind", "must be IdentityVault"))
        if vault.get("exportsKeyMaterial") is not False:
            issues.append(ValidationIssue(f"{path}.exportsKeyMaterial", "must be false"))
    return refs


def _check_entity(
    entity: Any,
    path: str,
    domains: set[str],
    vault_refs: set[str],
    identity_uuid_domains: dict[str, str],
    identity_refs: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(entity, dict):
        issues.append(ValidationIssue(path, "entity must be an object"))
        return
    for key in ["entityRef", "displayName", "identityDomains", "identities", "entityRepresentation", "accessPolicy"]:
        if key not in entity:
            issues.append(ValidationIssue(f"{path}.{key}", "missing required key"))

    entity_domains = _string_list(entity.get("identityDomains"))
    if len(entity_domains) != len(set(entity_domains)):
        issues.append(ValidationIssue(f"{path}.identityDomains", "duplicate identityDomain on entity"))
    for domain in entity_domains:
        if domain not in domains:
            issues.append(ValidationIssue(f"{path}.identityDomains", f"unknown identityDomain {domain}"))

    identities = _list(entity.get("identities"))
    identity_domains = []
    entity_identity_refs: set[str] = set()
    for index, identity in enumerate(identities):
        identity_path = f"{path}.identities[{index}]"
        domain, identity_ref = _check_identity(
            identity,
            identity_path,
            domains,
            vault_refs,
            identity_uuid_domains,
            issues,
        )
        if domain:
            identity_domains.append(domain)
        if identity_ref:
            entity_identity_refs.add(identity_ref)
            identity_refs[identity_ref] = identity

    if set(identity_domains) != set(entity_domains):
        issues.append(
            ValidationIssue(
                f"{path}.identities",
                "entity must have exactly one identity for every listed identityDomain",
            )
        )

    _check_entity_representation(entity.get("entityRepresentation"), f"{path}.entityRepresentation", issues)
    _check_extensions(
        entity.get("entityRepresentationExtensions"),
        f"{path}.entityRepresentationExtensions",
        entity_identity_refs,
        issues,
    )
    _check_entity_access_policy(entity.get("accessPolicy"), f"{path}.accessPolicy", issues)


def _check_identity(
    identity: Any,
    path: str,
    domains: set[str],
    vault_refs: set[str],
    identity_uuid_domains: dict[str, str],
    issues: list[ValidationIssue],
) -> tuple[str | None, str | None]:
    if not isinstance(identity, dict):
        issues.append(ValidationIssue(path, "identity must be an object"))
        return None, None

    identity_ref = identity.get("identityRef")
    uuid = identity.get("uuid")
    domain = identity.get("identityDomain")
    fingerprint = identity.get("publicKeyFingerprint")
    home_vault = identity.get("homeVaultReference")

    if not isinstance(identity_ref, str) or not identity_ref.startswith("identity:"):
        issues.append(ValidationIssue(f"{path}.identityRef", "must start with identity:"))
        identity_ref = None
    if not isinstance(uuid, str) or not UUID_RE.match(uuid):
        issues.append(ValidationIssue(f"{path}.uuid", "must be a UUID string"))
    elif uuid in identity_uuid_domains:
        issues.append(ValidationIssue(f"{path}.uuid", "identity UUID reused in the package"))
    elif isinstance(domain, str):
        identity_uuid_domains[uuid] = domain

    if not isinstance(domain, str) or domain not in domains:
        issues.append(ValidationIssue(f"{path}.identityDomain", "unknown identityDomain"))
        domain = None
    if not isinstance(fingerprint, str) or not SHA256_RE.match(fingerprint):
        issues.append(ValidationIssue(f"{path}.publicKeyFingerprint", "must be sha256:<64 lowercase hex>"))
    if not isinstance(home_vault, str) or home_vault not in vault_refs:
        issues.append(ValidationIssue(f"{path}.homeVaultReference", "must point to a listed vaultRef"))

    policy = _dict(identity.get("keyMaterialPolicy"))
    if policy.get("storage") != "IdentityVault":
        issues.append(ValidationIssue(f"{path}.keyMaterialPolicy.storage", "must be IdentityVault"))
    if policy.get("exportAllowed") is not False:
        issues.append(ValidationIssue(f"{path}.keyMaterialPolicy.exportAllowed", "must be false"))
    if policy.get("fixtureContains") != "public-descriptor-only":
        issues.append(ValidationIssue(f"{path}.keyMaterialPolicy.fixtureContains", "must be public-descriptor-only"))
    return domain, identity_ref


def _check_entity_representation(value: Any, path: str, issues: list[ValidationIssue]) -> None:
    representation = _dict(value)
    if not isinstance(representation.get("name"), str):
        issues.append(ValidationIssue(f"{path}.name", "missing name"))
    for key in REQUIRED_ENTITY_REPRESENTATION_ARRAYS:
        if not isinstance(representation.get(key), list):
            issues.append(ValidationIssue(f"{path}.{key}", "must be a list for Swift decode compatibility"))


def _check_extensions(
    value: Any,
    path: str,
    entity_identity_refs: set[str],
    issues: list[ValidationIssue],
) -> None:
    extensions = _dict(value)
    if extensions.get("schema") != "haven.entityRepresentation.simulated.v0":
        issues.append(ValidationIssue(f"{path}.schema", "unexpected extension schema"))
    for index, ref in enumerate(_list(extensions.get("identityRefs"))):
        if not isinstance(ref, dict) or ref.get("identityRef") not in entity_identity_refs:
            issues.append(ValidationIssue(f"{path}.identityRefs[{index}]", "identityRef must refer to an entity identity"))
    for index, endpoint in enumerate(_list(extensions.get("contactEndpointRefs"))):
        _check_contact_endpoint(endpoint, f"{path}.contactEndpointRefs[{index}]", issues)


def _check_contact_endpoint(endpoint: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(endpoint, dict):
        issues.append(ValidationIssue(path, "contact endpoint must be an object"))
        return
    if not isinstance(endpoint.get("endpointId"), str):
        issues.append(ValidationIssue(f"{path}.endpointId", "missing endpointId"))
    if not isinstance(endpoint.get("endpointCell"), str) or not CELL_ENDPOINT_RE.match(endpoint["endpointCell"]):
        issues.append(ValidationIssue(f"{path}.endpointCell", "must be a cell:// endpoint"))
    if "contact.request" not in _string_list(endpoint.get("acceptedTopics")):
        issues.append(ValidationIssue(f"{path}.acceptedTopics", "must include contact.request"))
    if "purpose://personal.chat.invite.receive" not in _string_list(endpoint.get("purposes")):
        issues.append(ValidationIssue(f"{path}.purposes", "must include purpose://personal.chat.invite.receive"))
    policy = _dict(endpoint.get("policy"))
    if policy.get("mode") != "ownerApprovalRequired":
        issues.append(ValidationIssue(f"{path}.policy.mode", "must be ownerApprovalRequired"))
    if policy.get("requireSignature") is not True:
        issues.append(ValidationIssue(f"{path}.policy.requireSignature", "must be true"))
    if policy.get("requireExpiry") is not True:
        issues.append(ValidationIssue(f"{path}.policy.requireExpiry", "must be true"))


def _check_entity_access_policy(value: Any, path: str, issues: list[ValidationIssue]) -> None:
    policy = _dict(value)
    if policy.get("ownerAccess") != "ownerProofRequired":
        issues.append(ValidationIssue(f"{path}.ownerAccess", "must be ownerProofRequired"))
    if policy.get("defaultNonOwnerAccess") != "denied":
        issues.append(ValidationIssue(f"{path}.defaultNonOwnerAccess", "must be denied"))
    if policy.get("requiresExplicitGrant") is not True:
        issues.append(ValidationIssue(f"{path}.requiresExplicitGrant", "must be true"))


def _check_explicit_grants(
    value: Any,
    path: str,
    identity_refs: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    for index, grant in enumerate(_list(value)):
        grant_path = f"{path}[{index}]"
        if not isinstance(grant, dict):
            issues.append(ValidationIssue(grant_path, "grant must be an object"))
            continue
        subject = grant.get("subjectIdentityRef")
        if subject not in identity_refs:
            issues.append(ValidationIssue(f"{grant_path}.subjectIdentityRef", "unknown subject identity"))
        capabilities = _string_list(grant.get("capabilities"))
        if not capabilities:
            issues.append(ValidationIssue(f"{grant_path}.capabilities", "must not be empty"))
        for cap_index, capability in enumerate(capabilities):
            if capability in BROAD_CAPABILITIES or capability.endswith(".*"):
                issues.append(ValidationIssue(f"{grant_path}.capabilities[{cap_index}]", "broad capability is not allowed"))
        if grant.get("requiresOwnerApproval") is not True:
            issues.append(ValidationIssue(f"{grant_path}.requiresOwnerApproval", "must be true"))


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [item for item in _list(value) if isinstance(item, str)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to a developer identity pack JSON file")
    args = parser.parse_args(argv)

    try:
        package = load_package(args.path)
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"failed to load package: {error}", file=sys.stderr)
        return 2

    issues = validate_package(package)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"valid developer identity pack: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

