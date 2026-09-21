# CorrLaw — repo-ready research starter

**Goal:** test whether automatically constructed alternative equations reveal false
consensus in symbolic law discovery and improve selection of new simulated measurements.
Laptop CPU experiments only. No laboratory work or additional paid APIs required.
A useful negative result is acceptable; novelty/publication are not guaranteed.

## Start
Copy this folder's CONTENTS, including `.research/`, `.gitignore` and `.gitattributes`,
into the root of your existing cloned repository. Do not copy or replace `.git`.
Merge existing README/AGENTS/.gitignore/project files rather than blindly overwriting
them, and retain any existing LICENSE. There is no Git repository inside this kit.

Open Codex in that repository root and paste:

> Read AGENTS.md and CODEX_PROMPT.md, then execute the CorrLaw research sprint.
> This existing repository is the persistent record. Run the work, keep state and
> evidence on disk, and make scoped local Git progress commits. Do not stop at a
> plan. Resume existing work rather than restarting it. Do not push or publish.

Use this kit instead of the earlier standalone `CODEX_RESEARCH_PROMPT.md`.
The complete agent prompt is `CODEX_PROMPT.md`. For a later/new session use
`RESUME_PROMPT.md`. No need to paste the full research specification into every chat.

## What is actually included
- Short persistent instructions plus the complete scientific research specification.
- Prewritten task plan, state, handoff, decision/claims ledgers and reading list.
- Draft development/confirmation configurations; the agent must finalize them.
- A stdlib-only POSIX helper for deadline-aware runs, immutable run IDs, source
  provenance, protocol freeze checks, careful local commits and orphan recovery.
- Helper unit tests and a supplied analytical circle sanity check.

**Not included:** a completed symbolic-regression experiment, a solved research
problem, generated scientific results, or a background multi-agent service.
`src/corrlaw/` is intentionally only a package scaffold. Codex implements the science.
The helper and sanity check work before NumPy/PySR or any other science packages are
installed. See `STARTER_VALIDATION.md` for what was tested during preparation.

## File map
| File | Purpose |
|---|---|
| `CODEX_PROMPT.md` | Complete lead-agent kickoff instructions |
| `AGENTS.md` | Small instruction index and invariants |
| `RESUME_PROMPT.md` | New-session recovery without old chat context |
| `docs/RESEARCH_SPEC.md` | Detailed hypothesis, benchmark, baselines and science rules |
| `docs/WORKFLOW.md` | Run, checkpoint, freeze and recovery procedures |
| `docs/PROTOCOL.md` | Draft evaluation contract; must be finalized before confirmation |
| `.research/STATE.md` / `HANDOFF.md` | Current situation and one exact next action |
| `.research/PLAN.md` | Tasks, dependencies and completion evidence |
| `.research/DECISIONS.md` / `CLAIMS.md` | Durable decisions and evidence-backed claims |
| `tools/lab.py` | Local recorder, runner, checkpoint and freeze helper |
| `results/runs/` | Created on execution; tracked small essential artifacts |
| `work/` | Created on execution; ignored raw logs and larger checkpoints |
| `reports/REPORT.md` | Honest evidence-linked final report |

## Local checks
```sh
python3 tools/lab.py doctor
python3 -m unittest discover -s tests -v
```

Do not run `start` just to inspect the archive; it starts the ten-hour budget.
The agent does that when execution begins. The clock persists across sessions, and
pauses count. The final hour is reserved for audit/reporting. The helper is not an
API-credit meter and cannot force Codex itself to stay active or restart.

## Git defaults
Local commits: enabled. Automatic pushes: disabled. No remote/identity is invented.
The lead preserves user changes, owns only selected files, and inspects its diffs.
The checkpoint helper does not push and is not a complete secret scanner.

A local commit is not a remote backup. To explicitly authorize remote backups, the
owner can add this instruction to the session:

> After reviewed checkpoints, push normal updates only to the already configured
> origin and this designated research branch. Never force-push, change repository
> visibility, publish releases or papers, or alter credentials/remotes.

Then have the lead record that authorization and update the recorded push policy.
No automatic push occurs merely because this archive is copied into a GitHub clone.
Ignored raw outputs remain local even when code/summary commits are pushed.

## License and attribution
No LICENSE is imposed by this starter kit, so it does not overwrite your repository's
choice or assume ownership/authorship details. A public repo is not by itself an
open-source license. Before public release, select a license for your original code,
check dependency/source terms and retain required attribution. License selection
need not block local experiments. Record actual human/AI contributions honestly.
