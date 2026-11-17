# -*- coding: utf-8 -*-
"""Utleder erklæringskandidater fra Fables tolkning av TRENINGSRADENE (T1–T3 + NT partall). Aldri fra T4 eller S*.

Ut (alle med kilde per oppføring, så Kjetil kan dømme dem som erklærte kilder):
  lex/leksikon.json   ref -> [{frase, stoette, presisjon, eksempler}]   (fra baerende_ord)
  lex/verb.json       verb-lemma -> {ref: P(ref|verb)}                 (fra handling)
  lex/acts.json       conversation.* -> [hele ytringer/fraser]          (fra samtaleformålene)
  lex/bakgrunn.json   ord som er vanligere i negativer enn i ekte rader
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
import eval7 as E
import r5

HERE = Path(__file__).resolve().parent
OUT = HERE / "lex"; OUT.mkdir(exist_ok=True)
M = r5.Matcher(flags=dict(lex=False, desc_no=False, acts=False, dekomp=False))
norm = lambda s: " ".join(M.words(s))


def derive(min_support=2, min_prec=0.6, min_len=4):
    rows = E.train_rows(silver=True)
    texts = [(norm(r["tekst"]), r["gold"]) for r in rows]
    cand = defaultdict(Counter)
    for r in rows:
        tk = r["tolk"] or {}
        for p in tk.get("baerende_ord") or []:
            p2 = norm(p)
            if len(p2) < min_len or all(w in r5.STOP for w in p2.split()): continue
            cand[r["gold"]][p2] += 1
    lex = defaultdict(list)
    for ref, c in cand.items():
        for p, sup in c.items():
            occ = [g for t, g in texts if f" {p} " in f" {t} "]
            prec = sum(g == ref for g in occ) / max(1, len(occ))
            if sup >= min_support and prec >= min_prec:
                lex[ref].append({"frase": p, "stoette": sup, "presisjon": round(prec, 2), "forekomster": len(occ)})
    # verb
    vc = defaultdict(Counter)
    for r in rows:
        if r["gold"] == E.NEG: continue
        h = norm((r["tolk"] or {}).get("handling") or "")
        if not h or len(h.split()) > 2: continue
        for form in {h.split()[0], r5.stem(h.split()[0])}:
            vc[form][r["gold"]] += 1
    verbs = {}
    for v, c in vc.items():
        tot = sum(c.values())
        keep = {ref: round(n / tot, 2) for ref, n in c.items() if n >= 2 and n / tot >= 0.34}
        if keep: verbs[v] = keep
    # samtalehandlinger: hele (normaliserte) ytringer + bærende ord, bare der Fable var enig
    acts = defaultdict(set)
    for r in rows:
        if not r["gold"].startswith("purpose://conversation."): continue
        t = norm(r["tekst"])
        if 0 < len(t.split()) <= 6: acts[r["gold"]].add(t)
        for p in (r["tolk"] or {}).get("baerende_ord") or []:
            p2 = norm(p)
            if p2: acts[r["gold"]].add(p2)
    # fjern act-fraser som også er act-fraser for en annen handling
    allp = Counter(p for s in acts.values() for p in s)
    acts = {k: sorted(p for p in v if allp[p] == 1) for k, v in acts.items()}
    # bakgrunn
    pos = Counter(); neg = Counter(); npos = nneg = 0
    for r in rows:
        ws = set(M.toks(r["tekst"]))
        if r["gold"] == E.NEG: neg.update(ws); nneg += 1
        else: pos.update(ws); npos += 1
    bg = sorted(w for w, n in neg.items() if n >= 2 and n / nneg > 3 * (pos[w] + 1) / npos)
    return dict(lex), verbs, acts, bg


if __name__ == "__main__":
    lex, verbs, acts, bg = derive()
    kilde = "Fable-tolkning (baerende_ord/handling) av treningsradene T1–T3 + NT partall, der Fable valgte samme formål som generatoren. 2026-10-07."
    json.dump({"kilde": kilde, "leksikon": lex}, open(OUT / "leksikon.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"kilde": kilde, "verb": verbs}, open(OUT / "verb.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"kilde": kilde, "acts": acts}, open(OUT / "acts.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"kilde": kilde, "bakgrunn": bg}, open(OUT / "bakgrunn.json", "w"), ensure_ascii=False, indent=1)
    print("leksikon:", sum(len(v) for v in lex.values()), "fraser på", len(lex), "formål; verb:", len(verbs), "; acts:",
          {k[-12:]: len(v) for k, v in acts.items()}, "; bakgrunn:", len(bg))
