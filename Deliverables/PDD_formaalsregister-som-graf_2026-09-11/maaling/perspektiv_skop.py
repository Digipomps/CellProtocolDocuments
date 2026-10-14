#!/usr/bin/env python3
"""Offline, declared Perspective + scope ablation; existing evaluator and 44 cohort.

python3 -B <this file> --init-profiles  # explicit one-time extraction; never overwrite
python3 -B <this file>                # reproduce results and pending judgment sheet
No network, model calls, dependencies, product runtime or original input edits.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import re
import statistics as st
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evaluer
from leksikon import Lexicon, PURPOSE_PATH, lesson_text, purpose_text, tok
from spredning import Spread
from laer_vekter import summary_ci, timer

ROOT = HERE.parents[3]
PDD = HERE.parent
PROFILES = HERE / 'perspektiver.json'
RESULT = HERE / 'perspektiv_resultater.json'
SEED = 20260912
ITERATIONS = 10000
K = 10
# Frozen before the first measurement. Order also breaks training-selection ties.
WEIGHTS = {
    '1_tfidf': (1., 0., 0.),
    '2_perspektiv': (0., 1., 0.),
    '3_skop': (0., 0., 1.),
    '4_tekst_perspektiv': (.5, .5, 0.),
    '5_tekst_skop': (.5, 0., .5),
    '6_tekst_perspektiv_skop': (.5, .25, .25),
    '6a_teksttung': (.75, .125, .125),
    '6b_lik': (1/3, 1/3, 1/3),
    '6c_perspektivtung': (.25, .5, .25),
    '6d_skoptung': (.25, .25, .5),
}
GRID = list(WEIGHTS)[5:]
SHORT_QUERIES = ['status', 'hva mangler', 'rydd opp', 'deploy', 'sjekk dette',
                 'neste steg', 'kan vi gå videre', 'virker det',
                 'hva bør jeg passe på', 'hva står igjen', 'hjelp meg videre', 'hva gjør vi nå']
# Each tuple: scope, literal interests, literal entities. Words must occur in §1.
DOMAIN = [
 ('deploy', ['tilstand', 'challenge'], ['agenten', 'menylinjen']),
 ('deploy', ['arbeidskø', 'status'], ['dispatcheren', 'Mac']),
 ('bridge', ['autorisasjon', 'kanal'], ['socket', 'klienten']),
 ('arbeid', ['samtaler', 'ruting'], ['Butler', 'chat']),
 ('correspondence', ['vedlegg', 'kryptert'], ['melding', 'relasjonscellen']),
 ('egne-data', ['redigering', 'tilgang'], ['entiteten', 'AIGateway']),
 ('egne-data', ['nøkkel', 'persist'], ['ScopedCredentialCell', 'scaffoldet']),
 ('kunnskap', ['matching', 'formål'], ['registeret', 'Perspective']),
 ('gui', ['flater', 'paritet'], ['Porthole', 'Binding']),
 ('musikk', ['lyd', 'vern'], ['artisten', 'lytteren']),
 ('musikk', ['avspilling', 'samtykke'], ['artisten', 'lytteren']),
 ('palazzo', [], []),
 ('palazzo', ['kommentar', 'meny'], ['gjesten', 'huset']),
 ('palazzo', ['tilgang', 'formål'], ['gjest', 'personale']),
 ('palazzo', ['artikler', 'interesser'], ['gjesten', 'huset']),
 ('administrasjon', ['mandat', 'tilbakekall'], ['scaffold', 'organisasjonsentitet']),
 ('gui', ['paritet', 'handlinger'], ['Binding', 'Porthole']),
 ('administrasjon', ['grants', 'kvittering'], ['AIGateway', 'WebFetch']),
 ('arbeid', ['arbeidsflyt', 'kø'], ['oppgave', 'agent']),
]
SCOPE_ROOTS = {
 'deploy': ['purpose://scaffold.operations', 'purpose://quality.build-and-regression'],
 'bridge': ['purpose://access.audit.privacy', 'purpose://cell.contract-explicit'],
 'arbeid': ['purpose://project-work.overview-and-sharing', 'purpose://digital-work.coordinate'],
 'correspondence': ['purpose://contact.communication', 'purpose://self-determination.data'],
 'egne-data': ['purpose://self-determination.data', 'purpose://skeleton.owner-entity-access'],
 'kunnskap': ['purpose://grounding', 'purpose://knowledge'],
 'gui': ['purpose://gui.quality.functional-accessible'],
 'musikk': ['purpose://self-determination.data', 'purpose://access.audit.privacy'],
 'palazzo': ['purpose://personal-context.semantic-state', 'purpose://self-determination.data.manner',
             'purpose://contact.communication'],
 'administrasjon': ['purpose://governance', 'purpose://scaffold.operations'],
}


def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def clean_text(s):
    # Goal/verifier references are not semantic matcher input, even in §1.
    s = re.sub(r'\b(?:lesson\.[a-z0-9-]+|test\.[a-zA-Z0-9_.-]+|purpose://[^\s`|)]+)', '', s)
    return re.sub(r'\s+', ' ', s.replace('`', '').replace('*', '')).strip()


def origin(path, line, quote):
    return dict(path=rel(path), line=line, quote=quote, fileSha256=sha(path))


def make_node(ref, title, text, src, weight=1.):
    return dict(ref=ref, title=clean_text(title), text=clean_text(text), weight=weight,
                sources={field: src for field in ('ref', 'title', 'text')},
                weightSource='Simulert, fast lik vekt for formål; 0.5 for interesser/entiteter; ikke observert brukerprioritet.')


def init_profiles(data):
    if PROFILES.exists():
        raise ValueError('perspektiver.json finnes; bevar menneskets rettelser')
    profiles = []
    for task, (scope, interests, entities) in zip(data['tasks'], DOMAIN):
        path = evaluer.REPO / 'Deliverables' / task['taskRef'] / 'FORMAALSSPEC.md'
        lines = path.read_text().splitlines()
        section = []
        inside = False
        for i, line in enumerate(lines, 1):
            if re.match(r'^##\s+(?:§\s*)?1[.]?\s+', line):
                inside = True
                continue
            if inside and re.match(r'^##\s+(?:§\s*)?\d+[.]?\s+', line):
                break
            if inside:
                section.append((i, line))
        purposes = []
        for i, line in section:
            cols = re.split(r'(?<!\\)\|', line)
            if line.startswith('|') and len(cols) >= 6 and ('purpose://' in cols[1] or '…' in cols[1]):
                if not cols[2].strip() or not cols[4].strip():
                    continue
                ref = cols[1].strip().strip('`')
                purposes.append(make_node(ref, cols[2], cols[4], origin(path, i, line)))
                if len(purposes) == 3:
                    break
        if task['taskRef'].startswith('PDD_butler'):
            purposes = []
            for i, last in [(43, 46), (49, 55), (77, 82)]:
                ref = re.search(r'purpose://[^`]+', lines[i-1])[0]
                purposes.append(make_node(ref, lines[i-1], ' '.join(lines[i:last]), origin(path, i, '\n'.join(lines[i-1:last]))))
        if task['taskRef'].startswith('PDD_scaffold-admin'):
            purposes = []
            for i in (70, 74, 78):
                line = lines[i-1]
                ref = re.search(r'purpose://[^`]+', line)[0]
                title = line.split('—', 1)[1]
                purposes.append(make_node(ref, title, title, origin(path, i, line)))
        missing = not purposes
        if missing:
            # Strict §1 provenance: the two requested slots are visibly unknown,
            # have zero weight and never introduce invented semantic content.
            src = origin(path, 20, lines[19])
            purposes = [dict(ref=None, title='ukjent', text='', weight=0.,
                            sources={f: src for f in ('ref', 'title', 'text')},
                            weightSource='ukjent §1; ingen aktivering') for _ in range(2)]
        associated = {}
        for kind, terms in [('interests', interests), ('entities', entities)]:
            values = []
            for term in terms:
                hit = next(((i, l) for i, l in section if term.lower() in l.lower()), None)
                if hit:
                    i, line = hit
                    values.append(make_node('simulated-'+kind+'://'+term.lower(), term, term, origin(path, i, line), .5))
                else:
                    values.append(dict(ref=None, title='ukjent: '+term, text='', weight=0.,
                                       sources={f: origin(path, section[0][0], 'Ordet ikke funnet i §1') for f in ('ref', 'title', 'text')},
                                       weightSource='ukjent; ingen aktivering'))
            associated[kind] = values
        profiles.append(dict(taskRef=task['taskRef'], taskRefSource=rel(path), simulated=True,
            activePurposes=purposes, **associated,
            scope=dict(ref='simulated-scope://'+scope, weight=1.,
                sources={'ref': origin(path, 1, lines[0]), 'weight': 'Deklarert lik skopvekt, ikke målt'},
                assumption='Område valgt manuelt fra oppgavens tittel og §1; ikke observert aktivt skop.'),
            missingSection1Purposes=missing))
    scopes=[]
    for scope, roots in SCOPE_ROOTS.items():
        scopes.append(dict(ref='simulated-scope://'+scope, title=scope,
            purposeRoots=roots, childDecay=.8,
            sources={'ref':'Deklarert simulering, ingen runtime-skopref', 'title':'Deklarert områdenavn',
                     'purposeRoots':'Manuelt områdeforslag fra eksisterende Book/pakkenoder; ikke fasit- eller oppgavespesifikke lærdomskanter.',
                     'childDecay':'Fast simulert bidrag 0.8 per parentRef-ledd'},
            limitation='Ingen kobling til produksjonens skopregister er påstått.'))
    for scope in scopes:
        origins={}
        for ref in scope['purposeRoots']:
            for file in (PURPOSE_PATH, HERE/'korpus_44.json'):
                hit=next((i for i,line in enumerate(file.read_text().splitlines(),1)
                          if '"purposeRef": "'+ref+'"' in line), None)
                if hit:
                    origins[ref]=dict(path=rel(file), line=hit,
                        status='Eksisterende node; koblingen fra skopet er simulert.')
                    break
            assert ref in origins
        scope['purposeRootSources']=origins
    output=dict(schema='haven.simulated-perspective-scope.v1', snapshotHash=data['snapshotHash'],
        status='SIMULERT; Kjetil har ikke bekreftet dette som sitt perspektiv',
        policy='Første tre innholdsfylte formålsrader i §1; Butler: rot+A+B; admin: første tre blad. Ingen §4/source/dom brukes. Forkortede refs er lokale etiketter, aldri oppfunne kanoniske refs.',
        scopePolicy='Alle oppgaver i samme område deler samme skoptre; Book parentRef-etterkommere av purposeRoots. Ingen Arendalsuka-oppgave i kohorten.',
        profiles=profiles, scopes=scopes)
    evaluer.write_json(PROFILES, output)


class Experiment:
    """Serving only sees cleaned lesson fields and declared semantic context.

    Text retains spike cosine and reverse-ref ties. Context is a max-product
    ablation reusing Spread.activate (one hop, .5 damping, .5 edge weight).
    No task IDs, source labels, or annotation provenance enter score functions.
    """
    def __init__(self, lessons, packages, declarations):
        self.lessons = {l['lessonRef']: {k: copy.deepcopy(v) for k, v in l.items()
                       if k in {'lessonRef', 'symptom', 'cause', 'prevention', 'tags', 'purposeRefs'}} for l in lessons}
        self.lex = Lexicon(list(self.lessons.values()), packages)
        self.graph = Spread(self.lex)
        self.f = evaluer.spike_functions()
        docs = {r: self.f['tok'](lesson_text(l)) for r, l in self.lessons.items()}
        df = Counter(t for ts in docs.values() for t in set(ts))
        self.f['N'] = len(docs)
        self.f['idf'] = {t: math.log(len(docs)/(1+n))+1 for t, n in df.items()}
        self.vectors = {r: self.f['vek'](ts) for r, ts in docs.items()}
        self.scopes = {s['ref']: s for s in declarations['scopes']}
        self.scope_nodes = {}
        for ref, scope in self.scopes.items():
            pending = [(r, 0) for r in scope['purposeRoots']]
            depths = {}
            while pending:
                r, depth = pending.pop(0)
                if r in depths and depths[r] <= depth:
                    continue
                if r not in self.lex.purposes:
                    raise ValueError('Ukjent skoptre-rot: '+r)
                depths[r] = depth
                pending.extend((c, depth+1) for c, n in self.lex.purposes.items() if n.get('parentRef') == r)
            self.scope_nodes[ref] = [dict(ref=r, title=self.lex.purposes[r].get('title', ''),
                 text=purpose_text(self.lex.purposes[r]), weight=scope['childDecay']**depth,
                 depth=depth) for r, depth in sorted(depths.items())]
        # Context activations cached by semantic content, not task identity.
        self.context_cache = {}

    @staticmethod
    def semantic_nodes(profile):
        return [{k: n[k] for k in ('ref', 'title', 'text', 'weight')}
                for field in ('activePurposes', 'interests', 'entities') for n in profile[field]
                if n['ref'] is not None and n['weight'] > 0]

    def context_scores(self, nodes):
        key = evaluer.digest(nodes)
        if key in self.context_cache:
            return self.context_cache[key]
        best, evidence = {}, {}
        for node in nodes:
            scores, paths, _ = self.graph.activate(node['title']+' '+node['text'], hops=1)
            # An explicitly known active purpose can also seed its existing refs.
            if node['ref'] in self.lex.purposes:
                for p, r in self.graph.edges:
                    if p == node['ref'] and .25 > scores.get(r, 0):
                        scores[r], paths[r] = .25, [p, r]
            for r in self.lessons:
                score = node['weight']*scores.get(r, 0.)
                if score > best.get(r, 0.):
                    best[r] = score
                    evidence[r] = dict(seedRef=node['ref'], seedTitle=node['title'],
                        path=paths[r], matchedStems=self.lex.evidence(node['title']+' '+node['text'], paths[r][0])[:8],
                        rawContribution=round(score, 8))
        value = (self.normalize(best), evidence)
        self.context_cache[key] = value
        return value

    @staticmethod
    def normalize(scores):
        peak = max(scores.values(), default=0.) or 1.
        return {r: v/peak for r, v in scores.items()}

    def components(self, query, profile):
        q = self.f['vek'](self.f['tok'](query))
        text = self.normalize({r: self.f['cos'](q, v) for r, v in self.vectors.items()})
        perspective, pe = self.context_scores(self.semantic_nodes(profile))
        scope, se = self.context_scores(self.scope_nodes[profile['scope']['ref']])
        return (text, perspective, scope), (pe, se)

    def rank(self, components, weights, k=None):
        scores = {r: sum(w*c.get(r, 0.) for w, c in zip(weights, components)) for r in self.lessons}
        ranking = sorted(self.lessons, key=lambda r: (scores[r], r), reverse=True)
        return ranking if k is None else ranking[:k]

    def adapter(self, profile, weights):
        # Evaluation orchestration binds the profile; matcher receives no taskRef.
        def matcher(query, lessons, context):
            assert {l['lessonRef'] for l in lessons} == set(self.lessons)
            components, _ = self.components(query, profile)
            return self.rank(components, weights)
        return matcher

    def package(self, query, profile, weights, ranking, components, evidence):
        pe, se = evidence
        nodes=[]
        for r in ranking[:K]:
            reasons={}
            if weights[0]:
                reasons['text'] = dict(score=round(components[0].get(r, 0), 6),
                    matchedStems=sorted(set(tok(query)) & self.lex.tokens[r])[:8])
            for i, (name, es) in enumerate([('perspective', pe), ('scope', se)], 1):
                if weights[i] and r in es:
                    reasons[name] = dict(es[r], normalizedScore=round(components[i].get(r, 0), 6))
            nodes.append(dict(self.lessons[r], evidence=reasons))
        return dict(schema='haven.experimental-context-pack.v1', query=query,
                    weights=list(weights), nodes=nodes)


def stats_for_rows(rows, iterations):
    return {metric: summary_ci([r[metric] for r in rows.values()], iterations)
            for metric in ('p5', 'p5Upper', 'r10', 'mrr', 'mrr10', 'burden10')}


def score_row(ranking, labels, lessons):
    five = evaluer.score(ranking, labels, lessons, 5)
    ten = evaluer.score(ranking, labels, lessons, K)
    return dict(p5=five['p_lo'], p5Upper=five['p_hi'], r10=ten['recall_known'],
        mrr=ten['mrr_known'], mrr10=ten['mrr_at_k_known'], burden10=ten['paragraphs'], ranking=ranking)


def char_count(package):
    return len(json.dumps(package, ensure_ascii=False, sort_keys=True, separators=(',', ':')))


def select_holdout(train_ids, components, labels, model):
    candidates=[]
    for name in GRID:
        rows=[score_row(model.rank(components[t][0], WEIGHTS[name]), labels[t], list(model.lessons.values()))
              for t in train_ids]
        candidates.append(dict(candidate=name, weights=WEIGHTS[name],
            r10=st.mean(r['r10'] for r in rows), mrr=st.mean(r['mrr'] for r in rows)))
    winner = max(range(len(candidates)), key=lambda i: (candidates[i]['r10'], candidates[i]['mrr'], -i))
    return candidates[winner]['candidate'], candidates


def student_t_975(df):
    """Stdlib numerical Student-t quantile, Simpson integration + bisection.

    Used only for sample-size scenarios, never to replace bootstrap intervals.
    """
    coefficient = math.exp(math.lgamma((df+1)/2)-math.lgamma(df/2))/math.sqrt(df*math.pi)
    def cdf(x):
        steps=1024
        h=x/steps
        def density(t):
            return coefficient*(1+t*t/df)**(-(df+1)/2)
        return .5+h/3*(density(0)+density(x)+sum((4 if i%2 else 2)*density(i*h) for i in range(1,steps)))
    lo,hi=0.,20.
    for _ in range(36):
        mid=(lo+hi)/2
        if cdf(mid)<.975:lo=mid
        else:hi=mid
    return (lo+hi)/2


def run(iterations=ITERATIONS):
    start = time.perf_counter()
    data = evaluer.validate_snapshot(evaluer.read_json(HERE/'korpus_44.json'))
    truth = evaluer.read_json(HERE/'retrospektiv_fasit.json')
    assert truth['snapshotHash'] == data['snapshotHash']
    labels = {t['taskRef']: {} for t in data['tasks']}
    for j in truth['judgments']:
        assert j['basis'] == 'source' and j['relevant'] is True
        labels[j['taskRef']][j['lessonRef']] = True
    assert labels == evaluer.truth_labels(data, 'source')
    declared = evaluer.read_json(PROFILES)
    assert declared['snapshotHash'] == data['snapshotHash']
    profiles={p['taskRef']: p for p in declared['profiles']}
    assert set(profiles) == set(labels)
    assert all(2 <= len(p['activePurposes']) <= 5 for p in profiles.values())
    model = Experiment(data['lessons'], data['packages'], declared)
    components={t['taskRef']: model.components(t['query'], profiles[t['taskRef']]) for t in data['tasks']}
    positive_ids = [t for t, ls in labels.items() if ls]
    assert len(positive_ids) == 4 and sum(map(len, labels.values())) == 15
    folds={}
    for ref in labels:
        training = [t for t in positive_ids if t != ref]
        chosen, scores = select_holdout(training, components, labels, model)
        assert ref not in training
        folds[ref]=dict(trainingTaskRefs=training, selected=chosen, weights=WEIGHTS[chosen], grid=scores)
    rows={name: {} for name in [*WEIGHTS, '6_holdout']}
    packages={name: {} for name in rows}
    checks=[]
    for task in data['tasks']:
        ref=task['taskRef']; profile=profiles[ref]; cs, es=components[ref]
        baseline=evaluer.run_matcher(evaluer.tfidf_matcher, data, task)
        assert model.rank(cs, WEIGHTS['1_tfidf']) == baseline
        for name in rows:
            weights=folds[ref]['weights'] if name == '6_holdout' else WEIGHTS[name]
            ranking=evaluer.run_matcher(model.adapter(profile, weights), data, task)
            assert len(ranking) == len(set(ranking)) == 44
            assert ranking[:K] == model.rank(cs, weights, K)
            rows[name][ref]=score_row(ranking, labels[ref], data['lessons'])
            pack=model.package(task['query'], profile, weights, ranking, cs, es)
            # Whole-tree reference is deliberately lean, without judgment/source fields.
            full=dict(schema=pack['schema'], query=task['query'], weights=list(weights),
                      purposeTree=list(model.lex.purposes.values()), nodes=list(model.lessons.values()))
            compact, whole=char_count(pack), char_count(full)
            lean_full=dict(full, purposeTree=[{k:v for k,v in node.items() if k in
                ('purposeRef','parentRef','title','summary','matchingHints','interests')}
                for node in model.lex.purposes.values()])
            book57={n['purposeRef'] for n in evaluer.read_json(PURPOSE_PATH)['nodes']}
            full57=dict(full, purposeTree=[n for n in model.lex.purposes.values() if n['purposeRef'] in book57])
            packages[name][ref]=dict(chars=compact, roughTokens=compact/4, fullChars=whole,
                fullRoughTokens=whole/4, ratio=compact/whole,
                recallKnown=rows[name][ref]['r10'], packageHash=evaluer.digest(pack),
                leanFullChars=char_count(lean_full), leanRatio=compact/char_count(lean_full),
                book57FullChars=char_count(full57), book57Ratio=compact/char_count(full57),
                nodeRefs=ranking[:K], package=pack)
    summaries={name: stats_for_rows(rs, iterations) for name, rs in rows.items()}
    pairs=[]
    for a,b in itertools.combinations(rows,2):
        for metric in ('p5','r10','mrr'):
            ds=[rows[b][t][metric]-rows[a][t][metric] for t in labels if rows[a][t][metric] is not None]
            pairs.append(dict(a=a,b=b,metric=metric,**evaluer.paired_stats(ds,iterations,SEED)))
    for pair in pairs:
        pair['pBonferroni']=min(1.,len(pairs)*pair['p'])
    # Constructed ownership truth: all source lessons of the context owner are
    # positive, all other lessons negative ONLY here. No derived labels enter fit.
    amb_rows={name:{} for name in rows}
    amb_cases=[]
    for qidx,query in enumerate(SHORT_QUERIES):
        for ref in positive_ids:
            profile=profiles[ref];cs,es=model.components(query,profile)
            target={r:r in labels[ref] for r in model.lessons}
            case=f'q{qidx+1:02}:{ref}'
            amb_cases.append(dict(case=case,query=query,contextOwner=ref,positives=sorted(labels[ref]),constructed=True))
            for name in rows:
                weights=folds[ref]['weights'] if name=='6_holdout' else WEIGHTS[name]
                ranking=model.rank(cs,weights)
                assert name!='1_tfidf' or ranking==evaluer.tfidf_matcher(query,data['lessons'],{})
                amb_rows[name][case]=score_row(ranking,target,data['lessons'])
    # Resample four owners (clusters), not 48 correlated cases as independent tasks.
    amb_cluster={name:{ref:{m:st.mean(r[m] for c,r in rs.items() if c.endswith(':'+ref))
        for m in ('p5','p5Upper','r10','mrr','mrr10','burden10')} for ref in positive_ids}
        for name,rs in amb_rows.items()}
    amb_summary={name:stats_for_rows(rs,iterations) for name,rs in amb_cluster.items()}
    amb_pairs=[]
    for name in list(rows)[1:]:
        ds=[amb_cluster[name][t]['r10']-amb_cluster['1_tfidf'][t]['r10'] for t in positive_ids]
        amb_pairs.append(dict(a='1_tfidf',b=name,metric='r10',**evaluer.paired_stats(ds,iterations,SEED)))
    for pair in amb_pairs:
        pair['pBonferroni']=min(1.,len(amb_pairs)*pair['p'])
    # Same-word control: short-query baseline must be identical across contexts.
    for qidx in range(len(SHORT_QUERIES)):
        ranks=[r['ranking'] for c,r in amb_rows['1_tfidf'].items() if c.startswith(f'q{qidx+1:02}:')]
        assert all(r == ranks[0] for r in ranks)
    amb_swaps=[]
    for ref in positive_ids:
        for other in positive_ids:
            if ref == other: continue
            values=[]
            for query in SHORT_QUERIES:
                cs,_=model.components(query,profiles[other])
                ranking=model.rank(cs,WEIGHTS['6_tekst_perspektiv_skop'])
                values.append(score_row(ranking,labels[ref],data['lessons'])['r10'])
            amb_swaps.append(dict(target=ref,wrongContext=other,r10=st.mean(values)))
    token_summary={name:dict(meanChars=st.mean(r['chars'] for r in packs.values()),
        meanRoughTokens=st.mean(r['roughTokens'] for r in packs.values()),
        meanFullChars=st.mean(r['fullChars'] for r in packs.values()),
        meanFullRoughTokens=st.mean(r['fullRoughTokens'] for r in packs.values()),
        meanRatio=st.mean(r['ratio'] for r in packs.values()),
        minRatio=min(r['ratio'] for r in packs.values()),maxRatio=max(r['ratio'] for r in packs.values()),
        meanLeanFullChars=st.mean(r['leanFullChars'] for r in packs.values()),
        meanLeanRatio=st.mean(r['leanRatio'] for r in packs.values()),
        meanBook57FullChars=st.mean(r['book57FullChars'] for r in packs.values()),
        meanBook57Ratio=st.mean(r['book57Ratio'] for r in packs.values()),
        r10=summaries[name]['r10']) for name,packs in packages.items()}
    # Counterfactual planning at delta=.15; these are scenarios, not CI guarantees.
    ds=[rows['6_tekst_perspektiv_skop'][t]['r10']-rows['1_tfidf'][t]['r10'] for t in positive_ids]
    z=st.NormalDist().inv_cdf(.975); z80=st.NormalDist().inv_cdf(.8)
    planning=[]
    t975={}
    for label,sd in [('scenario',.1),('scenario',.2),('scenario',.3),('scenario',.5),('observed_n4',st.stdev(ds))]:
        if sd == 0:
            planning.append(dict(basis=label,sd=sd,delta=.15,n_ci_normal=None,n_ci_student_t=None,n_power80=None,
                limitation='Fire identiske R+-forskjeller gir ingen informativ varians for planlegging; n er ukjent.'))
            continue
        n_t=2
        while True:
            if n_t-1 not in t975:t975[n_t-1]=student_t_975(n_t-1)
            if t975[n_t-1]*sd/math.sqrt(n_t) < .15:break
            n_t+=1
        planning.append(dict(basis=label,sd=sd,delta=.15,
            n_ci_normal=math.floor((z*sd/.15)**2)+1,n_ci_student_t=n_t,
            n_power80=math.ceil(((z+z80)*sd/.15)**2)))
    # Warm, 30 batches of 19 queries. Index/context built once, query uncached.
    benchmarks={}
    for name,weights in WEIGHTS.items():
        benchmarks[name]=timer(lambda w=weights:[model.rank(model.components(t['query'],profiles[t['taskRef']])[0],w,K)
                                                for t in data['tasks']],30)
    benchmarks['6_holdout']=timer(lambda:[model.rank(model.components(t['query'],profiles[t['taskRef']])[0],folds[t['taskRef']]['weights'],K) for t in data['tasks']],30)
    per_query=[timer(lambda t=t:model.rank(model.components(t['query'],profiles[t['taskRef']])[0],WEIGHTS['6_tekst_perspektiv_skop'],K),30)
               for t in data['tasks']]
    fullpack=timer(lambda:[char_count(model.package(t['query'],profiles[t['taskRef']],WEIGHTS['6_tekst_perspektiv_skop'],
        model.rank(cs,WEIGHTS['6_tekst_perspektiv_skop'],K),cs,es))
        for t in data['tasks'] for cs,es in [model.components(t['query'],profiles[t['taskRef']])]],30)
    # Prior candidates are retained verbatim, not rerun under new conditions.
    prior=evaluer.read_json(HERE/'graf_resultater.json')
    assert prior['snapshotHash']==data['snapshotHash']
    for filename,digest in prior['hashes'].items():
        path=PURPOSE_PATH if filename==PURPOSE_PATH.name else HERE/filename
        assert sha(path)==digest, 'Tidligere sammenligningsgrunnlag endret: '+filename
    assert prior['summaries']['tfidf']==dict(summaries['1_tfidf'],
        burdenAll=prior['summaries']['tfidf']['burdenAll'],
        jaccard10=prior['summaries']['tfidf']['jaccard10'],common10=prior['summaries']['tfidf']['common10'])
    # Independent adapter/score invariant already uses the unchanged run_matcher.
    checks=['19/19 TF-IDF rankings exactly equal unchanged evaluator',
            'same source labels/hash, 19 tasks, 44 lessons, 15 positive pairs, n+=4',
            'all candidates unique in-corpus full ranks and identical top-k truncation',
            'every held-out task excluded from all weight fitting',
            'short-query baseline identical across all context owners',
            'constructed negatives not added to original truth',
            'only declared semantic fields enter context scoring; no source or taskRef']
    output=dict(schema='haven.perspective-scope-experiment.v1',seed=SEED,iterations=iterations,k=K,
        snapshotHash=data['snapshotHash'],labelsHash=evaluer.digest(labels),
        counts=dict(tasks=19,lessons=44,positiveTasks=4,positivePairs=15,purposes=len(model.lex.purposes),
                    simulatedProfiles=19,unknownPurposeProfiles=sum(p['missingSection1Purposes'] for p in profiles.values())),
        weights=WEIGHTS,holdout=folds,rows=rows,summaries=summaries,comparisons=pairs,
        previousCandidates=dict(source=rel(HERE/'graf_resultater.json'),sha256=sha(HERE/'graf_resultater.json'),
            snapshotAndCodeHashesVerified=True,summaries=prior['summaries']),
        ambiguity=dict(constructed=True,uniqueQueries=12,cases=amb_cases,rows=amb_rows,
                       clusterUnit='context owner task',nClusters=4,summaries=amb_summary,comparisons=amb_pairs,
                       wrongContext=amb_swaps,wrongContextMeanR10=st.mean(r['r10'] for r in amb_swaps)),
        tokens=dict(method='Unicode characters in compact sorted JSON / 4, no tokenizer/model; not billing tokens',
                    denominator='70 Book+package purpose nodes with full metadata + 44 clean lesson nodes + same query/weights; no original judgment/source metadata',
                    summaries=token_summary,perTask=packages),planning=planning,
        benchmark=dict(platform=platform.platform(),python=platform.python_version(),method='perf_counter; warm 30 batches x 19, context/index built once; query scoring not cached',
            servingBatch=benchmarks,candidate6PerQuery=per_query,candidate6PackBatch=fullpack),
        scopeNodeRefs={ref:[n['ref'] for n in ns] for ref,ns in model.scope_nodes.items()},checks=checks,
        hashes={rel(p):sha(p) for p in [Path(__file__),PROFILES,HERE/'evaluer.py',HERE/'laer_vekter.py',HERE/'leksikon.py',
           HERE/'spredning.py',HERE/'spike_tfidf_baseline.py',HERE/'korpus_44.json',HERE/'retrospektiv_fasit.json',PURPOSE_PATH]},
        elapsedSeconds=time.perf_counter()-start)
    evaluer.write_json(RESULT,output)
    write_judgment_sheet(data,labels,profiles,output)
    return output


def write_judgment_sheet(data,labels,profiles,result):
    path=HERE/'DOMMER_ventende.md'
    if path.exists() and '<!-- GENERATED; no judgments entered -->' not in path.read_text():
        raise ValueError('DOMMER-filen kan ha menneskesvar; vil ikke overskrive')
    lines=['<!-- GENERATED; no judgments entered -->','# Ventende dommer: 15 oppgaver',
        '', 'Dette er en tom arbeidsblankett, ikke fasit. Fjern GENERATED-kommentaren før du skriver svar, slik at ny målekjøring ikke overskriver dem.',
        'Kandidat 6 = tekst/perspektiv/skop (0,50/0,25/0,25); kandidat 1 = uendret TF-IDF. K=10, frosset 44-korpus.',
        'Samme lærdom har samme nummer i begge kolonner. Unionen kan ha opptil 20 rader. Kolonnene er synlige etter bestilling; dette er ikke blind merking.',
        '', 'Et treff: ville forebyggingen endret et konkret valg, en test eller en avgrensning i oppgaven? Generelt gode råd er ikke nok.',
        'Etter vanlig G1-lesing: svar 1) `1 3 ?4` (1,3 relevant; 4 uvurdert; resten i unionen irrelevant), eller `-` for ingen relevante. '
        '2) `3=lesson.tidligere`, eller `-` når du ikke identifiserer gjentakelse. '
        '3) `1=test.ref 3=u:sann-grunn`, eller `u:sann-grunn` for alle relevante. Ingen standardgrunn fylles inn. '
        'Lærdommer utenfor unionen er alltid uvurderte.',
        'Oppgi `sekunder=…`; mål median <60 sekunder på første fem etter G1-lesingen, også andel uvurderte. Tidsmålet er ikke mennesketestet.',
        'Å lese alt fra bunnen av er ikke lovet å ta under ett minutt. Utvid «Full tekst» ved behov (tilsvarer `v n` i judge). '
        'Svarene må valideres mot samme snapshot før import til purpose_dev.py judge-format; denne filen skriver ingen dom automatisk. '
        'Topp-10-pool gir dekning av poolens positive; ekte total R krever vurdering av alle 44 eller separat revisjonsutvalg.',
        'Korpus: `'+rel(HERE/'korpus_44.json')+'`; snapshotHash: `'+data['snapshotHash']+'`.', '']
    lines += ['For en absolutt R+@10-forskjell på 0,15: ved antatt paret s_d=0,30 er normalanslaget 16 og t-intervallanslaget 18 vurderte, uavhengige oppgaver; planlegging med 80 % styrke gir 32 nye oppgaver. Ved s_d=0,50 gir det henholdsvis 43, 46 og 88. Ingen garanti for bootstrap-CI. De 15 nedenfor utvider utviklingsgrunnlaget; de er ikke 15 uavhengige bekreftende tester. Dagens fire source-oppgaver erstatter ikke menneskedommer.', '']
    lessons={l['lessonRef']:l for l in data['lessons']}
    for task in data['tasks']:
        ref=task['taskRef']
        if labels[ref]: continue
        a=result['rows']['6_tekst_perspektiv_skop'][ref]['ranking'][:10]
        b=result['rows']['1_tfidf'][ref]['ranking'][:10]
        union=list(dict.fromkeys(a+b)); nums={r:i for i,r in enumerate(union,1)}
        goals='; '.join(p['title'] for p in profiles[ref]['activePurposes'])
        lines += ['## '+ref,'', '**Simulert perspektiv:** '+goals+'. **Skop:** '+profiles[ref]['scope']['ref']+'.',
                  'Oppgave: `CellProtocolDocuments/Deliverables/'+ref+'/FORMAALSSPEC.md` (§0/§1).',
                  '', '| Rang | Kandidat 6 | Kandidat 1 — TF-IDF |','|---:|---|---|']
        def cell(r):
            return f"**{nums[r]}** `{r}` — "+clean_text(lessons[r]['prevention']).replace('|','\\|')[:140]+('…' if len(clean_text(lessons[r]['prevention']))>140 else '')
        for i,(ra,rb) in enumerate(zip(a,b),1):lines.append(f'| {i} | {cell(ra)} | {cell(rb)} |')
        tests=sorted({x['testRef'] for p in data['packages']['packages'] for n in p['purposes'] for x in n.get('derivedTests',[])})
        tests=sorted(set(tests)|set(re.findall(r'\btest\.[a-zA-Z0-9_.-]+',task['section5'])))
        lines += ['',f'Union: {len(union)} lærdommer; øvrige {44-len(union)} uvurderte.',
                  '- Relevans: ', '- Gjentakelser: ', '- Håndhevelse / sann grunn: ', '- Sekunder: ', '',
                  '<details><summary>Full tekst og testreferanser</summary>','']
        for r in union:
            l=lessons[r]
            lines += [f"**{nums[r]} — {r}**", '', 'Symptom: '+l['symptom'], '', 'Forebygging: '+l['prevention'], '']
        lines += ['Kjente testrefs (eksistens i snapshot er ikke bevis for at testen er kjørt): '+', '.join('`'+x+'`' for x in tests),
                  '', '</details>', '']
    path.write_text('\n'.join(lines)+'\n')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--init-profiles',action='store_true')
    ap.add_argument('--iterations',type=int,default=ITERATIONS)
    args=ap.parse_args()
    if args.init_profiles:
        init_profiles(evaluer.validate_snapshot(evaluer.read_json(HERE/'korpus_44.json')))
        print('Created',rel(PROFILES));return
    output=run(args.iterations)
    for name,s in output['summaries'].items():
        print(name,*(f'{m}={s[m]["mean"]:.4f}' for m in ('p5','r10','mrr')))
    print('Result',rel(RESULT),'elapsedSeconds',round(output['elapsedSeconds'],2))


if __name__=='__main__':
    main()
