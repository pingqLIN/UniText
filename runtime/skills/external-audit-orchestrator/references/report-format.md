---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/report-format.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/report-format.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/report-format.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Report Format

Every completed audit should be normalized into this report structure.

Reviewer output should be JSON-first when the reviewer path supports it. Markdown reviewer output remains a fallback for manual or legacy paths.

## Audit Report

### Audit Mode

State one:

- same-provider-subagent
- external-web
- external-cli-mcp
- tb2-template

### Scope

State the reviewed scope exactly.

### Reviewer Status

For multi-reviewer runs, list each reviewer:

- reviewer id
- role
- status
- request id when available
- result path when available

### Reference Inputs

List only the sources actually used.

### Findings

Order by severity:

1. Critical
2. Warning
3. Suggestion

Each finding should contain:

- title
- severity
- location or scope
- risk
- recommended action

### Assumptions

List open assumptions that affected the review.

### Disposition

State one:

- accept
- fix-and-rerun
- escalate-to-human
- archive-only

### Next Action

One short paragraph with the exact next operational step.
