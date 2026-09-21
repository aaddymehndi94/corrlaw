"""Sparse greedy least-squares ensembles. Only anonymous measurements enter here."""
from dataclasses import dataclass
import numpy as np
from .features import Library

SPARSITIES = (1, 2, 3, 4, 6, 7)
MAX_TERMS = 7
MAX_COEFFICIENT = 20.
N_BOOTSTRAP = 8


def rmse(a, b):
    return float(np.sqrt(np.mean((a-b)**2)))


def tolerance(noise):
    return 0.002 + 3*noise


def sparse_path(a, y, available):
    """OMP with normalized residual correlations; retain intermediate sparsities."""
    active = []
    residual = y.copy()
    norms = np.maximum(np.linalg.norm(a, axis=0), 1e-12)
    for step in range(1, min(MAX_TERMS, len(available))+1):
        candidates = [j for j in available if j not in active]
        scores = np.abs(a[:, candidates].T @ residual) / norms[candidates]
        active.append(candidates[int(np.argmax(scores))])
        c = np.zeros(a.shape[1])
        c[active] = np.linalg.lstsq(a[:, active], y, rcond=1e-10)[0]
        residual = y - a @ c
        if step in SPARSITIES:
            c[np.abs(c) < 1e-10] = 0
            yield c


def model_errors(c, matrices, obs):
    a, cal, acquired = matrices
    train_error = rmse(a@c, obs.y)
    cal_error = rmse(cal@c, obs.calibration_y)
    acquired_max = float(np.max(np.abs(acquired@c-obs.acquired_y))) if len(acquired) else 0.
    score = train_error**2 + cal_error**2
    if len(acquired):
        score += float(np.mean((acquired@c-obs.acquired_y)**2))
    return train_error, cal_error, acquired_max, score


def admissible(c, errors, noise):
    return (np.isfinite(c).all() and np.count_nonzero(np.abs(c)>1e-10) <= MAX_TERMS
            and np.max(np.abs(c)) <= MAX_COEFFICIENT
            and max(errors[:2]) <= tolerance(noise)
            and errors[2] <= 0.002 + 4*noise)


@dataclass
class Fit:
    library: Library
    best: np.ndarray
    committee: np.ndarray
    candidates: list
    poor_fit: bool


def fit(obs, seed, diversified=False, library=None):
    lib = library or Library.build(obs.bounds, obs.probes)
    a, cal, acquired = [lib.transform(x) for x in (obs.x, obs.calibration_x, obs.acquired_x)]
    rng = np.random.default_rng(seed)
    candidates = []
    # Same base full-data candidates and number of bootstraps for both ensembles.
    for bootstrap in range(N_BOOTSTRAP+1):
        indices = np.arange(len(a)) if bootstrap == 0 else rng.integers(len(a), size=len(a))
        available = np.arange(a.shape[1])
        if diversified and bootstrap > 0:
            available = np.sort(rng.choice(available, max(7, int(0.7*len(available))), replace=False))
        for c in sparse_path(a[indices], obs.y[indices], available):
            if np.max(np.abs(c)) > MAX_COEFFICIENT:
                continue
            # Coefficient equivalence, never observational-prediction equivalence.
            if any(np.allclose(c, old['coefficients'], rtol=1e-7, atol=1e-9) for old in candidates):
                continue
            errors = model_errors(c, (a, cal, acquired), obs)
            candidates.append({'coefficients': c, 'errors': errors,
                               'terms': int(np.count_nonzero(c)),
                               'admissible': admissible(c, errors, obs.noise_std)})
    if not candidates:
        raise RuntimeError('no bounded sparse candidate')
    # Tiny fixed complexity penalty breaks equal-fit ties without a hidden target.
    best = min(candidates, key=lambda r: r['errors'][3]+1e-8*r['terms'])
    committee = [r['coefficients'] for r in candidates if r['admissible']]
    poor = not committee
    if poor:
        committee = [best['coefficients']]
    return Fit(lib, best['coefficients'], np.array(committee), candidates, poor)
