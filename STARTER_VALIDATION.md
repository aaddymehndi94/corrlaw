# Starter-kit validation

Prepared: 2026-09-21. This validates the starter tooling, NOT the research hypothesis.

## Tests actually run

`python3 -m unittest discover -s tests -v` passed all **32 tests** in the preparation
environment: Linux, Python 3.13.5. Raw output is in
`docs/STARTER_TEST_OUTPUT.txt`. The helper also parses as Python 3.8 syntax; a
Python 3.8 runtime was not separately tested.

Tests cover atomic JSON, immutable deadlines/run IDs, failed/missing commands,
timeouts, path/symlink rejection, source-change invalidation, report reserves,
freeze verification and draft rejection, explicit-file Git commits, staged-change
protection, basic sensitive-file/content guards, large-file rejection, exclusive
runner locks, orphan recovery and the supplied analytical circle identity.

## End-to-end integration actually run

In a disposable local Git repository, the package was imported and checkpointed,
a sprint initialized, the circle example executed through the run recorder, saved
provenance inspected, local raw files checked against Git ignore rules, and the
small result/event files committed. The resulting worktree was clean. There was
no configured remote and no push. Temporary fixture identity was local to the test.

The circle maximum observed on-ring disagreement was 2.220446049250313e-16;
the off-ring values were exactly 1/2 and 5/4 using rational arithmetic. These are
checks of a supplied identity, not newly discovered physical results.

## Not tested or performed

No PySR installation, model search, five-policy research comparison, scientific
confirmation, real-user Git repository access, GitHub push or publication occurred.
No claim of novelty or superior experiment selection has been established.
The tests do not establish adversarial isolation, complete secret detection, hard
CPU/memory limits, automatic agent restart or guaranteed uninterrupted operation.

## Clean delivery

The archive has no `.git`, active sprint record, live locks, local environment,
raw experiment outputs or pre-filled research results. Its clock starts only
when the owner/agent invokes `tools/lab.py start` in their repository.
`CHECKSUMS.sha256` checks the original package bytes, not a future scientific protocol.
