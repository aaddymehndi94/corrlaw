"""Preregistered optional engine check; not an acquisition-policy benchmark."""
import os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
os.environ['JULIA_DEPOT_PATH']=str(root/'.julia')
os.environ['PYTHON_JULIAPKG_PROJECT']=str(root/'.venv/julia_project')
os.environ['PYTHON_JULIACALL_THREADS']='1'
os.environ['JULIA_NUM_GC_THREADS']='1'
os.environ['JULIA_NUM_PRECOMPILE_TASKS']='1'
import json
import time
import numpy as np
from pysr import PySRRegressor
from pysr.julia_import import jl_version
from corrlaw.oracle import make_trial, reference
from corrlaw.experiment import load_config, save
from corrlaw.discovery import fit

out=Path(os.environ['CORRLAW_RESULT_DIR'])
c=load_config(root/'configs/pilot.json')
records=[]
for task in ('A','B'):
    for seed in (101,102,103):
        t=make_trial(task,seed,0,0,'constrained',c);start=time.perf_counter()
        model=PySRRegressor(niterations=10,populations=2,population_size=20,
            binary_operators=['+','-','*','/'],unary_operators=[],maxsize=10,
            parallelism='serial',deterministic=True,random_state=seed,
            timeout_in_seconds=60,progress=False,verbosity=0,
            output_directory=os.environ['CORRLAW_WORK_DIR'])
        model.fit(t.fit_x,t.fit_y)
        candidates=[]
        for index,row in model.equations_.iterrows():
            try:
                pred=model.predict(t.cal_x,index=index)
                cal=float(np.sqrt(np.mean((pred-t.cal_y)**2)))
                if not np.isfinite(cal):continue
                candidates.append(dict(index=int(index),equation=row['equation'],
                                       complexity=int(row['complexity']),loss=float(row['loss']),cal_rmse=cal))
            except (ValueError,TypeError,FloatingPointError):continue
        best=min(candidates,key=lambda r:r['cal_rmse']**2+1e-8*r['complexity'])
        off=float(np.sqrt(np.mean((model.predict(t.test_x,index=best['index'])-reference(task,t.test_x))**2)))
        fitted=fit(t.observations([]),np.random.SeedSequence([seed,400,0]))
        baseline_off=float(np.sqrt(np.mean((fitted.library.transform(t.test_x)@fitted.best-reference(task,t.test_x))**2)))
        records.append(dict(task=task,seed=seed,selected=best,candidates=candidates,
                            pysr_off_rmse=off,finite_library_off_rmse=baseline_off,
                            elapsed_seconds=time.perf_counter()-start))
        save(out/'comparison.json',dict(julia=jl_version,records=records,
            scope='A/B exact noiseless initial preparation; three search seeds; no acquisition comparison',
            parameters=dict(niterations=10,populations=2,population_size=20,maxsize=10,timeout_in_seconds=60,operators=['+','-','*','/'])))
        print(task,seed,off,flush=True)
