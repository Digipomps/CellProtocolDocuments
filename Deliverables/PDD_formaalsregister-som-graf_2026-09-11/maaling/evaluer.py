#!/usr/bin/env python3
"""Frozen, paired evaluation of lesson retrieval. Python stdlib, no model calls.

Matcher contract: matcher(query, lessons, context) -> ordered unique lessonRefs.
query is ONLY numbered §0; context has tags, surfaces and packages, never §4,
source, judgments or task identity. Custom CLI adapter: --matcher name=file.py:fn.
Run --help for snapshot, retro, evaluate, pool and power commands.
"""
from __future__ import annotations

import argparse
import ast
import collections
import copy
import datetime as dt
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import random
import re
import statistics as stats
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "Tools/PurposePackages"))
import purpose_dev
from purpose_judgments import save_record, validate_record

LESSON_REF = r"lesson\.[a-z0-9-]+"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def corpus_hash(data):
    return digest({"lessons": data["lessons"], "packages": data["packages"]})


def task_hash(task):
    return digest({k: task[k] for k in ("taskRef", "date", "query", "tags", "surfaces")})


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def section(text, number):
    """Only numbered top-level sections delimit a section; lookup emits ## too."""
    start = re.search(rf"^##\s+(?:§\s*)?{number}[.]?\s+[^\n]*\n", text, re.M)
    if not start:
        return ""
    tail = text[start.end():]
    end = re.search(r"^##\s+(?:§\s*)?\d+[.]?\s+", tail, re.M)
    return tail[:end.start() if end else len(tail)].strip()


def snapshot(repo=REPO):
    repo = Path(repo)
    files = {}

    def read(path):
        data = (repo / path).read_bytes()
        files[path] = hashlib.sha256(data).hexdigest()
        return data.decode("utf-8")

    lessons = json.loads(read("Book/haven_lessons_register_v0.json"))["lessons"]
    packages = json.loads(read("Book/haven_purpose_packages_v0.json"))
    tasks = []
    for folder in sorted((repo / "Deliverables").glob("PDD_*")):
        if not folder.is_dir():
            continue
        if not (folder / "FORMAALSSPEC.md").exists() or not (folder / "STATUS.md").exists():
            raise ValueError(f"ufullstendig oppgave: {folder.name}")
        spec = read(f"Deliverables/{folder.name}/FORMAALSSPEC.md")
        status = read(f"Deliverables/{folder.name}/STATUS.md")
        date = re.search(r"_(\d{4}-\d{2}-\d{2})$", folder.name)
        if not date or not section(spec, 0):
            raise ValueError(f"mangler dato eller §0: {folder.name}")

        def field(name):
            match = re.search(rf"^-\s*{name}:\s*(.*)$", status, re.M)
            return sorted(s.strip() for s in match[1].split(",") if s.strip()) if match else []

        old = re.search(r"##\s*§?0[^\n]*\n(.{0,2500})", spec, re.S)
        tasks.append({"taskRef": folder.name, "date": date[1], "query": section(spec, 0),
                      "legacyQuery": old[1] if old else spec[:2500], "section4": section(spec, 4),
                      "section5": section(spec, 5), "tags": field("tags"), "surfaces": field("surfaces")})
    body = {"schema": "haven.matching-corpus.v1", "lessons": lessons, "packages": packages,
            "tasks": tasks, "files": files}
    body["snapshotHash"] = digest(body)
    return body


def validate_snapshot(data):
    if data.get("schema") != "haven.matching-corpus.v1":
        raise ValueError("ukjent korpusskjema")
    if data.get("snapshotHash") != digest({k: v for k, v in data.items() if k != "snapshotHash"}):
        raise ValueError("snapshot-hash stemmer ikke")
    for items, key in [(data["lessons"], "lessonRef"), (data["tasks"], "taskRef")]:
        if len({x[key] for x in items}) != len(items):
            raise ValueError(f"duplikat {key}")
    return data


