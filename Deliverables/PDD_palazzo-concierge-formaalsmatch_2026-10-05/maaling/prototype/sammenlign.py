# -*- coding: utf-8 -*-
"""Hvilke TRENINGSRADER endrer seg mellom to datafiler: rettet (feil -> riktig) og ødelagt (riktig -> feil)."""
import sys, maal
fa, alle_a, ra = maal.maal(sys.argv[1], stille=True); fb, alle_b, rb = maal.maal(sys.argv[2], stille=True)
kor, solv = maal.les()
trening = {s["id"] for s in solv if not s["holdout"]}
rettet = [i for i in trening if not all(alle_a[i]) and all(alle_b[i])]
odelagt = [i for i in trening if all(alle_a[i]) and not all(alle_b[i])]
for navn, r in (("før", ra), ("etter", rb)):
    k = ("trening", "alle", "alle"); n = r[k + ("n",)]
    print("%-6s trening n=%d formål %.1f %% noder %.1f %% begge %.1f %%" % (navn, n, 100*r[k+("f",)]/n, 100*r[k+("nd",)]/n, 100*r[k+("b",)]/n))
print("rettet:", len(rettet), sorted(rettet)); print("ødelagt:", len(odelagt))
feil_b = {x[0]["id"]: x for x in fb}
for i in sorted(odelagt):
    s, d, t, f_ok, n_ok, f = feil_b[i]
    print("  ØDELAGT %s | %s" % (i, t[:140]))
    print("      fasit %s %s" % (s["formaal"], sorted(("-" if x["negativ"] else "+") + x["node"] for x in s["noder"])))
    print("      fikk  %s %s %s" % (f, sorted(("-" if x["slag"] in maal.NEG else "+") + x["node"] + "(" + x["ord"] + ")" for x in d["noder"]), d["klasser"]))
