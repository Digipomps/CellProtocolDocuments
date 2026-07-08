#!/usr/bin/env python3
"""Resolve an invite command against the generated developer invite seed."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Tools.DeveloperIdentityPack.generate_invite_relations import (  # noqa: E402
    DEFAULT_OUTPUT,
    validate_invite_seed,
)


INVITE_MARKERS = ["inviter", "invite", "legg til", "add", "ta med"]


def load_seed(path: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        seed = json.load(handle)
    if not isinstance(seed, dict):
        raise ValueError("invite seed must be a JSON object")
    issues = validate_invite_seed(seed)
    if issues:
        raise ValueError("\n".join(str(issue) for issue in issues))
    return seed


def resolve_invite_command(
    seed: dict[str, Any],
    command: str,
    message_body: str | None = None,
) -> dict[str, Any]:
    """Resolve an invite phrase to profile/contact refs and a simulated reply."""

    issues = validate_invite_seed(seed)
    if issues:
        raise ValueError("\n".join(str(issue) for issue in issues))

    target_phrase = invite_target_phrase(command)
    relation = _best_relation(seed, target_phrase)
    if relation is None:
        return {
            "ok": False,
            "command": command,
            "targetPhrase": target_phrase,
            "error": "no_invite_relation_match",
            "message": "No generated invite relation matched the command.",
        }

    endpoint = relation["contact"]["endpoints"][0]
    policy = relation["simulation"]["responsePolicy"]
    simulated_reply = _select_reply(policy, message_body or command)
    relation_ref = f"relations.people[id={relation['id']}]"

    return {
        "ok": True,
        "command": command,
        "targetPhrase": target_phrase,
        "matchedRelationRef": relation_ref,
        "profileID": relation["profileID"],
        "ownerUUID": relation["ownerUUID"],
        "displayName": relation["displayName"],
        "contactEndpoint": {
            "endpointId": endpoint["endpointId"],
            "endpointCell": endpoint["endpointCell"],
            "purposes": endpoint["purposes"],
            "interests": endpoint["interests"],
            "visibility": endpoint["visibility"],
        },
        "messagePayload": {
            "profileID": relation["profileID"],
            "contactEndpointID": endpoint["endpointId"],
            "contactEndpointCell": endpoint["endpointCell"],
            "body": message_body or "",
        },
        "simulatedReply": {
            "fromRelationRef": relation_ref,
            "policyRef": f"{relation_ref}.simulation.responsePolicy",
            "body": simulated_reply,
            "requiresAcceptedInviteBeforeReply": policy.get("requiresAcceptedInviteBeforeReply") is True,
        },
        "security": {
            "authority": "none_from_lookup",
            "notes": [
                "The resolved profile and endpoint are owner-local routing hints.",
                "Sending still requires the runtime ContactEndpoint/Resolver policy.",
                "The simulated reply is test data, not proof that an external user received a message.",
            ],
        },
    }


def invite_target_phrase(text: str) -> str:
    lower = text.lower()
    for marker in INVITE_MARKERS:
        match = lower.find(marker)
        if match >= 0:
            suffix = text[match + len(marker):]
            return (
                suffix.replace("i chatten", "")
                .replace("til chatten", "")
                .strip()
            )
    return text.strip()


def _best_relation(seed: dict[str, Any], target_phrase: str) -> dict[str, Any] | None:
    relations = seed.get("relations", {}).get("people", [])
    target_tokens = _tokens(target_phrase)
    best_score = 0.0
    best_relation: dict[str, Any] | None = None

    for relation in relations:
        if not isinstance(relation, dict):
            continue
        haystack_values = [
            relation.get("displayName", ""),
            relation.get("headline", ""),
            relation.get("summary", ""),
            relation.get("relationship", ""),
            *_string_list(relation.get("interests")),
            *_string_list(relation.get("purposeRefs")),
        ]
        haystack = " ".join(haystack_values)
        score = _match_score(target_phrase, target_tokens, haystack, relation.get("displayName", ""))
        if score > best_score:
            best_score = score
            best_relation = relation

    if best_score < 0.20:
        return None
    return best_relation


def _match_score(target_phrase: str, target_tokens: set[str], haystack: str, display_name: str) -> float:
    if not target_phrase.strip():
        return 0.0
    haystack_lower = haystack.lower()
    target_lower = target_phrase.lower()
    if target_lower in str(display_name).lower():
        return 0.95
    if target_lower in haystack_lower:
        return 0.80
    haystack_tokens = _tokens(haystack)
    overlap = len(target_tokens.intersection(haystack_tokens))
    return overlap / max(1, len(target_tokens))


def _select_reply(policy: dict[str, Any], message_body: str) -> str:
    replies = _string_list(policy.get("suggestedReplies"))
    if not replies:
        return "Invitasjon mottatt. Jeg kan svare som simulert testrelasjon."
    message_tokens = _tokens(message_body)
    topics = _string_list(policy.get("topics"))
    if message_tokens.intersection(_tokens(" ".join(topics))) and len(replies) > 1:
        return replies[1]
    return replies[0]


def _tokens(text: str) -> set[str]:
    return {token for token in re.split(r"[^A-Za-z0-9]+", text.lower()) if token}


def _string_list(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", help="Invite command, for example: inviter Jonas")
    parser.add_argument("--seed", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--message", default="", help="Optional message body for simulated reply selection")
    args = parser.parse_args(argv)

    try:
        seed = load_seed(args.seed)
        result = resolve_invite_command(seed, args.command, message_body=args.message)
    except Exception as error:  # pragma: no cover - CLI guard
        print(f"failed to resolve invite command: {error}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
