# Overnight research handoff — active

Repository: /Users/devikasv/dev/corrlaw; branch research/corrlaw-sprint-01.
Source checkpoint:87c5830. User authorized work until2026-09-22 08:00IST (02:30UTC).
New experiments stop01:30UTC; final hour is for audit/reporting. Original SPRINT
clock is preserved; OVERNIGHT overlay and wrapper enforce the earlier deadline.
The native goal is ACTIVE. The old finite-pilot completion does not finish this scope.

## Latest milestone — supersedes the earlier draft-install sequence below

Development002 completed all360 units with0executionfailures at20:46:44UTC,
duration5438.101186s. Its process/session ended normally; source87c5830 was unchanged
while it ran. All25 reviewed files from the install manifest have NOW BEEN INSTALLED
under a free runner lock. Do NOT reinstall the old draft manifest: original hashes
will correctly differ now. Full installed tests passed74 in6.58s.

Next command: run pysr-development-audit-002 through lab, timeout1800, invoking
`.venv/bin/python -m corrlaw.symbolic_audit results/runs/pysr-development-002
--output results/runs/pysr-development-002`. Then summarize and review complete
A/B results, profile100iterations using installed strong-development config,
audit/replay that profile, execute the two installed analytical/evaluator examples,
and finalize scope/protocol before v3freeze. No new CDEF PySR results have been seen.
The detailed earlier checklist below remains useful, but its installation/test steps
are COMPLETE. Installed source is authoritative; only PROTOCOL_V3 remains a draft.

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
  passed. Full installed suite is still required after integration (~74 tests).

## Watchdog

Idle-only same-thread daemon PID85026; scoped caffeinate PID85027. Read actual PID
file and health.json under work/overnight-watchdog. Queue acceptance was tested;
previous timed deliveries are retained. The daemon polls60s, nudges after15min of
no real progress, once per unchanged progress state, and ends at02:30UTC or STOP.
Respect any later user stop. No new sessions, messages to other people or unbounded
service. Availability is not guaranteed across app/host/service failure.
Details: notes/watchdog-operation.md. Stop the daemon when work completes.

## Exact next sequence after development finishes

1. Inspect run status/source provenance and confirm runner lock is free.
2. Review/install ONLY the25 mappings in work/drafts/install-manifest.json. Check
   every destination still matches its recorded original SHA256 (or remains absent)
   before copying. Do NOT blanket-copy old drafts. PROTOCOL_V3 is intentionally
   excluded because scope/runtime fields are unresolved.
3. Run full `.venv/bin/python -m pytest -q`, save a new test record. Inspect diffs;
   checkpoint explicit owned leaf paths, development artifacts and metadata.
4. Audit development with corrlaw.symbolic_audit; summarize into reports/pysr-development.
   The strengthened symbolic auditor is already installed; don't overwrite it with
   any stale file. Run through lab with a new audit ID and ample bounded timeout.
5. Run `pysr-strong-development-001` using installed configs/pysr-strong-development.json:
   A/B seed205, width0, noise.01, all5 policies,100 iterations,2048 pools/tests,10 units.
   Audit it and fresh-replay B-s205-w0-n0.01-constrained-augmented_qbc. This profiles
   the predetermined stronger budget before confirmation.
6. Run the tiny exact/evaluator checks through lab: `physical-prior-algebra-001`
   invokes examples/physical_prior_algebra.py; `representation-diagnostic-001`
   invokes examples/representation_diagnostic.py --parent results/runs/pysr-development-002.
7. Finalize current docs/PROTOCOL.md from work/drafts/PROTOCOL_V3.md; resolve every
   PENDING/DRAFT field and record full development/strong timing evidence and tests.
   Finalize primary/strong configs and scope BEFORE any new C/D/E/F outcomes.
   Commit inputs, create freezev3, verify, commit freeze metadata; then run confirmation.
8. After freeze, run declared full T16 search/prior diagnostics, full audits/replays,
   primary and stronger confirmation, exact replays, numerical report bundle, visual
   inspection, regeneration comparison, final report/claims/handoff/tests/gate.
   Ordering can adapt to resource/time, but only one heavy process may run.

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
