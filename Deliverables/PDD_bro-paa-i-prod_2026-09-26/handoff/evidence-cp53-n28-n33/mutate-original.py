from pathlib import Path
import subprocess, hashlib, json, sys
here=Path(__file__).resolve().parent
root=here.parents[4]/'CellProtocol/_wt-bro-kanal-auth-20260927'
paths=['Sources/CellApple/EntityRadar/EntityScannerCell.swift','Sources/CellApple/EntityRadar/ScannerService.swift']
saved={p:(root/p).read_bytes() for p in paths}
def old(p): return subprocess.check_output(['git','show','e1e5e11:'+p],cwd=root).decode()
def method(s,start,end): return s[s.index(start):s.index(end,s.index(start))]
try:
 s=old(paths[0])
 s=s.replace('    private var peerStates = [String: NearbyPeerStateMachine]()','''    private var peerStates = [String: NearbyPeerStateMachine]()
    // Test-only access to original retained dictionaries; no behavior change.
    var retainedPeerStateForTesting: (states: Int, beacons: Int, overlaps: Int, bytes: Int) {
        (peerStates.count, peerBeacons.count, peerOverlaps.count, 0)
    }
    func configureProbeForTesting(_ policy: NearbyDisclosurePolicy) {
        disclosurePolicy = policy; localBeacon = policy.beacon
    }''')
 (root/paths[0]).write_text(s)
 s=saved[paths[1]].decode(); original=old(paths[1])
 for start,end in [('    func stop() {','    var pendingInvitationCount:'),('    func session(_ session: MCSession, peer peerID: MCPeerID, didChange state: MCSessionState) {','    public func connected()')]:
  s=s.replace(method(s,start,end),method(original,start,end))
 (root/paths[1]).write_text(s)
 (here/'original-mutation.patch').write_bytes(subprocess.check_output(['git','diff','--']+paths,cwd=root))
 result=subprocess.run([sys.executable,str(here/'verify.py'),'original-mutation','test','--filter','ScannerRetainedStateTests|EntityScannerConsumerSecurityTests/testOutgoingProbe'],stdout=subprocess.DEVNULL,timeout=180)
 print('original mutation exit',result.returncode,flush=True)
finally:
 for p,data in saved.items(): (root/p).write_bytes(data)
 (here/'mutation-restoration.json').write_text(json.dumps({p:{'before':hashlib.sha256(data).hexdigest(),'restored':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p,data in saved.items()},indent=2)+'\n')
