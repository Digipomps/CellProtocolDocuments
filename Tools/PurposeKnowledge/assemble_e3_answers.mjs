import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";
const r = loadPurposeKnowledge({knowledgePath:"Book/haven_purpose_knowledge_base_v0.json",indexPath:"Book/haven_purpose_knowledge_base_index_v0.json"});
const cases = new Map(fs.readFileSync("Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl","utf8").split(/\n/).filter(l=>l.trim()&&!l.startsWith("#")).map(l=>{const c=JSON.parse(l);return[c.id,c];}));
const rows = fs.readFileSync("Tools/PurposeKnowledge/results/e3_apple_answers.jsonl","utf8").split(/\n/).filter(l=>l.trim()).map(l=>JSON.parse(l));
const byCase=new Map();
for(const row of rows){ if(!byCase.has(row.caseID))byCase.set(row.caseID,[]); byCase.get(row.caseID).push(row); }
function assemble(accepted,tc){
  let sel=accepted.map(a=>a.ref).filter(ref=>r.nodeByRef.has(ref)); if(!sel.length)sel=["purpose://prompt.unknown"];
  const expanded=r.expandCoverage(sel);
  const goalRefs=[...new Set(expanded.map(ref=>r.nodeByRef.get(ref)?.goal?.goalRef).filter(Boolean))];
  const core=[...accepted].sort((a,b)=>(b.resolverScore??0)-(a.resolverScore??0)).slice(0,2).map(a=>a.ref);
  const nearest=r.lowestCommonAncestor(r.primaryRefs(core.length?core:sel))??(core[0]??sel[0]);
  return {schema:"haven.purpose-model-output.v0",id:tc.id,status:sel.length===1&&sel[0]==="purpose://prompt.unknown"?"unknown":"resolved",purposeRefs:sel,topPurposeRefs:sel,expandedPurposeRefs:expanded,goalRefs,nearestSharedPurposeRef:nearest};
}
// resolver-score gate sweep for "calibration" proxy (no logprobs for single-shot Apple)
const gates=[0,3,4,5,8,12,20];
const out=[];
for(const[caseID,cand]of byCase){ const tc=cases.get(caseID); if(!tc)continue;
  const yes=cand.filter(c=>c.answer==="yes");
  out.push({id:caseID,model:"apple-fm-3b#micro-strict#post",response:assemble(yes,tc)});
  for(const g of gates){ const gated=yes.filter(c=>(c.resolverScore??0)>=g); out.push({id:caseID,model:`apple-fm-3b#gate${g}#post`,response:assemble(gated.length?gated:yes.slice(0,1),tc)}); }
}
fs.writeFileSync("Tools/PurposeKnowledge/results/e3_scorer.jsonl",out.map(o=>JSON.stringify(o)).join("\n")+"\n");
console.log("wrote",out.length,"rows");
