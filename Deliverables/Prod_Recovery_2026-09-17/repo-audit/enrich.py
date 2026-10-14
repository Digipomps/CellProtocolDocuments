from pathlib import Path
import json,subprocess,re,collections
OUT=Path(__file__).parent
f=OUT/'inventory.json'; a=json.loads(f.read_text())
def git(repo,*args):
 p=subprocess.run(['git','--no-optional-locks','-C',repo,*args],capture_output=True,text=True); return p.stdout.rstrip('\n') if p.returncode==0 else ''
def subject(s): return re.sub(r'\s+\(#\d+\)$','',s).lower().strip()
for r in a['repos']:
 base=r['base'];cache={}
 if not base: continue
 mainlog=[x.split('\t',1) for x in git(r['path'],'log','--format=%H%x09%s',base).splitlines()]
 subjects=collections.defaultdict(list)
 for sha,s in mainlog: subjects[subject(s)].append(sha)
 for ref in r['refs']:
  if not ref.get('branch_only'): ref['assessment']='ANCESTRY_IN_MAIN'; continue
  if ref['sha'] in cache: ref.update(cache[ref['sha']]);continue
  merge_base=git(r['path'],'merge-base',base,ref['ref'])
  if not merge_base:
   e={'merge_base':None,'assessment':'DIVERGENT_HISTORY_REQUIRES_REVIEW','changed_path_count':None,'endpoint_different_paths':[],'endpoint_identical_count':None,'subject_matches_on_main':{}}
   ref.update(e);cache[ref['sha']]=e;continue
  touched=git(r['path'],'-c','core.quotePath=false','diff','--name-only',base+'...'+ref['ref']).splitlines()
  direct=git(r['path'],'-c','core.quotePath=false','diff','--name-only',base,ref['ref'],'--',*touched).splitlines() if touched else []
  matches={}
  for commit in ref.get('commits',[]):
   sha,s=commit.split('\t',1)
   if subject(s) in subjects: matches[sha]=subjects[subject(s)]
  e={'merge_base':merge_base,'changed_path_count':len(touched),'endpoint_different_paths':direct,'endpoint_identical_count':len(set(touched)-set(direct)),'subject_matches_on_main':matches}
  if not direct: e['assessment']='CHANGED_PATHS_IDENTICAL_TO_MAIN'
  elif ref.get('patch_unique',0)==0: e['assessment']='PATCH_EQUIVALENT_IN_MAIN'
  elif '/archive-' in ref['ref'] or '/history/' in ref['ref']: e['assessment']='ARCHIVE_REQUIRES_CONTENT_TRIAGE'
  elif matches: e['assessment']='POSSIBLE_SQUASH_OR_PARTIAL_IN_MAIN'
  else: e['assessment']='UNIQUE_OR_REBASED_REQUIRES_REVIEW'
  ref.update(e);cache[ref['sha']]=e
 (OUT/'inventory-enriched.json').write_text(json.dumps(a,indent=2))
 print(r['repo'],dict(collections.Counter(x['assessment'] for x in r['refs'])),flush=True)
