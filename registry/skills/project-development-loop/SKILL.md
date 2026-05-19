---
name: project-development-loop
description: "Autonomous repo-maintenance loop for existing codebases only when the user explicitly invokes `$project-development-loop`/`project-development-loop`, asks for a time-boxed or overnight development loop, or clearly requests continuous repo execution through audit, implementation, review, reporting, and repeat. Do not use for one-off repo status reports, simple code review, normal bug fixes, planning-only tasks, skill editing, greenfield bootstrap, or requests that merely mention progress, audit, next steps, or development plans without asking to keep executing."
---

# Project Development Loop

## Overview

Use this skill only after an explicit invocation or a clearly continuous development-loop request for an existing codebase.
A normal repo question, status audit, plan draft, bug fix, review, or skill-editing request is not enough to enter this loop by itself.
Always operate in YOLO-style autonomy: start from evidence, not assumptions; audit the repo; choose the next work; execute, delegate, review, and report with minimal waiting; and repeat until there is no justified work left.
Once this skill is intentionally in scope, the user does not need to say `YOLO`, `yolo`, or any related trigger phrase. Invoking this skill already means autonomous execution unless a higher-priority instruction explicitly forces checkpoints.
This skill starts from existing project artifacts. It is not the right entry point for greenfield project bootstrap.

## Invocation Interpretation

Interpret the user's wording with these rules. Do not ask them to specify a profile name.
Before applying the patterns, verify that the skill was intentionally invoked. A clear invocation means explicit `$project-development-loop` / `project-development-loop`, or wording that combines repo development with keep-working, autonomous continuation, a duration, a deadline, sleep, or overnight execution. If the user only asks for a status report, code review, development plan, one bounded fix, or skill metadata cleanup, handle that task normally and do not start the loop.

### Pattern A: no explicit time

If the invocation does not include a clear duration, cutoff, or end time, treat it as maintenance mode.

- assume the user wants project maintenance first
- audit the repo for unfinished implementation items, partial tasks, documented TODOs, blocked follow-ups, and drift between code and docs
- implement the highest-value unfinished item that is justified by repo evidence
- if no unfinished development item is found, pivot into optimization and maintenance work such as hardening, tests, docs completion, onboarding cleanup, and operational polish
- prefer finishing existing intent over inventing new branch features
- stop cleanly once no meaningful maintenance, optimization, or documentation gap remains

### Pattern B: explicit duration or end time

If the invocation includes a clear budget such as `30m`, `2h`, `until 03:00`, or another explicit length, treat it as aggressive time-boxed development mode.

- treat this as the highest-throughput mode
- restate the budget and convert it into a concrete stopping boundary
- spend only the minimum needed startup slice on audit and planning, then keep executing until the boundary
- use the same maintenance-first ordering as Pattern A for baseline work
- after baseline work is complete, no active bug is found, and an external reviewer or equivalent independent review indicates no further optimization is currently justified, branch-feature development becomes allowed if it does not violate any higher-priority rule
- prefer tasks that can still land with review quality before the cutoff, but allow broader batches than maintenance mode when they remain plausibly reviewable
- avoid idle waiting, recap-heavy turns, or non-essential confirmation
- stop only at the deadline, when the remaining time is insufficient for a safe next task, or when a hard guardrail is hit

### Pattern C: `sleep`, `overnight`, and similar wording

If the invocation mentions `sleep`, `overnight`, `??`, or equivalent wording, treat it as overnight maintenance mode even if a time is also supplied.

- this mode follows Pattern A prioritization, not Pattern B branch-feature ambition
- assume multiple processes may be active at the same time
- favor bounded, reviewable maintenance batches over one large refactor
- leave the repo in a readable state at each stage boundary with review notes and a stage report
- bias toward stability, resumability, and morning handoff quality over raw throughput
- avoid destructive cleanup, irreversible migrations, production actions, or ambiguous architecture pivots unless the user explicitly pre-approved them

