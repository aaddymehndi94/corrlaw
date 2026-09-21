#!/usr/bin/env python3
"""Regenerate the numerical overnight report bundle from audited immutable runs."""
import argparse
import hashlib
import json
from pathlib import Path
from corrlaw.summarize import summarize
from corrlaw.positivity import analyze as positivity
from corrlaw.committee_diagnostic import analyze as committee
from corrlaw.compute_sensitivity import compare as sensitivity
from corrlaw.explain import explain
from corrlaw.experiment import save

PRIMARY=Path('results/runs/pysr-confirmation-v3-001')
STRONG=Path('results/runs/pysr-confirmation-strong-v3-001')
FINITE=Path('results/runs/confirmation-v2-001')


def audited(path):
    result=json.loads((path/'validation.json').read_text())
    if not result.get('valid') or result['completed_units']!=result['expected_units']:
        raise ValueError(f'incomplete or invalid source {path}')
    manifest=json.loads((path/'manifest.json').read_text())
    if len(manifest['units'])!=result['expected_units']:raise ValueError('source manifest changed after audit')
    for row in manifest['units']:
        if sha(path/row['path'])!=row['sha256']:raise ValueError('source artifact hash mismatch')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def render(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    families=[];sources=[]
    summaries=[(Path('results/runs/pysr-development-002'),'pysr-development'),
               (PRIMARY,'pysr-confirmation'),(STRONG,'pysr-confirmation-strong')]
    summaries.extend((Path('results/runs/prior-control-001')/prior,'prior-'+prior)
                     for prior in ('none','zero_origin','zero_origin_and_even'))
    for source,family in summaries:
        audited(source);summarize(source,output/family);families.append(family)
        sources.append(dict(run=str(source),manifest_sha256=sha(source/'manifest.json')))
        print('rendered',family,flush=True)
    audited(FINITE)
    sources.append(dict(run=str(FINITE),manifest_sha256=sha(FINITE/'manifest.json')))
    for source,name in [(PRIMARY,'pysr'),(FINITE,'finite')]:
        positivity(source,output/('positivity-'+name));families.append('positivity-'+name)
        committee(source,output/('committee-'+name));families.append('committee-'+name)
    sensitivity(PRIMARY,STRONG,output/'compute-sensitivity');families.append('compute-sensitivity')
    first_noise=json.loads((PRIMARY/'config.json').read_text())['output_noise_std'][0]
    for task in 'CDEF':
        unit=f'{task}-s93001-w0-n{first_noise:g}-constrained-augmented_qbc'
        family='witness-'+task
        explain(PRIMARY,unit,0,output/family);families.append(family)
    source=Path('results/runs/prior-control-001/zero_origin')
    explain(source,'B-s301-w0-n0-constrained-augmented_qbc',0,output/'witness-origin-only')
    families.append('witness-origin-only')
    files=[]
    for family in sorted(families):
        files.extend(dict(path=str(p.relative_to(output)),sha256=sha(p))
                     for p in sorted((output/family).rglob('*')) if p.is_file())
    result=dict(sources=sources,files=files,scope='Numerical summaries, conditions, paired diagnostics and figures; prose report is separately reviewed.')
    save(output/'overnight-bundle-manifest.json',result)
    return result


def compare(original,new,result):
    original=Path(original);new=Path(new)
    old=json.loads((original/'overnight-bundle-manifest.json').read_text())
    expected={r['path']:r['sha256'] for r in old['files']}
    actual={r['path']:r['sha256'] for r in result['files']}
    issues=[]
    if old['sources']!=result['sources']:issues.append('source manifests differ')
    if expected.keys()!=actual.keys():issues.append('artifact file sets differ')
    checked=[]
    for relative in sorted(expected.keys()|actual.keys()):
        a=original/relative;b=new/relative
        first=sha(a) if a.is_file() else None;second=sha(b) if b.is_file() else None
        valid=first==second and first==expected.get(relative) and second==actual.get(relative)
        if not valid:issues.append(relative)
        checked.append(dict(path=relative,original_sha256=first,regenerated_sha256=second,exact_match=valid))
    return dict(byte_identical=not issues,artifacts_checked=len(checked),issues=issues,artifacts=checked,
                scope=result['scope'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    parser.add_argument('--compare');parser.add_argument('--comparison-output');a=parser.parse_args()
    if a.compare and not a.comparison_output:parser.error('--comparison-output is required with --compare')
    result=render(a.output)
    if a.compare:
        checked=compare(a.compare,a.output,result);save(Path(a.comparison_output),checked)
        print(json.dumps({k:v for k,v in checked.items() if k!='artifacts'},indent=2))
        raise SystemExit(not checked['byte_identical'])
