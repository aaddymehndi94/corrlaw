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

Resolved after development:
- All 360 units completed; audit checked 21,651 witnesses without errors.
- Both witness expressions now must be admissible; resume checks source/config and
  existing manifest file hashes; tests include altered artifacts and missing library.
- PySR smoke and six static A/B fits actually ran. No PySR policy sweep is claimed.
- Thresholds retained unchanged; independent/shuffled A/B initial witness counts were
  zero across six task-control replicates each. Exact/near findings remain empirical.
- Pilot is fast enough for all C/D/E/F × five confirmation seeds × all controls,
  1,000 policy units. No confirmation outcome inspected at this decision.
- Plot legend overlapped the title on first render; moved legend below panels before
  freeze and regeneration. Numeric output unaffected. Compact confirmation unit JSON
  preserves all data while avoiding unnecessary pretty-print file expansion.
- Fixed tolerance/complexity choices are not optimized statistical confidence.
- No peer-independent validation or blind coding-agent evaluation is asserted.

Freeze blocker preserved: initial v1 freeze rejected ignored src/corrlaw.egg-info
created by the authorized editable installation. No freeze or confirmation was
created. Fix inventory to exclude generated *.egg-info directories and .DS_Store,
while still detecting new actual .py files; added a fixture regression test.
A scripted premature state update was corrected immediately after inspecting the
failed command. Freeze/confirmation completion is recorded only after success.
Also replaced inherited obsolete config notes before any confirmation. Numeric
settings are unchanged. Final test count is 48 with the inventory regression.

Final verification extension: after the first frozen round, serialized replay exposed
a container-equality checker defect. See D007 and the preserved failed run. Protocol
v2 changes only exact-JSON replay validation plus fresh seeds; core numeric modules
are unchanged. The added 49th test accepts tuple-to-array serialization and rejects
a real 1e-6 numeric modification. V1 is retained as exploratory; v2 independently
repeats the complete intended task/policy/control grid. No method was tuned on v1.
