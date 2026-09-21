"""Numerical B origin/parity prior controls, declared exploratory follow-ups."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
import traceback
import numpy as np
from corrlaw.diagnostics import prior_fit,prior_augment
from corrlaw.oracle import make_trial
from corrlaw.acquisition import select
from corrlaw.evaluation import evaluate,auc,symbolic_recovery
from corrlaw.experiment import save,digest,array_digest,units,engine_hash,scientific_content


def run_policy(trial,policy,c,prior):
    start=time.perf_counter();oracle=trial.oracle()
    records=[];models=[];fitting_seconds=augmentation_seconds=0.
    for budget in range(9):
        obs=trial.observations(oracle.records);t=time.perf_counter()
        fitted=prior_fit(obs,np.random.SeedSequence([trial.seed,400,budget]),prior)
        fitting_seconds+=time.perf_counter()-t
        ordinary=fitted.committee;t=time.perf_counter()
        augmented,witnesses,diagnostic=prior_augment(obs,fitted)
        augmentation_seconds+=time.perf_counter()-t
        if policy=='diversified_qbc':
            t=time.perf_counter()
            diversified=prior_fit(obs,np.random.SeedSequence([trial.seed,401,budget]),prior,True)
            fitting_seconds+=time.perf_counter()-t
            committee=diversified.committee
        else:committee=augmented if policy=='augmented_qbc' else ordinary
        if budget in c['query_budgets']:
            records.append(dict(budget=budget,total_labels=c['n_fit']+c['n_calibration']+budget,
                witness_count=len(witnesses),diagnostic=diagnostic,
                rounded_symbolic_recovery=symbolic_recovery(trial.task,fitted.library,fitted.best),
                **evaluate(trial,fitted,committee)))
        lib=fitted.library
        models.append(dict(budget=budget,powers=lib.powers,scale=lib.scale.tolist(),
            selected_coefficients=fitted.best.tolist(),selected_expression=lib.expression(fitted.best),
            committee=committee.tolist(),ordinary_committee=ordinary.tolist(),
            candidates=[dict(coefficients=r['coefficients'].tolist(),expression=lib.expression(r['coefficients']),
                             errors=list(r['errors']),terms=r['terms'],admissible=r['admissible']) for r in fitted.candidates],
            witnesses=witnesses,diagnostic=diagnostic))
        if budget<8:
            choice,score=select(policy,obs,fitted,committee,[r['query_id'] for r in oracle.records],
                                np.random.SeedSequence([trial.seed,402,budget]))
            oracle.measure(choice);oracle.records[-1]['acquisition_score']=score
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(status='completed',metrics=records,auc=auc(records),models=models,queries=oracle.records,
        prior=prior,initial_data_hash=array_digest(trial.fit_x,trial.fit_y,trial.cal_x,trial.cal_y,trial.pool,trial.probes),
        evaluation_hash=array_digest(trial.test_x,trial.same_x),runtime_seconds=time.perf_counter()-start,
        fitting_seconds=fitting_seconds,augmentation_seconds=augmentation_seconds,
        process_peak_rss_bytes=int(rss if sys.platform=='darwin' else rss*1024))


def run(c,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if c['tasks']!=['B'] or c['stage']!='development' or c['engine']!='finite_library_prior_control':
        raise ValueError('this preregistered exploratory control is restricted to B development')
    priors=c['priors']
    if priors!=['none','zero_origin','zero_origin_and_even']:raise ValueError('unexpected prior set')
    for prior in priors:
        directory=output/prior
        directory.mkdir();(directory/'units').mkdir()
        config={k:v for k,v in c.items() if k!='priors'};config['prior']=prior
        save(directory/'config.json',config);save(directory/'engine.json',dict(source_sha256=engine_hash()))
        manifest=[];failed=0;expected=list(units(config))
        for key,task,seed,width,noise,control,policy in expected:
            identity=dict(unit_id=key,task=task,seed=seed,width=width,noise=noise,control=control,
                          policy=policy,config_hash=digest(config))
            try:
                trial=make_trial(task,seed,width,noise,control,config)
                result=dict(identity,**run_policy(trial,policy,config,prior))
            except Exception as exc:
                result=dict(identity,status='failed',error=repr(exc),traceback=traceback.format_exc())
            file=directory/'units'/f'{key}.json';save(file,result)
            failed+=result['status']!='completed'
            manifest.append(dict(identity,status=result['status'],path=str(file.relative_to(directory)),
                sha256=hashlib.sha256(file.read_bytes()).hexdigest(),scientific_sha256=digest(scientific_content(result))))
            save(directory/'manifest.json',dict(units=manifest,failed=failed,expected_units=len(expected)))
            print(prior,len(manifest),len(expected),key,result['status'],flush=True)
        if failed:raise RuntimeError(f'{failed} failed units under {prior}')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True)
    parser.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'));args=parser.parse_args()
    if not args.output:parser.error('output or CORRLAW_RESULT_DIR required')
    run(json.loads(Path(args.config).read_text()),args.output)
