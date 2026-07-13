import fs from "node:fs";
import { loadPurposeKnowledge } from "./purpose_resolver.mjs";
const r = loadPurposeKnowledge({knowledgePath:"Book/haven_purpose_knowledge_base_v0.json",indexPath:"Book/haven_purpose_knowledge_base_index_v0.json"});
const cases = fs.readFileSync("Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl","utf8").split(/\n/).filter(l=>l.trim()&&!l.startsWith("#")).map(l=>JSON.parse(l));
const K=8;
const out=[];
for(const tc of cases){
  const res=r.resolvePrompt(tc.prompt,{});
  const scores=new Map((res.ranked??[]).map(i=>[i.purposeRef,i.score]));
  const picked=[];
  for(const ref of (res.ranked??[]).map(i=>i.purposeRef)){ if(picked.length>=K)break; if(ref&&!picked.includes(ref)&&r.nodeByRef.has(ref))picked.push(ref); }
  out.push({id:tc.id,prompt:tc.prompt,candidates:picked.map(ref=>{const n=r.nodeByRef.get(ref);return {ref,resolverScore:scores.get(ref)??0,title:n?.title??"",summary:n?.summary??"",goalOutcome:n?.goal?.outcome??""};})});
}
fs.writeFileSync("Tools/PurposeKnowledge/results/e3_input.json",JSON.stringify(out,null,1)+"\n");
console.log("wrote e3_input.json with",out.length,"cases,",out.reduce((s,c)=>s+c.candidates.length,0),"candidates");
