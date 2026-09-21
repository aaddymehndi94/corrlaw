"""Reconstruct scientific evidence without trusting successful search exits."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import numpy as np
from . import symbolic
from .features import Library
from .oracle import make_trial
from .experiment import save,digest,array_digest,units
from .symbolic_experiment import run_policy,scientific_content,evaluate,rounded_recovery
from .evaluation import auc


def inspect_run(path):
    path=Path(path);c=json.loads((path/'config.json').read_text())
    manifest=json.loads((path/'manifest.json').read_text())
    expected={r[0] for r in units(c)};actual={r['unit_id'] for r in manifest['units']}
    issues=[];groups=defaultdict(list);failed=[];completed=witnesses=equations=0
    if expected!=actual or len(actual)!=len(manifest['units']):
        issues.append('missing, unexpected or duplicate units')
    for row in manifest['units']:
        file=path/row['path'];u=json.loads(file.read_text());key=u['unit_id']
        def check(condition,message):
            if not condition:issues.append(f'{key}: {message}')
        check(hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256'],'file hash')
        check(digest(scientific_content(u))==row['scientific_sha256'],'science hash')
        check(u['config_hash']==digest(c),'configuration hash')
        if u['status']!='completed':
            failed.append(key);continue
        completed+=1
        trial=make_trial(u['task'],u['seed'],u['width'],u['noise'],u['control'],c)
        check(u['initial_data_hash']==array_digest(trial.fit_x,trial.fit_y,trial.cal_x,trial.cal_y,trial.pool,trial.probes),'initial data hash')
        check(u['evaluation_hash']==array_digest(trial.test_x,trial.same_x),'evaluation hash')
        groups[(u['task'],u['seed'],u['width'],u['noise'],u['control'])].append(u)
        ids=[r['query_id'] for r in u['queries']]
        check(len(ids)==8 and len(set(ids))==8,'query accounting')
        oracle=trial.oracle()
        for record in u['queries']:
            check(oracle.measure(record['query_id'])==record['label'],'query label')
            check(record['x']==trial.pool[record['query_id']].tolist(),'query coordinates')
            check(record['noise_realization_id']==oracle.records[-1]['noise_realization_id'],'query noise stream')
        check([m['budget'] for m in u['models']]==list(range(9)),'model budgets')
        check([m['budget'] for m in u['metrics']]==c['query_budgets'],'metric budgets')
        check(auc(u['metrics'])==u['auc'],'AUC')
        for model in u['models']:
            budget=model['budget'];obs=trial.observations(u['queries'][:budget])
            lib=Library([tuple(p) for p in model['powers']],np.asarray(model['scale']))
            rebuilt=Library.build(obs.bounds,obs.probes)
            check(lib.powers==rebuilt.powers and np.array_equal(lib.scale,rebuilt.scale),'feature dictionary')
            p=len(lib.powers)
            matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
            base=symbolic.Expression(model['selected_expression'],p)
            committee=[symbolic.Expression(s,p) for s in model['committee']]
            candidates=model['candidates']
            by_expression={r['expression']:r for r in candidates}
            for record in candidates:
                expression=symbolic.Expression(record['expression'],p)
                error=symbolic.errors(expression,matrices,obs)
                check(np.allclose(error,record['errors'],rtol=1e-12,atol=1e-12),'candidate errors')
                check(record['admissible']==symbolic.admissible(expression,error,obs.noise_std,c['search_settings']['max_complexity']),'candidate admissibility')
                check(expression.bounded(c['search_settings']['max_complexity']),'candidate complexity/coefficient cap')
                equations+=1
            full=[r for r in candidates if r['search']==0]
            selected=min(full,key=lambda r:r['errors'][3]+1e-8*r['complexity'])
            check(selected['expression']==model['selected_expression'],'common point-model selection')
            check(base.physical_expression(lib)==model['physical_expression'],'physical expression')
            plausible=[r['expression'] for r in candidates if r['admissible']]
            check(model['search_committee']==(plausible or [base.expression]),'search committee')
            ordinary=[symbolic.Expression(s,p) for s in model['search_committee']]
            fitted=symbolic.SymbolicFit(lib,base,ordinary,candidates,model['searches'],not plausible)
            for search in model['searches']:
                ix=np.asarray(search['bootstrap_indices']);n=c['n_fit']
                check(len(ix)==n+budget and np.all(ix[:n]>=0) and np.all(ix[:n]<n),'bootstrap original rows')
                check(np.array_equal(ix[n:],np.arange(n,n+budget)),'acquired rows retained')
                weight=np.ones(n+budget)
                if budget:weight[n:]=n/budget
                check(np.array_equal(weight,search['weights']),'acquisition fitness weights')
                columns=search['columns']
                check(len(set(columns))==len(columns) and all(0<=i<p for i in columns),'search feature subset')
                if search['repetition']==0:
                    check(np.array_equal(ix,np.arange(n+budget)) and columns==list(range(p)),'common full-data search')
            for witness in model['witnesses']:
                q=np.asarray(witness['q']);probes=lib.transform(obs.probes)
                check(np.isclose(np.sqrt(np.mean((probes@q)**2)),1,rtol=1e-10),'witness normalization')
                ratio=float(np.sqrt(np.mean((np.concatenate(matrices[:2])@q)**2)))
                check(ratio<=.1+1e-12 and np.isclose(ratio,witness['ratio'],atol=1e-12),'witness residual ratio')
                check(np.count_nonzero(q)<=3 and np.max(np.abs(q))<=20,'sparse witness cap')
                check(witness['base']==base.expression,'witness base identity')
                alt=symbolic.Expression(witness['alternative'],p)
                for expression in (base,alt):
                    check(symbolic.admissible(expression,symbolic.errors(expression,matrices,obs),obs.noise_std,c['search_settings']['max_complexity']),'witness admissibility')
                phi=lib.transform(obs.pool);difference=alt.predict(phi)-base.predict(phi)
                check(np.allclose(difference,witness['alpha']*(phi@q),rtol=1e-10,atol=1e-10),'alternative construction')
                location=int(np.argmax(np.abs(difference)))
                check(location==witness['disagreement_query_id'],'witness disagreement location')
                check(np.isclose(abs(difference[location]),witness['max_pool_difference'],atol=1e-12),'witness disagreement value')
                witnesses+=1
            expected_committee=model['search_committee']+([w['alternative'] for w in model['witnesses']] if u['policy']=='augmented_qbc' else [])
            check(model['committee']==expected_committee,'acquisition committee')
            if budget<8:
                choice,score=symbolic.select(u['policy'],obs,fitted,committee,ids[:budget],[u['seed'],1402,budget])
                check(choice==ids[budget],'acquisition choice')
                check(np.isclose(score,u['queries'][budget]['acquisition_score'],rtol=1e-12,atol=1e-12),'acquisition score')
            if budget in c['query_budgets']:
                saved=next(m for m in u['metrics'] if m['budget']==budget)
                for name,value in evaluate(trial,fitted,committee).items():
                    check(np.isclose(value,saved[name],rtol=1e-12,atol=1e-12),f'{name} metric')
                check(saved['total_labels']==c['n_fit']+c['n_calibration']+budget,'total label count')
                check(saved['rounded_symbolic_recovery']==rounded_recovery(trial.task,base,lib),'rounded recovery')
                check(saved['witness_count']==len(model['witnesses']),'witness count')
    for group,rows in groups.items():
        if {r['policy'] for r in rows}!=set(c['policies']):issues.append(f'{group}: missing policy')
        if len({r['models'][0]['selected_expression'] for r in rows})!=1:issues.append(f'{group}: unpaired initial estimator')
    return dict(valid=not issues and not failed,expected_units=len(expected),completed_units=completed,
                failed_units=failed,witnesses_checked=witnesses,candidates_checked=equations,errors=issues)


def reproduce(path,unit_id,output):
    path=Path(path);c=json.loads((path/'config.json').read_text())
    original=json.loads((path/'units'/f'{unit_id}.json').read_text())
    trial=make_trial(original['task'],original['seed'],original['width'],original['noise'],original['control'],c)
    repeated=run_policy(trial,original['policy'],c)
    old=scientific_content({k:original[k] for k in scientific_content(repeated)})
    new=scientific_content(repeated)
    exact=digest(old)==digest(new)
    save(Path(output)/'repeated.json',repeated)
    save(Path(output)/'reproduction.json',dict(parent=str(path),unit_id=unit_id,exact_match=exact,
         original_scientific_sha256=digest(old),repeated_scientific_sha256=digest(new)))
    return exact


def main():
    parser=argparse.ArgumentParser();parser.add_argument('run');parser.add_argument('--output',required=True)
    parser.add_argument('--reproduce');args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    if args.reproduce:valid=reproduce(args.run,args.reproduce,out)
    else:
        result=inspect_run(args.run);save(out/'validation.json',result);print(json.dumps(result,indent=2));valid=result['valid']
    raise SystemExit(not valid)


if __name__=='__main__':main()
