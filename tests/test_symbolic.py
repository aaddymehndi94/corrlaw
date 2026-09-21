import ast
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import numpy as np
import sympy as sp
from corrlaw.features import Library
from corrlaw.oracle import make_trial, reference
from corrlaw.symbolic import Expression, SymbolicFit, augment, errors, admissible, select
from corrlaw.symbolic import arithmetic_complexity
from corrlaw.symbolic_experiment import load_config, scientific_content

ROOT=Path(__file__).resolve().parents[1]


class SymbolicTests(unittest.TestCase):
    def setUp(self):
        self.config=load_config(ROOT/'configs/pysr-fair-smoke.json')
        self.trial=make_trial('A',201,0,0,'constrained',self.config)
        self.obs=self.trial.observations([])
        self.lib=Library.build(self.obs.bounds,self.obs.probes)

    def base(self):
        j=self.lib.powers.index((1,1))
        model=Expression(f'{self.lib.scale[j]:.17g}*z{j}',len(self.lib.powers))
        return SymbolicFit(self.lib,model,[model],[],[],False)

    def test_numerical_contract_and_no_oracle_import(self):
        tree=ast.parse((ROOT/'src/corrlaw/symbolic.py').read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom):
                self.assertNotIn(node.module,('oracle','evaluation','experiment','symbolic_experiment'))
        f=self.base()
        np.testing.assert_allclose(f.best.predict(self.lib.transform(self.trial.pool)),
                                   reference('A',self.trial.pool),atol=1e-14)

    def test_rational_grammar_can_express_series_capacitance(self):
        u=self.lib.powers.index((1,0));v=self.lib.powers.index((0,1))
        a=f'({self.lib.scale[u]:.17g}*z{u})';b=f'({self.lib.scale[v]:.17g}*z{v})'
        model=Expression(f'{a}*{b}/({a}+{b})',len(self.lib.powers))
        np.testing.assert_allclose(model.predict(self.lib.transform(self.trial.pool)),
                                   reference('F',self.trial.pool),atol=1e-14)

    def test_nonfinite_unknown_and_complexity_rejections(self):
        with self.assertRaises(ValueError):Expression('unknown+z1',3)
        with self.assertRaises(ValueError):Expression('1/z1',3).predict(np.zeros((3,3)))
        self.assertFalse(Expression('21*z1',3).bounded(31))
        self.assertFalse(Expression('z0+z1+z2',3).bounded(2))
        np.testing.assert_array_equal(Expression('2',3).predict(np.zeros((3,3))),np.full(3,2.))

    def test_common_arithmetic_tree_budget(self):
        examples={'z0-z1':3,'z0/z1':3,'z0**3':5,'z0**(-2)':5,
                  'z0/(z1+z2)':5,'z0/z1+z2':5,'z0*z1*z2':5,
                  '-z0-z1':5,'-2*z0-z1':5,'z0**2-z1**2':7,
                  '(z0+z1)*(z0-z1)':7,'z0**2/z1**3':9}
        for expression,expected in examples.items():
            self.assertEqual(arithmetic_complexity(sp.sympify(expression)),expected,expression)
        self.assertTrue(Expression('z0**8',3).bounded(15))
        self.assertFalse(Expression('z0**9',3).bounded(15))

    def test_saved_alternatives_are_valid_and_discriminating(self):
        fitted=self.base();settings=self.config['search_settings']
        committee,ws,state=augment(self.obs,fitted,settings)
        self.assertTrue(ws);self.assertEqual(state,'ambiguity_witness_found')
        matrices=[self.lib.transform(x) for x in (self.obs.x,self.obs.calibration_x,self.obs.acquired_x)]
        for w in ws:
            alt=Expression(w['alternative'],len(self.lib.powers))
            self.assertTrue(admissible(alt,errors(alt,matrices,self.obs),0,self.config['search_settings']['max_complexity']))
            self.assertGreater(w['max_pool_difference'],.01)
            q=np.array(w['q']);self.assertAlmostEqual(np.sqrt(np.mean((self.lib.transform(self.obs.probes)@q)**2)),1)
        selected,score=select('augmented_qbc',self.obs,fitted,committee,[],2)
        self.assertGreater(score,0)
        second,_=select('augmented_qbc',self.obs,fitted,committee,[selected],2)
        self.assertNotEqual(selected,second)

    def test_inadmissible_base_cannot_create_witness(self):
        fitted=self.base();fitted.best=Expression('10',len(self.lib.powers))
        _,ws,state=augment(self.obs,fitted,self.config['search_settings'])
        self.assertEqual(ws,[]);self.assertEqual(state,'poor_observational_fit')

    def test_independent_control_does_not_emit_witnesses(self):
        trial=make_trial('A',201,0,0,'independent_inputs',self.config)
        obs=trial.observations([]);lib=Library.build(obs.bounds,obs.probes)
        j=lib.powers.index((1,1));base=Expression(f'{lib.scale[j]:.17g}*z{j}',len(lib.powers))
        _,ws,_=augment(obs,SymbolicFit(lib,base,[base],[],[],False),self.config['search_settings'])
        self.assertEqual(ws,[])

    def test_scientific_contract_strips_only_timing(self):
        data={'runtime_seconds':2,'models':[{'searches':[{'runtime_seconds':1,'seed':8}]}],
              'auc':.123,'queries':[{'label':4}]}
        result=scientific_content(data)
        self.assertEqual(result,{'models':[{'searches':[{'seed':8}]}],'auc':.123,'queries':[{'label':4}]})
        self.assertIn('runtime_seconds',data)

    def test_config_rejects_invalid_methods(self):
        with tempfile.TemporaryDirectory() as d:
            c=self.config;c['search_settings']['searches']=1
            p=Path(d)/'config.json';p.write_text(json.dumps(c))
            with self.assertRaises(ValueError):load_config(p)

    def test_config_rejects_search_and_alternative_budget_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            c=self.config;c['search_settings']['max_complexity']=31
            p=Path(d)/'config.json';p.write_text(json.dumps(c))
            with self.assertRaises(ValueError):load_config(p)

    def test_retention_preserves_good_models_and_refilters_old_aliases(self):
        import pandas as pd
        from corrlaw.symbolic import fit
        class WeakSearch:
            def __init__(self,**kwargs):pass
            def fit(self,*args,**kwargs):
                self.equations_=pd.DataFrame([{'sympy_format':'0','complexity':1,'loss':1.}])
        correct=self.base().best
        j=self.lib.powers.index((0,2))
        alias=Expression(f'{self.lib.scale[j]:.17g}*z{j}',len(self.lib.powers))
        history=[dict(expression=m.expression,search=0,generation=0,index=i,
                      search_complexity=3,search_loss=0.,errors=[0.,0.,0.,0.],
                      bounded=True,complexity=m.complexity,admissible=True)
                 for i,m in enumerate((correct,alias))]
        oracle=self.trial.oracle()
        oracle.measure(int(np.argmax(abs(self.trial.pool[:,0]-self.trial.pool[:,1]))))
        obs=self.trial.observations(oracle.records)
        with patch.dict('sys.modules',{'pysr':SimpleNamespace(PySRRegressor=WeakSearch)}):
            fitted=fit(obs,[201,1400,1],self.config['search_settings'],history=history,generation=1)
        self.assertEqual(fitted.best.expression,correct.expression)
        bad=next(r for r in fitted.candidates if r['expression']==alias.expression)
        self.assertFalse(bad['admissible'])
        self.assertGreater(bad['errors'][2],.1)
        self.assertNotIn(alias.expression,[m.expression for m in fitted.committee])


if __name__=='__main__':unittest.main()
