// Offline check of this deliverable. Uses the existing web validator; no render or Swift build.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../../..');
const file = path.join(__dirname, 'tre.candidate.skeleton.json');
const raw = fs.readFileSync(file, 'utf8');
const ctx = { window: {}, candidateJSON: raw };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'CellScaffold/Public/js/skeleton-runtime.js'), 'utf8'), ctx);
const validation = vm.runInContext('window.HavenSkeletonRuntime.validateSkeleton(JSON.parse(candidateJSON))', ctx);
const candidate = JSON.parse(raw);
const counts = {}, actions = new Set(), fields = new Set(), modifierValues = {};
let itemConditions = 0;
const allowed = {
  VStack: ['elements','spacing','modifiers'], HStack: ['elements','spacing','modifiers'],
  List: ['keypath','selectionMode','flowElementSkeleton','modifiers'],
  Text: ['text','keypath','modifiers'],
  Button: ['keypath','label','labelKeypath','payloadKeypath','payload','modifiers'],
  Spacer: ['width','modifiers']
};
const numeric = ['padding','width','height','cornerRadius','borderWidth','fontSize'];
const string = ['hAlignment','vAlignment','background','foregroundColor','borderColor','fontWeight','multilineTextAlignment'];
const boolean = ['maxWidthInfinity'];
function checkCondition(c) {
  if (c.allOf) return c.allOf.forEach(checkCondition);
  if (c.scope !== 'item' || typeof c.keypath !== 'string') throw new Error('Condition must read item data');
}
function visit(node, inRow = false) {
  const keys = Object.keys(node);
  if (keys.length !== 1) throw new Error('Expected canonical single wrapper');
  const type = keys[0], spec = node[type];
  if (!allowed[type]) throw new Error('Unexpected element '+type);
  for (const key of Object.keys(spec)) if (!allowed[type].includes(key)) throw new Error('Unexpected field '+type+'.'+key);
  counts[type] = (counts[type] || 0) + 1;
  for (const [k,v] of Object.entries(spec.modifiers || {})) {
    if (k === 'visibility') {
      if (!inRow) throw new Error('Top-level visibility');
      checkCondition(v.when); itemConditions++; continue;
    }
    if (numeric.includes(k)) { if (!Number.isFinite(v)) throw new Error('Non-number '+k); }
    else if (string.includes(k)) { if (typeof v !== 'string') throw new Error('Non-string '+k); }
    else if (boolean.includes(k)) { if (typeof v !== 'boolean') throw new Error('Non-bool '+k); }
    else if (k === 'lineLimit') { if (!Number.isInteger(v)) throw new Error('Non-int lineLimit'); }
    else throw new Error('Unexpected modifier '+k);
    (modifierValues[k] ||= new Set()).add(v);
  }
  if (type === 'Button') actions.add(spec.keypath);
  for (const [k,v] of Object.entries(spec)) if (/keypath$/i.test(k)) fields.add(v);
  if (type === 'List') {
    if (!spec.flowElementSkeleton?.VStack) throw new Error('Non-VStack row');
    visit(spec.flowElementSkeleton, true);
  }
  for (const child of spec.elements || []) visit(child, inRow);
}
visit(candidate);
if (raw.includes('KEYPATH-MANGLER')) throw new Error('Comment marker in JSON');
const scenario = JSON.parse(fs.readFileSync(path.join(__dirname, 'tre.preview.json'), 'utf8'));
if (path.resolve(__dirname, scenario.skeletonFile) !== file) throw new Error('Wrong scenario skeletonFile');
if (scenario.mode !== 'preview' || scenario.configurationName !== 'Co-Pilot Chat' || scenario.sourceCellEndpoint !== 'cell:///PersonalChatHub') throw new Error('Scenario target mismatch');
if (JSON.stringify(scenario.viewports) !== JSON.stringify([{name:'web',width:2000,height:1250},{name:'app',width:780,height:1688}])) throw new Error('Wrong viewports');
const keypathDoc = fs.readFileSync(path.join(__dirname, 'tre.keypaths.md'), 'utf8');
for (const f of fields) if (!keypathDoc.includes(f)) throw new Error('Undocumented keypath '+f);
const report = {
  candidate: path.relative(root,file),
  sha256: crypto.createHash('sha256').update(raw).digest('hex'),
  validator: 'CellScaffold/Public/js/skeleton-runtime.js:240',
  webStructuralValidation: validation,
  swiftSkeletonElementDecoder: 'NOT_RUN: no standalone build-free offline tool found in searched directories; builds forbidden',
  fieldTypeCheck: 'PASS: candidate subset checked against SkeletonDescription.swift:519,758,974,1240,1307,1407,1752; this script is not the Swift decoder',
  rootStateConditions: 0, itemConditions, elementCounts: counts,
  declaredActionKeypaths: [...actions].sort(),
  bindingKeypaths: [...fields].sort(),
  modifierValues: Object.fromEntries(Object.entries(modifierValues).map(([k,v])=>[k,[...v]])),
  runtimeExploreReachabilityAndPixelVerification: 'NOT_RUN',
  note: 'All helperTree contracts are proposed and missing. Static action extraction does not prove runtime reachability or action success.'
};
fs.writeFileSync(path.join(__dirname,'tre.validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if (!validation.valid) process.exitCode = 1;
