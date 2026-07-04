#!/usr/bin/env python3
"""Run Co-pilot chat language benchmark cases through an OpenAI-compatible API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from run_llama_cli_cases import (
    DEFAULT_CASES,
    DEFAULT_CONTEXTS,
    DEFAULT_OUT,
    build_prompt,
    extract_last_json_object,
    load_contexts,
    load_jsonl,
    resolve_context,
    score_case,
)


PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
    },
    "featherless": {
        "base_url": "https://api.featherless.ai/v1",
        "api_key_env": "FEATHERLESS_API_KEY",
    },
    "nanogpt": {
        "base_url": "https://nano-gpt.com/api/v1",
        "api_key_env": "NANOGPT_API_KEY",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "api_key_env": "MISTRAL_API_KEY",
    },
}

USER_AGENT = "HAVEN-CoPilotChatBenchmark/0.1"


def post_json(url: str, api_key: str, payload: dict[str, Any], timeout_seconds: int) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:1200]
        return {
            "error": {
                "type": "http_error",
                "status": error.code,
                "body": body,
            }
        }


def extract_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]
    return ""


def filter_cases(
    cases: list[dict[str, Any]],
    case_ids: list[str],
    categories: list[str],
    limit: int | None,
) -> list[dict[str, Any]]:
    if case_ids:
        wanted = set(case_ids)
        cases = [case for case in cases if case["id"] in wanted]
        missing = wanted.difference({case["id"] for case in cases})
        if missing:
            raise SystemExit(f"Unknown case id(s): {', '.join(sorted(missing))}")
    if categories:
        wanted_categories = set(categories)
        cases = [case for case in cases if case["category"] in wanted_categories]
    if limit is not None:
        cases = cases[:limit]
    return cases


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url")
    parser.add_argument("--api-key-env")
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path)
    parser.add_argument("--contexts", default=DEFAULT_CONTEXTS, type=Path)
    parser.add_argument("--out", default=DEFAULT_OUT, type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=420)
    parser.add_argument(
        "--token-parameter",
        choices=["auto", "max_tokens", "max_completion_tokens"],
        default="auto",
        help="Chat Completions token field. OpenAI GPT-5/o-series routes use max_completion_tokens.",
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--omit-temperature", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--json-mode", action="store_true")
    args = parser.parse_args(argv)

    provider = PROVIDERS[args.provider]
    base_url = (args.base_url or provider["base_url"]).rstrip("/")
    api_key_env = args.api_key_env or provider["api_key_env"]
    api_key = os.environ.get(api_key_env, "")
    if not api_key:
        raise SystemExit(f"Missing {api_key_env}. Export it for this process; do not write it to files.")

    cases = filter_cases(load_jsonl(args.cases), args.case_id, args.category, args.limit)
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
            token_parameter = args.token_parameter
            if token_parameter == "auto":
                token_parameter = (
                    "max_completion_tokens"
                    if args.provider == "openai" and (args.model.startswith("gpt-5") or args.model.startswith("o"))
                    else "max_tokens"
                )
            payload: dict[str, Any] = {
                "model": args.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Du er Co-pilot chat for HAVEN. Returner kun gyldig JSON "
                            "som matcher skjemaet i brukerprompten."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                token_parameter: args.max_tokens,
                "stream": False,
            }
            if not args.omit_temperature:
                payload["temperature"] = args.temperature
            if args.json_mode:
                payload["response_format"] = {"type": "json_object"}

            started = time.monotonic()
            response = post_json(
                f"{base_url}/chat/completions",
                api_key,
                payload,
                args.timeout_seconds,
            )
            elapsed = round(time.monotonic() - started, 3)
            raw = extract_text(response)
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
                        "providerID": args.provider,
                        "modelID": args.model,
                        "elapsedSeconds": elapsed,
                        "parsed": parsed,
                        "scores": scores,
                        "rawModel": response.get("model") if isinstance(response, dict) else None,
                        "rawUsage": response.get("usage") if isinstance(response, dict) else None,
                        "rawOutput": raw,
                        "error": response.get("error") if isinstance(response, dict) else None,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            out_handle.flush()
            print(f"{case['id']}: {scores['total']}/{scores['max']} parseError={scores['parseError']}")

    percent = (total / maximum * 100) if maximum else 0.0
    print(
        f"Completed {completed} cases. Score {total}/{maximum} "
        f"({percent:.1f}%). Parse errors: {parse_errors}. Output: {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
