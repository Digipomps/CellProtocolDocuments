import json, itertools, re
L = json.load(open("Book/haven_lessons_register_v0.json"))["lessons"]
P = json.load(open("Book/haven_purpose_packages_v0.json"))
raw = json.dumps(P)
# hvilke lærdommer er faktisk referert fra en pakke (altsaa haandhevet av en derivedTest)?
haandhevet = {l["lessonRef"] for l in L if l["lessonRef"] in raw}
print(f"lærdommer totalt: {len(L)}")
print(f"referert fra en formaalspakke (kan haandheves av en derivedTest): {len(haandhevet)}")
print(f"kun i registeret (maa huskes av et menneske): {len(L)-len(haandhevet)}")

def like(a,b,k):
    return len(set(a['tags'])&set(b['tags']))>=k and set(a.get('purposeRefs',[]))&set(b.get('purposeRefs',[]))
print("\nfoelsomhet i 'gjentakelse'-maalet (terskel = antall felles tags):")
for k in (2,3,4):
    par=[(a,b) for a,b in itertools.combinations(sorted(L,key=lambda x:x['date']),2) if a['date']<b['date'] and like(a,b,k)]
    hh=sum(1 for a,b in par if a['lessonRef'] in haandhevet)
    print(f"  k={k}: {len(par):3} gjentakelsespar, hvorav {hh} der den tidligere var haandhevet")

print("\nalvorlighet paa gjentatte moenstre:")
par=[(a,b) for a,b in itertools.combinations(sorted(L,key=lambda x:x['date']),2) if a['date']<b['date'] and like(a,b,2)]
from collections import Counter
print(" ", dict(Counter(b['severity'] for a,b in par)))
print("\nde tre hyppigste gjentatte temaene:")
c=Counter()
for a,b in par:
    for t in set(a['tags'])&set(b['tags']): c[t]+=1
for t,n in c.most_common(6): print(f"  {t}: {n}")
