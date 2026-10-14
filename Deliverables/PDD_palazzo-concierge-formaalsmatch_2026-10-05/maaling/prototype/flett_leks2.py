# -*- coding: utf-8 -*-
"""Runde 2: fletter forslagene fra ordlistetrådene inn som et tillegg til datafilen, med kontroller.
Emner og allergener (én tråd per fil): det tråden kalte sikkert, minus det som alt treffer, er for kort,
eller er et annet ord i grafen. Stikkord (tre tråder, samme innfil): det minst to tråder kalte sikkert, det én kalte sikkert
og en annen var usikker på, og det én kalte sikkert når uttrykket har minst to ord eller minst seks tegn.
Det som er avvist eller plukket for hånd, står i ../ordlister2/haand/ (avvist.json, haandplukket.json, utelatt.json).
Bruk: python3 flett_leks2.py <grunnfil> <ut tillegg.json> [mappe med trådenes filer]"""
import json, sys, collections
import husgraf, dekomp
from ordtreff import normalize, term_matches_token
import stier
L = (sys.argv[3] if len(sys.argv) > 3 else stier.ORDLISTER2).rstrip("/") + "/"
H = stier.ORDLISTER2_HAAND + "/"
grunn = json.load(open(sys.argv[1], encoding="utf-8"))
korpus = json.load(open(husgraf.KORPUS, encoding="utf-8"))
g = husgraf.Graf(grunn, korpus); sp = dekomp.Spraak(grunn)
alle_termer = {}
for t in g.termer: alle_termer.setdefault(" ".join(t.ord), set()).update(t.noder)
stikkord = set()
for _, mo in sp.stikk: stikkord.update(o for o, _ in mo)
for mo in sp.nektelser + sp.engelske_nektelser: stikkord.update(o for o, _ in mo)
for navn, liste in sp.ordlister.items():
    for mo in liste: stikkord.update(o for o, _ in mo)
stikkord |= sp.skiller | sp.skiller_etter_komma | sp.spoerreord | sp.bindeord | sp.kopula
FUNKSJONSORD = set("og i a pa av til for med er en et ei den det de som at om fra har jeg vi du dere han hun the of and to in is it te no na ka e d".split())

logg = collections.OrderedDict()
def vurder(form, node):
    n = normalize(form.lstrip("="))
    if not n or any(c.isdigit() for c in n): return None, "tom eller tall"
    ord_ = n.split(" ")
    if n in alle_termer:
        return None, "står alt (%s)" % ",".join(sorted(alle_termer[n]))
    if len(ord_) == 1:
        if n in stikkord or n in FUNKSJONSORD: return None, "er et stikkord eller funksjonsord"
        if len(n) < 3: return None, "under tre tegn"
        for t in g.termer:
            if node in t.noder and len(t.ord) == 1 and not t.eksakt and term_matches_token(t.ord[0], n, True):
                return None, "treffes alt av «%s»" % t.ord[0]
        if len(n) <= 4: return "=" + form.lstrip("="), "kort: bare nøyaktig treff"
    else:
        if all(o in stikkord or o in FUNKSJONSORD for o in ord_): return None, "bare stikkord og funksjonsord"
    return form, "tatt med"

tillegg = {"ordformer": collections.OrderedDict(), "allergenord": collections.OrderedDict(), "stikk": collections.OrderedDict(), "nektelser": [], "ordlister": collections.OrderedDict()}
UTELATT = json.load(open(H + "utelatt.json", encoding="utf-8")) if __import__("os").path.exists(H + "utelatt.json") else {}
for fil in ("emner-A.json", "emner-B.json"):
    d = json.load(open(L + fil, encoding="utf-8"))
    for nokkel, former in d["forslag"].items():
        er_allergen = nokkel in g.allergener
        if not er_allergen and nokkel not in g.kanter and nokkel not in grunn["graf"]["emner_uten_kant"]:
            logg[(nokkel, "*")] = "ukjent nøkkel"; continue
        node = ("allergen:" if er_allergen else "emne:") + nokkel
        for f in former:
            if f in UTELATT.get(nokkel, []): logg[(nokkel, f)] = "utelatt for hånd"; continue
            ny, hvorfor = vurder(f, node)
            logg[(nokkel, f)] = hvorfor
            if ny: tillegg["allergenord" if er_allergen else "ordformer"].setdefault(nokkel, []).append(ny)

