#!/usr/bin/env node
// Score a v1 facet-declaration arm against the ground truth.
//
//   node score_arm_v1.mjs <facets.json> [armName]
//
// Changes from score_arm.mjs, all traceable to measured failures in arm B2:
//
//   1. systemKind gates classification. Only `capability` is classified; abstract
//      branches, facets, governance criteria and internal tests are skipped.
//   2. aiInvolvement is NOT read from the arm's declaration. It comes from
//      aiinvolvement_registry_v0.json, because arm B2 measured 0.579 agreement on
//      that field and the information is not present in purpose text at all.
//   3. The Annex III 4 flag is `supportsWorkAllocationOrMonitoring`, widened to
//      cover showing, tracking or supporting human allocation of work.
//   4. Results are reported twice: as-is, and with every declaration whose
//      confidence is not `high` routed to human review (counted as caught).
//
// Rules are otherwise identical to run B so the arms stay comparable.

import fs from "node:fs";
import path from "node:path";

const dir = path.dirname(new URL(import.meta.url).pathname);
const read = (f) => JSON.parse(fs.readFileSync(path.isAbsolute(f) ? f : path.join(dir, f), "utf8"));

const armPath = process.argv[2];
const armName = process.argv[3] ?? path.basename(armPath ?? "arm", ".json");
if (!armPath) { console.error("usage: node score_arm_v1.mjs <facets.json> [armName]"); process.exit(1); }

const kb = read("../../Book/haven_purpose_knowledge_base_v0.json");
const truth = read("ground_truth_v0.json").labels;
const registry = read("aiinvolvement_registry_v0.json");
const rawArm = read(armPath);
const arm = rawArm.declarations ?? rawArm;

const DOMAIN_TO_ANNEX = {
  biometrics: "III.1", "critical-infrastructure": "III.2", education: "III.3",
  employment: "III.4", "essential-services": "III.5", "law-enforcement": "III.6",
  "migration-border": "III.7", "justice-democracy": "III.8",
};

function runRules(ref, f) {
  if (!f) return { refs: [], why: ["no declaration"] };

  // (1) systemKind gate
  const kind = f.systemKind ?? "capability";
  if (kind !== "capability") return { refs: [], why: [`skipped: systemKind=${kind}`] };

  // (2) aiInvolvement from the registry, never from the declaration
  const aiInvolvement = registry.values[ref] ?? "none";

  const flags = f.flags ?? {};
  const refs = [], why = [];
  const modelInvolved = aiInvolvement === "model-assisted" || aiInvolvement === "model-generated";
  const modelGenerated = aiInvolvement === "model-generated";
  const toHuman = f.outputModality === "natural-language-to-human" || f.outputModality === "ui-render";

  if (modelInvolved && toHuman) { refs.push("50.1"); why.push(`50.1 <- registry:${aiInvolvement} + ${f.outputModality}`); }
  if (modelGenerated && (f.outputModality === "natural-language-to-human" || f.outputModality === "synthetic-media")) { refs.push("50.2"); why.push("50.2 <- model-generated content leaves the system"); }
  if (f.outputModality === "synthetic-media" || (modelGenerated && flags.publishedToPublic)) { refs.push("50.4"); why.push("50.4 <- generated content published"); }
  if (f.domain === "biometrics" && (flags.infersEmotion || flags.deducesSensitiveAttribute)) refs.push("50.3");

  const annex = DOMAIN_TO_ANNEX[f.domain];
  if (annex) {
    let attaches = true;
    // (3) widened flag
    if (annex === "III.4") attaches = !!(flags.supportsWorkAllocationOrMonitoring || flags.evaluatesPersonPerformance);
    if (annex === "III.3") attaches = f.decisionEffect !== "none";
    if (annex === "III.5") attaches = f.decisionEffect === "automated-decision-with-legal-or-similar-effect";
    if (attaches) { refs.push(annex); why.push(`${annex} <- domain=${f.domain}`); }
  }
  if ((f.domain === "employment" || f.domain === "education") && flags.infersEmotion) refs.push("5.1.f");
  if (f.domain === "biometrics" && flags.deducesSensitiveAttribute) refs.push("5.1.g");
  if (flags.infersPersonalCharacteristics && f.dataSubjects !== "none") { refs.push("5.1.c"); why.push("5.1.c boundary <- infersPersonalCharacteristics"); }
  return { refs: [...new Set(refs)], why };
}

