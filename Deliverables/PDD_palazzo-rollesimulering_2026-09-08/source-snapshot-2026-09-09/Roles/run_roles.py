#!/usr/bin/env python3
"""
run_roles.py -- let every role try to reach its purposes, and judge each stop.

Each role is a file in roles/. Each purpose in it names an action on the running
Palazzo server, the access it expects, and the observable state that would prove
it was reached. The actor performs them over HTTP with the role's principal
header and the gateway token -- production's own path, not a call into the App
module (lesson.tested-a-different-path-than-production).

Three rules decide what an outcome may be called, and all three exist because
leaving them out has cost this project something:

  CALIBRATION FIRST. Every role declares one purpose it can certainly reach and
  one it certainly cannot. Both are run before anything else. If the certain one
  is reported stopped, or the forbidden one reached, the harness is broken --
  not the system -- and the rest of the report is not read. An instrument that
  has not been shown to distinguish the two outcomes produces outcomes anyway.

  NOTHING UNEVALUATED IS EVER "REACHED". A purpose counts as reached only when
  its state assertion actually ran and was true. Empty body, missing field,
  timeout: UKLASSIFISERT, never a silent green. (In the nodegraph work a
  conformance check compared `err > tol`, which is False for NaN, so a result
  that was never evaluated counted as passing.)

  A STOP IS RIGHT OR WRONG, NEVER JUST RED. An expected denial is `riktig` with
  the reason from the role file. An unexpected one is UKLASSIFISERT and fails
  the run until a human writes which it is into the role file. The run never
  classifies a stop itself.

Exit codes, checked in order of severity rather than numeric order:
  2  calibration failed        the instrument is untrustworthy; read nothing else
  5  privacy leak              a purpose declared forbidden was answered
  3  null-principal leak       a principal with no grants reached something
  4  unclassified outcomes     a stop no human has judged yet
  0  clean
A single fault often trips more than one of these -- the calibration pair is the
earliest and strongest check, and will usually fire first. That is by design:
what you want reported is the most informative finding, not the first one.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))

REACHED = "OPPNÅDD"
STOPPED = "STOPPET"
UNCLASSIFIED = "UKLASSIFISERT"


# ----------------------------------------------------------------- transport
class Reply:
    def __init__(self, status: int, body: str, error: Optional[str] = None):
        self.status = status
        self.body = body
        self.error = error
        try:
            self.json = json.loads(body) if body else None
        except Exception:
            self.json = None

    @property
    def denied(self) -> bool:
        return self.status in (401, 403)

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300


def call(base: str, token: Optional[str], principal: str, action: Dict[str, Any],
         timeout: float = 10.0) -> Reply:
    url = base.rstrip("/") + action["path"]
    data = None
    headers = {"X-Palazzo-Principal": principal, "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if action.get("json") is not None:
        data = json.dumps(action["json"]).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method=action.get("method", "GET"))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return Reply(r.status, r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return Reply(e.code, e.read().decode("utf-8", "replace"))
    except Exception as e:  # connection refused, timeout, DNS
        return Reply(0, "", error=f"{type(e).__name__}: {e}")


# ------------------------------------------------------------ state language
class NotEvaluable(Exception):
    """The assertion could not be run. Never the same as 'it was false'."""


def resolve(doc: Any, path: str) -> Any:
    """Dotted path with [i] indexing and a trailing # for length."""
    if doc is None:
        raise NotEvaluable("no body")
    want_len = path.endswith("#")
    if want_len:
        path = path[:-1].rstrip(".")
    cur = doc
    if path:
        for part in path.split("."):
            key, _, idx = part.partition("[")
            if key:
                if not isinstance(cur, dict) or key not in cur:
                    raise NotEvaluable(f"missing field {key!r}")
                cur = cur[key]
            if idx:
                i = int(idx.rstrip("]"))
                if not isinstance(cur, list) or i >= len(cur):
                    raise NotEvaluable(f"missing index {i}")
                cur = cur[i]
    if want_len:
        if not isinstance(cur, (list, dict, str)):
            raise NotEvaluable("length of a non-collection")
        return len(cur)
    return cur


