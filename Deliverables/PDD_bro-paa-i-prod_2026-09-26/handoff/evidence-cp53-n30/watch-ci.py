from pathlib import Path
import subprocess,json,time,sys
here=Path(__file__).resolve().parent
head=(here/'head.txt').read_text().strip()
deadline=json.loads((here/'ci-deadline.json').read_text())['deadline']
gh='/opt/homebrew/bin/gh'
last=None
while time.time()<deadline:
    p=subprocess.run([gh,'pr','view','53','--repo','Digipomps/CellProtocol','--json','headRefOid,headRefName,state,mergedAt,statusCheckRollup'],capture_output=True,text=True)
    if p.returncode:
        print('GitHub read failed; retrying within deadline',flush=True);time.sleep(30);continue
    state=json.loads(p.stdout)
    (here/'ci-current.json').write_text(json.dumps(state,indent=2)+'\n')
    if state['headRefOid'] != head:
        print('Waiting for pushed head',flush=True);time.sleep(15);continue
    checks=state['statusCheckRollup']
    status=[dict(name=x.get('workflowName',x.get('name')),status=x.get('status'),conclusion=x.get('conclusion')) for x in checks]
    if status!=last:
        print(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'checks':status}),flush=True);last=status
    if len(checks)>=5:
        remaining=max(1,int(deadline-time.time()))
        with (here/'ci-native-watch.log').open('w') as log:
            try:
                watched=subprocess.run([gh,'pr','checks','53','--repo','Digipomps/CellProtocol','--watch','--fail-fast','--interval','30'],stdout=log,stderr=subprocess.STDOUT,timeout=remaining)
                code=watched.returncode
            except subprocess.TimeoutExpired: code=124
        final=subprocess.run([gh,'pr','view','53','--repo','Digipomps/CellProtocol','--json','headRefOid,headRefName,state,mergedAt,statusCheckRollup'],capture_output=True,text=True)
        if final.returncode==0:(here/'final-pr.json').write_text(final.stdout)
        result={'head':head,'watchExit':code,'finished':time.time(),'deadline':deadline}
        (here/'ci-watch-result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
        sys.exit(code)
    time.sleep(15)
(here/'ci-watch-result.json').write_text(json.dumps({'head':head,'watchExit':124,'deadline':deadline},indent=2)+'\n')
sys.exit(124)
