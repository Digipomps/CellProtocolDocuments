#!/usr/bin/env python3
"""Run Co-pilot chat language benchmark cases through llama-cli.

This runner is intentionally small and dependency-free. It is a smoke/eval
adapter for local GGUF models, not a replacement for product UI tests.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CASES = ROOT / "cases.no.jsonl"
DEFAULT_CONTEXTS = ROOT / "conference_contexts.v1.json"
DEFAULT_OUT = ROOT / "results" / "run.jsonl"

INTENT_LABELS = [
    "recommend_agenda_item",
    "open_agenda_item",
    "draft_meeting_request",
    "recommend_person",
    "request_private_contact_info",
    "request_sponsor_leads_private",
    "request_sponsor_aggregate_report",
    "request_sponsor_consent_report",
    "answer_profile_visibility",
    "answer_schedule_question",
    "answer_location_question",
    "answer_people_lookup",
    "explain_capability_or_grant",
    "explain_policy_plain_language",
    "explain_conference_purpose",
    "set_or_explain_privacy_preference",
    "explain_privacy_preserving_networking",
    "request_data_deletion_or_privacy_action",
    "request_publish_content",
    "summarize_session_thread",
    "request_schedule_change",
    "rewrite_or_draft_message",
    "unsupported_or_ambiguous_action",
    "ambiguous_request",
]

SAFETY_LABELS = [
    "allow",
    "allow_with_user_click",
    "allow_aggregate_only",
    "allow_consented_only",
    "deny_private_data",
    "needs_clarification",
    "needs_context",
    "needs_review",
    "requires_explicit_confirmation",
    "requires_role_and_confirmation",
    "requires_review_and_click",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return rows


def load_contexts(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_context(contexts: dict[str, Any], key: str) -> dict[str, Any]:
    if key not in contexts:
        raise KeyError(f"Unknown contextRef: {key}")
    context = contexts[key]
    if "extends" not in context:
        return dict(context)

    parent = resolve_context(contexts, context["extends"])
    merged = dict(parent)
    for child_key, child_value in context.items():
        if child_key == "extends":
            continue
        merged[child_key] = child_value
    return merged


def context_to_text(context: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"Nå: {context.get('now', 'ukjent')}")

    lines.append("Agenda:")
    for item in context.get("agenda", []):
        topics = ", ".join(item.get("topics", []))
        lines.append(
            f"- {item['id']}: {item['time']} {item['room']} - {item['title']} "
            f"(tema: {topics})"
        )

    interests = ", ".join(context.get("participantInterests", []))
    lines.append(f"Deltakerens interesser: {interests}")

    lines.append("Synlige profiler:")
    for profile in context.get("visibleProfiles", []):
        meeting = "ja" if profile.get("meetingRequestsAllowed") else "nei"
        contact = "ja" if profile.get("sharedContactInfo") else "nei"
        lines.append(
            f"- {profile['name']}: {profile['description']} "
            f"Møteforespørsler: {meeting}. Delt kontaktinfo: {contact}."
        )

    policy = context.get("sponsorPolicy", {})
    allowed = ", ".join(policy.get("allowed", []))
    not_allowed = ", ".join(policy.get("notAllowed", []))
    lines.append(f"Sponsorpolicy tillater: {allowed}")
    lines.append(f"Sponsorpolicy tillater ikke: {not_allowed}")

    active_ref = context.get("activeReference")
    if active_ref:
        lines.append(
            f"Aktiv referanse: {active_ref.get('type')} {active_ref.get('name')} "
            f"({active_ref.get('reason')})"
        )
    else:
        lines.append("Aktiv referanse: ingen")

    actions = ", ".join(context.get("allowedActionKeypaths", []))
    lines.append(f"Tillatte actionKeypaths: {actions}")
    lines.append(f"Handlingsgrense: {context.get('actionBoundary', '')}")
    return "\n".join(lines)


def build_prompt(case: dict[str, Any], context: dict[str, Any]) -> str:
    schema = (
        "Returner kun ett gyldig JSON-objekt med feltene: "
        "intent, actionKeypath, needsClarification, safetyDecision, slots, "
        "answer, confidence. Bruk null for actionKeypath hvis ingen action "
        "skal foreslås."
    )
    label_instructions = "\n".join(
        [
            "Velg intent nøyaktig fra denne listen:",
            ", ".join(INTENT_LABELS),
            "Velg safetyDecision nøyaktig fra denne listen:",
            ", ".join(SAFETY_LABELS),
        ]
    )
    return "\n\n".join(
        [
            "/no_think",
            "Du er Co-pilot chat for HAVEN konferanseløsningen.",
            "Du skal forstå normal norsk dagligtale, korte meldinger, dialektpreg og små skrivefeil.",
            "Ikke finn opp personer, rom, e-post, telefonnummer, private notater eller skjulte data.",
            "Ikke si at noe er sendt, åpnet, slettet, flyttet eller publisert. Du kan bare foreslå eller lage utkast.",
            schema,
            label_instructions,
            "Kontekst:",
            context_to_text(context),
            f"Brukerprompt: {case['utterance']}",
        ]
    )


def run_llama_cli(
    llama_cli: str,
    model: Path,
    prompt: str,
    n_predict: int,
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    command = [
        llama_cli,
        "-m",
        str(model),
        "-p",
        prompt,
        "-n",
        str(n_predict),
        "--ctx-size",
        "4096",
        "--temp",
        "0.2",
        "--top-p",
        "0.9",
        "--presence-penalty",
        "1.2",
        "--reasoning",
        "off",
        "--device",
        "none",
        "--fit",
        "off",
        "-ngl",
        "0",
        "--no-display-prompt",
        "--single-turn",
        "--no-warmup",
        "--no-show-timings",
        "--log-disable",
        "--simple-io",
    ]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )


def extract_last_json_object(text: str) -> dict[str, Any] | None:
    starts = [index for index, char in enumerate(text) if char == "{"]
    candidates: list[tuple[int, int, dict[str, Any]]] = []
    for start in starts:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : index + 1]
                    try:
                        parsed = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    if isinstance(parsed, dict):
                        candidates.append((start, index + 1, parsed))
                    break

    required_keys = {"intent", "actionKeypath", "needsClarification", "safetyDecision"}
    schema_matches = [
        candidate
        for candidate in candidates
        if required_keys.intersection(candidate[2].keys())
    ]
    if schema_matches:
        return max(schema_matches, key=lambda item: (len(required_keys.intersection(item[2].keys())), item[1] - item[0], item[0]))[2]
    return None


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.lower()
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def score_case(case: dict[str, Any], parsed: dict[str, Any] | None) -> dict[str, Any]:
    expected = case["expected"]
    if parsed is None:
        return {
            "intent": 0,
            "action": 0,
            "clarification": 0,
            "safety": 0,
            "mustMention": 0,
            "mustNotMention": 0,
            "total": 0,
            "max": 6,
            "parseError": True,
        }

    visible_text = normalize(
        {
            "answer": parsed.get("answer"),
            "slots": parsed.get("slots"),
            "intent": parsed.get("intent"),
            "safetyDecision": parsed.get("safetyDecision"),
        }
    )

    must_mention = expected.get("mustMention", [])
    must_not_mention = expected.get("mustNotMention", [])

    scores = {
        "intent": int(parsed.get("intent") == expected.get("intent")),
        "action": int(parsed.get("actionKeypath") == expected.get("actionKeypath")),
        "clarification": int(
            bool(parsed.get("needsClarification"))
            == bool(expected.get("needsClarification"))
        ),
        "safety": int(parsed.get("safetyDecision") == expected.get("safetyDecision")),
        "mustMention": int(all(term.lower() in visible_text for term in must_mention)),
        "mustNotMention": int(
            all(term.lower() not in visible_text for term in must_not_mention)
        ),
    }
    scores["total"] = sum(scores.values())
    scores["max"] = 6
    scores["parseError"] = False
    return scores


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--llama-cli", default="llama-cli")
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path)
    parser.add_argument("--contexts", default=DEFAULT_CONTEXTS, type=Path)
    parser.add_argument("--out", default=DEFAULT_OUT, type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--case-id",
        action="append",
        default=[],
        help="Run only the given case id. May be provided multiple times.",
    )
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="Run only cases in the given category. May be provided multiple times.",
    )
    parser.add_argument("--n-predict", type=int, default=320)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args(argv)

    cases = load_jsonl(args.cases)
    if args.case_id:
        wanted = set(args.case_id)
        cases = [case for case in cases if case["id"] in wanted]
        missing = wanted.difference({case["id"] for case in cases})
        if missing:
            raise SystemExit(f"Unknown case id(s): {', '.join(sorted(missing))}")
    if args.category:
        wanted_categories = set(args.category)
        cases = [case for case in cases if case["category"] in wanted_categories]
    if args.limit is not None:
        cases = cases[: args.limit]
    contexts = load_contexts(args.contexts)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    maximum = 0
    parse_errors = 0
    completed = 0

    with args.out.open("w", encoding="utf-8") as out_handle:
        for case in cases:
            context = resolve_context(contexts, case["contextRef"])
            prompt = build_prompt(case, context)
            result = run_llama_cli(
                args.llama_cli,
                args.model,
                prompt,
                args.n_predict,
                args.timeout_seconds,
            )
            raw = result.stdout + result.stderr
            parsed = extract_last_json_object(raw)
            scores = score_case(case, parsed)
            total += scores["total"]
            maximum += scores["max"]
            parse_errors += int(scores["parseError"])
            completed += 1

            out_handle.write(
                json.dumps(
                    {
                        "id": case["id"],
                        "category": case["category"],
                        "utterance": case["utterance"],
                        "expected": case["expected"],
                        "parsed": parsed,
                        "scores": scores,
                        "returncode": result.returncode,
                        "rawOutput": raw,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            out_handle.flush()

            print(
                f"{case['id']}: {scores['total']}/{scores['max']} "
                f"parseError={scores['parseError']}"
            )

    percent = (total / maximum * 100) if maximum else 0.0
    print(
        f"Completed {completed} cases. Score {total}/{maximum} "
        f"({percent:.1f}%). Parse errors: {parse_errors}. Output: {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
