# -*- coding: utf-8 -*-
"""Fletter forslagene fra ordlistetrådene inn som et tillegg til datafilen, med kontroller.
Emner og allergener: det tråden kalte sikkert, minus det som alt treffer, er for kort, eller er et annet ord i grafen.
Stikkord: det begge trådene foreslo, det én foreslo og den andre var usikker på, og en håndplukket liste.
Bruk: python3 flett_leks.py <grunnfil> <ut tillegg.json>"""
import json, sys, collections
import husgraf, dekomp
from ordtreff import normalize, term_matches_token
import stier
L = stier.ORDLISTER + "/"
grunn = json.load(open(sys.argv[1], encoding="utf-8"))
korpus = json.load(open(husgraf.KORPUS, encoding="utf-8"))
g = husgraf.Graf(grunn, korpus); sp = dekomp.Spraak(grunn)
alle_termer = {}                       # normalisert tekst -> noder
for t in g.termer: alle_termer.setdefault(" ".join(t.ord), set()).update(t.noder)
stikkord = set()                        # alle ord som står i stikkord, nektelser og ordlister
for _, mo in sp.stikk: stikkord.update(o for o, _ in mo)
for mo in sp.nektelser + sp.engelske_nektelser: stikkord.update(o for o, _ in mo)
for navn, liste in sp.ordlister.items():
    for mo in liste: stikkord.update(o for o, _ in mo)
stikkord |= sp.skiller | sp.skiller_etter_komma | sp.spoerreord | sp.bindeord | sp.kopula
FUNKSJONSORD = set("og i a pa av til for med er en et ei den det de som at om fra har jeg vi du dere han hun the of and to in is it".split())

logg = collections.OrderedDict()
def vurder(form, node, type_):
    n = normalize(form)
    if not n or any(c.isdigit() for c in n): return None, "tom eller tall"
    ord_ = n.split(" ")
    if n in alle_termer:
        return None, "står alt (%s)" % ",".join(sorted(alle_termer[n]))
    if len(ord_) == 1:
        if n in stikkord or n in FUNKSJONSORD: return None, "er et stikkord eller funksjonsord"
        if len(n) < 3: return None, "under tre tegn"
        # treffer en term for samme node alt, med regelen?
        for t in g.termer:
            if node in t.noder and len(t.ord) == 1 and not t.eksakt and term_matches_token(t.ord[0], n, True):
                return None, "treffes alt av «%s»" % t.ord[0]
        if len(n) <= 4: return "=" + form, "kort: bare nøyaktig treff"
    else:
        if all(o in stikkord or o in FUNKSJONSORD for o in ord_): return None, "bare stikkord og funksjonsord"
    return form, "tatt med"

tillegg = {"ordformer": collections.OrderedDict(), "allergenord": collections.OrderedDict(), "stikk": collections.OrderedDict(), "nektelser": [], "ordlister": collections.OrderedDict()}
UTELATT = {  # lest for hånd: ikke samme ting, eller et annet vanlig ord
 "N": ["nøter", "notter"], "fritert": ["fritere"], "eplemost": ["eplejuice", "apple juice", "äppeljuice", "æblejuice"], "alkoholfri vin": ["alkoholfritt vin"],
 "kjøtt": [], "krem": ["creme", "crème", "crema"], "kake": ["torte", "torta", "kuchen"], "italia": ["italien", "italienisch"],
 "brus": ["fizzy drink"], "skjell": ["musslor", "mussla", "muschel"], "sterk": ["pikant", "picante"], "vann": ["aqua"],
 "havbrasme": ["bream", "gilthead"], "øl": ["birre"], "sjømat": ["fisk og skalldyr", "fisk och skaldjur", "fisk og skaldyr"],
}
for fil, kilde in (("emner-A.json", "ordlistetråd A"), ("emner-B.json", "ordlistetråd B")):
    d = json.load(open(L + fil, encoding="utf-8"))
    for nokkel, former in d["forslag"].items():
        er_allergen = nokkel in g.allergener
        if not er_allergen and nokkel not in g.kanter:
            logg[(nokkel, "*")] = "ukjent nøkkel"; continue
        node = ("allergen:" if er_allergen else "emne:") + nokkel
        for f in former:
            if f in UTELATT.get(nokkel, []): logg[(nokkel, f)] = "utelatt for hånd"; continue
            ny, hvorfor = vurder(f, node, "allergen" if er_allergen else "emne")
            logg[(nokkel, f)] = hvorfor
            if ny: tillegg["allergenord" if er_allergen else "ordformer"].setdefault(nokkel, []).append(ny)

# stikkordene
a = json.load(open(L + "stikk-1.json", encoding="utf-8")); b = json.load(open(L + "stikk-2.json", encoding="utf-8"))
def nm(x): return " ".join((normalize(o[:-1]) + "*") if o.endswith("*") else normalize(o) for o in x.split(" ") if normalize(o.rstrip("*")))
HAANDPLUKKET = {
 "LIKER_IKKE": ["don t like", "dont like", "do not like", "doesn t like", "not for me", "not a fan of"],
 "SPISER": ["drikke"],
 "VIL": ["i d love", "we d love", "can we get", "i ll take", "vil jeg ha", "would like", "give me"],
 "SPOER": ["is this", "is that", "kor mye", "hva e", "ka er", "hvorfor", "kvifor", "why", "do you serve"],
 "bord": ["reserve", "booking", "booka"],
 "hus": ["menu", "restaurant*", "kitchen", "price*", "hos dokker", "til dokker"],
}
AVVIST = {  # lest for hånd: betyr like ofte noe annet
 "ALLERGI": ["kvalm", "livsfarlig", "sensitiv*"], "bord": ["plass til"], "VIL": ["tar jeg"], "TAALER": [], "aapningstid": ["stanger"],
 "drikkeord": ["alkoholfri*", "mocktail*"], "kosthold": ["celiak*", "coliak*"], "nektelser": ["ikk"], "hus": ["hund"],
}
eksisterende = {}
for klasse, mo in sp.stikk: eksisterende[" ".join(o + ("*" if s else "") for o, s in mo)] = klasse
for navn, liste in sp.ordlister.items():
    for mo in liste: eksisterende.setdefault(("L", navn, " ".join(o + ("*" if s else "") for o, s in mo)), navn)
nekt_har = set(" ".join(o for o, _ in mo) for mo in sp.nektelser + sp.engelske_nektelser)
for k in sorted(set(a["forslag"]) | set(b["forslag"]) | set(HAANDPLUKKET)):
    fa = {nm(x) for x in a["forslag"].get(k, [])}; fb = {nm(x) for x in b["forslag"].get(k, [])}
    ua = {nm(x) for x in a.get("usikre", {}).get(k, [])}; ub = {nm(x) for x in b.get("usikre", {}).get(k, [])}
    valgt = (fa & fb) | (fa & ub) | (fb & ua) | {nm(x) for x in HAANDPLUKKET.get(k, [])}
    for x in sorted(valgt):
        if not x or x in {nm(y) for y in AVVIST.get(k, [])}: logg[(k, x)] = "avvist for hånd"; continue
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
