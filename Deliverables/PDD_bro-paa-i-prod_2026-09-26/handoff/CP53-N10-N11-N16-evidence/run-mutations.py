from pathlib import Path
import subprocess, os, json, hashlib
root=Path.cwd(); wt=root/'CellProtocol/_wt-bro-kanal-auth-20260927'; evidence=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N10-N11-N16-evidence'
guard=root/'_worktrees/rel-2026.9/CellScaffold-job-e-20260927/scripts/check_build_capacity.sh'
scanner=wt/'Sources/CellApple/EntityRadar/ScannerService.swift'; admission=wt/'Sources/CellApple/EntityRadar/ScannerAdmission.swift'
env=os.environ.copy();env.update(SWIFTPM_MODULECACHE_OVERRIDE='/private/tmp/cp53-module-cache',CLANG_MODULE_CACHE_PATH='/private/tmp/cp53-module-cache')
mutations=[('N10',scanner,'let prior = control ? nil : dispatchTail','let prior: Task<Void, Error>? = nil','ScannerPeerAuthenticationTests/testActualScannerSetupLobbyDescriptionAttachAndFeedForEitherInviter'),
 ('N11',scanner,'guard !stopped, let invitation = invitations[remoteUUID], invitation.state == .pending,','guard !stopped, let invitation = invitations[remoteUUID], _foundPeersDict[remoteUUID] == invitation.peer, invitation.state == .pending,','ScannerServiceInvitationTests'),
 ('N16',admission,'guard total.count - oldCount < budget.count, local.count - oldCount < budget.perSourceCount,\n                  bytes <= budget.bytes - (total.bytes - oldBytes), bytes <= budget.perSourceBytes - (local.bytes - oldBytes) else { return nil }','// MUTATION: no retained-count/byte admission.','ScannerAdmissionTests')]
results=[]
for name,path,old,new,filter in mutations:
 original=path.read_bytes();source=original.decode();assert source.count(old)==1
 with (evidence/f'mutation-{name}-capacity.log').open('w') as f:
  g=subprocess.run(['bash',str(guard),str(wt)],stdout=f,stderr=subprocess.STDOUT)
 if g.returncode: print('CAPACITY BLOCKED',flush=True);break
 try:
  path.write_text(source.replace(old,new))
  (evidence/f'mutation-{name}.diff').write_text(subprocess.run(['git','diff','--',str(path.relative_to(wt))],cwd=wt,capture_output=True,text=True).stdout)
  cmd=['swift','test','--disable-sandbox','--disable-automatic-resolution','--cache-path','/private/tmp/bro-swift-cache','--jobs','4','--filter',filter]
  with (evidence/f'mutation-{name}.log').open('w') as f: result=subprocess.run(cmd,cwd=wt,env=env,stdout=f,stderr=subprocess.STDOUT)
  results.append(dict(finding=name,command=cmd,exit=result.returncode,sha256=hashlib.sha256(original).hexdigest()))
  print(name,result.returncode,flush=True)
 finally:
  path.write_bytes(original)
  assert path.read_bytes()==original
(evidence/'mutation-results.json').write_text(json.dumps(results,indent=2)+'\n')
