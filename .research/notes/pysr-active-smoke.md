# PySR active smoke 001 — development

Run pysr-active-smoke-001, source d1b0794, 91.55 s, all 10 policy trajectories
completed. Three 10-iteration searches per refit, all five policies, A/B seed201.
One compiled process; first trajectory 36.33 s including Julia import/compilation;
subsequent trajectories 4.56–8.73 s. No reported exceptions.

Observed failure: independent restarts can lose a previously near-exact fitted
expression. A/QBC budget6 coefficient ~1 becomes 1.018 at budget7, despite earlier
valid equation. Preserve all prior discovered candidates, reevaluate against every
new dataset, and select the common full-data point model from retained/current
full-search candidates. Apply same rule to every policy. This is a development
method revision; no claim that first smoke is confirmation. Raise fixed search
iterations from10 to30 and profile before choosing confirmation scope.

The archived smoke equations/queries/metrics remain unchanged. Formal validation
is saved separately under reports/audit/pysr-active-smoke-001. Watch for biased
retention: old scores must NEVER be reused; acquired labels always refilter models.

## Smoke002 and failed audit

Smoke002 (39ce0a7) completed10/10 in129.86s; all final errors near numerical
precision. Audit pysr-smoke-audit-002 flagged one selected-expression mismatch at
A/random/budget3. Both expressions have exactly score3.0000000000000004e-08:
`z9*1.0963298297896746` and `z9*(0.09632982978967461 + z14/z14)`.
They simplify to equivalent predictions. Promotion of an existing bootstrap equation
to full-search eligibility changed persisted list order relative to the transient
full_candidates list. The checker required one particular tied expression.

Fix for subsequent development: select directly from persisted full-eligible
candidates and use `(score, expression_string)` as an explicit lexical tie rule.
Audit uses the same declared total ordering. Preserve the original failed audit;
no retrospective edits to its result or smoke002. A third bounded smoke and fresh
process replay will check the final rule before development and confirmation.

## Final smoke and reproduction

Smoke003 (e1ce316):10/10 complete in145.33s. Audit003 valid:3163 candidate records
and500 alternatives, all queries/metrics reconstructed. No numerical errors.
After a conservative numerical rejection screen before symbolic construction,
fresh process replay of A-s203-w0-n0-constrained-augmented_qbc matched ALL scientific
JSON exactly:51258273dd52241adbf4426162b0bb885a71fe1661a597d8ec3476bb3258431d.
Recorded augmentation time on that trajectory fell from1.426s to0.434s; descriptive
single-process timing, not a cross-machine speed guarantee. No final tolerance or
saved-error calculation changed. Source optimization commit7581285.

The watchdog's first timed reminder was accepted18:13:55UTC. See local delivery log.
Next:360-unit A/B development across3 seeds,3 widths,2 noise levels and all controls.
