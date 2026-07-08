#!/usr/bin/env python3
"""Project a developer identity pack into owner-local chat invite seed data."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Tools.DeveloperIdentityPack.validate_identity_pack import (  # noqa: E402
    CELL_ENDPOINT_RE,
    FORBIDDEN_KEYS,
    ValidationIssue,
    load_package,
    validate_package,
)


SCHEMA = "cellprotocol.developerIdentityPack.inviteRelationSeed.v0"
DEFAULT_PACK = ROOT / "Tools" / "DeveloperIdentityPack" / "fixtures" / "developer_identity_pack.v0.json"
DEFAULT_OUTPUT = ROOT / "Tools" / "DeveloperIdentityPack" / "generated" / "developer_invite_relations.v0.json"
DEFAULT_REQUESTER_ENTITY_REF = "entity:dev-sim:eira"

INVITE_PURPOSE = "personal.chat.invite.receive"
SIMULATION_PURPOSE = "personal.chat.simulation.respond"
ASSIST_PURPOSE = "personal.chat.assist.invite"
CONTACT_DESCRIPTOR_SCHEMA = "haven.contact-endpoint.descriptor.v1"

SAFE_MUTATION_PREFIXES = (
    "relations.people[+]",
    "relations.entities.",
    "relations.identities.",
    "relations.chatInvites",
    "entityRepresentation.chatInviteProfile",
)

PERSONA_POLICIES: dict[str, dict[str, Any]] = {
    "entity:dev-sim:eira": {
        "headline": "Product and conference test persona",
        "relationship": "simulated-product-collaborator",
        "summary": "Simulated owner/developer persona for product, HAVEN team and conference invite tests.",
        "rolePrompt": (
            "Du er Eira, en simulert produktorientert utviklerpersona. "
            "Svar kort, si tydelig at du er simulert hvis noen spor, og hjelp til med aa teste om inviteflyten er klar."
        ),
        "topics": ["product", "havendev", "conference"],
        "suggestedReplies": [
            "Jeg kan bli med i testchatten. Send gjerne scenariet du vil at jeg skal validere.",
            "I denne testen ser jeg spesielt paa om invitasjonsteksten og endpoint-statusen er forstaaelig.",
        ],
    },
    "entity:dev-sim:jonas": {
        "headline": "Security and backend reviewer",
        "relationship": "simulated-security-reviewer",
        "summary": "Simulated developer relation for security, backend and access-control invite tests.",
        "rolePrompt": (
            "Du er Jonas, en simulert sikkerhets- og backendreviewer. "
            "Svar med konkrete tilgangskontroll-observasjoner og hold svaret avgrenset til testen."
        ),
        "topics": ["security", "backend", "havendev"],
        "suggestedReplies": [
            "Invitasjon mottatt. Jeg sjekker at endpoint-referansen bare er et rutinghint og ikke autoritet.",
            "For denne testen forventer jeg signerte, utlopende kontaktforesporsler og ingen privat rutemateriale i payload.",
        ],
    },
    "entity:dev-sim:mina": {
        "headline": "Conference participant and policy tester",
        "relationship": "simulated-conference-participant",
        "summary": "Simulated conference participant relation for event, policy and participant invite tests.",
        "rolePrompt": (
            "Du er Mina, en simulert konferansedeltaker. "
            "Svar som en deltaker som trenger praktisk kontekst og tydelige samtykkegrenser."
        ),
        "topics": ["participant", "conference", "policy"],
        "suggestedReplies": [
            "Jeg kan svare som simulert deltaker. Si hva invitasjonen gjelder og hvilke data testen trenger.",
            "I denne testen ser jeg etter tydelig formaal, samtykkegrense og neste steg i invitasjonen.",
        ],
    },
    "entity:dev-sim:noor": {
        "headline": "Operations and team admin tester",
        "relationship": "simulated-operations-admin",
        "summary": "Simulated operations relation for admin, team and staging-swarm invite tests.",
        "rolePrompt": (
            "Du er Noor, en simulert operations/admin-persona. "
            "Svar med praktiske driftsjekker og ikke lat som du har reell adminautoritet."
        ),
        "topics": ["admin", "operations", "team"],
        "suggestedReplies": [
            "Invitasjon mottatt. Jeg sjekker at dette holder seg i simulert owner-local testkontekst.",
            "For testen kan jeg sjekke navngiving, endpoint-beredskap og om handlingen krever eksplisitt eiergodkjenning.",
        ],
    },
}


def build_invite_seed(
    package: dict[str, Any],
    requester_entity_ref: str = DEFAULT_REQUESTER_ENTITY_REF,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic EntityAnchor invite seed object."""

    issues = validate_package(package)
    if issues:
        raise ValueError("\n".join(str(issue) for issue in issues))

    generated_at = generated_at or str(package.get("generatedAt") or "2026-07-06T00:00:00Z")
    relation_rows: list[dict[str, Any]] = []
    entity_records: dict[str, dict[str, Any]] = {}
    identity_records: dict[str, dict[str, Any]] = {}

    for entity in package.get("entities", []):
        if not isinstance(entity, dict):
            continue
        if entity.get("entityRef") == requester_entity_ref:
            continue
        if not _is_invitable_simulated_entity(entity):
            continue

        relation = _relation_from_entity(entity, generated_at)
        relation_rows.append(relation)

        entity_id = relation["entityRef"].split(".")[-1]
        endpoint_id = relation["contact"]["endpoints"][0]["endpointId"]
        entity_records[entity_id] = _entity_record_from_relation(relation, endpoint_id)

        for identity in entity.get("identities", []):
            if not isinstance(identity, dict):
                continue
            identity_id = _identity_record_id(identity)
            identity_records[identity_id] = _identity_record(identity, entity_id)

    relation_rows.sort(key=lambda item: item["displayName"].lower())
    entity_records = dict(sorted(entity_records.items()))
    identity_records = dict(sorted(identity_records.items()))
    chat_invite_profile = _chat_invite_profile(relation_rows)

    seed_mutations: list[dict[str, Any]] = []
    seed_mutations.extend({"keypath": "relations.people[+]", "value": relation} for relation in relation_rows)
    seed_mutations.extend(
        {"keypath": f"relations.entities.{entity_id}", "value": record}
        for entity_id, record in entity_records.items()
    )
    seed_mutations.extend(
        {"keypath": f"relations.identities.{identity_id}", "value": record}
        for identity_id, record in identity_records.items()
    )
    seed_mutations.append({"keypath": "relations.chatInvites", "value": _empty_chat_invite_bookkeeping()})
    seed_mutations.append({"keypath": "entityRepresentation.chatInviteProfile", "value": chat_invite_profile})

    return {
        "schema": SCHEMA,
        "version": 0,
        "generatedAt": generated_at,
        "sourcePack": {
            "schema": package.get("schema"),
            "generatedAt": package.get("generatedAt"),
            "contentHash": _package_hash(package),
        },
        "requesterEntityRef": requester_entity_ref,
        "intendedRuntime": {
            "cellEndpoint": "cell:///EntityAnchor",
            "ownerLocalKeypaths": [
                "relations.people",
                "relations.entities",
                "relations.identities",
                "relations.chatInvites",
                "entityRepresentation.chatInviteProfile",
            ],
            "personalCopilotLookupPath": "relations.people",
            "inviteCommandExamples": _prompt_examples(relation_rows),
        },
        "access": {
            "ownerAccess": "ownerProofRequired",
            "defaultNonOwnerAccess": "denied",
            "requiresExplicitGrant": True,
            "notes": [
                "Names and profile ids are lookup hints inside the owner's EntityAnchor.",
                "Endpoint ids are routing hints and do not grant access.",
                "Private keys and private route material stay inside IdentityVault and ContactEndpointCell.",
            ],
        },
        "relations": {
            "people": relation_rows,
            "entities": entity_records,
            "identities": identity_records,
            "chatInvites": _empty_chat_invite_bookkeeping(),
        },
        "entityRepresentation": {
            "chatInviteProfile": chat_invite_profile,
        },
        "seedMutations": seed_mutations,
    }