## Time Budget Rules

- If the user gives a duration or end time, honor it as a hard planning input.
- Pattern A has no inferred countdown. Work until the current justified maintenance batch is complete.
- Pattern B maximizes active execution time and reserves only the smallest realistic final slice for review and reporting.
- Pattern C may also have a duration or wake boundary, but it should still optimize for safe unattended increments rather than aggressive expansion.
- If there is not enough time left to complete and review a new task safely, stop opening new work.
- For overnight runs, bias toward multiple reviewed increments rather than one unfinished large change.

If the user explicitly asks for slower supervision, checkpoints, or approval before edits, temporarily downgrade to supervised behavior for that turn.

## External Process Requirement

Pattern B and Pattern C require durable external-process support. Do not rely on the live model session alone.

Accepted examples:

- a repo-local CLI wrapper
- a PowerShell or shell batch runner
- a task scheduler entry
- a watcher script that writes checkpoints, status, and telemetry to disk or another durable sink

Minimum requirements for Pattern B:

- persist the active batch, deadline, last completed checkpoint, and next intended action outside the model session
- make the run resumable if the host session or agent process exits unexpectedly
- write enough structured state that the next audit can recover without guessing

Additional requirements for Pattern C:

- run timed monitoring through an external process instead of purely in-session polling
- monitor total machine-level token usage when multiple agent processes may be active
- provide periodic feedback back to the project execution agent or its durable state channel so task width, cadence, or batching can be adjusted
- record threshold breaches or abnormal growth as visible blockers for the next audit

## Scheduled Automation Ideas

Borrow these ideas when designing unattended loops, overnight runs, or deadline-driven runs:

- Package repeatable work into a reusable command, script, or skill invocation instead of freehand prompts each time.
- Treat short-interval loops as session-scoped helpers, not durable orchestration. If the host session exits, assume the loop is gone.
- Persist high-signal state outside the model session because unattended runs can end unexpectedly.
- Favor resume-friendly batches. If a run is interrupted, the next audit should be able to pick up from saved evidence.
- Use explicit deadlines and batch boundaries instead of vague "keep going for a while" instructions.
- Avoid scheduling exact boundary times when precise timing matters; add a small offset to reduce collisions and timing surprises.
- For automation that must survive restarts, use durable schedulers outside the session rather than relying on session-only loops.
- For Pattern B and Pattern C, prefer writing or reusing a thin external supervisor rather than keeping orchestration logic implicit in conversational state.
- For Pattern C, include a timed telemetry path for whole-machine token usage and a feedback path that the execution agent can actually consume.

Read [references/scheduled-automation.md](./references/scheduled-automation.md) when you need the distilled notes from the Claude scheduled-tasks docs.

## Core Rules

- Read repository instructions first, including `AGENTS.md`, workflow docs, roadmap docs, and task trackers when present.
- Build the initial picture from real artifacts: git status/history, README, roadmap/spec docs, package or build files, key entrypoints, existing tests, and the current code paths that implement headline features.
- Compare three views before planning: stated goal, recorded history, and actual code.
- Distinguish clearly between `goal`, `in_progress`, `done`, `blocked`, `unknown`, and `optimization`.
- Quantify completion conservatively. Use ranges or words like `partial`, `mostly done`, or `unclear` when exact percentages would be fake precision.
- Move from audit to action without waiting for extra confirmation unless the next choice is genuinely consequential.
- Do not delegate or spawn subagents unless the active environment and user request explicitly allow delegation. If delegation is not authorized, still perform the evaluation and state the recommended structure.
- Prefer direct execution when the next task is obvious and bounded. Write a plan first when the work is broad, risky, or has multiple plausible branches.
- Treat review as a real gate, not a ceremonial recap. Look for regressions, missing tests, incomplete edge cases, and plan drift.
- In Pattern B and Pattern C, prefer tasks with clean stop points and summarize progress at every phase boundary.
- In Pattern B, bias toward throughput over comfort. Keep momentum high until the time boundary.
- In Pattern A and Pattern C, prefer existing unfinished work, optimization, and documentation completion over speculative new features.
- In Pattern B, do not start branch-feature work until maintenance-first gates have been satisfied and independent review says further optimization is unnecessary for now.
- When Codex Calendar Todo is available, record high-signal milestones there so the next loop can rebuild context quickly.

