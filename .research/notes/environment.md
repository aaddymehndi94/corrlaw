# Environment
Host observed by `tools/lab.py doctor`: Darwin arm64, 8 logical CPUs.
Python: 3.14.5 (/opt/homebrew/bin/python3), local .venv.
Resolved Python package versions: requirements.lock.txt (pip freeze, editable package excluded).
`pip check`: no broken requirements found, 2026-09-21.
CPU request: up to four BLAS threads; optional Julia smoke explicitly one search,
GC and precompile thread. One helper-managed heavy experiment at a time.
Julia bootstrap initially selected 1.13.0 under .venv/julia_project; its package depot
is local .julia. Existence of a downloaded binary is not a successful PySR experiment.
No global/system package, credentials, paid API, cloud or remote repository changes.

Confirmed optional runtime: PySR 2.5.0, Julia 1.13.0; real smoke plus six fits succeeded.
Exact Julia environment: configs/JuliaProject.toml and configs/JuliaManifest.toml.
Main confirmation: 1,000 units in 343.107057 seconds (lab runner wall time), CPU only.
No more experiments are needed for the registered scope; final audit/replay/report
remain required before completion.
