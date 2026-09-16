// Offline structural check using the repository's existing web validator.
// No browser, server, build, dependency install or Swift decoder is used.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../../..');
const runtimePath = path.join(root, 'CellScaffold/Public/js/skeleton-runtime.js');
const candidatePath = path.join(__dirname, 'chat.candidate.skeleton.json');
const source = fs.readFileSync(runtimePath, 'utf8');
const raw = fs.readFileSync(candidatePath, 'utf8');
const context = { window: {} };
vm.createContext(context);
vm.runInContext(source, context, { filename: runtimePath });
// Parse in the same realm because validateSkeleton checks object prototypes.
context.candidateJSON = raw;
const result = vm.runInContext('window.HavenSkeletonRuntime.validateSkeleton(JSON.parse(candidateJSON))', context);
const candidate = JSON.parse(raw);
const counts = {};
const actions = new Set();
let conditionCount = 0;
function visit(node, inRow = false) {
  const type = Object.keys(node)[0];
  const spec = node[type];
  counts[type] = (counts[type] || 0) + 1;
  if (spec.modifiers?.visibility) {
    conditionCount++;
    if (!inRow || spec.modifiers.visibility.when.scope !== 'item') throw new Error('Root-dependent condition');
  }
  if (['Button','TextArea'].includes(type)) {
    for (const k of ['keypath','targetKeypath','submitActionKeypath']) if (spec[k]) actions.add(spec[k]);
  }
  if (type === 'List') {
    if (!spec.flowElementSkeleton?.VStack) throw new Error('List row must be VStack');
    visit(spec.flowElementSkeleton, true);
  }
  for (const child of spec.elements || []) visit(child, inRow);
}
visit(candidate);
const scenario = JSON.parse(fs.readFileSync(path.join(__dirname, 'chat.preview.json'), 'utf8'));
if (!fs.existsSync(path.resolve(__dirname, scenario.skeletonFile))) throw new Error('Missing skeletonFile');
const report = {
  candidate: path.relative(root,candidatePath),
  sha256: crypto.createHash('sha256').update(raw).digest('hex'),
  validator: 'CellScaffold/Public/js/skeleton-runtime.js:240',
  webStructuralValidation: result,
  swiftSkeletonElementDecoder: 'NOT_RUN; no existing standalone offline decoder found in the requested tool directories; builds forbidden',
  rootStateConditions: 0,
  itemConditions: conditionCount,
  elementCounts: counts,
  declaredActionKeypaths: [...actions].sort(),
  note: 'Static extraction is not SkeletonReachabilityAudit and proves neither row presence nor successful actions. Modifier type/provenance checks were performed against source separately.'
};
fs.writeFileSync(path.join(__dirname,'chat.validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if (!result.valid) process.exitCode=1;