def validate_invite_seed(seed: dict[str, Any]) -> list[ValidationIssue]:
    """Validate the generated owner-local invite seed."""

    issues: list[ValidationIssue] = []
    _check_forbidden_keys(seed, "$", issues)

    if seed.get("schema") != SCHEMA:
        issues.append(ValidationIssue("$.schema", f"expected {SCHEMA!r}"))
    if seed.get("version") != 0:
        issues.append(ValidationIssue("$.version", "expected version 0"))

    access = _dict(seed.get("access"))
    if access.get("defaultNonOwnerAccess") != "denied":
        issues.append(ValidationIssue("$.access.defaultNonOwnerAccess", "must be denied"))
    if access.get("requiresExplicitGrant") is not True:
        issues.append(ValidationIssue("$.access.requiresExplicitGrant", "must be true"))

    relations = _dict(seed.get("relations"))
    people = _list(relations.get("people"))
    if not people:
        issues.append(ValidationIssue("$.relations.people", "must contain at least one relation"))

    seen_profile_ids: set[str] = set()
    for index, relation in enumerate(people):
        path = f"$.relations.people[{index}]"
        if not isinstance(relation, dict):
            issues.append(ValidationIssue(path, "relation must be an object"))
            continue
        _check_relation(relation, path, seen_profile_ids, issues)

    invite_profile = _dict(_dict(seed.get("entityRepresentation")).get("chatInviteProfile"))
    candidate_refs = _string_list(invite_profile.get("candidateRefs"))
    expected_candidate_refs = [f"relations.people[id={relation['id']}]" for relation in people if isinstance(relation, dict)]
    if candidate_refs != expected_candidate_refs:
        issues.append(ValidationIssue("$.entityRepresentation.chatInviteProfile.candidateRefs", "must match relation rows"))

    for index, mutation in enumerate(_list(seed.get("seedMutations"))):
        path = f"$.seedMutations[{index}]"
        if not isinstance(mutation, dict):
            issues.append(ValidationIssue(path, "mutation must be an object"))
            continue
        keypath = mutation.get("keypath")
        if not isinstance(keypath, str) or not keypath.startswith(SAFE_MUTATION_PREFIXES):
            issues.append(ValidationIssue(f"{path}.keypath", "mutation keypath is not an allowed owner-local invite seed path"))
        if "value" not in mutation:
            issues.append(ValidationIssue(f"{path}.value", "missing mutation value"))

    return issues


