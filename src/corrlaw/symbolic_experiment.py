"""Paired PySR active experiments with immutable equations and query records."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
import traceback
import numpy as np
import sympy as sp
from . import symbolic
from .acquisition import POLICIES
from .oracle import make_trial, reference, CONTROLS
from .experiment import KEYS, save, digest, array_digest, units, engine_hash
from .evaluation import auc


SETTINGS = {'searches', 'niterations', 'search_maxsize', 'max_complexity', 'timeout_seconds'}
DEADLINE = 1790040600.0  # 2026-09-22 01:30 UTC: user deadline minus reporting hour.


def load_config(path):
    c = json.loads(Path(path).read_text())
    if set(c) != KEYS | {'search_settings'}:
        raise ValueError('unexpected symbolic configuration keys')
    if c['schema_version'] != 1 or c['status'] != 'ready' or c['engine'] != 'pysr_feature_grammar':
        raise ValueError('unsupported symbolic configuration')
    if c['stage'] not in ('development', 'confirmation'):
        raise ValueError('invalid stage')
    for field, legal in [('tasks', 'AB' if c['stage']=='development' else 'CDEF'),
                         ('policies', POLICIES), ('controls', CONTROLS),
                         ('constraint_widths', [0, .01, .05]), ('output_noise_std', [0, .01])]:
        if not c[field] or len(set(c[field])) != len(c[field]) or any(v not in legal for v in c[field]):
            raise ValueError(f'invalid {field}')
    if c['query_budgets'] != [0, 1, 2, 4, 8]:
        raise ValueError('invalid query budgets')
    for field in ('n_fit','n_calibration','n_query_candidates','n_test'):
        if type(c[field]) != int or c[field] < (32 if field=='n_fit' else 8):
            raise ValueError(f'invalid {field}')
    if not c['seeds'] or len(set(c['seeds'])) != len(c['seeds']) or any(type(s)!=int or s<0 for s in c['seeds']):
        raise ValueError('invalid seeds')
    settings = c['search_settings']
    if set(settings) != SETTINGS or any(type(v)!=int or v<=0 for v in settings.values()):
        raise ValueError('invalid search settings')
    if settings['searches'] < 2 or settings['max_complexity'] < settings['search_maxsize']:
        raise ValueError('invalid ensemble or complexity limits')
    return c


def rounded_recovery(task, model, lib):
    x0, x1 = sp.symbols('x0 x1')
    expression = sp.sympify(model.physical_expression(lib))
    expression = expression.xreplace({n: sp.Rational(str(round(float(n), 6)))
                                     for n in expression.atoms(sp.Float)})
    ref = {'A':x0*x1,'B':x0*x0+2*x1*x1,'C':x0*x0/x1,'D':x0*x1*x1,
           'E':x0+x1,'F':x0*x1/(x0+x1)}[task]
    return bool(sp.cancel(expression-ref)==0)


def evaluate(trial, fitted, committee):
    lib = fitted.library
    off, same = lib.transform(trial.test_x), lib.transform(trial.same_x)
    error = symbolic.rmse(fitted.best.predict(off), reference(trial.task, trial.test_x))
    spread = float(np.sqrt(np.mean(np.var(symbolic.predictions(committee, off), axis=1))))
    return dict(off_rmse=error, same_rmse=symbolic.rmse(fitted.best.predict(same),
               reference(trial.task, trial.same_x)), committee_rms_std=spread,
               false_consensus=bool(error>.1 and spread<.05))


def scientific_content(unit):
    data = copy.deepcopy(unit)
    for name in ('runtime_seconds','fitting_seconds','augmentation_seconds','process_peak_rss_bytes'):
        data.pop(name, None)
    for model in data.get('models', []):
        for search in model['searches']:
            search.pop('runtime_seconds', None)
    return data


def run_policy(trial, policy, c, enforce_cutoff=False):
    start = time.perf_counter()
    oracle = trial.oracle()
    records, models = [], []
    fitting_seconds = augmentation_seconds = 0.
    history=[]
    for budget in range(9):
        if enforce_cutoff and time.time() >= DEADLINE:
            raise TimeoutError('overnight experiment cutoff reached')
        obs = trial.observations(oracle.records)
        fit_start = time.perf_counter()
        fitted = symbolic.fit(obs, [trial.seed, 1400, budget], c['search_settings'],
                              diversified=policy=='diversified_qbc',history=history,generation=budget)
        history=fitted.candidates
        fitting_seconds += time.perf_counter()-fit_start
        aug_start = time.perf_counter()
        augmented, witnesses, diagnostic = symbolic.augment(obs, fitted, c['search_settings'])
        augmentation_seconds += time.perf_counter()-aug_start
        committee = augmented if policy=='augmented_qbc' else fitted.committee
        if budget in c['query_budgets']:
            records.append(dict(budget=budget,total_labels=c['n_fit']+c['n_calibration']+budget,
                witness_count=len(witnesses),diagnostic=diagnostic,
                rounded_symbolic_recovery=rounded_recovery(trial.task,fitted.best,fitted.library),
                **evaluate(trial,fitted,committee)))
        models.append(dict(budget=budget,powers=fitted.library.powers,scale=fitted.library.scale.tolist(),
            selected_expression=fitted.best.expression,
            physical_expression=fitted.best.physical_expression(fitted.library),
            committee=[m.expression for m in committee],
            search_committee=[m.expression for m in fitted.committee],
            candidates=fitted.candidates,searches=fitted.searches,
            witnesses=witnesses,diagnostic=diagnostic))
        if budget<8:
            query_id,score=symbolic.select(policy,obs,fitted,committee,
                [r['query_id'] for r in oracle.records],[trial.seed,1402,budget])
            oracle.measure(query_id)
            oracle.records[-1]['acquisition_score']=score
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(status='completed',metrics=records,auc=auc(records),models=models,queries=oracle.records,
        initial_data_hash=array_digest(trial.fit_x,trial.fit_y,trial.cal_x,trial.cal_y,trial.pool,trial.probes),
        evaluation_hash=array_digest(trial.test_x,trial.same_x),runtime_seconds=time.perf_counter()-start,
        fitting_seconds=fitting_seconds,augmentation_seconds=augmentation_seconds,
        process_peak_rss_bytes=int(rss if sys.platform=='darwin' else rss*1024))


def run(c, output, resume=False):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    provenance={'source_sha256':engine_hash()}
    old_manifest={}
    if (output/'config.json').exists():
        if not resume or json.loads((output/'config.json').read_text())!=c:
            raise ValueError('existing output requires matching configuration and resume')
        if json.loads((output/'engine.json').read_text())!=provenance:
            raise ValueError('resume requires identical source')
        if (output/'manifest.json').exists():
            old_manifest={r['unit_id']:r for r in json.loads((output/'manifest.json').read_text())['units']}
    else:
        save(output/'config.json',c);save(output/'engine.json',provenance)
    unit_dir=output/'units';unit_dir.mkdir(exist_ok=True)
    manifest=[];failed=0;expected=list(units(c))
    for key,task,seed,width,noise,control,policy in expected:
        path=unit_dir/f'{key}.json'
        identity=dict(unit_id=key,task=task,seed=seed,width=width,noise=noise,control=control,
                      policy=policy,config_hash=digest(c))
        if path.exists():
            row=old_manifest.get(key)
            if not row or hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:
                raise ValueError('unverified saved unit; preserve and use a new run ID')
            result=json.loads(path.read_text())
            if any(result.get(k)!=v for k,v in identity.items()):
                raise ValueError('unit identity mismatch')
        else:
            try:
                trial=make_trial(task,seed,width,noise,control,c)
                result=dict(identity,**run_policy(trial,policy,c,enforce_cutoff=True))
            except Exception as exc:
                result=dict(identity,status='failed',error=repr(exc),traceback=traceback.format_exc())
            save(path,result)
        failed+=result['status']!='completed'
        manifest.append(dict(identity,status=result['status'],path=str(path.relative_to(output)),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            scientific_sha256=digest(scientific_content(result))))
        save(output/'manifest.json',dict(units=manifest,failed=failed,expected_units=len(expected)))
        print(f'{len(manifest)}/{len(expected)} {key} {result["status"]}',flush=True)
        if time.time()>=DEADLINE:
            raise TimeoutError('overnight experiment cutoff reached')
    return failed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True)
    parser.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'))
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    if not args.output:parser.error('output or CORRLAW_RESULT_DIR is required')
    raise SystemExit(bool(run(load_config(args.config),args.output,args.resume)))


if __name__=='__main__':main()
