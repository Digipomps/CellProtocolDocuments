# -*- coding: utf-8 -*-
"""Sølvfasit av to blinde tolker: en rad er med når A og B har samme formål og samme mengde (node, fortegn).
Regelen er den samme som for sølvfasit v1 (skriptet kontrolleres ved at det gjenskaper v1 fra tolk-raa.json).
Bruk: lag_solv.py <korpus.jsonl> <tolk-raa.json> <ut-solv.jsonl> <ut-uenige.jsonl>"""
import json, sys
NEG = {"liker-ikke", "taaler-ikke", "spiser-ikke"}

def nokkel(x):
    return (x["formaal"], frozenset((n["node"], n["slag"] in NEG) for n in x.get("noder", [])))

def solvrad(kor, a, b):
    # Nodene er mengden (node, fortegn) de to er enige om, sortert. Slaget er det begge sa;
    # sa de hvert sitt slag med samme fortegn, står begge.
    aslag = {n["node"]: n["slag"] for n in a.get("noder", [])}
    bslag = {n["node"]: n["slag"] for n in b.get("noder", [])}
    noder = []
    for node, neg in sorted({(n["node"], n["slag"] in NEG) for n in a.get("noder", [])}):
        sa, sb = aslag[node], bslag.get(node, aslag[node])
        noder.append({"negativ": neg, "node": node, "slag": sa if sa == sb else [sa, sb]})
    return {"allergi": a.get("allergi") if a.get("allergi") == b.get("allergi") else None,
            "formaal": a["formaal"], "holdout": kor["holdout"], "id": kor["id"], "kilde": kor["kilde"],
            "noder": noder, "ukjent_ord": sorted(set(a.get("ukjent", [])) | set(b.get("ukjent", []))),
            "usikker": bool(a.get("usikker")) or bool(b.get("usikker"))}

def lag(korpus, raa):
    A, B = raa["A"], raa["B"]
    solv, uenige, mangler = [], [], []
    for kor in sorted(korpus, key=lambda k: k["id"]):
        i = kor["id"]
        if i not in A or i not in B: mangler.append(i); continue
        if nokkel(A[i]) == nokkel(B[i]): solv.append(solvrad(kor, A[i], B[i]))
        else: uenige.append({"A": A[i], "B": B[i], "holdout": kor["holdout"], "id": i, "kilde": kor["kilde"], "tekst": kor["tekst"]})
    return solv, uenige, mangler

if __name__ == "__main__":
    korpus = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
    raa = json.load(open(sys.argv[2], encoding="utf-8"))
    solv, uenige, mangler = lag(korpus, raa)
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        for r in solv: f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(sys.argv[4], "w", encoding="utf-8") as f:
        for r in uenige: f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    print("rader i korpuset: %d | enige: %d | uenige: %d | mangler tolkning: %d" % (len(korpus), len(solv), len(uenige), len(mangler)))
    print("enige: trening %d, avholdt %d" % (sum(1 for r in solv if not r["holdout"]), sum(1 for r in solv if r["holdout"])))