def _relation_from_entity(entity: dict[str, Any], generated_at: str) -> dict[str, Any]:
    entity_ref = _required_string(entity, "entityRef")
    display_name = _required_string(entity, "displayName")
    slug = _safe_slug(entity_ref.split(":")[-1])
    relation_id = f"person-dev-sim-{slug}"
    entity_id = f"entity-dev-sim-{slug}"
    policy = PERSONA_POLICIES.get(entity_ref, _default_persona_policy(display_name))
    primary_identity = _primary_identity(entity)
    extensions = _dict(entity.get("entityRepresentationExtensions"))
    chat_profile = _dict(extensions.get("chatInviteProfile"))
    endpoint = _normalized_endpoint(_list(extensions.get("contactEndpointRefs"))[0], chat_profile)
    lookup_tokens = _string_list(chat_profile.get("lookupTokens"))
    interest_refs = _string_list(chat_profile.get("interestRefs"))
    persona_topics = _string_list(policy.get("topics"))
    interests = _normalize_strings(
        lookup_tokens
        + interest_refs
        + persona_topics
        + [
            display_name,
            display_name.split()[0],
            policy["relationship"],
            "invite-candidate",
            "simulated-ai-persona",
            "private-relation",
        ]
    )
    purpose_refs = _normalize_strings(
        [_strip_purpose_ref(item) for item in _string_list(chat_profile.get("purposeRefs"))]
        + [ASSIST_PURPOSE, SIMULATION_PURPOSE, INVITE_PURPOSE]
    )
    identity_refs = [
        _identity_record_id(identity)
        for identity in entity.get("identities", [])
        if isinstance(identity, dict)
    ]

    return {
        "id": relation_id,
        "profileID": f"relation-{relation_id}",
        "ownerUUID": primary_identity["uuid"],
        "identityRefs": [f"relations.identities.{identity_id}" for identity_id in identity_refs],
        "entityRef": f"relations.entities.{entity_id}",
        "displayName": display_name,
        "headline": policy["headline"],
        "summary": policy["summary"],
        "sourceEntityRef": entity_ref,
        "relationship": policy["relationship"],
        "status": "simulated",
        "contactEndpointID": endpoint["endpointId"],
        "contactEndpointCell": endpoint["endpointCell"],
        "contactEndpointPurposes": endpoint["purposes"],
        "contactEndpointInterests": endpoint["interests"],
        "contact": {
            "endpointStatus": "simulated-endpoint",
            "endpoints": [endpoint],
        },
        "purposeRefs": purpose_refs,
        "interests": interests,
        "simulation": {
            "enabled": True,
            "agentKind": "ai-persona",
            "disclosureLabel": _dict(entity.get("simulation")).get("disclosureLabel", "Simulated developer persona"),
            "personaRef": f"developerIdentityPack.entities[{entity_ref}]",
            "rolePrompt": policy["rolePrompt"],
            "behaviorInstructions": [
                "Say clearly that you are simulated if asked.",
                "Keep replies scoped to the active test scenario.",
                "Do not claim proof-backed identity, external delivery or real-world contact.",
            ],
            "responsePolicy": {
                "mode": "test-relevant-short-reply",
                "language": "nb",
                "maxSuggestedReplySentences": 2,
                "topics": persona_topics,
                "suggestedReplies": policy["suggestedReplies"],
                "requiresAcceptedInviteBeforeReply": True,
            },
            "perspectivePurposeRefs": [SIMULATION_PURPOSE, ASSIST_PURPOSE],
            "perspectiveInterestRefs": _normalize_strings(persona_topics + interest_refs),
            "allowedTooling": [
                "PerspectiveCell.matchPurpose",
                "PerspectiveCell.perspective.query.activePurposes",
                "PerspectiveCell.perspective.query.interestsFromActivePurposes",
            ],
            "mustNot": [
                "impersonate-real-person",
                "send-external-message",
                "claim-proof-backed-identity",
                "read-owner-private-data-without-grant",
            ],
        },
        "createdAt": generated_at,
        "updatedAt": generated_at,
    }


