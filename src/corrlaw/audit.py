"""Artifact validation and fresh-process reproduction, independent of run success."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from .acquisition import POLICIES
from .discovery import admissible, model_errors, fit
from .experiment import digest, scientific_content, units, run_policy, save
from .features import Library
from .oracle import make_trial, reference


def inspect_run(path):
    path = Path(path)
    c = json.loads((path/'config.json').read_text())
    manifest = json.loads((path/'manifest.json').read_text())
    expected = {r[0] for r in units(c)}
    actual = {r['unit_id'] for r in manifest['units']}
    errors = []
    if actual != expected or len(actual) != len(manifest['units']):
        errors.append('missing, unexpected or duplicate units')
    groups = {}; witness_checked = 0; completed = 0; failed = []
    for row in manifest['units']:
        file = path/row['path']; u = json.loads(file.read_text())
        if hashlib.sha256(file.read_bytes()).hexdigest() != row['sha256']:
            errors.append(f'{row["unit_id"]}: file hash mismatch')
        if digest(scientific_content(u)) != row['scientific_sha256']:
            errors.append(f'{row["unit_id"]}: science hash mismatch')
        if u['status'] != 'completed':
            failed.append(u['unit_id']); continue
        completed += 1
        trial = make_trial(u['task'],u['seed'],u['width'],u['noise'],u['control'],c)
        group = (u['task'],u['seed'],u['width'],u['noise'],u['control'])
        groups.setdefault(group,[]).append(u)
        ids = [r['query_id'] for r in u['queries']]
        if len(ids) != 8 or len(set(ids)) != 8:
            errors.append(f'{u["unit_id"]}: incorrect query accounting')
        oracle = trial.oracle()
        for r in u['queries']:
            if oracle.measure(r['query_id']) != r['label'] or r['x'] != trial.pool[r['query_id']].tolist():
                errors.append(f'{u["unit_id"]}: label or coordinate mismatch')
        if [r['budget'] for r in u['metrics']] != c['query_budgets']:
            errors.append(f'{u["unit_id"]}: wrong budgets')
        for r in u['metrics']:
            if r['total_labels'] != c['n_fit']+c['n_calibration']+r['budget']:
                errors.append(f'{u["unit_id"]}: wrong total labels')
        for model in u['models']:
            obs=trial.observations(u['queries'][:model['budget']])
            lib=Library([tuple(p) for p in model['powers']],np.array(model['scale']))
            matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
            for witness in model['witnesses']:
                for name in ('base','alternative'):
                    coeff=np.array(witness[name])
                    if not admissible(coeff, model_errors(coeff,matrices,obs),obs.noise_std):
                        errors.append(f'{u["unit_id"]}: inadmissible {name}')
                witness_checked += 1
            metric = next((r for r in u['metrics'] if r['budget']==model['budget']),None)
            if metric:
                predicted=lib.transform(trial.test_x)@np.array(model['selected_coefficients'])
                off=float(np.sqrt(np.mean((predicted-reference(trial.task,trial.test_x))**2)))
                if not np.isclose(off,metric['off_rmse'],rtol=1e-12,atol=1e-12):
                    errors.append(f'{u["unit_id"]}: metric mismatch')
    for group, records in groups.items():
        if {r['policy'] for r in records} != set(c['policies']):
            errors.append(f'{group}: missing policy (including failed units)')
        if len({r['initial_data_hash'] for r in records}) != 1 or len({r['evaluation_hash'] for r in records}) != 1:
            errors.append(f'{group}: unpaired initial/evaluation data')
        initial = [r['models'][0]['selected_coefficients'] for r in records]
        if any(v != initial[0] for v in initial):
            errors.append(f'{group}: different initial point estimators')
    return dict(valid=not errors and not failed, expected_units=len(expected), completed_units=completed,
                failed_units=failed, witnesses_checked=witness_checked, errors=errors)


def reproduce(path, unit_id, output):
    path=Path(path); c=json.loads((path/'config.json').read_text())
    original=json.loads((path/'units'/f'{unit_id}.json').read_text())
    trial=make_trial(original['task'],original['seed'],original['width'],original['noise'],original['control'],c)
    repeated=run_policy(trial,original['policy'],c)
    original_science={k:original[k] for k in scientific_content(repeated)}
    exact=original_science==scientific_content(repeated)
    save(Path(output)/'reproduction.json',dict(parent=str(path),unit_id=unit_id,exact_match=exact,
          original_scientific_sha256=digest(original_science),
          repeated_scientific_sha256=digest(scientific_content(repeated)),
          metrics=repeated['metrics'],queries=repeated['queries']))
    return exact


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('run'); parser.add_argument('--output',required=True)
    parser.add_argument('--reproduce')
    args=parser.parse_args(); output=Path(args.output); output.mkdir(parents=True,exist_ok=True)
    if args.reproduce:
        valid=reproduce(args.run,args.reproduce,output)
    else:
        result=inspect_run(args.run); save(output/'validation.json',result); print(json.dumps(result,indent=2)); valid=result['valid']
    raise SystemExit(0 if valid else 1)

if __name__=='__main__': main()
