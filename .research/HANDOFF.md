# Overnight research handoff — ACTIVE

Repository /Users/devikasv/dev/corrlaw, branch research/corrlaw-sprint-01.
User deadline:2026-09-22 08:00 IST =02:30 UTC. New experiments stop01:30 UTC.
Original SPRINT unchanged; OVERNIGHT overlay and wrapper enforce earlier limits.
Native goal active. Old finite-pilot completion does NOT finish this extension.

## Current milestone and exact next action

Freeze v3 VERIFIED75 files at scientific input commit5e27579; metadata7f2f62a.
ACTIVE primary: pysr-confirmation-v3-001, PID90656, execsession47505,
started2026-09-21T21:14:39+00:00, timeout12600s, phaseconfirmation/freezev3.
Command uses corrlaw.symbolic_experiment --config configs/pysr-confirmation-v3.json.
Monitor completion; next strong100 before01:30UTC. Do not restart or duplicate it.
The main study is now open: no scientific source/config edits or outcome-based tuning.

One heavy process, <=4 numerical threads, serial Julia. Do not edit frozen source,
configs, tests, tools or scientific documents. Run IDs immutable; preserve failures.
All installed code is current. Do NOT reinstall stale work/drafts manifests.

## Frozen scope

Primary: CDEF, seeds93001–93005,widths0/.01,noise.01, all five policies and all
controls (nonconstrained controls at width0):500 trajectories. Stronger: same tasks,
seeds and policies, constrained width0,noise.01,100iterations:100 trajectories.
Both are actual PySR over generic feature terminals,3searches/refit,15-node search
AND accepted arithmetic caps. Primary30iterations.192initial labels plus8queries.

Scope chose output-noise.01 only for new confirmation using A/B timings BEFORE new
CDEF. Noiseless and width.05 remain in development, old finite has both noise levels.
Both final configs/protocol, methods/benchmarks, code/tests/tools/dependencies and
static diagnostic plans/deadline records are frozen. Dynamic state/reports are not.
Unexpected partial tiers must be reported, not cherry-picked or called complete.

## Completed evidence

- Revised pysr-development-002:360/360,0failures,5438.101186s, unchanged source87c5830.
  Audit002 valid193650 candidates,15062 witnesses,879.641s. Summary under
  reports/pysr-development; PNG visually inspected. Detailed review/resources in
  notes/pysr-development-review.md and fair-development-resources.json.
- Strong-development001:10/10,286.047903s; steadymean25.034s,max27.826s excluding
 59.611s startup. Audit valid8392 candidates,64 witnesses. Preselected B205 noisy
 augmented fresh replay EXACT19bd3facc14fcfa46d6524d24786e2cb966c6824b68a049c218eb8c4b34790f8.
- physical-prior-algebra-001 valid exact SymPy checks. representation-diagnostic-001
 reproduced the selected development encoding limitation. Both artifacts inspected.
-74 prefreeze tests passed in6.47s; notes/overnight-prefreeze-tests.txt.
- Common15-node fairness revision superseded old10search/31accepted cap BEFORE new
 CDEF. Interrupted development001 preserved224units. Fair smoke/replay001 passed.
 Failed earlier tie audit002 preserved; lexical tie correction predates this study.
- Installed paired committee, matched compute sensitivity and search-audit modules;
 report renderer and fail-closed overnight completion gate. No further code work planned.

## Remaining sequence (adjust order only for timing)

1. Primary500, then strong100 as pysr-confirmation-strong-v3-001 under freezev3.
   Before01:30 UTC also run search-diagnostic-001 and prior-control-001 (T16), both
   declared exploratory diagnostics. See module CLIs and configs/prior-control.json.
2. Full symbolic audits into each parent run; expected500/100. Fresh exact replays:
   pysr-reproduce-v3-001: F-s93001-w0.01-n0.01-constrained-augmented_qbc.
   pysr-reproduce-strong-v3-001: E-s93001-w0-n0.01-constrained-augmented_qbc.
   Use audit phase/freezev3 for validation; do NOT relabel new experiments as audit.
