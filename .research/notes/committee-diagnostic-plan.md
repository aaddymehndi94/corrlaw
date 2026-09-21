# Predeclared committee diagnostic — before v3 confirmation

For every augmented-policy trajectory, compare the original search committee with
its witness-augmented committee on the SAME saved measurement history and the SAME
point predictor. Use budgets0/1/2/4/8 and every condition. Reconstruct predictions
from saved equations; hidden labels enter only this post-acquisition evaluation.
Retain existing thresholds (off-preparation error>0.1, committee RMSspread<0.05),
with no threshold selection. Record both directions of threshold crossing, the
number of added alternatives, poor observational fit, and per-seed counts by task,
control and budget. Separate high-error/low-spread flags removed with a valid
observational fit from singleton/poor-fit fallbacks. Width/noise details remain in
unit artifacts. Apply separately to old finite v2 and new PySR v3 evidence.

This tests whether adding alternatives exposes a misleadingly small disagreement
on known benchmark errors. It does NOT improve the fixed point predictor by itself,
provide calibrated confidence, or establish improved acquisition. Later budgets
follow augmented-policy histories and are not a comparison with the different
ordinary-QBC intervention history. Treat within-trajectory comparisons accordingly.

Adding committee members need not increase variance. For N old predictions with
mean mu and variance v and M new predictions with mean nu and variance w, the
combined variance is (N*v+M*w)/(N+M) + N*M*(mu-nu)^2/(N+M)^2. The second term is
nonnegative, but weighting can still decrease the original variance. Both crossing
directions must therefore remain visible; no monotonic uncertainty claim is made.

Acceptance: parent hashes/completeness; recompute saved augmented spread/error/flag;
unit tests for upward/downward crossings; save per-condition and per-seed counts.
