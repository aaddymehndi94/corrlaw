# Execution plan

Change task status only with an evidence path/run ID. Keep old failures in dated notes.
States: NOT_STARTED, ACTIVE, BLOCKED, DONE, SKIPPED_WITH_REASON.
One ACTIVE implementation task by default. All rows below start NOT_STARTED.

| ID | Depends on | Task | Acceptance evidence | Status |
|---|---|---|---|---|
| T01 | none | Inspect repository, initialize bounded sprint, check environment/Git ownership | 32 starter tests; notes/startup.md; sanity-001 | DONE |
| T02 | T01 | Run analytical sanity and minimal science-environment smoke | sanity-001; notes/environment.md; requirements.lock.txt; pysr-smoke-001 | DONE |
| T03 | T02 | Targeted prior-work and equivalence audit | docs/RELATED_WORK.md; docs/EQUIVALENCE.md | DONE |
| T04 | T03 | Implement oracle/data generation, learning contracts and evaluator | tests/test_science.py; notes/development-tests.txt | DONE |
| T05 | T04 | Complete one small end-to-end finite-library comparison | finite-smoke-001/validation.json: 10 units, 500 witnesses checked | DONE |
| T06 | T05 | Development sweep and failure analysis | development-001/validation.json; reports/development; 360 complete units | DONE |
| T07 | T05 | Bounded PySR smoke and small comparison | pysr-smoke-001/pysr.json; pysr-compare-001/comparison.json (six fits) | DONE |
| T08 | T06,T07 | Freeze a feasible confirmation protocol | v1 freeze blocked by generated egg-info inventory; regression fix under test | ACTIVE |
| T09 | T08 | Run held-out confirmation without changing methods | confirmation-v1-001 planned after valid freeze; no confirmation started | NOT_STARTED |
| T10 | T09 | Independent-process reproduction and skeptical audit | reproduced artifact/metrics; leakage/fairness/freeze audit; unresolved issues listed | NOT_STARTED |
| T11 | T10 | Write evidence-linked report and handoff; final local checkpoint | report, figures, claims ledger, exact reproduction commands and Git status | NOT_STARTED |

T07 may use the documented fallback and still satisfy its dependency. A missing PySR
run must not be described as an evolutionary-symbolic-regression result.
T09 completion at the minimum scope is a pilot, not a broad benchmark conclusion.
At reporting cutoff, move to T10/T11 with existing evidence even when earlier tasks
remain blocked/incomplete. Label that scope honestly; do not mark skipped science DONE.
