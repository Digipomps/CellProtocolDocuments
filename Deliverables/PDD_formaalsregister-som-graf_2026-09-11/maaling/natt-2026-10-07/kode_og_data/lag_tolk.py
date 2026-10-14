# Lager blinde tolkebatcher: opake formål-id-er, opake meldings-id-er, stokket på tvers av skribenter.
import json, random, sys
from pathlib import Path
import register_v1 as R, natt_trening as T
HERE=Path(__file__).resolve().parent
rnd=random.Random(20261007)
n=R.load_register()
skip={'purpose://prompt.unknown','purpose://root','purpose://conversation'}
refs=[r for r,v in sorted(n.items()) if not v['facetOnly'] and r not in skip]
codes=rnd.sample(range(1000,9999),len(refs))
ref2c={r:f"P{c}" for r,c in zip(refs,codes)}
items=[(ref2c[r], n[r]['title'], n[r]['desc'][:400]) for r in refs]; rnd.shuffle(items)
reg="\n".join(f"{c} | {t} | {d}" for c,t,d in items)
msgs=[]
for f in sorted((HERE/'gen').glob('*.json')):
    w=f.stem
    for i,r in enumerate(json.load(open(f))): msgs.append({"id":f"{w}-{i:03d}","flate":r['flate'],"tekst":r['tekst']})
rnd.shuffle(msgs)
mcodes=rnd.sample(range(100000,999999),len(msgs))
key={}
for m,c in zip(msgs,mcodes): key[f"M{c}"]=m['id']; m['mid']=f"M{c}"
B=50; bd=HERE/'tolk_inn'; bd.mkdir(exist_ok=True)
for i in range(0,len(msgs),B):
    json.dump([{"mid":m['mid'],"flate":m['flate'],"tekst":m['tekst']} for m in msgs[i:i+B]],open(bd/f"b{i//B:02d}.json",'w'),ensure_ascii=False,indent=0)
json.dump({"ref2code":ref2c,"msgkey":key},open(HERE/'tolk_noekkel_IKKE_TIL_TOLK.json','w'),ensure_ascii=False)
open(HERE/'tolk_register.txt','w').write(reg)
print(len(msgs),"meldinger",(len(msgs)+B-1)//B,"batcher",len(refs),"formål")
