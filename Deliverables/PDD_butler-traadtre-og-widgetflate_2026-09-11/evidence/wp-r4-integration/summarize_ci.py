#!/usr/bin/python3
import collections
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
commands = [json.loads(line) for line in (root / "ci-commands.jsonl").read_text().splitlines()]
tests = [c for c in commands if c["argv"][1] == "test"]
chunks = []
for path in sorted((root / "ci-chunks").glob("bolk-*.log"), key=lambda p: int(p.stem.split("-")[-1])):
    number = int(path.stem.split("-")[-1])
    log = path.read_text(errors="replace")
    status_log = re.sub(r"error: Process [^\n]*exited with unexpected signal code \d+\n", "", log)
    events = re.findall(r"Test Case '([^']+)' (started|passed|failed|skipped)", status_log)
    counts = collections.Counter(state for _, state in events)
    started = collections.Counter(name for name, state in events if state == "started")
    completed = collections.Counter(name for name, state in events if state != "started")
    command = tests[number - 1] if number <= len(tests) else None
    chunks.append({
        "chunk": number,
        "command": command["command"] if command else None,
        "exit": command["exit"] if command else None,
        "started": counts["started"],
        "passed": counts["passed"],
        "failed": counts["failed"],
        "skipped": counts["skipped"],
        "aborted_tests": list((started - completed).elements()),
        "failed_tests": [name for name, state in events if state == "failed"],
        "signals": re.findall(r"exited with unexpected signal code (\d+)", log),
        "assertions": [line for line in log.splitlines() if re.search(r"\.swift:\d+(?::\d+)?: error:", line)],
    })
summary = {
    "completed_chunks": len(tests),
    "totals": {k: sum(c[k] for c in chunks) for k in ["started", "passed", "failed", "skipped"]},
    "aborted": sum(len(c["aborted_tests"]) for c in chunks),
    "chunks": chunks,
}
(root / "ci-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
lines = ["# WP-R4 — CI-filter: faktisk kjørte kommandoer og resultater", "", "Filter, bolkdeling og fem skip-regler er fra uendret `ci/run-tests.sh`. Wrapperen legger bare til `--disable-sandbox`, kjører kapasitetskontrollen og registrerer kommando/exit.", "", "| Bolk | Exit | Startet | Bestått | Feilet | Skippet | Avbrutt | Signal |", "|---|---:|---:|---:|---:|---:|---:|---|"]
for c in chunks:
    lines.append(f'| {c["chunk"]} | {c["exit"]} | {c["started"]} | {c["passed"]} | {c["failed"]} | {c["skipped"]} | {len(c["aborted_tests"])} | {", ".join(c["signals"])} |')
lines += ["", "Tallene teller XCTest-statuslinjer fra hver bolk, uten duplikater fra samleloggens feilekko. Avbrutt = startet uten bestått/feilet/skippet før prosessavslutning. Tester som ikke rakk å starte i en krasjet bolk er ikke talt som kjørt."]
for c in chunks:
    lines += ["", f'## Bolk {c["chunk"]}', "", "```sh", c["command"] or "RUNNING", "```", "", f'Exit: {c["exit"]}.']
    for name in c["failed_tests"]:
        lines += ["", "Feilet: `" + name + "`."]
    for name in c["aborted_tests"]:
        lines += ["", "Avbrutt: `" + name + "`."]
    if c["assertions"]:
        lines += ["", "```text", *c["assertions"], "```"]
(root / "CI-RESULTATER.md").write_text("\n".join(lines) + "\n")
print(json.dumps({k:v for k,v in summary.items() if k != "chunks"}, ensure_ascii=False))
print("Failed chunks:", [c["chunk"] for c in chunks if c["exit"]])
