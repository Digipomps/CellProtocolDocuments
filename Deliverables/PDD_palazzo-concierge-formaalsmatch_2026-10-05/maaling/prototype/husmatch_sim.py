# -*- coding: utf-8 -*-
"""Etterregning av matchen (pakke 4) utenfor Swift: samme regning som PalazzoSignalGraph.contributions
med vekter på kantene. Brukes bare til å kontrollere forventningene i PalazzoHusmatchTests."""
import json, sys, unicodedata, re

def tok(s, hard=False):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    if hard:
        s = s.replace("ø", "o").replace("æ", "ae")
    s = "".join(c if c.isalnum() else " " for c in s)
    return "".join(s.split())

def last(sti):
    d = json.load(open(sti, encoding="utf-8"))
    g = d["graf"]
    poster = {}
    for del_ in ("retter", "drikke"):
        for pid, kanter in g[del_].items():
            poster[pid] = [(k["emne"], k["vekt"]) for k in kanter]
    return d["versjon"], g["terskel"], poster

def match(poster, terskel, interesser, own=1.0, negskala=1.0):
    """interesser: [(emne, negativ)] -> [(post, sum, [(emne, bidrag, negativ)])] sortert."""
    ut = []
    for pid, kanter in poster.items():
        if not kanter: continue
        w = {}
        for e, v in kanter: w[tok(e)] = v
        tags = set(w)
        total = sum(w[t] for t in sorted(tags))
        if total <= 0: continue
        bidrag = []
        for emne, neg in interesser:
            t = tok(emne)
            if t not in tags: continue
            vekt = -own if neg else own
            score = vekt * w[t] / total * (negskala if neg else 1.0)
            bidrag.append((emne, score, neg))
        if not any(not b[2] for b in bidrag): continue
        s = sum(b[1] for b in bidrag)
        if s < terskel: continue
        ut.append((pid, s, bidrag))
    ut.sort(key=lambda x: (-x[1], x[0]))
    return ut

if __name__ == "__main__":
    for sti in sys.argv[1:]:
        versjon, terskel, poster = last(sti)
        print("==", versjon, "terskel", terskel, "poster med kanter:", sum(1 for k in poster.values() if k), "av", len(poster))
        # kontroller: ingen post har samme emne to ganger, og ingen to emner blir samme token
        alle = sorted({e for k in poster.values() for e, _ in k})
        for hard in (False, True):
            sett = {}
            for e in alle: sett.setdefault(tok(e, hard), []).append(e)
            koll = {t: v for t, v in sett.items() if len(v) > 1}
            print("   emner med kant:", len(alle), "| token-kollisjoner (hard=%s):" % hard, koll)
        for pid, k in poster.items():
            em = [e for e, _ in k]
            if len(em) != len(set(em)): print("   DOBBEL KANT", pid, em)
        def vis(navn, inn):
            r = match(poster, terskel, inn)
            print("  %-22s -> %s" % (navn, [(p, round(s, 4)) for p, s, _ in r]))
            return r
        vis("ost", [("ost", False)])
        vis("dessert", [("dessert", False)])
        vis("dessert, -ost", [("dessert", False), ("ost", True)])
        vis("-ost", [("ost", True)])
        vis("pistasj", [("pistasj", False)])
        vis("pistasj, dessert", [("pistasj", False), ("dessert", False)])
        vis("eple", [("eple", False)])
        r = vis("øl", [("øl", False)])
        print("     antall øl:", len(r))
