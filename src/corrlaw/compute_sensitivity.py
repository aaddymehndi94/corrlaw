"""Compare only paired conditions across predeclared PySR search budgets."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import numpy as np
from corrlaw.experiment import save,units


def load(run):
    run=Path(run);c=json.loads((run/'config.json').read_text());m=json.loads((run/'manifest.json').read_text())
    expected={r[0] for r in units(c)}
    if len(m['units'])!=len(expected) or {r['unit_id'] for r in m['units']}!=expected:
        raise ValueError('incomplete or duplicate input manifest')
    result={}
    for entry in m['units']:
        p=run/entry['path']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('unit hash mismatch')
        u=json.loads(p.read_text())
        if u['status']!='completed':raise ValueError('input contains failures')
        result[u['unit_id']]=u
    return c,result


def compare(primary,strong,output):
    c1,old=load(primary);c2,new=load(strong)
    for field in ('engine','n_fit','n_calibration','n_query_candidates','n_test','query_budgets','policies'):
        if c1[field]!=c2[field]:raise ValueError(f'unpaired {field}')
    if c1['search_settings']['niterations']!=30 or c2['search_settings']['niterations']!=100:
        raise ValueError('unexpected search-iteration contrast')
    for field in c1['search_settings']:
        if field!='niterations' and c1['search_settings'][field]!=c2['search_settings'][field]:
            raise ValueError(f'unpaired search setting {field}')
    rows=[]
    for key,b in sorted(new.items()):
        if key not in old:raise ValueError('secondary condition missing from primary')
        a=old[key]
        if any(a[field]!=b[field] for field in ('initial_data_hash','evaluation_hash')):
            raise ValueError('initial/evaluation data are not paired')
        rows.append(dict(unit_id=key,task=b['task'],seed=b['seed'],width=b['width'],noise=b['noise'],control=b['control'],
            policy=b['policy'],primary_auc=a['auc'],strong_auc=b['auc'],delta=b['auc']-a['auc'],
            primary_error_at8=a['metrics'][-1]['off_rmse'],strong_error_at8=b['metrics'][-1]['off_rmse']))
    groups=defaultdict(list)
    for row in rows:groups[(row['task'],row['policy'])].append(row)
    summary=[]
    for key,rs in sorted(groups.items()):
        seeds=[]
        for seed in sorted({r['seed'] for r in rs}):
            subset=[r for r in rs if r['seed']==seed]
            seeds.append(dict(seed=seed,conditions=len(subset),primary_auc=float(np.mean([r['primary_auc'] for r in subset])),
                strong_auc=float(np.mean([r['strong_auc'] for r in subset])),delta=float(np.mean([r['delta'] for r in subset]))))
        summary.append(dict(task=key[0],policy=key[1],seed_values=seeds,
            primary_auc_mean=float(np.mean([r['primary_auc'] for r in seeds])),
            strong_auc_mean=float(np.mean([r['strong_auc'] for r in seeds])),
            mean_delta=float(np.mean([r['delta'] for r in seeds]))))
    acquisition=[]
    index={(r['task'],r['seed'],r['width'],r['noise'],r['control'],r['policy']):r for r in rows}
    for task in c2['tasks']:
        for comparator in c2['policies']:
            if comparator=='augmented_qbc':continue
            by_seed=defaultdict(list)
            for key,a in index.items():
                if key[0]!=task or key[-1]!='augmented_qbc':continue
                b=index[(*key[:-1],comparator)]
                by_seed[key[1]].append((a['primary_auc']-b['primary_auc'],a['strong_auc']-b['strong_auc']))
            values=[dict(seed=seed,primary_delta=float(np.mean([r[0] for r in pairs])),strong_delta=float(np.mean([r[1] for r in pairs])))
                    for seed,pairs in sorted(by_seed.items())]
            acquisition.append(dict(task=task,comparator=comparator,seed_values=values,
                primary_mean_delta=float(np.mean([v['primary_delta'] for v in values])),
                strong_mean_delta=float(np.mean([v['strong_delta'] for v in values]))))
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    save(out/'summary.json',dict(primary_run=str(primary),strong_run=str(strong),paired_units=len(rows),
        scope='Only conditions present in both frozen tiers. Seed means; no pooling across tiers.',
        policy_summaries=summary,paired_acquisition_deltas=acquisition))
    save(out/'paired_units.json',dict(rows=rows))
    return len(rows)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('primary');p.add_argument('strong');p.add_argument('--output',required=True)
    a=p.parse_args();print(json.dumps(dict(paired_units=compare(a.primary,a.strong,a.output))))
