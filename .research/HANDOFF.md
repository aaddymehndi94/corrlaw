# Overnight research handoff — active

Repository: /Users/devikasv/dev/corrlaw; branch research/corrlaw-sprint-01.
Current source checkpoint:f4065cd; development002 used87c5830. User authorized work until2026-09-22 08:00IST (02:30UTC).
New experiments stop01:30UTC; final hour is for audit/reporting. Original SPRINT
clock is preserved; OVERNIGHT overlay and wrapper enforce the earlier deadline.
The native goal is ACTIVE. The old finite-pilot completion does not finish this scope.

## Latest milestone (21:12 UTC) — supersedes older pending items below

Both development runs are complete and audited. Revised360:193650 candidates,
15062 witnesses, zero audit errors. Strong10:8392 candidates,64 witnesses, zero
errors; fresh B205 noisy augmented replay exact19bd3fac... . Physical-prior exact
algebra and development representation scripts also completed successfully.
74 prefreeze tests passed in6.47s. Development PNG inspected. A's large mean error
is a retained rational spike at seed202/q2, not an execution failure or false consensus;
see notes/development-rational-spike.json and pysr-development-review.md.

Final protocol v3 is READY_TO_FREEZE in docs/PROTOCOL.md. Configs validated:
primary500 (CDEF,5seeds93001–93005,widths0/.01,noise.01,allpolicies/allcontrols);
strong100 (same tasks/seeds/policies,constrained width0,noise.01,100iterations).
Measured stronger profile286.048s, steadymean25.034s. Scope chosen BEFORE new CDEF.
No v3freeze or new CDEF outcomes yet. Next checkpoint inputs/evidence, freeze v3,
verify/checkpoint metadata, then primary500 and strong100 through lab, sequentially.
Installed source is current; do NOT reinstall old draft manifest. Cost disclosure
is installed in METHOD/checklist. Work/overnight-report-outline.md is a prose aid,
NOT a result. The remaining T16 diagnostics and final reporting steps below remain.

## Completed and preserved evidence

- T13 DONE: fair-smoke001 has10/10 units; fair-smoke-audit001 validated4379 candidates
  and460 witnesses, random streams, full witness search and actual acquisitions.
- fair-replay001 exactly reproduced B-s204-w0-n0-constrained-augmented_qbc in a fresh
  process. See notes/fair-smoke-validation.md and its reproduction.json.
- Searches and accepted equations now share a15-node arithmetic-tree cap. The earlier
 10-node search/31-SymPy acceptance mismatch was corrected BEFORE new confirmation.
  Development001 was deliberately interrupted at224 completed units and preserved.
  No new C/D/E/F PySR confirmation outcomes have been inspected. NO v3 freeze yet.
- Old smoke003/replay003 were valid under the former cap. Failed tie audit002 remains
  archived; lexical point-model ties were corrected before revised development.
- Installed suite passed67 tests at552f2f0. New draft committee/sensitivity tests
  passed5 checks; draft wrapper-deadline tests passed2; exact algebra draft assertions
  passed. The installed suite subsequently passed all 74 tests at f4065cd.

## Watchdog

Idle-only same-thread daemon PID85026; scoped caffeinate PID85027. Read actual PID
file and health.json under work/overnight-watchdog. Queue acceptance was tested;
previous timed deliveries are retained. The daemon polls60s, nudges after15min of
no real progress, once per unchanged progress state, and ends at02:30UTC or STOP.
Respect any later user stop. No new sessions, messages to other people or unbounded
service. Availability is not guaranteed across app/host/service failure.
Details: notes/watchdog-operation.md. Stop the daemon when work completes.

## Exact next sequence

1. Await `pysr-development-audit-002` (exec session 47149); inspect validation.json.
2. Add the finite/prior diversified-search cost disclosure from
   work/finite-compute-clarification.md to METHOD.md and the interpretation checklist.
   No numerical algorithm changes. Do this after the active audit ends.
