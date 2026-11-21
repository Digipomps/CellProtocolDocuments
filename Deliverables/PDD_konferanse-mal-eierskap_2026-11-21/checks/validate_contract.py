#!/usr/bin/env python3
"""Validator for Book/conference_entity_template_v0.json.

Kjører alle fixtures i ../contract/fixtures/. Hver fixture er en «verden»:
{
  "test": "test.kme.…",            # hvilken avledet test den dekker
  "world": {"organizers": [...], "events": [...], "participants": [...]},
  "expect": {"errors": [...], "derived": {...}}   # derived er valgfritt
}
Validatoren regner ut feilkoder og avledede verdier og sammenligner med expect.
Ren standardbibliotek. Exit 0 når alle fixtures stemmer.

Bruk: python3 checks/validate_contract.py [--contract STI] [--fixtures MAPPE]
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
REPO = TASK.parent.parent
UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def leaves(obj, prefix=""):
    """Flat liste av nøkkelstier til bladverdier. Tom liste/objekt telles som blad."""
    if isinstance(obj, dict) and obj:
        out = []
        for k, v in obj.items():
            out += leaves(v, f"{prefix}.{k}" if prefix else k)
        return out
    return [prefix] if prefix else []


def get_path(obj, path):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def covered_by(path, pattern):
    """Om nøkkelstien ligger under et malmønster. «*» står for ett segment."""
    p = path.split(".")
    q = pattern.split(".")
    if len(p) < len(q):
        return False
    return all(b == "*" or a == b for a, b in zip(p, q))


def has_cycle(start, parent_of):
    seen = set()
    cur = start
    while cur is not None:
        if cur in seen:
            return True
        seen.add(cur)
        cur = parent_of.get(cur)
    return False


def embedded_representation(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "EntityRepresentation":
            return True
        for k, v in obj.items():
            if k in ("entityRepresentation", "entityRepresentations"):
                return True
            if embedded_representation(v):
                return True
    elif isinstance(obj, list):
        return any(embedded_representation(v) for v in obj)
    return False


def check(contract, world):
    errors = []
    template = contract["template"]
    patterns = template["keypaths"]
    threshold = contract.get("proposalThreshold", 2)

    organizers = world.get("organizers", [])
    org_parent = {o.get("uuid"): o.get("partOf") for o in organizers}
    for o in organizers:
        if any(f not in o for f in ("uuid", "name", "members", "admins")):
            errors.append("organizer.missing-field")
            continue
        if any(a not in o["members"] for a in o["admins"]):
            errors.append("organizer.admin-not-member")
        if has_cycle(o["uuid"], org_parent):
            errors.append("organizer.partof-cycle")

    events = world.get("events", [])
    event_parent = {e.get("uuid"): get_path(e, "event.partOf") for e in events}
    owned = {}
    missing_fixed = {}
    extensions = {}
    reserved_used = {}
    for e in events:
        uid = e.get("uuid")
        owner = get_path(e, "event.ownedBy")
        if not owner:
            errors.append("event.missing-owner")
        else:
            owned.setdefault(owner, []).append(uid)
        ref, ver = get_path(e, "template.ref"), get_path(e, "template.version")
        if not ref or not ver:
            errors.append("event.missing-template")
        elif ref == template["uuid"] and ver != template["version"]:
            errors.append("event.unknown-template-version")
        if has_cycle(uid, event_parent):
            errors.append("event.partof-cycle")
        body = {k: v for k, v in e.items() if k != "uuid"}
        missing = [k["keypath"] for k in patterns
                   if k["status"] == "fixed" and "*" not in k["keypath"] and get_path(e, k["keypath"]) is None]
        if missing:
            missing_fixed[uid] = missing
        for path in leaves(body):
            match = next((k for k in patterns if covered_by(path, k["keypath"])), None)
            if match is None:
                extensions.setdefault(path, []).append(uid)
            elif match["status"] == "reserved":
                reserved_used.setdefault(uid, set()).add(match["keypath"])

    for p in world.get("participants", []):
        for key, slice_ in (p.get("conference") or {}).items():
            if not UUID.match(key):
                errors.append("participant.slice-key-not-uuid")
            if embedded_representation(slice_):
                errors.append("participant.embedded-entity-representation")

    proposals = [
        {"keypath": path, "usedBy": sorted(set(users)), "proposedFor": "next", "status": "proposed"}
        for path, users in sorted(extensions.items()) if len(set(users)) >= threshold
    ]
    derived = {
        "organizerEvents": {k: sorted(v) for k, v in sorted(owned.items())},
        "extensions": {k: sorted(set(v)) for k, v in sorted(extensions.items())},
        "proposals": proposals,
        "missingFixed": missing_fixed,
        "reservedUsed": {k: sorted(v) for k, v in reserved_used.items()},
    }
    return sorted(errors), derived


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", default=str(REPO / "Book" / "conference_entity_template_v0.json"))
    ap.add_argument("--fixtures", default=str(TASK / "contract" / "fixtures"))
    args = ap.parse_args()
    contract = json.loads(Path(args.contract).read_text())
    files = sorted(Path(args.fixtures).glob("*.json"))
    if not files:
        print("Ingen fixtures funnet", file=sys.stderr)
        return 2
    failed = 0
    for f in files:
        fx = json.loads(f.read_text())
        errors, derived = check(contract, fx["world"])
        exp = fx["expect"]
        problems = []
        if errors != sorted(exp.get("errors", [])):
            problems.append(f"feil {errors} ≠ forventet {sorted(exp.get('errors', []))}")
        for key, want in exp.get("derived", {}).items():
            if derived.get(key) != want:
                problems.append(f"{key} {json.dumps(derived.get(key), ensure_ascii=False)} ≠ forventet {json.dumps(want, ensure_ascii=False)}")
        status = "OK " if not problems else "FEIL"
        print(f"{status} {f.name} [{fx.get('test', '?')}]" + ("" if not problems else " — " + "; ".join(problems)))
        failed += bool(problems)
    print(f"{len(files) - failed}/{len(files)} fixtures stemmer")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
