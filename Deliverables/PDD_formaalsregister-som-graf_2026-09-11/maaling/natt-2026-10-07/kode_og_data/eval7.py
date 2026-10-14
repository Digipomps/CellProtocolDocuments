# -*- coding: utf-8 -*-
"""Måleharness for 2026-10-07-natten. Ren stdlib.

Korpus: gen/<skribent>.json (rådgiver-personaer), gen/N*.json (negativer), tolket blindt av Fable (tolk/*.json).
Delinger etter SKRIBENT, ikke tilfeldig: T1–T3 trening, T4 utvikling (velge varianter), S1–S4 + NS forseglet.
"""
from __future__ import annotations
import json, math, random, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import natt_trening as T

U = "purpose://prompt.unknown"
NEG = "NEG"
SEED = 20261007

TRAIN = ["T1", "T2", "T3"]
DEV = ["T4"]
SEALED = ["S1", "S2", "S3", "S4"]


def load_maal():
    tg = json.load(open(HERE / "maal_v1.json", encoding="utf-8"))
    return {x["code"]: x for x in tg}


def load_tolk():
    out = {}
    d = HERE / "tolk"
    if d.exists():
        for f in sorted(d.glob("*.json")):
            for r in json.load(open(f, encoding="utf-8")):
                out[r["id"]] = r
    return out


def load_set(writers, neg_file=None, silver=True, neg_part=None):
    """Rader: dict(id, writer, flate, tekst, gold, stil, tolk_enig).
    gold = purpose-ref for ekte, NEG for negativer. silver=True: bare rader der Fable valgte samme som generatoren
    (for negativer: Fable valgte INGEN/UKLART)."""
    maal = load_maal(); tolk = load_tolk(); rows = []
    for w in writers:
        for i, r in enumerate(json.load(open(HERE / "gen" / f"{w}.json", encoding="utf-8"))):
            rid = f"{w}-{i:03d}"
            m = maal.get(r["code"])
            if not m: continue
            tk = tolk.get(rid)
            agree = (tk is not None and tk.get("valg") == m["ref"])
            rows.append({"id": rid, "writer": w, "flate": r["flate"], "tekst": r["tekst"], "gold": m["ref"],
                         "stil": r.get("stil", ""), "tolk": tk, "enig": agree})
    if neg_file:
        for i, r in enumerate(json.load(open(HERE / "gen" / f"{neg_file}.json", encoding="utf-8"))):
            rid = f"{neg_file}-{i:03d}"
            if neg_part == "even" and i % 2: continue
            if neg_part == "odd" and not i % 2: continue
            tk = tolk.get(rid)
            agree = tk is not None and tk.get("valg") in (NEG, "INGEN", "UKLART", None)
            rows.append({"id": rid, "writer": neg_file, "flate": r["flate"], "tekst": r["tekst"], "gold": NEG,
                         "stil": r.get("type", ""), "tolk": tk, "enig": agree})
    if silver:
        rows = [r for r in rows if r["enig"] or r["tolk"] is None]
    return rows


# ---------------------------------------------------------------- metrikk
def run(pred_fn, rows, tau, nodes=None, accept=None):
    """pred_fn(flate, tekst) -> rangert [(ref, score)]. accept: ref -> sett av godtatte refs (etikett-kart)."""
    res = []
    for r in rows:
        ranked = pred_fn(r["flate"], r["tekst"])
        best = ranked[0] if ranked else (U, 0.0)
        pred = best[0] if best[1] >= tau else U
        top3 = [x for x, _ in ranked[:3]] if best[1] >= tau else []
        ok_set = accept(r) if accept else {r["gold"]}
        if r["gold"] == NEG:
            hit = pred == U; hit3 = hit
        else:
            hit = pred in ok_set; hit3 = any(x in ok_set for x in top3)
        res.append({"id": r["id"], "writer": r["writer"], "gold": r["gold"], "pred": pred, "score": round(best[1], 3),
                    "hit": hit, "hit3": hit3, "neg": r["gold"] == NEG, "stil": r["stil"], "tekst": r["tekst"], "flate": r["flate"]})
    return res


def summary(res):
    real = [x for x in res if not x["neg"]]; neg = [x for x in res if x["neg"]]
    s = {"n_real": len(real), "n_neg": len(neg),
         "top1": sum(x["hit"] for x in real) / max(1, len(real)),
         "top3": sum(x["hit3"] for x in real) / max(1, len(real)),
         "unknown_on_real": sum(x["pred"] == U for x in real) / max(1, len(real)),
         "neg_false_accept": sum(not x["hit"] for x in neg) / max(1, len(neg))}
    s["balanced"] = s["top1"] - s["neg_false_accept"]
    return s


def ci(res, key="hit", iters=2000, seed=SEED):
    real = [1 if x[key] else 0 for x in res if not x["neg"]]
    if not real: return (0, 0)
    rnd = random.Random(seed); vals = []
    for _ in range(iters):
        smp = [real[rnd.randrange(len(real))] for _ in real]; vals.append(sum(smp) / len(smp))
    vals.sort(); return (round(vals[int(.025 * iters)], 3), round(vals[int(.975 * iters)], 3))


def mcnemar(a, b):
    """Eksakt tosidig McNemar på ekte rader, a og b er run()-resultater over samme rader."""
    bb = sum(1 for x, y in zip(a, b) if not x["neg"] and x["hit"] and not y["hit"])
    cc = sum(1 for x, y in zip(a, b) if not x["neg"] and not x["hit"] and y["hit"])
    n = bb + cc
    if n == 0: return bb, cc, 1.0
    k = min(bb, cc)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return bb, cc, min(1.0, 2 * p)


MAX_FA = 0.10   # forhåndsbestemt 2026-10-07 før dev ble brukt: høyeste top1 med negFA <= 10 % på trening

def choose_tau(pred_fn, rows, grid=None, max_fa=MAX_FA):
    grid = grid or ([round(0.05 * i, 2) for i in range(0, 30)] + [round(1.5 + 0.1 * i, 2) for i in range(0, 36)])
    best = (grid[-1], -9)
    for tau in grid:
        s = summary(run(pred_fn, rows, tau))
        if s["neg_false_accept"] <= max_fa + 1e-9 and s["top1"] > best[1] + 1e-9: best = (tau, s["top1"])
    return best[0]


def fmt(s, c=None):
    t = f"top1={s['top1']:.3f} top3={s['top3']:.3f} negFA={s['neg_false_accept']:.3f} unk={s['unknown_on_real']:.3f} n={s['n_real']}/{s['n_neg']}"
    if c: t += f" CI{list(c)}"
    return t


# ---------------------------------------------------------------- frossen R4 (natt 23.9) på gammelt register
def make_r4_frozen():
    nodes = T.load_union(); ch = T.children_map(nodes)
    idx = T.TfIdf({r: T.node_text(n) for r, n in nodes.items()})
    from natt_korpus import FLATE_SKOP  # noqa
    def f(flate, text):
        sc = T.add(T.m_tfidf_alias_boost(nodes, text, idx), T.qword_prior_specific(text))
        return T.rank(T.apply_scope_mult(nodes, sc, flate, ch, text, gain=3.0)[0], nodes, exclude_facet=True)
    return f, nodes, 0.15


def train_rows(silver=True): return load_set(TRAIN, "NT", silver, "even")
def dev_rows(silver=True): return load_set(DEV, "NT", silver)
def sealed_rows(silver=True): return load_set(SEALED, "NS", silver)