def _entity_record_from_relation(relation: dict[str, Any], endpoint_id: str) -> dict[str, Any]:
    relation_id = relation["id"]
    return {
        "entityKind": "simulated-person-representation",
        "label": relation["displayName"],
        "status": "simulated",
        "identityRefs": relation["identityRefs"],
        "relationRefs": [f"relations.people[id={relation_id}]"],
        "contactEndpointRefs": [
            f"relations.people[id={relation_id}].contact.endpoints[endpointId={endpoint_id}]",
        ],
        "simulationRef": f"relations.people[id={relation_id}].simulation",
        "sourceEntityRef": relation["sourceEntityRef"],
    }


def _identity_record(identity: dict[str, Any], entity_id: str) -> dict[str, Any]:
    return {
        "identityRef": identity["identityRef"],
        "identityUUID": identity["uuid"],
        "domain": identity["identityDomain"],
        "displayName": identity.get("displayName", ""),
        "publicKeyFingerprint": identity["publicKeyFingerprint"],
        "homeVaultReference": identity["homeVaultReference"],
        "entityRefs": [f"relations.entities.{entity_id}"],
        "proofRefs": [],
        "source": "developerIdentityPack.publicDescriptor",
        "keyMaterialPolicy": {
            "storage": "IdentityVault",
            "exportAllowed": False,
            "fixtureContains": "public-descriptor-only",
        },
    }


def _chat_invite_profile(relations: list[dict[str, Any]]) -> dict[str, Any]:
    lookup_tokens: list[str] = []
    interest_refs: list[str] = []
    candidate_refs: list[str] = []
    endpoint_refs: list[str] = []

    for relation in relations:
        relation_id = relation["id"]
        endpoint_id = relation["contact"]["endpoints"][0]["endpointId"]
        candidate_refs.append(f"relations.people[id={relation_id}]")
        endpoint_refs.append(f"relations.people[id={relation_id}].contact.endpoints[endpointId={endpoint_id}]")
        lookup_tokens.extend(_lookup_tokens_for_relation(relation))
        interest_refs.extend(relation["interests"])

    return {
        "purposeRefs": [ASSIST_PURPOSE, SIMULATION_PURPOSE, INVITE_PURPOSE],
        "interestRefs": _normalize_strings(interest_refs + ["invite-candidate", "contact-endpoint", "simulated-ai-persona"]),
        "lookupTokens": _normalize_strings(lookup_tokens),
        "candidateRefs": candidate_refs,
        "contactEndpointRefs": endpoint_refs,
        "simulationResponseRefs": [f"{candidate}.simulation.responsePolicy" for candidate in candidate_refs],
        "notes": "Generated owner-local invite candidates. Seed into cell:///EntityAnchor before testing 'inviter <name>'.",
    }


