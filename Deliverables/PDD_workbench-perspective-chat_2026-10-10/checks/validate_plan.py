#!/usr/bin/env python3
"""Bounded document checks. Does not mark PDD/product gates green."""
from pathlib import Path
import json, re, hashlib, sys
ROOT=Path(__file__).resolve().parent.parent
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT
plan=json.loads((ROOT/'plan.json').read_text())
spec=(SOURCE/'FORMAALSSPEC.md').read_text()
expected=set(re.findall(r'^\| (purpose://candidate\.workbench-perspective-chat\.[^ |]+) \|',spec,re.M))
expected.remove(plan['rootPurposeRef'])
packages=plan['workPackages']
actual=[p['purposeRef'] for p in packages]
assert len(actual)==len(set(actual))==len(expected)==7
assert set(actual)==expected
seen=set()
for p in packages:
    assert set(p['dependsOn'])<=seen, p['id']
    assert p['executor'] and p['tests'] and p['artifacts']
    assert p['status']=='planned'
    seen.add(p['id'])
tests=set(re.findall(r'^\| (test\.[^ |]+) \|',spec,re.M))
assert set(plan['requiredTests'])==tests
assert {t for p in packages for t in p['tests']}==tests
for f in ['PLAN.md','dataflow.md','handoff/README.md','contract/workbench-v1.json','contract/fixtures.json','contract/retention.json','contract/gui-binding-inventory.json','images/plan-g2-v1.html','images/plan-g2-v1.png','evidence/g2-source-refresh.md']:
    assert (ROOT/f).is_file(),f
bindings=json.loads((ROOT/'contract/gui-binding-inventory.json').read_text())['bindings']
actions=json.loads((SOURCE/'images/action-inventory.json').read_text())
assert sorted(a['keypath'] for a in actions)==sorted(b['keypath'] for b in bindings)
receipt=json.loads((SOURCE/'evidence/g1-gui-approval.json').read_text())
manifest=SOURCE/receipt['manifest']
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==receipt['manifestSHA256']
images=json.loads(manifest.read_text())
assert len(images)==receipt['approvedImageCount']
for img in images:
    assert hashlib.sha256((SOURCE/img['path']).read_bytes()).hexdigest()==img['sha256'],img['path']
assert plan['gates']['G2']=='pending' and plan['gates']['G3']=='pending'
print(json.dumps({'scope':'G2 document structure only','leafWorkPackages':len(actual),'mappedTests':len(tests),'candidateActions':len(bindings),'unchangedApprovedImages':len(images),'status':'PASS','productTests':'not run'},ensure_ascii=False))
