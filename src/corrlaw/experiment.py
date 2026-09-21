"""Paired experiment coordinator; immutable unit files and explicit failure ledger."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import sys
import time
import traceback
import numpy as np
from .oracle import make_trial, TASKS, CONTROLS
from .discovery import fit
from .witnesses import augment
from .acquisition import POLICIES, select
from .evaluation import evaluate, auc, symbolic_recovery

KEYS = {'schema_version', 'status', 'stage', 'tasks', 'seeds', 'constraint_widths',
        'output_noise_std', 'n_fit', 'n_calibration', 'n_query_candidates', 'n_test',
        'query_budgets', 'policies', 'controls', 'engine', 'notes'}


def load_config(path):
    c = json.loads(Path(path).read_text())
    if set(c) != KEYS:
        raise ValueError(f'config missing {KEYS-set(c)}; unknown {set(c)-KEYS}')
    if c['schema_version'] != 1 or c['status'] != 'ready' or c['engine'] != 'finite_library':
        raise ValueError('unsupported or unfinished configuration')
    if c['stage'] not in ('development', 'confirmation'):
        raise ValueError('invalid stage')
    allowed = 'AB' if c['stage'] == 'development' else 'CDEF'
    for field, legal in [('tasks', allowed), ('policies', POLICIES), ('controls', CONTROLS),
                         ('constraint_widths', [0, .01, .05]), ('output_noise_std', [0, .01])]:
        if not c[field] or len(set(c[field])) != len(c[field]) or any(v not in legal for v in c[field]):
            raise ValueError(f'invalid {field}')
    if c['query_budgets'] != [0, 1, 2, 4, 8]:
        raise ValueError('budgets must be 0,1,2,4,8')
    for field in ('n_fit', 'n_calibration', 'n_query_candidates', 'n_test'):
        if not isinstance(c[field], int) or c[field] < (32 if field == 'n_fit' else 8):
            raise ValueError(f'invalid {field}')
    if not c['seeds'] or len(set(c['seeds'])) != len(c['seeds']) or any(type(s) != int or s < 0 for s in c['seeds']):
        raise ValueError('invalid seeds')
    return c


def save(path, data):
    path = Path(path)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')
    tmp.replace(path)


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, allow_nan=False).encode()).hexdigest()


def array_digest(*arrays):
    h = hashlib.sha256()
    for array in arrays:
        h.update(str(array.shape).encode()); h.update(np.ascontiguousarray(array).tobytes())
    return h.hexdigest()


def run_policy(trial, policy, c):
    clock = time.perf_counter()
    oracle = trial.oracle()
    records = []; models = []; augmentation_seconds = 0.; fitting_seconds = 0.
    for budget in range(max(c['query_budgets'])+1):
        obs = trial.observations(oracle.records)
        model_seed = np.random.SeedSequence([trial.seed, 400, budget])
        t = time.perf_counter()
        # The point predictor is identical across policies; diversity changes only acquisition.
        fitted = fit(obs, model_seed)
        fitting_seconds += time.perf_counter()-t
        ordinary = fitted.committee
        t = time.perf_counter()
        augmented, witnesses, diagnostic = augment(obs, fitted)
        augmentation_seconds += time.perf_counter()-t
        if policy == 'diversified_qbc':
            t = time.perf_counter()
            committee_fit = fit(obs, np.random.SeedSequence([trial.seed, 401, budget]), True, fitted.library)
            fitting_seconds += time.perf_counter()-t
            committee = committee_fit.committee
        elif policy == 'augmented_qbc':
            committee = augmented
        else:
            committee = ordinary
        if budget in c['query_budgets']:
            score = evaluate(trial, fitted, committee)
            records.append(dict(budget=budget, total_labels=c['n_fit']+c['n_calibration']+budget,
                                witness_count=len(witnesses), diagnostic=diagnostic,
                                rounded_symbolic_recovery=symbolic_recovery(trial.task, fitted.library, fitted.best), **score))
        lib = fitted.library
        models.append({'budget': budget, 'powers': lib.powers, 'scale': lib.scale.tolist(),
                       'selected_coefficients': fitted.best.tolist(),
                       'selected_expression': lib.expression(fitted.best),
                       'committee': committee.tolist(), 'ordinary_committee': ordinary.tolist(),
                       'candidates': [dict(coefficients=r['coefficients'].tolist(),
                                           expression=lib.expression(r['coefficients']),
                                           errors=list(r['errors']), terms=r['terms'],
                                           admissible=r['admissible']) for r in fitted.candidates],
                       'witnesses': witnesses, 'diagnostic': diagnostic})
        if budget < max(c['query_budgets']):
            query_id, acquisition_score = select(policy, obs, fitted, committee,
                              [r['query_id'] for r in oracle.records],
                              np.random.SeedSequence([trial.seed, 402, budget]))
            oracle.measure(query_id)
            oracle.records[-1]['acquisition_score'] = acquisition_score
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {'status': 'completed', 'metrics': records, 'auc': auc(records), 'models': models,
            'queries': oracle.records,
            'initial_data_hash': array_digest(trial.fit_x, trial.fit_y, trial.cal_x, trial.cal_y, trial.pool, trial.probes),
            'evaluation_hash': array_digest(trial.test_x, trial.same_x),
            'runtime_seconds': time.perf_counter()-clock, 'fitting_seconds': fitting_seconds,
            'augmentation_seconds': augmentation_seconds,
            'process_peak_rss_bytes': int(rss if sys.platform == 'darwin' else rss*1024)}


def units(c):
    for task, seed, width, noise, control in itertools.product(c['tasks'], c['seeds'],
            c['constraint_widths'], c['output_noise_std'], c['controls']):
        # Controls have a fixed exact-surface base, avoiding redundant width sweeps.
        if control != 'constrained' and width != 0:
            continue
        for policy in c['policies']:
            key = f'{task}-s{seed}-w{width:g}-n{noise:g}-{control}-{policy}'
            yield key, task, seed, width, noise, control, policy


def scientific_content(unit):
    return {k: v for k, v in unit.items() if k not in
            ('runtime_seconds', 'fitting_seconds', 'augmentation_seconds', 'process_peak_rss_bytes')}


def engine_hash():
    root = Path(__file__).resolve().parent
    return digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))})


def run(c, output, resume=False):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    config_path = output/'config.json'
    provenance_path = output/'engine.json'
    provenance = {'source_sha256': engine_hash()}
    old_manifest = {}
    if config_path.exists():
        if not resume or json.loads(config_path.read_text()) != c:
            raise ValueError('output exists; matching config and --resume required')
        if not provenance_path.exists() or json.loads(provenance_path.read_text()) != provenance:
            raise ValueError('resume requires identical engine source')
        if (output/'manifest.json').exists():
            old_manifest = {r['unit_id']: r for r in json.loads((output/'manifest.json').read_text())['units']}
    else:
        save(config_path, c)
        save(provenance_path, provenance)
    unit_dir = output/'units'; unit_dir.mkdir(exist_ok=True)
    manifest = []; failures = 0
    for key, task, seed, width, noise, control, policy in units(c):
        path = unit_dir/f'{key}.json'
        identity = dict(unit_id=key, task=task, seed=seed, width=width, noise=noise,
                        control=control, policy=policy, config_hash=digest(c))
        if path.exists():
            old = json.loads(path.read_text())
            prior = old_manifest.get(key)
            if not prior or hashlib.sha256(path.read_bytes()).hexdigest() != prior['sha256']:
                raise ValueError(f'unverified or changed saved unit {key}; preserve it and use a new run ID')
            if not resume or any(old.get(k) != v for k, v in identity.items()):
                raise ValueError(f'existing or inconsistent unit {key}')
            result = old
        else:
            try:
                trial = make_trial(task, seed, width, noise, control, c)
                result = dict(identity, **run_policy(trial, policy, c))
            except Exception as e:
                result = dict(identity, status='failed', error=repr(e), traceback=traceback.format_exc())
            save(path, result)
        failed = result['status'] != 'completed'
        failures += failed
        manifest.append(dict(identity, status=result['status'], path=str(path.relative_to(output)),
                             sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             scientific_sha256=digest(scientific_content(result))))
        save(output/'manifest.json', {'units': manifest, 'failed': failures,
                                     'expected_units': len(list(units(c)))})
        print(f'{len(manifest)}/{len(list(units(c)))} {key} {result["status"]}', flush=True)
    return failures
