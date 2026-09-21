"""Independent artifact and algebraic-prior checks, plus exact prior-aware replay."""
import argparse
import json
from pathlib import Path
import numpy as np
from corrlaw.audit import inspect_run
from corrlaw.diagnostics import prior_library
from corrlaw.oracle import make_trial
from corrlaw.prior_experiment import run_policy
from corrlaw.experiment import save,digest,scientific_content


def inspect_prior(path):
    path=Path(path);result=inspect_run(path)
    c=json.loads((path/'config.json').read_text())
    m=json.loads((path/'manifest.json').read_text())
    checks=0
    for row in m['units']:
        u=json.loads((path/row['path']).read_text())
        if u['status']!='completed':continue
        trial=make_trial(u['task'],u['seed'],u['width'],u['noise'],u['control'],c)
        for model in u['models']:
            obs=trial.observations(u['queries'][:model['budget']])
            lib=prior_library(obs,c['prior'])
            if [list(p) for p in lib.powers]!=model['powers'] or lib.scale.tolist()!=model['scale']:
                result['errors'].append(f'{u["unit_id"]}: incorrect prior grammar')
            if c['prior']!='none':
                origin=lib.transform(np.zeros((1,2)))
                arrays=[model['selected_coefficients'],*model['committee']]
                arrays+=[r['coefficients'] for r in model['candidates']]
                for coeff in arrays:
                    if float((origin@np.asarray(coeff))[0])!=0.:
                        result['errors'].append(f'{u["unit_id"]}: origin violation')
            checks+=1
    result['valid']=not result['errors'] and not result['failed_units']
    result['prior_models_checked']=checks
    return result


def reproduce(path,unit_id,output):
    path=Path(path);c=json.loads((path/'config.json').read_text())
    original=json.loads((path/'units'/f'{unit_id}.json').read_text())
    trial=make_trial(original['task'],original['seed'],original['width'],original['noise'],original['control'],c)
    repeated=run_policy(trial,original['policy'],c,c['prior'])
    old={k:original[k] for k in scientific_content(repeated)}
    new=scientific_content(repeated);exact=digest(old)==digest(new)
    save(Path(output)/'reproduction.json',dict(parent=str(path),unit_id=unit_id,prior=c['prior'],
        exact_match=exact,original_scientific_sha256=digest(old),repeated_scientific_sha256=digest(new)))
    return exact


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('--output',required=True)
    p.add_argument('--reproduce');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    if a.reproduce:valid=reproduce(a.run,a.reproduce,out)
    else:
        result=inspect_prior(a.run);save(out/'validation.json',result);print(json.dumps(result,indent=2));valid=result['valid']
    raise SystemExit(not valid)
