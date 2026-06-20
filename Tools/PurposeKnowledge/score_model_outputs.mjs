#!/usr/bin/env node

import fs from "node:fs";

const args = parseArgs(process.argv.slice(2));
const casesPath = args.cases ?? "Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl";
const outputsPath = args.outputs;
const outPath = args.out ?? "Tools/PurposeKnowledge/results/latest-model-output-score.json";

if (!outputsPath) {
  console.error("Usage: node Tools/PurposeKnowledge/score_model_outputs.mjs --outputs path/to/model_outputs.jsonl");
  process.exit(2);
}

const cases = new Map(readJSONL(casesPath).map((item) => [item.id, item]));
const outputs = readJSONL(outputsPath);
const results = outputs.map((output) => scoreOutput(output, cases.get(output.id)));
const known = results.filter((result) => result.caseFound);
const passed = known.filter((result) => result.ok).length;
const report = {
  schema: "haven.purpose-model-output-score.v0",
  generatedAt: new Date().toISOString(),
  casesPath,
  outputsPath,
  outputCount: outputs.length,
  knownCaseCount: known.length,
  passed,
  failed: known.length - passed,
  passRate: known.length === 0 ? 0 : Math.round((passed / known.length) * 10000) / 100,
  byModel: summarizeBy(results, "model"),
  byCategory: summarizeBy(results, "category"),
  results
};

fs.writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(`${passed}/${known.length} known cases passed (${report.passRate}%)`);
console.log(`wrote ${outPath}`);
if (known.some((result) => !result.ok) && !args.allowFailures) {
  for (const result of known.filter((item) => !item.ok).slice(0, 12)) {
    console.error(`${result.id}: ${result.issues.join("; ")}`);
  }
  process.exit(1);
}

function scoreOutput(output, testCase) {
  if (!testCase) {
    return {
      id: output.id,
      model: output.model ?? "unknown-model",
      category: "unknown-case",
      caseFound: false,
      ok: false,
      issues: ["case id not found"],
      output
    };
  }

  const response = output.response ?? output;
  const expected = testCase.expected ?? {};
  const purposeRefs = new Set(response.expandedPurposeRefs ?? response.purposeRefs ?? response.topPurposeRefs ?? []);
  const goalRefs = new Set(response.goalRefs ?? []);
  const issues = [];

  for (const ref of expected.mustIncludePurposeRefs ?? []) {
    if (!purposeRefs.has(ref)) issues.push(`missing purpose ${ref}`);
  }
  for (const ref of expected.mustTopPurposeRefs ?? []) {
    const topRefs = new Set(response.topPurposeRefs ?? response.purposeRefs ?? []);
    if (!topRefs.has(ref)) issues.push(`missing top purpose ${ref}`);
  }
  for (const ref of expected.mustExcludePurposeRefs ?? []) {
    if (purposeRefs.has(ref)) issues.push(`unexpected purpose ${ref}`);
  }
  for (const ref of expected.mustIncludeGoalRefs ?? []) {
    if (!goalRefs.has(ref)) issues.push(`missing goal ${ref}`);
  }
  if (expected.nearestSharedPurposeRef && response.nearestSharedPurposeRef !== expected.nearestSharedPurposeRef) {
    issues.push(`nearestSharedPurposeRef expected ${expected.nearestSharedPurposeRef} got ${response.nearestSharedPurposeRef ?? "null"}`);
  }
  if (expected.status && response.status !== expected.status) {
    issues.push(`status expected ${expected.status} got ${response.status ?? "null"}`);
  }

  const unknownRefs = [...purposeRefs].filter((ref) => !String(ref).startsWith("purpose://"));
  for (const ref of unknownRefs) {
    issues.push(`invalid purpose ref ${ref}`);
  }

  return {
    id: testCase.id,
    model: output.model ?? response.model ?? "unknown-model",
    category: testCase.category ?? "uncategorized",
    source: testCase.source ?? "manual",
    caseFound: true,
    ok: issues.length === 0,
    issues,
    expected,
    response
  };
}

function readJSONL(path) {
  return fs.readFileSync(path, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((line, index) => {
      try {
        return JSON.parse(line);
      } catch (error) {
        throw new Error(`${path}:${index + 1}: ${error.message}`);
      }
    });
}

function summarizeBy(results, key) {
  const summary = {};
  for (const result of results.filter((item) => item.caseFound)) {
    const bucket = result[key] ?? "unknown";
    const current = summary[bucket] ?? { cases: 0, passed: 0, failed: 0, passRate: 0 };
    current.cases += 1;
    if (result.ok) current.passed += 1;
    else current.failed += 1;
    current.passRate = Math.round((current.passed / current.cases) * 10000) / 100;
    summary[bucket] = current;
  }
  return Object.fromEntries(Object.entries(summary).sort(([left], [right]) => left.localeCompare(right)));
}

function parseArgs(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--allow-failures") {
      result.allowFailures = true;
      continue;
    }
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    result[key] = argv[index + 1];
    index += 1;
  }
  return result;
}
