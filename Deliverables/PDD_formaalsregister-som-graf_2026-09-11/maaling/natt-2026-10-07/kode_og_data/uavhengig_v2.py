# Frossen R4 (og senere varianter) på butler-trådens uavhengige korpus v2 (264 meldinger, fire nye skribenter).
# Etikett: generatorens etikett der Haiku-tolken var enig (sølv), ellers gull hvis dømt; resten utelates.
import json, sys
from pathlib import Path
import eval7 as E
HERE = Path(__file__).resolve().parent
KD = json.load(open(HERE / "etikett_kart_butler_v2.json")); K = KD["kart"]

def rows(frossen=False):
    fas = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "fasit-v2.jsonl")}
    out = []; dropped = 0
    for l in open(HERE / "korpus-v2.jsonl"):
        r = json.loads(l); f = fas[r["id"]]
        lab = f.get("goldLabel") or (f["silverLabel"] if f["agreement"] else None)
        if lab is None: dropped += 1; continue
        m = K[lab]
        if frossen and lab in KD["kart_frossen_tillegg"]: m = m + KD["kart_frossen_tillegg"][lab]
        kind = {"NEG": "neg", "HULL": "hull", "UMULIG": "umulig"}.get(m if isinstance(m, str) else "", "ekte")
        out.append({"id": r["id"], "writer": r["generatedBy"], "flate": "butler", "tekst": r["text"], "label": lab,
                    "gold": E.NEG if kind != "ekte" else m[0], "accept": set(m) if kind == "ekte" else set(), "kind": kind,
                    "stil": r["style"]})
    return out, dropped

def score(fn, tau, rs):
    ekte = [r for r in rs if r["kind"] == "ekte"]; neg = [r for r in rs if r["kind"] == "neg"]; hull = [r for r in rs if r["kind"] == "hull"]
    def pred(r):
        rk = fn(r["flate"], r["tekst"]); b = rk[0] if rk else (E.U, 0)
        return b[0] if b[1] >= tau else E.U, [x for x, _ in rk[:3]] if b[1] >= tau else []
    res = {}
    P = {r["id"]: pred(r) for r in rs}
    res["ekte_n"] = len(ekte); res["top1"] = sum(P[r["id"]][0] in r["accept"] for r in ekte) / len(ekte)
    res["top3"] = sum(any(x in r["accept"] for x in P[r["id"]][1]) for r in ekte) / len(ekte)
    act = lambda p: p.startswith("purpose://conversation")
    res["neg_n"] = len(neg); res["neg_FA"] = sum(P[r["id"]][0] != E.U and not act(P[r["id"]][0]) for r in neg) / len(neg)
    res["neg_FA_streng"] = sum(P[r["id"]][0] != E.U for r in neg) / len(neg)
    um = [r for r in rs if r["kind"] == "umulig"]; res["umulig_n"] = len(um); res["umulig_forslag"] = [P[r["id"]][0] for r in um]
    res["hull_n"] = len(hull); res["hull_forslag"] = sum(P[r["id"]][0] != E.U for r in hull) / len(hull)
    res["per_label"] = {}
    for r in ekte:
        a = res["per_label"].setdefault(r["label"], [0, 0]); a[0] += P[r["id"]][0] in r["accept"]; a[1] += 1
    res["hits"] = {r["id"]: P[r["id"]][0] in r["accept"] for r in ekte}
    res["pred"] = {r["id"]: P[r["id"]][0] for r in rs}
    return res

if __name__ == "__main__":
    rs, dropped = rows(frossen=True)
    fn, nodes, tau = E.make_r4_frozen()
    s = score(fn, tau, rs)
    print("utelatt (uenig tolk, ikke dømt):", dropped)
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items() if k not in ("hits", "pred", "per_label")})
    print({k: f"{a}/{b}" for k, (a, b) in sorted(s["per_label"].items())})
    json.dump({"R4_frossen": {k: v for k, v in s.items() if k != "hits"}}, open(HERE / "uavhengig_v2_R4.json", "w"), ensure_ascii=False, indent=1, default=list)
