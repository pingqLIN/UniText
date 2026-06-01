---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/reviewer-gate-failures.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/reviewer-gate-failures.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/reviewer-gate-failures.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Reviewer Gate Failure Handling

Use this reference when a reviewer run does not produce a complete, substantive review.

## Passing Gate Requirements

A reviewer gate passes only when all are true:

- raw reviewer output exists and is archived
- the output contains severity-ordered findings or an explicit no-findings verdict
- stdout and stderr, or the equivalent transcript, are captured when the reviewer is a CLI
- the normalized report records `Audit Gate` as `passed`

Do not treat lifecycle state, request artifacts, acknowledgements, or wrapper success as reviewer approval.

## Failure Classifications

- `failed`: the reviewer path ran but did not produce a usable review. Examples: acknowledgement-only response, `shutdown` without output, timeout, empty stdout/stderr, policy-blocked commands, or request-only artifacts.
- `partial`: the reviewer produced actionable findings, but the final normalization or final reviewer pass failed. Preserve useful findings, but do not claim a clean reviewer pass.
- `unavailable`: the reviewer path could not run because of authentication, quota, billing, permission, account, `ConnectionRefused`, or API availability problems.

## Required Failure Record

Record these fields whenever a gate is `failed`, `partial`, or `unavailable`:

- target repo, commit, and scope
- reviewer path and reviewer id
- command or routing method
- exit code, timeout, or unavailable reason
- raw stdout path
- raw stderr path
- whether substantive findings were captured
- final gate classification
- next action: retry same lane, switch lane, operator action, or archive-only

## Health Check

Before sending a full packet to a fragile reviewer path, run a tiny health check that must return a substantive sentinel, such as `AUDIT_OK`. The sentinel must not be only AGENTS/runtime acknowledgement text. If the health check fails, classify the lane as failed or unavailable before spending a full reviewer run.

## Retry Rule

If the first response is acknowledgement-only, timeout, shutdown, request-only, or lacks raw output, mark the gate failed and switch lanes instead of repeatedly nudging the same stalled reviewer. A follow-up prompt is not enough evidence unless it produces raw substantive output.

## Evidence Paths

Prefer ignored evidence paths:

- target-project evidence: `reports\` or `.audit\`
- package-local scratch: `validation\scratch\external-review-<timestamp>\`

Stderr noise is not a finding unless it blocks reviewer output. Keep stdout and stderr separate when possible.
