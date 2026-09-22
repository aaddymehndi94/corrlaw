"""Read-only comparison of the existing finite model-selection objective.

This analyzes saved fits, without fitting models or changing acquisition histories.
Run from any directory; --output selects a new derived artifact for reproduction.
"""
import argparse
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[2]
PARENT = ROOT / 'results/runs/confirmation-v2-001'
DIAGNOSTIC = ROOT / 'results/runs/search-diagnostic-001'
TOLERANCE = 1e-12  # Descriptive roundoff band, not a new scientific fit threshold.


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze():
    meta = json.loads((DIAGNOSTIC / 'diagnostics.json').read_text())
    assert meta['complete'] and meta['rows'] == 1200
    assert len(meta['unit_ids']) == len(set(meta['unit_ids'])) == 400
    manifest = json.loads((PARENT / 'manifest.json').read_text())
    originals = {r['unit_id']: r for r in manifest['units']}
    rows, sources = [], []
    for key in meta['unit_ids']:
        source = PARENT / originals[key]['path']
        assert sha(source) == originals[key]['sha256']
        old = json.loads(source.read_text())
        path = DIAGNOSTIC / 'units' / (key + '.json')
        unit = json.loads(path.read_text())
        assert unit['unit_id'] == key
        assert len(unit['rows']) == 3
        assert {r['budget'] for r in unit['rows']} == {0, 2, 8}
        sources.append(dict(unit_id=key, original_sha256=sha(source), diagnostic_sha256=sha(path)))
        for record in unit['rows']:
            budget = record['budget']
            model = next(m for m in old['models'] if m['budget'] == budget)
            candidates = [r for r in model['candidates'] if r['coefficients'] == model['selected_coefficients']]
            assert candidates
            previous = candidates[0]
            new = record['exhaustive']
            assert model['powers'] == new['powers'] and model['scale'] == new['scale']
            assert model['selected_expression'] == record['original_expression']
            old_metric = next(r for r in old['metrics'] if r['budget'] == budget)
            assert old_metric['off_rmse'] == record['original_off_rmse']
            old_score = previous['errors'][3] + 1e-8 * previous['terms']
            new_score = new['observed_errors'][3] + 1e-8 * new['terms']
            rows.append(dict(unit_id=key, task=old['task'], seed=old['seed'], budget=budget,
                             original_score=old_score, exhaustive_score=new_score,
                             score_delta=new_score-old_score, original_terms=previous['terms'],
                             exhaustive_terms=new['terms'], original_off_rmse=old_metric['off_rmse'],
                             exhaustive_off_rmse=new['off_rmse'], exhaustive_admissible=new['admissible']))
    assert len(rows) == 1200
    groups = []
    for task in 'CDEF':
        for budget in (0, 2, 8):
            group = [r for r in rows if r['task'] == task and r['budget'] == budget]
            assert len(group) == 100
            groups.append(dict(task=task, budget=budget, rows=len(group),
                lower_objective=sum(r['score_delta'] < -TOLERANCE for r in group),
                higher_objective=sum(r['score_delta'] > TOLERANCE for r in group),
                lower_hidden_error=sum(r['exhaustive_off_rmse'] < r['original_off_rmse']-TOLERANCE for r in group),
                lower_error_despite_higher_objective=sum(r['score_delta'] > TOLERANCE and r['exhaustive_off_rmse'] < r['original_off_rmse']-TOLERANCE for r in group),
                original_mean_score=statistics.mean(r['original_score'] for r in group),
                exhaustive_mean_score=statistics.mean(r['exhaustive_score'] for r in group)))
    return dict(scope='Exploratory comparison of the original recorded selection objective on identical archived histories. No refitting or acquisition changes. Use with separate scientific audits.',
                caution='A lower objective establishes a better-scoring available candidate, not global coefficient optimality. Lower hidden error with higher objective can reflect the restricted support class. Rows share seeds and sometimes observations; they are not independent replications.',
                objective='observed_errors[3] + 1e-8 * nonzero terms', descriptive_roundoff_band=TOLERANCE,
                script_sha256=sha(Path(__file__)), parent_manifest_sha256=sha(PARENT/'manifest.json'),
                diagnostic_metadata_sha256=sha(DIAGNOSTIC/'diagnostics.json'), rows=rows, groups=groups, sources=sources)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(ROOT/'reports/audit/search-objective.json'))
    args = parser.parse_args()
    result = analyze()
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['groups'], indent=2))
