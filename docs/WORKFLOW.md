# Research workflow and recovery

## Why these files exist
`AGENTS.md` is the short index. `CODEX_PROMPT.md` is the lead's operating prompt.
`docs/RESEARCH_SPEC.md` is the scientific specification. `.research/STATE.md` is the
current summary, not the full history. `.research/PLAN.md` tracks acceptance evidence.
Detailed decisions, claims, notes, immutable run records and Git preserve the history.
Do not load every record into each context; follow pointers from the current state.

The helper is ordinary local Python, not an agent orchestrator. It cannot guarantee
Codex keeps running, resumes itself, stays within an API-credit budget, or obeys
instructions outside commands sent through it. It does not provide adversarial
isolation, calibrated scientific confidence, hard memory limits or remote backups.

## Startup
Run from the existing repository root. Copy/merge the kit, including hidden files,
without replacing `.git`, the owner's LICENSE, or existing work.

```sh
python3 tools/lab.py doctor
python3 tools/lab.py start
python3 -m unittest discover -s tests -v
python3 tools/lab.py run --id sanity-001 --task T02 --purpose "Supplied analytical sanity check" --timeout 60 -- python3 examples/circle_sanity.py
python3 tools/lab.py status
```

If `sanity-001` exists, inspect it. Use a new explicit ID for an intentional repeat.
This sanity check tests the recorder and known circle identity, not the research
method. The implementation work begins after it passes.

`start` stores `.research/SPRINT.json` once. A repeated call retains the original
start/deadline and initially selected reporting reserve. Pauses count against this
elapsed budget; this is intentionally not an active-CPU-hours budget. Editing
`configs/sprint.json` later does not retroactively grant more time. Do not delete or
rewrite the sprint record to get more budget. Additional sprints need owner approval.

Use `python3 --version` and available interpreters, not assumed system versions.
The helper targets Python 3.8+ on POSIX. Scientific packages may need a newer
compatible interpreter. Resolve that in a local venv without system upgrades.
Create `requirements.lock.txt` from the actual working package versions, filtering
local/private URL credentials and documenting the exact Python/Julia versions.

## The repeating work unit
1. Choose one ready task and write its acceptance check.
2. Read only relevant notes/config/source. Avoid rediscovering documented failures.
3. Implement a small change and run focused tests.
4. Run the bounded experiment through the helper and inspect its artifacts.
5. Review the conclusion skeptically; update a decision or claim only with evidence.
6. Update state/plan/handoff pointers and checkpoint exact paths in Git.
7. Continue, or use the remaining reporting reserve when experiments must stop.

Write concise decisions and experiment notes, not internal reasoning transcripts.
Before a long job, save its exact command, task, run ID and expected outputs so an
interrupted context can locate it. Do not modify source/config while it is running.

## Experiment execution
The experiment CLI is for Codex to implement. Until then, only the circle example
and tests are runnable scientific-adjacent commands. A future example is:

```sh
# Run only AFTER src/corrlaw/__main__.py and its arguments exist and pass tests:
python3 tools/lab.py run --id dev-A-s101-qbc-001 --task T06 --purpose "Paired development comparison" --timeout 600 -- .venv/bin/python -m corrlaw run --config configs/pilot.json
```

The generic helper:
- creates a new run ID directory and records command, purpose, Git commit, source
  hashes, deadline, requested thread count, timing, exit status and log hash;
- refuses reused IDs and simultaneous helper-managed heavy runs;
- bounds subprocess duration by requested timeout AND remaining phase budget;
- records unsuccessful exits, missing executables, timeouts and interruptions;
- marks code/config edits during a run as invalidating provenance;
- provides `CORRLAW_RESULT_DIR` and `CORRLAW_WORK_DIR` to the child command.

It does NOT validate a model or metric simply because the process exits zero.
It requests up to four library threads through environment variables; that is not
a hard OS-wide CPU cap. The agent must avoid nested parallelism and monitor memory.
Raw log/dataset/checkpoint bytes stay local under `work/`. The manifest's hashes
are not copies of those bytes. Preserve/reconstruct decisive outputs before cleanup.
Do not put credentials in command arguments, notes, config, or environment dumps.

## Git checkpoints
Only one lead owns the real worktree and Git index. Inspect:

```sh
git status --short --branch
git diff --stat
git diff --cached --stat
```

For a completed change, inspect the actual diff and run its tests. Then checkpoint
ONLY exact files you own. For example (adjust the list to what actually changed):

```sh
python3 tools/lab.py checkpoint --message "test: add oracle query accounting [T04]" --paths src/corrlaw/oracle.py tests/test_oracle.py .research/STATE.md .research/PLAN.md
```

The helper refuses existing staged changes, broad directories, common credential
filenames/content, ignored files and files over the configured 2 MiB limit. It does
not prove the absence of secrets or the correctness of the change. Human/agent diff
review is still required. Supply deletions only when intentionally deleting an owned
tracked file. Never erase raw scientific evidence merely to make a commit smaller.

