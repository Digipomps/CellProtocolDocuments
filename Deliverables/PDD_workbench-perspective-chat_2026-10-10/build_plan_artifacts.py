from pathlib import Path
import json, re, hashlib, shutil, sys
ROOT=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT
def write(rel,value):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
std=re.findall(r'^\| (test\.[^ |]+) \|', (SOURCE/'FORMAALSSPEC.md').read_text(),re.M)
assert len(std)==len(set(std))==22
leaves=['events','continuity','perspectives','models','embedding','history','actions']
packages=[]
extras={
'events':['test.build','test.regression','test.cell.contract-fixtures','test.cell.auth-negative','test.cells.dataflow-matches-contracts'],
'continuity':['test.cell.auth-negative','test.regression'],
'perspectives':['test.cell.contract-fixtures','test.cell.auth-negative','test.cells.capability-audit'],
'models':['test.cell.auth-negative','test.cells.capability-audit'],
'embedding':['test.build','test.regression','test.gui.reference-image-exists','test.gui.parity','test.gui.load-time','test.skeleton.no-unreachable-elements','test.skeleton.purpose-actions-reachable','test.cell.contract-fixtures'],
'history':['test.cell.auth-negative','test.cell.contract-fixtures','test.gui.parity','test.skeleton.purpose-actions-reachable'],
'actions':['test.gui.parity','test.build','test.regression','test.docs-updated','test.status-current','test.cell.stub-scan','test.cells.capability-audit','test.skeleton.purpose-actions-reachable','test.end-to-end']}
artifacts={
'events':['contract/','dataflow.md','TESTRESULT.md#events'],
'continuity':['TESTRESULT.md#continuity','private-owner-export-reference'],
'perspectives':['TESTRESULT.md#perspectives','ACCEPT.md#packages'],
'models':['TESTRESULT.md#models','private-input-manifest-reference'],
'embedding':['TESTRESULT.md#embedding','TESTRESULT.md#load-time','ACCEPT.md#parity'],
'history':['TESTRESULT.md#history','contract/retention.json'],
'actions':['TESTRESULT.md#actions','TESTRESULT.md#end-to-end','ACCEPT.md','handoff/README.md']}
for i,leaf in enumerate(leaves,1):
 packages.append(dict(id=f'W{i}',purposeRef=f'purpose://candidate.workbench-perspective-chat.{leaf}',dependsOn=[f'W{x}' for x in range(1,i)],executor='Codex; authorized queue/environment executor for bounded runs',status='planned',tests=[f'test.{leaf}']+extras[leaf],artifacts=artifacts[leaf]))
