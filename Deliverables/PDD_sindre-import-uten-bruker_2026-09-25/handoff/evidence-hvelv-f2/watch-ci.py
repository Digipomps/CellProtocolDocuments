import datetime,json,pathlib,subprocess,time
out=pathlib.Path(__file__).resolve().parent
run='36396748001'
repo='Digipomps/CellScaffold'
head='b658ef53e14dccdb12009991e78b1b44d47dac8a'
deadline=datetime.datetime.fromisoformat('2026-09-28T09:20:08+00:00')
remaining=max(1,(deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds())
result={'run':run,'head':head,'deadline':deadline.isoformat(),'timed_out':False}
with (out/'ci-watch.log').open('w') as log:
 try:
  completed=subprocess.run(['gh','run','watch',run,'--repo',repo,'--interval','30','--exit-status'],stdout=log,stderr=subprocess.STDOUT,timeout=remaining)
  result['watch_exit']=completed.returncode
 except subprocess.TimeoutExpired:
  result['timed_out']=True
result['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
terminal=subprocess.run(['gh','run','view',run,'--repo',repo,'--json','databaseId,headSha,status,conclusion,url,jobs,createdAt,updatedAt'],text=True,capture_output=True)
result['terminal_query_exit']=terminal.returncode
if terminal.returncode==0:
 result['workflow']=json.loads(terminal.stdout)
else: result['terminal_error']=terminal.stderr
(out/'ci-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='workflow'},indent=2))
if 'workflow' in result: print(json.dumps({k:v for k,v in result['workflow'].items() if k!='jobs'},indent=2))
