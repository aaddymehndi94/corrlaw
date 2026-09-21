# Final skeptical audit — 2026-09-21

Final primary evidence: confirmation-v2-001, 1,000 complete policy units; validated
all paired initial/evaluator hashes, eight distinct acquired IDs, measured values,
total label counts, scored off-errors and 91,325 accepted alternative records.
The failure ledger is empty for execution failures. Scientific poor fits and large
hidden errors remain in the numerical results; they were not erased as exceptions.
Runner run.json retains its default NOT_REVIEWED field; the dedicated validation.json
and audit run are the scientific review evidence, without rewriting run history.

Fresh-process reproduction: reproduce-v2-001 exact canonical scientific JSON match
for preselected C-s92001-w0-n0.01-constrained-augmented_qbc. Excluded fields are only
runtime_seconds, fitting_seconds, augmentation_seconds and cumulative process RSS.
The earlier tuple/list false negative is preserved; no numeric tolerances were relaxed.
Regression test includes rejecting an actual 1e-6 metric change. All 49 tests pass.

All five generated report artifacts match byte-for-byte in a separate regeneration
folder. The final PNG was visually inspected: titles, axes, legend and seed ranges
are legible, with no overlap. Link checks on README and REPORT find no missing local
files. Report figures aggregate only the planned constrained grid; all controls,
conditions and individual paired seed scores remain linked.

Fairness/leakage: no numerical method changes between v1 and v2; learner modules
never import oracle/evaluation; broad public probes are unlabeled; no hidden-label
feedback; all 192 initial labels count. Baselines share point predictor and labels;
committee augmentation/feature dropout affect query selection only. D-optimal shares
the library and uses a stable information solve. Absolute residual tolerances are
explicit, uncalibrated engineering choices. Witnesses can miss ambiguity when the
library is inadequate; poor fit is kept distinct in records.

Interpretation: on the final constrained suite augmented mean AUC is worse than
all three active baselines on all four tasks. It improves relative to random on
average. This is scoped negative evidence, not a proof that augmentation never helps.
The 47/80 first-query match with D-optimal supports partial overlap, not identity.
Task E search failures and task F misspecification must remain visible. No physics
discovery, novelty, independent peer validation or publication claim is justified.

Source verification: v2 checks live against its freeze. V1's original 34 frozen
files verify against their historical commit (reports/audit/revision_provenance.json).
No methods or metrics were changed after the final v2 confirmation. No active jobs
remain after the final audits; no pushes, remote changes, paid services or extra
Codex sessions were used. Local Git progress checkpoints preserve the evidence.
