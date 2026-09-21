"""Evaluator-only physical models, preparation sampling, and audited measurements."""
from dataclasses import dataclass
import numpy as np
from .contracts import Observations

TASKS = tuple('ABCDEF')
CONTROLS = ('constrained', 'independent_inputs', 'matched_marginal_shuffle',
            'surface_restricted_queries')


def bounds(task):
    if task not in TASKS:
        raise ValueError('unknown task')
    if task == 'B':
        return np.array([[-1.5, 1.5], [-1.5, 1.5]])
    if task == 'E':
        return np.array([[0.6, 1.4], [0.3, 2.0]])
    return np.array([[0.5, 1.5], [0.5, 1.5]])


def reference(task, x):
    b = bounds(task)
    x = np.asarray(x)
    if x.ndim != 2 or x.shape[1] != 2 or not np.isfinite(x).all():
        raise ValueError('invalid coordinates')
    if np.any(x < b[:, 0] - 1e-12) or np.any(x > b[:, 1] + 1e-12):
        raise ValueError('outside permitted physical domain')
    u, v = x.T
    return {'A': lambda: u*v, 'B': lambda: u*u+2*v*v,
            'C': lambda: u*u/v, 'D': lambda: u*v*v,
            'E': lambda: u+v, 'F': lambda: u*v/(u+v)}[task]()


def dimensional(task, first, second, scales=(1., 1.)):
    """Return dimensional ideal-model output and its physical reference scale."""
    a, b = scales
    if a <= 0 or b <= 0:
        raise ValueError('reference scales must be positive')
    if task in 'BEF' and a != b:
        raise ValueError('this model requires common input reference scales')
    if task == 'A': return first*second, a*b
    if task == 'B': return 0.5*(first**2 + 2*second**2), 0.5*a*a
    if task == 'C': return first**2/second, a*a/b
    if task == 'D': return 0.5*first*second**2, 0.5*a*b*b
    if task == 'E': return first+second, a
    if task == 'F': return first*second/(first+second), a
    raise ValueError('unknown task')


def sample(task, n, width, control, rng):
    if width not in (0, 0.01, 0.05) or control not in CONTROLS:
        raise ValueError('unsupported preparation')
    b = bounds(task)
    if control == 'independent_inputs':
        return rng.uniform(b[:, 0], b[:, 1], size=(n, 2))
    if task == 'B':
        angle = rng.uniform(0, 2*np.pi, n)
        radius = 1 + rng.uniform(-width, width, n)
        x = radius[:, None]*np.column_stack((np.cos(angle), np.sin(angle)))
    else:
        # Reject outside the declared box; no clipping-induced boundary masses.
        chunks = []
        count = 0
        while count < n:
            u = rng.uniform(*b[0], n-count)
            v = (u*u if task == 'E' else u) + rng.uniform(-width, width, len(u))
            part = np.column_stack((u, v))
            part = part[(v >= b[1, 0]) & (v <= b[1, 1])]
            chunks.append(part)
            count += len(part)
        x = np.concatenate(chunks)
    if control == 'matched_marginal_shuffle':
        x[:, 1] = rng.permutation(x[:, 1])
    return x


@dataclass
class Trial:
    task: str
    seed: int
    noise: float
    fit_x: np.ndarray
    fit_y: np.ndarray
    cal_x: np.ndarray
    cal_y: np.ndarray
    pool: np.ndarray
    probes: np.ndarray
    test_x: np.ndarray
    same_x: np.ndarray
    query_noise: np.ndarray
    stream_key: str

    def observations(self, acquired):
        ids = np.array([r['query_id'] for r in acquired], dtype=int)
        ax = self.pool[ids]
        ay = np.array([r['label'] for r in acquired])
        return Observations(np.concatenate((self.fit_x, ax)),
                            np.concatenate((self.fit_y, ay)), self.cal_x.copy(),
                            self.cal_y.copy(), ax.copy(), ay, self.pool.copy(),
                            self.probes.copy(), bounds(self.task), self.noise)

    def oracle(self):
        return QueryOracle(self)


class QueryOracle:
    def __init__(self, trial):
        self._trial = trial
        self.records = []
        self._seen = set()

    def measure(self, query_id):
        if not isinstance(query_id, (int, np.integer)):
            raise ValueError('query ID must be integer')
        t = self._trial
        if query_id < 0 or query_id >= len(t.pool) or query_id in self._seen:
            raise ValueError('invalid or repeated query')
        value = float(reference(t.task, t.pool[[query_id]])[0] + t.query_noise[query_id])
        self._seen.add(int(query_id))
        record = {'query_id': int(query_id), 'x': t.pool[query_id].tolist(),
                  'label': value, 'noise_realization_id': f'{t.stream_key}:query:{query_id}'}
        self.records.append(record)
        return value


def make_trial(task, seed, width, noise, control, config):
    # Numeric independent SeedSequence namespaces; stable across policy/run order.
    key = [1 if config['stage'] == 'development' else 2, TASKS.index(task),
           seed, int(width*10000), int(noise*10000), CONTROLS.index(control)]
    rngs = [np.random.default_rng(s) for s in np.random.SeedSequence(key).spawn(9)]
    fit = sample(task, config['n_fit'], width, control, rngs[0])
    cal = sample(task, config['n_calibration'], width, control, rngs[1])
    b = bounds(task)
    pool = (sample(task, config['n_query_candidates'], 0, 'constrained', rngs[2])
            if control == 'surface_restricted_queries'
            else rngs[2].uniform(b[:, 0], b[:, 1], (config['n_query_candidates'], 2)))
    probes = rngs[3].uniform(b[:, 0], b[:, 1], (512, 2))
    test = rngs[4].uniform(b[:, 0], b[:, 1], (config['n_test'], 2))
    same = sample(task, config['n_test'], width, control, rngs[5])
    return Trial(task, seed, noise, fit, reference(task, fit)+rngs[6].normal(0, noise, len(fit)),
                 cal, reference(task, cal)+rngs[7].normal(0, noise, len(cal)), pool, probes,
                 test, same, rngs[8].normal(0, noise, len(pool)), ':'.join(map(str, key)))
