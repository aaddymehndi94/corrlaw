#!/usr/bin/env python3
"""Fail-closed evidence gate for the user-authorized overnight extension."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def read(relative,issues):
    path=ROOT/relative
    if not path.is_file():
        issues.append(f'missing {relative}');return {}
    try:return json.loads(path.read_text())
    except (ValueError,OSError) as exc:
        issues.append(f'invalid {relative}: {exc}');return {}


def main():
    issues=[];plan=(ROOT/'.research/PLAN.md').read_text()
    for task in range(12,18):
        rows=[r for r in plan.splitlines() if r.startswith(f'| T{task:02d} |')]
        if len(rows)!=1 or not rows[0].endswith('| DONE |'):
            issues.append(f'T{task:02d} lacks completion evidence')
    for name in ('pysr-confirmation-v3-001','pysr-confirmation-strong-v3-001'):
        run=read(f'results/runs/{name}/run.json',issues)
        audit=read(f'results/runs/{name}/validation.json',issues)
        if run.get('status')!='completed':issues.append(f'{name} did not complete')
        if not audit.get('valid') or audit.get('completed_units')!=audit.get('expected_units'):
            issues.append(f'{name} is incomplete or invalid')
    for name in ('pysr-reproduce-v3-001','pysr-reproduce-strong-v3-001','prior-reproduce-001'):
        result=read(f'results/runs/{name}/reproduction.json',issues)
        if not result.get('exact_match'):issues.append(f'{name} lacks exact reproduction')
    for prior in ('none','zero_origin','zero_origin_and_even'):
        result=read(f'results/runs/prior-control-001/{prior}/validation.json',issues)
        if not result.get('valid') or result.get('completed_units')!=result.get('expected_units'):
            issues.append(f'prior {prior} incomplete or invalid')
    search=read('results/runs/search-diagnostic-001/diagnostics.json',issues)
    if not search.get('complete'):issues.append('exhaustive-search diagnosis incomplete')
    search_audit=read('results/runs/search-diagnostic-001/validation.json',issues)
    if not search_audit.get('valid') or not search_audit.get('reproduction',{}).get('exact_coefficients'):
        issues.append('exhaustive-search artifact audit/replay failed')
    representation=read('results/runs/representation-diagnostic-001/diagnostic.json',issues)
    if not representation.get('known_relation_alternatives'):issues.append('representation limitation check missing')
    algebra=read('results/runs/physical-prior-algebra-001/algebra.json',issues)
    if not algebra.get('valid'):issues.append('physical-prior exact algebra missing/invalid')
    for name in ('pysr','finite'):
        diagnostic=read(f'reports/committee-{name}/summary.json',issues)
        if not diagnostic.get('rows') or not diagnostic.get('summaries'):
            issues.append(f'{name} saved-committee diagnostic missing')
    sensitivity=read('reports/compute-sensitivity/summary.json',issues)
    if not sensitivity.get('paired_units'):issues.append('matched-condition compute sensitivity missing')
    positivity=read('reports/positivity-pysr/summary.json',issues)
    if positivity.get('failed_units'):issues.append('positivity input contains failures')
    regeneration=read('reports/audit/overnight-report-regeneration.json',issues)
    if not regeneration.get('byte_identical'):issues.append('report regeneration not verified')
    for relative in ('reports/REPORT.md','.research/CLAIMS.md','.research/HANDOFF.md',
                     '.research/notes/overnight-final-audit.md','.research/notes/overnight-final-tests.txt'):
        if not (ROOT/relative).is_file():issues.append(f'missing {relative}')
    tests=ROOT/'.research/notes/overnight-final-tests.txt'
    if tests.exists() and ('passed' not in tests.read_text() or 'FAILED' in tests.read_text()):
        issues.append('final tests do not show a pass')
    verification=subprocess.run([sys.executable,'tools/lab.py','verify','--id','v3'],cwd=ROOT,capture_output=True,text=True)
    if verification.returncode:issues.append('v3 freeze verification failed: '+verification.stderr.strip())
    result=dict(complete=not issues,issues=issues,
                scope='Overnight PySR acquisition comparison, compute sensitivity, search/prior diagnostics and audited report',
                deadline_utc='2026-09-22T02:30:00Z')
    (ROOT/'.research/overnight-completion.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return int(bool(issues))


if __name__=='__main__':sys.exit(main())
