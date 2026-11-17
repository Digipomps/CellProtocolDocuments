# -*- coding: utf-8 -*-
"""Lager referansen Swift-koden holdes mot: for hver setning i korpuset, formålet og nodene prototypen gir,
og tallene mot sølvfasiten regnet her. Swift-testen regner de samme tallene selv og krever at de er like.
Bruk: python3 lag_referanse.py <datafil> <ut.json>"""
import json, sys, collections
import husgraf, dekomp, maal
data = json.load(open(sys.argv[1], encoding="utf-8"))
g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
kjente = maal.katalognoder(); kor, solv = maal.les()
rader = []; ut = {}
for i in sorted(kor):
    d = dekomp.dekomponer(kor[i]["tekst"], g, sp)
    ut[i] = d
    rader.append({"id": i, "formaal": dekomp.merkelapp(d),
                  "noder": sorted(("-" if x["slag"] in dekomp.NEGATIVE else "+") + x["node"] + "|" + x["slag"] for x in d["noder"]),
                  "allergi": d["allergi"]})
tall = collections.OrderedDict()
def legg(noekkel, f_ok, n_ok):
    t = tall.setdefault(noekkel, {"n": 0, "formaal": 0, "noder": 0, "begge": 0})
    t["n"] += 1; t["formaal"] += int(f_ok); t["noder"] += int(n_ok); t["begge"] += int(f_ok and n_ok)
for s in solv:
    del_ = "holdout" if s["holdout"] else "trening"
    d = ut[s["id"]]
    f_ok = dekomp.merkelapp(d) == s["formaal"]
    fas = {(n["node"], n["negativ"]) for n in s["noder"] if n["node"] != "ukjent"}
    fikk = {(n["node"], n["slag"] in maal.NEG) for n in d["noder"] if n["node"] in kjente}
    n_ok = fas == fikk
    legg(del_ + "/alle", f_ok, n_ok); legg(del_ + "/kilde:" + s["kilde"], f_ok, n_ok); legg(del_ + "/formaal:" + s["formaal"], f_ok, n_ok)
json.dump({"versjon": data["versjon"], "korpus": "korpus-v1.jsonl (769 setninger)", "fasit": "solvfasit-v1.jsonl (689 rader)",
           "regel": "En rad er riktig på noder når mengden (node, fortegn) er lik fasitens. Noden ukjent telles ikke, og heller ikke noder tolken ikke hadde i katalogen sin.",
           "maalt": {k: tall[k] for k in sorted(tall)}, "rader": rader},
          open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
print("referanse:", len(rader), "rader, versjon", data["versjon"])
for k in sorted(tall):
    if k.startswith("trening/alle") or (k.startswith("trening/kilde")): print("  ", k, tall[k])