## Loop

### 1. Audit the current project state

Perform a fast but evidence-based startup audit.

Check at least these sources when they exist:

- repo instructions such as `AGENTS.md`
- `README`, roadmap, spec, milestone, changelog, or progress docs
- git branch, recent commits, dirty files, open review notes, or TODO markers
- app entrypoints, server entrypoints, main UI surface, tests, and scripts

Produce a concise progress snapshot covering:

- project goal
- completed capabilities
- work in progress
- blocked or unstable areas
- missing but planned capabilities
- confidence level of the audit

Read [references/templates.md](./references/templates.md) when you need a reusable progress snapshot format.
Immediately follow the snapshot with the next action instead of waiting for permission.

### 2. Decide plan-first vs dispatch-first

Dispatch immediately when all of the following are true:

- the next task is already clear from the audit
- the task is bounded enough to finish in one round
- dependencies are understood
- there is no meaningful architecture fork to resolve first

Write a development plan first when any of the following are true:

- there are multiple unresolved next steps
- the code and docs disagree materially
- the work needs sequencing across modules
- the user asked for planning, roadmap, or task decomposition
- the task likely benefits from review checkpoints or multi-agent coordination

When writing a plan, keep it executable. Include intended outcome, task order, review points, and what counts as done.
Write the plan only as much as needed to unlock execution, then start the first step in the same turn whenever feasible.
In Pattern B and Pattern C, include explicit batch boundaries and a stop condition tied to the remaining time.

### 3. Evaluate execution shape

Choose the lightest structure that matches the difficulty.

Use this rubric:

- Light: one bounded fix, one module, low uncertainty. Work locally. Review locally after implementation.
- Medium: several related edits, moderate uncertainty, or one meaningful verification sidecar. Use one lead agent plus optional reviewer or one worker if delegation is explicitly allowed.
- Heavy: broad refactor, ambiguous product state, architecture tradeoffs, or high regression risk. Prefer a strong reviewer first, then split execution into disjoint worker tasks if delegation is explicitly allowed.
- Critical: high-risk data, auth, sync, migration, reliability, or release work. Use the highest-reasoning reviewer available before and after execution, and use workers only with clearly separated ownership.

Model choice should follow capability class, not hard-coded product names:

- reviewer: highest-reasoning available model
- lead implementer: strong coding model with enough reasoning for the task
- worker: smaller or cheaper coding model for bounded subtasks
- explorer: fast low-cost model for repo reconnaissance

If subagents are not allowed, state the recommended reviewer-worker shape anyway and continue locally.
Prefer parallel delegation only when it shortens the critical path and write scopes are clearly separated.
In Pattern C, avoid deep dependency chains that could leave the run stalled on one blocked branch.

### 4. Execute and review

After execution, run a review pass before declaring progress.

Review should confirm:

- requested behavior exists in code
- adjacent behavior was not broken
- tests or runtime checks cover the change enough for the task class
- docs, plan, or progress notes still reflect reality

When the task is substantial, summarize what changed and what remains before moving to the next loop.
Treat review as the handoff gate into the next task selection, not the end of the session.

### 5. Write a stage completion report

After a meaningful task cluster or phase, write a short stage report.

Cover:

- what was completed
- what was validated
- what risks remain
- what should happen next
- whether outside review is recommended

Read [references/templates.md](./references/templates.md) when you need a reusable stage report template.
Keep the report short enough that it does not stall the next loop.
In Pattern B and Pattern C, always emit a final stage report before the budget ends.

### 6. Evaluate external review

Consider external review when:

