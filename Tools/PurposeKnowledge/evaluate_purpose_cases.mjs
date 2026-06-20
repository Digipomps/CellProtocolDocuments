#!/usr/bin/env node

import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";

const args = parseArgs(process.argv.slice(2));
const casesPath = args.cases ?? "Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl";
const outPath = args.out ?? "Tools/PurposeKnowledge/results/latest-purpose-eval.json";

const resolver = loadPurposeKnowledge({
  knowledgePath: args.knowledge ?? "Book/haven_purpose_knowledge_base_v0.json",
  indexPath: args.index ?? "Book/haven_purpose_knowledge_base_index_v0.json"
});

const cases = readJSONL(casesPath);
const results = cases.map((testCase) => evaluateCase(testCase, resolver.resolvePrompt(testCase.prompt, {
  visibleCapabilities: testCase.visibleCapabilities ?? []
})));

const passed = results.filter((result) => result.ok).length;
const report = {
  schema: "haven.purpose-knowledge-eval-report.v0",
  generatedAt: new Date().toISOString(),
  casesPath,
  caseCount: results.length,
  passed,
  failed: results.length - passed,
  passRate: results.length === 0 ? 0 : Math.round((passed / results.length) * 10000) / 100,
  byCategory: summarizeBy(results, "category"),
  bySource: summarizeBy(results, "source"),
  results
};

fs.writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(`${passed}/${results.length} passed (${report.passRate}%)`);
console.log(`wrote ${outPath}`);
if (report.failed > 0 && !args.allowFailures) {
  for (const result of results.filter((item) => !item.ok).slice(0, 12)) {
    console.error(`${result.id}: ${result.issues.join("; ")}`);
  }
  process.exit(1);
}

function evaluateCase(testCase, actual) {
  const expected = testCase.expected ?? {};
  const issues = [];
  const expanded = new Set(actual.expandedPurposeRefs ?? []);
  const top = new Set(actual.topPurposeRefs ?? []);
  const goals = new Set(actual.goalRefs ?? []);

  for (const ref of expected.mustIncludePurposeRefs ?? []) {
    if (!expanded.has(ref) && !top.has(ref)) issues.push(`missing purpose ${ref}`);
  }
  for (const ref of expected.mustTopPurposeRefs ?? []) {
    if (!top.has(ref)) issues.push(`missing top purpose ${ref}`);
  }
  for (const ref of expected.mustExcludePurposeRefs ?? []) {
    if (expanded.has(ref) || top.has(ref)) issues.push(`unexpected purpose ${ref}`);
  }
  for (const ref of expected.mustIncludeGoalRefs ?? []) {
    if (!goals.has(ref)) issues.push(`missing goal ${ref}`);
  }
  if (expected.nearestSharedPurposeRef && actual.nearestSharedPurposeRef !== expected.nearestSharedPurposeRef) {
    issues.push(`nearestSharedPurposeRef expected ${expected.nearestSharedPurposeRef} got ${actual.nearestSharedPurposeRef}`);
  }
  if (expected.status && actual.status !== expected.status) {
    issues.push(`status expected ${expected.status} got ${actual.status}`);
  }

  return {
    id: testCase.id,
    category: testCase.category ?? "uncategorized",
    source: testCase.source ?? "manual",
    ok: issues.length === 0,
    issues,
    prompt: testCase.prompt,
    expected,
    actual
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
  for (const result of results) {
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
