import subprocess, pathlib, os, sys, json, datetime
root=pathlib.Path('/Users/kjetil/Build/Digipomps/HAVEN')
wt=root/'CellProtocol/_wt-bro-kanal-auth-20260927'
evidence=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N23-N26-evidence'
name,action,*extra=sys.argv[1:]
env=os.environ.copy();env['SWIFTPM_MODULECACHE_OVERRIDE']='/private/tmp/cp53-module-cache';env['CLANG_MODULE_CACHE_PATH']='/private/tmp/cp53-module-cache'
if name=='multipeer': env['CP53_MULTIPEER_TEST']='1'
guard=['bash',str(root/'_worktrees/rel-2026.9/CellScaffold-job-e-20260927/scripts/check_build_capacity.sh'),str(wt)]
g=subprocess.run(guard,capture_output=True,text=True);(evidence/(name+'-capacity.log')).write_text(g.stdout+g.stderr)
print(g.stdout+g.stderr,flush=True)
if g.returncode: sys.exit(g.returncode)
cmd=['swift',action,'--disable-sandbox','--disable-automatic-resolution','--cache-path','/private/tmp/bro-swift-cache','--jobs','4']+extra
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (evidence/(name+'.log')).open('w') as f: code=subprocess.call(cmd,cwd=wt,env=env,stdout=f,stderr=subprocess.STDOUT)
result=dict(command=cmd,cwd=str(wt),started=start,finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit=code)
(evidence/(name+'-result.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
lines=(evidence/(name+'.log')).read_text(errors='replace').splitlines()
for line in lines:
 if ': error:' in line or line.startswith('error:') or 'Build complete!' in line: print(line)
summary=[line for line in lines if 'Executed ' in line]
if summary: print(summary[-1])
sys.exit(code)
