# Reporting checks for the overnight extension

- Call the main engine evolutionary symbolic regression over generic feature
  terminals. It is not a raw-variable-only PySR replication of the active-learning
  paper. Feature/library dropout is established prior work, as is disagreement
  acquisition. Retained-candidate history is an implementation choice, not novelty.
- All policy comparisons within an engine share their point-selection rule, search
  resources, noise streams, domains and budgets. Cross-engine changes are confounded
  by search, rational grammar, historical candidate retention and intervention
  fitness weights. Do not attribute every improvement to one factor.
- PySR searches and all accepted formulas use a common15-node arithmetic-tree
  cap over generic feature terminals. Expanded physical complexity differs because
  each terminal can represent a monomial. The superseded10/31 cap mismatch was
  corrected before confirmation; interrupted development001 is preserved. The
  grammar contains F via rational composition, unlike the original finite span.
  Representation does not guarantee successful search.
- A successful process is not enough: require complete expected units, hashes,
  independent recalculation of equations/metrics/queries, and exact substantive
  fresh-process replay. Preserve failed tie audit002; do not silently relabel it.
- Accepted alternatives satisfy declared empirical tolerances. RMSE<=.002+3*sigma
  is NOT a calibrated likelihood test, posterior credible set or global physical
  validity guarantee. Rational expressions are checked on finite public inputs;
  hidden-test failures must remain visible. No global absence-of-poles proof.
- Symbolic cancellation may fill removable singularities; saved canonical expression
  is the evaluated model. Numeric and six-decimal rounded recovery are distinct.
- Candidate sets are not independent posterior draws. Literal equation deduplication
  can retain algebraically equivalent presentations; equal-weight committee variance
  is an acquisition heuristic. Do not interpret its spread as calibrated uncertainty.
- All policies execute witness instrumentation for diagnostics. Timing includes this
  extra work even for policies that never use witnesses; report augmentation time
  separately. Julia cold-start is charged to the first trajectory, and process peak
  memory is cumulative rather than attributable to individual policies.
- Acquisition weights deliberately retain sparse new evidence; calibration labels
  select/filter candidates but do not enter PySR fitness. All labels count (192+q).
- Restricted-query negative controls may find alternative equations but cannot
  obtain off-surface evidence. Their actual query coordinates and persistent hidden
  errors matter more than a particular diagnostic label.
- Origin knowledge excludes1+v^2 but not all cubic circle aliases. Under origin and
  evenness, a degree<=3 polynomial dictionary collapses to u^2,v^2. That strong
  restricted class explains any trivial initial recovery; no universal uniqueness.
- Reused pilot search diagnostics are exploratory and hold acquisition trajectories
  fixed. Exhaustive <=3-support search changes search/complexity breadth; it is not a
  rerun of the five-policy experiment or a newly held-out result.
- Summary means/ranges use seeds as units. Keep width/noise/control results visible;
  do not turn hundreds of correlated policy conditions into independent replicates.
- Novelty has not been established. A useful negative result or a transparent
  benchmark/ambiguity-explanation tool is an acceptable conclusion.

- The .002 absolute fit-tolerance floor also applies at zero injected noise. Near-
  preparation alternatives accepted under that floor are approximately compatible,
  not literally indistinguishable from exact noiseless measurements. Do not turn
  numerical optimizer tolerance into a structural-identifiability theorem. Exact
  algebraic circle/line relations are separate supplied analytical statements; a
  floating fitted/normalized witness is only verified to its recorded residual.

- The saved-committee diagnostic compares ordinary and augmented disagreement on
  identical augmented-policy histories. A spread-threshold crossing does not correct
  the unchanged point model, imply calibration, or prove better queries. Adding
  central/equivalent committee members can reduce variance; report both directions.
- D-optimal here means regularized information gain in the declared linear feature
  dictionary. It is a comparator for geometric directions, not a solution to
  nonlinear optimal design over every rational formula in the PySR search class.
- Origin, coordinate parity and global positivity still admit the explicit degree4
  alternative U+alpha*r²*(r²-1),0<alpha<=1. Strong degree3 prior-control recovery is
  therefore class-dependent; sampled-probe positivity cannot replace this algebra.

- Log-scale error curves use a1e-10 display floor only. Saved values, tables and
  statistical summaries retain their original numerical errors without clipping.
