#!/usr/bin/python3
import collections, json, re, sys
from pathlib import Path
E = Path(sys.argv[1]); web = sys.argv[2]; home = Path.home()
P = E.parent / "wp-r4-integration"; D = E.parent / "wp-r4b-stackdiagnose"
rows = []
for f in sorted((E / "cs-ci/ci-chunks").glob("bolk-*.log"), key=lambda p: int(p.stem.split("-")[-1])):
    log = f.read_text(errors="replace")
    clean = re.sub(r"error: Process [^\n]*exited with unexpected signal code \d+\n", "", log)
    ev = re.findall(r"Test Case '([^']+)' (started|passed|failed|skipped)", clean)
    st = collections.Counter(n for n, s in ev if s == "started"); dn = collections.Counter(n for n, s in ev if s != "started")
    rows.append({"chunk": int(f.stem.split("-")[-1]), "counts": dict(collections.Counter(s for _, s in ev)),
                 "aborted": list((st - dn).elements()), "failed": sorted({n for n, s in ev if s == "failed"}),
                 "signals": re.findall(r"exited with unexpected signal code (\d+)", log)})
tot = collections.Counter()
for r in rows: tot.update(r["counts"])
aborted = [t for r in rows for t in r["aborted"]]; failed = [t for r in rows for t in r["failed"]]
before = set((E / "cs-ci/diagnostic-reports.before.txt").read_text().split())
stack = 0
for f in sorted((home / "Library/Logs/DiagnosticReports").glob("xctest*.ips")):
    if f.name in before: continue
    try:
        raw = f.read_text(); d = json.loads(raw[raw.index("\n") + 1:])
    except Exception:
        continue
    if not any(web in i.get("path", "") for i in d.get("usedImages", [])): continue
    if (d.get("exception") or {}).get("message") == "Thread stack size exceeded": stack += 1
wpr = json.loads((P / "ci-summary.json").read_text())
wpr_aborted = [t for c in wpr["chunks"] for t in c["aborted_tests"]]
passed_now = {t for f in (E / "cs-ci/ci-chunks").glob("bolk-*.log") for t in re.findall(r"Test Case '([^']+)' passed", f.read_text(errors="replace"))}
def frames(p):
    if not p.exists(): return {}
    out = {}
    for fs in json.loads(p.read_text()).values():
        for k, v in fs.items(): out[k] = max(v, out.get(k, 0))
    return out
fb, fa, fm = frames(D / "frames-wpr.json"), frames(E / "frames-after.json"), frames(D / "frames-main.json")
res = {"chunks": len(rows), "failed_chunks": sum(1 for r in rows if r["failed"] or r["aborted"] or r["signals"]),
       "totals": dict(tot), "aborted": aborted, "failed": failed, "stack_reports": stack,
       "wpr_crashers_passing_now": sum(1 for t in wpr_aborted if t in passed_now), "wpr_crashers": len(wpr_aborted)}
(E / "cs-ci/summary.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
L = ["## CellScaffold CI-filter mot den boksa kandidaten", "",
     f"Bolker med logg: {len(rows)}; bolker med feil/avbrudd/signal: {res['failed_chunks']}. Teststatus: {dict(tot)}.",
     f"Avbrutte tester: {len(aborted)}. Nye krasjrapporter med `Thread stack size exceeded`: {stack}.",
     f"De {len(wpr_aborted)} testene som krasjet i WP-R4 og nå består: {res['wpr_crashers_passing_now']}.",
     f"WP-R4 til sammenligning: {wpr['totals']}, avbrutt {wpr['aborted']}.", ""]
if failed: L += ["Feilede tester:", ""] + [f"- `{t}`" for t in failed] + [""]
if aborted: L += ["Avbrutte tester:", ""] + [f"- `{t}`" for t in aborted] + [""]
L += ["## Stackramme fra prologen (debug, arm64), byte", "", "| Funksjon | main e3ae9fc0 | WP-R før boks | WP-R med boks |", "|---|---:|---:|---:|"]
keys = sorted(set(fb) | set(fa), key=lambda k: -max(fb.get(k, 0), fa.get(k, 0)))[:15]
keys += [k for k in set(fb) | set(fa) if "chatHubSkeletonBody" in k and k not in keys]
for k in keys: L.append(f"| `{k[:140]}` | {fm.get(k, '—')} | {fb.get(k, '<8K')} | {fa.get(k, '<8K')} |")
L += ["", "Rålogger: `evidence/wp-r4d-boks/cs-ci/` (swift-ci.log, ci-chunks/bolk-*.log, summary.json); kommandoer: `tools/ci-commands.jsonl`."]
print("\n".join(L))
