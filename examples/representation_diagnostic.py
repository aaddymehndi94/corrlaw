"""Post hoc A/B encoding diagnostic, using the supplied circle relation explicitly.

This is an evaluator-side explanation, not learner discovery or a method change.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import numpy as np
import sympy as sp
from corrlaw.features import Library
from corrlaw.symbolic import Expression,errors
from corrlaw.oracle import make_trial


def analyze(parent):
    parent=Path(parent);c=json.loads((parent/'config.json').read_text())
    key='B-s201-w0-n0-constrained-augmented_qbc'
    manifest=json.loads((parent/'manifest.json').read_text())
    entry=next(r for r in manifest['units'] if r['unit_id']==key)
    source=parent/entry['path']
    if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('source hash mismatch')
    unit=json.loads(source.read_text());model=unit['models'][0]
    trial=make_trial('B',201,0,0,'constrained',c);obs=trial.observations([])
    lib=Library([tuple(x) for x in model['powers']],np.asarray(model['scale']))
    base=Expression(model['selected_expression'],len(lib.powers));q=np.zeros(len(lib.powers))
    # Supplied evaluator-side relation, deliberately NOT called an inferred witness.
    for power,coefficient in [((0,0),-1),((0,2),1),((2,0),1)]:
        i=lib.powers.index(power);q[i]=coefficient*lib.scale[i]
    q/=np.sqrt(np.mean((lib.transform(obs.probes)@q)**2))
    expr=sum(sp.Float(float(v),17)*z for v,z in zip(q,base.symbols))
    matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
    constant=base.symbols[lib.powers.index((0,0))]
    assert lib.scale[lib.powers.index((0,0))]==1.
    rows=[]
    for alpha in (-1.,-.25,.25,1.):
        alt=Expression(str(base.symbolic+sp.Float(alpha,17)*expr),len(q))
        reduced=Expression(str(sp.expand(alt.symbolic.subs(constant,1))),len(q))
        for inputs in (obs.x,obs.calibration_x,obs.pool,obs.probes):
            phi=lib.transform(inputs)
            if not np.allclose(alt.predict(phi),reduced.predict(phi),rtol=1e-12,atol=1e-12):
                raise ValueError('constant folding changed predictions')
        rows.append(dict(alpha=alpha,arithmetic_complexity=alt.complexity,
            observed_errors=errors(alt,matrices,obs),constant_folded_complexity=reduced.complexity,
            constant_folded_expression=reduced.expression,
            folded_errors=errors(reduced,matrices,obs),folded_bounded=reduced.bounded(c['search_settings']['max_complexity'])))
    return dict(scope='Post hoc A/B representation diagnostic using the supplied circle relation; NOT an algorithm-generated witness or a primary method change.',
        parent=str(parent),unit_id=key,source_sha256=entry['sha256'],selected=model['selected_expression'],
        selected_complexity=base.complexity,model_witness_count=len(model['witnesses']),
        ordinary_committee_size=len(model['search_committee']),initial_metric=unit['metrics'][0],
        known_relation_alternatives=rows,
        implication='Formula encoding can obstruct bounded witness construction; no witness is not uniqueness. No constant-folding ablation was run.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parent',required=True)
    p.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'));a=p.parse_args()
    if not a.output:p.error('output or CORRLAW_RESULT_DIR required')
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True);result=analyze(a.parent)
    (out/'diagnostic.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
