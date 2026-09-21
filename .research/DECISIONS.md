# Decision ledger

## D001 — Starter design (not an experimental finding)
Use a short root instruction file, durable repository notes, immutable run IDs,
scoped local Git commits, and a single lead writer. No external orchestration service.
Reason: spend the sprint on experiments rather than another agent platform.
Evidence: design choice; not a measured effectiveness claim.

## D002 — Scientific success is not required to be positive
Known-method equivalence, negative results and incomplete evidence must remain visible.
Do not optimize thresholds or baselines to obtain a favorable result.
Evidence: research policy, not a finding.

For new entries use D003, D004, ... with UTC time, decision, concise rationale,
alternatives considered, supporting run/source paths, and what would reverse it.
Do not overwrite earlier decisions; add a superseding entry.

## D003 — 2026-09-21: implement a finite-library acquisition pilot
Use a shared greedy sparse point predictor with bootstrap/search-size committees;
change acquisition only. Library subsampling is the diversified baseline. Explicit
alternatives obey the same seven-term/normalized-coefficient bound. This isolates
the acquisition effect without giving the proposed policy a better predictor.
Evidence: docs/METHOD.md, scientific tests and forthcoming finite-smoke-001.
Reconsider only on development evidence, before freezing confirmation.

## D004 — 2026-09-21: optional PySR is usable, not the main engine
Real PySR 2.5.0 / Julia 1.13.0 setup and fit succeeded within 600 s in
pysr-smoke-001 (471.57 s including first installation/compilation). Preserve its
actual equations. Predeclare a small A/B exact/noiseless initial-data comparison on
seeds 101–103, arithmetic +,-,*,/, maxsize 10, two populations of 20, ten iterations,
60 s search cap each; select by calibration MSE + 1e-8 complexity. Archive all
candidate equations. This checks engine behavior; it is not a PySR acquisition
benchmark and cannot establish a general evolutionary-search advantage.
