# Experiment records

`tools/lab.py run` creates `results/runs/<run_id>/run.json` and
`source_hashes.json` BEFORE executing the supplied command. It also creates an
immutable event file in `.research/events/`. Its raw console log is local at
`work/runs/<run_id>/console.log`; the finished manifest records that log's hash.

The experiment implementation must write small essential scientific outputs into
`CORRLAW_RESULT_DIR`: normalized metrics, all baseline failures, selected equations,
query IDs/labels, exact config, seeds and artifact provenance. These should be
committed after inspection. `run.json` says whether a process finished, NOT whether
its scientific claims are valid. Do not write invented default metrics for failures.

Large matrices/search dumps/checkpoints go in `CORRLAW_WORK_DIR` and are ignored by
Git. Preserve them locally; include hashes, size, deterministic reconstruction
instructions and small decisive exports in the tracked run folder. Where exact
stochastic reconstruction is not guaranteed, retain decisive equation/model outputs
rather than claiming a seed alone reproduces everything. Local ignored data are NOT
backed up by Git commits or pushes.

Use a new ID for retries/reproductions and link to the parent attempt. Never overwrite
an existing run, erase failed runs, or report only successful seeds. Unexpected
termination may leave status `running`; use the documented recovery procedure.

Proposed per-experiment outputs to implement:
- `config.json`: full resolved inputs; known reference formulas remain evaluator-only.
- `metrics.json`: per-task/seed/policy/budget metrics and failures.
- `equations.json`: candidate expressions, complexity, fits, witness metadata.
- `queries.csv`: acquired points/IDs, noise realization IDs, label budget ledger.
- `validation.json`: checked invariants and remaining issues.

No benchmark runner/model or scientific result is implemented by this README.
