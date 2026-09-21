"""Exploratory search and physical-prior diagnostics; separate from PySR evidence."""
from itertools import combinations
import numpy as np
from corrlaw.discovery import (Fit, fit, model_errors, admissible,
                               MAX_COEFFICIENT, MAX_TERMS)
from corrlaw.features import Library
from corrlaw.witnesses import augment


def exhaustive_fit(obs, max_terms=3):
    """Enumerate generic supports; no task identity or reference expression."""
    lib=Library.build(obs.bounds,obs.probes)
    matrices=[lib.transform(x) for x in (obs.x,obs.calibration_x,obs.acquired_x)]
    a=matrices[0];candidates=[];supports=0
    for size in range(1,min(max_terms,len(lib.powers))+1):
        for support in combinations(range(len(lib.powers)),size):
            supports+=1
            coeff=np.zeros(len(lib.powers))
            coeff[list(support)]=np.linalg.lstsq(a[:,support],obs.y,rcond=1e-10)[0]
            coeff[np.abs(coeff)<1e-10]=0
            if np.max(abs(coeff))>MAX_COEFFICIENT:
                continue
            error=model_errors(coeff,matrices,obs)
            candidates.append(dict(coefficients=coeff,errors=error,
                                   terms=int(np.count_nonzero(coeff)),
                                   admissible=admissible(coeff,error,obs.noise_std)))
    if not candidates:raise RuntimeError('no bounded exhaustive candidate')
    selected=min(candidates,key=lambda r:(r['errors'][3]+1e-8*r['terms'],tuple(r['coefficients'])))
    plausible=[r['coefficients'] for r in candidates if r['admissible']]
    return Fit(lib,selected['coefficients'],np.asarray(plausible or [selected['coefficients']]),candidates,not plausible),supports


def prior_library(obs,prior):
    """Algebraic restrictions for a signed polynomial domain, not hidden labels."""
    full=Library.build(obs.bounds,obs.probes)
    if any(a<0 or b<0 for a,b in full.powers):
        raise ValueError('origin prior requires nonsingular polynomial features')
    if prior not in ('none','zero_origin','zero_origin_and_even'):
        raise ValueError('unknown prior')
    keep=[]
    for j,(a,b) in enumerate(full.powers):
        if prior!='none' and (a,b)==(0,0):continue
        if prior=='zero_origin_and_even' and (a%2 or b%2):continue
        keep.append(j)
    return Library([full.powers[j] for j in keep],full.scale[keep])


def prior_fit(obs,seed,prior,diversified=False):
    lib=prior_library(obs,prior)
    # The original min7-feature rule retains the entire class when priors leave
    # fewer than7 columns. Do not ask np.random.choice for unavailable features.
    return fit(obs,seed,diversified and len(lib.powers)>=7,lib)


def prior_augment(obs,fitted):
    if len(fitted.library.powers)>=3:
        return augment(obs,fitted)
    # Under zero origin + parity in degree<=3, the class consists of u^2,v^2.
    # Search its sole two-column relation with the same normalization/filtering.
    lib=fitted.library
    a,cal,acquired,probes=[lib.transform(x) for x in
                          (obs.x,obs.calibration_x,obs.acquired_x,obs.probes)]
    observed=np.concatenate((a,cal))
    base_errors=model_errors(fitted.best,(a,cal,acquired),obs)
    base_valid=admissible(fitted.best,base_errors,obs.noise_std)
    if not base_valid:return fitted.committee,[],'poor_observational_fit'
    if a.shape[1]!=2:raise ValueError('unexpected restricted class')
    _,vectors=np.linalg.eigh(observed.T@observed/len(observed))
    q=vectors[:,0];norm=np.sqrt(np.mean((probes@q)**2))
    if norm<1e-8:return fitted.committee,[],'no_witness_within_search_budget'
    q=q/norm
    if q[np.argmax(abs(q))]<0:q=-q
    ratio=float(np.sqrt(np.mean((observed@q)**2)))
    ws=[];alternatives=[]
    if ratio<=.1 and max(abs(q))<=20:
        for alpha in (-1.,-.25,.25,1.):
            coeff=fitted.best+alpha*q;coeff[abs(coeff)<1e-10]=0
            error=model_errors(coeff,(a,cal,acquired),obs)
            if not admissible(coeff,error,obs.noise_std):continue
            difference=lib.transform(obs.pool)@(coeff-fitted.best)
            location=int(np.argmax(abs(difference)))
            ws.append(dict(base=fitted.best.tolist(),alternative=coeff.tolist(),q=q.tolist(),alpha=alpha,
                           ratio=ratio,base_expression=lib.expression(fitted.best),
                           alternative_expression=lib.expression(coeff),q_expression=lib.expression(q),
                           errors=list(error),terms=int(np.count_nonzero(coeff)),
                           max_pool_difference=float(abs(difference[location])),disagreement_query_id=location))
            alternatives.append(coeff)
    committee=np.concatenate((fitted.committee,np.array(alternatives))) if alternatives else fitted.committee
    if ws and max(w['max_pool_difference'] for w in ws)<=1e-6:
        status='no_discriminating_query_in_allowed_pool'
    else:status='ambiguity_witness_found' if ws else 'no_witness_within_search_budget'
    return committee,ws,status
