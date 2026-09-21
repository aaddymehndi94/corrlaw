# Handoff — active overnight research
Repository: /Users/devikasv/dev/corrlaw; branch research/corrlaw-sprint-01.
User requested unattended work until 2026-09-22 08:00 IST (02:30 UTC), with final
hour for audit/reporting. Experiments end 01:30 UTC. SPRINT.json unchanged; lab.py
now enforces the earlier OVERNIGHT.json deadline by min, never extending the clock.
Native goal remains ACTIVE. Same-thread watchdog has an explicit deadline and STOP
file under work/overnight-watchdog. It now nudges only after15m without real file/run
progress, once per unchanged progress timestamp, and retries queue failures.
Read current PID in work/overnight-watchdog/pid; bounded caffeinate keeps host awake.
Queue acceptance was tested and timed deliveries succeeded; availability is not
unconditional. User stop/scope changes always supersede queued reminders.

IMPORTANT: before ANY new PySR confirmation, a fairness issue was found. Search
maxsize10 versus accepted SymPy complexity31 could favor added alternatives.
Development001 was deliberately interrupted (all completed units preserved).
notes/complexity-fairness-revision.md explains the change. Do not call that partial
run final evidence. Revised search and every accepted expression share a15-node
arithmetic-tree budget (+,-,*,/), including expanded integer powers. Loader rejects
unequal caps. T13 reopened for revised smoke/audit/replay, then T14 development.

Next: pysr-fair-smoke-001, configs/pysr-fair-smoke.json, A/B seed204, five policies,
30iterations per search. After validation, run pysr-development-002 using
configs/pysr-development-v2.json (360 units; all widths/noise/controls; three seeds).
Execution now goes seed-first to cover tasks fairly if an unexpected cutoff happens.
Review complete A/B results and actual runtime before finalizing frozen C/D/E/F
scope. Candidate primary/100-iteration sensitivity scope is in
work/pysr-confirmation-scope-plan.md; reduce counts BEFORE freeze if necessary.
No new C/D/E/F PySR outcomes have been inspected. All old v2 finite results remain
historical pilot evidence. Confirmation needs a new v3 freeze and fresh93001+ seeds.

New installed files: diagnostics.py (generic exhaustive<=3-support search and B
origin/parity library controls); search_diagnostic.py; prior_experiment.py and audit;
positivity.py; explain.py; CLI dispatch; summary figure labels. Their declared
exploratory designs are in notes/diagnostic-plan.md. Five draft tests passed before
installation; the installed full suite passed67 tests (notes/overnight-tests-02.txt). No full diagnostic experiment
yet. Explanations on old C and PySR A artifacts rendered and visually inspected under
work/witness-preview and work/witness-pysr-preview. These are previews, not outcomes.

Further interpretation limits: notes/overnight-interpretation-checklist.md and
notes/dimensional-prior-note.md. Direct SymPy unit balances for A/C/D show strong
full-dimensional priors fix monomial powers under no-additional-parameter assumptions;
reports/audit/dimensional-prior-algebra.json stores them. APS Buckingham1914 metadata
verified; no novelty claim. Positivity and numerical fit tolerance are not global
physical validity or structural uniqueness proofs.

Old smoke003 passed 3163 candidate/500 witness audit and exact replay under its own
former complexity rule. Its earlier failed tie-order audit002 remains recorded.
Current tests include a new explicit arithmetic-budget regression and equal-cap guard.
Pytest discovery restricted to tests/ to avoid duplicate ignored work/ draft modules.

Do not edit source/config while an experiment runs. One heavy process, <=4 numerical
threads. Local scoped commits only; preserve failures. No push, paid APIs, cloud,
system configuration changes, or additional Codex sessions. Drafts in work/ remain
for provenance; installed files are now the authoritative implementations.

Milestone19:16UTC: fair smoke completed10/10, strengthened artifact audit valid
(4379 candidates/460 witnesses), and fresh B fair-replay001 exactly matched.
T13 nowDONE; next is full development002, config pysr-development-v2.json.
No new confirmation yet. Fair smoke validation note has exact hash.
