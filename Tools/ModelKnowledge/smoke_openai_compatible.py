#!/usr/bin/env python3
"""Run a small synthetic chat-completions smoke test against a provider."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = ROOT / "Tools" / "ModelKnowledge" / "generated"
USER_AGENT = "HAVEN-ModelKnowledge/0.1"

PROVIDERS = {
    "featherless": {
        "base_url": "https://api.featherless.ai/v1",
        "api_key_env": "FEATHERLESS_API_KEY",
        "default_model": "Qwen/Qwen2.5-7B-Instruct",
    },
    "nanogpt": {
        "base_url": "https://nano-gpt.com/api/v1",
        "api_key_env": "NANOGPT_API_KEY",
        "default_model": "gpt-4.1-nano",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "api_key_env": "MISTRAL_API_KEY",
        "default_model": "mistral-small-latest",
    },
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> Any:
    headers = {"User-Agent": USER_AGENT, **headers}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:1000]
        raise SystemExit(f"HTTP {error.code} from {url}: {body}") from error


def extract_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str):
                    return content
            text = first.get("text")
            if isinstance(text, str):
                return text
    text = payload.get("response") or payload.get("text")
    return text if isinstance(text, str) else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--max-tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args(argv)

    provider = PROVIDERS[args.provider]
    api_key = os.environ.get(provider["api_key_env"], "")
    if not api_key:
        raise SystemExit(f"Missing {provider['api_key_env']}. Export it for this process; do not paste it into files.")
    model = args.model or provider["default_model"]
    prompt = (
        "Svar kort på norsk. Du er en modell-evalueringsrute for HAVEN. "
        "Forklar med én setning hva en trygg modelltest bør inneholde."
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du er en kort, presis norsk testassistent."},
            {"role": "user", "content": prompt},
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = provider["base_url"].rstrip("/") + "/chat/completions"
    started = time.monotonic()
    response = post_json(url, headers, payload)
    elapsed = time.monotonic() - started
    text = extract_text(response)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result = {
        "providerID": args.provider,
        "modelID": model,
        "purposeRef": "purpose://conference.co-pilot.model-evaluation",
        "dataClass": "synthetic",
        "timestamp": timestamp,
        "elapsedSeconds": round(elapsed, 3),
        "promptHash": "sha256:" + sha256(prompt),
        "responseHash": "sha256:" + sha256(text),
        "responsePreview": text[:500],
        "rawUsage": response.get("usage") if isinstance(response, dict) else None,
        "rawModel": response.get("model") if isinstance(response, dict) else None,
    }
    out = args.out or (DEFAULT_OUT_DIR / f"{args.provider}_smoke_{timestamp}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote smoke result to {out}")
    print(result["responsePreview"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
