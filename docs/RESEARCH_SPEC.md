# CorrLaw scientific specification

This is the scientific contract, not a second agent controller. Execute it using `CODEX_PROMPT.md` and `docs/WORKFLOW.md`. All numerical measurements are simulated. No empirical research result or novelty claim is established by this specification.

## 1. Mission and research claim

Investigate this question:

Can an inexpensive ambiguity detector find plausible alternative equations that a symbolic-regression ensemble missed because its observations lie near a lower-dimensional sampling surface, and can those alternatives guide useful new measurements?

The proposed method is a near-nullspace-augmented equation committee. Its novelty and usefulness are hypotheses, not facts. Do not claim to invent active learning, ensemble uncertainty, identifiability analysis, or optimal experimental design. Do not claim to discover a new law of nature. We are testing reliability of computational law discovery using known simulated physics.

Primary comparison: ordinary equation-disagreement sampling versus the augmented committee, with random sampling, diversity-enhanced committees, and regularized D-optimal design as serious competing baselines. A useful negative result is acceptable.

## 2. Execution boundaries

Use the existing repository, the ten-hour recorded deadline, the single-lead workflow, local Git checkpoints, and recovery rules in `AGENTS.md` and `docs/WORKFLOW.md`. No paid APIs, cloud compute, laboratory work or new orchestration platform. The agent implements the research; the supplied helper records and bounds commands.

## 3. Read the closest work before claiming novelty

Review the relevant methods and limitations in these primary sources. Spend at most 30 minutes on targeted additional literature checking; use what is actually accessible and record any inaccessible full texts.

- SRSD: Rethinking Symbolic Regression Datasets and Benchmarks for Scientific Discovery. https://arxiv.org/abs/2206.10540 and https://github.com/omron-sinicx/srsd-benchmark
- Active Learning in Symbolic Regression with Physical Constraints. Read the revised paper, not only its original abstract. https://arxiv.org/abs/2305.10379
- Ensemble-SINDy: Robust sparse model discovery in the low-data, high-noise limit, with active learning and control. https://arxiv.org/abs/2111.10992
- Materials-Discovery Workflows Guided by Symbolic Regression: Identifying Acid-Stable Oxides for Electrocatalysis. Relevant here for ensemble overconfidence and feature dropout, not its expensive materials calculations. https://arxiv.org/abs/2412.05947
- Experimental Design for Missing Physics. The arXiv record also lists an IFAC-PapersOnLine journal/proceedings reference; verify the linked publication rather than assuming it is unpublished. https://arxiv.org/abs/2604.01231
- Attractor Geometry Determines the Identifiability Limits of System Discovery, submitted 20 July 2026. https://arxiv.org/abs/2607.18490
- PySR official repository and documentation. https://github.com/astroautomata/PySR and https://ai.damtp.cam.ac.uk/pysr/

Update `docs/RELATED_WORK.md`: citation, actual contribution, overlap with this project, and a narrow possible remaining contribution. Distinguish preprints from reviewed publications. Verify bibliographic details rather than inventing them.

Specifically investigate whether the proposed augmentation is equivalent to an existing optimal-design or linear uncertainty method. If it is, acknowledge that equivalence and benchmark the existing method. Do not rename established mathematics and call it novel. If the exact repair already exists, focus on a reproducible comparison or uncovered failure condition within this same project, not an unrelated pivot.

## 4. Concrete physical benchmark and analytical sanity test

Use synthetic measurements from small algebraic physical systems. This deliberately gives the evaluator exact reference functions without requiring laboratory access.

Begin with this sanity case, written in dimensionless coordinates u and v:

    true reference: f(u,v) = u^2 + 2*v^2
    alternative:    g(u,v) = 1 + v^2
    observations:   u^2 + v^2 = 1

Their difference is u^2 + v^2 - 1, so they agree at every observed position on the unit circle. At (u,v)=(0,1/2), f=1/2 and g=5/4. A uniform angular sampling has zero population Pearson correlation between u and v despite the exact nonlinear dependence. Verify these statements independently with SymPy and numerical tests.

Physical interpretation: a dimensionless quadratic potential with different stiffnesses along two axes, sampled only at positions on a circle. The sampling restriction is an experimental preparation choice, not a universal conservation law. Off-circle preparations are permitted in this benchmark. State the energy-reference convention and supplied priors: imposing an additional known boundary value can exclude this particular alternative. Do not quietly withhold a prior from one method and give it to another.

