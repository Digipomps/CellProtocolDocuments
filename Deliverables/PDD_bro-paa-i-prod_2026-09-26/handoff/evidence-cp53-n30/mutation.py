from pathlib import Path
import subprocess, hashlib, json
here=Path(__file__).resolve().parent
root=here.parents[4]/'CellProtocol/_wt-bro-kanal-auth-20260927'
p=root/'Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift'
fixed=p.read_bytes()
source=fixed.decode()
original=subprocess.check_output(['git','show','dab8106:Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift'],cwd=root,text=True)
start='    private func setupWebSocketCallbacks(on webSocket: WebSocket) {'
old=original[original.index(start):original.index('    func handleWebSocketClose')]
a=source.index(start); b=source.index('    /// Count/bytes are reserved', a)
mutated=source[:a]+old+'\n'+source[b:]
try:
    p.write_text(mutated)
    (here/'original-callback-mutation.patch').write_text(subprocess.check_output(['git','diff','--','Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift'],cwd=root,text=True))
    result=subprocess.run(['python3',str(here/'verify.py'),'original-callback-mutation','test','--filter','VaporWebSocketAdmissionTests/testAuthenticatedFeedOrderSurvivesHeldFirstDispatchAndMixedTextBinaryBurst|VaporWebSocketAdmissionTests/testDefaultAdaptersUseTheSameProcessWideBudget'])
finally:
    p.write_bytes(fixed)
    (here/'mutation-restoration.json').write_text(json.dumps(dict(sha256_before=hashlib.sha256(fixed).hexdigest(),sha256_restored=hashlib.sha256(p.read_bytes()).hexdigest()),indent=2)+'\n')
