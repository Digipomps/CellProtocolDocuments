#!/usr/bin/env python3
"""Run Co-pilot chat language benchmark cases through Gemma 4 Transformers.

This adapter keeps the same benchmark contract as run_llama_cli_cases.py, but
uses Gemma's chat template instead of the GGUF/llama-cli prompt path.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoProcessor

from run_llama_cli_cases import (
    DEFAULT_CASES,
    DEFAULT_CONTEXTS,
    DEFAULT_OUT,
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
DEFAULT_GEMMA_OUT = ROOT / "results" / "gemma4_run.jsonl"


def build_messages(case: dict[str, Any], context: dict[str, Any]) -> list[dict[str, str]]:
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
    system = "\n".join(
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
            'Formatmal, ikke kopier verdiene: {"intent":"intent_label","actionKeypath":"action.path.or.null","needsClarification":false,"safetyDecision":"safety_label","slots":{},"answer":"Kort svar.","confidence":0.7}',
            schema,
            label_instructions,
        ]
    )
    user = "\n\n".join(
        [
            "Kontekst:",
            context_to_text(context),
            f"Brukerprompt: {case['utterance']}",
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def choose_device(name: str) -> torch.device:
    if name == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    if name == "mps" and not torch.backends.mps.is_available():
        raise SystemExit("Requested --device mps, but torch.backends.mps.is_available() is false")
    if name == "cuda" and not torch.cuda.is_available():
        raise SystemExit("Requested --device cuda, but torch.cuda.is_available() is false")
    return torch.device(name)


def resolve_dtype(name: str) -> str | torch.dtype:
    if name == "auto":
        return "auto"
    return {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }[name]


def first_parameter_device(model: torch.nn.Module) -> torch.device:
    try:
        return next(model.parameters()).device
    except StopIteration:
        return torch.device("cpu")


def move_inputs_to_device(inputs: dict[str, Any], device: torch.device) -> dict[str, Any]:
    moved: dict[str, Any] = {}
    for key, value in inputs.items():
        moved[key] = value.to(device) if hasattr(value, "to") else value
    return moved


def apply_chat_template(processor: Any, messages: list[dict[str, str]]) -> str:
    try:
        return processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )


def decode_response(processor: Any, generated_ids: torch.Tensor) -> tuple[str, str]:
    decoded = processor.decode(generated_ids, skip_special_tokens=False)
    parsed_text = decoded
    if hasattr(processor, "parse_response"):
        try:
            parsed = processor.parse_response(decoded)
            if isinstance(parsed, str):
                parsed_text = parsed
            elif isinstance(parsed, dict) and isinstance(parsed.get("content"), str):
                parsed_text = parsed["content"]
            else:
                parsed_text = json.dumps(parsed, ensure_ascii=False)
        except Exception as exc:  # noqa: BLE001 - keep raw output for eval diagnostics.
            parsed_text = f"{decoded}\n\n[processor.parse_response failed: {exc}]"
    return decoded, parsed_text


def generate_case(
    processor: Any,
    model: torch.nn.Module,
    device: torch.device,
    messages: list[dict[str, str]],
    max_new_tokens: int,
) -> dict[str, Any]:
    prompt = apply_chat_template(processor, messages)
    inputs = processor(text=prompt, return_tensors="pt")
    inputs = move_inputs_to_device(dict(inputs), device)
    input_len = inputs["input_ids"].shape[-1]

    start = time.monotonic()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    elapsed = time.monotonic() - start

    generated = output_ids[0][input_len:]
    decoded, response_text = decode_response(processor, generated)
    parsed = extract_last_json_object(response_text) or extract_last_json_object(decoded)
    return {
        "prompt": prompt,
        "decoded": decoded,
        "responseText": response_text,
        "parsed": parsed,
        "elapsedSeconds": round(elapsed, 3),
        "generatedTokens": int(generated.shape[-1]),
    }


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
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--cases", default=DEFAULT_CASES, type=Path)
    parser.add_argument("--contexts", default=DEFAULT_CONTEXTS, type=Path)
    parser.add_argument("--out", default=DEFAULT_GEMMA_OUT, type=Path)
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
    parser.add_argument("--max-new-tokens", type=int, default=320)
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "mps", "cuda"],
        default="auto",
        help="Default auto chooses cuda, then mps, then cpu.",
    )
    parser.add_argument(
        "--dtype",
        choices=["auto", "float32", "float16", "bfloat16"],
        default="auto",
    )
    parser.add_argument(
        "--threads",
        type=int,
        help="Set torch CPU thread count before loading the model.",
    )
    args = parser.parse_args(argv)

    if args.threads:
        torch.set_num_threads(args.threads)

    device = choose_device(args.device)
    dtype = resolve_dtype(args.dtype)
    cases = filter_cases(load_jsonl(args.cases), args)
    contexts = load_contexts(args.contexts)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"Loading {args.model_dir} with dtype={args.dtype} on device={device}...",
        flush=True,
    )
    processor = AutoProcessor.from_pretrained(args.model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir,
        dtype=dtype,
        local_files_only=True,
    )
    model.to(device)
    model.eval()
    model_device = first_parameter_device(model)
    print(f"Loaded. First parameter device={model_device}", flush=True)

    total = 0
    maximum = 0
    parse_errors = 0
    completed = 0

    with args.out.open("w", encoding="utf-8") as out_handle:
        for case in cases:
            context = resolve_context(contexts, case["contextRef"])
            messages = build_messages(case, context)
            result = generate_case(
                processor,
                model,
                device,
                messages,
                args.max_new_tokens,
            )
            parsed = result["parsed"]
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
                        "modelDir": str(args.model_dir),
                        "device": str(device),
                        "dtype": args.dtype,
                        "elapsedSeconds": result["elapsedSeconds"],
                        "generatedTokens": result["generatedTokens"],
                        "rawOutput": result["responseText"],
                        "rawDecoded": result["decoded"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            out_handle.flush()
            print(
                f"{case['id']}: {scores['total']}/{scores['max']} "
                f"parseError={scores['parseError']} "
                f"time={result['elapsedSeconds']}s tokens={result['generatedTokens']}",
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
