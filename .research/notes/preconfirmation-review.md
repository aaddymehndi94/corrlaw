# Preconfirmation design review (ongoing, development only)

2026-09-21, lead self-review; this is not independent scientific validation.

Resolved:
- Baseline fairness: shared point estimator/search budget; diversified committee gets
  equal bootstrap count with feature subsampling; augmented alternatives only affect
  acquisition. All labels, including calibration, count. Calibration is not a hidden
  test set and may be used for model filtering and geometry.
- No formula/preparation/task identifier enters the learner. Bounds determine safe
  reciprocal grammar equally for every policy. Evaluation is after selection and
  cannot alter learner RNGs. Tests inspect module dependencies and interface fields.
- Measurement noise is candidate-ID keyed and shared across policies. Different
  acquired coordinates can legitimately receive different noises.
- Witness alternatives obey coefficient/term limits, observed/calibration RMSE and
  per-acquired-point residual tests. Feature scaling uses broad public probes.
- Width controls change preparation inputs before labels are computed.
- D-optimal uses all known measured coordinates and Cholesky leverage on exactly
  the same features. A one-mode equivalence is derived in docs/EQUIVALENCE.md.
- Uniform box tests also change marginal coverage relative to the ring. The report
  must not call this only decorrelation at fixed marginal distributions.

Before freeze:
- Profile all five policies; check every artifact and inspect failures.
- Preserve whether PySR actually became usable; do not relabel an import as search.
- Strengthen resume checks to validate completed-unit hashes and source provenance.
- Assert both base and alternative admissibility when saving a witness.
- Add missing-library witness-search diagnostic and false-alarm controls.
- Record actual configuration, dependency versions, resolved run counts and figure plan.
- Keep any failed development attempt without silently rewriting its output.
