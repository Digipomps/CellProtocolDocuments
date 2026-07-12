#!/usr/bin/env node
// E1: shortlist experiment. Same purpose-decomposition task in two arms:
//   full-taxonomy : the model sees the entire compact purpose KB
//   shortlist     : the model sees only top-K deterministic resolver candidates
// Small models, OpenAI-compatible API (NanoGPT). Secret-free: key from env.
// Outputs one JSONL scoreable by score_model_outputs.mjs (model field encodes
// modelID#arm) plus a manifest with parse failures, timing, and hashes.

import fs from "node:fs";
import crypto from "node:crypto";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";

const args = parseArgs(process.argv.slice(2));
const casesPath = args.cases ?? "Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl";
const outDir = args.outDir ?? "Tools/PurposeKnowledge/results";
const provider = args.provider ?? "nanogpt";
const baseURL = provider === "nanogpt" ? "https://nano-gpt.com/api/v1" : args.baseURL;
const apiKey = process.env.NANOGPT_API_KEY ?? process.env.E1_API_KEY;
const models = (args.models ?? "meta-llama/llama-3.2-3b-instruct,Qwen/Qwen3-8B").split(",");
const shortlistK = Number(args.k ?? 8);
const concurrency = Number(args.concurrency ?? 6);
const maxTokens = Number(args.maxTokens ?? 1400);
const temperature = Number(args.temperature ?? 0.1);
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

function nodeLine(ref) {
  const node = resolver.nodeByRef.get(ref);
  if (!node) return null;
  const parent = node.parentRef ? ` parent=${node.parentRef}` : "";
  const goal = node.goal?.goalRef ? ` goal=${node.goal.goalRef}` : "";
  return `${ref} | ${node.title ?? node.name ?? ""}${parent}${goal}`;
}

const allNodeLines = [...resolver.nodeByRef.keys()].sort().map(nodeLine).filter(Boolean);

function shortlistLines(prompt) {
  const resolution = resolver.resolvePrompt(prompt, {});
  const ranked = (resolution.ranked ?? []).map((item) => item.purposeRef);
  const picked = [];
  const add = (ref) => {
    if (ref && !picked.includes(ref) && resolver.nodeByRef.has(ref)) picked.push(ref);
  };
  for (const ref of ranked) {
    if (picked.length >= shortlistK) break;
    add(ref);
  }
  // Parents so nearestSharedPurposeRef stays derivable, plus the honest fallback.
  for (const ref of [...picked]) add(resolver.nodeByRef.get(ref)?.parentRef);
  add("purpose://prompt.unknown");
  return { lines: picked.map(nodeLine).filter(Boolean), candidateRefs: picked };
}

function buildPrompt(testCase, arm, knownLines) {
  const armRule = arm === "shortlist"
    ? "Select ONLY from the candidate purposeRefs listed below, or purpose://prompt.unknown if none fit."
    : "Select ONLY purposeRefs that appear in the list below, or purpose://prompt.unknown if none fit.";
  return `You are evaluating a user prompt against the HAVEN purpose taxonomy.

Task:
- Select the smallest sufficient set of HAVEN purposeRefs for the prompt.
- ${armRule}
- Include goalRefs (from the listing) that would prove the purposes are achieved.
- Include nearestSharedPurposeRef: the deepest listed purpose that is an ancestor of (or equal to) all selected primary purposes, using the parent= links.
- Do not invent purposeRefs. Unknown or new purposes go in candidatePurposeRefs.
- This is analysis only; no side effects.

Return ONLY JSON, no markdown, matching:
{
  "schema": "haven.purpose-model-output.v0",
  "id": "${testCase.id}",
  "status": "resolved | unknown | partial",
  "purposeRefs": ["purpose://..."],
  "goalRefs": [],
  "nearestSharedPurposeRef": "purpose://...",
  "candidatePurposeRefs": [],
  "missingCapabilities": [],
  "reviewRequired": false,
  "confidence": 0.0,
  "sideEffectFree": true,
  "mutatesPerspective": false,
  "mutatesEntity": false,
  "briefRationale": "One short sentence."
}

Known purposes (ref | title parent= goal=):
${knownLines.join("\n")}

Case:
id: ${testCase.id}
prompt: ${testCase.prompt}
visibleCapabilities: ${JSON.stringify(testCase.visibleCapabilities ?? [])}`;
}