def assert_state(reply: Reply, spec: Dict[str, Any]) -> Tuple[bool, str]:
    op = spec.get("op", "eq")
    got = resolve(reply.json, spec.get("path", ""))
    want = spec.get("value")
    if op == "eq":
        return got == want, f"{spec.get('path','')} = {got!r}"
    if op == "ne":
        return got != want, f"{spec.get('path','')} = {got!r}"
    if op == "gte":
        return isinstance(got, (int, float)) and got >= want, f"{spec.get('path','')} = {got!r}"
    if op == "contains":
        return (want in got) if isinstance(got, (list, str, dict)) else False, \
               f"{spec.get('path','')} = {got!r}"
    if op == "each_eq":
        if not isinstance(got, list):
            raise NotEvaluable("each_eq on a non-list")
        return all(x == want for x in got), f"{spec.get('path','')} = {got!r}"
    raise NotEvaluable(f"unknown op {op!r}")


# --------------------------------------------------------------- evaluation
def judge(purpose: Dict[str, Any], reply: Reply) -> Dict[str, Any]:
    expect = purpose.get("expect", {})
    want_access = expect.get("access", "allowed")
    # A role file may pre-declare what a stop MEANS ("stop_is": "riktig"|"feil"),
    # which is a human classification recorded in advance. Not every legitimate
    # non-reach is a denial: the waiter's brief without consent answers 200 with
    # "ikke delt" for all five keypaths. That is the purpose not being reached,
    # correctly, and it must not flood the unclassified list.
    declared = purpose.get("stop_is")
    out: Dict[str, Any] = {
        "purposeRef": purpose.get("purposeRef"),
        "title": purpose.get("title"),
        "action": f"{purpose['action'].get('method','GET')} {purpose['action']['path']}",
        "http": reply.status if not reply.error else f"-- {reply.error}",
        "expected": want_access,
    }

    if reply.error:
        out.update(outcome=UNCLASSIFIED, classification=UNCLASSIFIED,
                   evidence=reply.error,
                   why="the request never completed; nothing was observed")
        return out

    observed = "denied" if reply.denied else ("allowed" if reply.ok else "error")
    out["observed"] = observed

    if want_access == "denied":
        if observed == "denied":
            out.update(outcome=STOPPED, classification="riktig",
                       evidence=f"HTTP {reply.status}",
                       why=purpose.get("why", "declared forbidden in the role file"))
        elif observed == "allowed":
            out.update(outcome=REACHED, classification="LEKKASJE",
                       evidence=f"HTTP {reply.status}",
                       why="a purpose declared forbidden was reached")
        else:
            out.update(outcome=UNCLASSIFIED, classification=UNCLASSIFIED,
                       evidence=f"HTTP {reply.status}",
                       why="neither allowed nor denied")
        return out

    # expected allowed
    if observed == "denied":
        out.update(outcome=STOPPED, classification=declared or UNCLASSIFIED,
                   evidence=f"HTTP {reply.status}",
                   why=purpose.get("why") if declared else
                       "stopped where the role file expected access; a human must "
                       "mark this riktig or feil in the role file")
        return out
    if observed == "error":
        out.update(outcome=UNCLASSIFIED, classification=UNCLASSIFIED,
                   evidence=f"HTTP {reply.status}", why="neither allowed nor denied")
        return out

    spec = expect.get("state")
    if not spec:
        out.update(outcome=UNCLASSIFIED, classification=UNCLASSIFIED,
                   evidence=f"HTTP {reply.status}",
                   why="no observable state declared, so nothing proves the purpose "
                       "was reached; add expect.state to the role file")
        return out
    try:
        passed, seen = assert_state(reply, spec)
    except NotEvaluable as e:
        out.update(outcome=UNCLASSIFIED, classification=UNCLASSIFIED,
                   evidence=f"HTTP {reply.status}; {e}",
                   why="the state assertion could not be evaluated, which is not "
                       "the same as reaching the purpose")
        return out
    if passed:
        out.update(outcome=REACHED, classification="—", evidence=seen, why="")
    else:
        out.update(outcome=STOPPED, classification=declared or UNCLASSIFIED,
                   evidence=seen,
                   why=purpose.get("why") if declared else
                       "access was granted but the expected state was not reached")
    return out


