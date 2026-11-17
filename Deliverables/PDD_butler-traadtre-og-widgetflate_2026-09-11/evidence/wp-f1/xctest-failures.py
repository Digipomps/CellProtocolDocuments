#!/usr/bin/python3
"""Skriver feilede og avbrutte XCTest-tester fra en macOS swift test-logg som Klasse/metode."""
import collections, re, sys
log = open(sys.argv[1], errors="replace").read()
ev = re.findall(r"Test Case '-\[\w+\.(\w+) (\w+)\]' (started|passed|failed|skipped)", log)
st = collections.Counter(f"{c}/{m}" for c, m, s in ev if s == "started")
dn = collections.Counter(f"{c}/{m}" for c, m, s in ev if s != "started")
failed = sorted({f"{c}/{m}" for c, m, s in ev if s == "failed"})
aborted = sorted((st - dn).keys())
for t in failed: print("FEILET", t)
for t in aborted: print("AVBRUTT", t)
