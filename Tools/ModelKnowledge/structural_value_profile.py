#!/usr/bin/env python3
"""Structural Value Profile for typed HAVEN graphs (pure Python, no deps).

Computes pillars 1, 3 and 4 of the profile proposed in
Deliverables/Fractal_Dimension_Data_Value_Advisory_2026-07-04.md, plus
null-model z-scores and a bootstrap stability check. Pillar 2 (realized/
current value) is intentionally reported as unavailable: it requires
FlowElement usage traces, which static corpora do not carry.

Content-blind: consumes only the normalized edgelist structure and coarse
edge/node types, never node prose.

Usage:
    python3 Tools/ModelKnowledge/structural_value_profile.py \
        --graph Tools/ModelKnowledge/generated/graphs/haven_purpose_graph.json \
        [--nulls 100 --bootstrap 100 --drop 0.1 --seed 7]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import zlib
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


# ----------------------------- graph model -----------------------------

class Graph:
    def __init__(self, node_ids, undirected_edges, directed_edge_count, edge_types):
        self.nodes = list(node_ids)
        self.index = {n: i for i, n in enumerate(self.nodes)}
        self.adj = defaultdict(set)  # undirected, simple
        for u, v in undirected_edges:
            if u != v:
                self.adj[u].add(v)
                self.adj[v].add(u)
        self.n = len(self.nodes)
        self.m = sum(len(s) for s in self.adj.values()) // 2  # undirected simple edges
        self.directed_edge_count = directed_edge_count
        self.edge_types = edge_types

    @classmethod
    def from_file(cls, path: Path) -> "Graph":
        data = json.loads(path.read_text(encoding="utf-8"))
        node_ids = [n["id"] for n in data["nodes"]]
        seen = set(node_ids)
        u_edges = []
        etypes = []
        for e in data["edges"]:
            u, v = e["u"], e["v"]
            for x in (u, v):
                if x not in seen:
                    seen.add(x)
                    node_ids.append(x)
            u_edges.append((u, v))
            etypes.append(e.get("type", "edge"))
        g = cls(node_ids, u_edges, len(data["edges"]), etypes)
        g.meta = {"graphID": data.get("graphID"), "kind": data.get("kind"),
                  "source": data.get("source"), "directed": data.get("directed", True)}
        return g

    def degree(self, node):
        return len(self.adj[node])


# --------------------------- basic structure ---------------------------

def components(g: Graph):
    seen = set()
    comps = []
    for start in g.nodes:
        if start in seen:
            continue
        comp = []
        q = deque([start])
        seen.add(start)
        while q:
            x = q.popleft()
            comp.append(x)
            for y in g.adj[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(comp)
    return sorted(comps, key=len, reverse=True)


def bfs_distances(g: Graph, source, allowed=None):
    dist = {source: 0}
    q = deque([source])
    while q:
        x = q.popleft()
        for y in g.adj[x]:
            if allowed is not None and y not in allowed:
                continue
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def diameter_and_effective(g: Graph, comp):
    """Exact diameter and 90th-percentile effective diameter of a component."""
    allowed = set(comp)
    all_d = []
    ecc = 0
    for s in comp:
        dist = bfs_distances(g, s, allowed)
        vals = [d for d in dist.values()]
        ecc = max(ecc, max(vals) if vals else 0)
        all_d.extend(v for v in vals if v > 0)
    all_d.sort()
    if not all_d:
        return 0, 0.0
    idx = min(len(all_d) - 1, int(math.ceil(0.9 * len(all_d)) - 1))
    return ecc, float(all_d[idx])


def triangles_and_wedges(g: Graph):
    triangles = 0
    wedges = 0
    for v in g.nodes:
        neigh = g.adj[v]
        d = len(neigh)
        wedges += d * (d - 1) // 2
        nb = list(neigh)
        for i in range(len(nb)):
            for j in range(i + 1, len(nb)):
                if nb[j] in g.adj[nb[i]]:
                    triangles += 1
    triangles //= 3
    return triangles, wedges


def mean_local_clustering(g: Graph):
    total = 0.0
    counted = 0
    for v in g.nodes:
        nb = list(g.adj[v])
        d = len(nb)
        if d < 2:
            continue
        links = 0
        for i in range(len(nb)):
            for j in range(i + 1, len(nb)):
                if nb[j] in g.adj[nb[i]]:
                    links += 1
        total += 2 * links / (d * (d - 1))
        counted += 1
    return total / counted if counted else 0.0


def articulation_points_and_bridges(g: Graph):
    """Iterative Tarjan over the whole undirected graph."""
    disc = {}
    low = {}
    timer = [0]
    aps = set()
    bridges = 0
    for root in g.nodes:
        if root in disc:
            continue
        stack = [(root, None, iter(g.adj[root]))]
        disc[root] = low[root] = timer[0]
        timer[0] += 1
        root_children = 0
        while stack:
            node, parent, it = stack[-1]
            advanced = False
            for nxt in it:
                if nxt == parent:
                    continue
                if nxt not in disc:
                    if parent is None:
                        root_children += 1
                    disc[nxt] = low[nxt] = timer[0]
                    timer[0] += 1
                    stack.append((nxt, node, iter(g.adj[nxt])))
                    advanced = True
                    break
                else:
                    low[node] = min(low[node], disc[nxt])
            if not advanced:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[node])
                    if stack[-1][1] is not None and low[node] >= disc[p]:
                        aps.add(p)
                    if low[node] > disc[p]:
                        bridges += 1
        if root_children > 1:
            aps.add(root)
    return len(aps), bridges


# --------------------------- spectral (Jacobi) -------------------------

def normalized_laplacian(g: Graph, comp):
    idx = {n: i for i, n in enumerate(comp)}
    k = len(comp)
    L = [[0.0] * k for _ in range(k)]
    deg = {n: len(g.adj[n] & set(comp)) for n in comp}
    for a in comp:
        ia = idx[a]
        da = deg[a]
        if da == 0:
            continue
        L[ia][ia] = 1.0
        for b in g.adj[a]:
            if b in idx and b != a:
                db = deg[b]
                if db > 0:
                    L[ia][idx[b]] = -1.0 / math.sqrt(da * db)
    return L


def jacobi_eigenvalues(A, sweeps=100, tol=1e-10):
    n = len(A)
    if n == 0:
        return []
    a = [row[:] for row in A]
    for _ in range(sweeps):
        off = 0.0
        for p in range(n):
            for q in range(p + 1, n):
                off += a[p][q] * a[p][q]
        if off < tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-14:
                    continue
                app, aqq, apq = a[p][p], a[q][q], a[p][q]
                phi = 0.5 * math.atan2(2 * apq, aqq - app)
                c, s = math.cos(phi), math.sin(phi)
                for i in range(n):
                    aip, aiq = a[i][p], a[i][q]
                    a[i][p] = c * aip - s * aiq
                    a[i][q] = s * aip + c * aiq
                for i in range(n):
                    api, aqi = a[p][i], a[q][i]
                    a[p][i] = c * api - s * aqi
                    a[q][i] = s * api + c * aqi
    return [a[i][i] for i in range(n)]


def von_neumann_entropy(g: Graph, comp):
    L = normalized_laplacian(g, comp)
    eig = jacobi_eigenvalues(L)
    trace = sum(eig)
    if trace <= 0:
        return 0.0
    rho = [max(0.0, e) / trace for e in eig]
    s = 0.0
    for p in rho:
        if p > 1e-12:
            s -= p * math.log(p)
    return s


# ------------------------------ entropy/MDL ----------------------------

def degree_entropy(g: Graph):
    counts = defaultdict(int)
    for v in g.nodes:
        counts[len(g.adj[v])] += 1
    total = g.n
    s = 0.0
    for c in counts.values():
        p = c / total
        s -= p * math.log(p)
    return s


def type_entropy(g: Graph):
    counts = defaultdict(int)
    for t in g.edge_types:
        counts[t] += 1
    total = len(g.edge_types) or 1
    s = 0.0
    for c in counts.values():
        p = c / total
        s -= p * math.log(p)
    return s


def compressibility_ratio(g: Graph):
    lines = []
    for n in sorted(g.nodes):
        nb = sorted(g.index[x] for x in g.adj[n])
        lines.append(f"{g.index[n]}:" + ",".join(map(str, nb)))
    raw = ("\n".join(lines)).encode("utf-8")
    if not raw:
        return 1.0
    comp = zlib.compress(raw, 9)
    return len(comp) / len(raw)


# ------------------------------ null models ----------------------------

def er_null(n, m, rng):
    """Erdos-Renyi G(n,m): random simple undirected graph, same n and m."""
    node_ids = list(range(n))
    edges = set()
    max_edges = n * (n - 1) // 2
    m = min(m, max_edges)
    while len(edges) < m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        e = (u, v) if u < v else (v, u)
        edges.add(e)
    g = Graph(node_ids, list(edges), m, ["edge"] * m)
    return g


def null_zscores(g: Graph, nulls, rng):
    comp = components(g)[0]
    obs_svn = von_neumann_entropy(g, comp) / math.log(len(comp)) if len(comp) > 1 else 0.0
    obs_clust = mean_local_clustering(g)
    obs_deg = degree_entropy(g) / math.log(g.n) if g.n > 1 else 0.0
    svn_s, clu_s, deg_s = [], [], []
    for _ in range(nulls):
        h = er_null(g.n, g.m, rng)
        hc = components(h)[0]
        svn_s.append(von_neumann_entropy(h, hc) / math.log(len(hc)) if len(hc) > 1 else 0.0)
        clu_s.append(mean_local_clustering(h))
        deg_s.append(degree_entropy(h) / math.log(h.n) if h.n > 1 else 0.0)

    def z(obs, sample):
        mu = sum(sample) / len(sample)
        var = sum((x - mu) ** 2 for x in sample) / len(sample)
        sd = math.sqrt(var)
        return (obs - mu) / sd if sd > 1e-9 else 0.0, mu, sd

    zsvn = z(obs_svn, svn_s)
    zclu = z(obs_clust, clu_s)
    zdeg = z(obs_deg, deg_s)
    return {
        "vn_entropy_norm": {"observed": round(obs_svn, 4), "null_mean": round(zsvn[1], 4), "null_sd": round(zsvn[2], 4), "z": round(zsvn[0], 3)},
        "mean_clustering": {"observed": round(obs_clust, 4), "null_mean": round(zclu[1], 4), "null_sd": round(zclu[2], 4), "z": round(zclu[0], 3)},
        "degree_entropy_norm": {"observed": round(obs_deg, 4), "null_mean": round(zdeg[1], 4), "null_sd": round(zdeg[2], 4), "z": round(zdeg[0], 3)},
    }


# ------------------------------- profile -------------------------------

def core_metrics(g: Graph):
    comps = components(g)
    giant = comps[0]
    diam, eff = diameter_and_effective(g, giant)
    tri, wedge = triangles_and_wedges(g)
    transitivity = (3 * tri / wedge) if wedge else 0.0
    open_triad_ratio = 1.0 - transitivity
    isolates = sum(1 for v in g.nodes if len(g.adj[v]) == 0)
    leaves = sum(1 for v in g.nodes if len(g.adj[v]) == 1)
    aps, bridges = articulation_points_and_bridges(g)
    svn = von_neumann_entropy(g, giant)
    svn_norm = svn / math.log(len(giant)) if len(giant) > 1 else 0.0
    return {
        "N": g.n,
        "E_directed": g.directed_edge_count,
        "E_undirected_simple": g.m,
        "density_undirected": round(2 * g.m / (g.n * (g.n - 1)), 5) if g.n > 1 else 0.0,
        "mean_degree": round(2 * g.m / g.n, 3) if g.n else 0.0,
        "components": len(comps),
        "giant_fraction": round(len(giant) / g.n, 4) if g.n else 0.0,
        "diameter_giant": diam,
        "effective_diameter_p90": eff,
        "isolates": isolates,
        "leaf_fraction": round(leaves / g.n, 4) if g.n else 0.0,
        "articulation_points": aps,
        "bridges": bridges,
        "transitivity": round(transitivity, 4),
        "open_triad_ratio": round(open_triad_ratio, 4),
        "mean_local_clustering": round(mean_local_clustering(g), 4),
        "degree_entropy_norm": round(degree_entropy(g) / math.log(g.n), 4) if g.n > 1 else 0.0,
        "type_entropy": round(type_entropy(g), 4),
        "compressibility_ratio": round(compressibility_ratio(g), 4),
        "vn_entropy": round(svn, 4),
        "vn_entropy_norm": round(svn_norm, 4),
        "usable_box_scales_estimate": diam,
    }


def bootstrap_stability(g: Graph, resamples, drop, rng):
    data = json_edges(g)
    keys = ["giant_fraction", "open_triad_ratio", "mean_local_clustering",
            "degree_entropy_norm", "vn_entropy_norm", "effective_diameter_p90"]
    acc = {k: [] for k in keys}
    for _ in range(resamples):
        kept = [e for e in data if rng.random() > drop]
        h = Graph([n for n in g.nodes], kept, len(kept), ["edge"] * len(kept))
        m = core_metrics(h)
        for k in keys:
            acc[k].append(m[k])
    out = {}
    for k in keys:
        vals = acc[k]
        mu = sum(vals) / len(vals)
        var = sum((x - mu) ** 2 for x in vals) / len(vals)
        sd = math.sqrt(var)
        cv = sd / mu if abs(mu) > 1e-9 else 0.0
        out[k] = {"mean": round(mu, 4), "sd": round(sd, 4), "cv": round(cv, 4)}
    return out


def json_edges(g: Graph):
    seen = set()
    edges = []
    for u in g.nodes:
        for v in g.adj[u]:
            e = (u, v) if u < v else (v, u)
            if e not in seen:
                seen.add(e)
                edges.append(e)
    return edges


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", type=Path, required=True)
    ap.add_argument("--nulls", type=int, default=100)
    ap.add_argument("--bootstrap", type=int, default=100)
    ap.add_argument("--drop", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    g = Graph.from_file(args.graph)
    profile = {
        "graphID": g.meta["graphID"],
        "kind": g.meta["kind"],
        "source": g.meta["source"],
        "pillar1_scale_health": {},
        "pillar2_current_value": {"status": "unavailable",
                                  "reason": "requires FlowElement usage traces; static corpus carries no traversal/read events"},
        "pillar3_potential_value": {},
        "pillar4_complexity": {},
        "null_model_zscores": {},
        "bootstrap_stability": {},
    }
    m = core_metrics(g)
    profile["pillar1_scale_health"] = {k: m[k] for k in [
        "N", "E_directed", "E_undirected_simple", "density_undirected", "mean_degree",
        "components", "giant_fraction", "diameter_giant", "effective_diameter_p90",
        "isolates", "leaf_fraction"]}
    profile["pillar3_potential_value"] = {k: m[k] for k in [
        "open_triad_ratio", "mean_local_clustering", "articulation_points", "bridges",
        "leaf_fraction", "type_entropy"]}
    profile["pillar4_complexity"] = {k: m[k] for k in [
        "vn_entropy", "vn_entropy_norm", "degree_entropy_norm", "compressibility_ratio",
        "usable_box_scales_estimate"]}
    profile["fractal_gate"] = {
        "usable_box_scales": m["usable_box_scales_estimate"],
        "estimable": m["usable_box_scales_estimate"] >= 15,
        "note": "box-covering fractal dimension gated off below ~15 usable radii (advisory 2026-07-04)",
    }
    profile["null_model_zscores"] = null_zscores(g, args.nulls, rng)
    profile["bootstrap_stability"] = bootstrap_stability(g, args.bootstrap, args.drop, rng)
    profile["params"] = {"nulls": args.nulls, "bootstrap": args.bootstrap, "drop": args.drop, "seed": args.seed}

    text = json.dumps(profile, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"Wrote profile to {args.out}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
