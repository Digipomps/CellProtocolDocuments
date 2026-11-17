# Oversetter Fables svar (opake koder) tilbake til meldings-id og purpose-ref. tolk/fable.json.
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
K=json.load(open(HERE/'tolk_noekkel_IKKE_TIL_TOLK.json')); c2r={c:r for r,c in K['ref2code'].items()}
def dec(x):
    if x in (None,'null',''): return None
    if x in ('INGEN','UKLART'): return x
    return c2r.get(x, 'UGYLDIG:'+str(x))
out=[]; bad=0
for f in sorted((HERE/'tolk_ut').glob('*.json')):
    for r in json.load(open(f)):
        mid=r.get('mid'); rid=K['msgkey'].get(mid)
        if not rid: bad+=1; continue
        r2=dict(r); r2['id']=rid; r2['valg']=dec(r.get('valg')); r2['alternativ']=dec(r.get('alternativ'))
        if r2['valg'] in ('INGEN','UKLART'): r2['valg_raa']=r2['valg']; r2['valg']='NEG'
        out.append(r2)
(HERE/'tolk').mkdir(exist_ok=True)
json.dump(out,open(HERE/'tolk'/'fable.json','w'),ensure_ascii=False,indent=0)
print(len(out),'rader, ukjente mid:',bad, 'ugyldige valg:', sum(str(r['valg']).startswith('UGYLDIG') for r in out))
