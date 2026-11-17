#!/usr/bin/python3
import collections, json, re, sys
from pathlib import Path

E = Path(sys.argv[1]); H = Path(sys.argv[2]); home = Path.home()
P = E.parent / "wp-r4-integration"

def layout(path):
    d = {}
    if path.exists():
        for l in path.read_text(errors="replace").splitlines():
            p = l.split("\t")
            if p[0] == "LAYOUT" and len(p) >= 3: d[p[1]] = int(p[2])
    return d
lm, lw = layout(E / "layout-main.log"), layout(E / "layout-wpr.log")

def frames(path):
    if not path.exists(): return {}
    flat = {}
    for mod, fs in json.loads(path.read_text()).items():
        for k, v in fs.items(): flat[k] = max(v, flat.get(k, 0))
    return flat
fm, fw = frames(E / "frames-main.json"), frames(E / "frames-wpr.json")

def chunks(dirpath):
    rows = []
    for f in sorted(dirpath.glob("bolk-*.log"), key=lambda p: int(p.stem.split("-")[-1])):
        log = f.read_text(errors="replace")
        clean = re.sub(r"error: Process [^\n]*exited with unexpected signal code \d+\n", "", log)
        ev = re.findall(r"Test Case '([^']+)' (started|passed|failed|skipped)", clean)
        st = collections.Counter(n for n, s in ev if s == "started")
        dn = collections.Counter(n for n, s in ev if s != "started")
        rows.append({"chunk": int(f.stem.split("-")[-1]),
                     "counts": dict(collections.Counter(s for _, s in ev)),
                     "aborted": list((st - dn).elements()),
                     "passed": [n for n, s in ev if s == "passed"],
                     "failed": [n for n, s in ev if s == "failed"],
                     "signals": re.findall(r"exited with unexpected signal code (\d+)", log)})
    return rows
base = chunks(E / "baseline" / "ci-chunks")
wpr = json.loads((P / "ci-summary.json").read_text())
wpr_aborted = [t for c in wpr["chunks"] for t in c["aborted_tests"]]

b_pass = {t for c in base for t in c["passed"]}
b_fail = {t for c in base for t in c["failed"]}
b_abort = {t for c in base for t in c["aborted"]}
tot = collections.Counter()
for c in base: tot.update(c["counts"])

before = set((E / "baseline" / "diagnostic-reports.before.txt").read_text().split()) if (E / "baseline" / "diagnostic-reports.before.txt").exists() else set()
reports = []
for f in sorted((home / "Library/Logs/DiagnosticReports").glob("xctest*.ips")):
    if f.name in before: continue
    try:
        raw = f.read_text(); d = json.loads(raw[raw.index("\n") + 1:])
    except Exception:
        continue
    imgs = [i.get("path", "") for i in d.get("usedImages", [])]
    if not any("/_worktrees/wp-r4b/scaffold-main/" in s for s in imgs): continue
    i = d.get("faultingThread"); fr = d["threads"][i]["frames"] if i is not None else []
    reports.append({"report": f.name, "message": (d.get("exception") or {}).get("message"),
                    "signal": (d.get("exception") or {}).get("signal"), "thread": i,
                    "stack": [x.get("symbol") for x in fr[:8]]})
(E / "baseline" / "crash-reports.json").write_text(json.dumps(reports, indent=1, ensure_ascii=False) + "\n")
stack_reports = [r for r in reports if r["message"] == "Thread stack size exceeded"]

rows = []
for t in wpr_aborted:
    s = "bestått" if t in b_pass else "feilet" if t in b_fail else "krasjet" if t in b_abort else "ikke kjørt"
    rows.append((t, s))
only_wpr = sum(1 for _, s in rows if s in ("bestått", "feilet"))
also_main = sum(1 for _, s in rows if s == "krasjet")
not_run = sum(1 for _, s in rows if s == "ikke kjørt")
exitcode = (E / "baseline" / "swift-ci.exit").read_text().strip() if (E / "baseline" / "swift-ci.exit").exists() else "?"
n = len(wpr_aborted)
mod_a, mod_b = lm.get("SkeletonModifiers"), lw.get("SkeletonModifiers")
hub = lambda F: max([v for k, v in F.items() if "chatHubSkeletonBody" in k] or [0])
if not base:
    status = f"STATUS: STOPPET — basiskjøringen på main ga ingen bolklogger (exit {exitcode}); se evidence/wp-r4b-stackdiagnose/baseline/swift-ci.log"
