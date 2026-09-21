# CorrLaw

A reproducible local research pilot for ambiguity in equation discovery. It asks
whether explicit alternative equations help select new measurements beyond random
sampling, ordinary query-by-committee (QBC), library-diversified QBC and regularized
D-optimal design. All measurements are simulated from declared ideal physical models.
The supplied circle identity is a sanity check, not a discovery.

Start with [the research report](reports/REPORT.md), [current state](.research/STATE.md),
and [claims ledger](.research/CLAIMS.md). The main experiment uses finite-library
sparse regression. A real optional PySR smoke and small development comparison are
recorded separately; they are not a full evolutionary-search acquisition benchmark.

## Local setup

Python 3.14.5 was used on Apple Silicon macOS. Exact resolved Python versions are
in `requirements.lock.txt`; Julia dependencies used by optional PySR live in the
local environment. No Julia is needed for the main experiment.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m pip install -e .
.venv/bin/python -m pytest -q
```

The lockfile includes optional PySR. For just the finite-library implementation,
`requirements.in` installs the scientific dependencies without initiating Julia.
PySR's Julia setup runs only when importing PySR, and the supplied examples direct
its depot and project into this repository's ignored local directories.

## Run and inspect

```sh
# Standalone repeat into a NEW output directory (never overwrite evidence):
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 \
  .venv/bin/python -m corrlaw run --config configs/smoke.json --output work/my-smoke
.venv/bin/python -m corrlaw.audit work/my-smoke --output work/my-smoke
.venv/bin/python -m corrlaw.summarize work/my-smoke --output work/my-smoke-report
```

For research-sprint execution use `tools/lab.py run` so deadlines, provenance,
failures and timeouts are recorded. Read [WORKFLOW](docs/WORKFLOW.md) first.
`python3 tools/lab.py start` initializes one ten-hour elapsed budget; repeated calls
never reset it. Do not run new experiments past its cutoff without a new user
authorization. Confirmation requires a reviewed committed protocol and matching
freeze. `--resume` accepts only identical configuration/source and hash-verified
saved units; use a new run ID for intentional repeats or changed code.

## What is saved

Each `results/runs/<run-id>/units/*.json` contains one task/seed/condition/policy:
all candidate coefficients and equations, every accepted ambiguity witness,
selected query IDs/coordinates/labels, five budget metrics, timing and data hashes.
The manifest records expected/completed units and hashes. `validation.json` checks
pairing, accounting, reconstructed labels/metrics and both witness expressions.
Generated reports include condition-level CSVs, paired seed-level summaries and
SVG/PNG figures. Raw logs, Julia artifacts and caches remain ignored under `work/`,
`.venv/` and `.julia/`; local Git commits do not back those up remotely.

[Physical assumptions](docs/BENCHMARKS.md), [method](docs/METHOD.md),
[protocol](docs/PROTOCOL.md), [related work](docs/RELATED_WORK.md), and
[known-method overlap](docs/EQUIVALENCE.md) define the scientific scope.
No lack of a witness is interpreted as proof of uniqueness. Negative results count.

## Continuation and completion

The active task goal and `.research/PLAN.md` guide continued work. Run
`python3 tools/completion_check.py` for the disk-evidence completion gate. It exits
nonzero when required tasks, confirmation validation, reproduction or freeze checks
are missing. It cannot restart Codex after an app/machine shutdown; use
[RESUME_PROMPT.md](RESUME_PROMPT.md) to recover from the durable state.
Local scoped progress commits are authorized by the repository instructions.
Pushes, publication and paid services are not enabled. No license was supplied;
this work does not silently impose one or assign human authorship.
