#!/usr/bin/env python3
"""score.py — poengsetter Butlers AI-løse forståelse mot en frosset fasit.

Bruk:  python3 score.py <korpus-mappe> <rapport-mappe>
  - leser <rapport-mappe>/<navn>.resultat.jsonl (skrevet av ButlerForstaaelseMaalingTests)
  - kobler hver linje til <korpus-mappe>/<navn>.jsonl på id
  - fasit: korpus-v*: etiketten via ../etikett-kart.json; fixtures-v*: PromptPurposeLab `gold`
  - valgfritt ../fasit/*.jsonl (fasit-v1, fasit-v2, kallimachos-fasit-v1): tolkens etikett (sølv) → egen tabell for delmengden der
    generator og tolk er enige (renere fasit)
Skriver markdown på stdout og rapport-<dato>-<etikett>.json i rapport-mappa.
Harnessen dømmer ingenting; alt skjønn om hva som er riktig står her og i etikett-kart.json.
Python 3.9-kompatibel (macOS /usr/bin/python3).
"""
import json, os, sys, random, datetime
from collections import Counter, defaultdict

ACTIONABLE = {"suggested", "needs_candidate_selection", "needs_invite"}
GULL_BRUKT = [0]


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def as_dict(v):
    return v if isinstance(v, dict) else {}


def as_list(v):
    return v if isinstance(v, list) else []


def refs_of(item):
    item = as_dict(item)
    out = []
    for key in ("purposeRef", "resourcePurposeRef"):
        if isinstance(item.get(key), str):
            out.append(item[key])
    for key in ("purposeRefs",):
        out += [r for r in as_list(item.get(key)) if isinstance(r, str)]
    return out


def endpoint_refs(item):
    item = as_dict(item)
    out = []
    for key in ("sourceCellEndpoint",):
        if isinstance(item.get(key), str) and item.get(key):
            out.append("endpoint:" + item[key])
    return out


def kind_of(item):
    item = as_dict(item)
    for key in ("kind", "intentKind"):
        if isinstance(item.get(key), str):
            return item[key]
    return None


def prediction(rec):
    """Det brukeren faktisk ser (synlig) + en rangert kandidatliste for R@3/MRR."""
    if "topK" in rec and "suggestion" not in rec:
        # Kallimachos-adapteren (WP-D2): ren rangert liste, ingen hjelpere, ingen avklaring.
        ranked = [{"kind": "purpose", "refs": [as_dict(m).get("purposeRef")], "fra": "topK",
                   "score": as_dict(m).get("score")} for m in as_list(rec.get("topK"))]
        if rec.get("error"):
            return {"type": "feil"}, ranked
        if not ranked:
            return {"type": "ukjent"}, ranked
        return {"type": "handling", "kind": "purpose", "refs": ranked[0]["refs"]}, ranked
    sug = as_dict(rec.get("suggestion"))
    status = sug.get("status")
    kind = kind_of(sug)
    if rec.get("error"):
        visible = {"type": "feil"}
    elif status in ACTIONABLE and kind and kind != "unknown":
        refs = refs_of(sug)
        if kind == "resource_match":
            for m in as_list(rec.get("resourceMatches")):
                m = as_dict(m)
                if sug.get("targetPhrase") and sug.get("targetPhrase") in (m.get("title"), m.get("configurationName")):
                    refs += refs_of(m) + endpoint_refs(m)
                    break
        visible = {"type": "handling", "kind": kind, "refs": refs}
    elif status == "needs_clarification":
        options = as_list(as_dict(rec.get("clarification")).get("options"))
        visible = {"type": "avklaring", "kind": kind,
                   "valg": [{"intentKind": as_dict(o).get("intentKind"), "resourceTitle": as_dict(o).get("resourceTitle"),
                             "title": as_dict(o).get("title")} for o in options]}
    else:
        visible = {"type": "ukjent", "status": status}
    ranked = []
    if visible["type"] == "handling":
        ranked.append({"kind": visible["kind"], "refs": visible["refs"], "fra": "suggestion"})
    for c in as_list(rec.get("intentCandidates")):
        k = kind_of(c)
        if k and k != "unknown":
            ranked.append({"kind": k, "refs": refs_of(c), "fra": "intentCandidates"})
    for m in as_list(rec.get("resourceMatches")):
        ranked.append({"kind": "resource_match", "refs": refs_of(m) + endpoint_refs(m), "fra": "resourceMatches",
                       "title": as_dict(m).get("title")})
    # fjern dubletter, behold rekkefølge
    seen, uniq = set(), []
    for r in ranked:
        key = (r["kind"], tuple(r["refs"]))
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    return visible, uniq


