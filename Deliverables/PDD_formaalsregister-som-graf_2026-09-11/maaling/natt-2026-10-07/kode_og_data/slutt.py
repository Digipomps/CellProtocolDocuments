# -*- coding: utf-8 -*-
"""Sluttmåling. Kjøres ÉN gang etter at varianten og terskelen er frosset (VALGT.json).
Terskel: satt på utviklingssettene (ikke forseglet) ved negFA <= 10 %, lagret i VALGT.json før denne kjøres."""
import json, sys, hashlib
from collections import defaultdict
from pathlib import Path
import eval7 as E, abl4, curve, kjetil_sett as K, uavhengig_v2 as B, register_v1 as R

HERE = Path(__file__).resolve().parent
V = json.load(open(HERE / "VALGT.json"))
ACT = "purpose://conversation"


def check_seal():
    want = {l.split()[1]: l.split()[0] for l in open(HERE / "FORSEGLET_sha256.txt") if l.strip() and "gen/" in l}
    for f, h in want.items():
        got = hashlib.sha256(open(HERE / f, "rb").read()).hexdigest()
        assert got == h, f"forseglet fil endret: {f}"
    return len(want)


def evalset(m, tau, rows):
    out = []
    for r in rows:
        rk = m(r["flate"], r["tekst"]); b = rk[0] if rk else (E.U, 0.0)
        p = b[0] if b[1] >= tau else E.U
        if r["gold"] == E.NEG:
            hit = p == E.U or p.startswith(ACT); strict = p == E.U
        else:
            hit = p == r["gold"]; strict = hit
        out.append({"id": r["id"], "writer": r["writer"], "stil": r["stil"], "neg": r["gold"] == E.NEG, "hit": hit,
                    "strict": strict, "pred": p, "gold": r["gold"], "tekst": r["tekst"], "score": round(b[1], 3)})
    return out


def summ(res):
    real = [x for x in res if not x["neg"]]; neg = [x for x in res if x["neg"]]
    return {"n_ekte": len(real), "n_neg": len(neg),
            "top1": round(sum(x["hit"] for x in real) / max(1, len(real)), 3),
            "ci95": E.ci(res), "negFA_flate": round(sum(not x["hit"] for x in neg) / max(1, len(neg)), 3),
            "negFA_streng": round(sum(not x["strict"] for x in neg) / max(1, len(neg)), 3)}


def by(res, key):
    d = defaultdict(list)
    for x in res: d[x[key]].append(x)
    return {k: summ(v) for k, v in sorted(d.items())}


def main():
    n_sealed = check_seal()
    fn, _, tau4 = E.make_r4_frozen()
    m = abl4.build(**V["build"]); tau = V["tau"]
    out = {"valgt": V, "forseglede_filer_kontrollert": n_sealed}
    for silver in (True, False):
        rows = E.sealed_rows(silver)
        a = evalset(fn, tau4, rows); b = evalset(m, tau, rows)
        key = "forseglet_soelv" if silver else "forseglet_alle"
        bb, cc, p = E.mcnemar([dict(x, neg=x["neg"]) for x in a], [dict(x, neg=x["neg"]) for x in b])
        out[key] = {"R4": summ(a), "R5": summ(b), "mcnemar": {"R4_vant": bb, "R5_vant": cc, "p": p},
                    "R5_per_skribent": by(b, "writer"), "R4_per_skribent": by(a, "writer"),
                    "R5_per_stil": by(b, "stil"), "R4_per_stil": by(a, "stil")}
        if silver:
            out[key]["R5_bom"] = [x for x in b if not x["hit"]][:400]
    # kurve på forseglet (rapport, ikke valg)
    rows = E.sealed_rows(True)
    out["forseglet_kurve"] = {"R4": curve.curve(fn, rows), "R5": curve.curve(m, rows)}
    # butler v2 uavhengig
    rs, dropped = B.rows(frossen=False); rs4, _ = B.rows(frossen=True)
    s4 = B.score(fn, tau4, rs4); s5 = B.score(m, tau, rs)
    strip = lambda s: {k: v for k, v in s.items() if k not in ("hits", "pred")}
    out["butler_v2"] = {"R4": strip(s4), "R5": strip(s5), "utelatt": dropped}
    # Kjetils egne ord
    out["kjetil"] = {}
    for kind in ("ytring", "fritekst"):
        rs = K.rows(kind)
        out["kjetil"][kind] = {"R4": K.score(fn, rs, tau4)[0], "R5": K.score(m, rs, tau)[0]}
    json.dump(out, open(HERE / "SLUTT_resultat.json", "w"), ensure_ascii=False, indent=1, default=list)
    for k in ("forseglet_soelv", "forseglet_alle"):
        print(k, "R4", out[k]["R4"], "\n   R5", out[k]["R5"], "\n   McNemar", out[k]["mcnemar"])
    print("kurve", out["forseglet_kurve"])
    print("butler_v2 R4", {k: v for k, v in out["butler_v2"]["R4"].items() if k != "per_label"})
    print("butler_v2 R5", {k: v for k, v in out["butler_v2"]["R5"].items() if k != "per_label"})
    print("kjetil", out["kjetil"])


if __name__ == "__main__":
    main()
