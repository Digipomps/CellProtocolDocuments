#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";

const TOOL_DIR = "Tools/PurposeKnowledge";
const RESULTS_DIR = `${TOOL_DIR}/results`;
const CASES_PATH = `${TOOL_DIR}/fixtures/purpose_eval_cases.v0.jsonl`;
const INPUT_PATH = `${RESULTS_DIR}/e3_input.json`;
const APPLE_PATH = `${RESULTS_DIR}/e3_apple_answers.jsonl`;
const OUTPUTS_PATH = `${RESULTS_DIR}/e3b_deterministic_lca_outputs.jsonl`;
const REPORT_PATH = `${RESULTS_DIR}/e3b_deterministic_lca_report.json`;

const resolver = loadPurposeKnowledge({
  knowledgePath: "Book/haven_purpose_knowledge_base_v0.json",
  indexPath: "Book/haven_purpose_knowledge_base_index_v0.json"
});

const cases = new Map(readJSONL(CASES_PATH).map((item) => [item.id, item]));
const e3Input = JSON.parse(fs.readFileSync(INPUT_PATH, "utf8"));
const candidateCases = e3Input.filter((item) => (item.candidates ?? []).length > 0);
const eligibleIDs = candidateCases.map((item) => item.id).sort();
const splitByID = new Map(eligibleIDs.map((id, index) => [id, index % 5 >= 3 ? "test" : "train"]));
const inputByID = new Map(candidateCases.map((item) => [item.id, item]));
const zeroCandidateCases = e3Input.filter((item) => (item.candidates ?? []).length === 0);

assert(eligibleIDs.length === 50, `expected 50 eligible cases, found ${eligibleIDs.length}`);
assert([...splitByID.values()].filter((split) => split === "train").length === 30, "expected 30 train cases");
assert([...splitByID.values()].filter((split) => split === "test").length === 20, "expected 20 test cases");

const appleRows = readJSONL(APPLE_PATH).map((row) => ({ ...row, model: "apple-fm-3b" }));
const e2LogPaths = fs.readdirSync(RESULTS_DIR)
  .filter((name) => /^e2_micro_log_.*\.jsonl$/.test(name))
  .sort()
  .map((name) => `${RESULTS_DIR}/${name}`);
const e2Rows = deduplicateRows(e2LogPaths.flatMap(readJSONL));

const lanes = [
  {
    id: "apple-fm-3b",
    source: APPLE_PATH,
    rows: appleRows,
    isPositive: (row) => String(row.answer).toLowerCase() === "yes"
  },
  {
    id: "ministral-3b-2512",
    source: e2LogPaths.join(","),
    rows: e2Rows.filter((row) => row.model === "ministral-3b-2512"),
    isPositive: (row) => row.answer === "YES"
  },
  {
    id: "Qwen3-8B",
    source: e2LogPaths.join(","),
    rows: e2Rows.filter((row) => row.model === "Qwen3-8B"),
    isPositive: (row) => row.answer === "YES"
  },
  {
    id: "gpt-5.5",
    source: e2LogPaths.join(","),
    rows: e2Rows.filter((row) => row.model === "gpt-5.5"),
    isPositive: (row) => row.answer === "YES"
  }
];

const policies = [
  {
    id: "legacy_core2",
    description: "All positive model verdicts; LCA from the two highest resolver-score positives.",
    assemble: ({ positives, native }) => assemble(positives, legacyCoreLCA(positives), native)
  },
  {
    id: "legacy_gate8_core2",
    description: "Prior E3 score gate: positive verdicts with resolver score >= 8, one-positive fallback; LCA from top two.",
    assemble: ({ positives, native }) => {
      const gated = positives.filter((row) => row.resolverScore >= 8);
      const selected = gated.length ? gated : positives.slice(0, 1);
      return assemble(selected, legacyCoreLCA(selected), native);
    }
  },
  {
    id: "prompt_evidence_lca",
    description: "All positive model verdicts; LCA from the deterministic prompt resolver, independent of model over-selection.",
    assemble: ({ positives, native }) => assemble(positives, nativeLCA(native, positives), native)
  },
  {
    id: "constrained_multiselect",
    description: "Keep positive candidates supported by the resolver's native coverage; use native prompt-evidence LCA and a native-top fallback only when no compatible positive remains.",
    assemble: ({ positives, native }) => {
      const nativeCoverage = new Set(native.expandedPurposeRefs ?? []);
      let selected = positives.filter((row) => nativeCoverage.has(row.ref));
      if (!selected.length && native.status === "resolved") {
        selected = (native.topPurposeRefs ?? []).map((ref) => candidateRow(ref, native));
      }
      return assemble(selected, nativeLCA(native, selected), native);
    }
  },
  {
    id: "resolver_only_ceiling",
    description: "Deterministic resolver output without model verdicts; a coupled benchmark ceiling, not independent generalization evidence.",
    assemble: ({ native }) => {
      const selected = (native.topPurposeRefs ?? []).map((ref) => candidateRow(ref, native));
      return assemble(selected, nativeLCA(native, selected), native);
    }
  }
];