def hits(entry, gold):
    if gold["forventet"] == "formaal":
        return bool(set(entry["refs"]) & set(gold["purposeRefs"]))
    if gold["forventet"] == "hjelper":
        return entry["kind"] == gold["intentKind"]
    if gold["forventet"] == "flate":
        return bool(set(entry["refs"]) & (set(gold["purposeRefs"]) | {"endpoint:" + e for e in gold.get("endpoints", [])}))
    return False


KATALOG_REFS = {}  # konfigurasjonsnavn/tittel → purposeRefs, fylles fra katalog.json


def clarification_hits(visible, gold):
    """Spurte Butler, og var riktig mål blant alternativene brukeren fikk?"""
    for o in visible.get("valg", []):
        if gold["forventet"] == "hjelper" and o.get("intentKind") == gold.get("intentKind"):
            return True
        if gold["forventet"] == "flate":
            for key in (o.get("resourceTitle"), o.get("title")):
                if key and set(KATALOG_REFS.get(key, [])) & (set(gold.get("purposeRefs", [])) | {"endpoint:" + e for e in gold.get("endpoints", [])}):
                    return True
    return False


def judge_label(visible, ranked, gold):
    """→ (top1: bool, rang: int|None, utfall: str)"""
    f = gold["forventet"]
    if f in ("hjelper", "flate", "formaal"):
        rank = None
        for i, e in enumerate(ranked):
            if hits(e, gold):
                rank = i + 1
                break
        top1 = visible["type"] == "handling" and hits({"kind": visible["kind"], "refs": visible["refs"]}, gold)
        if top1:
            utfall = "riktig"
        elif visible["type"] == "handling":
            utfall = "feil handling"
        elif visible["type"] == "avklaring":
            utfall = "spurte, riktig blant valgene" if clarification_hits(visible, gold) else "spurte"
        elif visible["type"] == "feil":
            utfall = "kjørefeil"
        else:
            utfall = "stille"
        return top1, rank, utfall
    if f == "avklaring":
        ok = visible["type"] == "avklaring"
        return ok, (1 if ok else None), ("riktig" if ok else ("feil handling" if visible["type"] == "handling" else "stille"))
    if f == "hull":
        ok = visible["type"] != "handling" or visible.get("kind") == "capability_request"
        return ok, (1 if ok else None), ("riktig" if ok else "feil handling")
    # ingen / meta: riktig = ingen handling foreslått
    ok = visible["type"] != "handling"
    return ok, (1 if ok else None), ("riktig" if ok else "feil handling")


def gold_from_fixture(g):
    g = as_dict(g)
    if g.get("clarificationReason") or g.get("clarificationMissing"):
        return {"forventet": "avklaring", "purposeRefs": []}
    if g.get("shouldSuggest") and g.get("intentKind") and g.get("intentKind") != "resource_match":
        return {"forventet": "hjelper", "intentKind": g["intentKind"], "purposeRefs": [g.get("purposeRef")]}
    if g.get("shouldSuggest") or g.get("resourcePurposeRef"):
        refs = [r for r in (g.get("purposeRef"), g.get("resourcePurposeRef")) if r]
        return {"forventet": "flate", "intentKind": "resource_match", "purposeRefs": refs}
    return {"forventet": "ingen", "purposeRefs": []}


def ci(values, n=1000, seed=7):
    if not values:
        return (None, None)
    rnd = random.Random(seed)
    means = sorted(sum(rnd.choice(values) for _ in values) / len(values) for _ in range(n))
    return (means[int(0.025 * n)], means[int(0.975 * n)])


def pct(x):
    return "–" if x is None else "%.0f %%" % (100 * x)


