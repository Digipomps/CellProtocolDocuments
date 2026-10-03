#!/usr/bin/python3
"""Record exact CI commands and add the user-required --disable-sandbox flag."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
args = ["swift", sys.argv[1], "--disable-sandbox", *sys.argv[2:]]
record = {"argv": args, "command": shlex.join(args), "started": time.time()}
print("WP-R4 command: " + record["command"], file=sys.stderr, flush=True)
capacity = subprocess.run(["scripts/check_build_capacity.sh", "."], stdout=sys.stderr)
if capacity.returncode:
    record["exit"] = capacity.returncode
    record["blocked_before_swift"] = True
else:
    record["exit"] = subprocess.run(args).returncode
record["finished"] = time.time()
with (root / "ci-commands.jsonl").open("a") as handle:
    handle.write(json.dumps(record) + "\n")
sys.exit(record["exit"])
