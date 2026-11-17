# Tolkebatcher for nye skribenter (argv: skribenter... --prefix X). Samme opake formålskoder som runde 1.
import json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
args=sys.argv[1:]; pref=args[args.index('--prefix')+1]; ws=[a for a in args if not a.startswith('--') and a!=pref]
K=json.load(open(HERE/'tolk_noekkel_IKKE_TIL_TOLK.json'))
rnd=random.Random(hash(pref)%10**6+7)
msgs=[]
for w in ws:
    for i,r in enumerate(json.load(open(HERE/'gen'/f'{w}.json'))): msgs.append({"id":f"{w}-{i:03d}","flate":r['flate'],"tekst":r['tekst']})
rnd.shuffle(msgs)
used=set(K['msgkey'])
for m in msgs:
    while True:
        c=f"M{rnd.randrange(100000,999999)}"
        if c not in used: break
    used.add(c); K['msgkey'][c]=m['id']; m['mid']=c
B=50; bd=HERE/'tolk_inn'
names=[]
for i in range(0,len(msgs),B):
    nm=f"{pref}{i//B:02d}.json"; names.append(nm)
    json.dump([{"mid":m['mid'],"flate":m['flate'],"tekst":m['tekst']} for m in msgs[i:i+B]],open(bd/nm,'w'),ensure_ascii=False,indent=0)
json.dump(K,open(HERE/'tolk_noekkel_IKKE_TIL_TOLK.json','w'),ensure_ascii=False)
print(len(msgs), names)
