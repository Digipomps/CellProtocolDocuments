#!/usr/bin/env python3
"""Evaluate RAG-grounded Skeleton explanations across local model runtimes.

The evaluator is intentionally small and local-only. It uses the read-only
HAVEN Docs index as ground truth, sends the same prompt to each runnable model,
then stores raw outputs and a transparent heuristic score.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from haven_docs_mcp import DocsIndex  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = (
    ROOT
    / "Tools"
    / "HavenDocsMCP"
    / "results"
    / "skeleton_answer_model_eval_2026-07-01.json"
)


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    adapter: str
    model_path: Path
    runner_path: Path
    family: str
    note: str


MODEL_SPECS: dict[str, ModelSpec] = {
    "qwen3-1.7b-q8": ModelSpec(
        model_id="qwen3-1.7b-q8",
        adapter="llama-cli",
        model_path=ROOT / "Artifacts/local-models/gguf/Qwen3-1.7B-GGUF/Qwen3-1.7B-Q8_0.gguf",
        runner_path=Path("/opt/homebrew/bin/llama-cli"),
        family="Qwen3 GGUF",
        note="Small local text baseline.",
    ),
    "qwen3-4b-q4": ModelSpec(
        model_id="qwen3-4b-q4",
        adapter="llama-cli",
        model_path=ROOT / "Artifacts/local-models/gguf/Qwen3-4B-GGUF/Qwen3-4B-Q4_K_M.gguf",
        runner_path=Path("/opt/homebrew/bin/llama-cli"),
        family="Qwen3 GGUF",
        note="Middle local text model.",
    ),
    "qwen3-8b-q4": ModelSpec(
        model_id="qwen3-8b-q4",
        adapter="llama-cli",
        model_path=ROOT / "Artifacts/local-models/gguf/Qwen3-8B-GGUF/Qwen3-8B-Q4_K_M.gguf",
        runner_path=Path("/opt/homebrew/bin/llama-cli"),
        family="Qwen3 GGUF",
        note="Best previous local text-only Co-pilot baseline.",
    ),
    "gemma4-e2b-qat-mlx": ModelSpec(
        model_id="gemma4-e2b-qat-mlx",
        adapter="mlx-vlm",
        model_path=ROOT / "Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E2B-it-qat-4bit",
        runner_path=ROOT / "Artifacts/gemma4-runtime/venv-arm64/bin/python",
        family="Gemma 4 MLX/VLM",
        note="Local Apple Silicon multimodal-capable baseline.",
    ),
    "gemma4-e4b-qat-mlx": ModelSpec(
        model_id="gemma4-e4b-qat-mlx",
        adapter="mlx-vlm",
        model_path=ROOT / "Artifacts/gemma4-runtime/mlx/mlx-community-gemma-4-E4B-it-qat-4bit",
        runner_path=ROOT / "Artifacts/gemma4-runtime/venv-arm64/bin/python",
        family="Gemma 4 MLX/VLM",
        note="Best previous Gemma local Co-pilot baseline.",
    ),
}


GROUND_TRUTH_SECTIONS = [
    ("book-12-skeleton-spec", "chapter-12-skeleton-specification", 2600),
    ("book-12-skeleton-spec", "1-encoding-rule-all-elements", 1400),
    ("book-12-skeleton-spec", "4-keypath-rules", 1200),
    ("book-12-skeleton-spec", "5-encoding-caveats", 900),
    ("book-22-explore-contracts-skeleton-authoring", "skeleton-binding-rules", 2800),
    ("book-22-explore-contracts-skeleton-authoring", "skeleton-explore-validator", 1800),
    ("book-22-explore-contracts-skeleton-authoring", "authoring-workflow", 1200),
]


def build_ground_truth() -> list[dict[str, Any]]:
    index = DocsIndex()
    chunks: list[dict[str, Any]] = []
    for identifier, anchor, max_chars in GROUND_TRUTH_SECTIONS:
        section = index.read_section(identifier, anchor=anchor, max_chars=max_chars)
        citation = section["citation"]
        chunks.append(
            {
                "path": citation["path"],
                "heading": citation["heading"],
                "line_start": citation["line_start"],
                "line_end": citation["line_end"],
                "text": section["text"],
                "truncated": section["truncated"],
            }
        )
    return chunks


def citation_label(chunk: dict[str, Any]) -> str:
    return f"{chunk['path']}:{chunk['line_start']}-{chunk['line_end']}"


def build_prompts(chunks: list[dict[str, Any]]) -> tuple[str, str]:
    system_prompt = "\n".join(
        [
            "Du er en HAVEN dokumentasjonsassistent.",
            "Bruk bare GROUND TRUTH nedenfor som faktagrunnlag.",
            "Hvis noe ikke finnes i kildene, si at det mangler i grunnlaget.",
            "Svar paa norsk for en utvikler eller en annen spraakmodell.",
            "Ikke finn opp elementtyper, runtime-egenskaper eller sikkerhetsregler.",
            "Inkluder korte kildehenvisninger med Book/..:linjer.",
            "Hold svaret kompakt og komplett: 6 nummererte punkter, maks ca. 550 ord.",
        ]
    )

    ground_truth_text = "\n\n".join(
        [
            "\n".join(
                [
                    f"### {citation_label(chunk)}",
                    f"Heading: {chunk['heading']}",
                    chunk["text"],
                ]
            )
            for chunk in chunks
        ]
    )

    user_prompt = "\n\n".join(
        [
            "/no_think",
            "GROUND TRUTH:",
            ground_truth_text,
            "OPPGAVE:",
            (
                "Forklar hvordan CellProtocol Skeleton virker. Dekningen maa vaere "
                "god nok til at en agent kan slaa opp, forstaa og bruke dokumentasjonen "
                "uten aa gjette."
            ),
            "Maa dekke:",
            "- canonical model og single-key JSON encoding",
            "- CellConfiguration, discovery og cellReferences/default endpoint",
            "- keypath/url-bindinger, get/set og hva rendereren gjor",
            "- Explore-validering foer preview/commit",
            "- owner/entity access guardrail",
            "- viktige encoding caveats og dagens kjente grenser",
            "Bruk minst en kildehenvisning fra Book/12 og en fra Book/22.",
        ]
    )
    return system_prompt, user_prompt


def available(spec: ModelSpec) -> tuple[bool, str]:
    if not spec.runner_path.exists():
        return False, f"runner missing: {spec.runner_path}"
    if not spec.model_path.exists():
        return False, f"model missing: {spec.model_path}"
    return True, "available"


def run_llama_cli(
    spec: ModelSpec,
    system_prompt: str,
    user_prompt: str,
    n_predict: int,
    timeout_seconds: int,
    ctx_size: int,
    gpu_layers: int,
) -> tuple[subprocess.CompletedProcess[str], float, list[str]]:
    prompt = "\n\n".join([system_prompt, user_prompt])
    command = [
        str(spec.runner_path),
        "-m",
        str(spec.model_path),
        "-p",
        prompt,
        "-n",
        str(n_predict),
        "--ctx-size",
        str(ctx_size),
        "--temp",
        "0.0",
        "--top-p",
        "0.9",
        "--presence-penalty",
        "1.0",
        "--reasoning",
        "off",
        "-ngl",
        str(gpu_layers),
        "--no-display-prompt",
        "--single-turn",
        "--no-warmup",
        "--no-show-timings",
        "--log-disable",
        "--simple-io",
    ]
    start = time.monotonic()
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    return result, time.monotonic() - start, command


def run_mlx_vlm(
    spec: ModelSpec,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    timeout_seconds: int,
) -> tuple[subprocess.CompletedProcess[str], float, list[str]]:
    command = [
        str(spec.runner_path),
        "-m",
        "mlx_vlm.generate",
        "--model",
        str(spec.model_path),
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
    return result, time.monotonic() - start, command


def clean_answer(raw: str, prompt_text: str | None = None) -> str:
    text = raw.strip()
    if prompt_text and prompt_text in text:
        text = text.split(prompt_text, 1)[-1].strip()
    if "... (truncated)" in text:
        text = text.split("... (truncated)", 1)[-1].strip()
    if "\n\nExiting..." in text:
        text = text.split("\n\nExiting...", 1)[0].strip()
    if "\n/Users/" in text:
        text = text.split("\n/Users/", 1)[0].strip()
    text = re.sub(r"(?is)^.*?=========\s*Response\s*=========\s*", "", text)
    text = re.sub(r"(?is)^.*?assistant\s*[:：]\s*", "", text)
    text = re.sub(r"(?is)^.*?\n>\s*", "", text)
    text = re.sub(r"(?m)^> ?", "", text)
    text = re.sub(r"(?m)^load_backend:.*$", "", text)
    text = re.sub(r"(?m)^Loading model.*$", "", text)
    return text.strip()


def contains_any(text: str, needles: list[str]) -> bool:
    lower = text.lower()
    return any(needle.lower() in lower for needle in needles)


def score_answer(answer: str) -> dict[str, Any]:
    lower = answer.lower().replace("\\_", "_")
    categories: dict[str, int] = {}
    notes: list[str] = []

    categories["citations"] = (
        2
        if "book/12_skeleton_spec.md" in lower and "book/22_explore_contracts_for_skeleton_authoring.md" in lower
        else 1
        if "book/12_skeleton_spec.md" in lower or "book/22_explore_contracts_for_skeleton_authoring.md" in lower
        else 0
    )
    categories["encoding_model"] = int(
        contains_any(
            lower,
            [
                "single-key",
                "single key",
                "single-nokkel",
                "enkelt-nokkel",
                "enkelt-nøkkel",
                "enkeltnokkel",
                "enkeltnøkkel",
            ],
        )
        and "json" in lower
    ) * 2
    categories["configuration_endpoint"] = int(
        "cellconfiguration" in lower
        and ("cellreferences" in lower or "cell references" in lower)
        and contains_any(lower, ["cell:///porthole", "endpoint", "label"])
    ) * 2
    categories["binding_semantics"] = int(
        "keypath" in lower
        and "explore" in lower
        and (
            ("get" in lower and "set" in lower)
            or "read" in lower
            or "write" in lower
            or "les" in lower
            or "skriv" in lower
        )
    ) * 2
    categories["validation"] = int(
        "skeleton_explore_validator" in lower
        or ("preview" in lower and "commit" in lower and "valid" in lower)
    ) * 2
    categories["owner_access"] = int(
        contains_any(lower, ["owner", "eier", "entity"])
        and contains_any(lower, ["co-pilot", "copilot", "recovery", "tilbake"])
    ) * 2
    categories["caveats_limits"] = int(
        contains_any(lower, ["flowelementskeleton", "object", "legacy", "badge", "chip", "gauge", "progress", "limits", "grenser"])
        and contains_any(lower, ["renderer", "portable", "kanonisk", "canonical"])
    ) * 2
    categories["clarity_norwegian"] = (
        2
        if len(answer.split()) >= 140 and contains_any(lower, ["skeleton", "forklar", "betyr", "bruk"])
        else 1
        if len(answer.split()) >= 80
        else 0
    )

    hallucination_penalty = 0
    unsupported_patterns = [
        (r"\bmarkdown\b", "mentions Markdown as a Skeleton capability"),
        (r"\bwebview\b", "mentions WebView as a Skeleton capability"),
        (r"\bdatepicker\b", "mentions DatePicker as a Skeleton capability"),
        (r"\btrenger ikke\b.{0,80}\bexplore\b", "claims Explore is unnecessary"),
        (r"\bskriver\b.{0,80}\bdirekte\b.{0,80}\buten\b", "suggests direct writes without validation"),
    ]
    for pattern, note in unsupported_patterns:
        if re.search(pattern, lower):
            hallucination_penalty += 1
            notes.append(note)
    categories["hallucination_control"] = max(0, 2 - hallucination_penalty)

    total = sum(categories.values())
    maximum = len(categories) * 2
    missing = [name for name, score in categories.items() if score < 2]
    return {
        "categories": categories,
        "total": total,
        "max": maximum,
        "percent": round((total / maximum * 100) if maximum else 0, 1),
        "missing": missing,
        "notes": notes,
    }


def run_model(
    spec: ModelSpec,
    system_prompt: str,
    user_prompt: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    ok, availability_note = available(spec)
    if not ok:
        return {
            "model": spec.model_id,
            "family": spec.family,
            "adapter": spec.adapter,
            "status": "skipped",
            "availability": availability_note,
            "note": spec.note,
        }

    try:
        if spec.adapter == "llama-cli":
            result, elapsed, command = run_llama_cli(
                spec,
                system_prompt,
                user_prompt,
                args.n_predict,
                args.timeout_seconds,
                args.ctx_size,
                args.llama_gpu_layers,
            )
        elif spec.adapter == "mlx-vlm":
            result, elapsed, command = run_mlx_vlm(
                spec,
                system_prompt,
                user_prompt,
                args.max_tokens,
                args.timeout_seconds,
            )
        else:
            raise ValueError(f"Unknown adapter: {spec.adapter}")
    except subprocess.TimeoutExpired as exc:
        return {
            "model": spec.model_id,
            "family": spec.family,
            "adapter": spec.adapter,
            "status": "timeout",
            "elapsedSeconds": args.timeout_seconds,
            "error": str(exc),
            "note": spec.note,
        }

    raw = (result.stdout or "") + (result.stderr or "")
    prompt_text = "\n\n".join([system_prompt, user_prompt]) if spec.adapter == "llama-cli" else None
    answer = clean_answer(raw, prompt_text)
    score = score_answer(answer)
    return {
        "model": spec.model_id,
        "family": spec.family,
        "adapter": spec.adapter,
        "status": "completed" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "elapsedSeconds": round(elapsed, 3),
        "modelPath": str(spec.model_path.relative_to(ROOT)),
        "runnerPath": str(spec.runner_path),
        "command": [part if str(ROOT) not in part else part.replace(str(ROOT), "$ROOT") for part in command],
        "note": spec.note,
        "answer": answer,
        "rawOutput": raw,
        "score": score,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--models", nargs="*", default=list(MODEL_SPECS.keys()))
    parser.add_argument("--n-predict", type=int, default=650)
    parser.add_argument("--max-tokens", type=int, default=650)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--ctx-size", type=int, default=8192)
    parser.add_argument("--llama-gpu-layers", type=int, default=99)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    unknown = sorted(set(args.models).difference(MODEL_SPECS))
    if unknown:
        raise SystemExit(f"Unknown model id(s): {', '.join(unknown)}")

    ground_truth = build_ground_truth()
    system_prompt, user_prompt = build_prompts(ground_truth)
    selected = [MODEL_SPECS[model_id] for model_id in args.models]

    results: list[dict[str, Any]] = []
    payload = {
        "generatedAt": "2026-07-01",
        "purpose": "Evaluate RAG-grounded explanations of CellProtocol Skeleton.",
        "groundTruth": ground_truth,
        "systemPrompt": system_prompt,
        "userPrompt": user_prompt,
        "modelsRequested": args.models,
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)

    if not args.dry_run:
        for spec in selected:
            print(f"Running {spec.model_id} ({spec.adapter})...", flush=True)
            result = run_model(spec, system_prompt, user_prompt, args)
            results.append(result)
            args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            status = result.get("status")
            score = result.get("score", {})
            if score:
                print(
                    f"{spec.model_id}: {status} {score['total']}/{score['max']} "
                    f"({score['percent']}%) in {result.get('elapsedSeconds')}s",
                    flush=True,
                )
            else:
                print(f"{spec.model_id}: {status} - {result.get('availability') or result.get('error')}", flush=True)

    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
