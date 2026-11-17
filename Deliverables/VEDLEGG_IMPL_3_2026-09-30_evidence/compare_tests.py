#!/usr/bin/env python3
"""Summarize complete logs; never treat a compiler failure as a test pass."""
import json,re
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parent

def inspect(name):
    text=(root/(name+'.log')).read_text()
    xc=re.findall(r"Test Case '-\[(\S+) (\S+)\]' (passed|failed|skipped)",text)
    swift=re.findall(r'Test run with (\d+) tests? in (\d+) suites? (passed|failed)',text)
    failures={a+'.'+b for a,b,status in xc if status=='failed'}
    failures.update(re.findall(r'Test ([\w]+\([^\n]*?\)) recorded an issue',text))
    return dict(log=name+'.log',exit=int((root/(name+'.exit')).read_text()),
        built='Build complete!' in text,
        xctestCounts=dict(Counter(status for _,_,status in xc)),
        swiftTestingCount=sum(int(count) for count,_,_ in swift),
        swiftTestingBundles=len(swift),failed=sorted(failures),
        attachmentTests=[dict(name=a+'.'+b,result=status) for a,b,status in xc if a.endswith('.CorrespondenceAttachmentTests')],
        suiteSummaries=swift)

pairs=[('cellprotocol-baseline','cellprotocol-final-verified'),
       ('havenagentd-baseline-serial','havenagentd-final-serial')]
result=[]
for before,after in pairs:
    baseline,candidate=inspect(before),inspect(after)
    new=sorted(set(candidate['failed'])-set(baseline['failed']))
    result.append(dict(baseline=baseline,candidate=candidate,newFailures=new,
        comparableRunHasNewFailures=bool(new),
        finished=baseline['built'] and candidate['built'] and baseline['swiftTestingBundles']==candidate['swiftTestingBundles']))
(root/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([dict(before=x['baseline']['log'],after=x['candidate']['log'],newFailures=x['newFailures'],finished=x['finished']) for x in result],indent=2))
if any(x['newFailures'] or not x['finished'] for x in result): raise SystemExit(1)
