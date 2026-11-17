from pathlib import Path
import os, subprocess, json, time
haven = Path(__file__).resolve().parents[5]
root = haven / 'CellProtocol/_wt-bro-kanal-auth-20260927'
evidence = Path(__file__).resolve().parent
temporary = Path('/private/tmp/cp53-n27-n34-20260929')
temporary.mkdir(exist_ok=True)
env = dict(os.environ, SWIFTPM_MODULECACHE_OVERRIDE='/private/tmp/cp53-module-cache',
           CLANG_MODULE_CACHE_PATH='/private/tmp/cp53-module-cache', TMPDIR=str(temporary))
flags = ['--disable-sandbox', '--disable-automatic-resolution', '--cache-path', '/private/tmp/bro-swift-cache', '--jobs', '4']
commands = [
 ('full-build', ['swift', 'build'] + flags, {}),
 ('full-test', ['swift', 'test'] + flags, {}),
 ('native', ['swift', 'test'] + flags + ['--filter', 'ScannerMultipeerProcessTests/testTwoProcessesUseRealMultipeerInBothInvitationDirections'], {'CP53_MULTIPEER_TEST':'1'}),
]
results = []
for name, command, extra in commands:
    started = time.time()
    with (evidence / (name + '.log')).open('w') as log:
        log.write('COMMAND=' + ' '.join(command) + '\n'); log.flush()
        result = subprocess.run(command, cwd=root, env=dict(env, **extra), stdout=log, stderr=subprocess.STDOUT)
        log.write(f'\nCOMMAND_EXIT={result.returncode}\n')
    results.append(dict(name=name, command=command, exit=result.returncode, seconds=round(time.time()-started, 2)))
    (evidence/'local-results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(results[-1], flush=True)
    if name == 'full-build' and result.returncode: break
