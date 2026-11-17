// Offline: call the repository web structural validator, without a browser or build.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../../..');
const runtimePath = path.join(root, 'CellScaffold/Public/js/skeleton-runtime.js');
const schemaPath = path.join(root, 'CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift');
const schema = fs.readFileSync(schemaPath, 'utf8');
const modifierSource = schema.split('public struct SkeletonModifiers: Codable {')[1].split('public init() {}')[0];
const modifierTypes = new Map([...modifierSource.matchAll(/public var (\w+): ([^\n?]+)\?/g)].map(m => [m[1],m[2].trim()]));
const raw = fs.readFileSync(path.join(__dirname,'flate.candidate.skeleton.json'),'utf8');
const context = {window:{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(runtimePath,'utf8'),context,{filename:runtimePath});
context.candidateJSON = raw;
const structural = vm.runInContext('window.HavenSkeletonRuntime.validateSkeleton(JSON.parse(candidateJSON))',context);
const elementCounts = {};
const buttonActions = new Set(), dropActions = new Set();
let itemConditions = 0, modifiersChecked = 0;
function visit(node,inRow=false) {
  const [kind] = Object.keys(node);
  const value = node[kind];
  elementCounts[kind] = (elementCounts[kind] || 0) + 1;
  if (value.modifiers) {
    for (const [name,val] of Object.entries(value.modifiers)) {
      const type = modifierTypes.get(name);
      if (!type) throw new Error('Unknown modifier: '+name);
      if (type === 'Double' && (typeof val !== 'number' || !Number.isFinite(val))) throw new Error('Not Double: '+name);
      if (type === 'String' && typeof val !== 'string') throw new Error('Not String: '+name);
      if (type === 'Bool' && typeof val !== 'boolean') throw new Error('Not Bool: '+name);
      if (type === '[String]' && (!Array.isArray(val) || val.some(x => typeof x !== 'string'))) throw new Error('Not [String]: '+name);
      modifiersChecked++;
    }
    if (value.modifiers.visibility) {
      if (!inRow || value.modifiers.visibility.when.scope !== 'item') throw new Error('Root/context condition present');
      itemConditions++;
    }
    if (value.modifiers.dropActionKeypath) dropActions.add(value.modifiers.dropActionKeypath);
  }
  if (kind === 'Button') buttonActions.add(value.keypath);
  if (kind === 'List') {
    if (!value.flowElementSkeleton?.VStack) throw new Error('List row must be canonical VStack');
    visit(value.flowElementSkeleton,true);
  }
  for (const child of value.elements || []) visit(child,inRow);
}
visit(JSON.parse(raw));
if (raw.includes('KEYPATH-MANGLER:')) throw new Error('Missing-keypath marker in JSON');
const scenario = JSON.parse(fs.readFileSync(path.join(__dirname,'flate.preview.json'),'utf8'));
if (scenario.mode !== 'preview' || scenario.configurationName !== 'Co-Pilot Chat' || scenario.sourceCellEndpoint !== 'cell:///PersonalChatHub') throw new Error('Scenario contract mismatch');
if (!fs.existsSync(path.resolve(__dirname,scenario.skeletonFile))) throw new Error('skeletonFile missing');
if (JSON.stringify(scenario.viewports) !== JSON.stringify([{name:'web',width:2000,height:1250},{name:'app',width:780,height:1688}])) throw new Error('Viewport mismatch');
const report = {
  candidate:'CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/skjelett/flate.candidate.skeleton.json',
  sha256:crypto.createHash('sha256').update(raw).digest('hex'),
  validator:'CellScaffold/Public/js/skeleton-runtime.js:240',
  webStructuralValidation:structural,
  swiftSkeletonElementDecoder:'NOT_RUN — JSON er ikke kontrollert mot dekoderen',
  modifierNamesAndPrimitiveTypes:'Checked against current SkeletonModifiers declarations; not a Swift decode',
  modifiersChecked,
  rootStateConditions:0,
  itemConditions,
  elementCounts,
  declaredButtonActions:[...buttonActions].sort(),
  declaredDropActions:[...dropActions].sort(),
  scenarioStructure:'PASS; runtime data contracts incomplete',
  runtimePreview:'NOT_RUN — network excluded by task',
  note:'No Explore manifest, native decoder, reachability audit, live actions or pixel comparison was run.'
};
fs.writeFileSync(path.join(__dirname,'flate.validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if (!structural.valid) process.exitCode=1;
