#!/bin/bash
set -euo pipefail

mode=--dry-run
for argument in "$@"; do
    case "$argument" in
        --dry-run|--go) mode="$argument" ;;
        \#*) break ;;
        *) echo "Bruk: $0 [--dry-run|--go]" >&2; exit 2 ;;
    esac
done

handoff_dir="$(cd "$(dirname "$0")" && pwd)"
task_dir="$(cd "$handoff_dir/.." && pwd)"
haven_root="$(cd "$task_dir/../../.." && pwd)"
scaffold_dir="$haven_root/PalazzoScaffold"

echo "Arbeidskatalog: $scaffold_dir"
echo "swift build --disable-sandbox --disable-automatic-resolution --skip-update"
echo "swift test --disable-sandbox --disable-automatic-resolution --skip-update --triple x86_64-apple-macosx13.0 --disable-swift-testing -j 4"
echo "Alle XCTest-tester kjøres. Ingen --filter eller --skip."
echo "x86_64 matcher denne maskinens XCTest-laster. Swift Testing har ingen tester her."
if [ "$mode" = --dry-run ]; then
    echo "Tørrkjøring: ingen filer endres og ingen bygg eller tester startes."
    exit 0
fi

python3 - "$scaffold_dir" "$task_dir/evidence" <<'PY'
from pathlib import Path
import datetime
import json
import os
import re
import subprocess
import sys

scaffold = Path(sys.argv[1])
test_sources = list((scaffold / 'Tests').rglob('*.swift'))
if any(re.search(r'\bimport\s+Testing\b|@(?:Test|Suite)\b', p.read_text()) for p in test_sources):
    sys.exit('blocked: Swift Testing-tester finnes nå; den kjøreruten kan ikke slås av.')
resolved = json.loads((scaffold / 'Package.resolved').read_text())
for pin in resolved['pins']:
    if not (scaffold / '.build/checkouts' / pin['identity']).is_dir():
        sys.exit('blocked: mangler lokal avhengighet ' + pin['identity'] + '; ingen nedlasting utføres.')
expected = sum(len(re.findall(r'\bfunc\s+test\w+\s*\(', p.read_text())) for p in test_sources)
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
evidence = Path(sys.argv[2]) / ('local-build-' + stamp)
evidence.mkdir(parents=True)
environment = os.environ.copy()
environment['PALAZZO_FACADE_EVIDENCE_DIRECTORY'] = str(evidence / 'responses')
commands = [
    ('build', ['swift', 'build', '--disable-sandbox', '--disable-automatic-resolution', '--skip-update']),
    ('test', ['swift', 'test', '--disable-sandbox', '--disable-automatic-resolution', '--skip-update',
              '--triple', 'x86_64-apple-macosx13.0', '--disable-swift-testing', '-j', '4']),
]
results = []
for label, command in commands:
    logfile = evidence / (label + '.log')
    with logfile.open('w') as output:
        result = subprocess.run(command, cwd=scaffold, env=environment, stdout=output, stderr=subprocess.STDOUT)
    text = logfile.read_text(errors='replace')
    summaries = re.findall(r'Executed (\d+) tests?, with (\d+) failures?', text)
    results.append(dict(phase=label, command=command, exit_code=result.returncode,
                        summaries=summaries, log=str(logfile)))
    print(label + ': exit=' + str(result.returncode) + ', logg=' + str(logfile), flush=True)
(evidence / 'result.json').write_text(json.dumps(results, indent=2) + '\n')
last = results[-1]
passed = (all(r['exit_code'] == 0 for r in results) and bool(last['summaries'])
          and int(last['summaries'][-1][0]) >= expected and int(last['summaries'][-1][1]) == 0)
if not passed:
    sys.exit('blocked: skrevet, ikke verifisert. Les rålogger og faktisk XCTest-resultat.')
print('skrevet, verifisert med full regresjon (' + last['summaries'][-1][0] + ' XCTest-tester).')
print('WP5 / selvstendig oppstart og visuell paritet må fortsatt utføres separat.')
PY