const rowsByLaneCase = new Map();
for (const lane of lanes) {
  const grouped = groupBy(lane.rows, (row) => row.caseID);
  for (const id of eligibleIDs) {
    const input = inputByID.get(id);
    const scoreByRef = new Map((input.candidates ?? []).map((candidate) => [candidate.ref, candidate.resolverScore]));
    const laneRows = (grouped.get(id) ?? []).map((row) => ({
      ...row,
      resolverScore: row.resolverScore ?? scoreByRef.get(row.ref) ?? 0
    }));
    assert(laneRows.length === input.candidates.length, `${lane.id}/${id}: expected ${input.candidates.length} candidate rows, found ${laneRows.length}`);
    rowsByLaneCase.set(`${lane.id}\u0000${id}`, laneRows);
  }
}

const outputRows = [];
const evaluations = [];
for (const lane of lanes) {
  for (const id of eligibleIDs) {
    const testCase = cases.get(id);
    assert(testCase, `missing fixture case ${id}`);
    const input = inputByID.get(id);
    const modelRows = rowsByLaneCase.get(`${lane.id}\u0000${id}`);
    const positives = modelRows.filter(lane.isPositive).sort(compareCandidateRows);
    const native = resolver.resolvePrompt(testCase.prompt, {});

    for (const policy of policies) {
      const response = policy.assemble({ positives, native, input, testCase });
      const evaluation = scoreResponse(testCase, response);
      const split = splitByID.get(id);
      const positiveRefs = new Set(positives.map((row) => row.ref));
      const selectedRefs = new Set(response.topPurposeRefs);
      outputRows.push({
        id,
        model: `${lane.id}#${policy.id}`,
        split,
        response
      });
      evaluations.push({
        id,
        split,
        lane: lane.id,
        policy: policy.id,
        positiveCount: positives.length,
        selectedCount: response.topPurposeRefs.length,
        modelPositiveSelectedCount: [...selectedRefs].filter((ref) => positiveRefs.has(ref)).length,
        droppedPositiveCount: [...positiveRefs].filter((ref) => !selectedRefs.has(ref)).length,
        deterministicAddedCount: [...selectedRefs].filter((ref) => !positiveRefs.has(ref)).length,
        nearestSharedPurposeRef: response.nearestSharedPurposeRef,
        ...evaluation
      });
    }
  }
}

const metrics = {};
for (const lane of lanes) {
  metrics[lane.id] = {};
  for (const policy of policies) {
    const relevant = evaluations.filter((item) => item.lane === lane.id && item.policy === policy.id);
    metrics[lane.id][policy.id] = {
      train: summarize(relevant.filter((item) => item.split === "train")),
      test: summarize(relevant.filter((item) => item.split === "test")),
      all: summarize(relevant)
    };
  }
}

const zeroCandidateEvaluations = zeroCandidateCases.map((input, index) => {
  const testCase = cases.get(input.id);
  assert(testCase, `missing zero-candidate fixture case ${input.id}`);
  const native = resolver.resolvePrompt(testCase.prompt, {});
  const selected = (native.topPurposeRefs ?? []).map((ref) => candidateRow(ref, native));
  const response = assemble(selected, nativeLCA(native, selected), native);
  return {
    id: input.id,
    fixtureIndex: e3Input.findIndex((item) => item.id === input.id),
    splitByFullFixtureOrder: e3Input.findIndex((item) => item.id === input.id) % 5 >= 3 ? "test" : "train",
    candidateCount: 0,
    positiveCount: 0,
    selectedCount: response.topPurposeRefs.length,
    modelPositiveSelectedCount: 0,
    droppedPositiveCount: 0,
    deterministicAddedCount: response.topPurposeRefs.length,
    response,
    ...scoreResponse(testCase, response)
  };
});

