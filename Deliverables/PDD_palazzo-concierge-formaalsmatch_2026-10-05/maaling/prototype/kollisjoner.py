# -*- coding: utf-8 -*-
"""Hvert ord i treningsradene og i korpusets tekster som treffer en term uten å være lik den.
Listen leses for hånd: er det en bøyning eller sammensetning (bra), eller en kollisjon (inn i unntak)?"""
import json, sys, collections
import husgraf, dekomp, maal
from ordtreff import normalize, term_matches_token
data = json.load(open(sys.argv[1], encoding="utf-8"))
korpus = json.load(open(husgraf.KORPUS, encoding="utf-8"))
g = husgraf.Graf(data, korpus); sp = dekomp.Spraak(data)
kor, solv = maal.les()
tekster = [kor[s["id"]]["tekst"] for s in solv if not s["holdout"]]
for m in korpus["menu_items"]: tekster += [m["name"], m["description_nb"]]
for m in korpus["beverage_items"]: tekster += [m["name"]]
ord_ = collections.Counter()
for t in tekster:
    for _, o, _, _ in dekomp.setninger(t, sp):
        for x in o: ord_[x] += 1
par = collections.defaultdict(list)
for term in g.termer:
    if len(term.ord) != 1 or term.eksakt: continue
    w = term.ord[0]
    for o in ord_:
        if o == w or any(term_matches_token(u, o, False) for u in g.unntak.get(w, ())): continue
        if term_matches_token(w, o, True):
            par[(w, term.type, ",".join(term.noder))].append(o)
for (w, type_, noder), liste in sorted(par.items()):
    print("%-14s %-9s %-28s %s" % (w, type_, noder[:28], " ".join(sorted(liste))))
print(len(par), "termer med treff som ikke er like ordet")
# stammer i stikkordene
print()
for klasse, mo in sp.stikk:
    if len(mo) == 1 and mo[0][1]:
        w = mo[0][0]
        print("%-12s %-12s %s" % (klasse, w + "*", " ".join(sorted(o for o in ord_ if o != w and term_matches_token(w, o, False)))))
