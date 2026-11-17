#!/usr/bin/env python3
"""Reproducible source-positive retrieval experiment and simulated feedback.

python3 laer_vekter.py --out graf_resultater.json
python3 laer_vekter.py --benchmark-only

The primary truth remains incomplete. 'closed_world' is an explicit simulated
oracle assumption, NOT negative human judgments. Ten events reuse four tasks;
leave-one-task-out evaluations never train on that task's source positives.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import random
import statistics
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leksikon import BM25, HERE, PURPOSE_PATH, Lexicon, evaluer, load_data, tok, top_refs
from spredning import Spread

SEED = 20260912
PARAMETERS = dict(prior=.5, success=.6, failure=.3, retention=.98, hops=1, damping=.5)


class Learner:
    def __init__(self, lex, token_edges=True):
        self.lex = lex
        self.spread = Spread(lex)
        self.weights = {}
        self.lexical_weights = {} if token_edges else None
        self.frequency = {r: .5 for r in lex.lessons}

    def feedback(self, query, positives, negatives=()):
        """Only supplied labels update edges; unjudged is not a negative."""
        for weights in (self.weights, self.lexical_weights, self.frequency):
            if weights is not None:
                for edge in weights:
                    weights[edge] = .5 + .98*(weights[edge]-.5)
        activation = self.lex.activate(query)
        peak = max((activation.get(p, 0) for p in self.lex.purposes), default=0) or 1
        qt = set(tok(query))
        for positive, refs in ((True, positives), (False, negatives)):
            for ref in sorted(refs):
                def update(weights, key, eligibility=1):
                    old = weights.get(key, .5)
                    weights[key] = old + (.6*eligibility*(1-old) if positive else -.3*eligibility*old)
                update(self.frequency, ref)
                for purpose in self.spread.by_lesson[ref]:
                    eligibility = activation.get(purpose, 0)/peak
                    if eligibility:
                        update(self.weights, (purpose, ref), eligibility)
                if self.lexical_weights is not None:
                    for token in sorted(qt & self.lex.tokens[ref]):
                        update(self.lexical_weights, (token, ref))

    def rank(self, query, k=None):
        return self.spread.rank(query, weights=self.weights, lexical_weights=self.lexical_weights, k=k)

    def frequency_rank(self, query, k=None):
        # Query-independent control: same rewards and forgetting, no context.
        return top_refs(self.frequency, self.lex.lessons, k)

    def popularity_rank(self, query, k=None):
        # Stronger frequency control: preserve lexical relevance, but let only
        # a query-independent learned per-lesson scalar alter the ranking.
        scores, _, _ = self.spread.activate(query)
        return top_refs({r: scores.get(r, 0)*self.frequency[r]/.5
                         for r in self.lex.lessons}, self.lex.lessons, k)

    def guarded_rank(self, query, k=None):
        """Caller-side severity policy, separate from learned relevance.

        A blocker in the unlearned top five cannot be demoted below fifth.
        Severity is frozen catalogue metadata, not a source-derived label.
        The rule cannot rescue a blocker that lexical retrieval never found.
        """
        base = self.spread.rank(query, k=5)
        protected = [r for r in base if self.lex.lessons[r].get('severity') == 'blocker']
        ranking = self.rank(query, k=max(5, k) if k is not None else None)
        if not set(protected) <= set(ranking[:5]):
            ranking = protected + [r for r in ranking if r not in protected]
        return ranking if k is None else ranking[:k]


def schedule(tasks, labels, count=10):
    usable = [t for t in tasks if labels[t['taskRef']]]
    if not usable:
        return []
    # Ten events, sorted task round robin; no seed/ordering search for gains.
    return [usable[i % len(usable)] for i in range(count)]


def train(lex, tasks, labels, closed_world=False, token_edges=True, count=10):
    model = Learner(lex, token_edges)
    events = []
    for task in schedule(tasks, labels, count):
        positives = set(labels[task['taskRef']])
        negatives = set(lex.lessons)-positives if closed_world else set()
        before = model.rank(task['query'], 10)
        model.feedback(task['query'], positives, negatives)
        events.append({'taskRef': task['taskRef'], 'positives': sorted(positives),
                       'assumedNegatives': len(negatives), 'before10': before,
                       'after10': model.rank(task['query'], 10)})
    return model, events


def random_matcher(query, lessons, context):
    rng = random.Random(f'{SEED}:{hashlib.sha256(query.encode()).hexdigest()}')
    refs = sorted(l['lessonRef'] for l in lessons)
    rng.shuffle(refs)
    return refs


def all_matcher(query, lessons, context):
    return [l['lessonRef'] for l in lessons]


def summary_ci(values, iterations):
    # Same whole-task percentile bootstrap as evaluer.paired_stats. A marginal
    # mean does not need a costly permutation test against the meaningless null 0.
    values = [v for v in values if v is not None]
    if not values:
        return dict(n=0, mean=None, ci95=None)
    rng = random.Random(SEED)
    samples = [statistics.mean(rng.choices(values, k=len(values))) for _ in range(iterations)]
    return dict(n=len(values), mean=statistics.mean(values),
                ci95=[evaluer.quantile(samples, .025), evaluer.quantile(samples, .975)])


def evaluate_candidates(data, labels, matchers, iterations):
    # score/run_matcher are the common evaluator. Cache rankings across k.
    rankings = {name: {t['taskRef']: evaluer.run_matcher(fn, data, t) for t in data['tasks']}
                for name, fn in matchers.items()}
    rows, summaries = {}, {}
    for name, rankings_by_task in rankings.items():
        rows[name] = {}
        for task in data['tasks']:
            ref = task['taskRef']
            five = evaluer.score(rankings_by_task[ref], labels[ref], data['lessons'], 5)
            ten = evaluer.score(rankings_by_task[ref], labels[ref], data['lessons'], 10)
            rows[name][ref] = dict(p5=five['p_lo'], p5Upper=five['p_hi'],
                r10=ten['recall_known'], mrr=ten['mrr_known'], mrr10=ten['mrr_at_k_known'],
                burden10=ten['paragraphs'], burdenAll=ten['paragraphs_all'],
                ranking=rankings_by_task[ref])
        summaries[name] = {metric: summary_ci([r[metric] for r in rows[name].values()], iterations)
                           for metric in ('p5', 'p5Upper', 'r10', 'mrr', 'mrr10', 'burden10', 'burdenAll')}
        sets = [set(r['ranking'][:10]) for r in rows[name].values()]
        summaries[name]['jaccard10'] = statistics.mean(len(a & b)/len(a | b) if a | b else 1
                                                       for a, b in itertools.combinations(sets, 2))
        summaries[name]['common10'] = len(set.intersection(*sets))
    # Integrate random permutations exactly, avoiding a lucky/unlucky seed as
    # the only noise floor. Bootstrap still resamples tasks, never lesson pairs.
    random_rows = {}
    n = len(data['lessons'])
    for task in data['tasks']:
        ref = task['taskRef']
        m = len(labels[ref])
        probs = [(rank, math.comb(n-rank, m-1)/math.comb(n, m))
                 for rank in range(1, n-m+2)] if m else []
        random_rows[ref] = dict(p5=m/n, p5Upper=1.0, r10=min(10,n)/n if m else None,
            mrr=sum(prob/rank for rank, prob in probs) if m else None,
            mrr10=sum(prob/rank for rank, prob in probs if rank <= 10) if m else None,
            burden10=20, burdenAll=88, ranking=None)
    rows['tilfeldig_forventning'] = random_rows
    summaries['tilfeldig_forventning'] = {
        metric: summary_ci([r[metric] for r in random_rows.values()], iterations)
        for metric in ('p5', 'p5Upper', 'r10', 'mrr', 'mrr10', 'burden10', 'burdenAll')}
    summaries['tilfeldig_forventning'].update(jaccard10=None, common10=None)
    comparisons = []
    for a, b in itertools.combinations(rows, 2):
        for metric in ('p5', 'r10', 'mrr', 'burden10'):
            ds = [rows[b][r][metric]-rows[a][r][metric] for r in rows[a]
                  if rows[a][r][metric] is not None and rows[b][r][metric] is not None]
            comparisons.append(dict(a=a, b=b, metric=metric,
                                    **evaluer.paired_stats(ds, iterations, SEED)))
    m = len(comparisons)
    for row in comparisons:
        row['pBonferroni'] = min(1, m*row['p']) if row['p'] is not None else None
    return dict(rows=rows, summaries=summaries, comparisons=comparisons)


def timer(fn, repeats=30):
    values = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        values.append(1000*(time.perf_counter()-start))
    return {'medianMs': statistics.median(values), 'p95Ms': evaluer.quantile(values, .95),
            'maxMs': max(values), 'repeats': repeats}


def benchmark(data, labels):
    lex = Lexicon(data['lessons'], data['packages'])
    graph = Spread(lex)
    model, _ = train(lex, data['tasks'], labels, closed_world=True)
    bm25 = BM25(data['lessons'])
    queries = [t['query'] for t in data['tasks']]
    serving = {name: timer(lambda fn=fn: [fn(q) for q in queries]) for name, fn in {
        'leksikon': lambda q: lex.rank(q, 10),
        'graf1': lambda q: graph.rank(q, 1, k=10),
        'graf2': lambda q: graph.rank(q, 2, k=10),
        'graf3': lambda q: graph.rank(q, 3, k=10),
        'laert': lambda q: model.rank(q, 10),
        'laert_med_blockervern': lambda q: model.guarded_rank(q, 10),
        'bm25': lambda q: bm25.rank(q, 10)}.items()}
    cold = timer(lambda: [Spread(Lexicon(data['lessons'], data['packages'])).rank(q, 3, k=10)
                          for q in queries], 5)
    build_once = timer(lambda: build_and_query(data, queries), 20)
    learning = timer(lambda: train(lex, data['tasks'], labels, closed_world=True), 20)
    # Replicate lessons with unique IDs and same bounded number of purpose edges.
    # This is deliberately a dense-posting stress corpus, not added relevance data.
    scale = []
    query = max(queries, key=len)
    for factor in (1, 10, 100, 500):
        lessons = [dict(l, lessonRef=f'{l["lessonRef"]}@{i}') for i in range(factor) for l in data['lessons']]
        start = time.perf_counter()
        scaled = Spread(Lexicon(lessons, data['packages']))
        build_ms = 1000*(time.perf_counter()-start)
        timing = timer(lambda: scaled.rank(query, 3, k=10), 7)
        scale.append(dict(lessons=len(lessons), nodes=len(scaled.lexicon.tokens),
                          directedEdges=len(scaled.edges)*2, buildMs=build_ms, **timing))
    return dict(platform=platform.platform(), python=platform.python_version(),
                batchQueries=len(queries), servingBatch=serving,
                rebuildPerQueryBatch=cold, buildOnceAndBatch=build_once,
                tenLearningEvents=learning, scale=scale)


def build_and_query(data, queries):
    graph = Spread(Lexicon(data['lessons'], data['packages']))
    return [graph.rank(q, 3, k=10) for q in queries]


def probes(lex, graph, learned, data, labels):
    a, b = lex.activate('ikke bruk docker'), lex.activate('bruk docker')
    deploy = []
    for hops in range(4):
        scores, paths, seeds = graph.activate('deploy', hops)
        activated = {r for r in lex.lessons if scores.get(r, 0) > 0}
        deploy.append(dict(hops=hops, activeLessons=len(activated),
            newLessons=[dict(ref=r, path=paths[r], score=scores[r])
                        for r in sorted(activated) if seeds.get(r, 0) == 0]))
    blockers = [r for r, l in lex.lessons.items() if l.get('severity') == 'blocker']
    # Diagnostic: one verbatim prevention query per existing blocker. Not source truth.
    blocker_probes = []
    for ref in blockers:
        query = lex.lessons[ref]['prevention']
        before, after = graph.rank(query), learned.rank(query)
        blocker_probes.append(dict(ref=ref, query=query, beforeRank=before.index(ref)+1,
                                  afterRank=after.index(ref)+1,
                                  frequencyRank=learned.frequency_rank(query).index(ref)+1))
    # Explicitly synthetic rare-severe scenario. One blocker event followed by
    # nine source-labelled events. Never mixed into the source evaluation table.
    rare = Learner(lex)
    blocker = blockers[0]
    rare_query = lex.lessons[blocker]['prevention']
    rare.feedback(rare_query, {blocker}, set(lex.lessons)-{blocker})
    for task in schedule(data['tasks'], labels, 9):
        positives = set(labels[task['taskRef']])
        rare.feedback(task['query'], positives, set(lex.lessons)-positives)
    rare_probe = dict(ref=blocker, syntheticRelevance=True, events=10, blockerPositiveEvents=1,
        beforeRank=graph.rank(rare_query).index(blocker)+1,
        afterRank=rare.rank(rare_query).index(blocker)+1,
        protectedRank=rare.guarded_rank(rare_query).index(blocker)+1,
        frequencyRank=rare.frequency_rank(rare_query).index(blocker)+1,
        lexicalPopularityRank=rare.popularity_rank(rare_query).index(blocker)+1)
    return dict(negationSameActivation=a == b, dockerNodes=sorted(a), deploy=deploy,
                rollbackLessonCount=sum('rollback' in str(l).lower() for l in lex.lessons.values()),
                blockerSourcePositives=sum(r in lab for lab in labels.values() for r in blockers),
                blockerSelfTextProbes=blocker_probes, syntheticRareBlocker=rare_probe)


def run(iterations=10000, with_benchmark=True):
    start = time.perf_counter()
    data = load_data()
    labels = evaluer.truth_labels(data, 'source')
    lex = Lexicon(data['lessons'], data['packages'])
    graph = Spread(lex)
    learned, events = train(lex, data['tasks'], labels, closed_world=True)
    positive, _ = train(lex, data['tasks'], labels, closed_world=False)
    refs_only, _ = train(lex, data['tasks'], labels, closed_world=True, token_edges=False)
    # Group holdout; target query is used only to select the correct frozen fold.
    loo = {}
    for task in data['tasks']:
        if labels[task['taskRef']]:
            training_tasks = [t for t in data['tasks'] if t['taskRef'] != task['taskRef']]
            loo[task['query']], _ = train(lex, training_tasks, labels, closed_world=True)
    matchers = {
        'vis_alt44': all_matcher,
        'dagens_tag_vis_alt': evaluer.tag_matcher,
        'tilfeldig': random_matcher,
        'tfidf': evaluer.tfidf_matcher,
        'bm25': lambda q, ls, c: BM25(ls).rank(q),
        'leksikon': lambda q, ls, c: lex.rank(q),
        'graf1': lambda q, ls, c: graph.rank(q, 1),
        'graf2': lambda q, ls, c: graph.rank(q, 2),
        'graf3': lambda q, ls, c: graph.rank(q, 3),
        'laert_refs_trening': lambda q, ls, c: refs_only.rank(q),
        'laert_positiv_trening': lambda q, ls, c: positive.rank(q),
        'laert_lukket_trening': lambda q, ls, c: learned.rank(q),
        'hyppighet_trening': lambda q, ls, c: learned.frequency_rank(q),
        'leksikon_x_hyppighet_trening': lambda q, ls, c: learned.popularity_rank(q),
        'leksikon_x_hyppighet_holdout': lambda q, ls, c: loo.get(q, learned).popularity_rank(q),
        'laert_lukket_holdout': lambda q, ls, c: loo.get(q, learned).rank(q),
        'laert_holdout_blockervern': lambda q, ls, c: loo.get(q, learned).guarded_rank(q),
    }
    checks = self_check(data, labels, lex, graph, learned, loo)
    results = evaluate_candidates(data, labels, matchers, iterations)
    # LOO differs only for four labelled tasks; the other 15 have no training labels.
    results.update(schema='haven.graph-weight-experiment.v1', seed=SEED,
        snapshotHash=data['snapshotHash'], parameters=PARAMETERS,
        hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                [HERE/'leksikon.py', HERE/'spredning.py', HERE/'laer_vekter.py',
                 HERE/'evaluer.py', HERE/'spike_tfidf_baseline.py', PURPOSE_PATH]},
        counts=dict(tasks=len(data['tasks']), positiveTasks=sum(bool(x) for x in labels.values()),
                    positivePairs=sum(len(x) for x in labels.values()), lessons=len(lex.lessons),
                    purposes=len(lex.purposes), tokenTypes=len(lex.idf),
                    incidenceEdges=sum(len(x) for x in lex.tokens.values()),
                    purposeRefsEdges=len(graph.edges)),
        simulationEvents=events, checks=checks, probes=probes(lex, graph, learned, data, labels),
        learnedPurposeWeights=[dict(purpose=p, lesson=l, weight=w) for (p,l),w in sorted(learned.weights.items())])
    if with_benchmark:
        results['benchmark'] = benchmark(data, labels)
    results['elapsedSeconds'] = time.perf_counter()-start
    return results


def self_check(data, labels, lex, graph, learned, loo):
    """Targeted invariants for ranking, missing labels and leakage boundaries."""
    checked_queries = 0
    for task in data['tasks']:
        q = task['query']
        for rank in (lex.rank, learned.rank, learned.guarded_rank, learned.popularity_rank):
            full = rank(q)
            assert len(full) == len(set(full)) == len(lex.lessons)
            assert rank(q, 5) == full[:5] and rank(q, 10) == full[:10]
        for h in range(4):
            assert graph.rank(q, h, k=10) == graph.rank(q, h)[:10]
        protected = {r for r in graph.rank(q, k=5) if lex.lessons[r]['severity'] == 'blocker'}
        assert protected <= set(learned.guarded_rank(q, 5))
        checked_queries += 1
    empty = Learner(lex)
    q = data['tasks'][0]['query']
    before = empty.rank(q)
    empty.feedback(q, set())
    assert not empty.weights and not empty.lexical_weights and empty.rank(q) == before
    assert lex.activate('ikke bruk docker') == lex.activate('bruk docker')
    assert all(edge in graph.edges and 0 <= w <= 1 for edge, w in learned.weights.items())
    assert all(t in lex.tokens[r] and 0 <= w <= 1 for (t,r),w in learned.lexical_weights.items())
    assert len(loo) == sum(bool(l) for l in labels.values())
    assert not set(lex.purposes) & set(lex.lessons)
    return dict(status='passed', queries=checked_queries,
        checks=['full/top-k equivalence', 'unique in-corpus ranks', 'blocker top-5 preservation',
                'unjudged is not negative', 'explicit negation limitation',
                'updates only declared edges with bounded weights', 'four task holdout models'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--iterations', type=int, default=10000)
    parser.add_argument('--benchmark-only', action='store_true')
    parser.add_argument('--no-benchmark', action='store_true')
    args = parser.parse_args()
    if args.benchmark_only:
        data = load_data()
        result = benchmark(data, evaluer.truth_labels(data, 'source'))
    else:
        result = run(args.iterations, not args.no_benchmark)
    if args.out:
        evaluer.write_json(args.out, result)
    if 'summaries' in result:
        for name, values in result['summaries'].items():
            print(name, ' '.join(f'{k}={values[k]["mean"]:.4f}' for k in ('p5','r10','mrr','burden10')),
                  f'J={values["jaccard10"]}')
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