This example and its algebra are sanity tests, NOT novel findings.

Register this small task suite before comparing methods:

A. Hooke force with variable stiffness and extension: y=u*v; initial preparation v approximately u. Development task.
B. Anisotropic quadratic potential: y=u^2+2*v^2; initial preparations near a unit circle. Development task.
C. Centripetal acceleration: y=u^2/v, with normalized speed u and radius v; initial preparation v approximately u. Confirmation task.
D. Kinetic energy: y=u*v^2, with normalized mass u and speed v; initial preparation v approximately u. Confirmation task.
E. Parallel ideal capacitances: y=u+v; initial preparation v approximately u^2. Confirmation task.
F. Series ideal capacitances: y=u*v/(u+v); initial preparation v approximately u. Confirmation and diagnostic-library-misspecification task.

Derive and record each dimensional equation, reference scales, dimensionless form, physically meaningful input bounds, and permissible independent controls. Constants absorbed by nondimensionalization must be documented. Treat these as idealized physical models with stated assumptions, not universal experimental descriptions.

Do not ask a learner to vary a quantity independently when the benchmark defines it as a derived quantity. Do not perform interventions outside a model's declared validity domain.

For positive-variable tasks, use bounded, order-one positive inputs away from singularities. For the potential, allow signed coordinates over a bounded square covering the ring and nearby positions. Set bounds without consulting results.

Use exact and near constraints. Start with dimensionless widths 0, 0.01, and 0.05, and output noise levels 0 and 0.01 in the declared output reference units. Specify the actual sampling distribution for each width. Generate a new noisy measurement by evaluating the true function at the perturbed input, then adding output noise. Perturbing inputs is not the same as adding noise to already-computed labels.

Include an independent-input control and a matched-marginal shuffled-input control. Recompute labels after shuffling. Distinguish input-range extrapolation from changing dependence within the same input bounds. Also test a query pool restricted to the original preparation surface: no method should claim that impossible off-surface information was acquired.

Minimum acceptable completion is both development tasks and at least two confirmation tasks, with repeated seeds and every mandatory acquisition baseline. Reduce grid breadth before sacrificing baselines or repeats. If that minimum is not completed, label the result a partial pilot. Do not describe the subset as the full suite.

## 5. Evaluator first, and no answer leakage

Implement separate benchmark/oracle, discovery, acquisition, and evaluation modules. The learning code receives anonymous numerical columns, allowed operators, declared scales/bounds, training measurements, calibration measurements, and an unlabeled candidate pool. It must not receive the reference formula, task identity, latent sampling equation, hidden test labels, or known rival formula.

The agent may know the benchmarks while implementing them. Therefore this is NOT a genuinely blind test of the coding agent. Prevent algorithmic leakage with clean interfaces, import checks, query logs, and frozen evaluation files; do not pretend a file hash provides adversarial isolation from an agent controlling the repository.

Suggested initial labeled budget: 128 fitting points and 64 calibration points, identical across policies. Use about 2,048 unlabeled feasible query candidates and an independently generated hidden off-protocol test set. All initial labels count as measurements; report additional-query savings separately from total data use.

Use independent random streams for development, confirmation, queries, and evaluation. Commit or hash the protocol, oracle, metrics, seed list, and confirmation configurations before inspecting confirmation outcomes. Tune only on A/B development runs. Changes after confirmation inspection require a new protocol version and fresh confirmation seeds; mark earlier results exploratory.

Only the oracle may reveal new labels, and only for explicitly selected query IDs. Count every acquired measurement. Never provide oracle derivatives, normal directions, target-informed candidate ranking, or unqueried labels to a method. Fit all target-dependent preprocessing on the permitted observations.

## 6. Lean numerical implementation

Use NumPy, SciPy, SymPy, scikit-learn, matplotlib, pytest, and PySR where practical. Check the installed PySR API rather than copying outdated parameters. Pin actual working versions and record Julia/runtime versions.

Attempt a tiny PySR smoke test early. Bound installation/debugging attempts to about 25 minutes. If unavailable, finish a clearly labeled finite-library pilot with sparse regression; do not portray that fallback as a completed evolutionary symbolic-regression experiment.