Checkpoint after meaningful tested units, accepted experiment batches and before
risky changes. During longer editing stretches, preserve useful work approximately
every 20-30 minutes; do not create meaningless time-based commits. Use `wip:` and
record failing checks when a safe partial checkpoint is the honest state.

If a helper commit fails after staging (for example a hook failure), inspect the
index. Fix only your own staged files and finish that same commit with ordinary
Git if appropriate. Do not accidentally include someone else's staged work or
silently disable hooks. Missing Git identity/permissions should be recorded as a
checkpoint blocker, not "fixed" by inventing identity. Continue safe local science
where possible and say clearly that the checkpoint was not committed.

Do not reset, clean, auto-stash, amend history, force-push, change remotes or alter
Git's global configuration. No `git add .`/`git add -A`. Never initialize a nested repo.

Local commits are enabled; automatic push is disabled in `configs/sprint.json`.
The helper NEVER pushes, even if that policy flag is later changed. Only an explicit
owner instruction authorizes the lead to push. If authorized, use the already
configured remote and the designated research branch, normal fast-forward updates,
review staged/committed content, and stop on divergence/authentication surprises.
Never publish releases/papers or change repository visibility as part of a backup.
A local commit is not an off-laptop backup. Ignored raw files are not uploaded by Git.

## Freeze and confirmation
Complete `docs/PROTOCOL.md` and mark the draft fields resolved. Use only development
outcomes to choose thresholds, conditions and compute scope. Update confirmation
config to its finalized status and commit source, tests, configs, protocol and the
actual dependency lockfile. Only then change the protocol status to
`Status: READY_TO_FREEZE`, commit it, and create an immutable freeze:

```sh
# All named inputs must exist and already be committed:
python3 tools/lab.py freeze --id v1 --paths docs/PROTOCOL.md docs/RESEARCH_SPEC.md configs src tests tools examples pyproject.toml requirements.in requirements.lock.txt
python3 tools/lab.py verify --id v1
```

The helper checks that frozen inputs have a Git baseline and no uncommitted edits.
It records hashes including additions/removals inside the named directories. Commit
the newly generated freeze/event metadata too. The hash is not a secret evaluator.
The same coding agent can see the oracle; describe this as interface separation and
provenance control, not a blind agent study.

Actual confirmation commands require `--phase confirmation --freeze v1`:

```sh
# AFTER the experiment CLI is implemented:
python3 tools/lab.py run --id confirm-v1-001 --task T09 --purpose "Frozen paired confirmation" --phase confirmation --freeze v1 --timeout 900 -- .venv/bin/python -m corrlaw run --config configs/confirmation.json
```

After inspecting confirmation outcomes, do not edit the method and treat another
run on the same seeds as fresh confirmation. Document the change, version the
protocol, choose genuinely fresh confirmation data/seeds and retain the old result.
If a correctness bug invalidates a result, label/withdraw it rather than deleting it.

## Context compaction and restart
Before a context reset, write the current branch/commit, files changed and owner,
last validation, run IDs, active processes, protocol version, remaining budget,
blocker and ONE exact next action into state/handoff. Archive detail in named notes.

A restarted session begins with `RESUME_PROMPT.md`, not a reconstruction from chat.
Inspect `run.json` and logs for the named run before deciding to rerun anything.
Completed runs are reused as evidence; intentional reproductions get new IDs.
A graceful timeout/keyboard interruption is recorded automatically. A killed runner
or machine crash can leave status `running` and partial results.

```sh
python3 tools/lab.py status
python3 tools/lab.py reconcile
```

`reconcile` requires the runner lock to be free and refuses to act while a recorded
PID exists. PIDs may be reused; inspect rather than kill an unrelated process. It
marks clearly orphaned runs `interrupted_unverified` and preserves partial artifacts.
It does not implement numerical resume. The research batch runner should commit
atomic checkpoints per completed task/seed/policy and resume verified incomplete
units with recorded provenance, without silently replacing failed observations.

## Multiple agents without a new platform
Default: one lead executes and then reviews. No setup required.
Optional: use an already available native subagent for a read-only review with
specific input paths, scope, deadline, acceptance criteria and a named output note.
For actual parallel edits, the lead must first assign separate worktrees/branches
and nonoverlapping ownership. Only the lead integrates code and updates global
state/Git. Do not run two agents in one shared index. Do not exceed local compute
limits or let workers see confirmation metrics during method development.

Suggested review roles: numerical/algebra audit, data-leakage/fairness audit,
prior-work/novelty audit. Two model opinions do not replace an independent proof,
measurement or deterministic evaluator. No recursive self-spawned agent sessions.

## Completion and reporting
Use the final reserve to reproduce, audit, generate figures from saved data and
write the report. A bounded audit/reproduction command can use `--phase audit`;
do not relabel a new experimental sweep as audit to bypass the reporting cutoff.
Update claims and disclose incomplete scope. Leave a final local checkpoint plus
exact reproduction and resume instructions. Do not claim automatic continuation.
