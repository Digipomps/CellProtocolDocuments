from pathlib import Path
import subprocess,zipfile,json,sys,concurrent.futures,re
here=Path(__file__).resolve().parent
gh='/opt/homebrew/bin/gh'
def collect(spec):
    name,run=spec.split(':')
    info=json.loads(subprocess.check_output([gh,'api',f'repos/Digipomps/CellProtocol/actions/runs/{run}'],text=True))
    (here/f'ci-{name}-run.json').write_text(json.dumps(info,indent=2)+'\n')
    assert info['status']=='completed',(name,info['status'])
    archive=here/f'ci-{name}-logs.zip'
    if not archive.exists():
        with archive.open('wb') as out:
            subprocess.run([gh,'api',f'repos/Digipomps/CellProtocol/actions/runs/{run}/logs'],stdout=out,check=True)
    result={}
    with zipfile.ZipFile(archive) as z:
        for file in z.namelist():
            if not file.endswith('.txt'):continue
            lines=z.read(file).decode(errors='replace').splitlines()
            result[file]=[line for line in lines if 'Executed ' in line or 'HEAD is now' in line or '##[error]' in line or 'Co-Authored-By' in line]
    (here/f'ci-{name}-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    totals=[line for file,lines in result.items() if '/' not in file for line in lines if 'Executed ' in line]
    return {'name':name,'run':run,'head_sha':info['head_sha'],'conclusion':info['conclusion'],'summary':totals[-5:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(collect,sys.argv[1:]):print(json.dumps(result),flush=True)
