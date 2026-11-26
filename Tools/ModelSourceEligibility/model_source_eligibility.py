#!/usr/bin/env python3
"""Reference evaluator for Book/model_source_eligibility_contract_v1.json.

Pure standard library. `python3 model_source_eligibility.py` checks every vector in
Book/fixtures/model-source-eligibility/vectors.v1.json and exits non-zero on a mismatch.
The Swift implementation (CellScaffold Sources/App/Support/ModelSourceEligibility.swift)
must give the same result for the same vectors.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "Book" / "model_source_eligibility_contract_v1.json"
VECTORS = ROOT / "Book" / "fixtures" / "model-source-eligibility" / "vectors.v1.json"

BOOL_FIELDS = ("requireAvailableWhenOwnerOffline", "requireMeasuredHealth", "requireFallbackForPersonalDevice")


def effective_requirements(contract, purpose_ref, profile=None):
    by_ref = {p["purposeRef"]: p for p in contract["purposes"]}
    ref = purpose_ref if purpose_ref in by_ref else contract["strictestPurposeRef"]
    req = json.loads(json.dumps(by_ref[ref]))
    rejected = []
    profile = profile or {}

    if "allowedServingClasses" in profile:
        wanted = profile["allowedServingClasses"]
        if any(c not in req["allowedServingClasses"] for c in wanted):
            rejected.append("allowedServingClasses")
        req["allowedServingClasses"] = [c for c in req["allowedServingClasses"] if c in wanted]
    for field in BOOL_FIELDS:
        if field in profile:
            if req[field] and not profile[field]:
                rejected.append(field)
            req[field] = req[field] or profile[field]
    if "maxHealthAgeSeconds" in profile and profile["maxHealthAgeSeconds"] is not None:
        wanted, base = profile["maxHealthAgeSeconds"], req["maxHealthAgeSeconds"]
        if base is not None and wanted > base:
            rejected.append("maxHealthAgeSeconds")
        else:
            req["maxHealthAgeSeconds"] = wanted
    if "maxP50MsBySurface" in profile:
        base = req["maxP50MsBySurface"]
        loosened = False
        for surface in sorted(profile["maxP50MsBySurface"]):
            wanted = profile["maxP50MsBySurface"][surface]
            current = base.get(surface, base.get("default"))
            if current is not None and wanted > current:
                loosened = True
            else:
                base[surface] = wanted
        if loosened:
            rejected.append("maxP50MsBySurface")
    if "allowedRegions" in profile:
        wanted, base = profile["allowedRegions"], req["allowedRegions"]
        if base:
            if any(r not in base for r in wanted):
                rejected.append("allowedRegions")
            req["allowedRegions"] = [r for r in base if r in wanted]
        else:
            req["allowedRegions"] = list(wanted)
    return ref, req, rejected


def evaluate(contract, purpose_ref, source, context, profile=None):
    ref, req, rejected = effective_requirements(contract, purpose_ref, profile)
    result = {"eligible": True, "unmet": [], "effectivePurposeRef": ref, "rejectedLoosenings": rejected}
    cls = source.get("servingClass", "unknown")
    if cls == "rules":
        return result

    unmet = []
    personal = cls == "personal_device"
    health = source.get("health") or {}
    status = health.get("status", "unknown")
    measured_at = health.get("measuredAtEpoch")
    p50 = health.get("p50Ms")

    if not (context.get("requesterHasAccess") or context.get("requesterIsOwner")):
        unmet.append("access_via_agreement")
    if cls not in req["allowedServingClasses"]:
        unmet.append("serving_class_allowed")
    if personal and not source.get("declaredAvailable"):
        unmet.append("declared_available")
    if personal and not (context.get("requesterIsOwner") or context.get("explicitChoice")):
        unmet.append("owner_or_explicit_choice")
    if personal and req["requireFallbackForPersonalDevice"] and not context.get("fallbackAvailable"):
        unmet.append("fallback_present")
    if req["requireAvailableWhenOwnerOffline"] and source.get("availableWhenOwnerOffline") != "yes":
        unmet.append("available_when_owner_offline")

    health_bad = False
    if req["requireMeasuredHealth"]:
        fresh = measured_at is not None and (
            req["maxHealthAgeSeconds"] is None or context["nowEpoch"] - measured_at <= req["maxHealthAgeSeconds"])
        health_bad = not (status == "ok" and fresh)
    if cls in ("personal_device", "operator_host") and status == "failed":
        health_bad = True
    if health_bad:
        unmet.append("health_measured_ok")

    limits = req["maxP50MsBySurface"]
    limit = limits.get(context.get("surface") or "default", limits.get("default"))
    if limit is not None and (p50 is None or p50 > limit):
        unmet.append("response_time_within_limit")
    if req["allowedRegions"] and source.get("region") not in req["allowedRegions"]:
        unmet.append("region_allowed")

    result["unmet"] = unmet
    result["eligible"] = not unmet
    return result


def main():
    contract = json.loads(CONTRACT.read_text())
    cases = json.loads(VECTORS.read_text())["cases"]
    failed = 0
    for case in cases:
        got = evaluate(contract, case["purposeRef"], case["source"], case["context"], case.get("profile"))
        if got != case["expect"]:
            failed += 1
            print(f"FEIL {case['name']}\n  forventet {case['expect']}\n  fikk      {got}")
    print(f"{len(cases) - failed}/{len(cases)} vektorer stemmer")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
