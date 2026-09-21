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
