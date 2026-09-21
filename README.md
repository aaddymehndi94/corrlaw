# CorrLaw

A reproducible local study of ambiguity in equation discovery. It asks whether
explicit alternative equations expose misleadingly small committee disagreement,
and whether they help select new measurements beyond random sampling, ordinary
query-by-committee (QBC), feature-diversified QBC and regularized D-optimal design.
All measurements are simulated from declared ideal physical models. The supplied
circle identity is a sanity check, not a discovery.

Start with [the research report](reports/REPORT.md), [current state](.research/STATE.md)
and [claims ledger](.research/CLAIMS.md). The repository contains a finite-library
pilot, a PySR acquisition extension, physical-prior and search-failure diagnostics,
and a viewer for saved ambiguity witnesses. Consult the report and run audits for
which experiments actually completed; installed code alone is not research evidence.
The PySR engine searches arithmetic compositions of generic normalized features,
not only raw variables. No broad novelty or publication-readiness claim is made.

## Local setup

Python 3.14.5 on Apple Silicon macOS was used. Exact resolved Python packages are in
`requirements.lock.txt`; PySR 2.5.0 used Julia 1.13.0 and the saved Julia dependency
records in `configs/`. The finite-library engine and artifact analysis need no Julia.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m pip install -e .
.venv/bin/python -m pytest -q
```

The lockfile includes optional PySR. For only the finite-library implementation,
`requirements.in` provides scientific dependencies without initiating Julia.
PySR is imported lazily by actual searches; its depot/project stay in ignored
repository-local `.julia` and `.venv/julia_project` directories. A first search may
need to download/precompile Julia dependencies; subsequent runs reuse the local setup.

## Run and inspect

Run from the repository root. Choose a NEW output directory for an intentional
repeat; do not overwrite recorded evidence.

```sh
# Small finite-library experiment:
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 \
  .venv/bin/python -m corrlaw run --config configs/smoke.json --output work/my-smoke
.venv/bin/python -m corrlaw.audit work/my-smoke --output work/my-smoke
.venv/bin/python -m corrlaw.summarize work/my-smoke --output work/my-smoke-report

# Revised PySR experiment with matched search/acceptance complexity:
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 \
  .venv/bin/python -m corrlaw run --config configs/pysr-fair-smoke.json \
  --output work/my-pysr-smoke
.venv/bin/python -m corrlaw.symbolic_audit work/my-pysr-smoke \
  --output work/my-pysr-smoke

# Explain the first recorded witness; no hidden-error-based example selection:
.venv/bin/python -m corrlaw explain results/runs/confirmation-v2-001 \
  --unit C-s92001-w0-n0-constrained-augmented_qbc --output work/my-witness
```

For sprint execution use `tools/lab.py run` so deadlines, provenance, failures and
timeouts are recorded. Read [WORKFLOW](docs/WORKFLOW.md). `lab.py start` initializes
one elapsed budget; repeated calls never reset it. The earlier user-authorized
overnight cutoff is recorded in `.research/OVERNIGHT.json`. No new experiments are
authorized past that cutoff without a new user instruction. The reusable science
module has no permanently embedded historical cutoff; the wrapper supplies each
run's deadline and enforces it. This permits later authorized reproduction.

Confirmation requires a reviewed committed protocol and matching freeze. `--resume`
for the finite/PySR engines accepts only identical configuration/source and
hash-verified units. Use a new run ID for changed code or intentional repeats.
Prior controls use separate new output directories; their CLI does not support resume.
Historical PySR configs with unequal10/31 complexity caps are retained for provenance
and deliberately rejected by the revised configuration loader. They are not current
examples; use the fair-cap configs and their recorded source commits as appropriate.

## Evidence and scope

Every unit JSON contains a task/seed/condition/policy trajectory: all candidates,
selected equations, accepted alternatives, queried IDs/coordinates/labels/noise IDs,
metrics, timings and data hashes. PySR additionally saves raw search equations,
bootstrap rows, feature subsets, seeds and weights. Manifests record expected units
and hashes. An execution success does not substitute for `validation.json`.
Reports include all condition tables, paired seed summaries and SVG/PNG figures.
Raw logs, Julia search files and caches are local ignored artifacts; local Git
commits do not back them up remotely.

[Physical assumptions](docs/BENCHMARKS.md), [finite method](docs/METHOD.md),
[PySR method](docs/METHOD_PYSR.md), [current protocol](docs/PROTOCOL.md),
[related work](docs/RELATED_WORK.md) and [known-method overlap](docs/EQUIVALENCE.md)
define the scope. Seeds, not hidden points or conditions, are statistical units.
Empirical admissibility is not a calibrated posterior, a global physical-validity
certificate, or exact structural nonidentifiability. Failure to find a witness is
not proof of uniqueness. Negative and inconclusive results remain valid outcomes.

## Continuation and verification

The active task goal and `.research/PLAN.md` guide continued work. The overnight
watchdog queues bounded reminders to the same authorized thread after inactivity;
[its operating note](.research/notes/watchdog-operation.md) describes the stop file,
deadline and availability limits. It cannot guarantee execution after app/service
or machine failure. [RESUME_PROMPT.md](RESUME_PROMPT.md) recovers durable state.

`python3 tools/overnight_completion_check.py` checks the extension's saved evidence,
including confirmation audits, replays, diagnostics, figure regeneration and freeze.
The old `tools/completion_check.py` concerns only the historical finite pilot and
must not be used to declare the extension complete. Historical frozen bytes remain
inspectable at their recorded Git commits even after the live source evolves.
The final report gives exact replay and report-generation commands.

Local scoped commits are authorized. Pushes, publication and paid services are not.
No license was supplied; this work does not silently impose one or assign human
authorship. Research self-review is not independent peer review.
