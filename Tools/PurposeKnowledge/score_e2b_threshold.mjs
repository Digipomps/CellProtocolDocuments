#!/usr/bin/env node
// E2b threshold sweep. Reads the calibration log (per-candidate P(YES)),
// splits cases into train/test (deterministic by index parity), sweeps a
// P(YES) threshold on train to maximize strict pass rate, then reports the
// held-out test pass rate at that threshold vs the naive t=0 (accept-any-YES)
// baseline. Selection assembly reuses the E2 winning pipeline: keep accepted
// refs as the purpose set (expandCoverage), derive the LCA from the confident
// core (top-2 accepted refs by resolver score). No API calls.

import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";

const logFile = process.argv[2] ?? mostRecent("e2b_calib_log_");
const outPath = process.argv[3] ?? "Tools/PurposeKnowledge/results/e2b_threshold_report.json";

const resolver = loadPurposeKnowledge({
  knowledgePath: "Book/haven_purpose_knowledge_base_v0.json",
  indexPath: "Book/haven_purpose_knowledge_base_index_v0.json"
});
const cases = new Map(readJSONL("Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl").map((c) => [c.id, c]));
const rows = readJSONL(logFile);

// case order for a stable train/test split
const caseOrder = [...new Set(rows.map((r) => r.caseID))];
const split = new Map(caseOrder.map((id, i) => [id, i % 5 < 3 ? "train" : "test"])); // 60/40

const models = [...new Set(rows.map((r) => r.model))];

function assemble(accepted, testCase) {
  let sel = accepted.map((a) => a.ref).filter((ref) => resolver.nodeByRef.has(ref));
  if (sel.length === 0) sel = ["purpose://prompt.unknown"];
  const expanded = resolver.expandCoverage(sel);
  const goalRefs = [...new Set(expanded.map((ref) => resolver.nodeByRef.get(ref)?.goal?.goalRef).filter(Boolean))];
  const core = [...accepted].sort((a, b) => (b.resolverScore ?? 0) - (a.resolverScore ?? 0)).slice(0, 2).map((a) => a.ref);
  const nearest = resolver.lowestCommonAncestor(resolver.primaryRefs(core.length ? core : sel)) ?? (core[0] ?? sel[0]);
  return { purposeRefs: sel, expandedPurposeRefs: expanded, goalRefs, nearestSharedPurposeRef: nearest,
    status: sel.length === 1 && sel[0] === "purpose://prompt.unknown" ? "unknown" : "resolved" };
}

function caseOK(testCase, out) {
  const exp = testCase.expected ?? {};
  const refs = new Set(out.expandedPurposeRefs);
  const goals = new Set(out.goalRefs);
  for (const r of exp.mustIncludePurposeRefs ?? []) if (!refs.has(r)) return false;
  for (const r of exp.mustExcludePurposeRefs ?? []) if (refs.has(r)) return false;
  for (const r of exp.mustIncludeGoalRefs ?? []) if (!goals.has(r)) return false;
  if (exp.nearestSharedPurposeRef && out.nearestSharedPurposeRef !== exp.nearestSharedPurposeRef) return false;
  if (exp.status && out.status !== exp.status) return false;
  return true;
}

function passRateAt(modelRows, threshold, subset) {
  const byCase = new Map();
  for (const r of modelRows) {
    if (!byCase.has(r.caseID)) byCase.set(r.caseID, []);
    byCase.get(r.caseID).push(r);
  }
  let pass = 0;
  let total = 0;
  for (const [caseID, candRows] of byCase) {
    if (subset && split.get(caseID) !== subset) continue;
    const testCase = cases.get(caseID);
    if (!testCase) continue;
    total += 1;
    const accepted = candRows.filter((r) => r.pYes >= threshold);
    if (caseOK(testCase, assemble(accepted, testCase))) pass += 1;
  }
  return { pass, total, rate: total ? Math.round((pass / total) * 1000) / 10 : 0 };
}

const thresholds = [];
for (let t = 0; t <= 0.95; t += 0.05) thresholds.push(Math.round(t * 100) / 100);

const report = { schema: "haven.e2b-threshold-report.v0", generatedAt: new Date().toISOString(), logFile, split: "60/40 by index%5", models: {} };
for (const model of models) {
  // choose best threshold on train
  let best = { threshold: 0, rate: -1 };
  const sweep = [];
  for (const t of thresholds) {
    const tr = passRateAt(rows.filter((r) => r.model === model), t, "train");
    sweep.push({ threshold: t, train: tr.rate });
    if (tr.rate > best.rate) best = { threshold: t, rate: tr.rate };
  }
  const naiveTest = passRateAt(rows.filter((r) => r.model === model), 0, "test");
  const calibTest = passRateAt(rows.filter((r) => r.model === model), best.threshold, "test");
  const naiveAll = passRateAt(rows.filter((r) => r.model === model), 0, null);
  const calibAll = passRateAt(rows.filter((r) => r.model === model), best.threshold, null);
  report.models[model] = {
    bestThreshold: best.threshold, trainRateAtBest: best.rate,
    testNaive: naiveTest, testCalibrated: calibTest,
    allNaive: naiveAll, allCalibrated: calibAll,
    sweep
  };
}

fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + "\n");
console.log(`wrote ${outPath}`);
for (const [model, m] of Object.entries(report.models)) {
  console.log(`${model}: t*=${m.bestThreshold} | test naive ${m.testNaive.rate}% -> calibrated ${m.testCalibrated.rate}% | all ${m.allNaive.rate}% -> ${m.allCalibrated.rate}%`);
}

function mostRecent(prefix) {
  const dir = "Tools/PurposeKnowledge/results";
  const files = fs.readdirSync(dir).filter((f) => f.startsWith(prefix)).sort();
  if (!files.length) throw new Error(`no ${prefix}* found`);
  return `${dir}/${files[files.length - 1]}`;
}
function readJSONL(path) {
  return fs.readFileSync(path, "utf8").split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith("#")).map((l) => JSON.parse(l));
}
