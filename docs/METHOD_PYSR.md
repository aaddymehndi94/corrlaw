# PySR feature-grammar active experiment

This extension uses actual evolutionary equation searches, while retaining the
[benchmark distributions](BENCHMARKS.md) and [finite-pilot metrics](METHOD.md).
It is not raw-variable-only PySR and is not a direct replication of a published
active-learning implementation. Read the frozen [protocol](PROTOCOL.md) for the
primary/secondary grid, seeds and status of each evidence tier.

Each search receives generic monomial/Laurent feature terminals, RMS-normalized on
512 public unlabeled box probes. There are17 terminals on positive domains and10
on signed domains; the same rule generates them for every task. Numerical inputs
contain no task names, reference formulas, hidden labels or preparation equations.
The raw-variable physical expression is saved after substitution of these terminals.
A terminal's arithmetic cost is one; this deliberately differs from counting every
operation in the expanded physical formula. Unlike a linear combination of these
features, rational arithmetic composition can represent the series-capacitance law F.

## Search and model selection

For every budget0 through8, run one full-data search and two bootstrap searches.
PySR settings: binary+,-,*,/; no unary operators; populations2; population_size20;
precision 64; serial deterministic execution;30iterations for the primary tier and
100 for the secondary compute sensitivity; timeout30seconds per search. Search
maxsize and accepted arithmetic-tree size are both 15. Integer powers cost repeated
multiplication; inverse factors group into division; subtraction does not add a
fictitious multiplication by-1. Every numeric atom has absolute value at most 20.
Only finite predictions on available measurements and public pool/probes are
accepted. This is not a global absence-of-poles or physical-validity proof.

Full-data searches use every original fitting and acquired row. Bootstrap searches
sample128 original fitting rows with replacement and always retain every acquired
row. Original rows each have fitness weight1; all acquired rows together have
weight 128, to keep a few new measurements from being overwhelmed by the original
preparation. Calibration labels select/filter candidates but are not search-fitness
rows. All192 original labels count toward measurement cost.

Candidates survive between refits, with every error recomputed against the current
permitted data. A prior fit or prior admissibility decision is never retained.
Equations are deduplicated by their saved canonical-expression string, not by
agreement on the preparation data. Algebraically equivalent presentations may still
remain; this committee is not a collection of independent posterior draws.
If a bootstrap expression subsequently appears in a full-data search it becomes
eligible for the common point predictor. Search provenance/generation is retained.

The point predictor minimizes fitting MSE + calibration MSE + acquired-point MSE
(when acquired rows exist) +1e-8 times arithmetic complexity among all current or
retained FULL-data-search candidates. Exact score ties use lexical expression order.
Bootstrap-only candidates never change this common point predictor. Policies with
the same measurement history therefore have the same selected point model.

## Committees, witnesses and acquisitions

Ordinary acquisition uses all candidates satisfying fit/calibration RMSE<=.002+3σ
and maximum acquired residual<=.002+4σ. If none do, use the singleton point predictor
and record poor fit. These are empirical tolerances, not a posterior or a calibrated
likelihood test. The .002 floor applies even at zero injected noise. Approximate
compatibility at that floor is not exact structural nonidentifiability.

Diversified QBC has the same full-data search and the same number of bootstrap
searches, but each bootstrap retains max(7,floor(.7p)) random feature terminals.
All other policies use the same full feature set in their three searches. Every
policy has the same operator, complexity, coefficient, population and iteration
budgets. There is no additional ordinary-ensemble search for diversified QBC.

Witness construction follows the same two/three-column Gram eigenvector search,
public-probe RMS normalization, residual-ratio<=.1, coefficient cap20, fixed
alpha {-1,-.25,.25,1}, and at most 12 accepted directions as the finite pilot. Both
base and alternative must meet the SAME15-node arithmetic cap and residual tests.
The fast numerical rejection screen has1e-9 slack to avoid rejecting a candidate
near the cutoff; final acceptance uses the serialized expression and original
thresholds without slack. Save both expressions, direction, alpha, errors,
complexity and maximum disagreement location for every accepted witness.

Acquisition policies are random, QBC, diversified QBC, regularized D-optimal, and
augmented QBC. Both QBC variants use population prediction variance in fixed output
units. Augmented QBC appends the witness equations to the ordinary committee.
D-optimal uses ridge1e-4 leverage on the same generic feature dictionary. All
policies draw ties from the same paired stream and may never repeat a query ID.
The point prediction reported for error remains the common full-data selection;
it is not silently replaced by the augmented committee mean.

## Recording and validation

Save every raw search hall-of-fame, bootstrap row, feature subset, fitness weight,
search seed, retained candidate, selected equation, witness, query coordinate,
label/noise ID, metric, timing and cumulative process peak RSS. All policies compute
witness instrumentation; separate that cost when interpreting operational timing.
Julia cold-start belongs to the first trajectory. Timing is descriptive.

Artifact audits rebuild the data, verify hashes and paired inputs, reconstruct
random streams, score every candidate, replay all witness construction, check the
query rankings and metrics, and compare point models on identical histories.
Preselected fresh-process replay compares exact scientific JSON; only timing/RSS
are excluded. A successful process exit is insufficient. Failed/partial/superseded
runs remain in the archive. Summaries use seeds as statistical units, with conditions
averaged within each seed; neither test points nor committee members are replicates.
