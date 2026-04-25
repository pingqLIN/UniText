# Project Development Loop - Longer Runtime General Memo

Date: 2026-04-25
Status: working memo, not formal policy
Scope: general `$project-development-loop` improvement advice, not UniText-specific
Raw archive: `C:\Users\miles\.agents\.little_talks\2026-04-25_project-development-loop-longer-runtime-general.md`

## Background

This memo generalizes a prior long-running `$project-development-loop` stop check. The prior run continued for almost seven hours and stopped at a clean checkpoint, not because of a hard blocker. The remaining work was broader and safer to treat as a separate batch.

That behavior is safe, but it can cause an explicit long-running loop to underuse the requested runtime. The procedure needs a stronger middle layer between "finished current batch" and "stop cleanly".

## Core Diagnosis

The loop should not treat "the next task is larger or ambiguous" as an automatic stop condition.

For long-duration or overnight usage, that state should usually become:

1. classify the stop reason,
2. decompose the larger task if it is safe,
3. choose a smaller reviewable slice,
4. continue from the durable backlog,
5. stop only if a hard guardrail or true lack of safe work remains.

## General Recommendations

### 1. Add a Minimum Runtime Policy

For Pattern B and Pattern C, the invocation should support language such as:

```text
Continue until the deadline unless a hard guardrail is hit, the remaining time is insufficient for a safe reviewed task, or no safe micro/small maintenance task remains.
```

This prevents the loop from stopping early simply because the obvious next item is not immediately executable.

### 2. Replace Binary Stop/Continue With a Stop Taxonomy

Use explicit stop classes:

- `hard_stop`: auth, secrets, billing, quota, destructive operation, production mutation, unclear high-risk architecture fork.
- `time_stop`: remaining time cannot safely cover implementation, review, and handoff.
- `checkpoint_stop`: current batch is complete, but safe work may remain.
- `decomposition_needed`: next work is too broad as stated, but can be sliced.
- `backlog_exhausted`: no safe and meaningful maintenance, optimization, or documentation work remains.

Only `hard_stop`, `time_stop`, and true `backlog_exhausted` should normally end a time-boxed run before the requested boundary.

### 3. Maintain a Pre-Ranked Backlog

Long-running loops need a durable backlog, not only conversational intent. The backlog should classify tasks by size and risk:

- `micro`: 5-20 minutes, low risk, easy validation.
- `small`: 20-60 minutes, one reviewable change.
- `medium`: 1-3 hours, bounded but needs stronger review.
- `large`: requires decomposition before execution.

When the current task completes, the loop should pick the next safe `micro` or `small` item before stopping.

### 4. Add a Decompose-and-Continue Rule

When the next item is valuable but too large, the loop should create slices instead of ending:

```text
If the next task is broad but not blocked by a hard guardrail, write a brief decomposition, execute the first safe slice, and park the rest in the durable backlog.
```

This keeps the run active without drifting into an unreviewable refactor.

### 5. Reserve a Final Review Window Without Ending Too Early

For long runs, reserve the final 10-15% of the budget for review, validation, and handoff. Before that window, the loop should keep opening safe small tasks.

Example:

- 4HR run: reserve roughly 25-35 minutes.
- Overnight run: reserve the final 45-75 minutes.

The final window should be for consolidation, not a reason to stop hours early.

### 6. Strengthen Durable Supervisor State

Pattern B and Pattern C already require external state. The state file should explicitly include:

- requested deadline or duration,
- minimum runtime policy,
- active batch,
- current task size and risk,
- last activity timestamp,
- last completed checkpoint,
- stop class if stopping,
- next three safe actions,
- blocked reasons,
- test and review budget,
- whether decomposition mode is active.

This makes early stops auditable and makes resume behavior less dependent on chat memory.

### 7. Add an Idle-Prevention Fallback Queue

If no direct next feature or fix is ready, the loop should enter a safe optimization queue:

- test coverage gaps,
- lint or health-check failures,
- stale docs or examples,
- onboarding friction,
- TODO/FIXME triage,
- flaky or skipped test review,
- dependency or script drift,
- error-message clarity,
- developer tooling and diagnostics.

This queue should still obey project safety rules and avoid speculative product expansion in overnight mode.

### 8. Use Review Budget Modes

Not every slice needs heavyweight review. Suggested modes:

- `local_quick`: docs, examples, small tests, low-risk scripts.
- `local_deep`: shared behavior, parser changes, workflow changes.
- `external_reviewer`: auth, reliability, data flow, architecture, broad refactor.

The loop should avoid stalling on unnecessary review, but escalate review when risk justifies it.

### 9. Park Large Work Safely

Large tasks should not force a stop if smaller related work can proceed. Park them as:

- a decomposition memo,
- a backlog entry,
- a worktree candidate,
- or a future review gate.

Only create a worktree when it directly enables safe isolated execution. Otherwise, a parked plan plus a smaller next task is enough.

### 10. Require a Rich Early-Stop Report

If a loop stops before the requested boundary, the final report should always state:

- requested runtime or deadline,
- actual runtime,
- stop class,
- exact evidence for the stop,
- why the loop did not continue,
- next three safe actions,
- whether a new worktree or special project is recommended.

This turns early stops into diagnosable process events instead of ambiguous conversation endings.

## Suggested Invocation Phrases

```text
$project-development-loop overnight until 07:00;
minimum-run policy: decompose larger work into small slices;
stop only for hard guardrails, final review window, or no safe micro/small tasks remaining.
```

```text
$project-development-loop 6HR;
if the direct backlog is exhausted, enter optimization fallback:
tests, docs drift, health scripts, onboarding polish, diagnostics.
```

```text
$project-development-loop 4HR;
after every checkpoint, classify stop/continue state;
if the next task is large, decompose and run the first safe slice.
```

## Candidate Formal Outputs

- Generic Pattern B/C longer-runtime SOP.
- `$project-development-loop` skill update proposal.
- Durable supervisor state schema.
- Backlog queue template for long-running maintenance.
- Early-stop report template.

## Preferred Direction

The highest-value improvement is not making the loop more aggressive. It is making continuation safer and more mechanical:

```text
checkpoint complete -> classify -> choose backlog item -> decompose if needed -> execute next safe slice -> review -> repeat
```

That change should increase runtime while preserving the original safety goal of bounded, reviewable work.
