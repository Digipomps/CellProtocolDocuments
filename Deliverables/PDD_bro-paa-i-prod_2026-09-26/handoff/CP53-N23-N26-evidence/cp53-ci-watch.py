from pathlib import Path
import subprocess,json,datetime,time
root=Path('/Users/kjetil/Build/Digipomps/HAVEN')
e=root/'CellProtocolDocuments/Deliverables/PDD_bro-paa-i-prod_2026-09-26/handoff/CP53-N23-N26-evidence'
cmd=['gh','pr','checks','53','--repo','Digipomps/CellProtocol','--watch','--interval','30']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (e/'ci-watch.log').open('w') as out:
    try:
        result=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,timeout=3600)
        code=result.returncode
    except subprocess.TimeoutExpired:
        code=124
record=dict(command=cmd,started=start,finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=code)
(e/'ci-watch-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
print((e/'ci-watch.log').read_text()[-6000:])
