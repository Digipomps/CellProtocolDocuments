#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nattens formålsmatching-trening: hypotese -> mål -> juster -> iterer. Ren stdlib.

Alle tall skrives til natt_resultater.json. Ingen matcher ser gold-etikettene under
scoring; vekter/terskler velges bare på TRENING-delen, rapporteres på HOLDOUT.
"""
from __future__ import annotations
import json, math, random, re, sys, statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from natt_korpus import KORPUS, FLATE_SKOP, U as UNKNOWN

SEED = 20260923
random.seed(SEED)

# ---------------------------------------------------------------- taksonomi
def load_union():
    b = json.load(open(HERE / "book_taxonomy.json", encoding="utf-8"))
    r = json.load(open(HERE / "runtime_taxonomy.json", encoding="utf-8"))
    k = json.load(open(HERE / "kallimachos_taxonomy.json", encoding="utf-8"))
    nodes = {}
    for n in b:
        nodes[n["ref"]] = {"ref": n["ref"], "parent": n.get("parent"), "title": n["title"], "desc": n.get("desc", ""),
                           "aliases": list((n.get("hints") or {}).get("aliases", [])),
                           "tokens": list((n.get("hints") or {}).get("tokens", [])),
                           "signals": list(((n.get("goal") or {}).get("successSignals") or [])),
                           "outcome": ((n.get("goal") or {}).get("outcome") or ""), "src": "B"}
    for n in r:
        if n["ref"] in nodes:
            nodes[n["ref"]]["desc"] = (nodes[n["ref"]]["desc"] + " " + n.get("desc", "")).strip()
            nodes[n["ref"]]["src"] += "R"
            for a in n.get("aliases", []): nodes.setdefault(a, None)
        else:
            nodes[n["ref"]] = {"ref": n["ref"], "parent": n.get("parent"), "title": n["title"], "desc": n.get("desc", ""),
                               "aliases": [], "tokens": [], "signals": [], "outcome": "", "src": "R"}
    for n in k:
        if n["ref"] in nodes:
            nodes[n["ref"]]["src"] += "K"; continue
        nodes[n["ref"]] = {"ref": n["ref"], "parent": n.get("parent"), "title": n["title"], "desc": n.get("desc", "") or "",
                           "aliases": list((n.get("hints") or {}).get("aliases", [])),
                           "tokens": list((n.get("hints") or {}).get("tokens", [])),
                           "signals": [], "outcome": "", "src": "K"}
    nodes = {k_: v for k_, v in nodes.items() if v}
    # facet-only (INN-IA) per forsoningen: analysis.* unntatt decision-support; capability.* unntatt request-human-review og request-new-functionality
    for ref, n in nodes.items():
        ia = (ref.startswith("purpose://analysis.") and ref != "purpose://analysis.decision-support") or \
             (ref.startswith("purpose://capability.") and ref not in ("purpose://capability.request-human-review", "purpose://capability.request-new-functionality"))
        n["facetOnly"] = ia
    return nodes

# ---------------------------------------------------------------- tekst
WORD = re.compile(r"[a-zæøåäöüéè0-9]+")
STOP = set("og i på til av for med en et det er som at kan du jeg vi de den dette om ikke skal vil har hva hvor hvem hvordan hvorfor når mine min mitt meg seg the a an of to in on for and or is are be it this that with my me you your".split())

def tok(text: str):
    out = []
    for w in WORD.findall(text.lower()):
        if w in STOP or len(w) < 2: continue
        out.append(w[:7] if len(w) > 7 else w)
        if len(w) >= 6: out.append("~" + w[:5])   # grov norsk stamme
    return out

def node_text(n, use_hints=True, use_signals=True):
    parts = [n["title"], n["desc"]]
    if use_hints: parts += n["aliases"] + n["tokens"]
    if use_signals: parts += n["signals"] + [n["outcome"]]
    return " ".join(p for p in parts if p)

# ---------------------------------------------------------------- tf-idf
class TfIdf:
    def __init__(self, docs: dict):
        self.docs = docs
        self.tf = {r: Counter(tok(t)) for r, t in docs.items()}
        df = Counter()
        for c in self.tf.values(): df.update(c.keys())
        N = len(docs)
        self.idf = {w: math.log((N + 1) / (d + 1)) + 1 for w, d in df.items()}
        self.vec = {}
        for r, c in self.tf.items():
            v = {w: (1 + math.log(f)) * self.idf.get(w, 1.0) for w, f in c.items()}
            nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
            self.vec[r] = {w: x / nrm for w, x in v.items()}
    def query(self, text):
        q = Counter(tok(text))
        if not q: return {}
        qv = {w: (1 + math.log(f)) * self.idf.get(w, 1.0) for w, f in q.items()}
        nrm = math.sqrt(sum(x * x for x in qv.values())) or 1.0
        qv = {w: x / nrm for w, x in qv.items()}
        return {r: sum(qv[w] * v.get(w, 0.0) for w in qv) for r, v in self.vec.items()}

# ---------------------------------------------------------------- struktur
def ancestors(nodes, ref):
    out = []; cur = nodes.get(ref)
    while cur and cur.get("parent"):
        out.append(cur["parent"]); cur = nodes.get(cur["parent"])
    return out

def depth(nodes, ref): return len(ancestors(nodes, ref))

def children_map(nodes):
    ch = defaultdict(list)
    for r, n in nodes.items():
        if n.get("parent"): ch[n["parent"]].append(r)
    return ch

def subtree(nodes, roots, ch):
    seen = set(); stack = list(roots)
    while stack:
        r = stack.pop()
        if r in seen or r not in nodes: continue
        seen.add(r); stack.extend(ch.get(r, []))
    return seen

def coarse_of(nodes, ref, level=2):
    chain = [ref] + ancestors(nodes, ref)   # ref, parent, grandparent, ..., root
    # nivå 2 = barnebarn av root; velg det leddet som har dybde <= level
    for r in chain:
        if depth(nodes, r) <= level: return r
    return chain[-1]

# ---------------------------------------------------------------- matchere
def m_keyword(nodes, text, **kw):
    """M0: som dagens router — treff på hele ord fra tittel/alias, ingen vekting."""
    t = set(WORD.findall(text.lower()))
    sc = {}
    for r, n in nodes.items():
        words = set(WORD.findall((n["title"] + " " + " ".join(n["aliases"])).lower())) - STOP
        hit = len(t & words)
        if hit: sc[r] = float(hit)
    return sc

def m_tfidf(nodes, text, idx, **kw):
    return idx.query(text)

def m_tfidf_alias_boost(nodes, text, idx, boost=0.5, **kw):
    sc = idx.query(text); low = text.lower()
    for r, n in nodes.items():
        for a in n["aliases"]:
            if a and a.lower() in low:
                sc[r] = sc.get(r, 0.0) + boost
    return sc

def spread(nodes, sc, ch, up=0.5, down=0.3):
    out = dict(sc)
    for r, s in sc.items():
        if s <= 0: continue
        p = nodes[r].get("parent")
        if p in nodes: out[p] = out.get(p, 0.0) + s * up
        for c in ch.get(r, []): out[c] = out.get(c, 0.0) + s * down
    return out

def apply_scope(nodes, sc, flate, ch, text, w_fixed=None, adaptive=True, floor=0.0):
    roots = FLATE_SKOP.get(flate, [])
    inscope = subtree(nodes, roots, ch)
    ntok = len(tok(text))
    w = w_fixed if w_fixed is not None else (max(floor, 1.0 - min(1.0, ntok / 6.0)) if adaptive else 0.5)
    mx = max(sc.values()) if sc else 0.0
    out = {}
    for r in nodes:
        base = sc.get(r, 0.0)
        ctx = mx * 0.6 if r in inscope else 0.0
        out[r] = (1 - w) * base + w * ctx if mx > 0 else (1.0 if r in inscope else 0.0) * w
    return out, w

def apply_scope_mult(nodes, sc, flate, ch, text, adaptive=True, gain=1.0):
    """Skop MODULERER tekstbevis, skaper det aldri: score *= (1 + w*gain) innenfor skop. Null tekst -> null."""
    roots = FLATE_SKOP.get(flate, [])
    inscope = subtree(nodes, roots, ch)
    ntok = len(tok(text))
    w = (1.0 - min(1.0, ntok / 6.0)) if adaptive else 0.5
    return {r: (s * (1 + w * gain) if r in inscope else s) for r, s in sc.items()}, w

# Spørreord -> formålsfacett. Tabellen er avledet av Book 23s egne titler under self-determination.data
# (Duration, Recipients, Locality, Verifiability, Exercisability, Manner, Scope) og knowledge.explain-policy.
QWORD = {
    "hvor lenge": ["purpose://self-determination.data.duration"],
    "hvem": ["purpose://self-determination.data.recipients", "purpose://access.audit.privacy", "purpose://contact.introduction"],
    "hvor lagres": ["purpose://self-determination.data.locality"], "hvor er": ["purpose://self-determination.data.locality", "purpose://skeleton.owner-entity-access"],
    "hvordan vet": ["purpose://self-determination.data.verifiability", "purpose://test.acceptance"],
    "kan jeg": ["purpose://self-determination.data.exercisability"],
    "hvor mye": ["purpose://self-determination.data.scope"],
    "hva brukes": ["purpose://self-determination.data.use-purpose"], "til noe annet": ["purpose://self-determination.data.use-purpose"],
    "hvorfor": ["purpose://knowledge.explain-policy", "purpose://librarian.explain-haven"],
    "hva er": ["purpose://knowledge.explain-policy", "purpose://librarian.explain-haven"], "hva betyr": ["purpose://knowledge.explain-policy"],
    "hvordan virker": ["purpose://knowledge.explain-policy"], "forklar": ["purpose://knowledge.explain-policy", "purpose://librarian.explain-haven"],
    "slett": ["purpose://self-determination.data.duration", "purpose://librarian.requester-control"],
}
def qword_prior(text, weight=0.12):
    low = " " + text.lower() + " "; pri = {}
    for q, refs in QWORD.items():
        if (" " + q) in low or low.startswith(" " + q):
            for r in refs: pri[r] = pri.get(r, 0.0) + weight
    return pri

def add(a, b):
    o = dict(a)
    for k, v in b.items(): o[k] = o.get(k, 0.0) + v
    return o

def spread_capped(nodes, sc, ch, up=0.5, down=0.3):
    """Som spread, men en forelder får aldri overta sitt beste barn."""
    out = dict(sc)
    for r, s in sc.items():
        if s <= 0: continue
        p = nodes[r].get("parent")
        if p in nodes: out[p] = min(out.get(p, 0.0) + s * up, 0.9 * max(sc.get(c, 0.0) for c in ch.get(p, [r])) if ch.get(p) else out.get(p, 0.0) + s * up)
        for c in ch.get(r, []): out[c] = out.get(c, 0.0) + s * down
    return out

def lesson_text_by_purpose():
    # H8 leser nattens frosne snapshot (49 lærdommer) så tallene reproduseres bit for bit; faller tilbake til Book/ (levende register).
    f = HERE / "haven_lessons_register_v0.natt-snapshot.json"
    if not f.exists(): f = HERE.parents[3] / "Book" / "haven_lessons_register_v0.json"
    L = json.load(open(f, encoding="utf-8"))["lessons"]
    by = defaultdict(list)
    for l in L:
        t = " ".join([l.get("symptom", ""), l.get("cause", ""), l.get("prevention", "")])
        for p in l.get("purposeRefs", []): by[p].append(t)
    return {p: " ".join(v) for p, v in by.items()}

def qword_prior_specific(text, weight=0.12):
    """Vekt = weight / antall formål spørreordet peker på: et ord som kan bety tre ting er svakere bevis."""
    low = " " + text.lower() + " "; pri = {}
    for q, refs in QWORD.items():
        if (" " + q) in low:
            for r in refs: pri[r] = pri.get(r, 0.0) + weight / len(refs)
    return pri

def sibling_backoff(ranked, nodes, delta=0.05):
    """Er topp-2 søsken og marginen liten, svar med forelderen (grovere, men sannere)."""
    if len(ranked) < 2: return ranked
    (a, sa), (b, sb) = ranked[0], ranked[1]
    pa, pb = nodes.get(a, {}).get("parent"), nodes.get(b, {}).get("parent")
    if pa and pa == pb and (sa - sb) < delta and pa in nodes:
        return [(pa, sa)] + ranked
    return ranked

def adaptive_granularity(text, fine_fn, base_fn, f):
    return fine_fn(f, text) if len(tok(text)) <= 2 else base_fn(f, text)

def rank(sc, nodes, exclude_facet=False):
    items = [(r, s) for r, s in sc.items() if s > 0 and (not exclude_facet or not nodes[r]["facetOnly"])]
    return sorted(items, key=lambda x: (-x[1], x[0]))

# ---------------------------------------------------------------- granularitet
def make_fine(nodes):
    fine = {}
    for r, n in nodes.items():
        fine[r] = dict(n)
        sigs = n["signals"][:4] if n["signals"] else [s for s in re.split(r"(?<=[.;])\s+", n["desc"]) if len(s) > 20][:3]
        for i, s in enumerate(sigs):
            fr = f"{r}#{i+1}"
            fine[fr] = {"ref": fr, "parent": r, "title": n["title"], "desc": s, "aliases": [], "tokens": [], "signals": [], "outcome": "", "src": n["src"] + "f", "facetOnly": n["facetOnly"], "fine": True}
    return fine

def to_base(ref): return ref.split("#")[0]

# ---------------------------------------------------------------- evaluering
def evaluate(pred_fn, data, nodes, tau=None, coarse_level=None, label=""):
    top1 = mrr = 0; n_real = 0; fa = 0; n_decoy = 0; unk_real = 0; hier = 0
    per_len = defaultdict(lambda: [0, 0]); per_flate = defaultdict(lambda: [0, 0]); rows = []
    for flate, text, gold, lc in data:
        ranked = pred_fn(flate, text)
        ranked = [(to_base(r), s) for r, s in ranked]
        # dedup etter to_base, behold beste
        seen = set(); dd = []
        for r, s in ranked:
            if r not in seen: seen.add(r); dd.append((r, s))
        ranked = dd
        best = ranked[0] if ranked else (UNKNOWN, 0.0)
        pred = best[0] if (tau is None or best[1] >= tau) else UNKNOWN
        if gold == UNKNOWN:
            n_decoy += 1
            if pred != UNKNOWN: fa += 1
            rows.append((flate, text, gold, pred, round(best[1], 3))); continue
        n_real += 1
        if pred == UNKNOWN: unk_real += 1
        ok = pred == gold
        if coarse_level is not None:
            ok = coarse_of(nodes, pred, coarse_level) == coarse_of(nodes, gold, coarse_level) if pred != UNKNOWN else False
        top1 += ok
        per_len[lc][0] += ok; per_len[lc][1] += 1
        per_flate[flate][0] += ok; per_flate[flate][1] += 1
        if pred != UNKNOWN and (nodes.get(pred, {}).get("parent") == gold or nodes.get(gold, {}).get("parent") == pred or pred == gold): hier += 1
        for i, (r, s) in enumerate(ranked[:10]):
            if r == gold: mrr += 1 / (i + 1); break
        rows.append((flate, text, gold, pred, round(best[1], 3)))
    res = {"label": label, "n": n_real, "top1": top1 / max(1, n_real), "mrr10": mrr / max(1, n_real),
           "hier1": hier / max(1, n_real), "unknown_on_real": unk_real / max(1, n_real),
           "decoy_false_accept": fa / max(1, n_decoy), "n_decoy": n_decoy,
           "per_len": {k: v[0] / v[1] for k, v in per_len.items()},
           "per_flate": {k: v[0] / v[1] for k, v in per_flate.items()}}
    return res, rows

def bootstrap_ci(pred_fn, data, nodes, tau, iters=2000, seed=SEED):
    rnd = random.Random(seed); real = [d for d in data if d[2] != UNKNOWN]
    hits = []
    for flate, text, gold, lc in real:
        ranked = [(to_base(r), s) for r, s in pred_fn(flate, text)]
        best = ranked[0] if ranked else (UNKNOWN, 0.0)
        pred = best[0] if (tau is None or best[1] >= tau) else UNKNOWN
        hits.append(1 if pred == gold else 0)
    vals = []
    for _ in range(iters):
        smp = [hits[rnd.randrange(len(hits))] for _ in hits]
        vals.append(sum(smp) / len(smp))
    vals.sort(); return vals[int(0.025 * iters)], vals[int(0.975 * iters)]

def split(data, frac=0.6, seed=SEED):
    rnd = random.Random(seed); by = defaultdict(list)
    for d in data: by[(d[0], d[2] == UNKNOWN)].append(d)
    tr, ho = [], []
    for k, lst in by.items():
        lst = lst[:]; rnd.shuffle(lst); c = int(round(frac * len(lst)))
        tr += lst[:c]; ho += lst[c:]
    return tr, ho

def choose_tau(pred_fn, train, nodes):
    """Terskel valgt på trening: maksimer top1 - decoy_false_accept."""
    best = (None, -9)
    for tau in [0.0, 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30, 0.40]:
        r, _ = evaluate(pred_fn, train, nodes, tau=tau)
        score = r["top1"] - r["decoy_false_accept"]
        if score > best[1]: best = (tau, score)
    return best[0]

# ---------------------------------------------------------------- kjør
def main():
    nodes = load_union(); ch = children_map(nodes)
    fine = make_fine(nodes); chf = children_map(fine)
    coarse_refs = {r for r in nodes if depth(nodes, r) <= 2}
    coarse = {r: n for r, n in nodes.items() if r in coarse_refs}; chc = children_map(coarse)
    print(f"noder: union={len(nodes)} fine={len(fine)} coarse={len(coarse)}")

    idx_full = TfIdf({r: node_text(n) for r, n in nodes.items()})
    idx_nohints = TfIdf({r: node_text(n, use_hints=False) for r, n in nodes.items()})
    idx_fine = TfIdf({r: node_text(n) for r, n in fine.items()})
    idx_coarse = TfIdf({r: node_text(n) for r, n in coarse.items()})

    train, hold = split(KORPUS)
    print(f"trening={len(train)} holdout={len(hold)}")

    def P(fn): return fn
    cands = {}
    cands["M0 nøkkelord (som dagens router)"] = P(lambda f, t: rank(m_keyword(nodes, t), nodes))
    cands["M1 tf-idf tittel+desc, uten hints"] = P(lambda f, t: rank(m_tfidf(nodes, t, idx_nohints), nodes))
    cands["M2 tf-idf + hints (erklærte alias/tokens)"] = P(lambda f, t: rank(m_tfidf(nodes, t, idx_full), nodes))
    cands["M2b M2 + alias-boost"] = P(lambda f, t: rank(m_tfidf_alias_boost(nodes, t, idx_full), nodes))
    cands["M3 M2b + parentRef-spredning"] = P(lambda f, t: rank(spread(nodes, m_tfidf_alias_boost(nodes, t, idx_full), ch), nodes))
    cands["M4 M3 + skop fast 0.5"] = P(lambda f, t: rank(apply_scope(nodes, spread(nodes, m_tfidf_alias_boost(nodes, t, idx_full), ch), f, ch, t, w_fixed=0.5)[0], nodes))
    cands["M4a M3 + skop adaptiv (tynn tekst -> mer skop)"] = P(lambda f, t: rank(apply_scope(nodes, spread(nodes, m_tfidf_alias_boost(nodes, t, idx_full), ch), f, ch, t, adaptive=True)[0], nodes))
    cands["M5 M4a + facet-only ekskludert som primær"] = P(lambda f, t: rank(apply_scope(nodes, spread(nodes, m_tfidf_alias_boost(nodes, t, idx_full), ch), f, ch, t, adaptive=True)[0], nodes, exclude_facet=True))
    # granularitet
    cands["G-grov (dybde<=2, 1 nivå grovere)"] = P(lambda f, t: rank(apply_scope(coarse, spread(coarse, m_tfidf_alias_boost(coarse, t, idx_coarse), chc), f, chc, t, adaptive=True)[0], coarse, exclude_facet=True))
    cands["G-fin (blad splittet på successSignals)"] = P(lambda f, t: rank(apply_scope(fine, spread(fine, m_tfidf_alias_boost(fine, t, idx_fine), chf), f, chf, t, adaptive=True)[0], fine, exclude_facet=True))

    results = {"seed": SEED, "n_nodes": len(nodes), "n_fine": len(fine), "n_coarse": len(coarse), "train": len(train), "holdout": len(hold), "rounds": []}

    def run_round(name, cands, note):
        rnd = {"name": name, "note": note, "cands": []}
        for label, fn in cands.items():
            tau = choose_tau(fn, train, nodes)
            tr, _ = evaluate(fn, train, nodes, tau=tau)
            ho, rows = evaluate(fn, hold, nodes, tau=tau, label=label)
            hoc, _ = evaluate(fn, hold, nodes, tau=tau, coarse_level=2)
            lo, hi = bootstrap_ci(fn, hold, nodes, tau)
            rec = {"label": label, "tau": tau, "train_top1": round(tr["top1"], 3), "hold_top1": round(ho["top1"], 3),
                   "hold_ci": [round(lo, 3), round(hi, 3)], "hold_mrr": round(ho["mrr10"], 3), "hold_hier": round(ho["hier1"], 3),
                   "hold_coarse_top1": round(hoc["top1"], 3), "decoy_fa": round(ho["decoy_false_accept"], 3),
                   "unknown_on_real": round(ho["unknown_on_real"], 3), "per_len": {k: round(v, 3) for k, v in ho["per_len"].items()},
                   "per_flate": {k: round(v, 3) for k, v in ho["per_flate"].items()},
                   "errors": [r for r in rows if r[2] != r[3]][:12]}
            rnd["cands"].append(rec)
            print(f"  {label:52s} tau={tau!s:5s} tr={rec['train_top1']:.3f} ho={rec['hold_top1']:.3f} [{lo:.2f},{hi:.2f}] mrr={rec['hold_mrr']:.3f} grov={rec['hold_coarse_top1']:.3f} decoyFA={rec['decoy_fa']:.2f} unk={rec['unknown_on_real']:.2f} len={rec['per_len']}")
        results["rounds"].append(rnd); return rnd

    print("\n=== RUNDE 1: baselines og hypotesene H1–H5 ===")
    run_round("runde1", cands, "H1 hints > uten; H2 spredning; H3 skop adaptiv > fast; H4 facet-eksklusjon; H5 granularitet")
    json.dump(results, open(HERE / "natt_resultater.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n=== RUNDE 2: fiks det runde 1 avslørte ===")
    lt = lesson_text_by_purpose()
    idx_lessons = TfIdf({r: node_text(n) + " " + lt.get(r, "") for r, n in nodes.items()})
    fine_l = make_fine(nodes)
    idx_fine_l = TfIdf({r: node_text(n) + " " + lt.get(to_base(r), "") for r, n in fine_l.items()})
    c2 = {}
    base = lambda t, idx=idx_full: m_tfidf_alias_boost(nodes, t, idx)
    c2["R2-a M2b + skop MULTIPLIKATIVT adaptiv (H6)"] = lambda f, t: rank(apply_scope_mult(nodes, base(t), f, ch, t)[0], nodes, exclude_facet=True)
    c2["R2-b R2-a + spredning med tak (forelder overtar ikke barn)"] = lambda f, t: rank(apply_scope_mult(nodes, spread_capped(nodes, base(t), ch), f, ch, t)[0], nodes, exclude_facet=True)
    c2["R2-c R2-a + spørreords-prior (H10)"] = lambda f, t: rank(apply_scope_mult(nodes, add(base(t), qword_prior(t)), f, ch, t)[0], nodes, exclude_facet=True)
    c2["R2-d R2-a + lærdomstekst som norsk kilde (H8)"] = lambda f, t: rank(apply_scope_mult(nodes, m_tfidf_alias_boost(nodes, t, idx_lessons), f, ch, t)[0], nodes, exclude_facet=True)
    c2["R2-e alt: mult-skop + prior + lærdom"] = lambda f, t: rank(apply_scope_mult(nodes, add(m_tfidf_alias_boost(nodes, t, idx_lessons), qword_prior(t)), f, ch, t)[0], nodes, exclude_facet=True)
    c2["R2-f R2-e på FIN taksonomi (H9)"] = lambda f, t: rank(apply_scope_mult(fine_l, add(m_tfidf_alias_boost(fine_l, t, idx_fine_l), qword_prior(t)), f, chf, t)[0], fine_l, exclude_facet=True)
    c2["R2-g R2-f med skop-gain 2.0"] = lambda f, t: rank(apply_scope_mult(fine_l, add(m_tfidf_alias_boost(fine_l, t, idx_fine_l), qword_prior(t)), f, chf, t, gain=2.0)[0], fine_l, exclude_facet=True)
    run_round("runde2", c2, "H6 mult-skop stopper lokkedue-lekkasjen; H8 lærdomstekst; H9 fin; H10 spørreord")
    json.dump(results, open(HERE / "natt_resultater.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n=== RUNDE 3: prior som ikke lekker, og granularitet etter tekstlengde ===")
    c3 = {}
    r3a = lambda f, t: rank(apply_scope_mult(nodes, add(base(t), qword_prior_specific(t)), f, ch, t)[0], nodes, exclude_facet=True)
    c3["R3-a R2-c med spesifisitetsvektet prior (H11)"] = r3a
    c3["R3-b R3-a + søsken-tilbakefall (H12)"] = lambda f, t: sibling_backoff(r3a(f, t), nodes)
    r3fine = lambda f, t: rank(apply_scope_mult(fine_l, add(m_tfidf_alias_boost(fine_l, t, idx_fine_l), qword_prior_specific(t)), f, chf, t)[0], fine_l, exclude_facet=True)
    c3["R3-c adaptiv granularitet: fin bare ved <=2 tokens (H7)"] = lambda f, t: adaptive_granularity(t, r3fine, r3a, f)
    c3["R3-d R3-a uten skop i det hele tatt (ablasjon)"] = lambda f, t: rank(add(base(t), qword_prior_specific(t)), nodes, exclude_facet=True)
    c3["R3-e R3-a med prior-vekt 0.20"] = lambda f, t: rank(apply_scope_mult(nodes, add(base(t), qword_prior_specific(t, 0.20)), f, ch, t)[0], nodes, exclude_facet=True)
    c3["R3-f R3-a med prior-vekt 0.06"] = lambda f, t: rank(apply_scope_mult(nodes, add(base(t), qword_prior_specific(t, 0.06)), f, ch, t)[0], nodes, exclude_facet=True)
    run_round("runde3", c3, "H11 spesifisitet; H12 søsken-tilbakefall; H7 fin bare ved tynn tekst; ablasjon av skop")
    json.dump(results, open(HERE / "natt_resultater.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n=== RUNDE 4: hvor sterkt kan skop modulere før det lekker? ===")
    c4 = {}
    for g in (2.0, 3.0, 5.0):
        c4[f"R4 skop-gain {g}"] = (lambda g: (lambda f, t: rank(apply_scope_mult(nodes, add(base(t), qword_prior_specific(t)), f, ch, t, gain=g)[0], nodes, exclude_facet=True)))(g)
    # barn foran forelder: når barn og forelder begge treffer, senk forelderen med 0.8 (barn er mer spesifikt)
    def child_first(sc):
        out = dict(sc)
        for r, s_ in sc.items():
            p = nodes[r].get("parent")
            if p in out and out[p] > 0 and s_ > 0: out[p] = out[p] * 0.8
        return out
    c4["R4-b gain 3 + barn-foran-forelder"] = lambda f, t: rank(child_first(apply_scope_mult(nodes, add(base(t), qword_prior_specific(t)), f, ch, t, gain=3.0)[0]), nodes, exclude_facet=True)
    run_round("runde4", c4, "skop-gain 2/3/5 med spesifikk prior; barn-foran-forelder mot søskenforvirring")
    json.dump(results, open(HERE / "natt_resultater.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return results

if __name__ == "__main__":
    main()
