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

## D005 — 2026-09-21: freeze broad confirmation without method tuning
Development-001 completed 360 units in 86.23 s, validated 21,651 witnesses.
Augmented constrained AUC A/B: 0.07609/0.06413; ordinary QBC: 0.07608/0.05523;
D-optimal: 0.07625/0.06405. Evidence: reports/development/summary.json.
No consistent unique advantage; retain thresholds and all baselines. Resources
support C/D/E/F, five seeds, widths 0/.01, both noise levels and three controls:
1,000 confirmation units. Preselect one noisy C augmented unit for exact replay.
Do not change these decisions after opening confirmation outcomes.

## D006 — 2026-09-21: artifact and reporting fixes before freeze
Development artifacts are immutable. Save future unit JSON compactly, preserving
all numeric fields/candidates/witnesses; ~161 MB of pretty development evidence
remains tracked and compresses in Git. Move chart legend below panels after visual
inspection detected title overlap. Neither change alters computed scientific values.

## D007 — 2026-09-21: preserve and correct a replay-check false negative
confirmation-v1-001 completed 1,000 units; full artifact audit validated 96,345
alternative records. reproduce-v1-001 returned exact_match=false even though both
scientific hashes were identical (36e69b2b...e18e564). Cause: lib.powers is a list of
tuples in memory but a list of lists after JSON loading. Python container equality
was the wrong test of the serialized scientific contract. No numeric discrepancy
was observed. Preserve the failed attempt rather than editing its boolean.
Fix the checker to compare canonical serialized JSON exactly, with no rounding or
numeric tolerance. Add regression tests that accept saved-container equivalence
and reject a 1e-6 metric change. Because source is revised after the first round,
create protocol v2 with fresh seeds 92001–92005 and retain the first round as
exploratory. No learning method, threshold, metric, acquisition or scope changes.
Preselect the corresponding noisy C unit at seed 92001 for v2 replay.