def subset(data, exclude_lessons=(), exclude_tasks=()):
    """Explicit cohort restriction. Preserve the parent snapshot and source hashes."""
    if not set(exclude_lessons) <= {l["lessonRef"] for l in data["lessons"]}:
        raise ValueError("ukjent lærdom i eksklusjon")
    if not set(exclude_tasks) <= {t["taskRef"] for t in data["tasks"]}:
        raise ValueError("ukjent oppgave i eksklusjon")
    result = copy.deepcopy(data)
    result["cohort"] = {"parentSnapshotHash": data["snapshotHash"],
                        "excludedLessons": sorted(exclude_lessons), "excludedTasks": sorted(exclude_tasks)}
    result["lessons"] = [l for l in data["lessons"] if l["lessonRef"] not in exclude_lessons]
    result["tasks"] = [t for t in data["tasks"] if t["taskRef"] not in exclude_tasks]
    result.pop("snapshotHash")
    result["snapshotHash"] = digest(result)
    return result


def normalize(text):
    return re.findall(r"[a-zæøå0-9]+", text.lower())


def overlap(lesson, text):
    """Exact normalized five-word shingles; diagnostic, not relevance inference."""
    words = normalize(lesson.get("symptom", "") + " " + lesson.get("prevention", ""))
    other = normalize(text)
    a = {tuple(words[i:i+5]) for i in range(max(0, len(words)-4))}
    b = {tuple(other[i:i+5]) for i in range(max(0, len(other)-4))}
    return len(a & b) / len(a) if a else 0.0


def retrospective(data):
    """Positive-only silver labels; missing evidence is never a negative."""
    rows, unknown = [], []
    known = {x["lessonRef"] for x in data["lessons"]}
    for task in data["tasks"]:
        sec4 = task["section4"]
        auto = "Formålspakker som festes" in sec4 or "Lærdommer du må lese før dekomponering" in sec4
        cited = set(re.findall(LESSON_REF, sec4))
        unknown.extend({"taskRef": task["taskRef"], "lessonRef": ref} for ref in sorted(cited - known))
        for lesson in data["lessons"]:
            evidence = []
            source = str(lesson.get("source", ""))
            # A complete directory component, not a similarly prefixed task name.
            pattern = rf"(?<![\w-]){re.escape(task['taskRef'])}(?=$|[/\s#;,:.)])"
            if re.search(pattern, source):
                evidence.append({"kind": "source", "anchor": source})
            if lesson["lessonRef"] in cited:
                evidence.append({"kind": "auto_ref" if auto else "curated_ref",
                                 "anchor": f"Deliverables/{task['taskRef']}/FORMAALSSPEC.md#4"})
            score = overlap(lesson, sec4)
            if score >= 0.5:
                evidence.append({"kind": "overlap", "score": round(score, 6),
                                 "autoSection": auto})
            if evidence:
                rows.append({"taskRef": task["taskRef"], "lessonRef": lesson["lessonRef"],
                             "availableBeforeTaskDate": lesson["date"] < task["date"],
                             "evidence": evidence})
    judgments = [{"taskRef": row["taskRef"], "lessonRef": row["lessonRef"], "relevant": True,
                  "basis": "source"} for row in rows if any(e["kind"] == "source" for e in row["evidence"])]
    return {"schema": "haven.matching-silver.v1", "snapshotHash": data["snapshotHash"],
            "positiveOnly": True, "judgments": judgments, "rows": rows, "unknownSection4Refs": unknown}


def tag_matcher(query, lessons, context):
    """Adapter to the actual existing lookup functions; preserves register order."""
    tags, surfaces = set(context["tags"]), set(context["surfaces"])
    attached = purpose_dev.attach(context["packages"], tags, surfaces)
    refs = {n["purposeRef"] for p in attached for n in p["purposes"]}
    refs.update(r for p in attached for r in p.get("inheritedPurposeRefs", []))
    return [l["lessonRef"] for l in purpose_dev.matching_lessons({"lessons": lessons}, tags, surfaces, refs)]


