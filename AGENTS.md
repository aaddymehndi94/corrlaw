# CorrLaw working agreement

This repository is the persistent research memory. The chat is not the record.
Use the existing repository root; never create a nested clone or replace user work.
Respect higher-priority instructions, local permissions, and existing user files.

## Read on entry or after context loss
1. `.research/STATE.md` and `.research/HANDOFF.md`: current status and exact next action.
2. `.research/PLAN.md`: task dependencies and completion evidence.
3. `CODEX_PROMPT.md`: mission and session operating loop.
4. `docs/WORKFLOW.md`: checkpoints, recovery and Git procedure.
5. `docs/RESEARCH_SPEC.md` and `docs/PROTOCOL.md`: scientific contract.
Read relevant source notes or run files on demand, not the entire archive.

## Non-negotiable science rules
- Run experiments; do not stop at a scaffold, literature summary, or proposed plan.
- No invented outputs, citations, timing measurements, model scores or novelty claims.
- A successful process exit is not a verified scientific finding.
- The circle identity is supplied as a sanity test, not a discovery.
- Fairly compare random, ordinary QBC, diversified QBC, D-optimal and augmented QBC.
- A nullspace or poor conditioning alone does not prove every sparse law unidentifiable.
- Separate numerical learning interfaces from oracle formulas and hidden labels.
- Freeze protocol/code before confirmation. Never tune on held-out outcomes or
  silently alter tests, metrics, splits, baselines or failed-run records.
- Preserve failures and alternatives. Tie every report claim to a source or run ID.
- Negative, equivalent-to-existing-method, and inconclusive outcomes are legitimate.

## Working loop
Recover -> choose one ready task -> write acceptance test -> implement -> run ->
inspect -> skeptical review -> record evidence -> update state -> local Git checkpoint.
Then continue to the next ready task without requesting routine approval.

Keep `.research/STATE.md` short (roughly 80 lines or less), with one exact next action.
Update it at milestones, after failed experiments, before lengthy jobs, and before
ending or compacting the session. Put detail in run records or dated notes.

## Local commands available now (no third-party packages needed)
```sh
python3 tools/lab.py doctor
python3 -m unittest discover -s tests -v
python3 tools/lab.py start
python3 tools/lab.py status
python3 tools/lab.py run --id sanity-001 --task T02 --purpose "Analytical sanity only" --timeout 60 -- python3 examples/circle_sanity.py
```
`start` is idempotent and does NOT restart an existing deadline.
Run IDs are immutable. Inspect existing artifacts instead of overwriting them.
See `docs/WORKFLOW.md` for all helper commands and recovery behavior.

## Resource and coordination rules
- Ten hours total from first `start`, including setup and interruptions; last hour
  reserved for audit/reporting. Never extend/reset the budget without user direction.
- CPU only; up to four computation threads and one heavy experiment at a time.
- Local venv only; no sudo, paid APIs, cloud compute or system configuration changes.
- One lead agent owns the main worktree, Git index, state and confirmation runs.
- Default to sequential roles. Native subagents, if already available, may perform
  bounded read-only reviews or work in explicitly assigned isolated worktrees.
- Do not launch more Codex sessions/APIs merely to create an orchestration framework.
- Worker reviews are not independent scientific validation; execution evidence matters.
- Do not edit source/config while an experiment uses it.

## Git and privacy rules
Local progress commits are authorized. Push/publication is NOT enabled by this kit.
Use exact paths and inspect diffs; no blanket `git add .` or `git add -A`.
Never reset/clean/stash/amend/force-push or discard user changes. Never alter global Git
identity, credentials or remotes. Existing staged changes belong to their owner.
Only the lead commits; checkpoint at completed logical steps and before risky changes.
Use `wip:` when intentionally preserving incomplete work; state failing tests honestly.
No credentials, chat transcripts, full environment dumps, private data or bulk binaries.
Do not suppress security/test hooks. Checkpoint helper scanners are only a basic screen.

## Completion
Leave code, exact configurations, result/equation/query records, tests, a provenance-
linked report, a claims ledger, an honest handoff, and cleanly described Git status.
Never promise automatic continuation, a discovery, or publication.
