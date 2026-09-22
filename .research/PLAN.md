# Execution plan

Change task status only with an evidence path/run ID. Keep old failures in dated notes.
States: NOT_STARTED, ACTIVE, BLOCKED, DONE, SKIPPED_WITH_REASON.
T01–T11 are the completed pilot. T12–T17 are the user-authorized overnight extension.

| ID | Depends on | Task | Acceptance evidence | Status |
|---|---|---|---|---|
| T01 | none | Inspect repository, initialize bounded sprint, check environment/Git ownership | 32 starter tests; notes/startup.md; sanity-001 | DONE |
| T02 | T01 | Run analytical sanity and minimal science-environment smoke | sanity-001; notes/environment.md; requirements.lock.txt; pysr-smoke-001 | DONE |
| T03 | T02 | Targeted prior-work and equivalence audit | docs/RELATED_WORK.md; docs/EQUIVALENCE.md | DONE |
| T04 | T03 | Implement oracle/data generation, learning contracts and evaluator | tests/test_science.py; notes/development-tests.txt | DONE |
| T05 | T04 | Complete one small end-to-end finite-library comparison | finite-smoke-001/validation.json: 10 units, 500 witnesses checked | DONE |
| T06 | T05 | Development sweep and failure analysis | development-001/validation.json; reports/development; 360 complete units | DONE |
| T07 | T05 | Bounded PySR smoke and small comparison | pysr-smoke-001/pysr.json; pysr-compare-001/comparison.json (six fits) | DONE |
| T08 | T06,T07 | Freeze a feasible confirmation protocol | freezes/v2.json verified (34 inputs); c15cad8; v1 preserved | DONE |
| T09 | T08 | Run held-out confirmation without changing methods | confirmation-v2-001/run.json and manifest: 1,000 complete, zero execution failures | DONE |
| T10 | T09 | Independent-process reproduction and skeptical audit | confirmation-v2-001/validation.json; reproduce-v2-001 exact; reports/audit regeneration | DONE |
| T11 | T10 | Write evidence-linked report and handoff; final local checkpoint | report/figures/claims/handoff checkpoint 8070049; completion gate record | DONE |

T07 may use the documented fallback and still satisfy its dependency. A missing PySR
run must not be described as an evolutionary-symbolic-regression result.
T09 completion at the minimum scope is a pilot, not a broad benchmark conclusion.
At reporting cutoff, move to T10/T11 with existing evidence even when earlier tasks
remain blocked/incomplete. Label that scope honestly; do not mark skipped science DONE.

## Overnight extension (deadline 2026-09-22 08:00 IST)

| ID | Depends on | Task | Acceptance evidence | Status |
|---|---|---|---|---|
| T12 | T11 | Same-thread watchdog and explicit overnight deadline | OVERNIGHT.json; queue delivery test; idle-only daemon; live PID in work/overnight-watchdog/pid | DONE |
| T13 | T12 | Actual PySR five-policy active learner, tests and smoke | fair smoke001 valid: 4379 candidates/460 witnesses; fair replay001 exact | DONE |
| T14 | T13 | Development/profiling and fresh frozen protocol | development360 and strong10 valid; exact strong replay;74 tests; freeze v3 verified75inputs at5e27579 | DONE |
| T15 | T14 | Repeated PySR confirmation with all baselines and controls | primary500/strong100 complete/hash-checked,0failures; scientific audits pending | ACTIVE |
| T16 | T13 | Search-failure and physical-prior diagnostics | search1200rows/702fits and prior300 complete; algebra/encoding verified; audits pending | ACTIVE |
| T17 | T15,T16 | Artifact audit, reproduction, updated report and handoff | full audits starting; report draft prepared | ACTIVE |
