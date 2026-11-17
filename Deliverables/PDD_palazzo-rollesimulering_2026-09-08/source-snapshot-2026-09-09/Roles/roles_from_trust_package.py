#!/usr/bin/env python3
"""
roles_from_trust_package.py -- turn a trust package into role purposes.

The trust package (haven.agent-trust-package.v0) declares, per cell, which
keypaths an agent may touch and with which permission. That is a claim about
what will be enforced. Turning it into role purposes makes the role run an
AFTER-THE-FACT VERIFICATION of that claim, which is the half Kjetil described
when he proposed the package: see it before, verify it was honoured after.

The mapping needs no judgement, which is the point:

  a declared grant whose permission contains `r`  -> expect ACCESS ALLOWED
  the same keypath when the permission lacks `r`  -> expect ACCESS DENIED

So both directions come out of the package itself. A run that disagrees with the
generated file is a package that was not honoured, and the disagreement names
the cell, the keypath and the permission it was granted.

Paths in this file are relative to the repo that contains it (PalazzoScaffold).
Where that repo lives on a given machine is a device setting, not something this
file may assume.

usage:
  python3 Tests/Roles/roles_from_trust_package.py <package.json> [--reach r.json]
      [--principal 'guest:{agent_id}'] [--out Tests/Roles/roles/agent.json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Palazzo's generic cell read. A grant is about a keypath, and this is the route
# that asks for one, so it is the honest way to test a grant without inventing a
# surface for it.
CELL_GET = "/api/cell/get"


def purposes_from_package(pkg: dict, reach: list | None) -> list:
    out = []
    fleet = pkg.get("fleetID", "fleet")
    for cell in pkg.get("cells", []):
        cid = cell.get("id", "?")
        endpoint = cell.get("endpoint", "")
        declared = []
        for g in cell.get("templateGrants", []):
            declared.append((g.get("keypath", ""), g.get("permission", "----")))
        for c in cell.get("contracts", []):
            for g in c.get("grants", []):
                parts = g.split()
                if len(parts) == 2:
                    declared.append((parts[0], parts[1]))

        for keypath, perm in declared:
            readable = "r" in perm
            out.append({
                "purposeRef": f"purpose://candidate.palazzo-rollesimulering.agent."
                              f"{cid}.{keypath.replace('.', '-')}",
                "title": (f"Agenten {'når' if readable else 'når IKKE'} "
                          f"{cid}:{keypath} (pakken gir «{perm}»)"),
                "action": {"method": "POST", "path": CELL_GET,
                           "json": {"value": {"cell": endpoint, "keypath": keypath}}},
                "expect": ({"access": "allowed",
                            "state": {"path": "value", "op": "ne", "value": None}}
                           if readable else {"access": "denied"}),
                "stop_is": "riktig" if not readable else "feil",
                "why": (f"Tillitspakken {fleet} gir «{perm}» på {keypath}. "
                        + ("Stopper den, ble ikke pakken overholdt — eller pakken "
                           "lover noe systemet ikke gir."
                           if readable else
                           "Kommer den gjennom, ble pakken brutt.")),
                "from_package": {"fleetID": fleet, "cell": cid,
                                 "keypath": keypath, "permission": perm},
            })

    for r in reach or []:
        if r.get("permissions") == "----":
            out.append({
                "purposeRef": f"purpose://candidate.palazzo-rollesimulering.agent."
                              f"noreach.{'-'.join(r.get('path', ['?']))}",
                "title": f"Agenten når ingen vei via {' → '.join(r.get('path', []))}",
                "action": {"method": "POST", "path": CELL_GET,
                           "json": {"value": {"cell": r.get("path", ["?"])[-1],
                                              "keypath": "state"}}},
                "expect": {"access": "denied"},
                "stop_is": "riktig",
                "why": r.get("summary", "Ingen Grant i pakken."),
                "from_package": {"reach": r.get("path"), "permissions": "----"},
            })
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--reach")
    ap.add_argument("--principal", default="guest:{agent_id}")
    ap.add_argument("--out")
    args = ap.parse_args(argv)

    pkg = json.load(open(args.package))
    reach = json.load(open(args.reach)) if args.reach else None
    purposes = purposes_from_package(pkg, reach)

    role = {
        "role": "agent",
        "principal": args.principal,
        "generated_from": {
            "schema": pkg.get("schema"),
            "fleetID": pkg.get("fleetID"),
            "packageDigest": pkg.get("packageDigest"),
            "generatedAt": pkg.get("generatedAt"),
            "source": os.path.basename(args.package),
        },
        "note": ("Generert fra tillitspakken. Kjøringen er dermed etterprøvingen "
                 "av at pakken ble overholdt. Rediger ikke for hånd — regenerer "
                 "når pakken endres, så digesten i generated_from følger med."),
        "purposes": purposes,
    }
    text = json.dumps(role, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"{len(purposes)} formål skrevet til {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
