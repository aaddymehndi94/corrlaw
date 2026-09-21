"""Reconstruct exhaustive-diagnostic errors and replay a preselected selected support."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from corrlaw.diagnostics import exhaustive_fit
from corrlaw.discovery import model_errors,admissible,rmse
from corrlaw.evaluation import symbolic_recovery
from corrlaw.experiment import array_digest,save,units
from corrlaw.features import Library
from corrlaw.oracle import make_trial,reference


def inspect(diagnostic,parent):
    diagnostic=Path(diagnostic);parent=Path(parent)
    meta=json.loads((diagnostic/'diagnostics.json').read_text())
    c=json.loads((parent/'config.json').read_text());m=json.loads((parent/'manifest.json').read_text())
    sources={r['unit_id']:r for r in m['units']}
    expected={r[0] for r in units(c) if r[5]=='constrained'}
    issues=[];checked=0;replayed=None
    if not meta['complete'] or set(meta['unit_ids'])!=expected or len(meta['unit_ids'])!=len(expected):
        issues.append('incomplete or duplicate diagnostics')
    for key in sorted(expected):
        file=diagnostic/'units'/f'{key}.json'
        if not file.exists():issues.append(f'missing {key}');continue
        source=parent/sources[key]['path']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=sources[key]['sha256']:
            issues.append(f'{key}: source hash mismatch');continue
        original=json.loads(source.read_text());rows=json.loads(file.read_text())['rows']
        trial=make_trial(original['task'],original['seed'],original['width'],original['noise'],original['control'],c)
        if [r['budget'] for r in rows]!=[0,2,8]:issues.append(f'{key}: wrong budgets')
        for r in rows:
            prefix=f'{key} q{r["budget"]}'
            def check(value,label):
                if not value:issues.append(f'{prefix}: {label}')
            obs=trial.observations(original['queries'][:r['budget']])
            d=r['exhaustive'];lib=Library.build(obs.bounds,obs.probes);coeff=np.asarray(d['coefficients'])
            observation_hash=array_digest(obs.x,obs.y,obs.calibration_x,obs.calibration_y,
                obs.acquired_x,obs.acquired_y,obs.probes,obs.bounds,trial.test_x,trial.same_x)
            check(observation_hash==r['observation_hash'],'observation hash')
            check(d['powers']==[list(p) for p in lib.powers] and d['scale']==lib.scale.tolist(),'dictionary')
            check(np.count_nonzero(coeff)==d['terms'] and d['terms']<=3 and max(abs(coeff))<=20,'sparse class')
            check(d['expression']==lib.expression(coeff),'saved expression')
            matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
            error=model_errors(coeff,matrices,obs)
            check(np.allclose(error,d['observed_errors'],rtol=1e-12,atol=1e-12),'observed errors')
            check(admissible(coeff,error,obs.noise_std)==d['admissible'],'admissibility')
            for name,inputs in [('off_rmse',trial.test_x),('same_rmse',trial.same_x)]:
                metric=rmse(lib.transform(inputs)@coeff,reference(trial.task,inputs))
                check(np.isclose(metric,d[name],rtol=1e-12,atol=1e-12),name)
            check(symbolic_recovery(trial.task,lib,coeff)==d['rounded_recovery'],'rounded recovery')
            old=next(v for v in original['metrics'] if v['budget']==r['budget'])
            check(old['off_rmse']==r['original_off_rmse'],'original error')
            check(d['attempted_supports']==833,'enumerated support count')
            if key=='E-s92001-w0-n0.01-constrained-augmented_qbc' and r['budget']==2:
                fitted,count=exhaustive_fit(obs)
                same=np.array_equal(fitted.best,coeff)
                check(same and count==d['attempted_supports'],'fresh exhaustive support replay')
                replayed=dict(unit_id=key,budget=2,exact_coefficients=bool(same),attempted_supports=count)
            checked+=1
    if checked!=1200 or meta['rows']!=checked:issues.append('incorrect total diagnostic rows')
    if replayed is None:issues.append('missing preselected support replay')
    return dict(valid=not issues,rows_checked=checked,reproduction=replayed,errors=issues)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('diagnostic');p.add_argument('--parent',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();r=inspect(a.diagnostic,a.parent);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    save(out/'validation.json',r);print(json.dumps(r,indent=2));raise SystemExit(not r['valid'])
