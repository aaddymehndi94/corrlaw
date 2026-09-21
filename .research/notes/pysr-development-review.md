# Revised PySR development review

Run `pysr-development-002`: all 360 A/B policy trajectories completed, zero execution
failures, 5438.101186 seconds. Source87c5830 remained unchanged. The subsequent
`pysr-development-audit-002` passed after879.641036 seconds:193650 candidate records
and15062 witness records, no errors. Records across budgets/policies are repeated
algorithm artifacts, not independent discoveries. The audit reconstructs inputs,
labels, candidate fits/classes, random streams, witness construction and queries.

`reports/pysr-development` contains all controls, condition CSV, seed-level summaries
and error curves. The PNG was visually inspected: both task panels, labels and
shared legend are legible, and the large A spike remains visible without clipping.
The1e-10 plotting floor is display-only; numerical metrics are unaltered.

Constrained mean AUC for A: augmented1.11568, ordinary QBC1.11590, diversified.00620783,
D-optimal.00636089, random.0112494. For B: augmented.0521975, QBC.0523984,
diversified.0531318, D-optimal.0617576, random.0717262. These three-seed development
means do not establish a general acquisition advantage or a confirmation result.

A's high ordinary/augmented AUC is driven by the same noisy exact-preparation
seed202 trajectory: at budget2 a15-node rational point model has off-RMSE106.518539
and same-preparation RMSE.002071285, despite admissible observed fit/calibration
errors. Both trajectories have AUC19.974498. Saved committee spread19.435965 is high,
so this is NOT false consensus under the declared threshold. Full selected equation
and recorded fit errors: `development-rational-spike.json`. This post-hoc development
inspection neither excludes the case nor adds a hidden-outcome model filter.
Finite-value checks do not provide global boundedness/pole-freedom guarantees.

A separate selected B201 exact/noiseless representation limitation is declared in
`representation-limitation.md`; its ordinary committee is already broad. The
reproducible evaluator-side example remains to be executed through the wrapper.

Resource choice will use this complete run and the100-iteration A/B profile before
any new C/D/E/F outcomes. Later development trajectories averaged about18 seconds;
peak batch RSS2.353GB. No constant-throughput guarantee is assumed. Freeze the
predeclared method unchanged; restrict the new confirmation grid for runtime rather
than tuning it to the observed development performance.
