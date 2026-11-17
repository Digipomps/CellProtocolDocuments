#!/usr/bin/env node
// Research harness: can an EU AI Act classification be DERIVED from a HAVEN purpose declaration?
//
// Run A: lexical derivation from the free text that already exists in the knowledge base.
// Run B: rule derivation from five declared structured facets (the proposed schema addition).
// Both are scored against the same hand-authored ground truth.
//
// This tool does not write to Book/. It is isolated by construction.

import fs from "node:fs";
import path from "node:path";

const dir = path.dirname(new URL(import.meta.url).pathname);
const read = (f) => JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));

const kb = read("../../Book/haven_purpose_knowledge_base_v0.json");
const overlay = read("eu_ai_act_overlay_v0.json");
const facets = read("haven_purpose_regulatory_facets_v0.json").declarations;
const truth = read("ground_truth_v0.json").labels;

// ---------------------------------------------------------------- normalisation
// Same normalisation as Tools/PurposeKnowledge/derive_purpose_index.mjs, so run A
// measures the real index behaviour rather than a stricter or looser variant.
const normalize = (v) =>
  String(v ?? "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/æ/g, "ae").replace(/ø/g, "o").replace(/å/g, "a")
    .replace(/[^a-z0-9:/._-]+/g, " ")
    .trim().replace(/\s+/g, " ");

const tokens = (v) => normalize(v).split(/[\s:/._-]+/).filter((t) => t.length >= 3);

function nodeBlob(n) {
  const g = n.goal ?? {};
  return [
    n.title, n.summary, g.outcome,
    ...(g.successSignals ?? []),
    ...(n.interests ?? []),
    ...(n.matchingHints?.aliases ?? []),
    ...(n.matchingHints?.tokens ?? []),
  ].join(" ");
}

// ---------------------------------------------------------------- run A: lexical
// Score each HAVEN node against each overlay node's statutory tokens.
// IDF-weighted so that generic tokens ("system", "data", "risk") count for less,
// which is the most favourable reasonable setup for the lexical hypothesis.
const kbNodes = kb.nodes;
const docTokenSets = new Map(kbNodes.map((n) => [n.purposeRef, new Set(tokens(nodeBlob(n)))]));

const df = new Map();
for (const set of docTokenSets.values()) {
  for (const t of set) df.set(t, (df.get(t) ?? 0) + 1);
}
const N = kbNodes.length;
const idf = (t) => Math.log((N + 1) / ((df.get(t) ?? 0) + 1));

const LEXICAL_THRESHOLD = Number(process.env.LEX_THRESHOLD ?? 0.6);

function runLexical(ref) {
  const set = docTokenSets.get(ref);
  const hits = [];
  for (const o of overlay.nodes) {
    const trig = (o.triggerTokens ?? []).flatMap((t) => tokens(t));
    if (!trig.length) continue;
    let score = 0, matched = [];
    for (const t of new Set(trig)) {
      if (set.has(t)) { score += idf(t); matched.push(t); }
    }
    const norm = score / Math.sqrt(new Set(trig).size);
    if (norm >= LEXICAL_THRESHOLD) hits.push({ ref: o.ref, score: +norm.toFixed(3), matched });
  }
  return hits.sort((a, b) => b.score - a.score);
}

// ---------------------------------------------------------------- run B: rules
const OVERLAY_TO_SHORT = {
  "purpose://regulatory.eu-ai-act.transparency.ai-interaction": "50.1",
  "purpose://regulatory.eu-ai-act.transparency.synthetic-content-marking": "50.2",
  "purpose://regulatory.eu-ai-act.transparency.emotion-biometric-notice": "50.3",
  "purpose://regulatory.eu-ai-act.transparency.deepfake-and-public-interest-text": "50.4",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.1.biometrics": "III.1",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.2.critical-infrastructure": "III.2",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.3.education": "III.3",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.4.employment": "III.4",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.5.essential-services": "III.5",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.6.law-enforcement": "III.6",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.7.migration-border": "III.7",
  "purpose://regulatory.eu-ai-act.high-risk.annex-iii.8.justice-democracy": "III.8",
  "purpose://regulatory.eu-ai-act.prohibited.emotion-inference-work-education": "5.1.f",
  "purpose://regulatory.eu-ai-act.prohibited.biometric-categorisation-sensitive": "5.1.g",
  "purpose://regulatory.eu-ai-act.prohibited.social-scoring": "5.1.c",
};
const SHORT_OF = (r) => OVERLAY_TO_SHORT[r] ?? r;

const DOMAIN_TO_ANNEX = {
  biometrics: "III.1", "critical-infrastructure": "III.2", education: "III.3",
  employment: "III.4", "essential-services": "III.5", "law-enforcement": "III.6",
  "migration-border": "III.7", "justice-democracy": "III.8",
};

function runRules(ref) {
  const f = facets[ref];
  if (!f) return { art50: [], annexIII: [], prohibited: [], skipped: "no facet declaration" };
  const flags = f.flags ?? {};
  const art50 = [], annexIII = [], prohibited = [], why = [];

  const modelInvolved = f.aiInvolvement === "model-assisted" || f.aiInvolvement === "model-generated";
  const modelGenerated = f.aiInvolvement === "model-generated";
  const toHuman = f.outputModality === "natural-language-to-human" || f.outputModality === "ui-render";

  if (modelInvolved && toHuman) {
    art50.push({ ref: "50.1", label: "confirmed" });
    why.push("50.1: aiInvolvement=" + f.aiInvolvement + " and outputModality=" + f.outputModality);
  }
  if (modelGenerated && (f.outputModality === "natural-language-to-human" || f.outputModality === "synthetic-media")) {
    art50.push({ ref: "50.2", label: "confirmed" });
    why.push("50.2: model-generated content leaves the system");
  }
  if (f.outputModality === "synthetic-media" || (modelGenerated && flags.publishedToPublic)) {
    art50.push({ ref: "50.4", label: "confirmed" });
    why.push("50.4: generated content published to the public");
  }
  if (f.domain === "biometrics" && (flags.infersEmotion || flags.deducesSensitiveAttribute)) {
    art50.push({ ref: "50.3", label: "confirmed" });
  }

  // Annex III by declared domain, then the Article 6(3) derogation test.
  const annex = DOMAIN_TO_ANNEX[f.domain];
  if (annex) {
    let attaches = true;
    if (annex === "III.4") attaches = !!(flags.allocatesTasksToPersons || flags.evaluatesPersonPerformance);
    if (annex === "III.3") attaches = f.decisionEffect !== "none";
    if (annex === "III.5") attaches = f.decisionEffect === "automated-decision-with-legal-or-similar-effect";
    if (attaches) {
      const derogationCandidate =
        f.decisionEffect === "informational" && !flags.performsProfiling;
      annexIII.push({
        ref: annex,
        label: "conditional",
        article6_3: derogationCandidate ? "derogation-candidate" : "no-derogation",
      });
      why.push(`${annex}: domain=${f.domain}` + (derogationCandidate ? " (art.6(3) derogation candidate, still surfaced)" : ""));
    }
  }

  if ((f.domain === "employment" || f.domain === "education") && flags.infersEmotion) {
    prohibited.push({ ref: "5.1.f", label: "confirmed" });
  }
  if (f.domain === "biometrics" && flags.deducesSensitiveAttribute) {
    prohibited.push({ ref: "5.1.g", label: "confirmed" });
  }
  if (flags.infersPersonalCharacteristics && f.dataSubjects !== "none") {
    prohibited.push({ ref: "5.1.c", label: "boundary" });
    why.push("5.1.c boundary: declares inference of personal characteristics");
  }

  return { art50, annexIII, prohibited, why };
}

// ---------------------------------------------------------------- scoring
// A prediction counts as a hit if the duty reference matches. Label strength
// (confirmed / conditional / boundary) is reported separately, because a
// classifier that downgrades a confirmed duty to conditional has still surfaced it.
function refsOf(list) { return new Set((list ?? []).map((x) => SHORT_OF(x.ref ?? x))); }

function scoreOne(predicted, expected) {
  const p = new Set([...refsOf(predicted.art50), ...refsOf(predicted.annexIII), ...refsOf(predicted.prohibited)]);
  const e = new Set([...refsOf(expected.art50), ...refsOf(expected.annexIII), ...refsOf(expected.prohibited)]);
  const tp = [...e].filter((x) => p.has(x));
  const fp = [...p].filter((x) => !e.has(x));
  const fn = [...e].filter((x) => !p.has(x));
  return { tp, fp, fn };
}

function aggregate(rows) {
  let tp = 0, fp = 0, fn = 0, exact = 0;
  for (const r of rows) {
    tp += r.tp.length; fp += r.fp.length; fn += r.fn.length;
    if (!r.fp.length && !r.fn.length) exact += 1;
  }
  const precision = tp + fp ? tp / (tp + fp) : 1;
  const recall = tp + fn ? tp / (tp + fn) : 1;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return {
    truePositives: tp, falsePositives: fp, falseNegatives: fn,
    precision: +precision.toFixed(3), recall: +recall.toFixed(3), f1: +f1.toFixed(3),
    nodesExactlyRight: exact, nodesTotal: rows.length,
    nodeAccuracy: +(exact / rows.length).toFixed(3),
  };
}

// ---------------------------------------------------------------- execute
const rowsA = [], rowsB = [], detail = [];

for (const n of kbNodes) {
  const ref = n.purposeRef;
  const expected = truth[ref] ?? { art50: [], annexIII: [], prohibited: [] };

  const lexHits = runLexical(ref);
  const predA = { art50: [], annexIII: [], prohibited: [] };
  for (const h of lexHits) {
    const s = SHORT_OF(h.ref);
    if (s.startsWith("50.")) predA.art50.push({ ref: s });
    else if (s.startsWith("III.")) predA.annexIII.push({ ref: s });
    else if (s.startsWith("5.")) predA.prohibited.push({ ref: s });
    else predA.annexIII.push({ ref: s });
  }

  const predB = runRules(ref);

  const sa = scoreOne(predA, expected);
  const sb = scoreOne(predB, expected);
  rowsA.push(sa); rowsB.push(sb);

  detail.push({
    purposeRef: ref,
    expected: [...refsOf(expected.art50), ...refsOf(expected.annexIII), ...refsOf(expected.prohibited)],
    runA: { predicted: [...refsOf(predA.art50), ...refsOf(predA.annexIII), ...refsOf(predA.prohibited)], fp: sa.fp, fn: sa.fn, topLexical: lexHits.slice(0, 3) },
    runB: { predicted: [...refsOf(predB.art50), ...refsOf(predB.annexIII), ...refsOf(predB.prohibited)], fp: sb.fp, fn: sb.fn, why: predB.why ?? [] },
  });
}

const summary = {
  schema: "haven.regulatory-overlay.experiment-result.v0",
  ranAt: process.env.RUN_STAMP ?? "see report",
  lexicalThreshold: LEXICAL_THRESHOLD,
  overlayNodes: overlay.nodes.length,
  havenNodes: kbNodes.length,
  runA_lexical: aggregate(rowsA),
  runB_declaredFacets: aggregate(rowsB),
};

fs.mkdirSync(path.join(dir, "results"), { recursive: true });
fs.writeFileSync(path.join(dir, "results/summary.json"), JSON.stringify(summary, null, 2) + "\n");
fs.writeFileSync(path.join(dir, "results/detail.json"), JSON.stringify(detail, null, 2) + "\n");

console.log(JSON.stringify(summary, null, 2));
console.log("\n--- run A worst false positives (lexical) ---");
for (const d of detail.filter((d) => d.runA.fp.length).sort((a, b) => b.runA.fp.length - a.runA.fp.length).slice(0, 12)) {
  console.log(`${d.purposeRef}\n    FP: ${d.runA.fp.join(", ")}\n    via: ${d.runA.topLexical.map((h) => SHORT_OF(h.ref) + "[" + h.matched.slice(0, 6).join("|") + "]").join("  ")}`);
}
console.log("\n--- run B disagreements ---");
for (const d of detail.filter((d) => d.runB.fp.length || d.runB.fn.length)) {
  console.log(`${d.purposeRef}\n    expected: ${d.expected.join(", ") || "(none)"}\n    got:      ${d.runB.predicted.join(", ") || "(none)"}\n    FP: ${d.runB.fp.join(", ") || "-"}   FN: ${d.runB.fn.join(", ") || "-"}`);
}

// ---------------------------------------------------------------- stratified view
// The aggregate hides the finding that matters. Split by ground-truth label strength.
function strata(rows, kind) {
  const out = {};
  for (const n of kbNodes) {
    const e = truth[n.purposeRef] ?? {};
    for (const group of ["art50", "annexIII", "prohibited"]) {
      for (const item of e[group] ?? []) {
        const lab = item.label ?? "confirmed";
        out[lab] ??= { expected: 0, found: 0 };
        out[lab].expected += 1;
        const d = detail.find((d) => d.purposeRef === n.purposeRef);
        const pred = kind === "A" ? d.runA.predicted : d.runB.predicted;
        if (pred.includes(SHORT_OF(item.ref))) out[lab].found += 1;
      }
    }
  }
  for (const k of Object.keys(out)) out[k].recall = +(out[k].found / out[k].expected).toFixed(3);
  return out;
}

const stratified = { runA_lexical: strata(rowsA, "A"), runB_declaredFacets: strata(rowsB, "B") };

// Threshold sweep for run A, so the result cannot be blamed on one bad cutoff.
const sweep = [];
for (const th of [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0]) {
  const rows = kbNodes.map((n) => {
    const set = docTokenSets.get(n.purposeRef);
    const pred = { art50: [], annexIII: [], prohibited: [] };
    for (const o of overlay.nodes) {
      const trig = [...new Set((o.triggerTokens ?? []).flatMap((t) => tokens(t)))];
      if (!trig.length) continue;
      let s = 0;
      for (const t of trig) if (set.has(t)) s += idf(t);
      if (s / Math.sqrt(trig.length) >= th) {
        const sh = SHORT_OF(o.ref);
        (sh.startsWith("50.") ? pred.art50 : sh.startsWith("III.") ? pred.annexIII : pred.prohibited).push({ ref: sh });
      }
    }
    return scoreOne(pred, truth[n.purposeRef] ?? {});
  });
  const a = aggregate(rows);
  sweep.push({ threshold: th, precision: a.precision, recall: a.recall, f1: a.f1, falsePositives: a.falsePositives });
}

const extended = { ...summary, stratifiedRecallByLabelStrength: stratified, runA_thresholdSweep: sweep };
fs.writeFileSync(path.join(dir, "results/summary.json"), JSON.stringify(extended, null, 2) + "\n");
console.log("\n--- stratified recall by ground-truth label strength ---");
console.log(JSON.stringify(stratified, null, 2));
console.log("\n--- run A threshold sweep ---");
console.table(sweep);
