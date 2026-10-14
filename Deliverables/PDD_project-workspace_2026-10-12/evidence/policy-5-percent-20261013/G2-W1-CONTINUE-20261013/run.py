from pathlib import Path
import datetime, hashlib, json, os, re, resource, signal, subprocess, sys, time
HERE=Path(__file__).resolve().parent
H=Path.home()/'Build/Digipomps/HAVEN'
CS=Path.home()/'.codex/worktrees/workbench-navigation-contrast/CellScaffold'
CP=H/'_worktrees/codex-workbench-entity-journal-20261012'
JOB='g2-w1-entity-continue-20261013'
sys.dont_write_bytecode=True
from workbench_xctest_receipt import validate_xctest
import owned_process
from command_control import run_owned_command, install_interrupt_handlers, deferred_cleanup_interruptions
M=json.loads((HERE/'manifest.json').read_text())

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(root,*args): return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
def verify():
 for label,root in [('cp',CP),('cs',CS)]:
  m=M[label]
  assert git(root,'rev-parse','HEAD')==m['base'],label+' base changed'
  assert git(root,'branch','--show-current')==m['branch'],label+' branch changed'
  assert git(root,'status','--porcelain','--untracked-files=all')==m['status'],label+' worktree changed'
  for name,sha in m['files'].items(): assert digest(root/name)==sha,label+': '+name
 for name,sha in M['scripts'].items(): assert digest(HERE/name)==sha,name+' changed'
 approval=H/'CellProtocolDocuments/Deliverables/PDD_workbench-perspective-chat_2026-10-10/evidence/entity-retest-approval-20261012.json'
 assert digest(approval)==M['approvalSHA256'],'approval changed'
 print('INPUT VERIFIED: CP candidate + unchanged 17 consumer tests + remote pins + runner',flush=True)

def authorize_continuation():
 a=json.loads((HERE/'AUTHORIZATION.json').read_text())
 assert a['jobID']==JOB and a['approved'] is True,'continuation not authorized'
 assert a['source']=='Kjetil user message' and a['userWords'].strip(),'missing explicit user word'
 assert a['manifestSHA256']==digest(HERE/'manifest.json'),'authorization targets another packet'

def admitted():
 a=json.loads((HERE/'ADMISSION.json').read_text())
 assert a['jobID']==JOB and a['coordinator']=='Deploy prosjekt køadministrasjon'
 assert a['exclusiveBuildWindow'] is True
 expiry=datetime.datetime.fromisoformat(a['expiresAt'])
 assert datetime.datetime.now(datetime.timezone.utc)<expiry,'admission expired'
 q=H/'_losen-queue'
 foreign=[p.name for p in (q/'running').glob('*.job') if p.name!=JOB+'.job']
 waiting=[p.name for lane in q.glob('inbox*') for p in lane.glob('*.job') if p.name!=JOB+'.job']
 assert not foreign and not waiting,('queue occupied',foreign,waiting)
 print('ADMISSION VERIFIED: exclusive coordinated window',flush=True)

group_confirmed=True
interruptions=[]
def command(argv,cwd,env,log,timeout=3600):
 global group_confirmed
 group_confirmed=False
 children=[]
 try:
  with log.open('w') as output:
   return run_owned_command(argv, owner=owned_process, cwd=cwd, env=env,
      stdout=output, stderr=subprocess.STDOUT, timeout=timeout, started=children.append)
 finally:
  # Only the primitive's explicit reap-after-proof permits restoration.
  group_confirmed=not children or children[0].anchor_reaped

def check_tests(log,expected):
 return validate_xctest(log.read_text(errors='replace'),expected,0)

def pins_compatible(root,label):
 before=json.loads((HERE/(label+'-Package.resolved.before')).read_bytes())
 after_path=root/'Package.resolved'
 after=after_path.read_bytes() if after_path.exists() else b''
 (HERE/(label+'-Package.resolved.after')).write_bytes(after)
 assert after,'Package.resolved disappeared'
 a={p['identity']:p for p in json.loads(after)['pins']}
 b={p['identity']:p for p in before['pins']}
 removed=set(b)-set(a)
 assert not(set(a)-set(b)) and all(a[k]==b[k] for k in a),label+' unrelated dependency drift'
 assert not removed or (label=='cs' and removed=={'cellprotocol'}),label+' unexpected pin removal'

