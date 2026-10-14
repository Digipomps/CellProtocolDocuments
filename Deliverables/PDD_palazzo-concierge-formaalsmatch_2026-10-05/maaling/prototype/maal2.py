# -*- coding: utf-8 -*-
"""Mål prototypen mot en sølvfasit for et navngitt korpus (brukt for tillegget fra nye skribenter).
Bruk: maal2.py <datafil> <korpus.jsonl> <solv.jsonl> [alle|trening]
«alle» skriver ETT samlet tall for hele settet (lov for en datafil som var frosset før setningene ble skrevet);
«trening» skriver tall for treningsradene og lar radene som feiler der, hentes av den som kaller.
Rader merket holdout skrives aldri ut, og det skrives ingen tall for dem alene."""
import json, sys, collections
import husgraf, dekomp
NEG = set(dekomp.NEGATIVE)
import stier
KAT = json.load(open(stier.KATALOG, encoding="utf-8"))
def katalognoder():
    ut = set()
    for navn in ("retter", "drikke", "emner", "allergener"):
        for r in KAT[navn]: ut.add(r["node"])
    return ut
def maal(grafsti, korpussti, solvsti, utvalg="trening"):
    data = json.load(open(grafsti, encoding="utf-8"))
    g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
    kjente = katalognoder()
    kor = {}
    for l in open(korpussti, encoding="utf-8"):
        r = json.loads(l); kor[r["id"]] = r
    solv = [json.loads(l) for l in open(solvsti, encoding="utf-8")]
    res = collections.Counter(); feil = []; maal.siste = {}
    for s in solv:
        if utvalg == "trening" and s["holdout"]: continue
        d = dekomp.dekomponer(kor[s["id"]]["tekst"], g, sp)
        f = dekomp.merkelapp(d)
        f_ok = f == s["formaal"]
        fas = {(n["node"], n["negativ"]) for n in s["noder"] if n["node"] != "ukjent"}
        fikk = {(n["node"], n["slag"] in NEG) for n in d["noder"] if n["node"] in kjente}
        n_ok = fas == fikk
        nokler = [("alle", "alle")]
        if utvalg == "trening": nokler += [("kilde", kor[s["id"]].get("skribent") or s["kilde"]), ("formaal", s["formaal"])]
        for k in nokler:
            res[k + ("n",)] += 1; res[k + ("f",)] += f_ok; res[k + ("nd",)] += n_ok; res[k + ("b",)] += (f_ok and n_ok)
        if not s["holdout"]: maal.siste[s["id"]] = (f_ok and n_ok)
        if not s["holdout"] and not (f_ok and n_ok):
            feil.append((s, d, kor[s["id"]]["tekst"], f_ok, n_ok, f))
    return res, feil, data.get("versjon")
def skriv(res, merke):
    for k in sorted({x[:2] for x in res}, key=lambda x: (x[0] != "alle", x[0], x[1])):
        n = res[k + ("n",)]
        print("%-8s %-8s %-14s n=%3d  formål %3d (%5.1f %%)  noder %3d (%5.1f %%)  begge %3d (%5.1f %%)" % (merke, k[0], k[1], n, res[k+("f",)], 100*res[k+("f",)]/n, res[k+("nd",)], 100*res[k+("nd",)]/n, res[k+("b",)], 100*res[k+("b",)]/n))
if __name__ == "__main__":
    utvalg = sys.argv[4] if len(sys.argv) > 4 else "trening"
    res, feil, versjon = maal(sys.argv[1], sys.argv[2], sys.argv[3], utvalg)
    print("datafil:", versjon, "| utvalg:", utvalg)
    skriv(res, utvalg)
