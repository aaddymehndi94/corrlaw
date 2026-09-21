"""Saved-artifact comparison of original and augmented disagreement on identical data.

The evaluator uses hidden labels only after acquisition has finished. Threshold
crossings describe a heuristic diagnostic, not calibrated uncertainty or causality.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import numpy as np
from corrlaw.experiment import save, units
from corrlaw.features import Library
from corrlaw.oracle import make_trial, reference
from corrlaw.symbolic import Expression, predictions


def spread_summary(original, augmented, error, poor_fit):
    a=float(np.sqrt(np.mean(np.var(original,axis=1))))
    b=float(np.sqrt(np.mean(np.var(augmented,axis=1))))
    high=bool(error>.1)
    old=bool(high and a<.05);new=bool(high and b<.05)
    return dict(off_rmse=float(error),ordinary_rms_spread=a,augmented_rms_spread=b,
                high_error=high,ordinary_false_consensus=old,augmented_false_consensus=new,
                spread_threshold_crossed_up=bool(a<.05 and b>=.05),
                spread_threshold_crossed_down=bool(a>=.05 and b<.05),
                high_error_low_spread_flag_removed=bool(old and not new),
                high_error_low_spread_flag_added=bool(new and not old),
                poor_observational_fit=bool(poor_fit))


def analyze(run,output):
    run=Path(run);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    c=json.loads((run/'config.json').read_text());m=json.loads((run/'manifest.json').read_text())
    expected={r[0] for r in units(c)}
    if {r['unit_id'] for r in m['units']}!=expected or len(m['units'])!=len(expected):
        raise ValueError('incomplete or duplicate parent manifest')
    if any(r['status']!='completed' for r in m['units']):raise ValueError('parent contains failures')
    rows=[]
    for entry in m['units']:
        path=run/entry['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('parent hash mismatch')
        u=json.loads(path.read_text())
        if u['policy']!='augmented_qbc':continue
        trial=make_trial(u['task'],u['seed'],u['width'],u['noise'],u['control'],c)
        for model in u['models']:
            budget=model['budget']
            if budget not in c['query_budgets']:continue
            lib=Library([tuple(p) for p in model['powers']],np.asarray(model['scale']))
            phi=lib.transform(trial.test_x)
            if 'selected_coefficients' in model:
                base=phi@np.asarray(model['selected_coefficients'])
                original=phi@np.asarray(model['ordinary_committee']).T
                augmented=phi@np.asarray(model['committee']).T
            else:
                base=Expression(model['selected_expression'],len(lib.powers)).predict(phi)
                original=predictions([Expression(s,len(lib.powers)) for s in model['search_committee']],phi)
                augmented=predictions([Expression(s,len(lib.powers)) for s in model['committee']],phi)
            error=float(np.sqrt(np.mean((base-reference(trial.task,trial.test_x))**2)))
            values=spread_summary(original,augmented,error,model['diagnostic']=='poor_observational_fit')
            saved=next(r for r in u['metrics'] if r['budget']==budget)
            if not np.isclose(saved['off_rmse'],error,rtol=1e-12,atol=1e-12):raise ValueError('saved error mismatch')
            if not np.isclose(saved['committee_rms_std'],values['augmented_rms_spread'],rtol=1e-12,atol=1e-12):
                raise ValueError('saved augmented spread mismatch')
            if saved['false_consensus']!=values['augmented_false_consensus']:raise ValueError('saved flag mismatch')
            rows.append(dict(unit_id=u['unit_id'],task=u['task'],seed=u['seed'],width=u['width'],noise=u['noise'],
                             control=u['control'],budget=budget,ordinary_size=original.shape[1],
                             augmented_size=augmented.shape[1],witnesses=len(model['witnesses']),**values))
    group=defaultdict(list)
    for r in rows:group[(r['task'],r['control'],r['budget'])].append(r)
    counts=('high_error','ordinary_false_consensus','augmented_false_consensus',
            'spread_threshold_crossed_up','spread_threshold_crossed_down',
            'high_error_low_spread_flag_removed','high_error_low_spread_flag_added','poor_observational_fit')
    summaries=[]
    for key,rs in sorted(group.items()):
        seeds=[]
        for seed in sorted({r['seed'] for r in rs}):
            subset=[r for r in rs if r['seed']==seed]
            seeds.append(dict(seed=seed,conditions=len(subset),**{name:sum(r[name] for r in subset) for name in counts}))
        summaries.append(dict(task=key[0],control=key[1],budget=key[2],conditions=len(rs),seed_counts=seeds,
                             with_witness=sum(r['witnesses']>0 for r in rs),
                             valid_fit_flag_removed=sum(r['high_error_low_spread_flag_removed'] and not r['poor_observational_fit'] for r in rs),
                             **{name:sum(r[name] for r in rs) for name in counts}))
    save(output/'summary.json',dict(source_run=str(run),engine=c['engine'],rows=len(rows),summaries=summaries,
        scope='Original versus augmented committee evaluated on identical saved augmented-policy histories; no acquisition rerun.',
        thresholds=dict(high_error_gt=.1,low_spread_lt=.05),
        interpretation='A threshold crossing does not correct the fixed point predictor, calibrate confidence, or show better acquisitions.'))
    (output/'units').mkdir(exist_ok=True)
    grouped=defaultdict(list)
    for r in rows:grouped[r['unit_id']].append(r)
    for key,rs in grouped.items():save(output/'units'/f'{key}.json',dict(rows=rs))
    print(json.dumps(dict(units=len(grouped),rows=len(rows))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('--output',required=True)
    a=p.parse_args();analyze(a.run,a.output)
