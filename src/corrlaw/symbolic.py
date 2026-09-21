"""Numerical-only PySR ensembles over a generic dimensionless feature grammar.

No task names, preparation formulas, oracle imports or hidden labels enter here.
Julia is imported lazily so algebra tests do not start the search runtime.
"""
from dataclasses import dataclass
from itertools import combinations
import os
from pathlib import Path
import time
import numpy as np
import sympy as sp
from .features import Library
from .discovery import rmse, tolerance
from .acquisition import leverage


def configure_julia():
    root = Path(__file__).resolve().parents[2]
    os.environ['JULIA_DEPOT_PATH'] = str(root/'.julia')
    os.environ['PYTHON_JULIAPKG_PROJECT'] = str(root/'.venv/julia_project')
    for name in ('PYTHON_JULIACALL_THREADS', 'JULIA_NUM_GC_THREADS',
                 'JULIA_NUM_PRECOMPILE_TASKS'):
        os.environ[name] = '1'


@dataclass
class Expression:
    expression: str
    n_features: int

    def __post_init__(self):
        self.symbols = sp.symbols(f'z0:{self.n_features}')
        self.symbolic = sp.sympify(self.expression, locals={str(z): z for z in self.symbols})
        if not self.symbolic.free_symbols.issubset(set(self.symbols)):
            raise ValueError('unknown expression variable')
        self.function = sp.lambdify(self.symbols, self.symbolic, 'numpy', cse=True)

    def predict(self, phi):
        with np.errstate(all='ignore'):
            result = np.asarray(self.function(*phi.T))
        if np.iscomplexobj(result):
            raise ValueError('complex predictions')
        result = np.broadcast_to(result, (len(phi),)).astype(float).copy()
        if not np.isfinite(result).all():
            raise ValueError('nonfinite predictions')
        return result

    @property
    def complexity(self):
        return sum(1 for _ in sp.preorder_traversal(self.symbolic))

    def bounded(self, max_complexity):
        return (self.complexity <= max_complexity and
                all(abs(float(n)) <= 20 for n in self.symbolic.atoms(sp.Number)))

    def physical_expression(self, lib):
        x0, x1 = sp.symbols('x0 x1')
        substitutions = {z: x0**a*x1**b/sp.Float(float(scale), 17)
                         for z, (a, b), scale in zip(self.symbols, lib.powers, lib.scale)}
        return str(self.symbolic.xreplace(substitutions))


def errors(model, matrices, obs):
    train, cal, acquired = [model.predict(a) for a in matrices]
    fit_rmse, cal_rmse = rmse(train, obs.y), rmse(cal, obs.calibration_y)
    acquired_max = float(np.max(np.abs(acquired-obs.acquired_y))) if len(acquired) else 0.
    score = fit_rmse**2 + cal_rmse**2
    if len(acquired):
        score += float(np.mean((acquired-obs.acquired_y)**2))
    return [fit_rmse, cal_rmse, acquired_max, score]


def admissible(model, error, noise, max_complexity):
    return (model.bounded(max_complexity) and max(error[:2]) <= tolerance(noise)
            and error[2] <= .002+4*noise)


@dataclass
class SymbolicFit:
    library: Library
    best: Expression
    committee: list
    candidates: list
    searches: list
    poor_fit: bool


