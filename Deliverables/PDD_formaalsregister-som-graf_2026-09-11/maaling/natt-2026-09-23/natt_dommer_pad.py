"""Fyll hver sak i natt_dommer_runde2.json opp til fem alternativer.

Astras motsvar §6: ni saker viste bare gold, tre viste ingenting. Det forankrer dommen til Losens etikett.
Her får hver sak nøyaktig fem alternativer: matcherens topp-5 beholdes; resten fylles med (1) gold-nodens søsken,
(2) noder i flatens skop, (3) hvilken som helst annen node — trukket med fast seed, aldri merket. Gold fjernes aldri.
Rekkefølgen stokkes på nytt per sak. Skriver natt_dommer_runde2.json på nytt og skriver ut JSON for artefaktet.
Ren stdlib. Kjør fra mappen: python3 natt_dommer_pad.py
"""
import json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import natt_trening as t  # noqa: E402
from natt_korpus import FLATE_SKOP  # noqa: E402

UNKNOWN = "purpose://prompt.unknown"
SEED = 20260924


def label(n):
    d = (n.get("desc") or n.get("outcome") or "").strip()
    return n["title"] + " — " + (d[:110] if d else "")


def main():
    nodes = t.load_union()
    ch = t.children_map(nodes)
    cases = json.loads((HERE / "natt_dommer_runde2.json").read_text(encoding="utf-8"))
    rnd = random.Random(SEED)
    changed = 0
    for c in cases:
        have = [a["ref"] for a in c["alternativer"]]
        gold = c["gold"]
        if gold != UNKNOWN and gold not in have:
            raise SystemExit("gold mangler blant alternativene: " + c["tekst"])
        pools = []
        if gold != UNKNOWN and nodes.get(gold, {}).get("parent"):
            pools.append([r for r in ch.get(nodes[gold]["parent"], []) if r != gold])
        pools.append(sorted(t.subtree(nodes, FLATE_SKOP[c["flate"]], ch)))
        pools.append(sorted(nodes))
        picked = list(have)
        for pool in pools:
            pool = [r for r in pool if r not in picked and r in nodes]
            rnd.shuffle(pool)
            while len(picked) < 5 and pool:
                picked.append(pool.pop())
            if len(picked) >= 5:
                break
        if len(picked) != 5:
            raise SystemExit("klarte ikke fylle: " + c["tekst"])
        by = {a["ref"]: a for a in c["alternativer"]}
        alts = [by.get(r) or {"ref": r, "label": label(nodes[r])} for r in picked]
        rnd.shuffle(alts)
        if alts != c["alternativer"]:
            changed += 1
        c["alternativer"] = alts
        c["utfylt"] = len(picked) - len(have)
    (HERE / "natt_dommer_runde2.json").write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    pub = [{"id": k, "flate": c["flate"], "tekst": c["tekst"], "alternativer": c["alternativer"]} for k, c in enumerate(cases)]
    (HERE / "natt_dommer_runde2_artefakt.json").write_text(json.dumps(pub, ensure_ascii=False), encoding="utf-8")
    print("saker", len(cases), "endret", changed, "alle fem:", all(len(c["alternativer"]) == 5 for c in cases))
    print("gold med:", all(c["gold"] == UNKNOWN or c["gold"] in {a["ref"] for a in c["alternativer"]} for c in cases))


if __name__ == "__main__":
    main()
