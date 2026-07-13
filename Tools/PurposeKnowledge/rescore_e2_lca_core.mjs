#!/usr/bin/env node
// E2 re-scoring: re-derive nearestSharedPurposeRef from the confident core
// (top-2 YES refs by deterministic resolver score) instead of all YES refs,
// so mild micro-task over-selection stops corrupting the derived LCA field.
// Reads the E2 micro log, emits a scorer-ready JSONL. No API calls.
// Usage: node Tools/PurposeKnowledge/rescore_e2_lca_core.mjs <e2_micro_log.jsonl>
import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";
const logFile = process.argv[2] ?? "Tools/PurposeKnowledge/results/e2_micro_log_20260713T055001Z.jsonl";
const r = loadPurposeKnowledge({knowledgePath:"Book/haven_purpose_knowledge_base_v0.json",indexPath:"Book/haven_purpose_knowledge_base_index_v0.json"});
const cases = new Map(fs.readFileSync("Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl","utf8").split(/\n/).filter(l=>l.trim()&&!l.startsWith("#")).map(l=>{const c=JSON.parse(l);return [c.id,c];}));
const log = fs.readFileSync(logFile,"utf8").split(/\n/).filter(l=>l.trim()).map(l=>JSON.parse(l));

// group YES refs per case+model
const grp = new Map();
for (const row of log){ if(row.answer!=="YES") continue; const k=row.caseID+"|"+row.model; if(!grp.has(k)) grp.set(k,[]); grp.get(k).push(row.ref); }

// deterministic resolver score per prompt to rank YES refs for LCA core
function rankedScores(prompt){ const res=r.resolvePrompt(prompt,{}); const m=new Map(); for(const it of res.ranked??[]) m.set(it.purposeRef,it.score); return m; }

const out=[];
for (const [k,yesRefs] of grp){
  const [caseID,model]=k.split("|"); const tc=cases.get(caseID); if(!tc) continue;
  const sel=yesRefs.filter(ref=>r.nodeByRef.has(ref)); const use=sel.length?sel:["purpose://prompt.unknown"];
  const expanded=r.expandCoverage(use);
  const goalRefs=[...new Set(expanded.map(ref=>r.nodeByRef.get(ref)?.goal?.goalRef).filter(Boolean))];
  // LCA core: top-2 YES refs by deterministic score (confident core), not all
  const scores=rankedScores(tc.prompt);
  const core=[...use].sort((a,b)=>(scores.get(b)??0)-(scores.get(a)??0)).slice(0,2);
  const nearest=r.lowestCommonAncestor(r.primaryRefs(core))??core[0];
  out.push({id:caseID,model:model.replace("#post","-lcafix#post"),response:{schema:"haven.purpose-model-output.v0",id:caseID,status:use[0]==="purpose://prompt.unknown"&&use.length===1?"unknown":"resolved",purposeRefs:use,topPurposeRefs:use,expandedPurposeRefs:expanded,goalRefs,nearestSharedPurposeRef:nearest}});
}
fs.writeFileSync("Tools/PurposeKnowledge/results/e2_scorer_lcafix.jsonl",out.map(o=>JSON.stringify(o)).join("\n")+"\n");
console.log("wrote",out.length,"rows");
