"""Render a saved ambiguity witness without selecting by hidden prediction error."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from corrlaw.features import Library
from corrlaw.oracle import make_trial
from corrlaw.experiment import save,digest,array_digest
from corrlaw.symbolic import Expression


def explain(run,unit_id,budget,output):
    run=Path(run);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    c=json.loads((run/'config.json').read_text());manifest=json.loads((run/'manifest.json').read_text())
    row=next(r for r in manifest['units'] if r['unit_id']==unit_id)
    path=run/row['path']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:
        raise ValueError('unit hash does not match manifest')
    unit=json.loads(path.read_text())
    if unit['status']!='completed' or unit['config_hash']!=digest(c):
        raise ValueError('incomplete unit or configuration mismatch')
    model=next(m for m in unit['models'] if m['budget']==budget)
    result=dict(source_run=str(run),unit_id=unit_id,budget=budget,diagnostic=model['diagnostic'],
                interpretation='Empirical ambiguity under the saved grammar and tolerances; not verified uniqueness.',
                witness_count=len(model['witnesses']))
    if not model['witnesses']:
        result['explanation']='No accepted witness in the saved search; this does not establish uniqueness.'
        save(output/'explanation.json',result);return result
    # A deterministic first witness, chosen before any inspection of hidden error.
    witness=model['witnesses'][0]
    trial=make_trial(unit['task'],unit['seed'],unit['width'],unit['noise'],unit['control'],c)
    if unit['initial_data_hash']!=array_digest(trial.fit_x,trial.fit_y,trial.cal_x,trial.cal_y,trial.pool,trial.probes):
        raise ValueError('data reconstruction mismatch')
    obs=trial.observations(unit['queries'][:budget])
    lib=Library([tuple(p) for p in model['powers']],np.asarray(model['scale']))
    if 'selected_coefficients' in model:
        base=lambda x:lib.transform(x)@np.asarray(witness['base'])
        alt=lambda x:lib.transform(x)@np.asarray(witness['alternative'])
    else:
        base_model=Expression(witness['base'],len(lib.powers));alt_model=Expression(witness['alternative'],len(lib.powers))
        base=lambda x:base_model.predict(lib.transform(x))
        alt=lambda x:alt_model.predict(lib.transform(x))
    base_probe=base(obs.probes);alt_probe=alt(obs.probes)
    result.update(base_minimum_on_public_probes=float(base_probe.min()),
                  alternative_minimum_on_public_probes=float(alt_probe.min()),
                  base_nonnegative_on_public_probes=bool(base_probe.min()>=-1e-10),
                  alternative_nonnegative_on_public_probes=bool(alt_probe.min()>=-1e-10),
                  positivity_note='Nonnegativity was not a supplied primary-study prior; finite probes do not prove global positivity.')
    result['observed_rmse']={name:dict(fitting=float(np.sqrt(np.mean((fn(obs.x)-obs.y)**2))),
                            calibration=float(np.sqrt(np.mean((fn(obs.calibration_x)-obs.calibration_y)**2))))
                            for name,fn in [('base',base),('alternative',alt)]}
    location=witness['disagreement_query_id']
    query=trial.pool[[location]]
    result.update(witness_index=0,base_expression=witness['base_expression'],
        alternative_expression=witness['alternative_expression'],witness_errors=witness['errors'],
        relation_observed_to_probe_ratio=witness['ratio'],alpha=witness['alpha'],
        maximum_disagreement_query=dict(query_id=location,x=query[0].tolist(),
            base_prediction=float(base(query)[0]),alternative_prediction=float(alt(query)[0])),
        actual_next_query=unit['queries'][budget] if budget<len(unit['queries']) else None,
        supplied_prior=c.get('prior','incomplete generic priors only'),
        total_measured_labels=c['n_fit']+c['n_calibration']+budget,
        selection_rule='first accepted witness, never selected by hidden prediction error')
    save(output/'explanation.json',result)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.fonttype':'none','svg.hashsalt':'corrlaw-witness-v1','font.size':10})
    b=obs.bounds
    a=np.linspace(*b[0],120);z=np.linspace(*b[1],120);xx,yy=np.meshgrid(a,z)
    grid=np.column_stack((xx.ravel(),yy.ravel()))
    try:
        first=base(grid).reshape(xx.shape);second=alt(grid).reshape(xx.shape)
    except ValueError:
        result['figure_status']='Not rendered: saved rational expression is nonfinite on the illustration grid.'
        save(output/'explanation.json',result);return result
    delta=second-first;vmin=min(first.min(),second.min());vmax=max(first.max(),second.max())
    extent=[b[0,0],b[0,1],b[1,0],b[1,1]]
    fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
    for ax,data,title in zip(axes,(first,second,delta),('Fitted equation','Accepted alternative','Alternative minus fitted')):
        if ax is axes[2]:
            limit=max(float(np.max(abs(delta))),1e-12)
            im=ax.imshow(data,origin='lower',extent=extent,aspect='equal',cmap='RdBu_r',vmin=-limit,vmax=limit)
        else:im=ax.imshow(data,origin='lower',extent=extent,aspect='equal',cmap='viridis',vmin=vmin,vmax=vmax)
        initial=np.concatenate((trial.fit_x,trial.cal_x))
        ax.scatter(initial[:,0],initial[:,1],s=4,c='white',alpha=.45,edgecolors='#666666',linewidths=.1,label='Initial measurements')
        ax.scatter(query[0,0],query[0,1],marker='*',s=130,c='#E69F00',edgecolors='black',linewidths=.6,clip_on=False,label='Largest saved-witness difference')
        if budget:
            acquired=np.array([r['x'] for r in unit['queries'][:budget]])
            ax.scatter(acquired[:,0],acquired[:,1],s=26,marker='x',c='red',label='Acquired measurements')
        ax.set(title=title,xlabel='Anonymous input x0',ylabel='Anonymous input x1')
        fig.colorbar(im,ax=ax,shrink=.78,label='Output reference units')
    fig.suptitle(f'Saved witness · {unit_id} · {budget} additional measurements',fontsize=10)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=3,frameon=False,fontsize=9)
    svg=output/'witness.svg';fig.savefig(svg,metadata={'Date':None},bbox_inches='tight')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(output/'witness.png',dpi=160,bbox_inches='tight');plt.close(fig)
    result['figure_status']='rendered';save(output/'explanation.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('--unit',required=True)
    p.add_argument('--budget',type=int,default=0);p.add_argument('--output',required=True)
    a=p.parse_args();print(json.dumps(explain(a.run,a.unit,a.budget,a.output),indent=2))
