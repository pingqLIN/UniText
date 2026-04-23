# Scheduled Automation Notes

These notes distill useful ideas from the Claude Code scheduled-tasks documentation:

- Session-scoped scheduling is good for quick polling while the session stays open.
- Session-scoped schedules are not durable across restarts.
- Missed schedule times do not replay one-by-one later; the next run happens when the system becomes available.
- Local timezone matters for scheduled times.
- Small timing offsets and jitter exist in real schedulers, so exact top-of-hour expectations are brittle.
- Recurring schedules need expiry or refresh rules so forgotten loops do not run forever.

How to apply that thinking to this skill:

- Make unattended work deadline-driven and batch-oriented.
- Persist important state outside the model context.
- Keep each batch resumable.
- Prefer durable schedulers for jobs that truly must survive restarts.

Source:

- https://code.claude.com/docs/en/scheduled-tasks
