from pathlib import Path
import subprocess, sys, json, difflib, hashlib
root=Path('/Users/kjetil/Build/Digipomps/HAVEN')
wt=root/'CellProtocol/_wt-bro-kanal-auth-20260927'
ev=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N23-N26-evidence'
bridge=wt/'Sources/CellBase/Cells/Bridging'
paths={name:bridge/(name+'.swift') for name in ['BridgeBase','BridgeMultiplexing','BridgeChannelTransport','BridgeChannelClientOperation']}
original={name:p.read_text() for name,p in paths.items()}
results=[]
def replace(s,a,b):
 assert s.count(a)==1,(a,s.count(a))
 return s.replace(a,b)
mutations={}
mutations['N23']={'BridgeBase':replace(original['BridgeBase'],'''            guard channelSession === channelSessionValue else { throw BridgeChannelAuthentication.Failure.staleGeneration }
            try channelSession.checkInbound(command)
            // Re-read the registered operation under the lifecycle lock. A copy
            // returned before retirement/timeout conveys no publication rights.
            guard let commandRequest = auditor.loadBridgeCommandForCommandId(command.cid) else { return }''','''            let commandRequest = lookedUp // MUTATION: trust the pre-suspension copy''')}
mutations['N24']={'BridgeMultiplexing':replace(original['BridgeMultiplexing'],'previousSends == 0 else {','true else { // MUTATION: allow reuse while an old send is pending')}
mutations['N25']={'BridgeChannelTransport':replace(original['BridgeChannelTransport'],'''            let result = try await factory(self, session)
            try await adoptFactoryResult(result, peer: false)''','''            let result = try await factory(self, session)
            try session.check() // MUTATION: throw before taking cleanup ownership
            try await adoptFactoryResult(result, peer: false)'''),
'BridgeMultiplexing':replace(original['BridgeMultiplexing'],'''            let delegate = try await channelFactory(targetEndpoint, principal, channelTransport)
            // Own cleanup''','''            let delegate = try await channelFactory(targetEndpoint, principal, channelTransport)
            try channelSession.check() // MUTATION: unowned late result
            // Own cleanup''')}
s=original['BridgeBase'];a=s.index('        try Task.checkCancellation()',s.index('    private func validateOriginSigning'));b=s.index('        if let permit',a)
s=s[:a]+'''        let now = signingWallClock() // MUTATION: omit post-lookup challenge/deadline/cancellation checks
'''+s[b:]
mutations['N26']={'BridgeBase':s,'BridgeChannelClientOperation':replace(original['BridgeChannelClientOperation'],'''        // The vault lookup may suspend past either deadline without observing
        // cancellation. Revalidate the local permit at private-key admission.
        try validate(challenge, now: wallClock())
''','''        // MUTATION: sign immediately after the suspended existence lookup.
''')}
filters={'N23':'BridgeResponseLifetimeTests/testHeldAuditor','N24':'BridgeMuxSendLifetimeTests|BridgePeerV3Tests/testPeerMuxHeld','N25':'BridgeFactoryLifetimeTests','N26':'BridgeSigningLifetimeTests'}
try:
 for name,changes in mutations.items():
  patch=''
  for file,text in changes.items():
   patch+=''.join(difflib.unified_diff(original[file].splitlines(True),text.splitlines(True),fromfile=file,tofile=file+'-mutant'))
   paths[file].write_text(text)
  (ev/('mutation-'+name+'.diff')).write_text(patch)
  run=subprocess.run([sys.executable,'/private/tmp/cp53-n23-n26-run.py','mutation-'+name,'test','--filter',filters[name]],capture_output=True,text=True)
  (ev/('mutation-'+name+'-console.txt')).write_text(run.stdout+run.stderr)
  log=(ev/('mutation-'+name+'.log')).read_text(errors='replace') if (ev/('mutation-'+name+'.log')).exists() else ''
  assertions=[x for x in log.splitlines() if ': error:' in x and 'Tests.swift:' in x]
  result={'finding':name,'exit':run.returncode,'assertionFailures':len(assertions),'restored':False,'tests':filters[name]}
  for file in changes: paths[file].write_text(original[file])
  result['restored']=all(paths[file].read_text()==original[file] for file in changes)
  results.append(result);print(json.dumps(result),flush=True)
  (ev/'mutation-results.json').write_text(json.dumps(results,indent=2)+'\n')
  if run.returncode==75: sys.exit(75)
  if run.returncode!=1 or not assertions or 'error: Build failed' in log: sys.exit(1)
finally:
 for file,text in original.items(): paths[file].write_text(text)
 (ev/'mutation-restoration.json').write_text(json.dumps({file:{'restored':p.read_text()==original[file],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for file,p in paths.items()},indent=2)+'\n')