def fit(obs, seed, settings, diversified=False, history=(), generation=0):
    configure_julia()
    from pysr import PySRRegressor
    lib = Library.build(obs.bounds, obs.probes)
    matrices = [lib.transform(x) for x in (obs.x, obs.calibration_x, obs.acquired_x)]
    domain = np.concatenate((lib.transform(obs.pool), lib.transform(obs.probes)))
    a = matrices[0]
    n_initial = len(obs.x)-len(obs.acquired_x)
    streams = np.random.SeedSequence(seed).spawn(settings['searches'])
    candidates, searches, full_candidates = [], [], []
    # Preserve discovered equations, but recompute every admissibility decision
    # against all currently available observations. Never preserve old scores.
    for old in history:
        candidate = Expression(old['expression'], a.shape[1])
        try:
            error = errors(candidate, matrices, obs)
            candidate.predict(domain)
        except (ValueError, FloatingPointError, OverflowError):
            continue
        record = dict(old, errors=error,
                      admissible=admissible(candidate,error,obs.noise_std,settings['max_complexity']))
        if record['search']==0:
            full_candidates.append(record)
        candidates.append(record)
    for repetition, stream in enumerate(streams):
        rng = np.random.default_rng(stream)
        indices = (np.arange(n_initial) if repetition == 0 else
                   rng.integers(n_initial, size=n_initial))
        indices = np.concatenate((indices, np.arange(n_initial, len(a))))
        columns = np.arange(a.shape[1])
        if diversified and repetition:
            columns = np.sort(rng.choice(columns, max(7, int(.7*len(columns))), replace=False))
        search_seed = int(rng.integers(1, 2**31-1))
        weights = np.ones(len(indices))
        if len(obs.acquired_x):
            weights[n_initial:] = n_initial/len(obs.acquired_x)
        start = time.perf_counter()
        model = PySRRegressor(
            niterations=settings['niterations'], populations=2, population_size=20,
            binary_operators=['+', '-', '*', '/'], unary_operators=[],
            maxsize=settings['search_maxsize'], precision=64,
            parallelism='serial', deterministic=True, random_state=search_seed,
            timeout_in_seconds=settings['timeout_seconds'], progress=False, verbosity=0,
            output_directory=os.environ.get('CORRLAW_WORK_DIR', str(Path.cwd()/'work/pysr')),
        )
        model.fit(a[indices][:, columns], obs.y[indices], weights=weights,
                  variable_names=[f'z{i}' for i in columns])
        raw = []
        for index, row in model.equations_.iterrows():
            expression = str(row['sympy_format'])
            record = dict(expression=expression, search=repetition, generation=generation,index=int(index),
                          search_complexity=int(row['complexity']), search_loss=float(row['loss']))
            try:
                candidate = Expression(expression, a.shape[1])
                error = errors(candidate, matrices, obs)
                candidate.predict(domain)
                record.update(errors=error, complexity=candidate.complexity,
                              bounded=candidate.bounded(settings['max_complexity']),
                              admissible=admissible(candidate, error, obs.noise_std,
                                                    settings['max_complexity']))
                if record['bounded']:
                    if repetition == 0:
                        full_candidates.append(record)
                    duplicate=next((r for r in candidates if r['expression']==expression),None)
                    if duplicate is None:
                        candidates.append(record)
                    elif repetition==0 and duplicate['search']!=0:
                        # Full-data eligibility must survive expression deduplication.
                        candidates[candidates.index(duplicate)]=record
            except (ValueError, TypeError, FloatingPointError, OverflowError) as exc:
                record.update(rejected=str(exc), admissible=False)
            raw.append(record)
        searches.append(dict(repetition=repetition, seed=search_seed,
                             columns=columns.tolist(), bootstrap_indices=indices.tolist(),
                             weights=weights.tolist(), equations=raw,
                             runtime_seconds=time.perf_counter()-start))
    if not full_candidates:
        raise RuntimeError('no bounded full-data PySR candidate')
    # Rank the persisted candidate set itself; lexical ties are independent of
    # whether an equation first appeared in a bootstrap or full-data search.
    full_candidates=[r for r in candidates if r['search']==0]
    selected = min(full_candidates, key=lambda r: (r['errors'][3]+1e-8*r['complexity'],r['expression']))
    best = Expression(selected['expression'], a.shape[1])
    committee = [Expression(r['expression'], a.shape[1]) for r in candidates if r['admissible']]
    return SymbolicFit(lib, best, committee or [best], candidates, searches, not committee)


