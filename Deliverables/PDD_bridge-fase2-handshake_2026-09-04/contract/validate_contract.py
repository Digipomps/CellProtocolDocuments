#!/usr/bin/env python3
"""Referansevalidator for haven.bridge.session-handshake.contract.v1 (ren stdlib).

Kjorer alle fixtures og sjekker at utfallet matcher "expect"/"code".
Dette er kontraktens semantikk i kjørbar form; Swift-implementasjonen i fase 2
skal bestå de samme casene. Kryptografisk signatur/issuer valideres IKKE her —
det gjenbruker dagens Swift-kjede (SproutResolverCompatibility.swift:839).
"""
import json, sys, datetime, pathlib

SCHEMA = "haven.bridge.session-handshake.v1"
SESSION_REQUIRED = ["contract_id", "schema_version", "issued_by", "identity_public_key",
                    "client_kind", "porthole_protocol", "bridge_endpoint",
                    "issued_at", "expires_at", "scope"]
HOST_DEFAULT_CAP = 64

def published_cell_name(target):
    name = target.rsplit("/", 1)[-1].strip()
    if not name or "/" in name or name in (".", ".."):
        return None
    return name

def evaluate(fx, now=None):
    now = now or datetime.datetime(2026, 9, 4, tzinfo=datetime.timezone.utc)
    s = fx.get("session", {})
    if s.get("schema_version") != SCHEMA:
        return "schemaVersionUnknown"
    if "scope" not in s:
        return "sessionScopeMissing"
    for f in SESSION_REQUIRED:
        if f not in s:
            return "sessionRequiredFieldMissing:" + f
    exp = datetime.datetime.fromisoformat(s["expires_at"].replace("Z", "+00:00"))
    if exp <= now:
        return "sessionContractExpired"
    scope = s["scope"]
    channels = scope.get("channels")
    if not isinstance(channels, list):
        return "sessionScopeMissing"
    ch = fx.get("channelOpen", {})
    name = published_cell_name(ch.get("targetEndpoint", ""))
    if name is None or name not in channels:
        return "channelOutsideScope"
    cap = min(int(scope.get("channelCap", HOST_DEFAULT_CAP)), HOST_DEFAULT_CAP)
    if int(fx.get("activeChannels", 0)) + 1 > cap:
        return "channelCapExceeded"
    pol = fx.get("policy", {})
    if pol.get("requireActorCellProof") and "proof" not in ch.get("actorCell", {}):
        return "channelActorProofRequired"
    if pol.get("requireHostCellProof") and "hostProof" not in fx:
        return "hostProofRequired"
    return "accept"

def main():
    fixdir = pathlib.Path(__file__).parent / "fixtures"
    failures = 0
    for p in sorted(fixdir.glob("*.json")):
        fx = json.loads(p.read_text())
        got = evaluate(fx)
        want = "accept" if fx["expect"] == "accept" else fx["code"]
        ok = got == want
        print(("PASS" if ok else "FAIL"), p.name, "->", got)
        failures += 0 if ok else 1
    print("resultat:", "0 feil" if failures == 0 else f"{failures} FEIL")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
