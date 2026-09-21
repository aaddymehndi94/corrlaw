# Intended research architecture

Implemented by the starter: `tools/lab.py`, helper tests, and the analytical circle
sanity check. Everything below is an implementation plan for Codex, not working
scientific code at initialization.

Suggested modules under `src/corrlaw/`:
- `contracts.py`: typed observation/candidate/query/result interfaces.
- `oracle.py`: private reference functions, physical preparation generators, splits,
  controlled noise and audited new-label access. No learner imports from here.
- `features.py`: one declared generic feature dictionary and input-only scaling.
- `discovery.py`: sparse finite-library baseline and optional real PySR adapter.
- `witnesses.py`: sparse near-null candidates, admissibility tests and provenance.
- `acquisition.py`: random/QBC/diversified/D-optimal/augmented policies. No oracle access.
- `evaluation.py`: reference errors, symbolic comparisons and diagnostic scoring.
- `experiment.py`: paired trials, saved artifacts, seeds and batch resume.
- `__main__.py`: a small documented CLI, not a web app.

Learner/acquisition inputs: anonymous numeric variables, measured data, permitted
priors/operators, bounds/scales and unlabeled query candidates. They must not receive
reference equations, preparation equations, true derivative information or hidden
labels. The evaluator knows the ground truth but cannot inform query selection.

Use tests to check forbidden imports and information flow. Those tests are useful
engineering controls, not proof that a coding agent with filesystem access is blind.
Keep batch checkpointing granular and stable. Store completed unit manifests before
scheduling the next one. Give intentional retries a parent ID and preserve failures.
Build one end-to-end path before adding modules merely for architectural symmetry.