First build a fast finite-library implementation for debugging and wider sweeps. Use a small, declared generic dictionary, such as low-degree monomials, plus bounded-domain reciprocal/Laurent features where valid. Keep the dictionary smaller than the initial sample count. Generate features by one rule, not task-specific insertion of the correct equation. Record which reference functions are representable and which are not.

Use sparse fitting and an ensemble obtained through bootstrap samples and/or multiple regularization settings. This is a finite-library baseline, not unrestricted discovery.

Then test PySR on a smaller preregistered subset using the same arithmetic grammar across tasks and several search seeds. Use bounded expression complexity and wall-clock limits. Reuse compiled Julia processes when supported. Save all candidate equations and search budgets, not just the winner.

Never deduplicate candidate equations merely because their predictions agree on the observational data: those aliases are exactly what we need to retain. Use algebraic simplification or predictions on unlabeled broader-domain probes to distinguish equivalence from observational agreement.

## 7. Proposed augmentation: search for explicit ambiguity witnesses

Given observations X and the generic dictionary Phi(X), find sparse feature combinations q(x) that are nearly zero on the observed preparation but not throughout the feasible input domain.

Start with SVD and sparse relations among small feature subsets. Normalize feature columns with RMS values from the public UNLABELED feasible pool, without centering away the constant column. Avoid unstable scaling by nearly zero training variance. Exclude algebraically identical features, but do not remove distinct features solely for being observationally collinear.

For plausible fitted expressions f_hat, construct bounded alternatives:

    f_alt(x) = f_hat(x) + alpha*q(x)

Normalize q on the unlabeled feasible pool. Choose a small, fixed grid of alpha values in normalized output units. Keep only alternatives that are finite, within the declared complexity/coefficient limits, satisfy equally supplied physical priors, and fit the available measurements within a preregistered tolerance. Choose this tolerance using development data and the supplied noise model, not hidden test outcomes. Explain its meaning; do not label it a calibrated posterior probability.

For near constraints, these are empirical ambiguity witnesses, not exact proofs. For exact constraints, an evaluator may separately verify a symbolic identity using the known preparation equation. The learner must infer its candidate relation rather than receive that equation.

Save each accepted witness: both expressions, observed fit errors, complexity, disagreement locations, and the assumptions under which they are admissible. Reject mere high-degree interpolation tricks outside the declared class.

Use the retained alternatives to augment the ordinary equation committee and select the next candidate by normalized prediction disagreement. Use the same disagreement formula for the unaugmented baseline so that candidate augmentation is the variable being tested. Acquisition must not use true prediction errors.

Critical interpretation rules:
- A small singular value alone does NOT prove a particular sparse physical law is unidentifiable. Demonstrate an admissible alternative.
- Failure to find an alternative is NOT proof of uniqueness.
- Structural identifiability, practical distinguishability at finite noise, and search-algorithm failure are different outcomes.
- A low-dimensional nonlinear preparation can have little or no pairwise Pearson correlation.
- A missing relevant dictionary feature can make the diagnostic miss ambiguity. Test and disclose that failure.

Use honest diagnostic states such as `ambiguity_witness_found`, `no_witness_within_search_budget`, `poor_observational_fit`, and `no_discriminating_query_in_allowed_pool`. Never output unsupported "physical law verified" confidence.

## 8. Acquisition baselines and fair budgets

Mandatory policies:
1. Uniform random sampling from the same permitted query pool.
2. Standard query-by-committee using plausible equations from the existing search/ensemble.
3. A diversity-enhanced committee using a documented feature/library-subsampling approach; credit relevant prior work.
4. Regularized greedy D-optimal design on the SAME generic feature dictionary, using a numerically stable information-matrix calculation.
5. The proposed near-nullspace-augmented committee.

Optionally add ordinary committee sampling mixed with a small fixed fraction of random exploration. Do not weaken existing approaches deliberately.

Compare cumulative additional-label budgets 0, 1, 2, 4, and 8. Refit using newly acquired labels, following the same update schedule for all policies. Pair policies by initial dataset, query pool, and reproducible measurement-noise streams. Resolve acquisition ties reproducibly. Keep feasible domains, physical priors, expression budgets, and fitting resources comparable; report augmentation overhead and total runtime.

