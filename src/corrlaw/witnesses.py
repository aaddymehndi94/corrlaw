"""Sparse empirical ambiguity witnesses from input geometry, not oracle formulas."""
from itertools import combinations
import numpy as np
from .discovery import admissible, model_errors


def augment(obs, fitted):
    lib = fitted.library
    a, cal, acquired, probes = [lib.transform(x) for x in
                               (obs.x, obs.calibration_x, obs.acquired_x, obs.probes)]
    all_a = np.concatenate((a, cal))
    gram = all_a.T @ all_a / len(all_a)
    proposals = []
    for size in (2, 3):
        subsets = np.array(list(combinations(range(a.shape[1]), size)))
        grams = gram[subsets[:, :, None], subsets[:, None, :]]
        _, vectors = np.linalg.eigh(grams)
        for subset, vector in zip(subsets, vectors[:, :, 0]):
            q = np.zeros(a.shape[1]); q[subset] = vector
            norm = np.sqrt(np.mean((probes@q)**2))
            if norm < 1e-8:
                continue
            q /= norm
            if q[np.argmax(np.abs(q))] < 0:
                q *= -1
            ratio = float(np.sqrt(np.mean((all_a@q)**2)))
            if ratio <= 0.1 and np.max(np.abs(q)) <= 20:
                proposals.append((ratio, tuple(subset), q))
    proposals.sort(key=lambda p: (p[0], p[1]))
    accepted = []; alternatives = []; directions = []
    base_errors = model_errors(fitted.best, (a, cal, acquired), obs)
    base_valid = admissible(fitted.best, base_errors, obs.noise_std)
    if not fitted.poor_fit and base_valid:
        for ratio, subset, q in proposals:
            if any(np.allclose(q, old, rtol=1e-6, atol=1e-7) for old in directions):
                continue
            any_accepted = False
            for alpha in (-1., -0.25, 0.25, 1.):
                c = fitted.best + alpha*q
                c[np.abs(c)<1e-10] = 0
                errors = model_errors(c, (a, cal, acquired), obs)
                if admissible(c, errors, obs.noise_std):
                    pool_difference = lib.transform(obs.pool)@(c-fitted.best)
                    loc = int(np.argmax(np.abs(pool_difference)))
                    accepted.append({'base': fitted.best.tolist(), 'alternative': c.tolist(),
                                     'q': q.tolist(), 'alpha': alpha, 'ratio': ratio,
                                     'base_expression': lib.expression(fitted.best),
                                     'alternative_expression': lib.expression(c),
                                     'q_expression': lib.expression(q),
                                     'errors': list(errors),
                                     'terms': int(np.count_nonzero(c)),
                                     'max_pool_difference': float(abs(pool_difference[loc])),
                                     'disagreement_query_id': loc})
                    alternatives.append(c); any_accepted = True
            if any_accepted:
                directions.append(q)
            if len(directions) == 12:
                break
    committee = np.concatenate((fitted.committee, np.array(alternatives))) if alternatives else fitted.committee
    if fitted.poor_fit or not base_valid:
        status = 'poor_observational_fit'
    elif accepted and max(w['max_pool_difference'] for w in accepted) <= 1e-6:
        status = 'no_discriminating_query_in_allowed_pool'
    else:
        status = 'ambiguity_witness_found' if accepted else 'no_witness_within_search_budget'
    return committee, accepted, status
