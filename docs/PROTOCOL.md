# CorrLaw experimental protocol
Status: READY_TO_FREEZE
Protocol ID: v3

All decisions resolved: YES. Finalized after audited A/B development and stronger-
search profiling, before any new C/D/E/F PySR confirmation outcomes.

## Question and evidence tiers

Do explicit bounded alternative equations expose misleadingly small committee
disagreement, and do they improve acquisition beyond random sampling, ordinary QBC,
feature-diversified QBC and regularized D-optimal? These are distinct questions.
No positive, novel or publication-ready outcome is assumed. All measurements are
simulated from the ideal systems in [BENCHMARKS](BENCHMARKS.md).

The primary extension uses actual deterministic serial PySR over generic normalized
features, described in [METHOD_PYSR](METHOD_PYSR.md). It is not raw-variable-only
PySR or a direct replication of a published active-learning implementation. The
finite-library v2 pilot remains historical evidence under its [archived protocol](PROTOCOL_V2.md);
its results are not pooled with PySR results.

Development uses A/B only: `configs/pysr-development-v2.json`, seeds 201–203,
widths 0/.01/.05, noise 0/.01, every policy and control (360 trajectories). A separate
A/B seed 205 run on noisy exact preparations profiles the predetermined 100-iteration
budget. The earlier 10-node search /31-SymPy-node acceptance rule was superseded
before ANY new C/D/E/F PySR confirmation. Its smoke records and interrupted 224-unit
development001 remain preserved. Revised searches and every accepted equation use
the same 15-node arithmetic-tree cap.

## Binding physical and numerical contract

[BENCHMARKS](BENCHMARKS.md) defines equations, output scales, domains, preparation
distributions and controls. Every policy receives the same incomplete priors:
anonymous dimensionless columns, domain, feature/operator/complexity limits, noise
and output scale. Positivity, symmetry, known boundary values and full physical
units are not primary-study inputs. Stronger-prior diagnostics are separate.

Full dimensional homogeneity, only the two named inputs and no additional
dimensional parameters already fix the monomial powers for A/C/D. This limits the
physical-discovery interpretation of a generic dimensionless benchmark. D-optimal
here is the regularized linear-feature information criterion on the shared
dictionary, not a solution to nonlinear optimal design over every rational PySR
formula. The witness search uses the same feature space; actual outcomes and query
agreements are reported without claiming universal method equivalence.

Each policy starts with 128 fitting and 64 calibration labels, then may acquire 8
nonrepeated query IDs. Pools have 2048 candidates;512 independent public unlabeled
box probes set feature scales; each same/off-preparation hidden test has 2048 points.
Gaussian query noise is fixed by candidate ID and paired across policies. Labels
are recomputed after input perturbations and shuffles. Calibration labels select
and filter models and count toward the 192 initial measurements. Hidden labels,
oracle derivatives and preparation formulas never enter acquisition. The coding
agent knows the benchmark; interface separation and hashes do not make it blind.

Each refit uses one full-data and two bootstrap searches, two populations of 20,
binary operators +,-,*,/, no unary operators, precision 64 and serial deterministic
execution. Primary iteration cap:30; secondary cap:100. The per-search safety
timeout is 30 seconds. Search and acceptance arithmetic-tree caps are both 15;
numeric atoms have absolute value at most 20. Acquired rows always survive
bootstrapping and have total fitness weight 128. Full-data candidate history is
retained and rescored on current measurements. Diversification changes bootstrap
feature subsets only; all policies share point selection on identical histories.
The historical finite/prior diversified policy performs18 paths versus9 for others;
its extra ordinary point-model fit is included in recorded costs (METHOD.md). The
new PySR policy comparison matches every policy at three searches per refit.
Exact tie, retention, fitness and acquisition rules are binding in METHOD_PYSR.

Admissibility requires fit/calibration RMSE<=.002+3σ and maximum acquired residual
<=.002+4σ, with common class limits. The .002 floor at zero injected noise permits
approximate compatibility; it is not exact observational indistinguishability.
Witnesses use two/three-feature Gram eigenvectors, public-probe RMS normalization,
observed residual ratio<=.1, alpha {-1,-.25,.25,1}, and at most 12 accepted directions.
Both equations must pass the same class and fit checks. Finite public checks do not
prove global pole-freedom, positivity or physical validity. No-witness does not
certify uniqueness; committee spread is not calibrated model confidence.

## Confirmation grid and preselected replay