write('plan.json',dict(schemaVersion='g2-plan-v1',date='2026-10-11',status='proposal-G2-pending',rootPurposeRef='purpose://candidate.workbench-perspective-chat.root',sourceSpec='FORMAALSSPEC.md',workPackages=packages,requiredTests=std,rootTest='test.end-to-end',firstUsableMilestone=['W1','W2','W3','W4','W5'],gates={'G1':'approved-2026-10-10','G1-GUI':'approved-2026-10-11','G2':'pending','G3':'pending'}))
def fields(required,rule): return {'required':required,'rule':rule}
contracts={
'command':fields(['schemaVersion','commandID','sessionID','expectedRevision','operation','input'],'Requester is resolved from authenticated context, never trusted from input. Duplicate commandID with different canonical payload hash is rejected. Mutations revalidate current authority.'),
'mountContext':fields(['sourceCellEndpoint','instanceID','componentID','revision'],'Separate authenticated host/transport context, not Meddle payload or authority. Server validates binding to session/source. Unsupported bridge fails closed.'),
'event':fields(['schemaVersion','eventID','aggregateID','revision','correlationID','causationID','occurredAt','purposeRefs','audience','type','payloadRef'],'Persist before publish. Emitter identity is verified through runtime source and authenticated envelope; a claimed event field is insufficient.'),
'commitReceipt':fields(['commandID','aggregateID','revision','eventIDs','durabilityStatus'],'Only committed means authoritative storage accepted. Chronicle/index projection cursors remain separate. Failure or unknown is not success.'),
'outbox':fields(['eventID','aggregateID','revision','deliveryState'],'Durable alongside authoritative commit or derived idempotently from journal. At-least-once delivery, deduplicate by eventID.'),
'eventNotification':fields(['eventID','aggregateID','revision','type'],'Flow may carry only a permitted minimal notice. Fetching payload requires same authorization. Do not broadcast private content/counts to shared listeners.'),
'snapshotCursor':fields(['aggregateID','revision','cursor','schemaVersion'],'Subscribe then snapshot and reconcile buffered events. eventsSince returns explicit gap/snapshot-required when history compacted; cursor opaque and scoped.'),
'packageRevision':fields(['packageID','revision','ownerRef','purposeRefs','instructionsRef','skillRefs','contextRefs','audience'],'Immutable published revision. Skills and context refs include version/hash. Package selection adds no grants.'),
'turnBinding':fields(['turnID','sessionID','packageID','packageRevision','routeID','providerID','modelID','inputManifestRef','purposeRefs','budgetRef'],'Immutable after dispatch; actual provider/model recorded in result, no silent fallback. Revocation checked before dispatch. Credentials remain protected references outside prompt.'),
'invocationReceipt':fields(['turnID','attemptID','state','sourceReceiptRef'],'State accepted/running/completed/failed/cancelRequested/cancelled/unknown must come from actual provider/adapter. Late response keeps original binding.'),
'actionProposal':fields(['proposalID','revision','proposalHash','actionKind','resourceBinding','requiredCapabilityRefs','inputSummary','purposeRefs'],'Preview is not approval. Bind target IDs/environment/PR SHAs; revalidate authority and fresh target at execution. Source/proposal text untrusted.'),
'effectAttempt':fields(['attemptID','commandID','proposalID','proposalHash','executorRef','state'],'Reserve durably before external await; allowed state transitions documented below. Query same ID after uncertainty; replay never dispatches.'),
'effectReceipt':fields(['attemptID','executorRef','sourceReceiptRef','state','resourceBinding'],'Only validated executor receipt may claim queue/running/merge/deploy outcome. No receipt from model prose or an imported generic done status.'),
'shareProjection':fields(['shareID','sourceRefs','selectedPayloadRef','audience','retentionPolicyRef'],'Explicit minimal copy with distinct ID/audience. Does not change private originals; revocation/deletion semantics explicit for this copy.'),
'query':fields(['scope','queryMode','query','limit'],'Authorized corpus before ranking/count/snippets, actual requester server-side. Modes text/purpose. Cursor/filter bound to same scope and grant epoch.'),
'historyResult':fields(['eventID','sourceRef','occurredAt','audience','projectionCursor'],'Only authorized payload/snippet. Open/model use revalidates. Index lag distinct from empty results; cached count/snippet/embedding inherits same boundary.'),
'migrationReceipt':fields(['migrationID','sourceRevision','targetSchemaVersion','mappingRef','checkpoint','inventoryDigest'],'Idempotent per source ID/revision. Private exports not in Git; legacy gaps explicitly marked, no invented text.'),
'releaseIntent':fields(['releaseID','artifactDigest','sourceSHA','environment','mandateRef','verificationRefs','rollbackRef'],'Only Admin/canonical deploy queue executor. Fresh claim/capacity check and staging evidence; a merged commit alone is not deployed.')}
operations=['selectPerspective','savePackage','selectModel','sendMessage','cancelTurn','proposeAction','executeProposal','shareSelection','searchHistory']
draftops=['savePackage','sendMessage','searchHistory']
write('contract/workbench-v1.json',dict(schemaVersion='proposal.workbench.v1',status='design-only-not-runtime-API',scope='Workbench integration; no global Meddle or FlowElement shape change implied',operations=operations,draftOperations=draftops,contracts=contracts,commandRules={'schemaVersion':1,'expectedRevision':'nonnegative integer','draftSnapshot':'Required for draft operations: mountInstanceID, fieldSequence, fieldKey, text; captured at button event, not inferred from global active state. Server validates against mountContext; package persistence has its own expectedPackageRevision.','legacyCompatibility':'Existing v0 callers remain behind explicit versioned adapter. Never infer a mounted caller session from legacy global selected state. Unknown wire version fails closed.'},effectTransitions={'reserved':['dispatched','denied','failed'],'dispatched':['accepted','unknown','failed'],'accepted':['running','completed','failed','cancelRequested','unknown'],'running':['completed','failed','cancelRequested','unknown'],'cancelRequested':['cancelled','completed','failed','unknown'],'unknown':['accepted','running','completed','failed','cancelled'],'completed':[],'denied':[],'failed':[],'cancelled':[]},effectTransitionRule='Transitions require authoritative evidence, including resolution from unknown. Replay reconstructs state only and never starts an attempt. A new attempt after terminal failure is separate, authorized and linked.',retentionContract='retention.json'))
write('contract/retention.json',dict(schemaVersion='proposal.retention.v1',status='policy-binding-design-not-a-new-default',beforeFirstPersistentWrite='Resolve and record an explicit existing owner/project policy per class. If absent, request that concrete owner choice and block affected persistent collection; G2 is not a retention choice.',classes=[
{'id':'private-chat-context','audience':'owner and explicit per-turn allowed recipient','policy':'existing owner policy; no new duration default','deletion':'payload, stored raw context, embeddings, snippets, caches; journal replay cannot restore deleted text','copies':'provider retention must be disclosed/accepted for selected route'},
{'id':'private-package','audience':'owner','policy':'existing owner package policy; explicit retained revisions','deletion':'package payload and derived context; active turn references retain only what its separate policy permits'},
{'id':'project-minimal-receipt','audience':'explicit project audience','policy':'explicit project evidence policy, separate from idea TTL','deletion':'only permitted minimal audit references can survive; never hide raw private payload in receipt','copies':'shared projection has own explicit audience and deletion policy'},
{'id':'derived-index-cache','audience':'no wider than source','policy':'derived; must not outlive source policy','deletion':'invalidate rights immediately, purge derived payload/embedding/cache; expose physical purge lag honestly'},
{'id':'migration-export','audience':'owner','policy':'explicit owner migration/recovery policy; no automatic source deletion','deletion':'owner-governed after proved migration/restore; never commit export to Git'}],ideaTTL='Existing idea TTL and dependency protection unchanged; not a retention policy for chat/receipts.'))
base={'schemaVersion':1,'commandID':'example-command-a','sessionID':'example-session-a','expectedRevision':8,'operation':'sendMessage','input':{'draftSnapshot':{'mountInstanceID':'mount-a','fieldSequence':3,'fieldKey':'message','text':'Eksempel fra montering A'},'packageID':'ideas','packageRevision':2}}
mount={'sourceCellEndpoint':'cell://localhost/example-helper','instanceID':'mount-a','componentID':'workbench.helper','revision':'v1'}
def variant(name,patch,valid,error=None):
 import copy
 c=copy.deepcopy(base);m=copy.deepcopy(mount);patch(c,m)
 return {'name':name,'command':c,'mountContext':m,'valid':valid,'expectedError':error}
