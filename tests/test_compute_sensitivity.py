import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from corrlaw.compute_sensitivity import compare
from corrlaw.experiment import units


class ComputeSensitivityTests(unittest.TestCase):
    def create(self,root,strong=False,mismatch=False):
        root.mkdir();(root/'units').mkdir()
        c=dict(tasks=['C'],seeds=[1,2],constraint_widths=[0] if strong else [0,.01],
            output_noise_std=[.01],controls=['constrained'],policies=['qbc','augmented_qbc'],
            engine='pysr_feature_grammar',n_fit=128,n_calibration=64,n_query_candidates=2048,n_test=2048,
            query_budgets=[0,1,2,4,8],search_settings=dict(niterations=100 if strong else 30,searches=3,
                search_maxsize=15,max_complexity=15,timeout_seconds=30))
        (root/'config.json').write_text(json.dumps(c));entries=[]
        for key,task,seed,width,noise,control,policy in units(c):
            auc=(.1 if policy=='qbc' else .05) if strong else (.2 if policy=='qbc' else .3)
            if width:auc=999. # Unmatched primary conditions must not enter the contrast.
            u=dict(unit_id=key,status='completed',task=task,seed=seed,width=width,noise=noise,control=control,
                policy=policy,auc=auc,metrics=[dict(off_rmse=auc)],initial_data_hash='changed' if mismatch else key,
                evaluation_hash=key)
            p=root/'units'/f'{key}.json';p.write_text(json.dumps(u))
            entries.append(dict(unit_id=key,path=str(p.relative_to(root)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
        (root/'manifest.json').write_text(json.dumps(dict(units=entries)))

    def test_contrast_uses_only_paired_conditions_and_preserves_sign(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.create(root/'primary');self.create(root/'strong',True)
            self.assertEqual(compare(root/'primary',root/'strong',root/'out'),4)
            result=json.loads((root/'out/summary.json').read_text())
            delta=result['paired_acquisition_deltas'][0]
            self.assertAlmostEqual(delta['primary_mean_delta'],.1)
            self.assertAlmostEqual(delta['strong_mean_delta'],-.05)
            q=next(r for r in result['policy_summaries'] if r['policy']=='qbc')
            self.assertAlmostEqual(q['primary_auc_mean'],.2)
            self.assertEqual(len(q['seed_values']),2)

    def test_mismatched_data_refuse_comparison(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.create(root/'primary');self.create(root/'strong',True,True)
            with self.assertRaisesRegex(ValueError,'not paired'):
                compare(root/'primary',root/'strong',root/'out')


if __name__=='__main__':unittest.main()
