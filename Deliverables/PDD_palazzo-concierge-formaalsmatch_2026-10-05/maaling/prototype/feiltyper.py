# -*- coding: utf-8 -*-
"""Hva slags feil: fortegn snudd (farligst), node mangler, node for mye. Trening vises; holdout bare som tall når HOLDOUT=1."""
import json, sys, os, collections
import husgraf, dekomp, maal
data = json.load(open(sys.argv[1], encoding="utf-8"))
g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
kjente = maal.katalognoder(); kor, solv = maal.les()
tell = collections.Counter(); snudd = []
for s in solv:
    del_ = "holdout" if s["holdout"] else "trening"
    d = dekomp.dekomponer(kor[s["id"]]["tekst"], g, sp)
    fas = {n["node"]: n["negativ"] for n in s["noder"] if n["node"] != "ukjent"}
    fikk = {n["node"]: (n["slag"] in maal.NEG) for n in d["noder"] if n["node"] in kjente}
    for n in set(fas) | set(fikk):
        tell[(del_, "noder i alt")] += 1
        if n in fas and n in fikk:
            if fas[n] == fikk[n]: tell[(del_, "riktig")] += 1
            elif fas[n] and not fikk[n]:
                tell[(del_, "SNUDD: fasit minus, fikk pluss")] += 1
                if del_ == "trening": snudd.append((s["id"], kor[s["id"]]["tekst"][:140], n, "fasit -, fikk +"))
            else:
                tell[(del_, "snudd: fasit pluss, fikk minus")] += 1
                if del_ == "trening": snudd.append((s["id"], kor[s["id"]]["tekst"][:140], n, "fasit +, fikk -"))
        elif n in fas:
            tell[(del_, "mangler" + (" (minus i fasit)" if fas[n] else ""))] += 1
        else:
            tell[(del_, "for mye" + (" (minus)" if fikk[n] else ""))] += 1
    # setninger der fasiten har noe gjesten unngår
    fneg = any(v for v in fas.values()) or any(n["node"] == "ukjent" for n in s["noder"])
    dneg = any(n["slag"] in ("taaler-ikke", "spiser-ikke") for n in d["noder"]) or d["formaal"] == "unngaa"
    if s["formaal"] == "unngaa":
        tell[(del_, "fasit unngaa")] += 1
        tell[(del_, "fasit unngaa, fikk unngaa")] += (d["formaal"] == "unngaa")
    if d["formaal"] == "unngaa":
        tell[(del_, "fikk unngaa")] += 1
    if s["allergi"]:
        tell[(del_, "fasit allergi")] += 1; tell[(del_, "fasit allergi, flagget")] += d["allergi"] or d["formaal"] == "unngaa"
for del_ in (("trening", "holdout") if os.environ.get("HOLDOUT") == "1" else ("trening",)):
    print(del_)
    for k in sorted(k for k in tell if k[0] == del_): print("   %-38s %d" % (k[1], tell[k]))
if "-v" in sys.argv:
    for x in snudd: print("  ", x)
