#!/usr/bin/env python3
"""Run selected existing XCTest cases with isolated storage, without building.

Raw logs stay in the task's temporary directory. This is a local diagnostic,
not a clean-build release gate. Caller explicitly supplies any live-test flags.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
TEMP = Path('/private/tmp/kallimachos-chain-20261013')
PRODUCTS = TEMP / 'products'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    p.add_argument('--selector', required=True)
    p.add_argument('--source-repo', type=Path, required=True)
    p.add_argument('--env-json', type=Path)
    a = p.parse_args()
    if not a.name.replace('-', '').isalnum():
        p.error('name must be alphanumeric/hyphens')
    raw = TEMP / (a.name + '.log')
    record = ROOT / 'evidence' / (a.name + '.json')
    if raw.exists() or record.exists():
        p.error('refusing to overwrite a run')
    exe = PRODUCTS / 'AppTests.xctest/Contents/MacOS/AppTests'
    expected = json.loads((ROOT / 'evidence/prebuilt-provenance.json').read_text())['binarySHA256']
    assert hashlib.sha256(exe.read_bytes()).hexdigest() == expected
    developer = Path(subprocess.check_output(['xcode-select', '-p'], text=True).strip())
    platform = developer / 'Platforms/MacOSX.platform/Developer'
    env = {
        'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'en_US.UTF-8',
        'CELL_SCAFFOLD_TEST_ISOLATION': '1',
        'DYLD_FRAMEWORK_PATH': str(platform / 'Library/Frameworks'),
        'DYLD_LIBRARY_PATH': str(platform / 'usr/lib') + ':' + str(developer / 'Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/macosx'),
        'HAVEN_COMMONS_CORPUS_ROOT': str(TEMP / 'public-corpus'),
    }
    additions = json.loads(a.env_json.read_text()) if a.env_json else {}
    assert all(k.startswith(('RUN_KALLIMACHOS_', 'KALLIMACHOS_')) for k in additions)
    assert additions.get('KALLIMACHOS_ADVISOR_LIVE_TIER', 'local') == 'local'
    env.update(additions)
    with tempfile.TemporaryDirectory(prefix=a.name + '-', dir=TEMP) as isolated:
        env.update(HOME=isolated, TMPDIR=isolated, CELL_VAULT_DOCUMENT_ROOT=isolated + '/CellsContainer')
        cmd = [str(developer / 'usr/bin/xctest'), '-XCTest', a.selector, str(PRODUCTS / 'AppTests.xctest')]
        started = time.monotonic()
        with raw.open('x') as f:
            try:
                result = subprocess.run(cmd, cwd=a.source_repo, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=1500)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 'timeout'
        elapsed = round(time.monotonic() - started, 3)
    lines = raw.read_text(errors='replace').splitlines()
    summary = [l for l in lines if l.startswith(('Test Suite ', 'Test Case ')) or 'Executed ' in l or 'error:' in l]
    # Only this allowlisted test summary is durable; raw runtime diagnostics can
    # contain synthetic UUIDs and temporary paths.
    record.write_text(json.dumps({'selector': a.selector, 'exitCode': code, 'elapsedSeconds': elapsed,
        'binarySHA256': expected, 'liveConfiguration': additions, 'summary': summary}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'exitCode': code, 'elapsedSeconds': elapsed, 'rawLog': str(raw)}, ensure_ascii=False))
    print('\n'.join(summary[-12:]))
    raise SystemExit(0 if code == 0 else 1)

if __name__ == '__main__':
    main()
