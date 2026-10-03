from pathlib import Path
import subprocess,json,datetime
ROOT=Path('/Users/kjetil/Build/Digipomps/HAVEN')
OUT=ROOT/'CellProtocolDocuments/Deliverables/Prod_Recovery_2026-09-17/repo-audit'
def git(repo,*args):
 p=subprocess.run(['git','--no-optional-locks','-C',str(repo),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 return p.stdout.rstrip("\n") if p.returncode==0 else None
def exists(repo,ref): return git(repo,'rev-parse','--verify',ref) is not None
def parsewt(raw):
 result=[]
 for b in (raw or '').split('\n\n'):
  d={}
  for l in b.splitlines():
   k,_,v=l.partition(' ');d[k]=v
  if d: result.append(d)
 return result
results=[]
for repo in sorted(ROOT.iterdir()):
 if not repo.is_dir() or not (repo/'.git').exists() or repo.name.startswith('CellScaffold'): continue
 status=git(repo,'status','--porcelain=v1','--untracked-files=all')
 base=next((r for r in ('origin/main','origin/master','main','master') if exists(repo,r)),None)
 head=git(repo,'rev-parse','HEAD')
 d={'repo':repo.name,'path':str(repo),'head':head,'branch':git(repo,'branch','--show-current'),'base':base,'base_sha':git(repo,'rev-parse',base) if base else None,'status':(status or '').splitlines(),'stashes':(git(repo,'stash','list','--format=%H%x09%gd%x09%gs') or '').splitlines(),'submodules':git(repo,'submodule','status'),'worktrees':[],'refs':[]}
 # No remote URLs recorded (credential-safe); names only.
 d['remotes']=(git(repo,'remote') or '').splitlines()
 for w in parsewt(git(repo,'worktree','list','--porcelain')):
  wp=Path(w['worktree']); w['exists']=wp.exists()
  if wp.exists(): w['status']=(git(wp,'status','--porcelain=v1','--untracked-files=all') or '').splitlines()
  d['worktrees'].append(w)
 refs=git(repo,'for-each-ref','--format=%(refname)%09%(objectname)%09%(committerdate:iso8601)%09%(subject)%09%(upstream)','refs/heads','refs/remotes') or ''
 for line in refs.splitlines():
  row=line.split('\t',4); r=dict(zip(('ref','sha','date','subject','upstream'),row))
  if base:
   counts=git(repo,'rev-list','--left-right','--count',base+'...'+r['ref'])
   if counts: r['base_only'],r['branch_only']=map(int,counts.split())
   if r.get('branch_only',0):
    cherry=git(repo,'cherry',base,r['ref'])
    r['patch_unique']=len([l for l in (cherry or '').splitlines() if l.startswith('+')])
    r['patch_equivalent']=len([l for l in (cherry or '').splitlines() if l.startswith('-')])
    r['cherry']= (cherry or '').splitlines()
    r['changed_paths']=(git(repo,'diff','--name-status',base+'...'+r['ref']) or '').splitlines()
    r['commits']=(git(repo,'log','--format=%H%x09%s',base+'..'+r['ref']) or '').splitlines()
  d['refs'].append(r)
 results.append(d)
 (OUT/'inventory.json').write_text(json.dumps({'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_freshness':'local refs only; no fetch; potentially stale','repos':results},indent=2))
 print(json.dumps({'repo':repo.name,'base':base,'refs':len(d['refs']),'unmerged_refs':sum(x.get('branch_only',0)>0 for x in d['refs']),'dirty':len(d['status']),'worktrees':len(d['worktrees']),'stashes':len(d['stashes'])}),flush=True)
