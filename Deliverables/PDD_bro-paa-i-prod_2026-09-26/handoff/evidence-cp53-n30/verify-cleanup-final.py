from pathlib import Path
import subprocess,json,os
here=Path(__file__).resolve().parent
filter='EphemeralIdentityVaultConcurrencyTests|PublisherAsyncLifetimeTests|BridgeDescriptionConcurrencyTests|EntityScannerConsumerSecurityTests|ScannerNearbyInteractionTests|ScannerPeerAuthenticationTests|ScannerServiceInvitationTests|ScannerAdmissionTests|BridgePeerV3Tests|BridgePeerRecordLayerTests|BridgePeerFlowControlTests|BridgeMultiplexingTests|BridgeMuxSendLifetimeTests|BridgeResponseLifetimeTests|BridgeFeedAndRPCOrderingTests|BridgeFactoryLifetimeTests|BridgeSigningLifetimeTests|VaporWebSocketAdmissionTests|BridgeChannelWebSocketTests'
for name,args in [('final-build',['build']),('final-test',['test']),('final-tsan',['test','--sanitize','thread','--filter',filter])]:
    with (here/(name+'-summary.txt')).open('w') as out:
        result=subprocess.run(['python3',str(here/'verify.py'),name]+args,env=dict(os.environ,TSAN_OPTIONS='halt_on_error=1'),stdout=out,stderr=subprocess.STDOUT)
    lines=(here/(name+'.log')).read_text().splitlines()
    errors=[l for l in lines if ': error:' in l]
    known=['testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns','testLegacyEmbeddedPrivateKeyStillSigns','testScopedSecretDataStaysStableInUnsignedTestHost']
    if name=='final-test':
        assert result.returncode==1 and len(errors)==3 and all(any(k in l for k in known) for l in errors),errors
    else: assert result.returncode==0,result.returncode
    print(name, json.loads((here/(name+'-result.json')).read_text()),flush=True)
    print([l.strip() for l in lines if l.strip().startswith('Executed')][-1:],flush=True)
