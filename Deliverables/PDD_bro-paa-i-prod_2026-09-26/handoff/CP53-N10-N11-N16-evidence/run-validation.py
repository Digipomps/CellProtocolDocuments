from pathlib import Path
import subprocess, os, json, datetime
root=Path.cwd();wt=root/'CellProtocol/_wt-bro-kanal-auth-20260927';ev=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N10-N11-N16-evidence'
guard=root/'_worktrees/rel-2026.9/CellScaffold-job-e-20260927/scripts/check_build_capacity.sh'
env=os.environ.copy();env.update(SWIFTPM_MODULECACHE_OVERRIDE='/private/tmp/cp53-module-cache',CLANG_MODULE_CACHE_PATH='/private/tmp/cp53-module-cache')
base=['--disable-sandbox','--disable-automatic-resolution','--cache-path','/private/tmp/bro-swift-cache','--jobs','4']
results=[]
for name,cmd,opt in [('build',['swift','build']+base,{}),('full-test',['swift','test']+base,{}),('multipeer',['swift','test']+base+['--filter','ScannerMultipeerProcessTests/testTwoProcessesUseRealMultipeerInBothInvitationDirections'],{'CP53_MULTIPEER_TEST':'1'})]:
 with (ev/f'{name}-capacity.log').open('w') as f: guardResult=subprocess.run(['bash',str(guard),str(wt)],stdout=f,stderr=subprocess.STDOUT)
 if guardResult.returncode: print('CAPACITY BLOCKED',flush=True);break
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (ev/f'{name}.log').open('w') as f:result=subprocess.run(cmd,cwd=wt,env=env|opt,stdout=f,stderr=subprocess.STDOUT)
 results.append(dict(name=name,command=cmd,env=opt,exit=result.returncode,start=start,end=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (ev/'validation-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,result.returncode,flush=True)