function extractJSON(text) {
  const stripped = text
    .replace(/<think>[\s\S]*?<\/think>/g, "")
    .replace(/```(?:json)?/g, "")
    .trim();
  const candidates = [];
  for (let start = 0; start < stripped.length; start += 1) {
    if (stripped[start] !== "{") continue;
    let depth = 0;
    for (let i = start; i < stripped.length; i += 1) {
      if (stripped[i] === "{") depth += 1;
      if (stripped[i] === "}") {
        depth -= 1;
        if (depth === 0) {
          candidates.push(stripped.slice(start, i + 1));
          start = i;
          break;
        }
      }
    }
  }
  for (const candidate of candidates.reverse()) {
    try {
      const parsed = JSON.parse(candidate);
      if (parsed && typeof parsed === "object" && (parsed.purposeRefs || parsed.schema)) return parsed;
    } catch {
      continue;
    }
  }
  return null;
}

// Deterministic post-processing: the pipeline's verify/expand stage. Drops
// invented refs, expands facets/coverage, derives goals and the LCA — the
// model only did semantic selection.
function postProcess(response, testCase) {
  const rawRefs = Array.isArray(response?.purposeRefs) ? response.purposeRefs : [];
  let refs = rawRefs.filter((ref) => resolver.nodeByRef.has(ref));
  if (refs.length === 0) refs = ["purpose://prompt.unknown"];
  const expanded = resolver.expandCoverage(refs);
  const goalRefs = [...new Set(expanded.map((ref) => resolver.nodeByRef.get(ref)?.goal?.goalRef).filter(Boolean))];
  const nearest = resolver.lowestCommonAncestor(resolver.primaryRefs(refs)) ?? refs[0];
  return {
    schema: "haven.purpose-model-output.v0",
    id: testCase.id,
    status: refs.length === 1 && refs[0] === "purpose://prompt.unknown" ? "unknown" : "resolved",
    purposeRefs: refs,
    topPurposeRefs: refs,
    expandedPurposeRefs: expanded,
    goalRefs,
    nearestSharedPurposeRef: nearest,
    droppedInventedRefs: rawRefs.filter((ref) => !resolver.nodeByRef.has(ref))
  };
}

async function callModel(modelID, prompt) {
  const body = {
    model: modelID,
    messages: [{ role: "user", content: prompt }],
    temperature,
    max_tokens: maxTokens,
    stream: false
  };
  const started = Date.now();
  const response = await fetch(`${baseURL}/chat/completions`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${(await response.text()).slice(0, 300)}`);
  }
  const payload = await response.json();
  const text = payload?.choices?.[0]?.message?.content ?? "";
  return { text, elapsedMs: Date.now() - started, usage: payload?.usage ?? null };
}

async function runJob(job) {
  const maxAttempts = 4;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const { text, elapsedMs, usage } = await callModel(job.modelID, job.prompt);
      const parsed = extractJSON(text);
      return {
        id: job.testCase.id,
        model: `${job.modelShort}#${job.arm}`,
        arm: job.arm,
        modelID: job.modelID,
        parseError: parsed === null,
        elapsedMs,
        usage,
        shortlistRecall: job.shortlistRecall,
        response: parsed ?? { schema: "haven.purpose-model-output.v0", id: job.testCase.id, status: "invalid" },
        responsePost: postProcess(parsed ?? {}, job.testCase),
        rawText: text
      };
    } catch (error) {
      if (attempt === maxAttempts) {
        return {
          id: job.testCase.id,
          model: `${job.modelShort}#${job.arm}`,
          arm: job.arm,
          modelID: job.modelID,
          parseError: true,
          error: String(error).slice(0, 300),
          shortlistRecall: job.shortlistRecall,
          response: { schema: "haven.purpose-model-output.v0", id: job.testCase.id, status: "error" },
          responsePost: postProcess({}, job.testCase)
        };
      }
      await new Promise((resolve) => setTimeout(resolve, 1500 * attempt));
    }
  }
  return null;
}

