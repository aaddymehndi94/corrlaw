import ast
import dataclasses
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import sympy as sp
from corrlaw.contracts import Observations
from corrlaw.oracle import bounds, reference, sample, make_trial, dimensional
from corrlaw.features import Library
from corrlaw.discovery import fit, admissible, model_errors
from corrlaw.witnesses import augment
from corrlaw.acquisition import leverage, disagreement, select, POLICIES
from corrlaw.evaluation import symbolic_recovery
from corrlaw.experiment import load_config, run_policy, scientific_content

ROOT = Path(__file__).resolve().parents[1]


class ScienceTests(unittest.TestCase):
    def config(self):
        return load_config(ROOT/'configs/smoke.json')

    def trial(self, task='A', width=0, noise=0, control='constrained'):
        return make_trial(task, 101, width, noise, control, self.config())

    def test_units_and_formulas(self):
        for task in 'ABCDEF':
            u,v = .8,1.1
            scales = (2.,2.) if task in 'BEF' else (2.,3.)
            value, scale = dimensional(task, u*scales[0], v*scales[1], scales)
            self.assertAlmostEqual(value/scale, reference(task,np.array([[u,v]]))[0])
        self.assertAlmostEqual(reference('D',np.array([[1.,1.]]))[0],1.)
        with self.assertRaises(ValueError): reference('C',np.array([[1.,0.]]))
        with self.assertRaises(ValueError): reference('B',np.array([[2.,0.]]))

    def test_support_constraints_and_fresh_labels(self):
        for task in 'ABCDEF':
            for width in (0,.01,.05):
                t=self.trial(task,width)
                self.assertTrue(np.all(t.fit_x >= bounds(task)[:,0]))
                self.assertTrue(np.all(t.fit_x <= bounds(task)[:,1]))
                np.testing.assert_array_equal(t.fit_y,reference(task,t.fit_x))
                u,v=t.fit_x.T
                delta=np.sqrt(u*u+v*v)-1 if task=='B' else v-(u*u if task=='E' else u)
                self.assertLessEqual(np.max(abs(delta)),width+1e-12)

    def test_shuffled_marginals_relabelled(self):
        for task in 'AB':
            x=sample(task,128,0,'constrained',np.random.default_rng(3))
            shuffled=sample(task,128,0,'matched_marginal_shuffle',np.random.default_rng(3))
            np.testing.assert_array_equal(x[:,0],shuffled[:,0])
            np.testing.assert_array_equal(np.sort(x[:,1]),np.sort(shuffled[:,1]))
            self.assertFalse(np.allclose(reference(task,x),reference(task,shuffled)))
            t=self.trial(task,control='matched_marginal_shuffle')
            np.testing.assert_array_equal(t.fit_y,reference(task,t.fit_x))

    def test_stream_separation_and_noise_pairing(self):
        t=self.trial(noise=.01); a=t.oracle(); b=t.oracle()
        self.assertEqual(a.measure(2),b.measure(2))
        a.measure(5); b.measure(3); self.assertEqual(a.measure(3),b.records[-1]['label'])
        self.assertFalse(np.array_equal(t.fit_x[:64],t.cal_x))
        self.assertFalse(np.array_equal(t.pool,t.test_x[:len(t.pool)]))
        with self.assertRaises(ValueError): a.measure(2)
        with self.assertRaises(ValueError): a.measure(-1)
        self.assertEqual(len(a.records),3)
        obs=t.observations(a.records)
        self.assertEqual(len(obs.y),131)
        np.testing.assert_array_equal(obs.acquired_y,np.array([r['label'] for r in a.records]))

    def test_anonymous_contract_and_imports(self):
        self.assertEqual({f.name for f in dataclasses.fields(Observations)},
           {'x','y','calibration_x','calibration_y','acquired_x','acquired_y','pool','probes','bounds','noise_std','output_scale'})
        for name in ('contracts','features','discovery','witnesses','acquisition'):
            tree=ast.parse((ROOT/'src/corrlaw'/f'{name}.py').read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn(node.module,('oracle','evaluation','experiment'))

    def test_circle_symbolic_and_prior(self):
        u,v,angle=sp.symbols('u v angle',real=True)
        f=u*u+2*v*v; g=1+v*v
        self.assertEqual(sp.expand(f-g),u*u+v*v-1)
        self.assertEqual(sp.trigsimp((f-g).subs({u:sp.cos(angle),v:sp.sin(angle)})),0)
        self.assertEqual(f.subs({u:0,v:sp.Rational(1,2)}),sp.Rational(1,2))
        self.assertEqual(g.subs({u:0,v:sp.Rational(1,2)}),sp.Rational(5,4))
        self.assertEqual(sp.integrate(sp.cos(angle)*sp.sin(angle),(angle,0,2*sp.pi)),0)
        self.assertNotEqual(f.subs({u:0,v:0}),g.subs({u:0,v:0}))

    def test_grammar_and_recovery(self):
        for task, power in [('A',(1,1)),('C',(2,-1)),('D',(1,2))]:
            t=self.trial(task); lib=Library.build(bounds(task),t.probes)
            self.assertLess(len(lib.powers),len(t.fit_x))
            c=np.zeros(len(lib.powers)); j=lib.powers.index(power); c[j]=lib.scale[j]
            self.assertTrue(symbolic_recovery(task,lib,c))
        t=self.trial('F'); lib=Library.build(bounds('F'),t.probes)
        self.assertTrue(all(abs(a)+abs(b)<=3 for a,b in lib.powers))

    def test_witnesses_admissible_and_broadly_distinct(self):
        for task in 'AB':
            obs=self.trial(task).observations([]); fitted=fit(obs,42)
            committee,witnesses,state=augment(obs,fitted)
            self.assertGreater(len(witnesses),0)
            self.assertEqual(state,'ambiguity_witness_found')
            for w in witnesses:
                c=np.array(w['alternative']); lib=fitted.library
                errors=model_errors(c,[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)],obs)
                self.assertTrue(admissible(c,errors,0))
                self.assertGreater(np.linalg.norm(lib.transform(obs.probes)@(c-fitted.best)),.1)

    def test_restricted_pool_and_independent_control(self):
        obs=self.trial('B',control='surface_restricted_queries').observations([])
        fitted=fit(obs,42); _,ws,status=augment(obs,fitted)
        self.assertTrue(ws); self.assertEqual(status,'no_discriminating_query_in_allowed_pool')
        obs=self.trial('B',control='independent_inputs').observations([])
        fitted=fit(obs,42); _,ws,status=augment(obs,fitted)
        self.assertEqual(ws,[])

    def test_design_equivalence_and_determinant(self):
        rng=np.random.default_rng(9); a=rng.normal(size=(20,4)); x=rng.normal(size=(30,4)); ridge=1e-4
        scores=leverage(a,x,ridge); info=a.T@a+ridge*np.eye(4)
        gain=np.array([np.linalg.slogdet(info+np.outer(v,v))[1]-np.linalg.slogdet(info)[1] for v in x])
        np.testing.assert_allclose(np.log1p(scores),gain,atol=1e-12)
        q=np.array([0.,0.,0.,1.]); base=np.ones(4); alpha=.25
        np.testing.assert_allclose(disagreement(x,np.array([base+alpha*q,base-alpha*q])),alpha**2*(x@q)**2)

    def test_end_to_end_replay_and_accounting(self):
        c=self.config(); t=self.trial()
        a=run_policy(t,'augmented_qbc',c); b=run_policy(t,'augmented_qbc',c)
        self.assertEqual(scientific_content(a),scientific_content(b))
        self.assertEqual(len(a['queries']),8)
        self.assertEqual(len({r['query_id'] for r in a['queries']}),8)
        self.assertEqual(a['metrics'][-1]['total_labels'],200)
        for policy in POLICIES:
            obs=t.observations([]); f=fit(obs,0)
            i,_=select(policy,obs,f,f.committee,[0,1],2)
            self.assertNotIn(i,[0,1])

    def test_missing_library_does_not_certify_uniqueness(self):
        # Linear features cannot express the circle relation; a zero-response
        # numerical contract isolates diagnostic coverage from poor model fit.
        from corrlaw.discovery import Fit
        obs=self.trial('B').observations([])
        obs=dataclasses.replace(obs,y=np.zeros_like(obs.y),calibration_y=np.zeros_like(obs.calibration_y))
        lib=Library([(0,0),(1,0),(0,1)],np.ones(3))
        f=Fit(lib,np.zeros(3),np.zeros((1,3)),[],False)
        _,w,state=augment(obs,f)
        self.assertEqual(w,[])
        self.assertEqual(state,'no_witness_within_search_budget')
        # A full generic dictionary does recover an ambiguity on the same inputs.
        _,w,state=augment(obs,fit(obs,10))
        self.assertTrue(w)

    def test_saved_resume_rejects_tampering(self):
        from corrlaw.experiment import run
        c=self.config();c['tasks']=['A'];c['policies']=['random']
        with tempfile.TemporaryDirectory() as d:
            run(c,d)
            run(c,d,resume=True)
            p=next((Path(d)/'units').glob('*.json'))
            value=json.loads(p.read_text());value['queries'][0]['label']+=1;p.write_text(json.dumps(value))
            with self.assertRaises(ValueError):run(c,d,resume=True)

    def test_base_must_also_be_admissible(self):
        obs=self.trial('A').observations([]);f=fit(obs,42)
        f.best=f.best.copy();f.best[0]+=10
        _,w,state=augment(obs,f)
        self.assertEqual(w,[])
        self.assertEqual(state,'poor_observational_fit')

    def test_saved_json_reproduction_preserves_exact_science(self):
        from corrlaw.experiment import run
        from corrlaw.audit import reproduce
        c=self.config();c['tasks']=['A'];c['policies']=['augmented_qbc']
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/'original'; run(c,output)
            replay=Path(d)/'replay';replay.mkdir()
            key=next((output/'units').glob('*.json')).stem
            self.assertTrue(reproduce(output,key,replay))
            record=json.loads((replay/'reproduction.json').read_text())
            self.assertEqual(record['original_scientific_sha256'],record['repeated_scientific_sha256'])
            original=output/'units'/f'{key}.json';value=json.loads(original.read_text())
            value['metrics'][0]['off_rmse']+=1e-6;original.write_text(json.dumps(value))
            self.assertFalse(reproduce(output,key,replay))

    def test_strict_configuration(self):
        c=self.config(); c['typo']=1
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config.json'; p.write_text(json.dumps(c))
            with self.assertRaises(ValueError): load_config(p)


if __name__=='__main__': unittest.main()