Start with a tiny end-to-end run. Profile it before scheduling the main sweep. Prioritize complete paired comparisons over a large number of incomplete searches. Aim for at least five confirmation seeds where feasible; report actual counts and avoid strong statistical claims from tiny samples.

## 9. Metrics, controls, and decision rules

Before running confirmation, freeze these primary outputs:

- Held-out off-protocol normalized RMSE versus additional measurements, normalized using an explicitly declared scale, not a convenient hidden-test denominator.
- Area under the error-versus-query-budget curve, with a fixed definition.
- Error on a hidden same-protocol set, to distinguish fitting failure from a failure to generalize across preparations.
- Rate of small committee disagreement combined with large hidden off-protocol error. Call this a false-consensus diagnostic, not a calibrated probability.
- Frequency and validity of ambiguity witnesses, including false alarms under the specified controls.
- Runtime, timeouts, memory, total labeled measurements, and failed runs.

Secondary outputs: algebraic recovery where SymPy can establish equivalence, coefficient accuracy where meaningful, and agreement on a separately held-out dense domain. String mismatch is not mathematical inequivalence; finite-grid agreement is not a proof. Numeric coefficient tolerances must be chosen on development tasks.

Pair results by task and seed. Report every completed task and policy, failures included. Use uncertainty summaries at the task/seed level, not millions of evaluation points as fake independent replicates. Do not choose only the best seeds, change the main metric after seeing results, or treat noisy correlated resampling as independent evidence.

A potential positive result requires reproducible additional value beyond ordinary QBC and simple existing safeguards on confirmation tasks. Be explicit when D-optimal design or diversified ensembles match or beat the proposal. If the augmentation is equivalent to a classical criterion or produces no improvement, the correct conclusion is that this proposed method has not established a new advantage.

Do not declare victory for the already-known ring identity or for rediscovering textbook equations.


## 10. Prior assumptions and known-method equivalence audit

Explicitly distinguish a generic dimensionless regression setting from a setting
where extra physical priors are supplied. A model may be observationally admissible
without satisfying an unstated physical boundary condition. Supply each declared
prior equally to every method and record how candidates are filtered.

For the circle example, g(0,0)=1 and f(0,0)=0. If the energy reference is known to
make the potential zero at the origin, g is already excluded. Do not claim the
extra measurement is necessary under that stronger prior. Use the unprimed example
only under its declared incomplete-prior setting; add a prior-aware control where
feasible. The same care applies to symmetry, positivity, and dimensional knowledge.

Before a big sweep, analyze this potential overlap. For a committee consisting of
f_hat + alpha*q and f_hat - alpha*q with equal weights, the prediction variance is
alpha^2*q(x)^2. For a linear feature model, regularized D-optimal acquisition ranks
points through feature-vector leverage, and a dominant unobserved direction can
produce the same ordering. Derive the conditions and compare actual acquisitions.
This is an analytical comparison to establish overlap, not an asserted new theorem.
A method that merely reconstructs this known uncertainty mechanism has not established
novelty. Its useful contribution, if any, might instead be sparse admissible witnesses,
nonlinear candidate support, or a carefully scoped failure benchmark.

## 11. Testing and completion

Implement scientific tests for dimensional normalization, generator support and
singularities, fresh labels after shuffling/perturbations, reference formulas,
allowed interventions, anonymous learner contracts, split/query accounting, noise
pairing, symbolic equivalence, sparse witness admissibility and deterministic replay.
The starter's helper tests are not these scientific tests.

Use artifact/run schemas in `results/README.md`; every conclusion must link to actual
files through `.research/CLAIMS.md`. Freeze only an implemented, reviewed protocol,
not this draft design. Save all failed attempts. Keep timeouts separate from valid
negative findings and implementation errors separate from failed hypotheses.

Reproduce at least one substantive result from a fresh process and regenerate its
numbers/figures from saved artifacts. Record unresolved differences instead of
rounding them away. A re-run with a new stochastic result is not exact reproduction.

Finish `reports/REPORT.md`, portable dependency records, tests, code, configs,
small decisive equation/query/result artifacts, and `.research/HANDOFF.md`.
The minimum scope and evidence rules above still apply. Do not invent a paper,
claim a newly discovered physical law, push code, or publish without authorization.
