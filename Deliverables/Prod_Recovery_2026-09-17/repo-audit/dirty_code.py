from pathlib import Path
import subprocess,json,hashlib
OUT=Path(__file__).parent;a=json.loads((OUT/'inventory.json').read_text()); result=[]
source_roots={'Sources','Tests','Binding','BindingTests','BindingUITests','Cells','Scripts','scripts','tools','tests','src','Packages','Apps','.github','Book','Tools','HavenAgentD','Contracts','Packaging','deploy'}
known={'Package.swift','Package.resolved','.gitignore','.gitmodules','Dockerfile','AGENTS.md'}
skip=('.build','node_modules','__pycache__','DerivedData','SourcePackages','build','Build','target','.havenbuild','.git','fixtures','Fixtures')
def g(repo,*args):
 p=subprocess.run(['git','--no-optional-locks','-C',str(repo),*args],capture_output=True,text=True);return p.stdout.strip() if p.returncode==0 else None
for r in a['repos']:
 refs=[r['base']]
 if r['repo']=='Binding':refs+=['codex/binding-haven-complete-20260910','origin/codex/entity-continuity-20260911','origin/codex/person-entity-read-route-20260911']
 if r['repo']=='CellProtocol':refs+=['pdd/tillitspakke-agentflaate']
 for w in r['worktrees']:
  for s in w.get('status',[]):
   p=s[3:]
   if p.startswith('"'):
    try:p=json.loads(p)
    except:continue
   ps=Path(p);parts=ps.parts
   if not parts or any(x in parts for x in skip):continue
   if parts[0] not in source_roots and p not in known:continue
   file=Path(w['worktree'])/p
   if not file.is_file() or file.is_symlink() or file.stat().st_size>2000000:continue
   if file.suffix not in ['.swift','.py','.sh','.yml','.yaml','.json','.js','.cjs','.mjs','.ts','.html','.css','.toml','.rb'] and p not in known:continue
   h=g(w['worktree'],'hash-object','--',p);matches=[]
   for ref in refs:
    if ref and g(r['path'],'rev-parse',ref+':'+p)==h:matches.append(ref)
   result.append({'repo':r['repo'],'worktree':w['worktree'],'path':p,'status':s[:2],'bytes':file.stat().st_size,'blob':h,'identical_to':matches,'assessment':'REPRESENTED_IDENTICALLY' if matches else 'REVIEW_DIRTY_SOURCE'})
(OUT/'dirty-code-inventory.json').write_text(json.dumps(result,indent=2))
from collections import Counter
print('Source candidates',len(result),'assessments',dict(Counter(x['assessment'] for x in result)))
for r in a['repos']:
 xs=[x for x in result if x['repo']==r['repo']];print(r['repo'],dict(Counter(x['assessment'] for x in xs)))
