# Final audit acceptance checks — fixed before inspecting confirmation summaries

1. Freeze v1 verifies after the confirmation process finishes; source/config unchanged.
2. Manifest exactly covers 1,000 planned policy units and all five paired policies.
3. Recompute every saved query label, scored hidden error and both sides of every
   ambiguity witness; verify per-condition initial/evaluator hashes and label totals.
4. Fresh process reproduces the preselected C-s91001-w0-n0.01-constrained-augmented_qbc
   unit, including candidate coefficients, alternatives, metric values and query IDs.
   Ignore only wall-clock timings and cumulative process RSS in exact equality.
5. Regenerate summary JSON/condition CSVs/figures from saved unit artifacts; compare
   generated numerical and image bytes in a separate output directory.
6. Inspect all tasks/controls, failures, seed-level paired AUC changes, witness coverage,
   false-consensus diagnostics and D-optimal query agreement. Do not drop F.
7. Record limitations: finite dictionary, known simulated functions, incomplete priors,
   small task/seed suite, explicit singular-value/optimal-design overlap, missing
   reciprocal-of-sum term, limited PySR scope and uncalibrated diagnostic thresholds.
8. Complete report/claims/state/handoff/plan, then run completion_check.py and require
   complete=true. The in-progress gate correctly refuses completion while T09–T11
   and validation/reproduction/report artifacts remain outstanding.
