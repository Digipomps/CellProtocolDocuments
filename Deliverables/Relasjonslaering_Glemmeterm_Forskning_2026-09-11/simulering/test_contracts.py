#!/usr/bin/env python3
"""Research contract checks, not production feature tests."""
import math, unittest
from study import Engine, MODES, adaptation, canonical, fold, life, norm, pref, replay, soft, snap, traces, references
class ResearchContracts(unittest.TestCase):
    def test_measured_references(self):references()
    def test_normalizer_has_floating_ties_rank_on_raw(self):
        a=4.;b=math.nextafter(a,math.inf)
        self.assertLess(a,b);self.assertEqual(soft(a),soft(b))
    def test_lifecycle_duplicate_is_idempotent_all_candidates(self):
        event=life('one',1.,'succeeded',activeInterestRefs=['i'])
        for mode in MODES:
            en=Engine(mode);en.apply(event);before=canonical(en.snapshot());count=len(en.updates);en.apply(event)
            self.assertEqual(before,canonical(en.snapshot()));self.assertEqual(count,len(en.updates))
    def test_cutover_keeps_legacy_prefix(self):
        events=[life(str(i),float(i),'succeeded',activeInterestRefs=['a','b']) for i in range(6)]
        old=replay(events[:3]);cut=replay(events[:3],'hybrid_raw_02',cutover=3.)
        self.assertEqual(old.snapshot(),cut.snapshot())
        old=replay(events);cut=replay(events,'hybrid_raw_02',cutover=3.)
        self.assertNotEqual(old.snapshot(),cut.snapshot());self.assertEqual(cut.snapshot(),replay(events,'hybrid_raw_02',cutover=3.).snapshot())
    def test_absent_competitor_keeps_age(self):
        events=[pref('p',0.,'P','absent'),pref('q',0.,'P','present'),life('s',86400.,'succeeded',activeInterestRefs=['present'])]
        en=replay(events,'hybrid_raw_02');edge=en.edges[('P','purposeInterest','absent')]
        self.assertLess(edge['w'],.6);self.assertEqual(edge['last'],0.)
    def test_stable_switch_requires_ten_observations(self):
        self.assertIsNone(adaptation(['B']*9,'B',0)['stable']);self.assertEqual(adaptation(['B']*10,'B',0)['stable'],0)
    def test_eligibility_and_confidence_boundaries(self):
        s=snap(activeInterestRefs=['both'],passiveInterestRefs=['both','passive'],activeEntityRefs=['entity'],activeContextBlocks=[dict(domain='t',blockId='low',confidence=.59),dict(domain='t',blockId='edge',confidence=.6)])
        self.assertEqual(traces(s),{('purposeInterest','both'):1.,('purposeInterest','passive'):.3,('purposeEntity','entity'):1.,('purposeContextBlock','t:edge'):.3})
        en=Engine();en.apply(life('x',0.,'succeeded',**s,contextConfidence=.59));self.assertEqual(en.edges,{})
    def test_norm_one_does_not_bound_raw_at_one(self):
        w=[1/math.sqrt(6)]*6
        self.assertAlmostEqual(norm(w),1);self.assertGreater(fold(w),1)
if __name__=='__main__':unittest.main()
