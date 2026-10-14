import eval7 as E
ACT = "purpose://conversation"
def preds(m, rows):
    out = []
    for r in rows:
        rk = m(r["flate"], r["tekst"]); b = rk[0] if rk else (E.U, 0.0)
        out.append((r, b[0], b[1]))
    return out
def curve(m, rows, fas=(0.0, 0.05, 0.10, 0.15), strict=False, P=None):
    """top1 når terskelen settes så andelen negativer med flateforslag er <= fa.
    Primær (forhåndsregel 2026-10-07): et samtalehandlings-svar på en negativ er ikke et flateforslag (Kjetils avgjørelse 1).
    strict=True: alt annet enn unknown teller som falsk aksept."""
    P = P or preds(m, rows)
    real = [(r, p, s) for r, p, s in P if r["gold"] != E.NEG]
    negs = [(p, s) for r, p, s in P if r["gold"] == E.NEG]
    fa_scores = sorted([s for p, s in negs if p != E.U and (strict or not p.startswith(ACT))], reverse=True)
    out = {}
    for fa in fas:
        k = int(fa * len(negs))
        tau = (fa_scores[k] + 1e-9) if k < len(fa_scores) else 0.0
        out[fa] = sum(1 for r, p, s in real if p == r["gold"] and s > tau) / len(real)
    return out
def tau_at(m, rows, fa=0.10, strict=False, P=None):
    P = P or preds(m, rows)
    negs = [(p, s) for r, p, s in P if r["gold"] == E.NEG]
    fa_scores = sorted([s for p, s in negs if p != E.U and (strict or not p.startswith(ACT))], reverse=True)
    k = int(fa * len(negs)); return (fa_scores[k] + 1e-9) if k < len(fa_scores) else 0.0
