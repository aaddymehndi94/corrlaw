# Current state
Status: ACTIVE
Task: T09 frozen v2 confirmation
Owner: Codex lead; branch research/corrlaw-sprint-01
Deadline 2026-09-22 03:01 UTC; experiment cutoff 02:01 UTC (ample time remains).
V1: 1,000 units completed; full artifact audit valid, 96,345 alternatives checked.
V1 replay was a false negative: exact scientific hashes match, tuple/list comparison
was incorrect after JSON serialization. Failed record is preserved unchanged.
Corrected checker compares canonical JSON exactly; regression test also rejects a
changed numeric metric. No numeric method/config changes except fresh v2 seeds.
Protocol v2 uses 92001–92005, all four tasks/all five policies/all controls.
V1 evidence retained as exploratory after revision. No active experiments.
49 tests passed; freeze v2 verified at c15cad8.
Next action: execute confirmation-v2-001 then audit and replay
C-s92001-w0-n0.01-constrained-augmented_qbc. See DECISIONS.md D007.
Do not claim completion until the actual saved-JSON replay and evidence gate pass.