The primary file is `configs/pysr-confirmation-v3.json`: C/D/E/F, seeds93001–93005,
widths0/.01, output noise.01, all five policies, constrained preparations plus
independent-input, shuffled-marginal and surface-restricted controls at width0.
This is500 policy trajectories (100 paired task/seed/condition trials).

The secondary file is `configs/pysr-confirmation-strong-v3.json`: C/D/E/F, the same
five seeds/policies, constrained width0, output noise.01,100 iterations per search.
This is100 trajectories, fully paired with the corresponding primary conditions.
Noiseless output and width.05 are omitted from new PySR confirmation to fit the
bounded overnight budget; both remain in A/B development, and the historical finite
confirmation retains noises0/.01. Stronger-search near-width.01 is not included.
These scope choices were made before any new C/D/E/F PySR outcomes, using A/B
resource evidence only; they are not selected favorable subsets of confirmation.

The360-unit revised development completed in5438.101186s (90.6min); later task/seed
blocks averaged about18s per trajectory, with peak cumulative RSS2.353GB. Its full
audit checked193650 candidate records and15062 witness records without errors.
The ten-unit100-iteration A/B profile completed in286.047903s, with25.034s mean
excluding the59.611s startup trajectory and27.826s maximum excluding startup.
Its artifact audit checked all ten units; the preselected replay and exact counts
are recorded in the finalization evidence below. A500-unit primary at22s/trajectory
and100-unit secondary at30s/trajectory would take about233min, leaving a buffer
before the01:30UTC experiment cutoff when started near21:15UTC. This is a planning
estimate, not a guarantee: later process costs grew, and CDEF can differ from A/B.
All runs remain subject to the absolute cutoff; unforeseen incompleteness must be
reported rather than dropped from a favorable aggregate.

Primary replay: `F-s93001-w0.01-n0.01-constrained-augmented_qbc`.
Secondary replay: `E-s93001-w0-n0.01-constrained-augmented_qbc`.
Use fresh processes and exact scientific JSON equality, excluding only timings/RSS,
including nested per-search timings. No rounding or relaxed tolerance may excuse a
mismatch. Preserve any failed record and diagnose it explicitly.

The stronger tier is secondary compute sensitivity, not a replacement selected for
favorable results. Its initial data, pools, probes and noise must match corresponding
primary conditions. Compare ONLY matched conditions across iteration budgets. Report
each tier separately; do not compare its narrow mean with the wider primary mean
or pool them as independent replications. Unexpected timeouts imply an incomplete
tier and must remain visible, without fabricated scores or favorable-case exclusion.

## Endpoints and aggregation

Primary endpoints are off-preparation RMSE in the fixed output reference scale 1
and trapezoidal AUC over budgets 0/1/2/4/8, divided by 8. No normalization by hidden
variance. Show every policy on each task. Average constrained width/noise conditions
within each seed, then report the mean and all five seed values/ranges. Paired deltas
are augmented minus comparator; negative favors augmentation. Seeds are statistical
units, not hidden test points, committee members or repeated conditions. No p-values,
population-wide superiority or broad null-effect claim is planned for this small suite.

Also report same-preparation error, six-decimal rounded symbolic recovery (distinct
from exact floating-point equality), witness coverage, poor fit, false consensus,
execution failures, first-query agreement, labels, runtime and separately timed
witness construction. False consensus uses unchanged off-RMSE>.1 and committee
RMS spread<.05. Consult poor-fit/singleton flags separately. Restricted pools test
the absence of feasible off-surface measurements; independent and matched-marginal
shuffled controls test preparation dependence.

A predeclared saved-committee diagnostic compares ordinary search and augmented
spread on IDENTICAL augmented-policy measurement histories and point predictions.
Reconstruct saved equations at budgets 0/1/2/4/8; use existing thresholds without
tuning. Record both upward/downward spread crossings and high-error/low-spread flags
removed/added, by task, control, budget and seed, retaining width/noise rows. Separate
removed flags with valid observational fit from poor-fit fallbacks. A threshold
crossing does not improve the fixed predictor or establish better acquisitions.
Later histories follow augmented QBC, not the different ordinary-QBC trajectory.
See `.research/notes/committee-diagnostic-plan.md` for the declared analysis.

## Separate exploratory diagnostics

These follow the negative finite pilot and are not fresh held-out confirmation.
The frozen `.research/notes/diagnostic-plan.md` declares three studies:

