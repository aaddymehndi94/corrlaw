"""Regenerate tables and publication-style figures from saved, hashed artifacts."""
import argparse
import csv
from collections import defaultdict
import json
from pathlib import Path
import numpy as np
from .experiment import save
from .acquisition import POLICIES

LABELS={'random':'Random','qbc':'QBC','diversified_qbc':'Diversified QBC',
        'regularized_d_optimal':'D-optimal','augmented_qbc':'Augmented QBC'}


def summarize(run, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    run=Path(run); output=Path(output); output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((run/'manifest.json').read_text())
    config=json.loads((run/'config.json').read_text())
    records=[json.loads((run/r['path']).read_text()) for r in manifest['units']]
    completed=[r for r in records if r['status']=='completed']
    condition_groups=defaultdict(list)
    for r in completed:
        condition_groups[(r['task'],r['width'],r['noise'],r['control'],r['policy'])].append(r)
    with (output/'conditions.csv').open('w',newline='') as file:
        writer=csv.writer(file);writer.writerow(['task','width','noise','control','policy','seeds','auc_mean','off_rmse_q0','off_rmse_q8','same_rmse_q8'])
        for key,rs in sorted(condition_groups.items()):
            writer.writerow([*key,len(rs),float(np.mean([r['auc'] for r in rs])),
                             float(np.mean([r['metrics'][0]['off_rmse'] for r in rs])),
                             float(np.mean([r['metrics'][-1]['off_rmse'] for r in rs])),
                             float(np.mean([r['metrics'][-1]['same_rmse'] for r in rs]))])
    groups=defaultdict(list)
    for r in completed: groups[(r['task'],r['control'],r['policy'])].append(r)
    summaries=[]
    for (task,control,policy),rows in sorted(groups.items()):
        seeds=sorted({r['seed'] for r in rows})
        seed_auc=[float(np.mean([r['auc'] for r in rows if r['seed']==s])) for s in seeds]
        by_budget=[]
        for budget in (0,1,2,4,8):
            seed_errors=[float(np.mean([next(m['off_rmse'] for m in r['metrics'] if m['budget']==budget)
                                       for r in rows if r['seed']==s])) for s in seeds]
            ms=[next(m for m in r['metrics'] if m['budget']==budget) for r in rows]
            by_budget.append(dict(budget=budget,mean=float(np.mean(seed_errors)),
                seed_min=min(seed_errors),seed_max=max(seed_errors),
                same_rmse_mean=float(np.mean([m['same_rmse'] for m in ms])),
                false_consensus_count=sum(m['false_consensus'] for m in ms),
                witness_count=sum(m['witness_count']>0 for m in ms),
                no_discriminating_count=sum(m['diagnostic']=='no_discriminating_query_in_allowed_pool' for m in ms),
                poor_fit_count=sum(m['diagnostic']=='poor_observational_fit' for m in ms),
                rounded_recovery_count=sum(m['rounded_symbolic_recovery'] for m in ms),denominator=len(ms)))
        summaries.append(dict(task=task,control=control,policy=policy,seeds=seeds,units=len(rows),
            auc_mean=float(np.mean(seed_auc)),auc_seed_values=seed_auc,budgets=by_budget,
            runtime_mean_seconds=float(np.mean([r['runtime_seconds'] for r in rows])),
            augmentation_mean_seconds=float(np.mean([r['augmentation_seconds'] for r in rows])),
            peak_batch_rss_bytes=max(r['process_peak_rss_bytes'] for r in rows)))
    # Paired conditions first averaged within seed; only seed-level deltas enter ranges.
    paired=[]; first_query=[]
    for task in sorted({r['task'] for r in completed}):
        for comparator in POLICIES[:-1]:
            delta=defaultdict(list); agreements=[]
            for a in completed:
                if a['task']!=task or a['control']!='constrained' or a['policy']!='augmented_qbc':continue
                match=next((b for b in completed if b['task']==task and b['seed']==a['seed'] and
                            b['width']==a['width'] and b['noise']==a['noise'] and
                            b['control']==a['control'] and b['policy']==comparator),None)
                if match:
                    delta[a['seed']].append(a['auc']-match['auc'])
                    agreements.append(a['queries'][0]['query_id']==match['queries'][0]['query_id'])
            values=[float(np.mean(v)) for s,v in sorted(delta.items())]
            if values:
                paired.append(dict(task=task,comparator=comparator,seed_deltas=values,
                    mean_delta=float(np.mean(values)),min_delta=min(values),max_delta=max(values),
                    negative_seeds=sum(v < -1e-10 for v in values),n_seeds=len(values)))
                first_query.append(dict(task=task,comparator=comparator,matches=sum(agreements),pairs=len(agreements)))
    result=dict(source_run=str(run),units=len(records),failed=[r['unit_id'] for r in records if r['status']!='completed'],
                summaries=summaries,paired_auc_deltas=paired,first_query_agreement=first_query)
    if config.get('engine')!='finite_library':
        result.update(engine=config.get('engine'),search_settings=config.get('search_settings'),
                      prior=config.get('prior'),expected_units=manifest['expected_units'],
                      incomplete=len(records)!=manifest['expected_units'])
    save(output/'summary.json',result)
    lines=['| Task | Control | Policy | AUC | Error at 8 | Seeds |','|---|---|---|---:|---:|---:|']
    for r in summaries:
        lines.append(f'| {r["task"]} | {r["control"]} | {LABELS[r["policy"]]} | {r["auc_mean"]:.6g} | {r["budgets"][-1]["mean"]:.6g} | {len(r["seeds"])} |')
    (output/'tables.md').write_text('\n'.join(lines)+'\n')
    tasks=sorted({r['task'] for r in completed}); cols=2; rows=(len(tasks)+1)//2
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','svg.hashsalt':'corrlaw-v1'})
    fig,axes=plt.subplots(rows,cols,figsize=(11,3.7*rows),squeeze=False,layout='constrained')
    colors=['#757575','#0072B2','#009E73','#E69F00','#CC79A7']
    for ax,task in zip(axes.flat,tasks):
        for policy,color in zip(POLICIES,colors):
            r=next(s for s in summaries if s['task']==task and s['control']=='constrained' and s['policy']==policy)
            x=[m['budget'] for m in r['budgets']]; y=np.maximum([m['mean'] for m in r['budgets']],1e-10)
            low=np.maximum([m['seed_min'] for m in r['budgets']],1e-10); high=np.maximum([m['seed_max'] for m in r['budgets']],1e-10)
            ax.plot(x,y,'o-',color=color,label=LABELS[policy],lw=1.7,ms=4)
            ax.fill_between(x,low,high,color=color,alpha=.08)
        ax.set(title=f'Task {task}',xlabel='Additional measurements',ylabel='Off-preparation NRMSE')
        ax.set_yscale('log'); ax.set_xticks([0,1,2,4,8]); ax.grid(alpha=.2)
    for ax in list(axes.flat)[len(tasks):]: ax.set_visible(False)
    handles,labels=axes.flat[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=5,frameon=False)
    title='Constrained preparations · means across conditions; shading is seed range'
    if config.get('engine')=='pysr_feature_grammar':
        title=f"PySR feature grammar · {config['search_settings']['niterations']} iterations per search\n"+title
    elif config.get('engine')=='finite_library_prior_control':
        label={'none':'No additional prior','zero_origin':'Known zero at origin',
               'zero_origin_and_even':'Known zero at origin + coordinate symmetry'}[config['prior']]
        title=label+'\n'+title
    fig.suptitle(title,fontsize=12)
    svg = output/'error_curves.svg'
    fig.savefig(svg,bbox_inches='tight',metadata={'Date': None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(output/'error_curves.png',dpi=160,bbox_inches='tight'); plt.close(fig)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('run');parser.add_argument('--output',required=True)
    args=parser.parse_args();result=summarize(args.run,args.output)
    print(json.dumps(dict(units=result['units'],failures=len(result['failed'])),indent=2))

if __name__=='__main__': main()
