#!/usr/bin/env python3
"""One-command local reproduction; no changes to the CellProtocol checkout."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--cellprotocol',type=pathlib.Path,default=ROOT.parents[3]/'CellProtocol');p.add_argument('--out',type=pathlib.Path,default=ROOT/'resultater');args=p.parse_args()
args.out.mkdir(parents=True,exist_ok=True)
expected=json.loads((ROOT/'source_manifest.json').read_text())
for name,sha in expected['files'].items():
    source=args.cellprotocol/name
    if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest()!=sha:raise SystemExit('Source mismatch: '+str(source)+'; reproduce from the recorded source revision, do not silently accept new code.')
# Numeric matrix first, so manifest describes only deterministic numeric artifacts.
subprocess.run([sys.executable,str(ROOT/'study.py'),'--out',str(args.out)],check=True)
contracts=subprocess.run([sys.executable,str(ROOT/'test_contracts.py')],capture_output=True,text=True)
(args.out/'python_contracts.txt').write_text(contracts.stdout+contracts.stderr);contracts.check_returncode()
with tempfile.TemporaryDirectory(prefix='relational-oracle-') as tmp:
    build=pathlib.Path(tmp)
    for name in ['Support.swift','Oracle.swift','TestMain.swift','build.sh']:shutil.copy2(ROOT/'oracle'/name,build/name)
    subprocess.run(['bash',str(build/'build.sh'),str(args.cellprotocol)],check=True)
    shutil.copy2(build/'direct-tests-output.txt',args.out/'swift_tests.txt')
    subprocess.run([sys.executable,str(ROOT/'parity.py'),'--oracle',str(build/'oracle'),'--out',str(args.out/'swift_parity.json')],check=True)
manifest=json.loads((args.out/'manifest.json').read_text())
# Non-numeric logs can already exist from a previous execution; verify numeric files.
for name,sha in manifest['files'].items():
    if name in ['swift_tests.txt','python_contracts.txt','swift_parity.json']:continue
    assert hashlib.sha256((args.out/name).read_bytes()).hexdigest()==sha,name
print('Completed: 144 synthetic logs / 1152 runs; 8 Python contracts; original 7 Swift engine tests; 20 differential fixtures (17 numeric, 3 migration). Full CellApple integration not tested.')
