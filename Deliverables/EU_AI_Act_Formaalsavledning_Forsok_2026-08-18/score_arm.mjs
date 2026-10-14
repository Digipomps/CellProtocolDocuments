#!/usr/bin/env node
// Score one facet-declaration arm against the same ground truth as run B.
//
//   node score_arm.mjs <facets.json> [armName]
//
// The facets file may be either shape:
//   { "declarations": { "<purposeRef>": { domain, decisionEffect, ... } } }
//   { "<purposeRef>": { ... } }
//
// Beyond precision/recall this reports per-field agreement against the reference
// facet declaration, because the operative question is not only "did the arm get
// the classification right" but "which of the five fields is hardest to declare".

import fs from "node:fs";
import path from "node:path";

const dir = path.dirname(new URL(import.meta.url).pathname);
const read = (f) => JSON.parse(fs.readFileSync(path.isAbsolute(f) ? f : path.join(dir, f), "utf8"));

const armPath = process.argv[2];
const armName = process.argv[3] ?? path.basename(armPath ?? "arm", ".json");
if (!armPath) { console.error("usage: node score_arm.mjs <facets.json> [armName]"); process.exit(1); }

const kb = read("../../Book/haven_purpose_knowledge_base_v0.json");
const truth = read("ground_truth_v0.json").labels;
const reference = read("haven_purpose_regulatory_facets_v0.json").declarations;
const rawArm = read(armPath);
const arm = rawArm.declarations ?? rawArm;

const FIELDS = ["domain", "decisionEffect", "dataSubjects", "outputModality", "aiInvolvement"];
const FLAGS = ["allocatesTasksToPersons", "evaluatesPersonPerformance", "infersPersonalCharacteristics",
  "infersEmotion", "deducesSensitiveAttribute", "producesPersonScore", "publishedToPublic", "performsProfiling"];

const DOMAIN_TO_ANNEX = {
  biometrics: "III.1", "critical-infrastructure": "III.2", education: "III.3",
  employment: "III.4", "essential-services": "III.5", "law-enforcement": "III.6",
  "migration-border": "III.7", "justice-democracy": "III.8",
};

// Identical rules to run B in derive_ai_act_classification.mjs. Kept in sync by hand;
// if they drift, the arms are no longer comparable.
function runRules(f) {
  if (!f) return { refs: [], why: ["no declaration"] };
  const flags = f.flags ?? {};
  const refs = [], why = [];
  const modelInvolved = f.aiInvolvement === "model-assisted" || f.aiInvolvement === "model-generated";
  const modelGenerated = f.aiInvolvement === "model-generated";
  const toHuman = f.outputModality === "natural-language-to-human" || f.outputModality === "ui-render";

  if (modelInvolved && toHuman) { refs.push("50.1"); why.push(`50.1 <- ${f.aiInvolvement}/${f.outputModality}`); }
  if (modelGenerated && (f.outputModality === "natural-language-to-human" || f.outputModality === "synthetic-media")) { refs.push("50.2"); why.push("50.2 <- model-generated content leaves the system"); }
  if (f.outputModality === "synthetic-media" || (modelGenerated && flags.publishedToPublic)) { refs.push("50.4"); why.push("50.4 <- generated content published"); }
  if (f.domain === "biometrics" && (flags.infersEmotion || flags.deducesSensitiveAttribute)) refs.push("50.3");

  const annex = DOMAIN_TO_ANNEX[f.domain];
  if (annex) {
    let attaches = true;
    if (annex === "III.4") attaches = !!(flags.allocatesTasksToPersons || flags.evaluatesPersonPerformance);
    if (annex === "III.3") attaches = f.decisionEffect !== "none";
    if (annex === "III.5") attaches = f.decisionEffect === "automated-decision-with-legal-or-similar-effect";
    if (attaches) { refs.push(annex); why.push(`${annex} <- domain=${f.domain}`); }
  }
  if ((f.domain === "employment" || f.domain === "education") && flags.infersEmotion) refs.push("5.1.f");
  if (f.domain === "biometrics" && flags.deducesSensitiveAttribute) refs.push("5.1.g");
  if (flags.infersPersonalCharacteristics && f.dataSubjects !== "none") { refs.push("5.1.c"); why.push("5.1.c boundary <- infersPersonalCharacteristics"); }
  return { refs: [...new Set(refs)], why };
}

