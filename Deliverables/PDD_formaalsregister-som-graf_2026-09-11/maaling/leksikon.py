#!/usr/bin/env python3
"""Deterministic text -> node activations. Experimental adapter, stdlib only.

No source, task identity or relevance labels enter the matcher. Uses the frozen
44-lesson evaluator snapshot by default. CLI: leksikon.py 'ikke bruk docker'.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import heapq
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evaluer

PURPOSE_PATH = evaluer.REPO / 'Book/haven_purpose_knowledge_base_v0.json'
SNAPSHOT_PATH = HERE / 'korpus_44.json'
_SPIKE = evaluer.spike_functions()
tok = _SPIKE['tok']


def lesson_text(lesson):
    return ' '.join([lesson.get('symptom', ''), lesson.get('cause', ''),
                     lesson.get('prevention', ''), ' '.join(lesson.get('tags', []))])


def purpose_nodes(packages):
    """Book 23 plus declared package nodes; never synthesize missing purposes."""
    nodes = {n['purposeRef']: n for n in evaluer.read_json(PURPOSE_PATH)['nodes']}
    for package in packages.get('packages', []):
        for node in package.get('purposes', []):
            nodes.setdefault(node['purposeRef'], node)
    return nodes


def purpose_text(node):
    hints = node.get('matchingHints', {})
    return ' '.join([node.get('title', ''), node.get('summary', ''),
                     ' '.join(node.get('interests', [])),
                     ' '.join(hints.get('aliases', [])),
                     ' '.join(hints.get('tokens', []))])


def top_refs(scores, refs, k=None):
    """Fixed-k selection is O(N log k); full ordering is O(N log N)."""
    key = lambda ref: (-scores.get(ref, 0.0), ref)
    return sorted(refs, key=key) if k is None else heapq.nsmallest(k, refs, key=key)


class Lexicon:
    def __init__(self, lessons, packages):
        self.lessons = {l['lessonRef']: l for l in lessons}
        self.purposes = purpose_nodes(packages)
        texts = {r: purpose_text(n) for r, n in self.purposes.items()}
        texts.update({r: lesson_text(l) for r, l in self.lessons.items()})
        self.forms = {r: sorted(set(re.findall(r'[a-zæøå0-9\-]{3,}', s.lower())))
                      for r, s in texts.items()}
        self.tokens = {r: set(tok(s)) for r, s in texts.items()}
        df = Counter(t for ts in self.tokens.values() for t in ts)
        self.idf = {t: 1 + math.log((1 + len(texts))/(1 + count)) for t, count in df.items()}
        self.norms = {r: math.sqrt(math.fsum(self.idf[t]**2 for t in sorted(ts))) or 1
                      for r, ts in self.tokens.items()}
        self.postings = defaultdict(list)
        for ref, ts in self.tokens.items():
            for token in sorted(ts):
                self.postings[token].append(ref)

    def activate(self, query, weights=None):
        """Binary IDF cosine; weights on observed token->node incidence edges.

        Original seven/five-character stems deliberately retain the spike's
        limitations. Unknown tokens do not activate nodes. Negation is lost.
        """
        tokens = sorted(set(tok(query)) & self.idf.keys())
        norm = math.sqrt(sum(self.idf[t]**2 for t in tokens)) or 1
        scores = defaultdict(float)
        for token in tokens:
            for ref in self.postings[token]:
                factor = 1.0 if weights is None else weights.get((token, ref), .5)/.5
                scores[ref] += self.idf[token]**2 * factor / (norm*self.norms[ref])
        return dict(scores)

    def rank(self, query, k=None, weights=None):
        return top_refs(self.activate(query, weights), self.lessons, k)

    def evidence(self, query, ref):
        return sorted(set(tok(query)) & self.tokens[ref])


class BM25:
    """BM25 eq. 86 (Stanford IR): log(N/df), k1=1.2, b=.75.

    Same document fields and tokenizer as the TF-IDF spike. Query terms are
    binary; there is no tuning against this small source-positive cohort.
    """
    def __init__(self, lessons):
        self.docs = {l['lessonRef']: Counter(tok(lesson_text(l))) for l in lessons}
        self.lengths = {r: sum(ts.values()) for r, ts in self.docs.items()}
        self.average = sum(self.lengths.values()) / max(1, len(self.docs)) or 1
        df = Counter(t for ts in self.docs.values() for t in ts)
        self.idf = {t: math.log(len(self.docs)/n) for t, n in df.items()}
        self.postings = defaultdict(list)
        for ref, ts in self.docs.items():
            for token, freq in ts.items():
                self.postings[token].append((ref, freq))

    def scores(self, query):
        scores = defaultdict(float)
        for token in sorted(set(tok(query))):
            for ref, freq in self.postings.get(token, ()):
                scores[ref] += self.idf[token] * freq * 2.2 / (
                    freq + 1.2 * (.25 + .75*self.lengths[ref]/self.average))
        return dict(scores)

    def rank(self, query, k=None):
        return top_refs(self.scores(query), self.docs, k)


def matcher(query, lessons, context):
    return Lexicon(lessons, context['packages']).rank(query)


def bm25_matcher(query, lessons, context):
    return BM25(lessons).rank(query)


def load_data():
    return evaluer.validate_snapshot(evaluer.read_json(SNAPSHOT_PATH))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='ikke bruk docker')
    parser.add_argument('--k', type=int, default=10)
    args = parser.parse_args()
    data = load_data()
    lex = Lexicon(data['lessons'], data['packages'])
    scores = lex.activate(args.query)
    print(json.dumps({'query': args.query, 'tokens': sorted(set(tok(args.query))),
        'activatedNodes': len(scores), 'lessons': [
            {'ref': r, 'score': scores.get(r, 0), 'matchedStems': lex.evidence(args.query, r)}
            for r in lex.rank(args.query, args.k)]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
