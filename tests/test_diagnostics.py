import json
from pathlib import Path
import unittest
import numpy as np
import sympy as sp
from corrlaw.oracle import make_trial,reference
from corrlaw.diagnostics import exhaustive_fit,prior_library,prior_fit,prior_augment
from corrlaw.discovery import admissible,model_errors

ROOT=Path(__file__).resolve().parents[1]


class DiagnosticTests(unittest.TestCase):
    def config(self):
        return json.loads((ROOT/'configs/smoke.json').read_text())

    def test_origin_only_does_not_eliminate_cubic_circle_alias(self):
        u,v=sp.symbols('u v')
        q=u*(u*u+v*v-1)
        self.assertEqual(q.subs({u:0,v:0}),0)
        self.assertEqual(sp.rem(q,u*u+v*v-1,u),0)
        self.assertNotEqual(sp.expand(q.subs(u,-u)-q),0)

    def test_prior_restricts_entire_shared_dictionary(self):
        trial=make_trial('B',301,0,0,'constrained',self.config());obs=trial.observations([])
        no=prior_library(obs,'none');origin=prior_library(obs,'zero_origin');even=prior_library(obs,'zero_origin_and_even')
        self.assertEqual(len(no.powers),10);self.assertEqual(len(origin.powers),9)
        self.assertNotIn((0,0),origin.powers)
        self.assertEqual(set(even.powers),{(2,0),(0,2)})
        fitted=prior_fit(obs,12,'zero_origin_and_even')
        np.testing.assert_allclose(fitted.library.transform(trial.pool)@fitted.best,reference('B',trial.pool),atol=1e-12)
        _,ws,state=prior_augment(obs,fitted)
        self.assertEqual(ws,[]);self.assertEqual(state,'no_witness_within_search_budget')
        # Diversity remains well-defined when a strong prior leaves fewer than7 columns.
        other=prior_fit(obs,13,'zero_origin_and_even',True)
        self.assertEqual(other.library.powers,fitted.library.powers)

    def test_origin_only_allows_valid_odd_witnesses(self):
        trial=make_trial('B',301,0,0,'constrained',self.config());obs=trial.observations([])
        fitted=prior_fit(obs,12,'zero_origin')
        _,ws,_=prior_augment(obs,fitted)
        self.assertTrue(ws)
        origin=fitted.library.transform(np.zeros((1,2)))
        for witness in ws:
            for name in ('base','alternative'):
                coeff=np.asarray(witness[name]);self.assertEqual(float((origin@coeff)[0]),0.)
                matrices=[fitted.library.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
                self.assertTrue(admissible(coeff,model_errors(coeff,matrices,obs),0))

    def test_prior_active_loop_replays_and_counts_every_label(self):
        from corrlaw.prior_experiment import run_policy
        from corrlaw.experiment import scientific_content
        c=self.config();c['tasks']=['B']
        trial=make_trial('B',301,.01,.01,'constrained',c)
        first=run_policy(trial,'augmented_qbc',c,'zero_origin_and_even')
        second=run_policy(trial,'augmented_qbc',c,'zero_origin_and_even')
        self.assertEqual(scientific_content(first),scientific_content(second))
        self.assertEqual(len({r['query_id'] for r in first['queries']}),8)
        self.assertEqual(first['metrics'][-1]['total_labels'],200)
        for model in first['models']:
            self.assertEqual(set(map(tuple,model['powers'])),{(2,0),(0,2)})
            self.assertEqual(model['witnesses'],[])

    def test_exhaustive_search_on_anonymous_intervened_observations(self):
        c=self.config();c['stage']='confirmation'
        trial=make_trial('E',92001,0,0,'constrained',c)
        oracle=trial.oracle()
        # Choose numerical off-preparation extremes; this fixture does not give a
        # formula or task ID to the exhaustive fitting function.
        for index in [int(np.argmax(trial.pool[:,1]-trial.pool[:,0])),int(np.argmin(trial.pool[:,1]-trial.pool[:,0]))]:
            oracle.measure(index)
        fitted,count=exhaustive_fit(trial.observations(oracle.records))
        self.assertEqual(count,833)
        self.assertLessEqual(np.count_nonzero(fitted.best),3)
        np.testing.assert_allclose(fitted.library.transform(trial.test_x)@fitted.best,
                                   reference('E',trial.test_x),atol=1e-9)


if __name__=='__main__':unittest.main()