def spike_functions():
    """Read the existing spike's functions without its corpus IO/printing.

    This reuses its actual tokenizer, weighting and cosine, including tie order.
    AST allowlist extracts only STOPP and function definitions from the local file.
    """
    path = HERE / "spike_tfidf_baseline.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    selected = [n for n in tree.body if
                (isinstance(n, ast.FunctionDef) and n.name in {"tok", "vek", "cos"}) or
                (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "STOPP" for t in n.targets))]
    namespace = {"math": math, "re": re, "collections": collections}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def tfidf_matcher(query, lessons, context):
    if not lessons:
        return []
    f = spike_functions()
    docs = {l["lessonRef"]: f["tok"](" ".join([l.get("symptom", ""), l.get("cause", ""),
            l.get("prevention", ""), " ".join(l.get("tags", []))])) for l in lessons}
    df = collections.Counter()
    for words in docs.values():
        df.update(set(words))
    f["N"] = len(docs)
    f["idf"] = {t: math.log(len(docs)/(1+df[t]))+1 for t in df}
    vectors = {r: f["vek"](d) for r, d in docs.items()}
    q = f["vek"](f["tok"](query))
    return [r for _, r in sorted(((f["cos"](q, v), r) for r, v in vectors.items()), reverse=True)]


def load_matcher(spec):
    builtins = {"tag": tag_matcher, "tfidf": tfidf_matcher}
    if spec in builtins:
        return spec, builtins[spec]
    try:
        name, target = spec.split("=", 1)
        filename, fn = target.rsplit(":", 1)
        module_spec = importlib.util.spec_from_file_location("matching_candidate_" + name, filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        matcher = getattr(module, fn)
        if not name or not callable(matcher):
            raise ValueError("matcher må være en funksjon med et navn")
        return name, matcher
    except (ValueError, AttributeError, OSError) as exc:
        raise ValueError("matcher må være tag, tfidf eller navn=fil.py:funksjon") from exc


def available_lessons(data, task, temporal):
    return [l for l in data["lessons"] if not temporal or l["date"] < task["date"]]


def run_matcher(matcher, data, task, temporal=False, legacy=False):
    lessons = available_lessons(data, task, temporal)
    # Remove labels/provenance from the function's inputs; this is not a process sandbox.
    allowed = {"lessonRef", "symptom", "cause", "prevention", "tags", "purposeRefs"}
    clean = [{k: copy.deepcopy(v) for k, v in l.items() if k in allowed} for l in lessons]
    context = copy.deepcopy({"tags": task["tags"], "surfaces": task["surfaces"], "packages": data["packages"]})
    ranking = list(matcher(task["legacyQuery"] if legacy else task["query"], clean, context))
    if any(not isinstance(r, str) for r in ranking) or len(ranking) != len(set(ranking)):
        raise ValueError("matcher må returnere unike lessonRef-strenger, i rangert rekkefølge")
    if not set(ranking) <= {l["lessonRef"] for l in lessons}:
        raise ValueError("matcher returnerte en lærdom utenfor tilgjengelig korpus")
    return ranking


def paragraphs(lesson):
    """Two displayed fields, split further on blank lines. No guessed reading time."""
    return sum(len([p for p in re.split(r"\n\s*\n", lesson.get(f, "").strip()) if p.strip()])
               for f in ("symptom", "prevention"))


def score(ranking, labels, lessons, k):
    if k < 1:
        raise ValueError("k må være positiv")
    refs = {l["lessonRef"] for l in lessons}
    labels = {r: v for r, v in labels.items() if r in refs}
    positives = {r for r, v in labels.items() if v}
    top = ranking[:k]
    hits = sum(r in positives for r in top)
    unknown = sum(r not in labels for r in top)
    relevant_rank = next((i for i, r in enumerate(ranking, 1) if r in positives), None)
    possible_rank = next((i for i, r in enumerate(ranking, 1) if labels.get(r) is not False), None)
    cost = {l["lessonRef"]: paragraphs(l) for l in lessons}
    return {"p_lo": hits/k, "p_hi": (hits+unknown)/k,
            "recall_known": hits/len(positives) if positives else None,
            "mrr_lo": 1/relevant_rank if relevant_rank else 0.0,
            "mrr_hi": 1/possible_rank if possible_rank else 0.0,
            "mrr_known": (1/relevant_rank if relevant_rank else 0.0) if positives else None,
            "mrr_at_k_known": (1/relevant_rank if relevant_rank and relevant_rank <= k else 0.0) if positives else None,
            "judged_at_k": (len(top)-unknown)/len(top) if top else 1.0,
            "known_positives": len(positives), "catalogue_judged": len(labels) == len(refs),
            "returned": len(ranking), "shown": len(top),
            "paragraphs": sum(cost[r] for r in top), "paragraphs_all": sum(cost[r] for r in ranking),
            "noise_lo": sum(cost[r] for r in top if labels.get(r) is False),
            "noise_hi": sum(cost[r] for r in top if r not in positives)}


def quantile(values, fraction):
    values = sorted(values)
    pos = (len(values)-1)*fraction
    lo = int(pos)
    return values[lo] + (values[min(lo+1, len(values)-1)]-values[lo])*(pos-lo)


def paired_stats(differences, iterations=10000, seed=20260911):
    """Paired task bootstrap and two-sided within-task sign permutation."""
    if iterations < 1:
        raise ValueError("iterations må være positiv")
    if not differences:
        return {"n": 0, "mean": None, "ci95": None, "p": None}
    rng = random.Random(seed)
    n = len(differences)
    mean = stats.mean(differences)
    boot = [stats.mean(rng.choices(differences, k=n)) for _ in range(iterations)]
    nonzero = [d for d in differences if d != 0]
    target = abs(sum(differences))
    if len(nonzero) <= 19:
        values = (abs(sum(sign*d for sign, d in zip(signs, nonzero)))
                  for signs in itertools.product((-1, 1), repeat=len(nonzero)))
        count = 2**len(nonzero)
        p = sum(v >= target-1e-12 for v in values)/count
        method = "exact"
    else:
        extreme = sum(abs(sum(rng.choice((-1, 1))*d for d in nonzero)) >= target-1e-12
                      for _ in range(iterations))
        p = (extreme+1)/(iterations+1)
        method = "monte-carlo-plus-one"
    return {"n": n, "mean": mean, "sd": stats.stdev(differences) if n > 1 else None,
            "ci95": [quantile(boot, .025), quantile(boot, .975)], "p": p,
            "permutation": method, "nonzeroPairs": len(nonzero), "iterations": iterations, "seed": seed}


def truth_labels(data, truth, human_paths=()):
    labels = {t["taskRef"]: {} for t in data["tasks"]}
    if truth == "human":
        tasks = {t["taskRef"]: t for t in data["tasks"]}
        selected = set()
        for path in human_paths:
            record = validate_record(read_json(path))
            if record["taskRef"] not in labels or record["corpusHash"] != corpus_hash(data):
                raise ValueError("menneskefasit tilhører et annet lærdoms-/pakkekorpus eller oppgave")
            task = tasks[record["taskRef"]]
            if record["taskHash"] != task_hash(task) or record["query"] != task["query"]:
                raise ValueError("oppgaveinput er endret siden menneskevurderingen")
            if record["lessons"] != data["lessons"]:
                raise ValueError("lærdomsteksten i menneskefasit avviker fra snapshot")
            selected.add(record["taskRef"])
            for row in record["judgments"]:
                dest = labels[record["taskRef"]]
                if row["lessonRef"] in dest and dest[row["lessonRef"]] != row["relevant"]:
                    raise ValueError("motstridende menneskevurderinger; avklar før evaluering")
                dest[row["lessonRef"]] = row["relevant"]
        # Never fill missing human tasks with silver labels.
        return {t: labels[t] for t in sorted(selected)}
    kinds = {"source": {"source"}, "curated": {"source", "curated_ref"},
             "overlap": {"source", "curated_ref", "overlap"}}[truth]
    for row in retrospective(data)["rows"]:
        if kinds & {e["kind"] for e in row["evidence"]}:
            labels[row["taskRef"]][row["lessonRef"]] = True
    return labels


def evaluate(matchers, data, labels, k=10, temporal=False, legacy=False, iterations=10000, seed=20260911):
    """Public API: supply any mapping name -> matcher function; all share labels."""
    per_task, summaries = {}, {}
    for name, matcher in matchers.items():
        rows = {}
        for task in data["tasks"]:
            if task["taskRef"] not in labels:
                continue
            ranking = run_matcher(matcher, data, task, temporal, legacy)
            rows[task["taskRef"]] = score(ranking, labels[task["taskRef"]], available_lessons(data, task, temporal), k)
            rows[task["taskRef"]]["ranking"] = ranking
        per_task[name] = rows
        keys = ["p_lo", "p_hi", "recall_known", "mrr_lo", "mrr_hi", "mrr_known", "mrr_at_k_known", "paragraphs",
                "paragraphs_all", "noise_lo", "noise_hi", "returned", "shown", "judged_at_k"]
        summary = {key: stats.mean(vals) if (vals := [r[key] for r in rows.values() if r[key] is not None]) else None for key in keys}
        summary.update(n=len(rows), n_positive=sum(r["known_positives"] > 0 for r in rows.values()),
                       n_complete=sum(r["catalogue_judged"] for r in rows.values()))
        sets = [set(r["ranking"][:k]) for r in rows.values()]
        js = [len(a & b)/len(a | b) if a | b else 1.0 for a, b in itertools.combinations(sets, 2)]
        summary["jaccard_at_k"] = stats.mean(js) if js else None
        summary["common_at_k"] = len(set.intersection(*sets)) if sets else 0
        summaries[name] = summary
    pairs = []
    for a, b in itertools.combinations(matchers, 2):
        for metric in ("recall_known", "p_exact", "mrr_exact"):
            differences = []
            for task, ra in per_task[a].items():
                rb = per_task[b][task]
                key = {"p_exact": "p_lo", "mrr_exact": "mrr_lo"}.get(metric, metric)
                if metric.endswith("exact"):
                    upper = "p_hi" if metric == "p_exact" else "mrr_hi"
                    if ra[key] != ra[upper] or rb[key] != rb[upper]:
                        continue
                if ra[key] is not None and rb[key] is not None:
                    differences.append(rb[key]-ra[key])
            pairs.append({"a": a, "b": b, "metric": metric, **paired_stats(differences, iterations, seed)})
    # Bonferroni over defined pairs/metrics in this invocation; cross-run selection is not corrected.
    m = sum(p["p"] is not None for p in pairs)
    for pair in pairs:
        pair["p_bonferroni"] = min(1, pair["p"]*m) if pair["p"] is not None else None
    return {"snapshotHash": data["snapshotHash"], "k": k, "temporal": temporal,
            "queryMode": "legacy-2500" if legacy else "numbered-section-0", "summaries": summaries,
            "paired": pairs, "perTask": per_task}


def fmt(x):
    return "NA" if x is None else f"{x:.3f}"


def print_report(report):
    k = report["k"]
    print(f"Snapshot {report['snapshotHash']}; k={k}; før dato={report['temporal']}; query={report['queryMode']}")
    print("Intervall = uvurdert relevans, IKKE konfidensintervall. R+ / MRR+ bruker kun kjente positiver.")
    print(f"| Matcher | n / n+ / fullt | P@{k} [lo,hi] | R+@{k} | MRR+ / MRR+@{k} | MRR [lo,hi] | Vurdert@k | Avsnitt@k / rangering | Støyavsnitt [lo,hi] |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, s in report["summaries"].items():
        print(f"| {name} | {s['n']} / {s['n_positive']} / {s['n_complete']} | {fmt(s['p_lo'])}–{fmt(s['p_hi'])} | {fmt(s['recall_known'])} | {fmt(s['mrr_known'])} / {fmt(s['mrr_at_k_known'])} | {fmt(s['mrr_lo'])}–{fmt(s['mrr_hi'])} | {fmt(s['judged_at_k'])} | {fmt(s['paragraphs'])} / {fmt(s['paragraphs_all'])} | {fmt(s['noise_lo'])}–{fmt(s['noise_hi'])} |")
    print("\nParvise forskjeller B−A; oppgavebootstrap 95 %, tosidig fortegnspermutasjon. Diagnostikk, ingen vinnerkonklusjon.")
    for pair in report["paired"]:
        print(f"{pair['b']}−{pair['a']} {pair['metric']}: n={pair['n']}, Δ={fmt(pair['mean'])}, CI={pair['ci95']}, p={fmt(pair['p'])}, p_Bonf={fmt(pair['p_bonferroni'])}")


def pool(data, task_ref, matchers, k, seed):
    task = next((t for t in data["tasks"] if t["taskRef"] == task_ref), None)
    if task is None:
        raise ValueError("ukjent taskRef")
    rankings = {name: run_matcher(fn, data, task) for name, fn in matchers.items()}
    presented = sorted({r for ranking in rankings.values() for r in ranking[:k]})
    random.Random(seed).shuffle(presented)
    tests = {t["testRef"] for p in data["packages"]["packages"] for n in p["purposes"] for t in n.get("derivedTests", [])}
    tests.update(re.findall(r"\btest\.[a-zA-Z0-9_.-]+", task["section5"]))
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    return {"schema": "haven.matching-judgment.v1", "taskRef": task_ref, "snapshotHash": data["snapshotHash"],
            "corpusHash": corpus_hash(data), "taskHash": task_hash(task),
            "query": task["query"], "stage": "G1", "createdAt": now, "updatedAt": now,
            "annotationSeconds": 0, "lessons": data["lessons"], "tests": sorted(tests),
            "rankings": rankings, "presented": presented, "judgments": []}


def power_rows():
    z = stats.NormalDist().inv_cdf(.975) + stats.NormalDist().inv_cdf(.8)
    return [{"sd": sd, "mde80_n19": z*sd/math.sqrt(19),
             "n_for_delta": {str(delta): math.ceil((z*sd/delta)**2) for delta in (.05, .1, .2)}}
            for sd in (.1, .2, .3, .5)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    snap = sub.add_parser("snapshot", help="frys lokalt korpus med innhold og filhasher")
    snap.add_argument("--repo", type=Path, default=REPO); snap.add_argument("--out", required=True)
    snap.add_argument("--corpus-from", help="gjenbruk frosne lærdommer/pakker mens nye oppgaver tilføyes")
    restrict = sub.add_parser("subset", help="dokumenter eksplisitt eksklusjon fra et lagret snapshot")
    restrict.add_argument("--snapshot", required=True); restrict.add_argument("--out", required=True)
    restrict.add_argument("--exclude-lesson", action="append", default=[])
    restrict.add_argument("--exclude-task", action="append", default=[])
    retro = sub.add_parser("retro", help="utled kilde-, sitat- og overlappevidens")
    retro.add_argument("--snapshot", required=True); retro.add_argument("--out", required=True)
    ev = sub.add_parser("evaluate", help="samme oppgaver, korpus, k og fasit for alle funksjoner")
    pl = sub.add_parser("pool", help="frys kandidatunion for blind menneskevurdering ved G1")
    for command in (ev, pl):
        command.add_argument("--snapshot", required=True)
        command.add_argument("--matcher", action="append", help="tag, tfidf eller navn=fil.py:funksjon; kan gjentas")
        command.add_argument("--k", type=int, default=10)
        command.add_argument("--seed", type=int, default=20260911)
        command.add_argument("--out", required=command is pl)
    pl.add_argument("--task", required=True)
    ev.add_argument("--truth", choices=["source", "curated", "overlap", "human"], default="source")
    ev.add_argument("--human", action="append", default=[])
    ev.add_argument("--before-task-date", action="store_true", help="konservativ datofilter, ikke historisk G1-replay")
    ev.add_argument("--legacy-query", action="store_true", help="kun yardstick: spikes opprinnelige 2500 tegn")
    ev.add_argument("--iterations", type=int, default=10000)
    sub.add_parser("power", help="scenarioer: normaltilnærming, alpha .05, styrke .80")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "snapshot":
            data = snapshot(args.repo)
            if args.corpus_from:
                parent = validate_snapshot(read_json(args.corpus_from))
                data["lessons"], data["packages"] = parent["lessons"], parent["packages"]
                data["corpusParentSnapshotHash"] = parent["snapshotHash"]
                for path in ("Book/haven_lessons_register_v0.json", "Book/haven_purpose_packages_v0.json"):
                    data["files"][path] = parent["files"][path]
                data.pop("snapshotHash")
                data["snapshotHash"] = digest(data)
            validate_snapshot(data); write_json(args.out, data)
            print(f"{len(data['tasks'])} oppgaver, {len(data['lessons'])} lærdommer; {data['snapshotHash']}")
            return 0
        if args.cmd == "power":
            print(json.dumps(power_rows(), indent=2)); return 0
        data = validate_snapshot(read_json(args.snapshot))
        if args.cmd == "subset":
            result = subset(data, args.exclude_lesson, args.exclude_task); write_json(args.out, result)
            print(f"{len(result['tasks'])} oppgaver, {len(result['lessons'])} lærdommer; {result['snapshotHash']}")
            return 0
        if args.cmd == "retro":
            result = retrospective(data); write_json(args.out, result)
            counts = collections.Counter(e["kind"] for r in result["rows"] for e in r["evidence"])
            source_tasks = {r["taskRef"] for r in result["rows"] if any(e["kind"] == "source" for e in r["evidence"])}
            print(f"Evidenspar {dict(counts)}; source-oppgaver {len(source_tasks)}; ukjente refs {len(result['unknownSection4Refs'])}")
            return 0
        if args.k < 1 or getattr(args, "iterations", 1) < 1:
            raise ValueError("k og iterations må være positive")
        specs = args.matcher or ["tag", "tfidf"]
        matchers = {}
        for spec in specs:
            name, fn = load_matcher(spec)
            if name in matchers:
                raise ValueError("duplisert matchernavn")
            matchers[name] = fn
        if args.cmd == "pool":
            if Path(args.out).exists():
                raise ValueError("pool-output finnes; velg ny fil for en ny kjøring")
            record = pool(data, args.task, matchers, args.k, args.seed)
            save_record(args.out, record)
            print(f"{len(record['presented'])} unike lærdommer; ingen menneskedommer opprettet. {args.out}")
            return 0
        if args.truth == "human" and not args.human:
            raise ValueError("--truth human krever --human; sølvfasit brukes aldri som reserve")
        started = time.perf_counter()
        labels = truth_labels(data, args.truth, args.human)
        report = evaluate(matchers, data, labels, args.k, args.before_task_date,
                          args.legacy_query, args.iterations, args.seed)
        code_files = [Path(__file__), Path(purpose_dev.__file__), HERE / "spike_tfidf_baseline.py",
                      REPO / "Tools/PurposePackages/purpose_judgments.py",
                      REPO / "Tools/PurposePackages/matching_judgment.schema.json"]
        code_files += [Path(s.split("=", 1)[1].rsplit(":", 1)[0]) for s in specs if "=" in s]
        report.update(truth=args.truth, elapsedSeconds=time.perf_counter()-started,
                      matcherSpecs=specs, codeHashes={str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in code_files},
                      labelsHash=digest(labels),
                      humanFileHashes={str(p): hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in args.human})
        print_report(report)
        if args.out:
            write_json(args.out, report)
        return 0
    except (ValueError, OSError) as exc:
        print(f"FEIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
