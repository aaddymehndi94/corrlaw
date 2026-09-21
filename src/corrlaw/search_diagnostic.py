"""Exploratory exhaustive-search audit of archived finite-library trajectories."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import numpy as np
from corrlaw.diagnostics import exhaustive_fit
from corrlaw.oracle import make_trial,reference
from corrlaw.experiment import save,array_digest,digest,units
from corrlaw.features import Library
from corrlaw.discovery import rmse,model_errors,admissible
from corrlaw.evaluation import symbolic_recovery


def run(parent,output):
    parent=Path(parent);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    c=json.loads((parent/'config.json').read_text())
    manifest=json.loads((parent/'manifest.json').read_text())
    if {r['unit_id'] for r in manifest['units']}!={r[0] for r in units(c)}:
        raise ValueError('incomplete parent manifest')
    if any(r['status']!='completed' for r in manifest['units']):
        raise ValueError('parent has failures; diagnose separately before this complete-case comparison')
    cache={};rows=[];saved=[];start=time.perf_counter()
    (output/'units').mkdir(exist_ok=True)
    for entry in manifest['units']:
        source=parent/entry['path']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError('parent artifact hash mismatch')
        u=json.loads(source.read_text())
        if u['config_hash']!=digest(c):raise ValueError('parent configuration mismatch')
        if u['status']!='completed' or u['control']!='constrained':continue
        trial=make_trial(u['task'],u['seed'],u['width'],u['noise'],u['control'],c)
        actual=array_digest(trial.fit_x,trial.fit_y,trial.cal_x,trial.cal_y,trial.pool,trial.probes)
        if actual!=u['initial_data_hash']:raise ValueError('archived data reconstruction mismatch')
        for budget in (0,2,8):
            obs=trial.observations(u['queries'][:budget])
            key=array_digest(obs.x,obs.y,obs.calibration_x,obs.calibration_y,
                             obs.acquired_x,obs.acquired_y,obs.probes,obs.bounds,trial.test_x,trial.same_x)
            if key not in cache:
                fitted,count=exhaustive_fit(obs)
                lib=fitted.library;phi=lib.transform(trial.test_x)
                matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
                errors=model_errors(fitted.best,matrices,obs)
                cache[key]=dict(
                    coefficients=fitted.best.tolist(),expression=lib.expression(fitted.best),
                    terms=int(np.count_nonzero(fitted.best)),observed_errors=list(errors),
                    admissible=admissible(fitted.best,errors,obs.noise_std),
                    off_rmse=rmse(phi@fitted.best,reference(trial.task,trial.test_x)),
                    same_rmse=rmse(lib.transform(trial.same_x)@fitted.best,reference(trial.task,trial.same_x)),
                    rounded_recovery=symbolic_recovery(trial.task,lib,fitted.best),
                    attempted_supports=count,bounded_candidates=len(fitted.candidates),
                    admissible_candidates=sum(r['admissible'] for r in fitted.candidates),
                    powers=lib.powers,scale=lib.scale.tolist())
            original=next(m for m in u['metrics'] if m['budget']==budget)
            model=u['models'][budget]
            old_lib=Library([tuple(p) for p in model['powers']],np.asarray(model['scale']))
            old_error=rmse(old_lib.transform(trial.test_x)@np.asarray(model['selected_coefficients']),reference(trial.task,trial.test_x))
            if not np.isclose(old_error,original['off_rmse'],rtol=1e-12,atol=1e-12):
                raise ValueError('original metric reconstruction mismatch')
            rows.append(dict(unit_id=u['unit_id'],task=u['task'],seed=u['seed'],width=u['width'],
                noise=u['noise'],policy=u['policy'],budget=budget,observation_hash=key,
                original_expression=model['selected_expression'],original_off_rmse=original['off_rmse'],
                original_diagnostic=model['diagnostic'],exhaustive=cache[key]))
        save(output/'units'/f'{u["unit_id"]}.json',dict(unit_id=u['unit_id'],rows=rows[-3:]))
        saved.append(u['unit_id'])
        if len(rows)%60==0:
            save(output/'diagnostics.json',dict(scope='exploratory reused v2 trajectories, no acquisition rerun',
                parent=str(parent),config_hash=digest(c),unit_ids=saved,rows=len(rows),unique_fits=len(cache),
                runtime_seconds=time.perf_counter()-start,complete=False))
            print(f'{len(rows)} diagnostic rows; {len(cache)} unique fits',flush=True)
    save(output/'diagnostics.json',dict(scope='exploratory reused v2 trajectories, no acquisition rerun',
        parent=str(parent),config_hash=digest(c),unit_ids=saved,rows=len(rows),unique_fits=len(cache),
        runtime_seconds=time.perf_counter()-start,complete=True))
    groups=[]
    for task in c['tasks']:
        for budget in (0,2,8):
            records=[r for r in rows if r['task']==task and r['budget']==budget]
            seed_means=[]
            for seed in sorted({r['seed'] for r in records}):
                matched=[r for r in records if r['seed']==seed]
                old=float(np.mean([r['original_off_rmse'] for r in matched]))
                new=float(np.mean([r['exhaustive']['off_rmse'] for r in matched]))
                seed_means.append(dict(seed=seed,original_mean=old,exhaustive_mean=new,delta=new-old))
            groups.append(dict(task=task,budget=budget,n_policy_conditions=len(records),
                unique_observations=len({r['observation_hash'] for r in records}),seed_means=seed_means,
                original_mean=float(np.mean([r['original_off_rmse'] for r in records])),
                exhaustive_mean=float(np.mean([r['exhaustive']['off_rmse'] for r in records])),
                original_poor_fit=sum(r['original_diagnostic']=='poor_observational_fit' for r in records),
                exhaustive_poor_fit=sum(not r['exhaustive']['admissible'] for r in records),
                exhaustive_rounded_recovery=sum(r['exhaustive']['rounded_recovery'] for r in records)))
    save(output/'summary.json',dict(exploratory=True,groups=groups,rows=len(rows),unique_fits=len(cache)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent',required=True)
    p.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'));a=p.parse_args()
    if not a.output:p.error('output or CORRLAW_RESULT_DIR required')
    run(a.parent,a.output)
