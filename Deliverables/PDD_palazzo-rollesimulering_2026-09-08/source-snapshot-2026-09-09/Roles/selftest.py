#!/usr/bin/env python3
"""
selftest.py -- prove the actor notices, before it is pointed at Palazzo.

Five runs against fixture_server.py, each a specific way a harness can be wrong.
The actor must return the right exit code every time. A green run here does not
say anything about Palazzo; it says the instrument reacts. That is the half that
can be established without a running scaffold, and the half that is worthless to
discover late.

  normal            -> 0  (everything behaves and every stop is declared)
  broken-positive   -> 2  (a certain purpose came back stopped)
  leaky-null        -> 2  (a forbidden purpose came back reached)
  ignores-principal -> 2  (calibration catches it BEFORE the null run does)
  null-leak         -> 3  (calibration green; only the null run sees it)
  unexpected-stop   -> 4  (an undeclared stop is handed to a human, not guessed)
  privacy-leak      -> 5  (a forbidden purpose was answered)
  unevaluable       -> 2  (a 200 whose assertion cannot run is not "reached")

Run: python3 selftest.py
"""
from __future__ import annotations

import multiprocessing as mp
import os
import tempfile
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fixture_server  # noqa: E402
import run_roles  # noqa: E402

ENV = [
    "guest_id=g1", "other_guest_id=g2", "staff_id=s1", "agent_id=a1",
    "guest_cell=plain-guest-cell",
    "consenting_guest_cell=consenting-guest-cell",
    "article_id=a1", "agreement_id=ag1",
]

CASES = [
    ("normal", 0, "alt oppfører seg, og hvert stopp er forhåndsklassifisert"),
    ("broken-positive", 2, "positiv referanse stoppet -> harnessen, ikke systemet"),
    ("leaky-null", 2, "nullreferanse nådd -> tilgang lages et sted"),
    ("ignores-principal", 2, "kalibreringen fanger den FØR nullkjøringen rekker det"),
    ("null-leak", 3, "kalibreringen er grønn; bare nullkjøringen ser denne"),
    ("unexpected-stop", 4, "et uventet stopp gjettes ikke — det gis til et menneske"),
    ("privacy-leak", 5, "et forbudt formål ble besvart — alvorligere enn nullekkasjen samme feil også gir"),
    ("unevaluable", 2, "200 uten lesbar tilstand er ikke OPPNÅDD"),
]


def wait_for(port: int, timeout: float = 5.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/scaffold/info",
                                   timeout=0.5)
            return True
        except Exception:
            time.sleep(0.05)
    return False


MINIMUM = {"gjest": 8, "annen-gjest": 4, "personale": 4, "hus": 6, "agent": 4}


def check_schema() -> list:
    """test.roles.schema — every purpose is complete, and every role carries
    both calibration references. A role that declares neither cannot be
    calibrated, and a run of it means nothing."""
    import json as _json
    bad = []
    seen = {}
    for name in sorted(os.listdir(os.path.join(HERE, "roles"))):
        if not name.endswith(".json"):
            continue
        d = _json.load(open(os.path.join(HERE, "roles", name)))
        role = d.get("role")
        seen[role] = len(d.get("purposes", []))
        kinds = {p.get("calibration") for p in d["purposes"] if p.get("calibration")}
        if kinds != {"positive", "null"}:
            bad.append(f"{role}: mangler kalibreringspar, har {sorted(kinds)}")
        for p in d["purposes"]:
            for field in ("purposeRef", "title", "action", "expect"):
                if field not in p:
                    bad.append(f"{role}/{p.get('purposeRef', '?')}: mangler {field}")
            if p.get("stop_is") and not p.get("why"):
                bad.append(f"{role}/{p['purposeRef']}: stop_is uten why")
            if p.get("expect", {}).get("access", "allowed") == "allowed" \
                    and "state" not in p.get("expect", {}):
                bad.append(f"{role}/{p['purposeRef']}: forventer tilgang uten "
                           f"observerbar tilstand — ingenting ville bevist at "
                           f"formålet ble nådd")
    for role, minimum in MINIMUM.items():
        if seen.get(role, 0) < minimum:
            bad.append(f"{role}: {seen.get(role, 0)} formål, minst {minimum} kreves")
    return bad


def main() -> int:
    schema_problems = check_schema()
    print("  " + ("ok  " if not schema_problems else "FAIL") +
          " test.roles.schema     " +
          (f"{len(MINIMUM)} roller, kalibreringspar og observerbar tilstand overalt"
           if not schema_problems else "; ".join(schema_problems[:3])))
    failures = list(("test.roles.schema", "-", p) for p in schema_problems[:1])
    port = 8099
    for mode, want, why in CASES:
        port += 1
        proc = mp.Process(target=fixture_server.serve, args=(port, mode), daemon=True)
        proc.start()
        if not wait_for(port):
            failures.append((mode, "fixture did not start", None))
            proc.terminate()
            continue
        argv = ["--base-url", f"http://127.0.0.1:{port}", "--env", *ENV,
                "--quiet", "--null-principal", "guest:nobody",
                "--json-out", os.path.join(tempfile.gettempdir(), f"selftest_{mode}.json")]
        got = run_roles.main(argv)
        proc.terminate()
        proc.join(timeout=2)
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {mode:18s} exit={got} (ventet {want}) — {why}")
        if not ok:
            failures.append((mode, want, got))

    print()
    if failures:
        print(f"{len(CASES)-len(failures)}/{len(CASES)} — aktøren reagerer ikke som den skal:")
        for m, w, g in failures:
            print(f"  {m}: ventet {w}, fikk {g}")
        return 1
    print(f"{len(CASES)}/{len(CASES)} — aktøren reagerer på hver feilform den er vist.")
    print("Dette sier ingenting om Palazzo. Det sier at instrumentet virker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
