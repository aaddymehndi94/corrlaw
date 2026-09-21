# Execution plan

Change task status only with an evidence path/run ID. Keep old failures in dated notes.
States: NOT_STARTED, ACTIVE, BLOCKED, DONE, SKIPPED_WITH_REASON.
One ACTIVE implementation task by default. All rows below start NOT_STARTED.

| ID | Depends on | Task | Acceptance evidence | Status |
|---|---|---|---|---|
| T01 | none | Inspect repository, initialize bounded sprint, check environment/Git ownership | 32 starter tests; notes/startup.md; sanity-001 | DONE |
| T02 | T01 | Run analytical sanity and minimal science-environment smoke | sanity-001; local venv installation in progress | ACTIVE |
| T03 | T02 | Targeted prior-work and equivalence audit | exact sources/status; algebra comparing single-null-mode acquisition with regularized design | NOT_STARTED |
| T04 | T03 | Implement oracle/data generation, learning contracts and evaluator | tests for units, distributions, split/query accounting and no formula leakage | NOT_STARTED |
| T05 | T04 | Complete one small end-to-end finite-library comparison | all five policies run on A/B; actual equation, query and metric artifacts | NOT_STARTED |
| T06 | T05 | Development sweep and failure analysis | repeated paired seeds; independent/shuffled/restricted-query controls; runtime profile | NOT_STARTED |
| T07 | T05 | Bounded PySR smoke and small comparison | real PySR run/equation archives OR documented finite-library-only fallback | NOT_STARTED |
| T08 | T06,T07 | Freeze a feasible confirmation protocol | complete protocol; committed code/config/lockfile; freeze manifest and verification | NOT_STARTED |
| T09 | T08 | Run held-out confirmation without changing methods | all policies; at least two confirmation tasks; intended repeated seeds; failures included | NOT_STARTED |
| T10 | T09 | Independent-process reproduction and skeptical audit | reproduced artifact/metrics; leakage/fairness/freeze audit; unresolved issues listed | NOT_STARTED |
| T11 | T10 | Write evidence-linked report and handoff; final local checkpoint | report, figures, claims ledger, exact reproduction commands and Git status | NOT_STARTED |

T07 may use the documented fallback and still satisfy its dependency. A missing PySR
run must not be described as an evolutionary-symbolic-regression result.
T09 completion at the minimum scope is a pilot, not a broad benchmark conclusion.
At reporting cutoff, move to T10/T11 with existing evidence even when earlier tasks
remain blocked/incomplete. Label that scope honestly; do not mark skipped science DONE.