async function main() {
  const jobs = [];
  let shortlistMisses = 0;
  for (const testCase of cases) {
    const shortlist = shortlistLines(testCase.prompt);
    const mustRefs = testCase.expected?.mustIncludePurposeRefs ?? [];
    // Pipeline recall: what the deterministic verify/expand stage can reach
    // from the shortlist candidates, mirroring postProcess.
    const coveredRefs = new Set([
      ...resolver.expandCoverage(shortlist.candidateRefs),
      "purpose://prompt.unknown"
    ]);
    const recall = mustRefs.length === 0
      ? 1
      : mustRefs.filter((ref) => coveredRefs.has(ref)).length / mustRefs.length;
    if (recall < 1) shortlistMisses += 1;
    for (const modelID of models) {
      const modelShort = modelID.split("/").pop();
      jobs.push({
        testCase, modelID, modelShort, arm: "full-taxonomy",
        prompt: buildPrompt(testCase, "full-taxonomy", allNodeLines), shortlistRecall: null
      });
      jobs.push({
        testCase, modelID, modelShort, arm: "shortlist",
        prompt: buildPrompt(testCase, "shortlist", shortlist.lines), shortlistRecall: recall
      });
    }
  }

  console.log(`E1: ${cases.length} cases x ${models.length} models x 2 arms = ${jobs.length} calls (K=${shortlistK}, concurrency=${concurrency})`);
  const results = [];
  let index = 0;
  async function worker() {
    while (index < jobs.length) {
      const job = jobs[index];
      index += 1;
      const result = await runJob(job);
      results.push(result);
      if (results.length % 20 === 0) console.log(`  ${results.length}/${jobs.length} done`);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));

  const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
  const outputsPath = `${outDir}/e1_shortlist_outputs_${stamp}.jsonl`;
  fs.writeFileSync(outputsPath, results.map((row) => JSON.stringify(row)).join("\n") + "\n");

  // Two scorer-ready views: raw model output vs deterministically post-processed.
  const rawScorerPath = `${outDir}/e1_scorer_raw_${stamp}.jsonl`;
  fs.writeFileSync(rawScorerPath, results.map((row) => JSON.stringify({
    id: row.id, model: `${row.model}#raw`, response: row.response
  })).join("\n") + "\n");
  const postScorerPath = `${outDir}/e1_scorer_post_${stamp}.jsonl`;
  fs.writeFileSync(postScorerPath, results.map((row) => JSON.stringify({
    id: row.id, model: `${row.model}#post`, response: row.responsePost
  })).join("\n") + "\n");
  console.log(`wrote ${rawScorerPath}`);
  console.log(`wrote ${postScorerPath}`);

  const manifest = {
    schema: "haven.e1-shortlist-experiment.v0",
    generatedAt: new Date().toISOString(),
    provider, models, shortlistK, temperature, maxTokens,
    caseCount: cases.length,
    callCount: results.length,
    parseFailures: results.filter((row) => row.parseError).length,
    shortlistRecallMissCases: shortlistMisses,
    promptTemplateHash: "sha256:" + crypto.createHash("sha256").update(buildPrompt(cases[0], "full-taxonomy", ["X"])).digest("hex"),
    outputsPath
  };
  const manifestPath = `${outDir}/e1_shortlist_manifest_${stamp}.json`;
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
  console.log(`wrote ${outputsPath}`);
  console.log(`wrote ${manifestPath}`);
  console.log(`parse failures: ${manifest.parseFailures}/${results.length}; shortlist raw-candidate recall misses: ${shortlistMisses}/${cases.length} cases`);
}

function readJSONL(path) {
  return fs.readFileSync(path, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"))
    .map((line) => JSON.parse(line));
}

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) {
        parsed[key] = next;
        i += 1;
      } else {
        parsed[key] = true;
      }
    }
  }
  return parsed;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
