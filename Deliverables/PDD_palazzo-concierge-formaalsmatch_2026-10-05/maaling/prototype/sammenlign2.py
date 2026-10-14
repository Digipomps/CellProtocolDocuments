# -*- coding: utf-8 -*-
"""Hvilke TRENINGSRADER endrer seg mellom to datafiler, i begge korpusene: rettet og ødelagt.
Avholdte rader måles ikke her. Bruk: sammenlign2.py <før> <etter> [vis]"""
import sys, maal2
import stier
SETT = [("korpus 1", stier.SETNINGER, stier.FASIT),
        ("korpus 2", stier.SETNINGER2, stier.FASIT2)]
def kjoer(fil):
    ut = {}
    for navn, kor, solv in SETT:
        res, feil, versjon = maal2.maal(fil, kor, solv, "trening")
        ut[navn] = (res, dict(maal2.maal.siste), {x[0]["id"]: x for x in feil})
    return ut
if __name__ == "__main__":
    a = kjoer(sys.argv[1]); b = kjoer(sys.argv[2]); vis = len(sys.argv) > 3
    for navn, _, _ in SETT:
        ra, sa, fa = a[navn]; rb, sb, fb = b[navn]
        k = ("alle", "alle"); n = ra[k + ("n",)]
        rettet = sorted(i for i in sa if not sa[i] and sb[i]); odelagt = sorted(i for i in sa if sa[i] and not sb[i])
        print("%s trening n=%d: %d (%.1f %%) -> %d (%.1f %%) | rettet %d, ødelagt %d" % (navn, n, ra[k+("b",)], 100*ra[k+("b",)]/n, rb[k+("b",)], 100*rb[k+("b",)]/n, len(rettet), len(odelagt)))
        for i in odelagt:
            s, d, t, f_ok, n_ok, f = fb[i]
            print("  ØDELAGT %s | %s" % (i, t[:150]))
            print("      fasit %s %s" % (s["formaal"], sorted(("-" if x["negativ"] else "+") + x["node"] for x in s["noder"])))
            print("      fikk  %s %s" % (f, sorted(("-" if x["slag"] in maal2.NEG else "+") + x["node"] + "(" + x.get("ord", "") + ")" for x in d["noder"])))
        if vis:
            for i in rettet: print("  rettet", i)
