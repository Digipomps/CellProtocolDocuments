#!/usr/bin/env python3
"""Bounded max-product activation on actual purposeRefs; no new runtime.

Mirrors best-path multiplicative evidence, not a full Swift parity port. For
fixed H <= 3, scans O(H*E), avoiding enumeration of all paths and feedback loops.
No parentRef edges: the measured ablation is strictly lesson <-> purposeRefs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leksikon import Lexicon, load_data, top_refs


class Spread:
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.edges = []
        self.by_lesson = {}
        for ref, lesson in lexicon.lessons.items():
            purposes = sorted(set(lesson.get('purposeRefs', [])))
            missing = set(purposes) - lexicon.purposes.keys()
            if missing:
                raise ValueError(f'Undeclared purposes: {sorted(missing)}')
            self.by_lesson[ref] = purposes
            self.edges.extend((p, ref) for p in purposes)

    def activate(self, query, hops=1, damping=.5, weights=None, lexical_weights=None):
        if hops not in range(4) or not 0 <= damping < 1:
            raise ValueError('Use 0..3 hops and damping in [0,1).')
        best = self.lexicon.activate(query, lexical_weights)
        paths = {r: [r] for r in best}
        seeds = dict(best)
        for _ in range(hops):
            previous, previous_paths = dict(best), dict(paths)
            for purpose, lesson in self.edges:
                weight = .5 if weights is None else weights.get((purpose, lesson), .5)
                for source, target in ((purpose, lesson), (lesson, purpose)):
                    value = previous.get(source, 0) * damping * weight
                    if value > best.get(target, 0):
                        best[target] = value
                        paths[target] = previous_paths[source] + [target]
        return best, paths, seeds

    def rank(self, query, hops=1, damping=.5, weights=None, lexical_weights=None, k=None):
        scores, _, _ = self.activate(query, hops, damping, weights, lexical_weights)
        return top_refs(scores, self.lexicon.lessons, k)


def one_hop(query, lessons, context):
    return Spread(Lexicon(lessons, context['packages'])).rank(query, 1)


def two_hops(query, lessons, context):
    return Spread(Lexicon(lessons, context['packages'])).rank(query, 2)


def three_hops(query, lessons, context):
    return Spread(Lexicon(lessons, context['packages'])).rank(query, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='deploy')
    args = parser.parse_args()
    data = load_data()
    model = Spread(Lexicon(data['lessons'], data['packages']))
    result = []
    for hops in (0, 1, 2, 3):
        scores, paths, seeds = model.activate(args.query, hops)
        result.append({'hops': hops, 'activeLessons': sum(scores.get(r, 0) > 0 for r in model.lexicon.lessons),
            'top10': [{'ref': r, 'score': scores.get(r, 0), 'seed': seeds.get(r, 0),
                       'path': paths.get(r, [])} for r in model.rank(args.query, hops, k=10)]})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
