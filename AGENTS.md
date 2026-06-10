# AGENTS.md

> Scope: repo-local baseline for coding agents and automation.
> Audience: coding agents and reviewers working inside this repository.
> Precedence: stricter higher-level instructions may add constraints; they never weaken this file.

## Mission

Operate from the smallest relevant surface, keep shared resources reviewable, and keep local or sensitive state out of shared docs.

## Non-negotiable rules

1. Do not push, upload, paste, post, or publish repository content without explicit user approval.
2. Do not treat a private remote, clean branch, or publishability report as publication permission.
3. Do not place secrets, live workspace values, or machine-specific state into shared surfaces.
4. Do not silently rewrite host configuration without a reviewed dry-run path.
5. Do not permanently delete files unless the request is explicit.

## Startup order

Use the smallest entrypoint that fits the task.

1. `RUNTIME.md`
2. `INDEX.md`
3. `OPERATIONS.md`
4. `DOCUMENT_PLACEMENT_POLICY.md`
5. `NO_PUBLISH_POLICY.md`

## Allowed without extra approval

- inspect repository files
- compare docs for ambiguity or drift
- draft documentation rewrites
- propose file locations
- run read-only or dry-run validation steps
- prepare handoff notes and review summaries

## Requires explicit approval

- `git push`
- uploading repository content to a network service
- posting to social platforms or cloud docs
- host-config mutation without dry-run review
- permanent file deletion
- publishing only part of a document when approval scope is ambiguous

## Session startup

For a new session, prefer:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\git-startup.ps1
```

## Handoff contract

When task is complete, report:

- files changed
- rationale
- validation performed
- assumptions still open
- approval-gated actions intentionally deferred

## Related docs

- `RUNTIME.md`
- `INDEX.md`
- `OPERATIONS.md`
- `DOCUMENT_PLACEMENT_POLICY.md`
- `NO_PUBLISH_POLICY.md`
- `SECRET_HANDLING_GUIDELINES.md`
