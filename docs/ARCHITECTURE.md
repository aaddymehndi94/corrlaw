# Implemented architecture

`contracts.py` defines the anonymous numerical observations. `oracle.py` holds
physical reference functions, declared domains/preparations, RNG split generation,
and an audited query-ID label interface. No learner imports it.

`features.py` creates the generic domain-safe polynomial/Laurent dictionary.
`discovery.py` fits sparse bootstrap committees and the common point predictor.
`witnesses.py` finds bounded empirical alternative equations.
`acquisition.py` selects IDs from unlabeled numerical candidate pools.

`evaluation.py` alone computes hidden function errors and rounded symbolic recovery.
`experiment.py` coordinates paired trials, stores immutable unit artifacts and an
incremental manifest, and verifies source/config/artifact identity on resume.
`audit.py` reconstructs data to validate saved measurements/metrics, checks both
witness expressions, and reproduces a named result in a fresh process.
`summarize.py` generates descriptive paired tables and figures from saved outputs.
`__main__.py` exposes the strict-config experiment CLI.

The main learner contract includes only measured inputs/outputs, unlabeled pool and
public probes, declared bounds/noise/output scale. It contains no task names,
preparation equation, reference formula, oracle derivatives or hidden test labels.
This is tested interface separation, not secrecy from a coding agent that knows
the repository. SymPy/reference checks never feed back into fitting or acquisition.

The stdlib `tools/lab.py` provides bounded job recording, freezes and local scoped
commits. `tools/completion_check.py` is a fail-closed evidence gate, not an agent
orchestrator. The active task goal carries the continuation request; durable state
supports restart without discarding completed work or resetting the clock.
