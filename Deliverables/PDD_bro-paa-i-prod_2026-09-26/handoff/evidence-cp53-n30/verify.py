from pathlib import Path
import os, subprocess, json, time, sys
haven = Path(__file__).resolve().parents[5]
root = haven / 'CellProtocol/_wt-bro-kanal-auth-20260927'
evidence = Path(__file__).resolve().parent
temporary = Path('/private/tmp/cp53-n30-20260929')
temporary.mkdir(exist_ok=True)
env = dict(os.environ, SWIFTPM_MODULECACHE_OVERRIDE=str(temporary/'module-cache'),
           CLANG_MODULE_CACHE_PATH=str(temporary/'module-cache'), TMPDIR=str(temporary))
flags = ['--disable-sandbox', '--disable-automatic-resolution', '--cache-path', '/private/tmp/bro-swift-cache', '--jobs', '4']
name = sys.argv[1]
command = ['swift', sys.argv[2]] + flags + sys.argv[3:]
started = time.time()
with (evidence / (name + '.log')).open('w') as log:
    log.write('COMMAND=' + ' '.join(command) + '\n'); log.flush()
    result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    log.write(f'\nCOMMAND_EXIT={result.returncode}\n')
record = dict(name=name, command=command, exit=result.returncode, seconds=round(time.time()-started, 2))
(evidence/(name+'-result.json')).write_text(json.dumps(record, indent=2)+'\n')
print(record, flush=True)
lines = (evidence/(name+'.log')).read_text().splitlines()
for line in lines:
    if 'error:' in line or 'Executed ' in line or 'failed' in line: print(line[:1200])
sys.exit(result.returncode)
