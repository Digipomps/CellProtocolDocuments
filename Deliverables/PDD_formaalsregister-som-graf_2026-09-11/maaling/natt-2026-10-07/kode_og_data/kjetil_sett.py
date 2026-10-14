# Kjetils 30 dommer (runde 2, 28.9) med v1-avgjørelsene (7.10). To tekster per sak: ytringen og Kjetils egen fritekst.
# Informativt sett: ikke brukt til tuning i natt, men lest av forrige økt.
import json
from pathlib import Path
import eval7 as E
HERE=Path(__file__).resolve().parent
V1={"hei":["purpose://conversation.open"],"nei":["purpose://conversation.reject"],"ja":["purpose://conversation.accept"],
    "hvem er du":["purpose://conversation.introduce-self"],
    "foreslå et forskningsspørsmål":["purpose://librarian.propose-research-question"],
    "ønske: eksport til regneark":["purpose://digital-work.export-to-file"],
    "noen må se på dette":["purpose://project-work.work-items","purpose://digital-work.coordinate"]}
SKIP={"send skjemaet til de påmeldte"}   # dekomponering, ikke et valg (Kjetil): utelatt
def rows(kind="ytring"):
    d=json.load(open(HERE/'dommer_runde2_chat.json'))['saker']; out=[]
    for s in d:
        if s['tekst'] in SKIP: continue
        acc=V1.get(s['tekst']) or [s['gold_kjetil']]
        gold=E.NEG if acc==[E.U] else acc[0]
        t=s['tekst'] if kind=="ytring" else s['fritekst_kjetil']
        out.append({"id":f"K{s['id']}","writer":"kjetil","flate":s['flate'],"tekst":t,"gold":gold,"accept":set(acc),"stil":kind,"tolk":None,"enig":True})
    return out
def score(m, rs, tau):
    real=[r for r in rs if r['gold']!=E.NEG]; neg=[r for r in rs if r['gold']==E.NEG]
    def p(r):
        rk=m(r['flate'],r['tekst']); b=rk[0] if rk else (E.U,0)
        return b[0] if b[1]>=tau else E.U
    P={r['id']:p(r) for r in rs}
    return {"top1":f"{sum(P[r['id']] in r['accept'] for r in real)}/{len(real)}",
            "neg_flateforslag":f"{sum(P[r['id']]!=E.U and not P[r['id']].startswith('purpose://conversation') for r in neg)}/{len(neg)}"}, P
