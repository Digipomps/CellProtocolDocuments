from pathlib import Path
import subprocess,os,time,json
root=Path('/Users/kjetil/Build/Digipomps/HAVEN')
wt=root/'CellProtocol/_wt-bro-kanal-auth-20260927'
evidence=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N14-N15-N18-evidence'
env=os.environ.copy();env['SWIFTPM_MODULECACHE_OVERRIDE']='/private/tmp/cp53-module-cache';env['CLANG_MODULE_CACHE_PATH']='/private/tmp/cp53-module-cache'
flags=['--disable-sandbox','--disable-automatic-resolution','--cache-path','/private/tmp/bro-swift-cache','--jobs','4']
results=[]
for name,cmd in [('build',['swift','build']+flags),('test',['swift','test']+flags),('multipeer',['swift','test']+flags+['--filter','ScannerMultipeerProcessTests/testTwoProcessesUseRealMultipeerInBothInvitationDirections'])]:
 with (evidence/(name+'-capacity.log')).open('w') as log:
  guard=subprocess.run(['bash',str(root/'_worktrees/rel-2026.9/CellScaffold-job-e-20260927/scripts/check_build_capacity.sh'),str(wt)],stdout=log,stderr=subprocess.STDOUT)
 if guard.returncode:print('STOPPED capacity',flush=True);break
 if name=='multipeer':env['CP53_MULTIPEER_TEST']='1'
 start=time.time()
 with (evidence/(name+'.log')).open('w') as log:
  result=subprocess.run(cmd,cwd=wt,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300)
 lines=(evidence/(name+'.log')).read_text(errors='replace').splitlines()
 summary=[l.strip() for l in lines if 'Executed ' in l or 'Build complete!' in l]
 results.append(dict(name=name,command=cmd,exit=result.returncode,seconds=time.time()-start,summary=summary[-5:]))
 (evidence/'validation-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results[-1]),flush=True)
