"""Exact supplied-class sanity checks; not a new law or novelty claim."""
import argparse
import json
import os
from pathlib import Path
import sympy as sp


def verify():
    u,v,a,b,c,alpha=sp.symbols('u v a b c alpha',real=True)
    radius=u*u+v*v;target=u*u+2*v*v
    difference=(radius-1)*(a*u+b*v+c)
    origin=sp.expand(difference).subs({u:0,v:0})
    gradient=[sp.diff(target+difference,z).subs({u:0,v:0}) for z in (u,v)]
    assert origin==-c and gradient==[-a,-b]
    solution=sp.solve([origin,*gradient],[a,b,c])
    assert solution=={a:0,b:0,c:0}
    quartic=sp.expand(target+alpha*radius*(radius-1))
    assert sp.rem(quartic-target,radius-1,u)==0
    assert quartic.subs({u:0,v:0})==0
    for z in (u,v):
        assert sp.expand(quartic.subs(z,-z)-quartic)==0
        assert sp.diff(quartic,z).subs({u:0,v:0})==0
    lower=(1-alpha)*radius+alpha*radius**2
    assert sp.expand(quartic-lower)==v*v
    point={u:sp.Rational(1,2),v:0,alpha:sp.Rational(1,4)}
    assert target.subs(point)==sp.Rational(1,4)
    assert quartic.subs(point)==sp.Rational(13,64)
    r,lam=sp.symbols('r lam',positive=True)
    denominator=(1+lam)*(r*r+1)+2*(1-lam)*r
    reduced=r*(r+1)/denominator
    derivative_numerator=sp.factor(sp.diff(reduced,r)*denominator**2)
    expected=(1-3*lam)*r*r+2*(1+lam)*r+1+lam
    assert sp.expand(derivative_numerator-expected)==0
    series=u*v/(u+v)
    family=u*v*(u+v)/((u+v)**2+lam*(u-v)**2)
    assert sp.cancel(family.subs(v,u)-u/2)==0
    assert sp.cancel(family-family.xreplace({u:v,v:u}))==0
    assert family.subs(u,0)==0 and family.subs(v,0)==0
    assert sp.cancel(family.subs(lam,0)-series)==0
    assert sp.cancel(sp.limit(family/u,u,0)-1/(1+lam))==0
    return dict(valid=True,series_family=str(family),series_monotonicity_numerator=str(expected),
        series_parameter_range='0 < lambda <= 1/3',
        series_small_input_ratio=str(1/(1+lam)),
        scope='Exact circle agreement, explicit polynomial-degree assumptions; analytic class sanity, not a numerical experiment.',
        target=str(target),cubic_difference=str(difference),origin=str(origin),
        gradient_at_origin=list(map(str,gradient)),cubic_origin_and_stationarity_solution={str(k):str(val) for k,val in solution.items()},
        quartic_alternative=str(quartic),nonnegative_lower_bound=str(lower),
        excess_over_lower_bound=str(sp.expand(quartic-lower)),alpha_range='0 < alpha <= 1',
        off_circle_point={'u':'1/2','v':'0','alpha':'1/4'},reference_value='1/4',alternative_value='13/64',
        limitation='Finite noisy agreement and finite positivity probes do not imply the exact global premises.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'));args=p.parse_args()
    if not args.output:p.error('output or CORRLAW_RESULT_DIR required')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    data=verify();(out/'algebra.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