const report = {
  schema: "haven.e3b-deterministic-selection-lca.v0",
  generatedAt: new Date().toISOString(),
  objective: "Test parameter-free deterministic selection/LCA policies on frozen E2-E4 model verdicts.",
  protocol: {
    eligibleCaseRule: "e3_input case has at least one resolver candidate",
    ordering: "lexicographic case ID order",
    split: "index % 5 >= 3 is test; otherwise train",
    eligibleCaseCount: eligibleIDs.length,
    zeroCandidateCaseCount: zeroCandidateCases.length,
    trainCaseCount: 30,
    testCaseCount: 20,
    splitIDHash: sha256Text(eligibleIDs.map((id) => `${id}\t${splitByID.get(id)}`).join("\n") + "\n"),
    testExpectedFieldsUsedForPolicyChoice: false,
    priorHeldOutAggregateResultsKnown: true,
    parameterTuning: "none; gate 8 appears only as the frozen legacy E3 comparator",
    evaluationOrder: "Policies are declared before scoreResponse reads any expected labels.",
    note: "This ordering reproduces the published Apple gate-8 held-out baseline. File order does not."
  },
  inputs: {
    cases: fileRecord(CASES_PATH),
    e3Input: fileRecord(INPUT_PATH),
    appleAnswers: fileRecord(APPLE_PATH),
    e2Logs: e2LogPaths.map(fileRecord)
  },
  lanes: lanes.map((lane) => ({ id: lane.id, candidateRows: lane.rows.length, source: lane.source })),
  policies: policies.map(({ id, description }) => ({ id, description })),
  metrics,
  pairedTestChanges: Object.fromEntries(lanes.map((lane) => [lane.id, pairedChanges(lane.id)])),
  pairedVsPublishedBaseline: Object.fromEntries(lanes.map((lane) => [lane.id, pairedVsPublishedBaseline(lane.id)])),
  zeroCandidateControls: {
    purpose: "Six cases had no model shortlist/verdict rows and are outside the 50-case E2-E4 comparison. They are checked separately through the deterministic unknown/negation path.",
    summary: summarize(zeroCandidateEvaluations),
    perCase: zeroCandidateEvaluations
  },
  caveats: [
    "The purpose resolver and the 56-case fixture were co-developed; resolver-backed gains are not independent out-of-distribution evidence.",
    "The same held-out split was evaluated in E2-E4 and its aggregate failure pattern motivated this work; it is reused hold-out, not a fresh blind test.",
    "Only 20 eligible cases are in the held-out split, so one case equals five percentage points.",
    "Frozen model verdicts isolate deterministic assembly; this run does not measure latency or fresh generation variance.",
    "resolver_only_ceiling intentionally removes the model and must not be described as model improvement."
  ],
  perCase: evaluations
};

fs.writeFileSync(OUTPUTS_PATH, outputRows.map((row) => JSON.stringify(row)).join("\n") + "\n");
fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2) + "\n");

console.log(`wrote ${OUTPUTS_PATH}`);
console.log(`wrote ${REPORT_PATH}`);
console.log("held-out strict pass rates:");
for (const lane of lanes) {
  const values = policies.map((policy) => `${policy.id}=${metrics[lane.id][policy.id].test.strict.passRate}%`);
  console.log(`  ${lane.id}: ${values.join(" | ")}`);
}

function assemble(selectedRows, nearestSharedPurposeRef, native) {
  let refs = stableUnique(selectedRows.map((row) => row.ref).filter((ref) => resolver.nodeByRef.has(ref)));
  if (!refs.length) refs = ["purpose://prompt.unknown"];
  const expandedPurposeRefs = resolver.expandCoverage(refs);
  const goalRefs = stableUnique(expandedPurposeRefs
    .map((ref) => resolver.nodeByRef.get(ref)?.goal?.goalRef)
    .filter(Boolean));
  const isUnknown = refs.length === 1 && refs[0] === "purpose://prompt.unknown";
  return {
    schema: "haven.purpose-model-output.v0",
    status: isUnknown ? "unknown" : "resolved",
    purposeRefs: refs,
    topPurposeRefs: refs,
    expandedPurposeRefs,
    goalRefs,
    nearestSharedPurposeRef: nearestSharedPurposeRef ?? (isUnknown ? "purpose://prompt.unknown" : native.nearestSharedPurposeRef ?? refs[0])
  };
}

function legacyCoreLCA(selectedRows) {
  const core = selectedRows.slice().sort(compareCandidateRows).slice(0, 2).map((row) => row.ref);
  if (!core.length) return "purpose://prompt.unknown";
  return resolver.lowestCommonAncestor(resolver.primaryRefs(core)) ?? core[0];
}

function nativeLCA(native, selectedRows) {
  if (native.status === "resolved" && native.nearestSharedPurposeRef) return native.nearestSharedPurposeRef;
  return legacyCoreLCA(selectedRows);
}

function candidateRow(ref, native) {
  const ranked = (native.ranked ?? []).find((item) => item.purposeRef === ref);
  return { ref, resolverScore: ranked?.score ?? 0, answer: "DETERMINISTIC" };
}

