# CorrLaw experimental protocol
Status: DRAFT
Protocol ID: not frozen

This is a completion checklist, not a registered final evaluation. Do not change
its status or create a freeze until the agent has filled every decision below
using development evidence only. Use a new version for subsequent changes.

## Question and primary comparison
Does explicit near-nullspace candidate augmentation reveal missed admissible
alternatives and improve off-preparation prediction per additional measurement
beyond ordinary QBC, diversified QBC, random and regularized D-optimal design?
Known-method equivalence or no additional benefit is a valid outcome.

## Tasks and independent replication units
Development: A/B. Confirmation candidates: C/D/E/F. Final subset: UNRESOLVED.
Minimum pilot: both development tasks, at least two confirmation tasks, all five
policies and repeated paired seeds. Aim for five confirmation seeds where feasible.
State any reduced scope before confirmation and preserve complete paired comparisons.
A task/seed is a replication unit; hidden evaluation points are not independent trials.

## Decisions to resolve before freeze
- Dimensional equations, scales, positivity/symmetry/boundary priors for each task.
- Exact input bounds, sampling distributions and near-surface perturbation mechanism.
- Primary incomplete-prior setting versus optional prior-aware controls.
- Known output noise model and units; singularity and out-of-domain handling.
- Shared fit/calibration/query/test counts and query budgets.
- Truly independent RNG streams and reusable paired measurement-noise realization IDs.
- Which control conditions run on which tasks; matched marginals and valid relabeling.
- Generic feature grammar, degree/reciprocal bounds, numerical protection and scaling.
- Ensemble sizes, search budgets, complexity penalties and finite-library/PySR scope.
- Near-null thresholds, sparse witness size, alpha grid, fit tolerance and admissibility.
- Exact acquisition scores, regularization, tie handling and query repetition policy.
- Coefficient/symbolic-equivalence tolerances and dense numerical comparison limits.
- Final confirmation seeds/task subset and planned run count/compute allocation.
- Exact normalized error, AUC and false-consensus diagnostic definitions/thresholds.
- Failed-run, timeout, missing-policy and reproduction-mismatch treatment.
- Data/compute budgets per policy and what is shared vs refit.
- Planned figures/tables and limitations of any inference from a small task suite.
- Final environment versions and code/config commit identifiers.

## Primary endpoints to implement and specify
1. Off-preparation normalized RMSE versus added-label budget, using a prespecified
   physically defined output scale, not a normalization chosen after seeing test data.
2. Fixed-definition area under that error curve (budget axis, quadrature and scaling).
3. Same-preparation hidden error and false-consensus rate under fixed thresholds.
4. Validity/coverage of admissible ambiguity witnesses and control-condition failures.
5. Full runtime, sample-count and failure accounting.

Secondary: algebraic recovery where justified, symbolic proof of supplied identities,
coefficient recovery and source-consistent prediction on a separate domain.

## Planned interpretation
Any improvement must be described relative to all serious baselines, not just a
weak ordinary ensemble. Equivalence to D-optimal/leverage acquisition must be stated.
The synthetic oracle is known to the coding agent; this is not a blind autonomous-
scientist evaluation. Finite-library-only evidence cannot establish general PySR
performance. A diagnostic that finds no witness cannot certify uniqueness.

## Freeze review
All decisions resolved: NO
Scientific tests passed with paths: NOT_YET
Development evidence and decisions: NOT_YET
Prior-work/equivalence audit: NOT_YET
Final intended configuration and code committed: NOT_YET
Freeze manifest: NOT_CREATED
