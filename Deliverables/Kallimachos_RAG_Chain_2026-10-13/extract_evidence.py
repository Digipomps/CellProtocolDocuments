#!/usr/bin/env python3
"""Allowlist public/synthetic response evidence from temporary XCTest logs.

XCTest's stderr can interrupt Swift stdout mid-JSON in a merged logfile. Remove
only its recognizable diagnostic lines before decoding, retain the original
temporary log and record the removal count. No model prose is corrected.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
TEMP = Path('/private/tmp/kallimachos-chain-20261013')

def normalized(name):
    raw = (TEMP / (name + '.log')).read_text(errors='replace')
    clean, count = re.subn(r"Test (?:Case|Suite) [^\n]*\n|\t Executed [^\n]*\n", '', raw)
    return clean, {'rawSHA256': hashlib.sha256(raw.encode()).hexdigest(),
                   'xctestDiagnosticLinesRemoved': count}

def field(s, name):
    m = re.search(r'^\[' + re.escape(name) + r'\] (.*)$', s, re.M)
    return m[1] if m else None

def after_json(s, marker):
    if marker not in s:
        return None
    tail = s.split(marker, 1)[1].lstrip()
    try:
        value, _ = json.JSONDecoder().raw_decode(tail)
        return value
    except ValueError:
        return None

def main():
    out = {'schema': 'haven.kallimachos.local-chain-observation.v1', 'traces': {}}
    s, meta = normalized('canary-01')
    arms = {}
    for m in re.finditer(r'\[canary ([ABC])\] status=(\S+) route=(\S+) answer=', s):
        arms[m[1]] = {'status': m[2], 'route': m[3], 'answer': after_json(s[m.start():], 'answer=')}
    null = s.split('[canary D null control] ', 1)[1].strip()
    # Only the synthetic answer; strip any later runtime diagnostics if present.
    null = null.split('\nAIInvoke', 1)[0].strip()
    out['canary'] = {'arms': arms, 'nullAnswer': null,
        'manualFinding': 'A follows 7/11, B states a gap, C follows 3/5. D invents an unrelated clinical explanation; it does not know either canary fact.'}
    out['traces']['canary-01'] = meta
    s, meta = normalized('fallback-offline-01')
    out['fallback'] = {key: field(s, key) for key in ['status', 'route', 'gate', 'deterministic', 'advice.raw']}
    out['traces']['fallback-offline-01'] = meta
    s, meta = normalized('live-name-01')
    out['liveName'] = {'statusLine': field(s, 'Kallimachos advisor live'), 'answer': after_json(s, '[Kallimachos advisor live] advice=')}
    out['traces']['live-name-01'] = meta
    s, meta = normalized('showcase-01')
    cases = []
    for segment in re.split(r'=== SHOWCASE \d+ ===', s)[1:]:
        case = {key: field(segment, key) for key in ['q', 'status', 'gate', 'route', 'deterministic', 'advice.contractParsed']}
        case['answer'] = after_json(segment, '[advice.raw] ')
        cost = field(segment, 'cost') or ''
        case['usage'] = {}
        for key in ['inputTokens', 'outputTokens', 'totalCostTicks']:
            m = re.search('"' + key + r'": (?:CellBase\.)?ValueType.integer\((\d+)\)', cost)
            if m:
                case['usage'][key] = int(m[1])
        cases.append(case)
    out['showcase'] = cases
    out['traces']['showcase-01'] = meta
    dest = ROOT / 'evidence/observations.json'
    if dest.exists():
        raise SystemExit('Refusing to overwrite observations')
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print('Saved', len(cases), 'showcase observations, canary and fallback evidence.')

if __name__ == '__main__':
    main()