def summarize(items):
    pos = [i for i in items if i["forventet"] in ("hjelper", "flate", "formaal") and i["mulig"]]
    neg = [i for i in items if i["forventet"] in ("ingen", "hull", "meta")]
    top1 = [1.0 if i["top1"] else 0.0 for i in pos]
    r3 = [1.0 if (i["rang"] is not None and i["rang"] <= 3) else 0.0 for i in pos]
    mrr = [1.0 / i["rang"] if i["rang"] else 0.0 for i in pos]
    negp = [1.0 if i["top1"] else 0.0 for i in neg]
    alle = [1.0 if i["top1"] else 0.0 for i in items]
    nyttig = [1.0 if (i["top1"] or i["utfall"] == "spurte, riktig blant valgene") else 0.0 for i in pos]
    out = {"n": len(items), "nPositive": len(pos), "nNegative": len(neg)}
    for name, vals in (("top1", top1), ("recallAt3", r3), ("mrr", mrr), ("negativePrecision", negp), ("alleRiktig", alle), ("nyttigPositiv", nyttig)):
        out[name] = (sum(vals) / len(vals)) if vals else None
        out[name + "CI95"] = ci(vals)
    out["utfall"] = dict(Counter(i["utfall"] for i in items))
    return out


def main():
    kdir, rdir = sys.argv[1], sys.argv[2]
    mdir = os.path.dirname(os.path.abspath(kdir))
    etikett = os.path.basename(os.path.abspath(rdir))
    kart = json.load(open(os.path.join(mdir, "etikett-kart.json"), encoding="utf-8"))["etiketter"]
    kpath_katalog = os.path.join(mdir, "katalog.json")
    if os.path.exists(kpath_katalog):
        kat = json.load(open(kpath_katalog, encoding="utf-8"))
        for c in kat.get("configurations", []):
            KATALOG_REFS.setdefault(c.get("name"), []).extend((c.get("purposeRefs") or []) + (["endpoint:" + c["sourceCellEndpoint"]] if c.get("sourceCellEndpoint") else []))
        for d in kat.get("documentation", []):
            KATALOG_REFS.setdefault(d.get("title"), []).extend(d.get("purposeRefs") or [])
    silver = {}
    fdir = os.path.join(mdir, "fasit")
    # Alle fasitfiler (fasit-v1, fasit-v2 for det uavhengige korpuset, kallimachos-fasit-v1): id-ene er unike på tvers.
    for fasit in sorted(os.path.join(fdir, fn) for fn in (os.listdir(fdir) if os.path.isdir(fdir) else []) if fn.endswith(".jsonl")):
        if os.path.exists(fasit):
            for r in load_jsonl(fasit):
                silver[r["id"]] = r
    report = {"schema": "haven.butler-maaling.rapport.v1", "variant": etikett,
              "skrevet": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "korpus": {}}
    md = ["## Poeng («%s»)" % etikett, ""]
    for fn in sorted(os.listdir(rdir)):
        if not fn.endswith(".resultat.jsonl"):
            continue
        navn = fn[: -len(".resultat.jsonl")]
        kpath = os.path.join(kdir, navn + ".jsonl")
        if not os.path.exists(kpath):
            kpath = os.path.join(mdir, "kallimachos", navn + ".jsonl")
        if not os.path.exists(kpath):
            continue
        korpus = {r["id"]: r for r in load_jsonl(kpath)}
        items = []
        for rec in load_jsonl(os.path.join(rdir, fn)):
            k = korpus.get(rec.get("id"))
            if not k:
                continue
            gl = None
            if "goldPurposeRef" in k:
                gold = ({"forventet": "ingen", "purposeRefs": []} if k["goldPurposeRef"] == "none"
                        else {"forventet": "formaal", "purposeRefs": [k["goldPurposeRef"]]})
            elif "label" in k:
                gold = kart[k["label"]]
                # Gullfasit fra dommerbenken (fasit/*.jsonl `goldLabel`) går foran generatorens etikett.
                # «ingen» = dommeren avviste begge viste etiketter → telles som graf-hull, ikke som bom.
                # SCORE_UTEN_GULL=1 gir gamle tall for sammenligning.
                gl = None if os.environ.get("SCORE_UTEN_GULL") else silver.get(k["id"], {}).get("goldLabel")
                if gl:
                    gold = kart[gl] if gl in kart else {"forventet": "formaal", "purposeRefs": [], "merknad": "dommeren: ingen av etikettene"}
                    GULL_BRUKT[0] += 1
            else:
                gold = gold_from_fixture(k.get("gold"))
            visible, ranked = prediction(rec)
            mulig = gold["forventet"] not in ("hjelper", "flate", "formaal") or bool(gold.get("purposeRefs") or gold.get("intentKind"))
            if gold["forventet"] == "flate" and not gold.get("endpoints"):
                mulig = False  # ingen flate i katalogen for dette formålet: graf-hull, telles for seg
            top1, rang, utfall = judge_label(visible, ranked, gold) if mulig else (False, None, "graf-hull")
            s = silver.get(k["id"], {})
            items.append({"id": k["id"], "text": k["text"], "label": (gl if ("label" in k and gl) else k.get("label")) or k.get("goldPurposeRef"), "lang": k.get("lang"),
                          "style": k.get("style"), "split": k.get("split", "fixtures"), "forventet": gold["forventet"],
                          "mulig": mulig, "top1": top1, "rang": rang, "utfall": utfall,
                          "synlig": visible, "topK": ranked[:5], "enig": s.get("agreement"), "ms": rec.get("ms")})
        if not items:
            continue
        splits = defaultdict(list)
        for i in items:
            splits[i["split"]].append(i)
        summ = {sp: summarize(v) for sp, v in sorted(splits.items())}
        summ["alle"] = summarize(items)
        if any(i["enig"] is not None for i in items):
            summ["enige (generator = tolk)"] = summarize([i for i in items if i["enig"]])
        report["korpus"][navn] = {"sammendrag": summ, "perId": items}
        md += ["### `%s` — %d meldinger" % (navn, len(items)), "",
               "| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |",
               "|---|---|---|---|---|---|---|---|"]
        for sp, s in summ.items():
            md.append("| %s | %d (%d+/%d−) | %s [%s–%s] | %s | %s | %.2f | %s | %s |" % (
                sp, s["n"], s["nPositive"], s["nNegative"], pct(s["top1"]), pct(s["top1CI95"][0]), pct(s["top1CI95"][1]),
                pct(s["nyttigPositiv"]), pct(s["recallAt3"]), s["mrr"] or 0.0, pct(s["negativePrecision"]), pct(s["alleRiktig"])))
        md += ["", "Utfall (alle): " + ", ".join("%s %d" % kv for kv in Counter(i["utfall"] for i in items).most_common()), ""]
        if any(i["label"] for i in items):
            per = defaultdict(list)
            for i in items:
                per[i["label"]].append(i)
            md += ["| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |", "|---|---|---|---|---|---|---|"]
            for lab in sorted(per, key=lambda l: (sum(x["top1"] for x in per[l]) / len(per[l]), l)):
                v = per[lab]
                c = Counter(x["utfall"] for x in v)
                wrong = Counter(("%s %s" % (x["synlig"].get("kind"), ",".join(x["synlig"].get("refs", [])[:1]))).strip()
                                for x in v if x["utfall"] == "feil handling")
                md.append("| %s | %s | %d/%d | %d | %d | %d | %s |" % (
                    lab, v[0]["forventet"], sum(x["top1"] for x in v), len(v), c.get("stille", 0), c.get("spurte", 0) + c.get("spurte, riktig blant valgene", 0),
                    c.get("feil handling", 0), "; ".join("%s ×%d" % kv for kv in wrong.most_common(2))))
            md.append("")
            for axis in ("style", "lang"):
                grp = defaultdict(list)
                for i in items:
                    grp[i[axis]].append(i)
                md.append("Per %s: " % axis + ", ".join("%s %s (n=%d)" % (g, pct(sum(x["top1"] for x in v) / len(v)), len(v))
                                                    for g, v in sorted(grp.items())))
            md.append("")
        worst = [i for i in items if i["utfall"] == "feil handling"][:12]
        if worst:
            md += ["Eksempler på feil handling (det brukeren ville fått foreslått):", ""]
            for i in worst:
                md.append("- `%s` «%s» → %s %s (forventet %s)" % (
                    i["id"], i["text"][:90], i["synlig"].get("kind"), ",".join(i["synlig"].get("refs", [])[:1]),
                    i["label"] or i["forventet"]))
            md.append("")
    report["gullfasitBrukt"] = GULL_BRUKT[0]
    md += ["", "Gullfasit fra dommerbenken brukt på %d meldinger%s." % (GULL_BRUKT[0], " (slått av med SCORE_UTEN_GULL)" if os.environ.get("SCORE_UTEN_GULL") else "")]
    out = os.path.join(rdir, "rapport-%s-%s.json" % (datetime.date.today().isoformat(), etikett))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    md.append("Full rapport per id: `%s`" % os.path.relpath(out, mdir))
    print("\n".join(md))


if __name__ == "__main__":
    main()
