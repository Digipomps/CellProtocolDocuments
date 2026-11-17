# -*- coding: utf-8 -*-
"""Feil på TRENINGSRADER: python3 vis.py <graf> <filter> [fra] [til]
filter: kilde=<k> | formaal=<fasit>:<fikk> | noder (riktig formål, feil noder) | alle"""
import sys
import maal
feil, alle, res = maal.maal(sys.argv[1], stille=True)
filt = sys.argv[2] if len(sys.argv) > 2 else "alle"
a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
b = int(sys.argv[4]) if len(sys.argv) > 4 else 10**6
NEG = maal.NEG
def med(x):
    s, d, t, f_ok, n_ok, f = x
    if filt == "alle": return True
    if filt == "noder": return f_ok and not n_ok
    if filt.startswith("kilde="): return s["kilde"] == filt[6:]
    if filt.startswith("formaal="):
        fa, fi = filt[8:].split(":")
        return (not f_ok) and (fa in ("*", s["formaal"])) and (fi in ("*", f))
    return False
ut = [x for x in feil if med(x)]
print(len(ut), "feil,", filt)
kort = lambda n: n.replace("emne:", "e:").replace("allergen:", "A:").replace("menu-", "m-").replace("bev-", "b-")
for s, d, t, f_ok, n_ok, f in ut[a:b]:
    fa = " ".join(sorted(("-" if x["negativ"] else "+") + kort(x["node"]) for x in s["noder"]))
    fi = " ".join(sorted(("-" if x["slag"] in NEG else "+") + kort(x["node"]) + "(" + x["ord"] + ")" for x in d["noder"]))
    print("%s|%s" % (s["id"], t[:150]))
    print("     F %-11s %s   %s" % (s["formaal"], fa, ("ukj:" + ",".join(s.get("ukjent_ord") or [])) if s.get("ukjent_ord") else ""))
    print("     D %-11s %s   %s" % (f + ("" if f_ok else " ✗"), fi, ",".join(d["klasser"])))
