#!/usr/bin/env python3
"""Independent observation-fixture validation. No runtime or sensor claims."""
import argparse, json
from pathlib import Path
from datetime import datetime, timedelta

def valid(event, now):
    required = {"schemaVersion", "revision", "observedAt", "validUntil", "transition", "labels", "configurationRevision"}
    if not required.issubset(event): return False
    if event["schemaVersion"] != 1: return False
    if any(type(event[k]) is not int or event[k] < 0 for k in ("revision", "configurationRevision")): return False
    if event["transition"] not in {"snapshot", "entered", "left", "configurationChanged"}: return False
    labels = event["labels"]
    if not isinstance(labels, list) or len(labels) > 128: return False
    if any(not isinstance(x, str) or not x or len(x.encode("utf8")) > 256 for x in labels): return False
    if len(set(labels)) != len(labels): return False
    parse = lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))
    try: observed, until = parse(event["observedAt"]), parse(event["validUntil"])
    except (TypeError, ValueError): return False
    return until > observed and observed <= now + timedelta(seconds=30)

parser = argparse.ArgumentParser()
parser.add_argument("--repo-root", required=True, type=Path)
args = parser.parse_args()
fixtures = sorted((args.repo_root / "Tests/CellBaseTests/Fixtures/PerspectiveContext").glob("*.json"))
assert len(fixtures) == 5, "Missing expected fixtures"
for fixture in fixtures:
    data = json.loads(fixture.read_text())
    now = datetime.fromisoformat(data["evaluatedAt"].replace("Z", "+00:00"))
    actual = valid(data["observation"], now)
    assert actual == data["valid"], fixture.name
    print(f"PASS {fixture.name}: {actual}")
print("5/5 observation fixtures passed")
