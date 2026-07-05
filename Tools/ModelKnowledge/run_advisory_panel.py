#!/usr/bin/env python3
"""Fan out one shared advisory brief to a panel of provider models.

Reads a panel spec JSON (shared brief + panelists with roles), sends the
brief to each panelist through an OpenAI-compatible chat-completions API,
and writes per-panelist and combined result JSON to the generated folder.

Secret-free: the API key comes from the environment only. Use synthetic or
public prompt material until SecretCredentialCell routing is in place.
"""

from __future__ import annotations

import argparse
import concurrent.futures
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


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> Any:
    headers = {"User-Agent": USER_AGENT, **headers}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


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


def run_panelist(
    panelist: dict[str, Any],
    spec: dict[str, Any],
    base_url: str,
    api_key: str,
    timeout: int,
) -> dict[str, Any]:
    system_prompt = (
        f"You are one member of an expert advisory panel. Your role: "
        f"{panelist['role']}. {panelist.get('roleInstructions', '')}"
    )
    payload = {
        "model": panelist["modelID"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": spec["sharedBrief"]},
        ],
        "temperature": spec.get("temperature", 0.2),
        "max_tokens": spec.get("maxTokens", 8000),
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    url = base_url.rstrip("/") + "/chat/completions"
    started = time.monotonic()
    result: dict[str, Any] = {
        "panelistName": panelist["name"],
        "modelID": panelist["modelID"],
        "role": panelist["role"],
        "promptHash": "sha256:" + sha256(spec["sharedBrief"]),
    }
    try:
        response = post_json(url, headers, payload, timeout)
        text = extract_text(response)
        result.update(
            {
                "status": "ok",
                "elapsedSeconds": round(time.monotonic() - started, 3),
                "responseText": text,
                "responseHash": "sha256:" + sha256(text),
                "rawUsage": response.get("usage") if isinstance(response, dict) else None,
                "rawModel": response.get("model") if isinstance(response, dict) else None,
            }
        )
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:1000]
        result.update(
            {
                "status": "http_error",
                "elapsedSeconds": round(time.monotonic() - started, 3),
                "error": f"HTTP {error.code}: {body}",
            }
        )
    except Exception as error:  # noqa: BLE001 - keep the panel running
        result.update(
            {
                "status": "error",
                "elapsedSeconds": round(time.monotonic() - started, 3),
                "error": f"{type(error).__name__}: {error}",
            }
        )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args(argv)

    provider = PROVIDERS[args.provider]
    api_key = os.environ.get(provider["api_key_env"], "")
    if not api_key:
        raise SystemExit(
            f"Missing {provider['api_key_env']}. Export it for this process; do not paste it into files."
        )

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    panelists = spec["panelists"]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(panelists)) as pool:
        futures = [
            pool.submit(run_panelist, p, spec, provider["base_url"], api_key, args.timeout)
            for p in panelists
        ]
        results = [f.result() for f in futures]

    combined = {
        "panelID": spec.get("panelID", args.spec.stem),
        "providerID": args.provider,
        "purposeRef": spec.get("purposeRef", "purpose://haven.advisory-panel"),
        "dataClass": spec.get("dataClass", "synthetic"),
        "timestamp": timestamp,
        "sharedBriefHash": "sha256:" + sha256(spec["sharedBrief"]),
        "sharedBrief": spec["sharedBrief"],
        "results": results,
    }
    out = args.out_dir / f"panel_{combined['panelID']}_{timestamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote panel results to {out}")
    for result in results:
        status = result["status"]
        elapsed = result.get("elapsedSeconds")
        length = len(result.get("responseText", "") or "")
        print(f"  {result['panelistName']} ({result['modelID']}): {status}, {elapsed}s, {length} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
