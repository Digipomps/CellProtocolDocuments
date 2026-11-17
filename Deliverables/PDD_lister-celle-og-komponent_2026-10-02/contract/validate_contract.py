#!/usr/bin/env python3
"""Strukturell validator for lists_cell_contract_v0.json + fixtures (ren stdlib).

Sjekker at hver fixture peker på en keypath i kontrakten, at request-formen er
en av formene kontraktens 'expects'-schema tillater, og at response-formen er
en gyldig MutationResult (status ok med stateVersion, eller error med code i
errorCodes). Kjør:  python3 validate_contract.py   (exit 0 = grønn)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
contract = json.load(open(os.path.join(HERE, "lists_cell_contract_v0.json")))
fixtures = json.load(open(os.path.join(HERE, "fixtures", "lists_cell_fixtures_v0.json")))
schemas = contract["schemas"]
sets = {e["keypath"]: e for e in contract["set"]}
gets = {e["keypath"]: e for e in contract["get"]}
errors = []


def matches(value, form):
    t = form.get("type")
    if t == "string":
        return isinstance(value, str) and (not form.get("nonEmpty") or value.strip() != "")
    if t == "bool":
        return isinstance(value, bool)
    if t == "object":
        if not isinstance(value, dict):
            return False
        if any(k not in value for k in form.get("required", [])):
            return False
        for k, allowed in form.get("values", {}).items():
            if value.get(k) not in allowed:
                return False
        for k, fixed in form.get("fixed", {}).items():
            if value.get(k) != fixed:
                return False
        return True
    return False


def matches_schema(value, name):
    schema = schemas[name]
    forms = schema.get("oneOf") or [schema]
    return any(matches(value, f) for f in forms)


for fx in fixtures["positive"]:
    kp = fx["keypath"]
    if kp not in sets:
        errors.append(f"{fx['name']}: ukjent set-keypath {kp}"); continue
    if not matches_schema(fx["request"], sets[kp]["expects"]):
        errors.append(f"{fx['name']}: request matcher ikke {sets[kp]['expects']}")
    if not (matches_schema(fx["response"], "MutationResult") and fx["response"].get("status") == "ok"):
        errors.append(f"{fx['name']}: response er ikke ok-MutationResult")

for fx in fixtures["negative"]:
    kp = fx["keypath"]
    if "expect" in fx:
        if fx["expect"] == "notFound":
            if kp in sets or kp in gets:
                errors.append(f"{fx['name']}: keypath finnes, men forventes notFound")
        elif fx["expect"] == "denied":
            if kp not in sets and kp not in gets:
                errors.append(f"{fx['name']}: denied-tilfelle må peke på en ekte keypath")
        else:
            errors.append(f"{fx['name']}: ukjent expect {fx['expect']}")
        continue
    if kp not in sets:
        errors.append(f"{fx['name']}: ukjent set-keypath {kp}"); continue
    resp = fx["response"]
    if not (matches_schema(resp, "MutationResult") and resp.get("status") == "error"):
        errors.append(f"{fx['name']}: response er ikke error-MutationResult")
    elif resp.get("code") not in contract["errorCodes"]:
        errors.append(f"{fx['name']}: feilkode {resp.get('code')} er ikke i errorCodes")

print(f"kontrakt v{contract['version']}: {len(sets)} set, {len(gets)} get, {len(fixtures['positive'])} positive, {len(fixtures['negative'])} negative fixtures")
for e in errors:
    print("FEIL:", e)
print("GRØNN" if not errors else f"RØD ({len(errors)})")
sys.exit(1 if errors else 0)