3. Summarize the audited development into reports/pysr-development. Run the installed
   configs/pysr-strong-development.json as pysr-strong-development-001, then audit
   and exactly replay B-s205-w0-n0.01-constrained-augmented_qbc in a fresh process.
4. Run physical-prior-algebra-001 and representation-diagnostic-001 from the installed
   examples through lab. The latter takes --parent results/runs/pysr-development-002.
5. Finalize primary/strong scope from complete A/B timings only. Resolve the draft
   work/drafts/PROTOCOL_V3.md into docs/PROTOCOL.md and create final configs.
   Commit inputs, freeze v3, verify, commit freeze metadata. No new CDEF outcomes yet.
6. Run primary/strong confirmation and declared T16 diagnostics sequentially. Audit
   all, perform exact replays, render/inspect/regenerate the report bundle, write
   final report/claims/audit note, run final tests and completion gate, checkpoint.
   New experiments stop 01:30 UTC; audit/reporting stop at 02:30 UTC.

The 25-file integration and full 74-test installed check are already COMPLETE at
f4065cd. Do NOT reinstall work/drafts/install-manifest.json. Installed code is
current; draft duplicates are historical. Only PROTOCOL_V3 is still a pending draft.

## What the25 prepared mappings contain

New source: committee_diagnostic.py, compute_sensitivity.py, search_diagnostic_audit.py.
Modified execution code: symbolic_experiment.py and tools/lab.py replace the embedded
historical cutoff with a wrapper-owned absolute cutoff. The wrapper still bounds
both child and parent by the earlier authorized deadline; scientific numerics are
unchanged. New/updated tests are included. New tools: render_overnight.py and updated
completion gate. New examples: physical_prior_algebra.py, representation_diagnostic.py.
Strong-development config; METHOD_PYSR; archived PROTOCOL_V2; updated README; annotated
PILOT_REPORT (original bytes remain in Git, protocol link corrected). Plans/notes
cover committee diagnostics, physical class limits, skeptical review, encoding
limitation and updated interpretation checks. Older diagnostics/prior/positivity/
explain/CLI/summarize drafts were ALREADY installed at552f2f0; do not replace them.

## Scope and remaining run IDs

work/pysr-confirmation-scope-plan.md records pre-outcome options.1000 primary units
may be tight. Prefer considering noisy-only primary: CDEF, seeds93001–93005,
widths0/.01, noise.01, allcontrols and5policies =500 units. This retains tasks,
replicates, near/exact preparations and controls; explicitly disclose omitted
noiseless PySR confirmation. Stronger tier can be100 units (width0 only) or200
(widths0/.01), constrained/noise.01, same tasks/seeds/policies. Choose using COMPLETE
A/B and100-iteration timings before freeze. Do not select by confirmation outcomes.
Preselected primary replay F-s93001-w0.01-n0.01-constrained-augmented_qbc remains valid.
Strong replay E-s93001-w0-n0.01-constrained-augmented_qbc remains valid.

Planned IDs: pysr-confirmation-v3-001, pysr-confirmation-strong-v3-001,
pysr-reproduce-v3-001, pysr-reproduce-strong-v3-001; search-diagnostic-001;
prior-control-001; prior-reproduce-001. Prior replay is B-s301-w0.01-n0.01-constrained-
augmented_qbc under zero_origin_and_even. Search diagnostic: old finite v2 parent,
1200 rows; its new auditor replays E-s92001-w0-n0.01-constrained-augmented_qbc atq2.
Diagnostic designs are declared, exploratory, and must not tune the new main method.

The report tool renders all six summary families, both positivity and committee
analyses, matched compute sensitivity, and preselected first CDEF witnesses at the
FIRST CONFIGURED noise level. It also renders origin-only B. It checks input audits
and hashes. Run once to reports, once to a NEW work directory with --compare reports
--comparison-output reports/audit/overnight-report-regeneration.json. Byte equality
covers numerical tables/diagnostics/figures; prose is separately reviewed.

## Scientific limitations to retain

