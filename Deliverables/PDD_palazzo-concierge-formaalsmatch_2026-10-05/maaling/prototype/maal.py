# -*- coding: utf-8 -*-
"""Mål prototypen mot sølvfasiten. Holdout skrives bare ut når HOLDOUT=1 er satt (det gjøres ikke under justering)."""
import json, sys, os, collections
import husgraf, dekomp
NEG = set(dekomp.NEGATIVE)
import stier
KAT = json.load(open(stier.KATALOG, encoding="utf-8"))
def katalognoder():
    ut = set()
    for navn in ("retter", "drikke", "emner", "allergener"):
        for r in KAT[navn]: ut.add(r["node"])
    return ut
def les():
    kor = {}
    for l in open(stier.SETNINGER, encoding="utf-8"):
        r = json.loads(l); kor[r["id"]] = r
    solv = [json.loads(l) for l in open(stier.FASIT, encoding="utf-8")]
    return kor, solv
def maal(grafsti, stille=False):
    data = json.load(open(grafsti, encoding="utf-8"))
    g = husgraf.Graf(data, json.load(open(husgraf.KORPUS, encoding="utf-8"))); sp = dekomp.Spraak(data)
    kjente = katalognoder()
    kor, solv = les()
    res = collections.Counter(); feil = []; alle = {}
    for s in solv:
        del_ = "holdout" if s["holdout"] else "trening"
        d = dekomp.dekomponer(kor[s["id"]]["tekst"], g, sp)
        f = dekomp.merkelapp(d)
        f_ok = f == s["formaal"]
        fas = {(n["node"], n["negativ"]) for n in s["noder"] if n["node"] != "ukjent"}
        # noder tolken ikke hadde i katalogen sin, telles verken for eller mot
        fikk = {(n["node"], n["slag"] in NEG) for n in d["noder"] if n["node"] in kjente}
        n_ok = fas == fikk
        for k in (("alle", "alle"), ("kilde", s["kilde"]), ("formaal", s["formaal"])):
            res[(del_,) + k + ("n",)] += 1; res[(del_,) + k + ("f",)] += f_ok; res[(del_,) + k + ("nd",)] += n_ok; res[(del_,) + k + ("b",)] += (f_ok and n_ok)
        alle[s["id"]] = (f_ok, n_ok)
        if del_ == "trening" and not (f_ok and n_ok):
            feil.append((s, d, kor[s["id"]]["tekst"], f_ok, n_ok, f))
    if not stille:
        for del_ in (("trening", "holdout") if os.environ.get("HOLDOUT") == "1" else ("trening",)):
            for k in sorted({x[:3] for x in res if x[0] == del_}, key=lambda x: (x[1] != "alle", x[1], x[2])):
                n = res[k + ("n",)]
                print("%-8s %-8s %-12s n=%3d  formål %5.1f %%  noder %5.1f %%  begge %5.1f %%" % (k[0], k[1], k[2], n, 100*res[k+("f",)]/n, 100*res[k+("nd",)]/n, 100*res[k+("b",)]/n))
    return feil, alle, res
if __name__ == "__main__":
    feil, alle, res = maal(sys.argv[1])
    c = collections.Counter((s["formaal"], f) for s, d, t, f_ok, n_ok, f in feil if not f_ok)
    print("feil formål (fasit, fikk), trening:", sorted(c.items(), key=lambda kv: -kv[1])[:20])