# ------------------------------------------------------------------ running
def load_roles(directory: str, only: Optional[List[str]]) -> List[Dict[str, Any]]:
    roles = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(directory, name)) as f:
            role = json.load(f)
        role["_file"] = name
        if only and role["role"] not in only:
            continue
        roles.append(role)
    return roles


def substitute(obj: Any, env: Dict[str, str]) -> Any:
    if isinstance(obj, str):
        for k, v in env.items():
            obj = obj.replace("{" + k + "}", v)
        return obj
    if isinstance(obj, dict):
        return {k: substitute(v, env) for k, v in obj.items()}
    if isinstance(obj, list):
        return [substitute(v, env) for v in obj]
    return obj


def run_role(role: Dict[str, Any], base: str, token: Optional[str],
             env: Dict[str, str], principal_override: Optional[str] = None
             ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    principal = principal_override or substitute(role["principal"], env)
    calib, normal = [], []
    for p in role["purposes"]:
        p = substitute(p, env)
        reply = call(base, token, principal, p["action"])
        row = judge(p, reply)
        row["role"] = role["role"]
        row["principal"] = principal
        row["calibration"] = p.get("calibration")
        (calib if p.get("calibration") else normal).append(row)
    return calib, normal


def calibration_verdict(rows: List[Dict[str, Any]]) -> List[str]:
    problems = []
    for r in rows:
        if r["calibration"] == "positive" and r["outcome"] != REACHED:
            problems.append(
                f"{r['role']}: positive reference {r['purposeRef']} came back "
                f"{r['outcome']} ({r['evidence']}) -- the harness cannot show a "
                f"purpose it is certain can be reached")
        if r["calibration"] == "null" and r["outcome"] == REACHED:
            problems.append(
                f"{r['role']}: null reference {r['purposeRef']} was REACHED "
                f"({r['evidence']}) -- the harness or the route is manufacturing "
                f"access")
    return problems


def report(calib: List[Dict[str, Any]], rows: List[Dict[str, Any]],
           problems: List[str], null_leaks: List[Dict[str, Any]],
           base: str, read: bool) -> str:
    out = ["# Rollesimulering — rapport", "",
           f"Kjørt {time.strftime('%Y-%m-%d %H:%M:%S')} mot `{base}`.", "",
           "## 0. Kalibrering", ""]
    out.append("Denne blokken står først med vilje. Er den rød, er tabellene "
               "under ikke lest — en aktør som ikke er vist å kunne skille de to "
               "utfallene, produserer utfall uansett.")
    out.append("")
    out.append("| rolle | referanse | formål | utfall | bevis |")
    out.append("|---|---|---|---|---|")
    for r in calib:
        out.append(f"| {r['role']} | {r['calibration']} | {r['title']} | "
                   f"{r['outcome']} | {r['evidence']} |")
    out.append("")
    if problems:
        out.append("**KALIBRERING FEILET.**")
        for p in problems:
            out.append(f"- {p}")
        out.append("")
        out.append("Kjøringen er en instrumenteringsrunde. Den gater ingenting, "
                   "og resten av rapporten er ikke lest.")
    else:
        out.append("Kalibrering OK: hver rolle viste både et oppnådd og et stoppet "
                   "utfall der svaret var kjent på forhånd.")
    out.append("")

    if null_leaks:
        out.append("## 0b. Nullkjøring — LEKKASJE")
        out.append("")
        out.append("En principal uten grants oppnådde noe. Suksessen lages av "
                   "harnessen eller ruten, ikke av systemet.")
        out.append("")
        for r in null_leaks:
            out.append(f"- {r['role']} / {r['purposeRef']}: {r['evidence']}")
        out.append("")

    if not read:
        out.append("---")
        out.append("")
        out.append("*Rolletabellene er utelatt: kalibreringen må være grønn før de "
                   "betyr noe.*")
        return "\n".join(out) + "\n"

    for role in sorted({r["role"] for r in rows}):
        out.append(f"## {role}")
        out.append("")
        out.append("| formål | handling | forventet | utfall | klassifisering | hvorfor / bevis |")
        out.append("|---|---|---|---|---|---|")
        for r in rows:
            if r["role"] != role:
                continue
            out.append(f"| {r['title']} | `{r['action']}` | {r['expected']} | "
                       f"{r['outcome']} | {r['classification']} | "
                       f"{r['why'] or r['evidence']} |")
        out.append("")

    wrong = [r for r in rows if r["classification"] == "feil"]
    unclassified = [r for r in rows if r["classification"] == UNCLASSIFIED]
    leaks = [r for r in rows if r["classification"] == "LEKKASJE"]
    out.append("## Feil stopp")
    out.append("")
    if wrong:
        for r in wrong:
            out.append(f"- {r['role']} / {r['purposeRef']} — {r['why']}")
    else:
        out.append("Ingen stopp er merket `feil` i rollefilene ennå.")
    out.append("")
    if unclassified:
        out.append("## Uklassifiserte — må avgjøres av et menneske")
        out.append("")
        for r in unclassified:
            out.append(f"- {r['role']} / {r['purposeRef']}: {r['why']} "
                       f"({r['evidence']})")
        out.append("")
        out.append("Skriv `riktig` eller `feil` i rollefilen. Kjøringen "
                   "klassifiserer aldri et stopp selv.")
        out.append("")
    if leaks:
        out.append("## PERSONVERNLEKKASJE")
        out.append("")
        for r in leaks:
            out.append(f"- {r['role']} / {r['purposeRef']}: {r['why']} ({r['evidence']})")
        out.append("")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--token", default=os.environ.get("PALAZZO_GATEWAY_TOKEN"))
    ap.add_argument("--roles", default=os.path.join(HERE, "roles"))
    ap.add_argument("--only", nargs="*", help="run only these role names")
    ap.add_argument("--env", nargs="*", default=[],
                    help="key=value substitutions used in role files")
    ap.add_argument("--out", default=None, help="write the report here")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--null-principal", default=None,
                    help="rerun every purpose as this principal; anything reached "
                         "that is not marked null_principal_may_reach is a leak "
                         "(use a fresh guest id with no grants)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    env = dict(kv.split("=", 1) for kv in args.env)
    roles = load_roles(args.roles, args.only)
    if not roles:
        print("no role files found", file=sys.stderr)
        return 1

    calib: List[Dict[str, Any]] = []
    rows: List[Dict[str, Any]] = []
    for role in roles:
        c, n = run_role(role, args.base_url, args.token, env)
        calib.extend(c)
        rows.extend(n)

    problems = calibration_verdict(calib)

    # The null-principal run: a valid principal with no grants and no
    # relationship to anyone's data. Every purpose it can still reach was
    # reached by the plumbing, not by the world -- EXCEPT the ones that address
    # the principal's own state or a genuinely public surface, which any
    # principal may legitimately reach. Those are marked
    # `null_principal_may_reach` in the role file and are listed as exempt in
    # the report, so the exemption is reviewable rather than silent. Without
    # that distinction the check would flag "a fresh guest read its own empty
    # entity", which is correct behaviour, and would have been discarded as
    # noise on first use.
    null_leaks: List[Dict[str, Any]] = []
    null_exempt: List[str] = []
    if args.null_principal:
        for role in roles:
            exempt = {p["purposeRef"] for p in role["purposes"]
                      if p.get("null_principal_may_reach")}
            null_exempt.extend(sorted(exempt))
            c, n = run_role(role, args.base_url, args.token, env,
                            principal_override=args.null_principal)
            for r in c + n:
                if r["outcome"] == REACHED and r["purposeRef"] not in exempt:
                    null_leaks.append(r)

    text = report(calib, rows, problems, null_leaks, args.base_url, read=not problems)
    if args.null_principal:
        text += ("\n*Nullkjøringen unntok " + str(len(null_exempt)) +
                 " formål som enhver principal lovlig kan nå (egen tilstand "
                 "eller offentlig flate): " + ", ".join(null_exempt) + "*\n")
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
    if not args.quiet:
        print(text)
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump({"calibration": calib, "rows": rows, "problems": problems,
                       "null_leaks": null_leaks, "null_exempt": null_exempt},
                      f, indent=2, ensure_ascii=False)

    if problems:
        return 2
    if any(r["classification"] == "LEKKASJE" for r in rows):
        return 5
    if null_leaks:
        return 3
    if any(r["classification"] == UNCLASSIFIED for r in rows):
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