- the phase changed architecture or data flows
- the work touched reliability, sync, auth, security, or compatibility
- implementation confidence is lower than the impact radius
- the user explicitly values independent validation

If external review is not worth the cost, say so briefly and continue.

### 7. Repeat or switch to optimization mode

Return to step 1 after each reviewed phase.

If the new audit finds no meaningful pending development items, decide whether to stop or pivot into optimization mode.

Enter optimization mode only when at least one of these is true:

- the user asked to keep improving
- the user gave a time budget for continued iteration
- the product is functionally complete but still has clear polish gaps

Optimization mode should look for cross-cutting improvement areas such as:

- multi-platform behavior and consistency
- onboarding and beginner friendliness
- UX and UI clarity
- reliability, resilience, and fallback behavior
- performance and stability
- compatibility with adjacent tools, integrations, or sister projects
- maintainability, test coverage, and operability

Pattern-specific follow-through:

- Pattern A: if there is no pending unfinished work, shift to optimization and documentation completion; stop when those are also exhausted
- Pattern B: if maintenance and optimization are both exhausted and review remains positive, branch-feature development may begin as a final expansion layer within the remaining budget
- Pattern C: if maintenance and optimization are both exhausted, stop cleanly rather than inventing ambitious new work

If there is no pending development work and no explicit signal to continue optimizing, stop cleanly.
If the user did signal continued development time or optimization intent, restart the loop with optimization targets instead of feature-gap targets.

## Output Contract

Unless the user asked for a different format, structure each loop result in this order:

1. Project state snapshot
2. Recommended next action
3. Execution shape recommendation
4. Review findings after work completes
5. Stage completion report
6. Continue, optimize, or stop

Use the templates in [references/templates.md](./references/templates.md) when you need more structure, but keep outputs concise.

## Autonomy Guardrails

Do not auto-continue across these boundaries without surfacing the risk:

- destructive file or data operations
- production deployment or live environment mutation
- auth, secrets, billing, quota, or compliance implications
- unclear architecture forks with long-term consequences
- low-confidence assumptions that could waste major effort

Do not auto-continue these at all in Pattern C unless the user explicitly pre-authorized them:

- destructive cleanup across many files
- migrations with difficult rollback
- production deployment
- secret rotation or auth boundary changes
- large dependency upgrades with unknown blast radius

When one of these appears, pause briefly, state the decision, state the tradeoff, and ask only the narrow question required to proceed.

## Codex Calendar Todo Integration

Use this integration when `Codex Calendar Todo` is available as the local planning hub.

Default API assumptions:

- health check: `http://127.0.0.1:4321/api/health`
- intake endpoint: `http://127.0.0.1:4321/api/agents/intake`

Log only high-value items, not every tiny step. Good moments to record are:

- startup audit summary
- chosen active batch or plan headline
- major blocker that should remain visible
- stage completion report
- overnight final report
- next recommended task for the next session

Prefer concise titles with a stable prefix such as:

- `[Audit]`
- `[Batch]`
- `[Stage]`
- `[Overnight]`
- `[Optimize]`

Use `scripts/log-codex-calendar-todo.mjs` to write a standardized intake item. The script supports dry runs, relative times, optional event windows, and `--paths` for file or folder references that the UI can turn into links.

Suggested patterns:

- after audit: log one todo capturing the repo state and next action
- before Pattern B or Pattern C execution: log the active batch with the cutoff time
- after review: log the stage report and the next recommended task
- after Pattern C: log a morning-ready summary with deferred risks

If the API is unavailable, continue the development loop and include the report in the normal response instead of blocking.

## Suggested Invocation Phrases

- `Use $project-development-loop to audit this repo and keep moving until the next reviewed milestone.`
- `Use $project-development-loop for 2 hours and keep working continuously until the deadline, stopping only for guardrails or final review.`
- `Use $project-development-loop sleep until 07:00 to work in bounded reviewed batches and leave a morning report.`
