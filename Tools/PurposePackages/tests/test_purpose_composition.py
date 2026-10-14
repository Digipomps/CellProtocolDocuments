"""Book 36 §§4–5: positive/negative paths plus temporal and CLI regressions."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from purpose_composition import Composition
import purpose_dev

ROOT, A, B, INV, COND = ['purpose://' + x for x in ('test', 'test.a', 'test.b', 'test.inv', 'test.condition')]


def when(second):
    return f'2026-09-09T10:00:{second:02d}+00:00'


def tree(kind='allOf', **fields):
    nodes = [dict(purposeRef=ROOT, parentRef=None, composition=dict(kind=kind, **fields)),
             dict(purposeRef=A, parentRef=ROOT), dict(purposeRef=B, parentRef=ROOT)]
    if kind in ('sequence', 'firstOf'):
        nodes[0]['childOrder'] = [A, B]
    return nodes


def attempt(ref, start, end=None, aid=None):
    result = dict(purposeRef=ref, attemptRef=aid or ref + '/attempt', attemptedAt=when(start))
    if end is not None:
        result['finishedAt'] = when(end)
    return result


def measure(ref, state='green', second=10, **extra):
    result = dict(purposeRef=ref, state=state, measuredAt=when(second), evidenceRef='TESTRESULT.md#actual-output', **extra)
    if state == 'blocked':
        result['reason'] = 'dependency unavailable'
    return result


def report(ref=ROOT, state='green', second=50, **extra):
    return dict(purposeRef=ref, state=state, reportedAt=when(second), **extra)


def run(kind='allOf', states=('green', 'green'), **fields):
    nodes = tree(kind, **fields)
    log = dict(attempts=[attempt(A, 1, 4), attempt(B, 11, 14)],
               measurements=[measure(A, states[0], 5), measure(B, states[1], 15)], reports=[])
    if kind == 'firstOf':
        log['reports'] = [report(branchRef=B)]
    return nodes, log


def invariant_run():
    nodes, log = run()
    nodes.extend([dict(purposeRef=INV, parentRef=ROOT, composition=dict(kind='invariant', over=ROOT)),
                  dict(purposeRef=COND, parentRef=INV)])
    for second, phase, ref in [(0, 'before', A), (6, 'after', A), (10, 'before', B), (16, 'after', B)]:
        log['measurements'].append(measure(COND, second=second, phase=phase, attemptRef=ref + '/attempt'))
    return nodes, log


class ValidationRules(unittest.TestCase):
    def assertValid(self, nodes, log=None):
        self.assertEqual(Composition(nodes, log).validate()[0], [])

    def assertInvalid(self, nodes, log=None, rule=None):
        errors = Composition(nodes, log).validate()[0]
        self.assertTrue(errors)
        if rule:
            self.assertIn(f'regel {rule}', '\n'.join(errors))

    def test_rule_1_non_leaf_requires_composition_warning_during_migration(self):
        nodes = tree()
        self.assertEqual(Composition(nodes).validate(), ([], []))
        del nodes[0]['composition']
        engine = Composition(nodes)
        self.assertEqual(engine.validate()[0], [])
        self.assertEqual(engine.missing_composition, [ROOT])
        self.assertIn('regel 1', engine.validate()[1][0])
        self.assertEqual(engine.evaluate(ROOT)['state'], 'unverified')
        self.assertInvalid(nodes, {'measurements': [measure(A), measure(B)], 'reports': [report()]}, 6)

    def test_rule_2_sequence_order_unambiguous(self):
        nodes = tree('sequence')
        self.assertValid(nodes)
        for order in (None, [], [A], [A, A], [A, B, ROOT], [A, {}]):
            with self.subTest(order=order):
                bad = copy.deepcopy(nodes)
                bad[0]['childOrder'] = order
                self.assertInvalid(bad, rule=2)
        nodes.append(copy.deepcopy(nodes[1]))
        self.assertInvalid(nodes, rule=2)

    def test_rule_3_anyof_threshold(self):
        for minimum in (1, 2):
            self.assertValid(tree('anyOf', min=minimum))
        self.assertValid(tree('anyOf'))
        for minimum in (3, 0, -1, True, 1.5, '1', None):
            with self.subTest(minimum=minimum):
                self.assertInvalid(tree('anyOf', min=minimum), rule=3)

    def test_rule_4_green_firstof_requires_registered_branch(self):
        nodes, log = run('firstOf', ('red', 'green'))
        self.assertValid(nodes, log)
        del log['reports'][0]['branchRef']
        self.assertInvalid(nodes, log, 4)

    def test_rule_5_invariant_requires_over_inside_same_tree(self):
        nodes, log = invariant_run()
        self.assertValid(nodes, log)
        for target in (None, 'purpose://missing', INV, A):
            with self.subTest(target=target):
                bad = copy.deepcopy(nodes)
                bad[3]['composition']['over'] = target
                self.assertInvalid(bad, log, 5)
        bad = copy.deepcopy(nodes)
        del bad[3]['composition']['over']
        self.assertInvalid(bad, log, 5)
        nodes += [dict(purposeRef='purpose://other', parentRef=None, composition={'kind': 'allOf'}),
                  dict(purposeRef='purpose://other.child', parentRef='purpose://other')]
        nodes[3]['composition']['over'] = 'purpose://other'
        self.assertInvalid(nodes, log, 5)

    def test_rule_6_green_report_must_follow_table_for_every_kind(self):
        for kind in ('allOf', 'sequence', 'anyOf', 'firstOf', 'invariant'):
            with self.subTest(kind=kind):
                nodes, log = invariant_run() if kind == 'invariant' else run(kind, ('red', 'green') if kind == 'firstOf' else ('green', 'green'))
                ref = INV if kind == 'invariant' else ROOT
                if kind != 'firstOf':
                    log['reports'] = [report(ref)]
                self.assertValid(nodes, log)
                if kind == 'invariant':
                    log['measurements'][2]['state'] = 'red'
                else:
                    for measurement in log['measurements']:
                        measurement['state'] = 'red'
                self.assertInvalid(nodes, log, 6)


class GateTable(unittest.TestCase):
    def assertState(self, nodes, log, expected, ref=ROOT):
        engine = Composition(nodes, log)
        self.assertEqual(engine.errors, [])
        self.assertEqual(engine.evaluate(ref)['state'], expected, engine.evaluate(ref))

    def test_allof_green_and_red(self):
        for states, expected in [(('green', 'green'), 'green'), (('green', 'red'), 'red')]:
            self.assertState(*run(states=states), expected)

    def test_sequence_green_and_red_at_attempt_time(self):
        nodes, log = run('sequence')
        self.assertState(nodes, log, 'green')
        # Both children are green now, but B was attempted while A was unverified.
        log['attempts'][1]['attemptedAt'] = when(2)
        self.assertState(nodes, log, 'red')
        self.assertState(nodes, log, 'red', B)
        log['reports'] = [report(B)]
        self.assertIn('regel 6', '\n'.join(Composition(nodes, log).validate()[0]))

    def test_anyof_green_and_red(self):
        self.assertState(*run('anyOf', ('red', 'green')), 'green')
        self.assertState(*run('anyOf', ('red', 'red')), 'red')
        self.assertState(*run('anyOf', ('red', 'green'), min=2), 'red')
        self.assertState(*run('anyOf', min=2), 'green')

    def test_firstof_green_and_red(self):
        nodes, log = run('firstOf', ('red', 'green'))
        self.assertState(nodes, log, 'green')
        self.assertEqual(Composition(nodes, log).evaluate(ROOT)['branchRef'], B)
        log['measurements'][1]['state'] = 'red'
        self.assertState(nodes, log, 'red')
        log['reports'] = []
        self.assertState(nodes, log, 'unverified')

    def test_invariant_green_and_red(self):
        nodes, log = invariant_run()
        self.assertState(nodes, log, 'green', INV)
        log['measurements'][2]['state'] = 'red'
        self.assertState(nodes, log, 'red', INV)
        self.assertIn('steg startet etter bruddet', Composition(nodes, log).evaluate(INV)['reason'])

    def test_blocked_is_preserved_for_every_kind_even_if_quorum_met(self):
        for kind in ('allOf', 'sequence', 'anyOf', 'firstOf', 'invariant'):
            with self.subTest(kind=kind):
                nodes, log = invariant_run() if kind == 'invariant' else run(kind, ('red', 'green') if kind == 'firstOf' else ('green', 'green'))
                if kind == 'invariant':
                    log['measurements'][2].update(state='blocked', reason='dependency unavailable')
                else:
                    log['measurements'][1].update(state='blocked', reason='dependency unavailable')
                ref = INV if kind == 'invariant' else ROOT
                self.assertState(nodes, log, 'blocked', ref)
                self.assertIn('dependency unavailable', Composition(nodes, log).evaluate(ref)['reason'])

    def test_sequence_revocation_equal_timestamp_missing_attempt_and_retry(self):
        for mutation, expected in [
            (lambda log: log['measurements'].append(measure(A, 'red', 8)), 'red'),
            (lambda log: log['attempts'][1].update(attemptedAt=when(5)), 'red'),
            (lambda log: log['attempts'].pop(), 'unverified'),
            (lambda log: log['attempts'].insert(1, attempt(B, 2, 3, 'early')), 'red'),
        ]:
            nodes, log = run('sequence')
            mutation(log)
            self.assertState(nodes, log, expected)

    def test_blocked_is_not_hidden_by_an_invalid_sequence_attempt(self):
        nodes, log = run('sequence', ('green', 'blocked'))
        log['attempts'][1]['attemptedAt'] = when(2)
        self.assertState(nodes, log, 'blocked', B)
        self.assertState(nodes, log, 'blocked')

    def test_nested_sequence_checks_historical_composed_predecessor(self):
        nodes, log = run('sequence')
        nodes[1]['composition'] = {'kind': 'allOf'}
        nested = 'purpose://test.a.nested'
        nodes.append(dict(purposeRef=nested, parentRef=A))
        log['measurements'][0]['purposeRef'] = nested
        self.assertState(nodes, log, 'green')
        log['measurements'][0]['measuredAt'] = when(12)
        self.assertState(nodes, log, 'red')

    def test_firstof_preference_order_stop_and_unknown_branch(self):
        nodes, log = run('firstOf', ('red', 'green'))
        log['attempts'][1]['attemptedAt'] = when(2)
        self.assertState(nodes, log, 'red')
        nodes, log = run('firstOf')
        self.assertState(nodes, log, 'red')  # Selected B although A is green.
        log['reports'][0]['branchRef'] = A
        self.assertState(nodes, log, 'red')  # B was attempted after success on A.
        log['attempts'].pop()
        log['measurements'].pop()
        self.assertState(nodes, log, 'green')
        log['reports'][0]['branchRef'] = ROOT
        self.assertTrue(Composition(nodes, log).errors)

    def test_firstof_cannot_resume_after_revoked_success(self):
        nodes, log = run('firstOf', ('green', 'green'))
        log['measurements'].append(measure(A, 'red', 8))
        self.assertState(nodes, log, 'red')

    def test_invariant_missing_or_misordered_measurements_and_unfinished_step(self):
        for mutate, expected in [
            (lambda log: log['measurements'].pop(), 'unverified'),
            (lambda log: log['measurements'][2].update(measuredAt=when(2)), 'red'),
            (lambda log: log['measurements'][3].update(measuredAt=when(12)), 'red'),
            (lambda log: log['measurements'][4].update(measuredAt=when(3)), 'red'),
            (lambda log: log['attempts'][1].pop('finishedAt'), 'unverified'),
            (lambda log: log['measurements'].append(measure(COND, 'red', 13)), 'red'),
        ]:
            nodes, log = invariant_run()
            mutate(log)
            self.assertState(nodes, log, expected, INV)

    def test_invariant_failure_cannot_be_bypassed_by_anyof_quorum(self):
        nodes, log = invariant_run()
        nodes[0]['composition'] = {'kind': 'anyOf'}
        self.assertState(nodes, log, 'green')
        log['measurements'][2]['state'] = 'red'
        self.assertState(nodes, log, 'red')

        # Move the invariant into a sibling branch; over still constrains ROOT.
        outer = 'purpose://outer'
        nodes.append(dict(purposeRef=outer, parentRef=None, composition={'kind': 'allOf'}))
        nodes[0]['parentRef'] = outer
        nodes[3]['parentRef'] = outer
        self.assertState(nodes, log, 'red')

    def test_invariant_over_firstof_checks_only_executed_alternatives(self):
        nodes, log = invariant_run()
        outer = 'purpose://outer'
        nodes.append(dict(purposeRef=outer, parentRef=None, composition={'kind': 'allOf'}))
        nodes[0].update(parentRef=outer, composition={'kind': 'firstOf'}, childOrder=[A, B])
        nodes[3]['parentRef'] = outer
        log['attempts'] = log['attempts'][:1]
        log['measurements'] = [m for m in log['measurements'] if m['purposeRef'] != B and m.get('attemptRef') != B + '/attempt']
        log['reports'] = [report(branchRef=A)]
        self.assertState(nodes, log, 'green', INV)
        self.assertState(nodes, log, 'green')
        log['measurements'].append(measure(B))
        self.assertState(nodes, log, 'unverified', INV)

    def test_measurements_cannot_be_replaced_by_opinions_or_green_reports(self):
        nodes, log = run()
        log['measurements'] = []
        log['reports'] = [report(), report(A), report(B)]
        log['opinions'] = [dict(purposeRef=ROOT, text='Everything should be fine')]
        self.assertState(nodes, log, 'unverified')
        self.assertTrue(Composition(nodes, log).validate()[0])
        log['measurements'] = [dict(purposeRef=A, measuredAt=when(5), state='green', evidenceRef='x', opinion='fine')]
        self.assertTrue(Composition(nodes, log).errors)

    def test_green_report_is_checked_at_report_time_not_using_future_evidence(self):
        nodes, log = run()
        log['reports'] = [report(second=12)]
        self.assertState(nodes, log, 'green')
        self.assertTrue(Composition(nodes, log).validate()[0])

    def test_malformed_input_is_rejected_without_traceback(self):
        cases = [(None, {}), (tree('invalid'), {}), (tree('sequence'), {'attempts': None}),
                 (tree(), {'measurements': [None]}), (tree(), {'measurements': [measure(A, second=3, extra='no')]}),
                 (tree(), {'measurements': [dict(purposeRef=A, state='green', measuredAt='2026-09-09', evidenceRef='x')]}),
                 (tree(), {'measurements': [measure(A, 'blocked', 3)]})]
        cases[-1][1]['measurements'][0].pop('reason')
        for nodes, log in cases:
            with self.subTest(nodes=nodes, log=log):
                engine = Composition(nodes, log)
                self.assertTrue(engine.validate()[0])
                self.assertEqual(engine.evaluate(ROOT)['state'], 'unverified')
        nodes = tree()
        nodes[0]['parentRef'] = B
        self.assertTrue(Composition(nodes).errors)


class CommandLineAndSchema(unittest.TestCase):
    def test_validate_repository_warning_count_and_preserved_canonical_nodes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = purpose_dev.validate()
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn('18 noder uten composition (18 Book 23-noder)', output.getvalue())
        kb = json.loads(Path(purpose_dev.KB_PATH).read_text())
        # Book 23 vokser (58 noder fra 2026-09); testen vokter at ingen kanonisk node forsvinner, ikke et fast antall.
        self.assertGreaterEqual(len(kb['nodes']), 57)
        self.assertFalse(any('composition' in n for n in kb['nodes']))

    def test_schema_references_resolve_and_composition_is_shared(self):
        book = TOOLS.parents[1] / 'Book'
        def walk(value, source):
            if isinstance(value, dict):
                if '$ref' in value:
                    file, _, fragment = value['$ref'].partition('#')
                    target = source.parent / file if file else source
                    resolved = json.loads(target.read_text())
                    for part in fragment.strip('/').split('/') if fragment else []:
                        resolved = resolved[part]
                for item in value.values():
                    walk(item, source)
            elif isinstance(value, list):
                for item in value:
                    walk(item, source)
        for source in book.glob('haven_purpose*.schema.json'):
            walk(json.loads(source.read_text()), source)
        shared = json.loads((book/'haven_purpose_composition_v0.schema.json').read_text())['$defs']
        self.assertEqual({s['properties']['kind']['const'] for s in shared['composition']['oneOf']},
                         {'allOf', 'sequence', 'anyOf', 'firstOf', 'invariant'})
        for filename in ('haven_purpose_knowledge_base_v0.json', 'haven_purpose_packages_v0.json'):
            document = json.loads((book/filename).read_text())
            self.assertTrue((book/document['schemaRef']).is_file())

    def test_gates_cli_all_states_and_validate_false_green(self):
        for state, code in [('green', 0), ('red', 1), ('blocked', 2), ('unverified', 3)]:
            with self.subTest(state=state), tempfile.TemporaryDirectory(prefix='purpose-composition-') as taskdir:
                nodes, log = run(states=('green', state))
                path = Path(taskdir) / purpose_dev.COMPOSITION_FILE
                path.write_text(json.dumps(dict(schema='haven.purpose-composition-run.v0', nodes=nodes, execution=log)))
                result = subprocess.run([sys.executable, str(TOOLS/'purpose_dev.py'), 'gates', taskdir], text=True, capture_output=True)
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertIn(f'Composition-port: {state}', result.stdout)
                self.assertNotIn('Traceback', result.stderr)
                log['reports'] = [report()]
                path.write_text(json.dumps(dict(nodes=nodes, execution=log)))
                checked = subprocess.run([sys.executable, str(TOOLS/'purpose_dev.py'), 'validate', taskdir], text=True, capture_output=True)
                self.assertEqual(checked.returncode, 0 if state == 'green' else 1, checked.stdout + checked.stderr)

    def test_missing_and_malformed_task_files_fail_closed(self):
        with tempfile.TemporaryDirectory() as taskdir:
            for content in (None, '{', '[]', '{"execution": []}', '{"nodes": 4}',
                            '{"nodes": [{"purposeRef": []}]}',
                            '{"execution": {"reports": [{"purposeRef": []}]}}'):
                path = Path(taskdir) / purpose_dev.COMPOSITION_FILE
                if content is not None:
                    path.write_text(content)
                result = subprocess.run([sys.executable, str(TOOLS/'purpose_dev.py'), 'gates', taskdir], text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)

    def test_gates_uses_root_composition_not_implicit_allof_over_descendants(self):
        for kind in ('anyOf', 'firstOf'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as taskdir:
                nodes, log = run(kind)
                nodes[2]['composition'] = {'kind': 'allOf'}
                nested = 'purpose://test.b.nested'
                nodes.append(dict(purposeRef=nested, parentRef=B))
                if kind == 'anyOf':
                    log['measurements'][1].update(purposeRef=nested, state='red')
                else:
                    log['attempts'].pop()
                    log['measurements'].pop()
                    log['reports'] = [report(branchRef=A)]
                (Path(taskdir)/purpose_dev.COMPOSITION_FILE).write_text(json.dumps(dict(nodes=nodes, execution=log)))
                result = subprocess.run([sys.executable, str(TOOLS/'purpose_dev.py'), 'gates', taskdir], text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('Composition-port: green', result.stdout)
                self.assertIn(B + (': red' if kind == 'anyOf' else ': unverified'), result.stdout)

    def test_composition_on_package_purpose_and_kb_node_reaches_cli(self):
        nodes, log = run('sequence')
        kb = {'nodes': [nodes[0], nodes[1]]}
        pk = {'packages': [dict(packageRef='test', triggers={'tags': ['*']}, purposes=[nodes[2]])], 'execution': log}
        engine, _ = purpose_dev.composition_context(kb, pk)
        self.assertEqual(engine.evaluate(ROOT)['state'], 'green')
        with tempfile.TemporaryDirectory() as taskdir, patch.object(purpose_dev, 'load_all', return_value=(kb, pk, {})):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(purpose_dev.gates(taskdir), 0)
            self.assertIn('Composition-port: green', output.getvalue())


if __name__ == '__main__':
    unittest.main()