1. Exhaustive supports of sizes 1/2/3 on archived v2 CDEF constrained observations:
   all five seeds/policies, widths 0/.01, noise 0/.01, budgets 0/2/8 (1200 rows). Use the
   same anonymous numerical interface, dictionary, coefficient cap, ordinary least
   squares and original score plus 1e-8 per term. Hold acquisition histories fixed;
   this changes search/support breadth, not the original query policies. F remains
   outside the finite linear span. Save selected equations and original/recomputed
   metrics. Exact support replay: noisy exact-preparation augmented E seed 92001,
   budget 2 (`E-s92001-w0-n0.01-constrained-augmented_qbc`).
2. B physical-prior controls: seeds 301–305, widths 0/.01, noise 0/.01, all five policies,
   and three shared priors (none; known zero at origin; origin plus coordinate
   evenness),300 trajectories. In the degree<=3 dictionary the strongest prior
   leaves only u²,v². Origin alone excludes1+v² but allows odd cubic circle aliases.
   No universal uniqueness follows. Exact replay: noisy width .01 augmented B seed 301
   under `zero_origin_and_even` (`B-s301-w0.01-n0.01-constrained-augmented_qbc`).
3. Descriptive positivity sensitivity: evaluate both saved witness equations on 512
   public box probes, with 1e-10 rounding slack; record condition coverage and counts.
   No new acquisitions or primary filter. Finite-probe passes are not global proofs.

These results may not tune the frozen PySR comparison. Dimensional balances and
polynomial/rational prior counterexamples are separate elementary analytical
controls under explicit assumptions, not new physical laws or algorithm outputs.
The degree 4 circle alternative illustrates why stronger-prior degree 3 recovery is
class-dependent. Its algebraic checks and the series-family example are recorded
by `examples/physical_prior_algebra.py` and the physical-prior class note.

## Execution and validation

One heavy process, CPU only, at most four requested numerical threads; Julia is
serial. User-authorized hard deadline:2026-09-22 02:30UTC (08:00IST). New experiments
stop at01:30UTC; the last hour is reserved for audit/reporting. Preserve the original
SPRINT clock and apply the earlier overnight overlay. The wrapper exports a bounded
per-run cutoff rather than embedding a historical date in reusable science code.
Use the audit phase for validation/replay, never to relabel a new research sweep.

Save complete units atomically with hashes; resume requires identical configuration,
source and verified prior artifacts. Preserve failed/interrupted runs. The audit
checks expected/completed sets, paired inputs/labels, candidate errors/class limits,
bootstrap streams, full witness construction, query rankings, metrics and common
point models on identical histories. Exact fresh-process replay and byte-identical
regeneration of numerical summaries/figures are completion requirements. A successful
process exit alone is insufficient. Peak RSS is cumulative, first-trajectory time
includes Julia startup, and all policies perform witness instrumentation. Timings
are descriptive, not isolated speed benchmarks.

Commit the primary/secondary configurations, methods, evaluator/auditor code, tests,
benchmark/protocol/method documents, diagnostic plans and resolved dependency records
before creating freeze v3. Do not edit source/config during a run. After opening new
confirmation outcomes, a scientific bug requires preserving and invalidating affected
evidence, a versioned correction and fresh seeds. It cannot be silently repaired on
the same seeds and described as new confirmation. Self-review and provenance checks
are not independent peer review. Pushes, publication and paid services are disabled.

## Deliverables and finalization evidence

Produce per-task constrained error curves with seed ranges, all-control/condition
tables, paired seed AUC differences, matched iteration-budget comparisons, saved-
committee diagnostics, physical-prior results, exhaustive-search diagnostics,
positivity coverage, and preselected first-witness illustrations. Link every claim
to a run/source and separate analytical controls, development, confirmation,
exploratory diagnostics and limitations. No manuscript or novelty claim is planned.

Finalization evidence: revised development360/360 valid (193650 candidates and
15062 witnesses checked). Strong development10/10 valid (8392 candidates,64 witnesses
checked); preselected B-s205-w0-n0.01-constrained-augmented_qbc reproduced exactly in
pysr-strong-development-replay-001, scientific SHA256
19bd3facc14fcfa46d6524d24786e2cb966c6824b68a049c218eb8c4b34790f8.
The physical-prior exact algebra and selected development representation diagnostic
completed successfully under their immutable run IDs. The installed suite passed
74 tests in6.47s (`.research/notes/overnight-prefreeze-tests.txt`). Both finalized
configuration loaders pass and enumerate exactly500/100 units. Freeze v3 records
the committed input hashes and source commit; it is created after this READY protocol
is committed, before either confirmation run starts.