3. Prior three tiers each100units, audit each with corrlaw.prior_audit; exact
   prior-reproduce-001 on strongest tier B-s301-w0.01-n0.01-constrained-augmented_qbc.
   Search diagnostic uses oldfinitev2,1200rows; corrlaw.search_diagnostic_audit also
   exactly replays selected E-s92001-w0-n0.01-constrained-augmented_qbc atq2.
4. .venv/bin/python tools/render_overnight.py --output reports. Requires all complete
   input audits, hashes, and produces six summary families, positivity, same-history
   committee analysis, matched compute sensitivity and first-witness examples.
   CDEF examples preselected seed93001,width0,FIRSTCONFIGUREDNOISE(.01),firstwitness.
   Also origin-only B301w0n0. Report no-witness honestly when applicable.
5. Visually inspect figures. Rerender to NEW work directory with --compare reports
   --comparison-output reports/audit/overnight-report-regeneration.json. It checks
   actual numerical tables/diagnostics/figure bytes; prose reviewed separately.
6. Rewrite reports/REPORT.md, append CLAIMS evidence, final audit note, tests,
   task statuses/handoff. Run tools/overnight_completion_check.py; livefreezev3
   verification and exact replays are required. Local exact-path checkpoints only.
7. Stop watchdog and verify its scoped caffeinate exits. Mark native goal complete
   only for achieved scope; if deadline prevents completion, state partial honestly.

## Scientific review points to retain in final report

- A202 noisy exact development, q2: ordinary andaug bothoffRMSE106.518539,
  sameRMSE.002071285, AUC19.974498. Valid rational point model; retained untrimmed.
  Committee spread19.435965 is high, so NOT false consensus. Full saved expression
  in notes/development-rational-spike.json. Do not invent a pole proof; finite-value
  checks are not global pole-freedom. No method tuned to hide this outcome.
- Selected B201 exact/noiseless has0addedwitnesses: encoded circle alternatives cost19,
  constant-feature folding gives equivalent9-node forms; no folding ablation performed.
  Ordinary committee9members/spread.435596,false_consensus=False. This is a post-hoc
  development construction limitation, NOT an overconfidence example.
- Finite/prior diversified baseline computes18paths versus9others (ordinarypointfit
  plus extraensemble); recorded fittingcost includes it. PySRmatches3searchesforall.
  METHOD/checklist explicitly disclose this. No blanket equal-compute claim.
- Strong origin+parity prior reduces degree<=3Bdictionaryto u²,v². Origin alone
  permits cubic aliases. Origin+localpositivity identifies exactcircledegree<=3,
  but degree4 U+alpha*r²(r²-1) survivesorigin/parity/globalpositivity. Class-dependent.
- F analytical rationalfamily retainsunits/positivity/symmetry/zeroaxes/monotonicity
  butagreesdiagonal; not an algorithm15-nodewitness. Precise small-input limit would
  exclude it. Full units/noextra parameters fix A/C/Dmonomialpowers; no discoveryclaim.
- Same-history spread threshold changes do not correctfixedmodel or prove queryvalue;
  report both crossingdirections and poor-fitflags. Spread is notcalibratedconfidence.
- Dopt is linear-feature criterion; crossenginegrammar/search/retention/weights differ.
  Reusedfinite supportdiagnostic is exploratory, historiesfixed,Fmisspecified.
- Empirical tolerances incl.002zero-noisefloor, finiteprobechecks, numericstringdedup,
  possiblealgebraicallyequivalent members, physicalincompletepriors, tinyseedcounts.
  No novelty/newlaw/publicationclaim. Self-review is not independentpeerreview.
- Timingincludescommonwitnessinstrumentation/Juliafirststartup; RSScumulative;
  lateprocesscosts grow. Plotfloor1e-10displayonly, numericaltablesunclipped.

## Watchdog and recovery

