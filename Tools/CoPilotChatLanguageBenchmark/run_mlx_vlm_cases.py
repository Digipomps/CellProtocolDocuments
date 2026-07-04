#!/usr/bin/env python3
"""Run Co-pilot chat language benchmark cases through mlx-vlm.

Use this for Apple Silicon MLX/VLM models such as Gemma 4 QAT 4-bit. The
script shells out to `python -m mlx_vlm.generate` because MLX/Metal may only be
available from an unsandboxed local process.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from run_llama_cli_cases import (
    DEFAULT_CASES,
    DEFAULT_CONTEXTS,
    INTENT_LABELS,
    SAFETY_LABELS,
    context_to_text,
    extract_last_json_object,
    load_contexts,
    load_jsonl,
    resolve_context,
    score_case,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT / "results" / "mlx_vlm_run.jsonl"


def build_system_prompt() -> str:
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
    return "\n".join(
        [
            "Du er Co-pilot chat for HAVEN konferanseløsningen.",
            "Du skal forstå normal norsk dagligtale, korte meldinger, dialektpreg og små skrivefeil.",
            "Ikke finn opp personer, rom, e-post, telefonnummer, private notater eller skjulte data.",
            "Ikke si at noe er sendt, åpnet, slettet, flyttet eller publisert. Du kan bare foreslå eller lage utkast.",
            "Ikke bruk Markdown, kodegjerder eller forklarende tekst rundt JSON.",
            "needsClarification skal være boolsk true eller false, ikke tekst.",
            "Alle stringverdier i JSON må stå i doble anførselstegn.",
            "Velg actionKeypath fra tillatte actionKeypaths når handlingen er trygg og relevant; ellers null.",
            "For agenda-anbefalinger skal answer nevne relevant klokkeslett og tema.",
            "answer skal være kort, maks 25 ord.",
            schema,
            label_instructions,
        ]
    )


def build_user_prompt(case: dict[str, Any], context: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "Kontekst:",
            context_to_text(context),
            f"Brukerprompt: {case['utterance']}",
        ]
    )


def run_mlx_vlm(
    python: str,
    model: Path,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    timeout_seconds: int,
) -> tuple[subprocess.CompletedProcess[str], float]:
    command = [
        python,
        "-m",
        "mlx_vlm.generate",
        "--model",
        str(model),
        "--system",
        system_prompt,
        "--prompt",
        user_prompt,
        "--max-tokens",
        str(max_tokens),
        "--temperature",
        "0.0",
        "--no-verbose",
    ]
    start = time.monotonic()
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    return result, time.monotonic() - start


def filter_cases(cases: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
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
    return cases


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path)
    parser.add_argument("--contexts", default=DEFAULT_CONTEXTS, type=Path)
    parser.add_argument("--out", default=DEFAULT_OUT, type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=180)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args(argv)

    cases = filter_cases(load_jsonl(args.cases), args)
    contexts = load_contexts(args.contexts)
    system_prompt = build_system_prompt()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    maximum = 0
    parse_errors = 0
    completed = 0

    with args.out.open("w", encoding="utf-8") as out_handle:
        for case in cases:
            context = resolve_context(contexts, case["contextRef"])
            user_prompt = build_user_prompt(case, context)
            result, elapsed = run_mlx_vlm(
                args.python,
                args.model,
                system_prompt,
                user_prompt,
                args.max_tokens,
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
                        "model": str(args.model),
                        "elapsedSeconds": round(elapsed, 3),
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
                f"parseError={scores['parseError']} time={elapsed:.3f}s",
                flush=True,
            )

    percent = (total / maximum * 100) if maximum else 0.0
    print(
        f"Completed {completed} cases. Score {total}/{maximum} "
        f"({percent:.1f}%). Parse errors: {parse_errors}. Output: {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