const expectedRefs = (ref) => {
  const e = truth[ref] ?? {};
  return [...(e.art50 ?? []), ...(e.annexIII ?? []), ...(e.prohibited ?? [])];
};

let tp = 0, fp = 0, fn = 0, exact = 0, missing = 0;
const strat = {};
const fieldAgree = Object.fromEntries([...FIELDS, "flags"].map((k) => [k, { same: 0, diff: 0, examples: [] }]));
const disagreements = [];
const confusion = Object.fromEntries(FIELDS.map((k) => [k, {}]));

for (const n of kb.nodes) {
  const ref = n.purposeRef;
  const a = arm[ref];
  if (!a) { missing += 1; continue; }
  const r = reference[ref];

  // per-field agreement against the reference declaration
  for (const k of FIELDS) {
    if (a[k] === r?.[k]) fieldAgree[k].same += 1;
    else {
      fieldAgree[k].diff += 1;
      if (fieldAgree[k].examples.length < 6) fieldAgree[k].examples.push(`${ref}: ref=${r?.[k]} arm=${a[k]}`);
      const key = `${r?.[k]} -> ${a[k]}`;
      confusion[k][key] = (confusion[k][key] ?? 0) + 1;
    }
  }
  const flagsEqual = FLAGS.every((k) => !!(a.flags ?? {})[k] === !!(r?.flags ?? {})[k]);
  flagsEqual ? fieldAgree.flags.same++ : fieldAgree.flags.diff++;

  // classification scoring
  const got = new Set(runRules(a).refs);
  const exp = expectedRefs(ref);
  const expSet = new Set(exp.map((x) => x.ref));
  const missHere = [...expSet].filter((x) => !got.has(x));
  const extraHere = [...got].filter((x) => !expSet.has(x));
  tp += [...expSet].filter((x) => got.has(x)).length;
  fn += missHere.length;
  fp += extraHere.length;
  if (!missHere.length && !extraHere.length) exact += 1;
  else disagreements.push({ purposeRef: ref, expected: [...expSet], got: [...got], missed: missHere, extra: extraHere });

  for (const item of exp) {
    const lab = item.label ?? "confirmed";
    strat[lab] ??= { expected: 0, found: 0 };
    strat[lab].expected += 1;
    if (got.has(item.ref)) strat[lab].found += 1;
  }
}

const precision = tp + fp ? tp / (tp + fp) : 1;
const recall = tp + fn ? tp / (tp + fn) : 1;
for (const k of Object.keys(strat)) strat[k].recall = +(strat[k].found / strat[k].expected).toFixed(3);
for (const k of Object.keys(fieldAgree)) {
  const t = fieldAgree[k].same + fieldAgree[k].diff;
  fieldAgree[k].agreement = t ? +(fieldAgree[k].same / t).toFixed(3) : null;
}

const out = {
  schema: "haven.regulatory-overlay.arm-result.v0",
  arm: armName,
  facetSource: armPath,
  nodesScored: kb.nodes.length - missing,
  nodesMissingDeclaration: missing,
  classification: {
    truePositives: tp, falsePositives: fp, falseNegatives: fn,
    precision: +precision.toFixed(3), recall: +recall.toFixed(3),
    f1: +((precision + recall) ? (2 * precision * recall) / (precision + recall) : 0).toFixed(3),
    nodesExactlyRight: exact, nodeAccuracy: +(exact / (kb.nodes.length - missing)).toFixed(3),
  },
  stratifiedRecallByLabelStrength: strat,
  perFieldAgreementVsReference: fieldAgree,
  confusionByField: confusion,
  disagreements,
};

fs.mkdirSync(path.join(dir, "results"), { recursive: true });
fs.writeFileSync(path.join(dir, `results/arm_${armName}.json`), JSON.stringify(out, null, 2) + "\n");

console.log(JSON.stringify({ ...out, disagreements: `${disagreements.length} (see results/arm_${armName}.json)`, confusionByField: undefined }, null, 2));
