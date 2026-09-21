#!/usr/bin/env python3
"""Completion gate: fail closed if required research evidence is missing.

This is a disk-evidence watchdog, not a service that can restart Codex.
The active Codex goal is responsible for continuing work after a failed check.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    issues=[]
    plan=(ROOT/'.research/PLAN.md').read_text()
    for task in range(1,12):
        rows=[r for r in plan.splitlines() if r.startswith(f'| T{task:02d} |')]
        if len(rows)!=1 or not rows[0].endswith('| DONE |'):
            issues.append(f'T{task:02d} lacks DONE evidence')
    required=['reports/REPORT.md','.research/CLAIMS.md','.research/HANDOFF.md',
              'requirements.lock.txt','reports/confirmation/summary.json',
              'results/runs/confirmation-v2-001/validation.json',
              'results/runs/reproduce-v2-001/reproduction.json',
              '.research/notes/final-tests.txt']
    for path in required:
        if not (ROOT/path).is_file():issues.append(f'missing {path}')
    validation=ROOT/'results/runs/confirmation-v2-001/validation.json'
    if validation.exists():
        data=json.loads(validation.read_text())
        if not data.get('valid') or data.get('completed_units')!=data.get('expected_units'):
            issues.append('confirmation is incomplete or invalid')
    replay=ROOT/'results/runs/reproduce-v2-001/reproduction.json'
    if replay.exists() and not json.loads(replay.read_text()).get('exact_match'):
        issues.append('fresh-process reproduction does not match')
    result=subprocess.run([sys.executable,'tools/lab.py','verify','--id','v2'],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:issues.append('protocol freeze verification failed: '+result.stderr.strip())
    tests=ROOT/'.research/notes/final-tests.txt'
    if tests.exists() and ('passed' not in tests.read_text() or 'FAILED' in tests.read_text()):
        issues.append('test evidence does not show a pass')
    output={'complete':not issues,'issues':issues,
            'scope':'bounded finite-library research pilot; no guarantee of research advantage',
            'watchdog':'completion gate plus active Codex task goal; no background agent restart'}
    (ROOT/'.research/completion.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2));return int(bool(issues))

if __name__=='__main__':sys.exit(main())
