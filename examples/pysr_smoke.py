"""Real bounded optional-engine smoke; complete setup must finish within lab timeout."""
import json
import os
from pathlib import Path
import time

root = Path(__file__).resolve().parents[1]
os.environ['JULIA_DEPOT_PATH'] = str(root/'.julia')
os.environ['PYTHON_JULIAPKG_PROJECT'] = str(root/'.venv/julia_project')
os.environ['PYTHON_JULIACALL_THREADS'] = '1'
os.environ['JULIA_NUM_THREADS'] = '1'
os.environ['JULIA_NUM_GC_THREADS'] = '1'
os.environ['JULIA_NUM_PRECOMPILE_TASKS'] = '1'
started = time.perf_counter()
import numpy as np
import pysr
from pysr import PySRRegressor
from pysr.julia_import import jl_version

out = Path(os.environ['CORRLAW_RESULT_DIR'])
rng = np.random.default_rng(800)
x = rng.uniform(.5,1.5,(64,2)); y = x[:,0]*x[:,1]
model = PySRRegressor(niterations=5, populations=2, population_size=20,
    binary_operators=['+','-','*','/'], unary_operators=[], maxsize=10,
    parallelism='serial', deterministic=True, random_state=800,
    timeout_in_seconds=60, progress=False, verbosity=0,
    output_directory=os.environ['CORRLAW_WORK_DIR'])
model.fit(x,y)
records=model.equations_[['complexity','loss','equation']].to_dict(orient='records')
(out/'pysr.json').write_text(json.dumps(dict(pysr=pysr.__version__, julia=jl_version,
    elapsed_seconds=time.perf_counter()-started,equations=records,
    rmse=float(np.sqrt(np.mean((model.predict(x)-y)**2)))),indent=2)+'\n')
print('PySR smoke complete',flush=True)
