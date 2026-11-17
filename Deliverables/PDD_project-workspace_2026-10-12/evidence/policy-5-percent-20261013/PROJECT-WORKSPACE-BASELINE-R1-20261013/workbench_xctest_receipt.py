"""Validate a completed, exact XCTest selection without classifying app logs as tests."""
import collections
import re
from xctest_receipts import require_green_results


def validate_xctest(text, expected, exit_code):
    if exit_code != 0:
        raise ValueError(f"test process exit {exit_code}")
    expected = list(expected)
    if not expected or len(set(expected)) != len(expected):
        raise ValueError("expected test manifest empty or duplicated")
    # XCTest on Darwin. Runtime diagnostics (including expected rejection errors)
    # are not test verdicts. Fail on actual XCTest failure/skip and compiler crash.
    cases = re.findall(r"Test Case '-\[\w+\.([^\]]+)\]' (started|passed|failed|skipped)\b", text, re.M)
    started = [name for name, state in cases if state == "started"]
    passed = [name for name, state in cases if state == "passed"]
    if collections.Counter(started) != collections.Counter(expected):
        raise ValueError("started test inventory mismatch")
    if collections.Counter(passed) != collections.Counter(expected):
        raise ValueError("passed test inventory mismatch")
    if any(state in ("failed", "skipped") for _, state in cases):
        raise ValueError("XCTest failure or skip")
    identifiers = {suite+'/'+method for suite, method in re.findall(r"Test Case '-\[([^ ]+) ([^]]+)\]' started\.$", text, re.M)}
    try:
        require_green_results(text, identifiers, allow_skips=False)
    except RuntimeError as error:
        raise ValueError(str(error)) from error
    if re.search(r"^Test Suite .+ (?:failed|skipped)\b|^error:|^.*?:\d+:\d+: error:|^.*unexpected signal|^.*[Ff]atal error:", text, re.M):
        raise ValueError("test suite, compiler or crash diagnostic")
    # Require every opened suite to close, with its own immediate summary.
    stack = []
    roots = []
    lines = text.splitlines()
    suite_methods = {}
    for name in expected:
        suite = name.split(" ", 1)[0]
        suite_methods[suite] = suite_methods.get(suite, 0) + 1
    counts = {}
    for index, line in enumerate(lines):
        match = re.match(r"^Test Suite '([^']+)' (started|passed) at ", line)
        if not match:
            continue
        name, state = match.groups()
        if state == "started":
            stack.append(name)
            continue
        if not stack or stack.pop() != name:
            raise ValueError("unbalanced XCTest suite")
        summary = re.match(r"\s*Executed (\d+) tests?, with (\d+) failures? \((\d+) unexpected\)", lines[index + 1] if index + 1 < len(lines) else "")
        if not summary or summary.groups()[1:] != ("0", "0"):
            raise ValueError("missing or nonzero XCTest summary")
        total = int(summary[1])
        if name in suite_methods:
            if name in counts or total != suite_methods[name]:
                raise ValueError("named suite total mismatch")
            counts[name] = total
        if not stack:
            roots.append(total)
    if stack or counts != suite_methods or sum(roots) != len(expected):
        raise ValueError("incomplete XCTest receipt")
    return sorted(passed)
