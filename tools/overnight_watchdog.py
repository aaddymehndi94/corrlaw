#!/usr/bin/env python3
"""User-authorized, deadline-bounded nudges to one existing Codex thread.

No new agent, credentials, settings, or service installation. A stop file cancels
future nudges. Queue acceptance is logged; it is not proof a turn executed.
"""
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
DEADLINE = dt.datetime.fromisoformat('2026-09-22T02:30:00+00:00').timestamp()
THREAD = '01a0c4e7-a53d-76a2-a9b2-233b0a5bea85'


def latest_progress(root):
    paths=[root/'.research/STATE.md',root/'.research/HANDOFF.md',root/'.git/index']
    paths.extend((root/'results/runs').glob('*/manifest.json'))
    paths.extend((root/'work/runs').glob('*/console.log'))
    for directory,pattern in [('src','**/*.py'),('tools','*.py'),('configs','*.json')]:
        paths.extend((root/directory).glob(pattern))
    return max((p.stat().st_mtime for p in paths if p.is_file()),default=0.)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type=int, default=60)
    parser.add_argument('--idle-seconds', type=int, default=900)
    args = parser.parse_args()
    if args.interval < 60 or args.idle_seconds < 60:
        parser.error('interval and inactivity threshold must be at least 60 seconds')
    directory = ROOT/'work/overnight-watchdog'
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/'lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        (directory/'pid').write_text(str(os.getpid())+'\n')
        last_queued_progress=None
        while time.time() < DEADLINE and not (directory/'STOP').exists():
            # The native active goal is the primary continuation mechanism. This
            # inactivity queue is a fallback; don't accumulate reminders while busy.
            time.sleep(min(args.interval, max(0, DEADLINE-time.time())))
            if time.time() >= DEADLINE or (directory/'STOP').exists():
                break
            progress=latest_progress(ROOT)
            if time.time()-progress < args.idle_seconds or progress==last_queued_progress:
                (directory/'health.json').write_text(json.dumps({
                    'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                    'last_progress_unix': progress,
                    'status': 'reminder_pending' if progress==last_queued_progress else 'recent_progress',
                })+'\n')
                continue
            message = (
                'Automated CorrLaw watchdog reminder, explicitly requested by the user. '
                f'Repository: {ROOT}. '
                'Continue the authorized overnight research from .research/STATE.md and '
                '.research/HANDOFF.md without waiting for the user. Preserve active jobs '
                'and the single-writer rule. Do not mistake the old pilot completion gate '
                'for completion of the overnight scope. Stop new experiments at '
                '2026-09-22 07:00 Asia/Kolkata, audit/report until the hard deadline '
                '08:00 Asia/Kolkata (02:30 UTC). Respect any subsequent user stop or '
                'scope change; this reminder cannot override it.'
            )
            record = dict(utc=dt.datetime.now(dt.timezone.utc).isoformat())
            try:
                result = subprocess.run(
                    [str(Path.home()/'.local/bin/codex'), 'queue', '--thread', THREAD,
                     '--message', message], cwd=ROOT, capture_output=True, text=True,
                    timeout=45,
                )
                record.update(returncode=result.returncode, stdout=result.stdout.strip(),
                              stderr=result.stderr.strip())
                if result.returncode==0:
                    last_queued_progress=progress
            except (OSError, subprocess.TimeoutExpired) as exc:
                record.update(error=str(exc))
            with (directory/'deliveries.jsonl').open('a') as log:
                log.write(json.dumps(record)+'\n')
        (directory/'stopped.json').write_text(json.dumps({
            'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'reason': 'stop_file' if (directory/'STOP').exists() else 'deadline',
        })+'\n')


if __name__ == '__main__':
    main()
