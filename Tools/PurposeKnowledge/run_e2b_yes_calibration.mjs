#!/usr/bin/env node
// E2b: calibrate the YES threshold via self-consistency. NanoGPT does not
// return token logprobs, so we estimate each candidate's P(YES) empirically:
// sample the per-candidate YES/NO/UNSURE micro-question N times at temperature
// > 0 and take the YES fraction as the confidence. score_e2b_threshold.mjs then
// picks a threshold on a train split and evaluates on held-out test cases.
// Secret-free: key from env.

import fs from "node:fs";
import crypto from "node:crypto";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";

const args = parseArgs(process.argv.slice(2));
const casesPath = args.cases ?? "Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl";
const outDir = args.outDir ?? "Tools/PurposeKnowledge/results";
const baseURL = "https://nano-gpt.com/api/v1";
const apiKey = process.env.NANOGPT_API_KEY;
const models = (args.models ?? "mistralai/ministral-3b-2512,Qwen/Qwen3-8B").split(",");
const shortlistK = Number(args.k ?? 8);
const samples = Number(args.samples ?? 5);
const temperature = Number(args.temperature ?? 0.8);
const concurrency = Number(args.concurrency ?? 8);
const limitCases = args.limit ? Number(args.limit) : null;

if (!apiKey) {
  console.error("Set NANOGPT_API_KEY in the environment.");
  process.exit(2);
}

const resolver = loadPurposeKnowledge({
  knowledgePath: args.knowledge ?? "Book/haven_purpose_knowledge_base_v0.json",
  indexPath: args.index ?? "Book/haven_purpose_knowledge_base_index_v0.json"
});

const allCases = readJSONL(casesPath);
const cases = limitCases ? allCases.slice(0, limitCases) : allCases;

function shortlistCandidates(prompt) {
  const resolution = resolver.resolvePrompt(prompt, {});
  const scores = new Map((resolution.ranked ?? []).map((item) => [item.purposeRef, item.score]));
  const picked = [];
  for (const ref of (resolution.ranked ?? []).map((item) => item.purposeRef)) {
    if (picked.length >= shortlistK) break;
    if (ref && !picked.includes(ref) && resolver.nodeByRef.has(ref)) picked.push(ref);
  }
  return { picked, scores };
}

function microPrompt(testCase, ref, modelID) {
  const node = resolver.nodeByRef.get(ref);
  const outcome = node?.goal?.outcome ? `\nGoal outcome: ${node.goal.outcome}` : "";
  const noThink = modelID.startsWith("Qwen/") ? "\n/no_think" : "";
  return `A user wrote this request to a software assistant:
"${testCase.prompt}"

Candidate purpose from our taxonomy:
${ref} — ${node?.title ?? ""}
Summary: ${node?.summary ?? ""}${outcome}

Question: Does fulfilling the user's request require this purpose? Consider it required if the request clearly needs it, even implicitly.
Answer with exactly one word: YES, NO, or UNSURE.${noThink}`;
}

function classify(text) {
  const cleaned = (text ?? "").replace(/<think>[\s\S]*?<\/think>/g, " ").toUpperCase();
  const match = cleaned.match(/\b(YES|NO|UNSURE)\b/);
  return match ? match[1] : "UNPARSED";
}

// Ask for `n` completions in one request; return the list of answer labels.
// Falls back to single-sample requests if the provider ignores `n`.
async function sampleAnswers(modelID, prompt, wantN) {
  const answers = [];
  const body = {
    model: modelID,
    messages: [{ role: "user", content: prompt }],
    temperature,
    max_tokens: modelID.startsWith("Qwen/") ? 320 : 8,
    n: wantN,
    stream: false
  };
  const response = await fetch(`${baseURL}/chat/completions`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${(await response.text()).slice(0, 200)}`);
  const payload = await response.json();
  for (const choice of payload?.choices ?? []) answers.push(classify(choice.message?.content));
  // Top up sequentially if the provider returned fewer than requested.
  while (answers.length < wantN) {
    const single = { ...body, n: 1 };
    const r = await fetch(`${baseURL}/chat/completions`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify(single)
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const p = await r.json();
    answers.push(classify(p?.choices?.[0]?.message?.content));
  }
  return answers.slice(0, wantN);
}

async function runJob(job) {
  for (let attempt = 1; attempt <= 4; attempt += 1) {
    try {
      const answers = await sampleAnswers(job.modelID, job.prompt, samples);
      const yes = answers.filter((a) => a === "YES").length;
      const no = answers.filter((a) => a === "NO").length;
      const unsure = answers.filter((a) => a === "UNSURE").length;
      const counted = yes + no + unsure;
      return { ...job, samples: answers.length, yes, no, unsure, pYes: counted ? yes / counted : 0 };
    } catch (error) {
      if (attempt === 4) return { ...job, samples: 0, yes: 0, no: 0, unsure: 0, pYes: 0, error: String(error).slice(0, 200) };
      await new Promise((resolve) => setTimeout(resolve, 1500 * attempt));
    }
  }
  return null;
}

async function main() {
  const jobs = [];
  for (const testCase of cases) {
    const { picked, scores } = shortlistCandidates(testCase.prompt);
    for (const modelID of models) {
      for (const ref of picked) {
        jobs.push({
          caseID: testCase.id, modelID, modelShort: modelID.split("/").pop(),
          ref, resolverScore: scores.get(ref) ?? 0, prompt: microPrompt(testCase, ref, modelID)
        });
      }
    }
  }
  console.log(`E2b self-consistency: ${cases.length} cases, ${jobs.length} candidates x ${samples} samples (concurrency=${concurrency})`);

  const results = [];
  let index = 0;
  async function worker() {
    while (index < jobs.length) {
      const job = jobs[index];
      index += 1;
      results.push(await runJob(job));
      if (results.length % 50 === 0) console.log(`  ${results.length}/${jobs.length} candidates done`);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));

  const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
  const logPath = `${outDir}/e2b_calib_log_${stamp}.jsonl`;
  fs.writeFileSync(logPath, results.map((row) => JSON.stringify({
    caseID: row.caseID, model: row.modelShort, ref: row.ref, resolverScore: row.resolverScore,
    pYes: row.pYes, yes: row.yes, no: row.no, unsure: row.unsure, samples: row.samples, error: row.error
  })).join("\n") + "\n");

  const manifest = {
    schema: "haven.e2b-yes-calibration.v0", method: "self-consistency",
    generatedAt: new Date().toISOString(),
    models, shortlistK, samples, temperature,
    caseCount: cases.length, candidateCount: results.length,
    callCountApprox: results.reduce((sum, row) => sum + (row.samples || 0), 0),
    promptTemplateHash: "sha256:" + crypto.createHash("sha256").update(microPrompt(cases[0], "purpose://root", "x")).digest("hex"),
    logPath
  };
  fs.writeFileSync(`${outDir}/e2b_calib_manifest_${stamp}.json`, JSON.stringify(manifest, null, 2) + "\n");
  console.log(`wrote ${logPath}`);
  console.log(`candidates: ${results.length}, total samples: ${manifest.callCountApprox}, errors: ${results.filter((r) => r.error).length}`);
}

function readJSONL(path) {
  return fs.readFileSync(path, "utf8").split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith("#")).map((l) => JSON.parse(l));
}
function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) { parsed[key] = next; i += 1; } else { parsed[key] = true; }
    }
  }
  return parsed;
}

main().catch((error) => { console.error(error); process.exit(1); });