const expectedOf = (ref) => {
  const e = truth[ref] ?? {};
  return [...(e.art50 ?? []), ...(e.annexIII ?? []), ...(e.prohibited ?? [])];
};

let tp = 0, fp = 0, fn = 0, exact = 0, missing = 0;
const strat = {};
const disagreements = [];
const routed = [];            // nodes sent to human review
let routedDuties = 0, routedCaught = 0;

for (const n of kb.nodes) {
  const ref = n.purposeRef;
  const a = arm[ref];
  if (!a) { missing += 1; continue; }

  const got = new Set(runRules(ref, a).refs);
  const exp = expectedOf(ref);
  const expSet = new Set(exp.map((x) => x.ref));
  const missed = [...expSet].filter((x) => !got.has(x));
  const extra = [...got].filter((x) => !expSet.has(x));

  tp += [...expSet].filter((x) => got.has(x)).length;
  fn += missed.length; fp += extra.length;
  if (!missed.length && !extra.length) exact += 1;
  else disagreements.push({ purposeRef: ref, expected: [...expSet], got: [...got], missed, extra, confidence: a.confidence });

  for (const item of exp) {
    const lab = item.label ?? "confirmed";
    strat[lab] ??= { expected: 0, found: 0 };
    strat[lab].expected += 1;
    if (got.has(item.ref)) strat[lab].found += 1;
  }

  // (4) confidence routing: a non-high declaration goes to a human, who is
  // assumed to resolve it. This is an assumption, not a measurement — it puts a
  // ceiling on what the routing policy can buy, not a guarantee.
  if (a.confidence !== "high") {
    routed.push(ref);
    routedDuties += expSet.size;
    routedCaught += missed.length;
  }
}

const totalExpected = tp + fn;
const precision = tp + fp ? tp / (tp + fp) : 1;
const recall = totalExpected ? tp / totalExpected : 1;
const recallWithRouting = totalExpected ? (tp + routedCaught) / totalExpected : 1;
for (const k of Object.keys(strat)) strat[k].recall = +(strat[k].found / strat[k].expected).toFixed(3);

const residual = disagreements.filter((d) => d.confidence === "high" && d.missed.length);

const out = {
  schema: "haven.regulatory-overlay.arm-result.v1",
  arm: armName,
  facetSource: armPath,
  aiInvolvementSource: { file: "aiinvolvement_registry_v0.json", status: registry.status, caveat: registry.consequence },
  nodesScored: kb.nodes.length - missing,
  nodesMissingDeclaration: missing,
  classification: {
    truePositives: tp, falsePositives: fp, falseNegatives: fn,
    precision: +precision.toFixed(3), recall: +recall.toFixed(3),
    f1: +((precision + recall) ? (2 * precision * recall) / (precision + recall) : 0).toFixed(3),
    nodesExactlyRight: exact, nodeAccuracy: +(exact / (kb.nodes.length - missing)).toFixed(3),
  },
  confidenceRouting: {
    nodesRoutedToHuman: routed.length,
    dutiesUnderRoutedNodes: routedDuties,
    missesRecoveredByRouting: routedCaught,
    recallAsIs: +recall.toFixed(3),
    recallWithRouting: +recallWithRouting.toFixed(3),
    assumption: "A human resolves every routed node correctly. Ceiling, not measurement.",
  },
  residualHighConfidenceMisses: residual,
  stratifiedRecallByLabelStrength: strat,
  disagreements,
};

fs.mkdirSync(path.join(dir, "results"), { recursive: true });
fs.writeFileSync(path.join(dir, `results/arm_${armName}.json`), JSON.stringify(out, null, 2) + "\n");
console.log(JSON.stringify({ ...out, disagreements: `${disagreements.length} (see file)` }, null, 2));
