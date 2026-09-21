# User-authorized overnight continuation

Authorization: user asked to keep working unattended until08:00 India time on
22September2026. The recorded harddeadline is02:30UTC; newexperiments stop01:30UTC.
The original SPRINT clock is preserved. OVERNIGHT.json narrows its deadline, and
lab.py enforces the earlier bound. The native active goal is the primary continuation
mechanism; the local watchdog is a fallback for stalled progress in this same thread.

Implementation: tools/overnight_watchdog.py invokes the installed Codex CLI's
`queue --thread ... --message ...` against thread
01a0c4e7-a53d-76a2-a9b2-233b0a5bea85. It does not launch a competing agent/session,
change global configuration, or message another person. Queue acceptance was tested;
timed deliveries were also accepted. Acceptance is not a guarantee that the app,
service, laptop or a later turn will remain available.

Current policy: poll every60seconds, queue only after15minutes without genuine
source/state/run progress, at mostone accepted nudge for each unchanged progress
state. Failed queue attempts can retry. Every reminder preserves active processes,
the one-writer rule, the deadline, and any later user stop/scope change. The earlier
periodic version generated three accepted reminders before it was refined; those
records are retained, not represented as idle-triggered deliveries.

Operational files (ignored local work directory):
- work/overnight-watchdog/pid: current daemon PID (not a permanent identifier).
- health.json: last check and latest real progress timestamp.
- deliveries.jsonl: actual CLI acceptance/failure records.
- STOP: creating this file cancels future nudges within the poll interval.
- stopped.json: deadline/stop-file reason when the daemon exits normally.

A single-instance flock prevents duplicate daemons. A scoped `caffeinate -i -w PID`
process follows the watchdog's lifetime and does not alter persistent power settings.
It ends when that daemon ends. The watchdog's harddeadline is unconditional; it
cannot extend research authorization. Stop it early when the work is completed or
the user requests stopping. No new jobs may be started simply to keep it busy.

Evidence: OVERNIGHT.json stores the initial acceptance ID; retained local delivery
log includes accepted messages at18:13:55,18:40:18 and18:55:19UTC. At19:34UTC the
idle-only daemon reports recentprogress while development002 advances. The process
uses bounded command timeouts and never treats its own heartbeat as task progress.
