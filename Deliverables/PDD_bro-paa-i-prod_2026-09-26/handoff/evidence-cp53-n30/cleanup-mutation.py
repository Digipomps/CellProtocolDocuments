from pathlib import Path
import subprocess,hashlib,json
here=Path(__file__).resolve().parent
root=here.parents[4]/'CellProtocol/_wt-bro-kanal-auth-20260927'
p=root/'Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift'
fixed=p.read_bytes()
try:
    p.write_bytes(subprocess.check_output(['git','show','fea7db5:Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift'],cwd=root))
    subprocess.run(['python3',str(here/'verify.py'),'cleanup-before-fix','test','--filter','VaporWebSocketAdmissionTests/testRejectedPayloadRetainsAdmissionUntilSecurityAuditReturns|VaporWebSocketAdmissionTests/testConcurrentCloseRetainsGateSlotUntilResolverCleanupReturns'])
finally:
    p.write_bytes(fixed)
    (here/'cleanup-mutation-restoration.json').write_text(json.dumps(dict(baseline='fea7db567b006becc42f4766af94d81806a284f7',sha256_before=hashlib.sha256(fixed).hexdigest(),sha256_restored=hashlib.sha256(p.read_bytes()).hexdigest()),indent=2)+'\n')
