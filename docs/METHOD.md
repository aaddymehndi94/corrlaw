# Finite-library method (implemented development version)

All policies have the same point predictor. Acquisition committees differ; reported
prediction error does not silently switch to an augmented committee mean.
128 fitting labels and 64 calibration labels are available initially. Acquired
measurements append to fitting data. Calibration labels select/filter models, so
all 192 initial labels count toward total cost. Models are refit after each of eight
queries; reported budgets are 0,1,2,4,8. Pools contain 2,048 candidates in full runs,
with 512 public unlabeled scaling probes and independent 2,048-point hidden tests
for each preparation. Query IDs cannot repeat. Noise is drawn once per candidate
ID and reused across policies, preserving paired measurements for overlapping IDs.

## Sparse equation search
Greedy orthogonal matching pursuit selects the largest absolute residual correlation
divided by the observed feature norm, then least-squares refits active columns with
rcond=1e-10. Save supports of sizes 1,2,3,4,6,7 from one full-data fit and eight
bootstrap fits. No task-specific term is inserted. Normalized coefficients must
be at most 20 in absolute value, and at most seven are nonzero. Coefficients below
1e-10 are zeroed. Observational aliases remain distinct; only coefficient-equivalent
vectors (rtol=1e-7, atol=1e-9) are deduplicated.

A selected point model minimizes training MSE + calibration MSE + (when queries
exist) acquired-point MSE, plus 1e-8 times term count. This last acquired component
prevents a few informative measurements being overwhelmed by the large initial
surface dataset in model selection. Coefficients are nevertheless fit by ordinary
least squares on fitting rows plus acquired rows. This distinction is intentional.
Plausibility requires both fit and calibration RMSE ≤ 0.002+3σ and every acquired
point residual ≤ 0.002+4σ. The tolerance is an engineering admissibility threshold,
not a calibrated posterior or statistical confidence level. If no candidate passes,
record poor_observational_fit and retain only the selected model for acquisition.

## Witness construction
For every two/three-column feature subset, find its smallest Gram eigenvector on
fitting+calibration coordinates. Normalize the resulting q to RMS=1 on public box
probes; discard probe RMS <1e-8 or coefficient magnitude >20. Recompute direct
observed RMS, accepting geometric proposals with ratio ≤0.1. Search in ascending
ratio/subset order; keep at most 12 distinct directions that yield alternatives.
For the point model f, try f+αq for α∈{-1,-0.25,0.25,1}. Each accepted alternative
must independently satisfy the same term/coefficient limits and residual tests as
ordinary candidates. Save base, alternative, q, alpha, residuals, complexity and
largest query-pool disagreement location. No alternatives are generated if the
ordinary candidate search has no plausible member.

This is empirical finite-class ambiguity. It is not an exhaustive sparse nullspace
search, a posterior, or a certificate of uniqueness. At a restricted pool, a found
witness with maximum feasible disagreement ≤1e-6 is explicitly labeled
no_discriminating_query_in_allowed_pool. Near-surface numerical results do not
constitute exact identities. The separate symbolic circle test is exact.

## Five acquisition policies
- Random: reproducible uniform scores, take the maximum among unmeasured IDs.
- QBC: population variance of predictions from plausible ordinary candidates.
- Diversified QBC: same full-data candidates plus eight bootstrap searches retaining
  max(7,floor(0.7p)) randomly chosen feature columns. Only acquisition uses this
  committee; the point predictor remains shared. Credit E-SINDy/library bagging
  and the SISSO feature-dropout study in RELATED_WORK.md.
- Regularized D-optimal: leverage φᵀ(ΦᵀΦ+1e-4 I)⁻¹φ on the identical dictionary,
  using all measured fit/calibration/acquired coordinates. Cholesky solve avoids
  explicit matrix inversion.
- Augmented QBC: same variance as ordinary QBC after adding accepted alternatives.

Prediction disagreement uses fixed output units (scale 1 after nondimensionalizing),
not a candidate's mean prediction denominator. Scores within rtol=1e-10,
atol=1e-14 tie and are selected reproducibly. Any numeric tie bias is shared.

## Evaluation and resource accounting
The finite-library implementation first computes the ordinary nine-path fit for the
shared point predictor (one full-data path plus eight bootstrap paths). Diversified
QBC additionally computes a separate nine-path diversified ensemble. It therefore
uses 18 fitting paths per refit versus 9 for the other policies; its acquisition
committee itself uses nine paths. Recorded fitting time includes that extra work.
The separate physical-prior control reuses this design. These comparisons share
label budgets and point selection, but do not have identical total search costs.
The PySR extension instead uses exactly three searches per policy/refit, including
diversified QBC; see METHOD_PYSR.md. This is a disclosure of the unchanged finite
implementation, not a retrospective alteration of its experiments.

Off-preparation and same-preparation errors are RMSE in the physical output reference
units. AUC is trapezoidal integration of errors at [0,1,2,4,8], divided by 8.
False consensus is a trial/budget diagnostic: hidden off-preparation RMSE >0.1 and
RMS committee standard deviation on the hidden inputs <0.05. These hidden diagnostics
never inform acquisition. Algebraic recovery means equivalence after rounding raw
coefficients to six decimal places and dropping magnitude <1e-6; it is expressly a
rounded coefficient diagnostic, not proof of equality of floating point estimates.

We compute witnesses for all policies to compare diagnostic coverage; that common
instrumentation cost is separately timed. Operational policy cost can subtract
augmentation_seconds for policies other than augmented QBC. RSS is cumulative peak
of the batch process, not isolated per-policy peak; recorded as such. Runtime also
includes artifacts and evaluator work inside each policy function. Failures have no
fabricated metric values and remain in the manifest. A timeout may leave a partial
manifest; expected-unit checks must catch this. Run success alone is not validation.

Stream namespaces distinguish stage/task/seed/width/noise/control and then spawn
independent fitting, calibration, pool, probe, off-test, same-test and three noise
streams. Search/tie seeds are shared across policies at each budget; numerical inputs
already encode the distinct trial. Stable order and strict JSON configuration make
replay inspectable. One process runs at a time through tools/lab.py with ≤4 requested
BLAS threads. Seed independence does not make multiple conditions on one task/seed
independent scientific replication units.