def _empty_chat_invite_bookkeeping() -> dict[str, Any]:
    return {
        "pending": [],
        "history": [],
        "notes": "Operational chat state lives in PersonalCopilot/Chat cells. This root holds owner-local refs only.",
    }


def _normalized_endpoint(endpoint: Any, chat_profile: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(endpoint, dict):
        raise ValueError("contact endpoint ref must be an object")
    purposes = _normalize_strings(
        [_strip_purpose_ref(item) for item in _string_list(endpoint.get("purposes"))]
        + [INVITE_PURPOSE, SIMULATION_PURPOSE]
    )
    interests = _normalize_strings(
        _string_list(chat_profile.get("interestRefs"))
        + _string_list(chat_profile.get("lookupTokens"))
        + ["invite-only-chat", "contact-endpoint", "simulated-ai-persona"]
    )
    return {
        "endpointId": endpoint["endpointId"],
        "endpointID": endpoint["endpointId"],
        "endpointCell": endpoint["endpointCell"],
        "cell": endpoint["endpointCell"],
        "registryEndpoint": "cell:///ContactEndpointRegistry",
        "descriptorSchema": CONTACT_DESCRIPTOR_SCHEMA,
        "schema": CONTACT_DESCRIPTOR_SCHEMA,
        "purposes": purposes,
        "acceptedTopics": _normalize_strings(_string_list(endpoint.get("acceptedTopics")) + ["chat.invitation"]),
        "interests": interests,
        "discoverabilityContext": "developer-identity-pack-invite-seed",
        "visibility": "owner-private",
        "policy": {
            "mode": "ownerApprovalRequired",
            "requireSignature": True,
            "requireExpiry": True,
        },
    }


def _check_relation(
    relation: dict[str, Any],
    path: str,
    seen_profile_ids: set[str],
    issues: list[ValidationIssue],
) -> None:
    for key in ["id", "profileID", "ownerUUID", "displayName", "entityRef", "contact", "simulation"]:
        if key not in relation:
            issues.append(ValidationIssue(f"{path}.{key}", "missing required key"))

    profile_id = relation.get("profileID")
    if not isinstance(profile_id, str) or profile_id in seen_profile_ids:
        issues.append(ValidationIssue(f"{path}.profileID", "must be a unique string"))
    elif profile_id:
        seen_profile_ids.add(profile_id)

    contact = _dict(relation.get("contact"))
    if contact.get("endpointStatus") != "simulated-endpoint":
        issues.append(ValidationIssue(f"{path}.contact.endpointStatus", "must be simulated-endpoint"))
    endpoints = _list(contact.get("endpoints"))
    if len(endpoints) != 1:
        issues.append(ValidationIssue(f"{path}.contact.endpoints", "must contain exactly one endpoint"))
    else:
        _check_seed_endpoint(endpoints[0], f"{path}.contact.endpoints[0]", issues)

    simulation = _dict(relation.get("simulation"))
    if simulation.get("enabled") is not True:
        issues.append(ValidationIssue(f"{path}.simulation.enabled", "must be true"))
    if not isinstance(simulation.get("rolePrompt"), str) or not simulation["rolePrompt"].strip():
        issues.append(ValidationIssue(f"{path}.simulation.rolePrompt", "missing rolePrompt"))
    response_policy = _dict(simulation.get("responsePolicy"))
    if response_policy.get("mode") != "test-relevant-short-reply":
        issues.append(ValidationIssue(f"{path}.simulation.responsePolicy.mode", "unexpected response mode"))
    if not _string_list(response_policy.get("suggestedReplies")):
        issues.append(ValidationIssue(f"{path}.simulation.responsePolicy.suggestedReplies", "must not be empty"))
    must_not = set(_string_list(simulation.get("mustNot")))
    for required in ["impersonate-real-person", "send-external-message", "claim-proof-backed-identity"]:
        if required not in must_not:
            issues.append(ValidationIssue(f"{path}.simulation.mustNot", f"missing {required}"))


def _check_seed_endpoint(endpoint: Any, path: str, issues: list[ValidationIssue]) -> None:
    if not isinstance(endpoint, dict):
        issues.append(ValidationIssue(path, "endpoint must be an object"))
        return
    if not isinstance(endpoint.get("endpointId"), str):
        issues.append(ValidationIssue(f"{path}.endpointId", "missing endpointId"))
    if not isinstance(endpoint.get("endpointCell"), str) or not CELL_ENDPOINT_RE.match(endpoint["endpointCell"]):
        issues.append(ValidationIssue(f"{path}.endpointCell", "must be a cell:// endpoint"))
    purposes = set(_string_list(endpoint.get("purposes")))
    for required in [INVITE_PURPOSE, SIMULATION_PURPOSE]:
        if required not in purposes:
            issues.append(ValidationIssue(f"{path}.purposes", f"missing {required}"))
    if "chat.invitation" not in _string_list(endpoint.get("acceptedTopics")):
        issues.append(ValidationIssue(f"{path}.acceptedTopics", "must include chat.invitation"))
    policy = _dict(endpoint.get("policy"))
    if policy.get("mode") != "ownerApprovalRequired":
        issues.append(ValidationIssue(f"{path}.policy.mode", "must be ownerApprovalRequired"))


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


def _is_invitable_simulated_entity(entity: dict[str, Any]) -> bool:
    simulation = _dict(entity.get("simulation"))
    extensions = _dict(entity.get("entityRepresentationExtensions"))
    if simulation.get("enabled") is not True:
        return False
    if simulation.get("kind") == "service":
        return False
    return bool(_list(extensions.get("contactEndpointRefs")))


def _primary_identity(entity: dict[str, Any]) -> dict[str, Any]:
    identities = [identity for identity in entity.get("identities", []) if isinstance(identity, dict)]
    preferred_domains = [
        "domain:personal:dev",
        "domain:team:haven-dev",
        "domain:conference:arendalsuka-demo",
        "domain:agent:personal-copilot-dev",
    ]
    for domain in preferred_domains:
        for identity in identities:
            if identity.get("identityDomain") == domain:
                return identity
    if not identities:
        raise ValueError(f"entity {entity.get('entityRef')} has no identities")
    return identities[0]


def _identity_record_id(identity: dict[str, Any]) -> str:
    return _safe_slug(str(identity.get("identityRef", "identity-unknown")))


def _lookup_tokens_for_relation(relation: dict[str, Any]) -> list[str]:
    display_name = relation["displayName"]
    return [
        display_name,
        display_name.split()[0],
        relation["headline"],
        relation["relationship"],
        *relation["interests"],
    ]


def _prompt_examples(relations: list[dict[str, Any]]) -> list[str]:
    examples: list[str] = []
    for relation in relations:
        first_name = relation["displayName"].split()[0]
        examples.append(f"inviter {first_name}")
    return examples


def _default_persona_policy(display_name: str) -> dict[str, Any]:
    return {
        "headline": "Simulated invite test persona",
        "relationship": "simulated-collaborator",
        "summary": f"Simulated relation for chat invite tests with {display_name}.",
        "rolePrompt": (
            f"Du er {display_name}, en simulert chat-invite testpersona. "
            "Svar kort og hold deg innenfor eksplisitt testkontekst."
        ),
        "topics": ["developer-testing"],
        "suggestedReplies": [
            "Invitasjon mottatt. Jeg kan svare som simulert relasjon for denne testen.",
        ],
    }


def _strip_purpose_ref(value: str) -> str:
    return value.removeprefix("purpose://")


def _normalize_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        cleaned = value.strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized


def _package_hash(package: dict[str, Any]) -> str:
    payload = json.dumps(package, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "unknown"


def _required_string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing {key}")
    return value


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [item for item in _list(value) if isinstance(item, str)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK, help="Developer identity pack JSON")
    parser.add_argument("--requester-entity-ref", default=DEFAULT_REQUESTER_ENTITY_REF)
    parser.add_argument("--generated-at", default=None, help="Override generatedAt for reproducible fixtures")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Seed JSON to write with --write")
    parser.add_argument("--write", action="store_true", help="Write the generated seed instead of printing to stdout")
    args = parser.parse_args(argv)

    try:
        package = load_package(args.pack)
        seed = build_invite_seed(package, requester_entity_ref=args.requester_entity_ref, generated_at=args.generated_at)
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"failed to build invite seed: {error}", file=sys.stderr)
        return 2

    issues = validate_invite_seed(seed)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(seed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote invite relation seed: {args.output}")
        return 0

    print(json.dumps(seed, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
