"""Source-bound XCTest receipt parsing; log content is not authenticated."""
import re

def discovered_tests(output):
    identifiers = set()
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if not re.fullmatch(r"[A-Za-z0-9_.]+/[A-Za-z0-9_]+", line):
            raise RuntimeError("Unexpected test discovery record: " + line)
        if line in identifiers:
            raise RuntimeError("Duplicate test discovery record: " + line)
        identifiers.add(line)
    if not identifiers:
        raise RuntimeError("Test discovery was empty")
    return identifiers


def require_green_results(output, expected, allow_skips):
    # Require complete, ordered XCTest bundles and exact named terminal cases.
    # This is log reconciliation, not authentication of arbitrary log content.
    def require(condition, message):
        if not condition:
            raise RuntimeError(message)
    expected = set(expected)
    require(expected, "Required green selection is empty")
    top = re.compile(r"^Test Suite '((?:All|Selected) tests)' (started|passed|failed)[^\n]*$", re.M)
    # SwiftPM's merged streams can interleave product text before a genuine
    # XCTest record. Require complete paired start/terminal records instead of
    # assuming every record starts at column zero (eight real cases did not).
    case_start = re.compile(r"Test Case '-\[([^ ]+) ([^]]+)\]' started\.$", re.M)
    terminal = re.compile(r"Test Case '-\[([^ ]+) ([^]]+)\]' (passed|failed|skipped) \([0-9]+[.,][0-9]+ seconds\)\.$", re.M)
    summary = re.compile(r"[ \t]*Executed ([0-9]+) tests?, with (?:(\d+) tests? skipped and )?([0-9]+) failures? \(([0-9]+) unexpected\) in [0-9]+[.,][0-9]+(?: \([0-9]+[.,][0-9]+\))? seconds(?:\n|$)")
    cases = {}
    started = set()
    active = None
    bundles = 0
    events = sorted([(m.start(), 'top', m) for m in top.finditer(output)] +
                    [(m.start(), 'case-start', m) for m in case_start.finditer(output)] +
                    [(m.start(), 'case', m) for m in terminal.finditer(output)])
    for _, kind, match in events:
        if kind in ('case', 'case-start'):
            identifier = match[1]+'/'+match[2]
            require(active is not None, 'Terminal test outside top-level bundle')
            require(identifier in expected, 'Unselected terminal test result: '+identifier)
            if kind == 'case-start':
                require(identifier not in started, 'Duplicate started test: '+identifier)
                started.add(identifier)
                active['pending'].add(identifier)
                continue
            require(identifier in active['pending'], 'Terminal case lacks matching start: '+identifier)
            require(identifier not in cases, 'Duplicate terminal test result: '+identifier)
            require(match[3]=='passed' or (allow_skips and match[3]=='skipped'),
                    'Required green test did not pass: '+identifier)
            cases[identifier] = match[3]
            active['pending'].remove(identifier)
            active['cases'].append(identifier)
        elif match[2]=='started':
            require(active is None, 'Overlapping or truncated top-level XCTest bundle')
            active = {'name':match[1], 'cases':[], 'pending':set()}
        else:
            require(active is not None and active['name']==match[1], 'Unmatched top-level XCTest bundle footer')
            require(not active['pending'], 'Top-level bundle has unfinished test cases')
            end = summary.match(output, match.end()+1)
            require(end is not None, 'Missing complete top-level XCTest bundle summary')
            count, skipped, failures, unexpected = (int(x or 0) for x in end.groups())
            require(match[2]=='passed' and failures==0 and unexpected==0, 'XCTest bundle was not green')
            require(count==len(active['cases']), 'Top-level summary does not match terminal test count')
            require(skipped==sum(cases[x]=='skipped' for x in active['cases']), 'Top-level skip count mismatch')
            bundles += 1
            active = None
    require(active is None and bundles>0, 'Missing complete top-level XCTest bundle footer')
    require(set(cases)==expected, 'Executed test IDs differ from discovery/selection: missing='+repr(sorted(expected-set(cases))))
    all_terminal = re.findall(r"Test Case .* (?:passed|failed|skipped)(?:[ \n]|$)",output,re.M)
    require(len(all_terminal)==len(cases), 'Malformed terminal XCTest test record')
    return {'selected':len(expected), 'passed':sum(s=='passed' for s in cases.values()),
            'skipped':sorted(k for k,v in cases.items() if v=='skipped')}

