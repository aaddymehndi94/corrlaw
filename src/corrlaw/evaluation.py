"""Hidden-label evaluation; never imported by a learner or acquisition module."""
import numpy as np
from .oracle import reference
from .discovery import rmse
from .acquisition import disagreement


def evaluate(trial, fitted, committee):
    lib = fitted.library
    off = lib.transform(trial.test_x)
    same = lib.transform(trial.same_x)
    error = rmse(off@fitted.best, reference(trial.task, trial.test_x))
    spread = float(np.sqrt(np.mean(disagreement(off, committee))))
    return {'off_rmse': error, 'same_rmse': rmse(same@fitted.best, reference(trial.task, trial.same_x)),
            'committee_rms_std': spread, 'false_consensus': bool(spread < 0.05 and error > 0.1)}


def symbolic_recovery(task, lib, coefficients):
    import sympy as sp
    u, v = sp.symbols('x0 x1')
    ref = {'A': u*v, 'B': u*u+2*v*v, 'C': u*u/v, 'D': u*v*v,
           'E': u+v, 'F': u*v/(u+v)}[task]
    # Explicit rounded-coefficient diagnostic, not proof about the unrounded fit.
    return bool(sp.cancel(lib.symbolic(coefficients)-ref) == 0)


def auc(metrics):
    x = np.array([r['budget'] for r in metrics], float)
    y = np.array([r['off_rmse'] for r in metrics])
    return float(np.trapezoid(y, x) / (x[-1]-x[0]))