elif not_run == n:
    status = f"STATUS: STOPPET — ingen av de {n} krasjtestene ble kjørt på main (exit {exitcode})"
elif also_main == 0 and not stack_reports:
    status = f"STATUS: REGRESJON — {only_wpr} av {n} krasjer bare med WP-R; SkeletonModifiers {mod_a} → {mod_b} byte, chatHubSkeletonBody-ramme {hub(fm)} → {hub(fw)} byte"
elif only_wpr == 0:
    status = f"STATUS: MILJØ — {also_main} av {n} krasjer også på uendret main; WP-R er ikke årsaken"
else:
    status = f"STATUS: BLANDET — {only_wpr} av {n} krasjer bare med WP-R, {also_main} også på main, {not_run} ikke kjørt"

L = [status, "", "# WP-R4b — stackdiagnose (fullført av skript etter Codex-kvotestopp)", "",
     "Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-r4b-maal.sh`. Codex-jobben `wp-r4b-stackdiagnose-20260919` stoppet 07:34Z på brukskvoten etter å ha målt main-oppsettet; resten er målt av skriptet i de samme worktreene. Revisjoner: `evidence/wp-r4b-stackdiagnose/maal-heads.txt`.", "",
     "## 1. MemoryLayout (size, byte)", "", "| Type | CP 533b42d5 (main-pin) | CP c81a3979 (WP-R) |", "|---|---:|---:|"]
for t in sorted(set(lm) | set(lw)):
    if t.startswith("Skeleton") and (lm.get(t, 0) >= 100 or lw.get(t, 0) >= 100):
        L.append(f"| `{t}` | {lm.get(t, '—')} | {lw.get(t, '—')} |")
L += ["", "Rålogger: `evidence/wp-r4b-stackdiagnose/layout-main.log`, `layout-wpr.log`.", "",
      "## 2. Stackramme fra prologen (debug, arm64), byte", "", "| Funksjon | main e3ae9fc0 | WP-R f851df49 |", "|---|---:|---:|"]
keys = [k for k in set(fm) | set(fw) if any(s in k for s in ("chatHubSkeletonBody", "retintClaudeVisuals", "retintClaudeChild", "SkeletonElement.encode", "SkeletonElement.init(from"))]
top = sorted(set(fm) | set(fw), key=lambda k: -max(fm.get(k, 0), fw.get(k, 0)))[:15]
for k in sorted(set(keys) | set(top), key=lambda k: -max(fm.get(k, 0), fw.get(k, 0))):
    L.append(f"| `{k[:140]}` | {fm.get(k, '—')} | {fw.get(k, '—')} |")
L += ["", "Rådata: `frames-main.json`, `frames-wpr.json` (alle funksjoner ≥ 8 KiB i App og CellBase).", "",
      "## 3. CI-filteret på uendret main", "",
      f"Exit {exitcode}. Bolker med logg: {len(base)}. Teststatus: {dict(tot)}. Avbrutte tester totalt: {len(b_abort)}. Nye xctest-krasjrapporter fra main-bygget: {len(reports)}, av dem `Thread stack size exceeded`: {len(stack_reports)}.", "",
      f"Til sammenligning WP-R4: {wpr['totals']}, avbrutt {wpr['aborted']}.", "",
      "## 4. De 21 krasjtestene fra WP-R4 kjørt på main", "", "| Test | På main |", "|---|---|"]
L += [f"| `{t}` | {s} |" for t, s in rows]
other = sorted(b_abort - set(wpr_aborted))
if other:
    L += ["", "Andre tester som krasjet på main men ikke i WP-R4:", ""] + [f"- `{t}`" for t in other]
L += ["", "Rålogger: `evidence/wp-r4b-stackdiagnose/baseline/` (swift-ci.log, ci-chunks/bolk-*.log, crash-reports.json); kommandoer: `baseline-tools/ci-commands.jsonl`."]
H.write_text("\n".join(L) + "\n")
print(status)
