"""Label-free acquisition functions with reproducible tie breaking."""
import numpy as np
from scipy.linalg import solve_triangular

POLICIES = ('random', 'qbc', 'diversified_qbc', 'regularized_d_optimal', 'augmented_qbc')


def disagreement(phi, committee):
    return np.var(phi @ committee.T, axis=1)


def leverage(observed, candidates, ridge=1e-4):
    info = observed.T @ observed + ridge*np.eye(observed.shape[1])
    lower = np.linalg.cholesky(info)
    solved = solve_triangular(lower, candidates.T, lower=True)
    return np.sum(solved*solved, axis=0)


def select(policy, obs, fitted, committee, seen, seed):
    if policy not in POLICIES:
        raise ValueError('unknown policy')
    rng = np.random.default_rng(seed)
    phi = fitted.library.transform(obs.pool)
    if policy == 'random':
        scores = rng.random(len(phi))
    elif policy == 'regularized_d_optimal':
        measured = fitted.library.transform(np.concatenate((obs.x, obs.calibration_x)))
        scores = leverage(measured, phi)
    else:
        scores = disagreement(phi, committee)
    scores[np.array(list(seen), dtype=int)] = -np.inf
    maximum = np.max(scores)
    if not np.isfinite(maximum):
        raise ValueError('empty query pool')
    tied = np.flatnonzero(np.isclose(scores, maximum, rtol=1e-10, atol=1e-14))
    choice = int(rng.choice(tied))
    return choice, float(scores[choice])