B seed201 exact/noiseless initial fit has0 witnesses although a known circle relation
fits. Its encoded alternatives cost19 arithmetic nodes; substituting the known
constant feature z0=1 gives equivalent9-node forms. This is a selected development
encoding/construction limitation, NOT discovered witnesses or a completed constant-
folding ablation. Keep the method unchanged and disclose no-witness≠uniqueness.
Saved scratch check: work/development002-representation-diagnostic.json.

Analytical controls: origin alone permits cubic circle aliases. In degree<=3,
origin plus local nonnegativity rules them out; origin+parity is the numerical
control. Degree4 U+alpha*r²(r²-1) survives origin, parity and global positivity.
A separate rational F family survives units, positivity, symmetry, zero-axis values
and monotonicity, while agreeing on the diagonal. Neither family is claimed as
an algorithm-generated15-node witness. Exact SymPy checks and stated assumptions
are in the prepared example/note. Full dimensional priors fix A/C/D monomial powers
under no-additional-parameter assumptions; reports/audit/dimensional-prior-algebra.json.

D-optimal is linear-feature information gain, not universal nonlinear optimal
design. Committee threshold crossings do not change the fixed predictor, prove
calibration, or establish query value. Cross-engine comparisons change several
model/search/weighting choices. All empirical tolerances and finite-probe limitations
must stay explicit. Reused v2 diagnostics are exploratory. No novelty/publication claim.

No pushes, paid APIs, cloud, global settings, discarded failures, or competing agents.

Latest presentation-only draft: summarize.py now uses one real panel for a one-task
prior report, with no empty second panel; multi-task figures remain unchanged.
Install manifest now has25 mappings. Mention1e-10 log-plot display floor in report;
CSV/JSON metrics are unclipped. Representation example ordinary spread=.435596,
9members,false_consensus=False; this is NOT an ensemble-overconfidence example.

BENCHMARKS.md draft now explicitly distinguishes finite-linear-span representability
(Fabsent) from PySR arithmetic-composition representability(Fpossible), and explains
the separate prior-control extension. No distributions/parameters changed.
Freeze the scientific method/benchmark/related-work documents, configs/src/tests/
tools/examples/dependencies and declared diagnostic plans; include the static
SPRINT/OVERNIGHT deadline records. Do not freeze dynamicSTATE/PLAN/HANDOFF orreport
outputs. Source remains unchanged during the active development run.

Complete development resources: notes/fair-development-resources.json. Later A/B
seed203 means17.74/18.03s per trajectory; peakbatchRSS2.353GB. Use conservative
later-run timing when finalizing main/strong scope; no guarantee of constant speed
in a longer Julia process. Audit is active; no source/config edits during it.
Review finding while developmentaudit runs: historicalfinite/prior diversifiedQBC
computes9ordinarypaths forcommonpointfit PLUS9diversifiedpaths (18vs9others). PySR
alreadyusesexactly3searches forallpolicies. DoNOTclaim equaloverallfinite compute.
Noalgorithmchangeplanned. Afteraudit andbeforefreeze, add costclarification from
work/finite-compute-clarification.md to docs/METHOD.md andfixbroadinterpretationchecklist
line. Reportlabel-efficiencywiththiscostdifference; oldaugnegativevsordinary/Dopt
isnotdependentontheextra-costdiversecomparison. Preservehistoricalruns/protocol.

21:04UTC milestone: development audit PASSED all360,193650 candidates,15062 witnesses,
0errors,879.641s. Summary generated and PNG visually inspected. Largest A AUC comes
from seed202 width0 noise.01, QBC andaug both19.974498; q2 offRMSE106.5185 but same
RMSE.002071. Full saved rational equation/fit record is in notes/development-rational-
spike.json. Preserve this valid high-error result untrimmed; no method change.
Strong development ACTIVE: pysr-strong-development-001, execsession71624, started
21:04:05UTC approximately, timeout1800. Audit/replay after it completes. Cost
clarification is now installed in METHOD.md and interpretation checklist.
