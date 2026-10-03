"""Compare complete WP13 XCTest logs with WP0c's recorded red test names.

Run from any cwd: python3 /path/to/evidence/wp13/compare_regression.py
Exit 0 means no new red names, not that either XCTest bundle is green.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "TESTRESULT.md"
baseline = REPORT.read_text().split("## WP0 — sluttmelding", 1)[0]
result = {}
for repo, module, expected_baseline, baseline_total in [
    ("CellProtocol", "CellBaseTests", 6, 1060),
    ("CellScaffold", "AppTests", 46, 2046),
]:
    stem = repo.lower()
    log_path = HERE / (stem + "-regression.log")
    # Concurrent stdout/stderr can interleave UTF-8 bytes. Keep the raw log
    # unchanged; replacement is only for parsing ASCII XCTest result lines.
    log = log_path.read_text(errors="replace")
    assert re.search(r"^Test Suite 'All tests' (?:passed|failed) at ", log, re.M), f"{repo}: incomplete log"
    baseline_red = sorted(set(re.findall(r"Test Case '-\[(" + module + r"\.[^]]+)\]' failed", baseline)))
    assert len(baseline_red) == expected_baseline, f"{repo}: unexpected baseline source"
    completed = re.findall(r"Test Case '-\[([^]]+)\]' (passed|failed|skipped) \(", log)
    started = re.findall(r"Test Case '-\[([^]]+)\]' started\.", log)
    counts = Counter(status for _, status in completed)
    red = sorted(name for name, status in completed if status == "failed")
    summaries = re.findall(r"^\s*Executed (\d+) tests?, with (?:(\d+) tests? skipped and )?(\d+) failures? \((\d+) unexpected\) in .* seconds$", log, re.M)
    assert summaries, f"{repo}: missing XCTest summary"
    total, skipped, failures, unexpected = (int(x or 0) for x in summaries[-1])
    assert len(started) == len(set(started)) == total, f"{repo}: total/unique start mismatch"
    assert len(completed) == len(set(name for name, _ in completed)) == total, f"{repo}: incomplete/duplicate cases"
    assert counts["skipped"] == skipped
    new_red = sorted(set(red) - set(baseline_red))
    resolved_red = sorted(set(baseline_red) - set(red))
    absent_baseline_red = sorted(set(baseline_red) - set(started))
    assert not absent_baseline_red, f"{repo}: baseline tests disappeared"
    for suffix, names in [("baseline-red", baseline_red), ("red", red), ("new-red", new_red), ("resolved-red", resolved_red)]:
        (HERE / f"{stem}-{suffix}.txt").write_text("\n".join(names) + ("\n" if names else ""))
    result[repo] = {
        "baselineTotal": baseline_total,
        "total": total,
        "passed": counts["passed"],
        "skipped": skipped,
        "failureReports": failures,
        "unexpectedFailureReports": unexpected,
        "baselineRedCount": len(baseline_red),
        "redCount": len(red),
        "newRed": new_red,
        "resolvedRed": resolved_red,
        "absentBaselineRed": absent_baseline_red,
        "wallSeconds": float(re.findall(r"^real ([0-9.]+)$", log, re.M)[-1]),
        "logSHA256": hashlib.sha256(log_path.read_bytes()).hexdigest(),
    }
(HERE / "regression-comparison.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(1 if any(r["newRed"] or r["absentBaselineRed"] for r in result.values()) else 0)
