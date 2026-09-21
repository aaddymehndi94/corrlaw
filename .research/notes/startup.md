# Startup — 2026-09-21
Lead: Codex, single writer. Clean clone at 6b95eca; branch research/corrlaw-sprint-01.
T01 acceptance: doctor succeeds, all 32 starter tests pass, clock initialized once.
T02 acceptance: sanity-001 completed; install local science environment and record versions.
T03 acceptance: verify primary source methods and derive single-mode D-optimal overlap.
T04 acceptance: scientific tests cover sampling, units, labels, accounting, interfaces,
identities, witnesses and deterministic replay. Expected implementation/testing <60 min.
T05 acceptance: A/B paired five-policy smoke with equations and query ledgers (<10 min).
T06 acceptance: repeated A/B with full width/noise grid and three controls (<45 min).
T07 acceptance: bounded real PySR installation/import/fit attempt, <=25 min; fallback if unavailable.
Completion guard: active Codex goal plus disk task plan; check T01–T11 evidence before marking
complete. Existing lab runner enforces job timeouts/deadline; no recursive agent process.
No promise of restart after app/machine termination. Resume via RESUME_PROMPT.md.

T04/T05 evidence: 47 total tests pass (notes/development-tests.txt). finite-smoke-001
completed 10 policy units in 2.65 s; audit reconstructed labels/metrics, checked
500 witnesses and pairing. AUC on A tied across policies at ~0.02556. On B all four
active policies tied at ~0.06849 versus random ~0.61032 (one seed, noiseless smoke;
not confirmation). Largest small artifact ~305 KB. Full pilot is 360 policy units.

Checkpoint hiccups (not scientific failures): the first scoped checkpoint correctly
rejected an ignored Finder .DS_Store file inadvertently included by the leaf-path
collector. A retry excluded it, but was refused because development-001 already
held the runner lock. No index changes occurred. Resolution: leave that lock alone,
wait for the active run to finish, then checkpoint only explicit eligible leaf files.
