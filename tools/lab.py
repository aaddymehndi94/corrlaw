#!/usr/bin/env python3
"""Small, dependency-free research notebook/runner. Python 3.8+, POSIX.

This is a convenience harness, not a security boundary or an agent service.
It never invokes Codex, installs packages, stages directories, or pushes Git.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Any, Dict, Iterable, List, Optional

try:
    import fcntl
except ImportError:
    fcntl = None

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".git", ".venv", "venv", ".julia", "node_modules"}
SOURCE_ROOTS = ("src", "tools", "tests", "examples", "configs", "pyproject.toml",
                "requirements.in", "requirements.lock.txt", "docs/PROTOCOL.md", "docs/RESEARCH_SPEC.md")
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
               "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "JULIA_NUM_THREADS")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$")
SECRET_RE = re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|"
                       rb"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|"
                       rb"(?:sk-proj-|sk-)[A-Za-z0-9_-]{30,}|AKIA[0-9A-Z]{16}")


class LabError(RuntimeError):
    pass


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]


def valid_id(value: str) -> str:
    if not ID_RE.fullmatch(value):
        raise LabError("ID must be 1-96 letters/digits/._- and start with a letter or digit.")
    return value


def inside(root: Path, value: str) -> Path:
    path = root / value
    if Path(value).is_absolute() or ".." in Path(value).parts:
        raise LabError("Use a repository-relative path without '..': " + value)
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        raise LabError("Path escapes repository: " + value)
    # Refuse symlinked path components, including links back into the project.
    cursor = root
    for part in Path(value).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise LabError("Symlinks are not accepted here: " + value)
    return path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LabError("Cannot read JSON at %s: %s" % (path, exc))


@contextlib.contextmanager
def lock(root: Path, name: str):
    if fcntl is None:
        raise LabError("This runner needs POSIX advisory locks (Linux/macOS); not Windows native.")
    path = root / ".research/runtime" / (name + ".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise LabError("Another process owns %s. Do not delete an active lock." % name)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def event(root: Path, kind: str, payload: Dict[str, Any]) -> None:
    """Immutable event files, not a concurrently appended shared JSONL file."""
    path = root / ".research/events" / (stamp() + ".json")
    atomic(path, {"time_utc": now(), "kind": kind, **payload})


def config(root: Path) -> Dict[str, Any]:
    return load(root / "configs/sprint.json")


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(["git", *args], cwd=str(root), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise LabError("Git unavailable or timed out: " + str(exc))
    if check and result.returncode:
        raise LabError(result.stderr.decode("utf-8", "replace").strip() or "Git command failed")
    return result


def git_info(root: Path) -> Dict[str, Any]:
    try:
        head = git(root, "rev-parse", "--verify", "HEAD", check=False)
        branch = git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
        dirty = git(root, "status", "--porcelain", "--untracked-files=normal", check=False)
        return {"commit": head.stdout.decode().strip() if not head.returncode else None,
                "branch": branch.stdout.decode().strip() if not branch.returncode else None,
                "working_tree_dirty": bool(dirty.stdout) if not dirty.returncode else None}
    except LabError:
        return {"commit": None, "branch": None, "working_tree_dirty": None}


def inventory(root: Path, paths: Iterable[str], required: bool = True) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for item in paths:
        path = inside(root, item)
        if not path.exists():
            if required:
                raise LabError("Missing inventory input: " + item)
            continue
        candidates = sorted(path.rglob("*")) if path.is_dir() else [path]
        for candidate in candidates:
            rel = candidate.relative_to(root)
            if any(part in IGNORED_PARTS for part in rel.parts) or candidate.suffix == ".pyc":
                continue
            if candidate.is_symlink():
                raise LabError("Symlink in inventory: " + str(rel))
            if candidate.is_file():
                files[rel.as_posix()] = digest(candidate)
    return dict(sorted(files.items()))


def start(root: Path) -> int:
    with lock(root, "metadata"):
        path = root / ".research/SPRINT.json"
        if path.exists():
            print("Existing sprint retained; deadline was NOT restarted.")
            return status(root)
        cfg = config(root)
        hours = float(cfg["budget_hours"])
        reserve = float(cfg["report_reserve_minutes"])
        if not math.isfinite(hours) or not math.isfinite(reserve) or not 0 <= reserve < hours * 60:
            raise LabError("Invalid sprint budget/reserve.")
        beginning = time.time()
        record = {"schema_version": 1, "started_utc": now(), "started_unix": beginning,
                  "deadline_unix": beginning + hours * 3600,
                  "report_reserve_seconds": reserve * 60, "initial_config": cfg}
        atomic(path, record)
        event(root, "sprint_started", {"deadline_unix": record["deadline_unix"]})
    return status(root)


def remaining(root: Path, phase: str) -> float:
    record = load(root / ".research/SPRINT.json")
    cutoff = float(record["deadline_unix"])
    if phase != "audit":
        cutoff -= float(record["report_reserve_seconds"])
    return cutoff - time.time()


def status(root: Path) -> int:
    path = root / ".research/SPRINT.json"
    if not path.exists():
        print("Sprint has not started. Run: python3 tools/lab.py start")
    else:
        record = load(path)
        print(json.dumps({"started_utc": record["started_utc"],
                          "remaining_total_seconds": round(remaining(root, "audit")),
                          "remaining_experiment_seconds": round(remaining(root, "development")),
                          "deadline_utc": dt.datetime.fromtimestamp(record["deadline_unix"], dt.timezone.utc).isoformat()}, indent=2))
    counts: Dict[str, int] = {}
    for path in sorted((root / "results/runs").glob("*/run.json")):
        record = load(path)
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    print("Run statuses:", json.dumps(counts, sort_keys=True))
    print("Next: read .research/STATE.md and .research/PLAN.md.")
    return 0


def doctor(root: Path) -> int:
    required = ["AGENTS.md", "CODEX_PROMPT.md", "docs/RESEARCH_SPEC.md", "docs/WORKFLOW.md",
                ".research/STATE.md", ".research/PLAN.md", "configs/sprint.json"]
    missing = [p for p in required if not (root / p).is_file()]
    info = {"python": platform.python_version(), "platform": platform.system(),
            "cpu_count": os.cpu_count(), "posix_locks": fcntl is not None,
            "missing_files": missing, "git": git_info(root)}
    # No environment dump, credential discovery, hostname, username, or remote URL.
    print(json.dumps(info, indent=2))
    config(root)
    return 1 if missing or fcntl is None else 0


def freeze(root: Path, identifier: str, paths: List[str]) -> int:
    valid_id(identifier)
    with lock(root, "runner"), lock(root, "metadata"):
        target = root / ".research/freezes" / (identifier + ".json")
        if target.exists():
            raise LabError("Freeze ID already exists; create a new version, never overwrite it.")
        protocol = (root / "docs/PROTOCOL.md").read_text()
        if "Status: READY_TO_FREEZE" not in protocol.splitlines():
            raise LabError("Protocol is not ready. Complete it, then set its status explicitly.")
        if re.search(r"\b(?:UNRESOLVED|NOT_YET|NOT_CREATED|NOT_READY)\b", protocol):
            raise LabError("Protocol still contains unresolved starter placeholders.")
        files = inventory(root, paths)
        if not files:
            raise LabError("Cannot freeze an empty inventory.")
        if "docs/PROTOCOL.md" not in files:
            raise LabError("A freeze must include docs/PROTOCOL.md.")
        provenance = git_info(root)
        if provenance["commit"] is None:
            raise LabError("Commit the implemented protocol/code before freezing it.")
        # Ensure every frozen file is committed and unchanged; unrelated notes may be dirty.
        for rel in files:
            tracked = git(root, "ls-files", "--error-unmatch", "--", rel, check=False)
            changed = git(root, "diff", "HEAD", "--", rel)
            if tracked.returncode or changed.stdout:
                raise LabError("Freeze input is uncommitted: " + rel)
        atomic(target, {"schema_version": 1, "freeze_id": identifier, "time_utc": now(),
                        "git": provenance, "roots": paths, "sha256": files})
        event(root, "protocol_frozen", {"freeze_id": identifier, "file_count": len(files)})
    print(str(target.relative_to(root)))
    return 0


def verify(root: Path, identifier: str, verbose: bool = True) -> int:
    valid_id(identifier)
    record = load(root / ".research/freezes" / (identifier + ".json"))
    current = inventory(root, record["roots"])
    old = record["sha256"]
    changes = [name for name in sorted(set(old) | set(current)) if old.get(name) != current.get(name)]
    if changes:
        raise LabError("Frozen inputs changed/added/removed: " + ", ".join(changes[:30]))
    if verbose:
        print("Freeze verified:", identifier, "(%s files)" % len(current))
    return 0


def stop_group(proc: subprocess.Popen) -> None:
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    # Also clean up same-group descendants if their parent exited first.
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait(timeout=5)


def run(root: Path, args: argparse.Namespace) -> int:
    identifier = valid_id(args.id)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise LabError("Supply a command after --.")
    if any(SECRET_RE.search(token.encode()) for token in command):
        raise LabError("Possible secret in command. Do not put credentials in arguments.")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise LabError("Timeout must be finite and positive.")
    with lock(root, "runner"):
        seconds = min(args.timeout, remaining(root, args.phase))
        if seconds < 1:
            raise LabError("No budget remains for this phase; write/report the existing evidence.")
        if args.phase == "confirmation" and not args.freeze:
            raise LabError("Confirmation runs require --freeze ID.")
        if args.freeze:
            verify(root, args.freeze, verbose=False)
        result_dir = root / "results/runs" / identifier
        if result_dir.exists():
            raise LabError("Run ID already exists. Inspect it; never overwrite or silently rerun it.")
        result_dir.mkdir(parents=True)
        work_dir = root / "work/runs" / identifier
        work_dir.mkdir(parents=True, exist_ok=False)
        logpath = work_dir / "console.log"
        snapshot = inventory(root, SOURCE_ROOTS, required=False)
        atomic(result_dir / "source_hashes.json", snapshot)
        cfg = config(root)
        threads = max(1, min(4, int(cfg.get("max_threads", 4)), os.cpu_count() or 1))
        env = os.environ.copy()
        env.update({key: str(threads) for key in THREAD_VARS})
        env.update({"MPLBACKEND": "Agg", "PYTHONUNBUFFERED": "1",
                    "CORRLAW_RUN_ID": identifier,
                    "CORRLAW_RESULT_DIR": str(result_dir),
                    "CORRLAW_WORK_DIR": str(work_dir)})
        begin = time.monotonic()
        meta = {"schema_version": 1, "run_id": identifier, "task": args.task,
                "phase": args.phase, "freeze_id": args.freeze,
                "purpose": args.purpose, "command": command, "started_utc": now(),
                "timeout_seconds": seconds, "threads_requested": threads,
                "python": platform.python_version(), "platform": platform.system(),
                "git": git_info(root), "status": "running", "pid": None,
                "log_path": str(logpath.relative_to(root)), "result_validation": "NOT_REVIEWED"}
        atomic(result_dir / "run.json", meta)
        event(root, "run_started", {"run_id": identifier, "task": args.task})
        proc = None
        exit_code = None
        outcome = "failed"
        error = None
        try:
            with logpath.open("wb") as output:
                proc = subprocess.Popen(command, cwd=str(root), env=env, stdout=output,
                                        stderr=subprocess.STDOUT, start_new_session=True)
                meta["pid"] = proc.pid
                atomic(result_dir / "run.json", meta)
                exit_code = proc.wait(timeout=seconds)
                outcome = "completed" if exit_code == 0 else "failed"
        except subprocess.TimeoutExpired:
            outcome = "timed_out"
            if proc is not None:
                stop_group(proc)
                exit_code = proc.returncode
        except KeyboardInterrupt:
            outcome = "interrupted"
            if proc is not None:
                stop_group(proc)
                exit_code = proc.returncode
        except OSError as exc:
            error = str(exc)
            outcome = "failed"
        finally:
            # Workers must not daemonize; clean up any remaining same-group children.
            if proc is not None and proc.poll() is not None:
                for sig in (signal.SIGTERM, signal.SIGKILL):
                    try:
                        os.killpg(proc.pid, sig)
                    except ProcessLookupError:
                        break
            try:
                after = inventory(root, SOURCE_ROOTS, required=False)
                changed = sorted(p for p in set(snapshot) | set(after) if snapshot.get(p) != after.get(p))
            except LabError as exc:
                changed = [str(exc)]
            if changed:
                outcome = "invalidated_source_changed"
                meta["source_changes"] = changed
            if args.freeze:
                try:
                    verify(root, args.freeze, verbose=False)
                except LabError as exc:
                    outcome = "invalidated_freeze_changed"
                    meta["freeze_error"] = str(exc)
            meta.update({"status": outcome, "ended_utc": now(), "returncode": exit_code,
                         "duration_seconds": round(time.monotonic() - begin, 6), "error": error,
                         "log_sha256": digest(logpath) if logpath.exists() else None})
            atomic(result_dir / "run.json", meta)
            event(root, "run_finished", {"run_id": identifier, "status": outcome,
                                          "duration_seconds": meta["duration_seconds"]})
        print(json.dumps(meta, indent=2))
        return 0 if outcome == "completed" else 1


def reconcile(root: Path) -> int:
    """Explicit recovery after a hard kill. Never kill a PID inferred from an old file."""
    with lock(root, "runner"):
        pending = []
        for path in sorted((root / "results/runs").glob("*/run.json")):
            record = load(path)
            if record["status"] != "running":
                continue
            pid = record.get("pid")
            if pid:
                try:
                    os.kill(pid, 0)
                    raise LabError("PID %s exists for %s. Inspect it; it may be active or reused. "
                                   "No automatic killing or reassignment." % (pid, record["run_id"]))
                except ProcessLookupError:
                    pass
                except PermissionError:
                    raise LabError("Cannot establish whether recorded PID is active; inspect manually.")
            pending.append((path, record))
        for path, record in pending:
            record.update({"status": "interrupted_unverified", "reconciled_utc": now(),
                           "result_validation": "NOT_REVIEWED"})
            atomic(path, record)
            event(root, "orphaned_run_reconciled", {"run_id": record["run_id"]})
        print("Marked %s orphaned runs interrupted; partial artifacts were preserved." % len(pending))
    return 0


def checkpoint(root: Path, message: str, paths: List[str]) -> int:
    """Commit only named leaf paths, refusing any pre-existing staging area."""
    if not config(root).get("local_commits", True):
        raise LabError("Local commits disabled in configs/sprint.json.")
    if not message.strip():
        raise LabError("Commit message cannot be empty.")
    with lock(root, "runner"), lock(root, "git"):
        top = git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if Path(top).resolve() != root.resolve():
            raise LabError("Starter must be at the Git repository root, not in a nested folder.")
        if git(root, "diff", "--name-only", "--diff-filter=U").stdout:
            raise LabError("Unresolved merge conflicts; do not checkpoint.")
        if git(root, "diff", "--cached", "--name-only", "-z").stdout:
            raise LabError("Pre-existing staged changes found. Do not include or unstage another person's work.")
        if git(root, "symbolic-ref", "--quiet", "HEAD", check=False).returncode:
            raise LabError("Detached HEAD: choose a safe branch before committing.")
        if not paths:
            raise LabError("Name the exact files to commit.")
        selected = []
        for name in paths:
            path = inside(root, name)
            parts = Path(name).parts
            if not parts or name in (".", "./") or path.is_dir():
                raise LabError("Only exact file paths, not directories, are accepted: " + name)
            if any(p in IGNORED_PARTS for p in parts) or parts[0] == "work" or parts[:2] == (".research", "runtime"):
                raise LabError("Local/cache/private path cannot be committed: " + name)
            if path.name.startswith(".env") or path.suffix.lower() in (".pem", ".key", ".p12", ".pfx"):
                raise LabError("Sensitive filename cannot be committed: " + name)
            if path.exists():
                if path.stat().st_size > int(config(root).get("max_tracked_file_bytes", 2097152)):
                    raise LabError("File exceeds checkpoint limit; retain locally with hash/reproduction metadata: " + name)
                if SECRET_RE.search(path.read_bytes()):
                    raise LabError("Possible secret found. Review/remove it before committing: " + name)
                if git(root, "check-ignore", "--quiet", "--", name, check=False).returncode == 0:
                    raise LabError("Ignored file cannot be force-added: " + name)
            elif git(root, "ls-files", "--error-unmatch", "--", name, check=False).returncode:
                raise LabError("Missing file is not a tracked deletion: " + name)
            selected.append(name)
        git(root, "add", "--", *selected)
        diff = git(root, "diff", "--cached", "--check", check=False)
        if diff.returncode:
            raise LabError("Staged whitespace errors. Inspect staging; the helper did NOT unstage it.")
        if not git(root, "diff", "--cached", "--name-only").stdout:
            print("No selected changes to commit.")
            return 0
        # Repository hooks are honored. A hook failure leaves the index for inspection.
        result = git(root, "commit", "-m", message, check=False)
        print(result.stdout.decode("utf-8", "replace"), end="")
        if result.returncode:
            raise LabError("Commit failed; staged files retained for inspection. " + result.stderr.decode("utf-8", "replace"))
        print("Local commit saved. Nothing was pushed.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project root (normally auto-detected).")
    sub = parser.add_subparsers(dest="action", required=True)
    for command in ("doctor", "start", "status", "reconcile"):
        sub.add_parser(command)
    p = sub.add_parser("note")
    p.add_argument("--kind", required=True)
    p.add_argument("--text", required=True)
    p = sub.add_parser("freeze")
    p.add_argument("--id", required=True)
    p.add_argument("--paths", nargs="+", required=True)
    p = sub.add_parser("verify")
    p.add_argument("--id", required=True)
    p = sub.add_parser("checkpoint")
    p.add_argument("--message", required=True)
    p.add_argument("--paths", nargs="+", required=True)
    p = sub.add_parser("run")
    p.add_argument("--id", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--purpose", required=True)
    p.add_argument("--phase", choices=("development", "confirmation", "audit"), default="development")
    p.add_argument("--freeze")
    p.add_argument("--timeout", type=float, required=True, help="Maximum subprocess wall-clock seconds.")
    p.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.action == "doctor":
            return doctor(root)
        if args.action == "start":
            return start(root)
        if args.action == "status":
            return status(root)
        if args.action == "note":
            event(root, args.kind, {"text": args.text})
            return 0
        if args.action == "freeze":
            return freeze(root, args.id, args.paths)
        if args.action == "verify":
            return verify(root, args.id)
        if args.action == "run":
            return run(root, args)
        if args.action == "reconcile":
            return reconcile(root)
        if args.action == "checkpoint":
            return checkpoint(root, args.message, args.paths)
        raise LabError("Unknown action")
    except (LabError, OSError, ValueError, KeyError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