def augment(obs, fitted, settings):
    lib = fitted.library
    matrices = [lib.transform(x) for x in (obs.x, obs.calibration_x, obs.acquired_x)]
    probes, pool = lib.transform(obs.probes), lib.transform(obs.pool)
    observed = np.concatenate(matrices[:2])
    gram = observed.T@observed/len(observed)
    proposals = []
    for size in (2, 3):
        subsets = np.array(list(combinations(range(gram.shape[0]), size)))
        _, vectors = np.linalg.eigh(gram[subsets[:, :, None], subsets[:, None, :]])
        for subset, vector in zip(subsets, vectors[:, :, 0]):
            q = np.zeros(gram.shape[0]); q[subset] = vector
            norm = float(np.sqrt(np.mean((probes@q)**2)))
            if norm < 1e-8:
                continue
            q /= norm
            if q[np.argmax(np.abs(q))] < 0:
                q *= -1
            ratio = float(np.sqrt(np.mean((observed@q)**2)))
            if ratio <= .1 and np.max(np.abs(q)) <= 20:
                proposals.append((ratio, tuple(subset), q))
    proposals.sort(key=lambda r: (r[0], r[1]))
    base_error = errors(fitted.best, matrices, obs)
    valid = admissible(fitted.best, base_error, obs.noise_std, settings['max_complexity'])
    accepted, alternatives, directions = [], [], []
    if valid:
        base_predictions=[fitted.best.predict(a) for a in matrices]
        for ratio, subset, q in proposals:
            if any(np.allclose(q, old, rtol=1e-6, atol=1e-7) for old in directions):
                continue
            used = False
            q_predictions=[a@q for a in matrices]
            q_expr=None
            for alpha in (-1., -.25, .25, 1.):
                # Cheap conservative rejection before symbolic construction.
                # Final acceptance and saved errors still use the serialized
                # expression with the original tolerances, without this slack.
                predicted=[base+alpha*delta for base,delta in zip(base_predictions,q_predictions)]
                if (rmse(predicted[0],obs.y)>tolerance(obs.noise_std)+1e-9 or
                    rmse(predicted[1],obs.calibration_y)>tolerance(obs.noise_std)+1e-9 or
                    (len(predicted[2]) and np.max(abs(predicted[2]-obs.acquired_y))>.002+4*obs.noise_std+1e-9)):
                    continue
                # Keep 17-digit coefficients in the persisted symbolic contract.
                if q_expr is None:
                    q_expr = sum(sp.Float(float(v), 17)*z for v, z in zip(q, fitted.best.symbols))
                alt = Expression(str(fitted.best.symbolic+sp.Float(alpha, 17)*q_expr), len(q))
                try:
                    error = errors(alt, matrices, obs)
                    if not admissible(alt, error, obs.noise_std, settings['max_complexity']):
                        continue
                    difference = alt.predict(pool)-fitted.best.predict(pool)
                    alt.predict(probes)
                except (ValueError, FloatingPointError, OverflowError):
                    continue
                location = int(np.argmax(np.abs(difference)))
                accepted.append(dict(base=fitted.best.expression, alternative=alt.expression,
                    q=q.tolist(), alpha=alpha, ratio=ratio, base_errors=base_error,
                    errors=error, complexity=alt.complexity,
                    base_expression=fitted.best.physical_expression(lib),
                    alternative_expression=alt.physical_expression(lib),
                    max_pool_difference=float(abs(difference[location])),
                    disagreement_query_id=location))
                alternatives.append(alt); used = True
            if used:
                directions.append(q)
            if len(directions) >= 12:
                break
    if not valid:
        diagnostic = 'poor_observational_fit'
    elif accepted and max(w['max_pool_difference'] for w in accepted) <= 1e-6:
        diagnostic = 'no_discriminating_query_in_allowed_pool'
    else:
        diagnostic = 'ambiguity_witness_found' if accepted else 'no_witness_within_search_budget'
    return fitted.committee+alternatives, accepted, diagnostic


def predictions(committee, phi):
    return np.column_stack([model.predict(phi) for model in committee])


def select(policy, obs, fitted, committee, seen, seed):
    rng = np.random.default_rng(seed)
    phi = fitted.library.transform(obs.pool)
    if policy == 'random':
        scores = rng.random(len(phi))
    elif policy == 'regularized_d_optimal':
        measured = fitted.library.transform(np.concatenate((obs.x, obs.calibration_x)))
        scores = leverage(measured, phi)
    else:
        scores = np.var(predictions(committee, phi), axis=1)
    scores[np.asarray(seen, dtype=int)] = -np.inf
    maximum = float(np.max(scores))
    if not np.isfinite(maximum):
        raise ValueError('no finite query score')
    tied = np.flatnonzero(np.isclose(scores, maximum, rtol=1e-10, atol=1e-14))
    choice = int(rng.choice(tied))
    return choice, float(scores[choice])