def nm(x): return " ".join((normalize(o[:-1]) + "*") if o.endswith("*") else normalize(o) for o in x.split(" ") if normalize(o.rstrip("*")))
traader = [json.load(open(L + "stikk-%d.json" % n, encoding="utf-8")) for n in (1, 2, 3)]
AVVIST = json.load(open(H + "avvist.json", encoding="utf-8")) if __import__("os").path.exists(H + "avvist.json") else {}
HAANDPLUKKET = json.load(open(H + "haandplukket.json", encoding="utf-8")) if __import__("os").path.exists(H + "haandplukket.json") else {}
eksisterende = {}
for klasse, mo in sp.stikk: eksisterende[" ".join(o + ("*" if s else "") for o, s in mo)] = klasse
for navn, liste in sp.ordlister.items():
    for mo in liste: eksisterende.setdefault(("L", navn, " ".join(o + ("*" if s else "") for o, s in mo)), navn)
nekt_har = set(" ".join(o for o, _ in mo) for mo in sp.nektelser + sp.engelske_nektelser)
noekler = set(HAANDPLUKKET)
for t in traader: noekler |= set(t["forslag"])
kandidater = collections.OrderedDict()
for k in sorted(noekler):
    sikre = collections.Counter(); usikre = collections.Counter()
    for t in traader:
        for x in {nm(y) for y in t["forslag"].get(k, [])}: sikre[x] += 1
        for x in {nm(y) for y in t.get("usikre", {}).get(k, [])}: usikre[x] += 1
    # Én tråd alene holder når uttrykket har minst to ord eller minst seks tegn: da er det sjelden et annet ord.
    def langt(x): return len(x.split(" ")) >= 2 or len(x.rstrip("*")) >= 6
    valgt = {x for x in sikre if sikre[x] >= 2 or (sikre[x] >= 1 and usikre[x] >= 1) or langt(x)} | {nm(x) for x in HAANDPLUKKET.get(k, [])}
    for x in sorted(set(sikre) - valgt):
        logg[(k, x)] = "bare én tråd, og kort"
    for x in sorted(valgt):
        if not x: continue
        if x in {nm(y) for y in AVVIST.get(k, [])}: logg[(k, x)] = "avvist for hånd"; continue
        if k == "nektelser":
            if x in nekt_har: continue
            tillegg["nektelser"].append(x); logg[(k, x)] = "tatt med"
        elif k in sp.ordlister:
            if ("L", k, x) in eksisterende: continue
            tillegg["ordlister"].setdefault(k, []).append(x); logg[(k, x)] = "tatt med"
        else:
            if x in eksisterende:
                logg[(k, x)] = "står alt i " + eksisterende[x]; continue
            if x.rstrip("*") in nekt_har: logg[(k, x)] = "er en nektelse"; continue
            tillegg["stikk"].setdefault(k, []).append(x); logg[(k, x)] = "tatt med"
json.dump(tillegg, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
c = collections.Counter(v.split(" (")[0].split(" «")[0] for v in logg.values())
print("vurdert:", len(logg), dict(c))
print("tatt med: ordformer %d, allergenord %d, stikk %d, nektelser %d, ordlister %d" % (
    sum(len(v) for v in tillegg["ordformer"].values()), sum(len(v) for v in tillegg["allergenord"].values()),
    sum(len(v) for v in tillegg["stikk"].values()), len(tillegg["nektelser"]), sum(len(v) for v in tillegg["ordlister"].values())))
json.dump([[k[0], k[1], v] for k, v in logg.items()], open(sys.argv[2].replace(".json", "-logg.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
