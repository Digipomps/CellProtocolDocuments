#!/usr/bin/env python3
"""Run Co-Pilot chat benchmark cases through OpenAI Responses API."""

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


def post_json(url: str, api_key: str, payload: dict[str, Any], timeout_seconds: int) -> Any:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:1200]
        return {"error": {"type": "http_error", "status": error.code, "body": body}}
    except urllib.error.URLError as error:
        return {"error": {"type": "url_error", "reason": str(error)}}


def extract_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    parts: list[str] = []
    output = payload.get("output")
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for content_item in content:
                    if not isinstance(content_item, dict):
                        continue
                    text = content_item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
    return "\n".join(parts)


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
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path)
    parser.add_argument("--contexts", default=DEFAULT_CONTEXTS, type=Path)
    parser.add_argument("--out", default=DEFAULT_OUT, type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--max-output-tokens", type=int, default=2000)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args(argv)

    api_key = os.environ.get(args.api_key_env, "")
    if not api_key:
        raise SystemExit(f"Missing {args.api_key_env}. Export it for this process; do not write it to files.")

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
            payload: dict[str, Any] = {
                "model": args.model,
                "max_output_tokens": args.max_output_tokens,
                "input": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Du er Co-pilot chat for HAVEN. Returner kun gyldig JSON "
                                    "som matcher skjemaet i brukerprompten."
                                ),
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": prompt}],
                    },
                ],
            }

            started = time.monotonic()
            response = post_json("https://api.openai.com/v1/responses", api_key, payload, args.timeout_seconds)
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
                        "providerID": "openai-responses",
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