def main():
 global group_confirmed
 verify()
 if sys.argv[1]=='check':
  print('CHECK ONLY: no Swift, no admission claim, no writes.');sys.exit(0)
 authorize_continuation()
 admitted()
 env={k:os.environ[k] for k in ('HOME','USER','LOGNAME','TMPDIR') if k in os.environ}
 env.update(PATH='/usr/bin:/bin:/usr/sbin:/sbin', LC_ALL='C')
 for key in ('CELLPROTOCOL_LOCAL_PACKAGE_PATH','DIMYMINT_LOCAL_PACKAGE_PATH','DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH','CELLPROTOCOL_PUBLISHED_API','HAVEN_SWIFTPM_CACHE_KEY','TEST_ISOLATION','CELL_SCAFFOLD_TEST_ISOLATION'):
  env.pop(key,None)
 env.update(HAVEN_BUILD_MIN_FREE_PERCENT='10',HAVEN_BUILD_MIN_FREE_GIB='40',HAVEN_BUILD_RESERVE_GIB='10',HAVEN_SWIFTPM_JOBS='2',HAVEN_SWIFTPM_RUNNER=str(HERE/'report-only-swiftpm.sh'),HAVEN_SWIFTPM_WAIT_SECONDS='60',HAVEN_SWIFTPM_CACHE_ROOT='/private/tmp/haven-swiftpm-bounded')
 # Admission and capacity precede consumption of the single test attempt.
 subprocess.run(['/bin/bash',str(CS/'scripts/check_build_capacity.sh'),str(CS)],env=env,check=True)
 (HERE/'attempt-started').mkdir()
 resource.setrlimit(resource.RLIMIT_FSIZE,(resource.RLIM_INFINITY,resource.getrlimit(resource.RLIMIT_FSIZE)[1]))
 install_interrupt_handlers(interruptions)
 original={root:(root/'Package.resolved').read_bytes() for root in (CP,CS)}
 for label,root in [('cp',CP),('cs',CS)]: (HERE/(label+'-Package.resolved.before')).write_bytes(original[root])
 result={'jobID':JOB,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phases':[],'status':'running'}
 rc=1
 try:
  for label,root,filter_,expected in [('cp',CP,'EntityAnchorLegacyBatchAuthorityTests',M['cpTests']),('cs',CS,'Workbench(SessionJournal|EntityJournalBoundary)Tests',M['csTests'])]:
   phase_env=dict(env)
   if label=='cp': phase_env['HAVEN_SWIFTPM_CACHE_KEY']='workbench-entity-journal-cp'
   else: phase_env['CELLPROTOCOL_LOCAL_PACKAGE_PATH']=str(CP)
   args=['/bin/bash',str(CS/'scripts/run_swift_bounded.sh'),'test']
   args+=['--disable-automatic-resolution'] if label=='cp' else ['--skip-update']
   args+=['--filter',filter_]
   log=HERE/(label+'-tests.log')
   print('START '+label+' (two jobs, managed cache)',flush=True)
   status=command(args,root,phase_env,log)
   (HERE/(label+'-exit-code.txt')).write_text(str(status)+'\n')
   phase={'phase':label,'exitCode':status,'log':log.name}
   result['phases'].append(phase)
   assert status==0,label+' failed; dependent test chain stopped'
   phase['passedTests']=check_tests(log,expected)
   pins_compatible(root,label)
   if label=='cs':
    prefixes=re.findall(r'running swift test with cache ([0-9a-f]+)',log.read_text())
    assert len(prefixes)==1,'cache evidence missing'
    states=list(Path('/private/tmp/haven-swiftpm-bounded/caches').glob(prefixes[0]+'*/workspace-state.json'))
    assert len(states)==1,'workspace-state missing'
    state=json.loads(states[0].read_bytes())
    matches=[d for d in state['object']['dependencies'] if d.get('packageRef',{}).get('location')==str(CP)]
    assert len(matches)==1 and matches[0]['state']['name']=='fileSystem','candidate local dependency not proved'
    (HERE/'consumer-local-dependency.json').write_text(json.dumps(matches[0],indent=2)+'\n')
   print('PASS '+label+': '+str(len(expected))+' expected tests',flush=True)
  result['status']='passed';rc=0
 except BaseException as e:
  result['status']='stopped';result['reason']=str(e);print('STOP: '+str(e),flush=True)
 finally:
  with deferred_cleanup_interruptions() as cleanup_interruptions:
   # Preserve post-run resolution bytes even when compilation/tests failed.
   for label,root in [('cp',CP),('cs',CS)]:
    p=root/'Package.resolved'
    (HERE/(label+'-Package.resolved.after')).write_bytes(p.read_bytes() if p.exists() else b'')
    if not p.exists(): result[label+'ResolutionMissing']=True
   if group_confirmed:
    for root,data in original.items():
     p=root/'Package.resolved'
     if not p.exists() or p.read_bytes()!=data: p.write_bytes(data)
    try: verify()
    except BaseException as e: result['postcheckError']=str(e);result['status']='stopped';rc=1
   else:
    result['postcheckError']='Process group termination unconfirmed; resolution files preserved for inspection, no restore attempted'
    result['status']='stopped';rc=1
  
   if interruptions or cleanup_interruptions:
    result['interruptions']=interruptions+cleanup_interruptions;result['status']='stopped';rc=1
   result['finishedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat()
   result['exitCode']=rc
   (HERE/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
   (HERE/'exit-code.txt').write_text(str(rc)+'\n')
   print('G2_W1_CONTINUE_TERMINAL '+json.dumps(result,ensure_ascii=False),flush=True)
 sys.exit(rc)

if __name__=="__main__": main()