fixtures=[variant('typed-send-mounted',lambda c,m:None,True),variant('second-mount-own-text',lambda c,m:(c.update(commandID='example-command-b'),m.update(instanceID='mount-b'),c['input']['draftSnapshot'].update(mountInstanceID='mount-b',text='Eksempel B',fieldSequence=4)),True),variant('missing-latest-text',lambda c,m:c['input'].pop('draftSnapshot'),False,'draft_required'),variant('wrong-mount',lambda c,m:m.update(instanceID='mount-b'),False,'draft_mount_mismatch'),variant('negative-revision',lambda c,m:c.update(expectedRevision=-1),False,'revision'),variant('unknown-operation',lambda c,m:c.update(operation='runArbitraryShell'),False,'operation'),variant('package-needs-own-revision',lambda c,m:c.update(operation='savePackage'),False,'package_revision'),variant('explicit-package-save',lambda c,m:(c.update(operation='savePackage'),c['input'].update(expectedPackageRevision=2)),True)]
write('contract/fixtures.json',{'status':'synthetic-design-examples-not-backend-tests','cases':fixtures,'runtimeOnlyCases':['unknown-command-id-reused-with-different-hash','revoked-requester','forged-emitter','write-applied-but-nil-return','duplicate-outbox-after-crash','provider-late-response','same-session-revision-race','replay-no-external-effects','search-count-and-snippet-cross-owner','stale-PR-head','unknown-submit-query-same-id']})
# Keep complete candidate coverage visible; exact binding is deliberately not invented before implementation.
actions=json.loads((SOURCE/'images/action-inventory.json').read_text())
domain_groups={
 'W1':[],
 'W3':['cancelShare','chooseContext','chooseSkills','inspectPackage','newPackage','packageDiff','preparePackageShare','savePackage','selectPerspective','selectShareAudience','setPackageInstructions','setPackagePurpose','setPackageTitle','sharePackageVersion','toggleContextSource','toggleSkill'],
 'W4':['confirmModelContext','inspectContext','reviewModelContext','selectModel','send','useLocalModel','useStarter'],
 'W5':['navigate','openAdmin','openDeveloper','openHistory','openPackages','openStandalone','setDraftMessage'],
 'W6':['openSource','prepareShare','searchHistory','setHistoryMode','setHistoryQuery','setHistoryScope'],
 'W7':['enqueue','followUp','inspectProposal','inspectRequirements','prepareAgentJob','readRepo','readCommandStatus']}
domain_map={'helper.'+key:wp for wp,keys in domain_groups.items() for key in keys}
assert set(domain_map)=={a['keypath'] for a in actions}
write('contract/gui-binding-inventory.json',{'status':'planned-not-implemented','allocationMeaning':'W5 owns host/Explore wiring; domainPackage allocates implementation responsibility, not a claim of existing support. Shared privacy checks apply to W3/W4/W6 alike.','source':'images/action-inventory.json','bindings':[{'keypath':a['keypath'],'ownerPackage':'W5','domainPackage':domain_map[a['keypath']],'status':'needs-Explore-or-host-binding-proof'} for a in actions]})
print('Created plan, proposed contracts, fixtures and complete candidate action inventory.')
