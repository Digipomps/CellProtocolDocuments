#!/usr/bin/env python3
"""Fetch model metadata from OpenAI-compatible providers.

No API key is written to output. Use environment variables only as a temporary
bridge until SecretCredentialCell-backed access exists.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
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
        "models_path": "/models",
        "api_key_env": "FEATHERLESS_API_KEY",
        "auth_header": "Authorization",
        "auth_value": "Bearer {api_key}",
    },
    "nanogpt": {
        "base_url": "https://nano-gpt.com/api/v1",
        "models_path": "/models",
        "api_key_env": "NANOGPT_API_KEY",
        "auth_header": "Authorization",
        "auth_value": "Bearer {api_key}",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "models_path": "/models",
        "api_key_env": "MISTRAL_API_KEY",
        "auth_header": "Authorization",
        "auth_value": "Bearer {api_key}",
    },
}


def request_json(url: str, headers: dict[str, str]) -> Any:
    headers = {"User-Agent": USER_AGENT, **headers}
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:800]
        raise SystemExit(f"HTTP {error.code} from {url}: {body}") from error


def normalize_models(provider_id: str, payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        items = payload["data"]
    elif isinstance(payload, dict) and isinstance(payload.get("models"), list):
        items = payload["models"]
    elif isinstance(payload, list):
        items = payload
    else:
        items = []
    normalized: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, str):
            model_id = item
            raw = {"id": item}
        elif isinstance(item, dict):
            model_id = str(item.get("id") or item.get("model") or item.get("name") or item.get("slug") or "")
            raw = item
        else:
            continue
        if not model_id:
            continue
        normalized.append(
            {
                "providerID": provider_id,
                "modelID": model_id,
                "object": raw.get("object") if isinstance(raw, dict) else None,
                "ownedBy": raw.get("owned_by") or raw.get("ownedBy") if isinstance(raw, dict) else None,
                "raw": raw,
            }
        )
    return normalized


def fetch(provider_id: str, out_dir: Path, no_auth: bool) -> Path:
    provider = PROVIDERS[provider_id]
    api_key = os.environ.get(provider["api_key_env"], "")
    if not api_key and not no_auth:
        raise SystemExit(f"Missing {provider['api_key_env']}. Do not paste it into docs; export it for this process.")
    headers = {"Accept": "application/json"}
    if api_key:
        headers[provider["auth_header"]] = provider["auth_value"].format(api_key=api_key)
    url = provider["base_url"].rstrip("/") + provider["models_path"]
    payload = request_json(url, headers)
    normalized = normalize_models(provider_id, payload)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{provider_id}_models_{timestamp}.json"
    out_path.write_text(
        json.dumps(
            {
                "providerID": provider_id,
                "fetchedAt": timestamp,
                "baseURL": provider["base_url"],
                "modelsPath": provider["models_path"],
                "modelCount": len(normalized),
                "models": normalized,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, type=Path)
    parser.add_argument("--no-auth", action="store_true", help="Try without API key for public model lists.")
    args = parser.parse_args(argv)

    out_path = fetch(args.provider, args.out_dir, args.no_auth)
    print(f"Wrote provider model metadata to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