function scoreResponse(testCase, response) {
  const expected = testCase.expected ?? {};
  const purposes = new Set(response.expandedPurposeRefs ?? []);
  const goals = new Set(response.goalRefs ?? []);
  const included = (expected.mustIncludePurposeRefs ?? []).every((ref) => purposes.has(ref));
  const excluded = (expected.mustExcludePurposeRefs ?? []).every((ref) => !purposes.has(ref));
  const goalsOK = (expected.mustIncludeGoalRefs ?? []).every((ref) => goals.has(ref));
  const lcaOK = !expected.nearestSharedPurposeRef || response.nearestSharedPurposeRef === expected.nearestSharedPurposeRef;
  const statusOK = !expected.status || response.status === expected.status;
  const validRefs = [...purposes].every((ref) => resolver.nodeByRef.has(ref));
  const selection = included && excluded;
  const strict = selection && goalsOK && lcaOK && statusOK && validRefs;
  return { strict, selection, included, excluded, goalsOK, lcaOK, statusOK, validRefs };
}

function summarize(items) {
  const metricNames = ["strict", "selection", "included", "excluded", "goalsOK", "lcaOK", "statusOK", "validRefs"];
  const result = { cases: items.length };
  for (const name of metricNames) {
    const passed = items.filter((item) => item[name]).length;
    result[name] = { passed, failed: items.length - passed, passRate: rate(passed, items.length) };
  }
  result.averagePositiveCount = average(items.map((item) => item.positiveCount));
  result.averageSelectedCount = average(items.map((item) => item.selectedCount));
  result.totalDroppedPositiveCount = items.reduce((sum, item) => sum + item.droppedPositiveCount, 0);
  result.totalDeterministicAddedCount = items.reduce((sum, item) => sum + item.deterministicAddedCount, 0);
  return result;
}

function pairedChanges(laneID) {
  const baseline = new Map(evaluations
    .filter((item) => item.lane === laneID && item.policy === "legacy_core2" && item.split === "test")
    .map((item) => [item.id, item.strict]));
  const result = {};
  for (const policy of policies.filter((item) => item.id !== "legacy_core2")) {
    let wins = 0;
    let losses = 0;
    let ties = 0;
    for (const item of evaluations.filter((candidate) => candidate.lane === laneID && candidate.policy === policy.id && candidate.split === "test")) {
      const before = baseline.get(item.id);
      if (!before && item.strict) wins += 1;
      else if (before && !item.strict) losses += 1;
      else ties += 1;
    }
    result[policy.id] = { wins, losses, ties };
  }
  return result;
}

function pairedVsPublishedBaseline(laneID) {
  const baselinePolicy = laneID === "apple-fm-3b" ? "legacy_gate8_core2" : "legacy_core2";
  const baseline = new Map(evaluations
    .filter((item) => item.lane === laneID && item.policy === baselinePolicy && item.split === "test")
    .map((item) => [item.id, item.strict]));
  const result = { baselinePolicy, comparisons: {} };
  for (const policyID of ["prompt_evidence_lca", "constrained_multiselect"]) {
    let wins = 0;
    let losses = 0;
    let ties = 0;
    for (const item of evaluations.filter((candidate) => candidate.lane === laneID && candidate.policy === policyID && candidate.split === "test")) {
      const before = baseline.get(item.id);
      if (!before && item.strict) wins += 1;
      else if (before && !item.strict) losses += 1;
      else ties += 1;
    }
    result.comparisons[policyID] = { wins, losses, ties };
  }
  return result;
}

function deduplicateRows(rows) {
  const byKey = new Map();
  for (const row of rows) byKey.set(`${row.model}\u0000${row.caseID}\u0000${row.ref}`, row);
  return [...byKey.values()];
}

function compareCandidateRows(left, right) {
  return (right.resolverScore ?? 0) - (left.resolverScore ?? 0) || String(left.ref).localeCompare(String(right.ref));
}

function groupBy(items, keyFor) {
  const result = new Map();
  for (const item of items) {
    const key = keyFor(item);
    if (!result.has(key)) result.set(key, []);
    result.get(key).push(item);
  }
  return result;
}

function readJSONL(filePath) {
  return fs.readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((line) => JSON.parse(line));
}

function fileRecord(filePath) {
  const data = fs.readFileSync(filePath);
  return { path: filePath, bytes: data.length, sha256: crypto.createHash("sha256").update(data).digest("hex") };
}

function sha256Text(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function stableUnique(values) {
  return [...new Set(values)];
}

function rate(passed, total) {
  return total ? Math.round((passed / total) * 1000) / 10 : 0;
}

function average(values) {
  return values.length ? Math.round((values.reduce((sum, value) => sum + value, 0) / values.length) * 100) / 100 : 0;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
