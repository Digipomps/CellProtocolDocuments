# -*- coding: utf-8 -*-
"""Endringsloggen for datafilen: for hver oppføring, hvilke TRENINGSRADER den retter.
Hver oppføring tas ut alene, og treningsradene måles på nytt. Radene som da blir feil, er dem oppføringen retter.
Holdout-radene måles ikke her. Bruk: python3 endringslogg.py <datafil> <ut.json>"""
import json, sys, copy, collections, time
import husgraf, dekomp, maal
data = json.load(open(sys.argv[1], encoding="utf-8"))
korpus = json.load(open(husgraf.KORPUS, encoding="utf-8"))
kjente = maal.katalognoder(); kor, solv = maal.les()
trening = [s for s in solv if not s["holdout"]]
from ordtreff import normalize, term_matches_token
ordene = {}
_sp0 = dekomp.Spraak(data)
for s in trening:
    o = set()
    for _, ord_, _, _ in dekomp.setninger(kor[s["id"]]["tekst"], _sp0): o.update(ord_)
    o.update(normalize(kor[s["id"]]["tekst"]).split(" "))      # også ordene før sammensetninger deles
    ordene[s["id"]] = o
def beroert(v):
    """Radene der oppføringen kan ha noe å si: de som har et ord som treffer det første ordet i den."""
    w = normalize(v.lstrip("=").split(" ")[0].rstrip("*"))
    if not w: return [s for s in trening]
    return [s for s in trening if any(t == w or term_matches_token(w, t, True) or (len(w) >= 3 and w in t) for t in ordene[s["id"]])]
def riktige(d, rader=None):
    g = husgraf.Graf(d, korpus); sp = dekomp.Spraak(d)
    ut = set()
    for s in (trening if rader is None else rader):
        t = dekomp.dekomponer(kor[s["id"]]["tekst"], g, sp)
        fas = {(n["node"], n["negativ"]) for n in s["noder"] if n["node"] != "ukjent"}
        fikk = {(n["node"], n["slag"] in maal.NEG) for n in t["noder"] if n["node"] in kjente}
        if dekomp.merkelapp(t) == s["formaal"] and fas == fikk: ut.add(s["id"])
    return ut
grunn = riktige(data)
print("grunnlinje:", len(grunn), "av", len(trening), flush=True)
oppf = []   # (sti, verdi)
G = data["graf"]; S = data["spraak"]
for navn in ("ordformer", "navneord", "allergenord", "unntak"):
    for k in G[navn]:
        for v in G[navn][k]: oppf.append((("graf", navn, k), v))
for k in G["allergenutsagn"]:
    for slag in G["allergenutsagn"][k]:
        for v in G["allergenutsagn"][k][slag]: oppf.append((("graf", "allergenutsagn", k, slag), v))
for navn in ("navnestopp", "emner_uten_kant", "drikkeemner", "stedsemner"):
    for v in G[navn]: oppf.append((("graf", navn), v))
for k in S["stikk"]:
    for v in S["stikk"][k]: oppf.append((("spraak", "stikk", k), v))
for k in S["ordlister"]:
    for v in S["ordlister"][k]: oppf.append((("spraak", "ordlister", k), v))
for navn in ("nektelser", "engelske_nektelser", "engelske_tegn", "leddskiller", "leddskiller_etter_komma", "spoerreord", "sammensatt", "bindeord", "kopula"):
    for v in S[navn]: oppf.append((("spraak", navn), v))
print("oppføringer:", len(oppf), flush=True)
ut = []; t0 = time.time()
for i, (sti, v) in enumerate(oppf):
    d = copy.deepcopy(data)
    x = d
    for p in sti[:-1]: x = x[p]
    x[sti[-1]] = [y for y in x[sti[-1]] if y != v]
    try:
        rader = beroert(v)
        r = riktige(d, rader); ids = {x["id"] for x in rader}
        retter = sorted((grunn & ids) - r); skader = sorted(r - grunn)
    except AssertionError as e:
        retter, skader = ["(grafen lar seg ikke bygge uten: %s)" % e], []
    ut.append({"sti": "/".join(sti), "oppfoering": v, "retter": retter, "uten_den_blir_riktig": skader})
    if i % 100 == 0: print(i, "%.0fs" % (time.time() - t0), flush=True)
json.dump({"versjon": data["versjon"], "trening": len(trening), "riktige": len(grunn), "oppfoeringer": ut}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("ferdig", len(ut), "%.0fs" % (time.time() - t0))