Idle-only same-thread daemon85026; scoped caffeinate85027. ActualPID/health under
work/overnight-watchdog. Poll60s,nudgeafter900s no REAL progress, once per unchanged
progress state. Stops at02:30UTC or STOPfile. Queueacceptancetested, no newagents/sessions.
See notes/watchdog-operation.md. App/host/service availability is not guaranteed.
Userstop overrides. No routine permissionrequests, pushes, paid/cloud/globalchanges.

Historical finitepilot:1000validv2units, exactreplay, negativeagainstactivebaselines;
reports/PILOT_REPORT.md and docs/PROTOCOL_V2.md archived. Old v2 livefreezenowdiffers
becauseextensioncodechanged; historicalbytesremain inGit. Oldcompletiongate does
NOTcomplete overnight. Current REPORT stillneedsrewrite. Work/overnight-report-outline.md
is only a prose aid with placeholders, not a finished result. Full earlier state
and superseded methods are preserved in localGit commits, nothing pushed.

First primary seed completed100/500,0executionfailures; resource-only review in
notes/confirmation-first-seed-resources.json. Report is now an honest IN-PROGRESS
landing page; archived pilot preserved. CLAIMS now includes verified development/
analytical C019–C027, no unaudited new confirmation claims. These report/ledger
updates are uncommitted while the runner lock is active.
After primary, consider running the short frozen exploratory T16 search/prior
studies before strong100 to reserve their completion; ordering may adapt to time,
scientific scope cannot. Strong timeout5400s can be bounded by absolute01:30cutoff.
No new experiments after01:30; audits/replays/reporting may use auditphase until02:30.

Final audit addition (read-only consistency check, no method change): after the
three prior-control tiers complete, verify identical unit-ID sets and matching
initial_data_hash/evaluation_hash across none/zero_origin/zero_origin_and_even for
each corresponding unit. Save reports/audit/prior-pairing.json and cite it when
interpreting prior effects. Individual prior audits reconstruct inputs, but this
explicit cross-tier check makes the shared-data comparison directly reviewable.

Latest primary milestone:300/500, first3complete seeds,0executionfailures. Main
execsession47505/PID90656 still active; monitoring cell392 ended normally. Read
notes/confirmation-three-seed-resources.json for resource growth. Do not re-run
the primary or change frozen source/config. Continue remaining2seeds, then the
short T16 search/prior studies and strong100 (timeout5400 but01:30UTC absolutecap).

Latest milestone:400/500,0executionfailures; main execsession47505/PID90656
active, monitoring cell394 ended normally. Lastseed93005 starting. Four-seed
resource file recorded. Report currentlyinterim; CLAIMSC019–27 verifieddev/algebra.

Additional interpretation checks identified BEFORE the new T16 diagnostic outcomes:
- For exhaustive supports, compare the same recorded model-selection objective
  (observed_errors[3]+1e-8*nonzero_terms) against the archived selected candidate,
  across ALL1200rows. Better hidden error alone cannot establish better optimization:
  restricting supports to<=3 also changes the model class/regularization. Save raw
  paired objective differences in an audit artifact if making a search-failure claim.
  This is read-only interpretation of the original declared objective, not a change
  to frozen fits/acquisitions. Enumeration is of ordinary-LS support fits with
  coefficient filtering, not global constrained optimization over all coefficients.
- Cross-engine aggregate AUCs use different seeds AND grids (oldfinite noises0/.01;
  newprimary noise.01only), plus grammar/search/retention/weighting changes. Do not
  portray those aggregate differences as a matched causal engine comparison.
- Strong30vs100 comparisons DO use the matched condition set and input hashes.

PRIMARY COMPLETE at00:12:34UTC:500/500,0executionfailures,10674.665679s.
All expected IDs and500 file hashes checked; full scientificaudit stillPENDING.
MainPID90656/session47505/monitor396 ended. Resource totals in notes/primary-
confirmation-resources.json. NEXT checkpoint owned results/state, short T16
search/prior runs, then strong100 by01:30. Audits/reporting must finish02:30.
