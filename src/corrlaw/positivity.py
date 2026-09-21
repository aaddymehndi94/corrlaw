"""Descriptive physical-prior sensitivity; never changes acquisitions or primary metrics."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import numpy as np
from corrlaw.features import Library
from corrlaw.symbolic import Expression
from corrlaw.oracle import make_trial
from corrlaw.experiment import save


def analyze(run,output):
    run=Path(run);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    config=json.loads((run/'config.json').read_text());manifest=json.loads((run/'manifest.json').read_text())
    if len(manifest['units'])!=manifest['expected_units']:
        raise ValueError('incomplete input manifest')
    rows=[];failed=[]
    for row in manifest['units']:
        path=run/row['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('unit hash mismatch')
        unit=json.loads(path.read_text())
        if unit['status']!='completed':failed.append(unit['unit_id']);continue
        trial=make_trial(unit['task'],unit['seed'],unit['width'],unit['noise'],unit['control'],config)
        for model in unit['models']:
            lib=Library([tuple(p) for p in model['powers']],np.asarray(model['scale']))
            phi=lib.transform(trial.probes);ws=model['witnesses']
            if 'selected_coefficients' in model:
                base=phi@np.asarray(model['selected_coefficients'])
                alternatives=(phi@np.asarray([w['alternative'] for w in ws]).T if ws else np.empty((len(phi),0)))
            else:
                base=Expression(model['selected_expression'],len(lib.powers)).predict(phi)
                # Algebraic construction validated separately by the artifact audit;
                # use the saved normalized direction and alpha, without label access.
                alternatives=(base[:,None]+phi@np.asarray([w['alpha']*np.asarray(w['q']) for w in ws]).T
                              if ws else np.empty((len(phi),0)))
            minima=alternatives.min(axis=0) if ws else np.array([])
            base_positive=bool(base.min()>=-1e-10)
            positive=int(np.count_nonzero(minima>=-1e-10)) if base_positive else 0
            rows.append(dict(unit_id=unit['unit_id'],task=unit['task'],seed=unit['seed'],width=unit['width'],
                noise=unit['noise'],control=unit['control'],policy=unit['policy'],budget=model['budget'],
                base_minimum=float(base.min()),base_nonnegative_on_probes=base_positive,
                witnesses=len(ws),both_nonnegative_on_probes=positive,
                alternative_minima=minima.tolist()))
    # Separate condition-level counts from the number of highly correlated witnesses.
    groups=defaultdict(list)
    for row in rows:groups[(row['task'],row['control'],row['policy'],row['budget'])].append(row)
    summary=[]
    for key,records in sorted(groups.items()):
        summary.append(dict(task=key[0],control=key[1],policy=key[2],budget=key[3],conditions=len(records),
            with_witness=sum(r['witnesses']>0 for r in records),
            with_nonnegative_pair=sum(r['both_nonnegative_on_probes']>0 for r in records),
            total_witnesses=sum(r['witnesses'] for r in records),
            nonnegative_pairs=sum(r['both_nonnegative_on_probes'] for r in records)))
    save(output/'summary.json',dict(source_run=str(run),failed_units=failed,summary=summary,
        scope='Descriptive finite-public-probe positivity only; no acquisition rerun or global positivity proof.',
        tolerance=1e-10,public_probe_count=512))
    (output/'units').mkdir(exist_ok=True)
    by_unit=defaultdict(list)
    for row in rows:by_unit[row['unit_id']].append(row)
    for key,records in by_unit.items():save(output/'units'/f'{key}.json',dict(rows=records))
    print(json.dumps(dict(units=len(by_unit),models=len(rows),failed=failed)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('--output',required=True)
    a=p.parse_args();analyze(a.run,a.output)
