---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/report-format.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/report-format.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/report-format.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
﻿---
---

# Report Format

Every completed or failed reviewer attempt should be normalized into this report structure.

## Audit Report

### Audit Mode

State one:

- same-provider-subagent
- external-web
- external-cli-mcp
- gemini-cli
- codex-exec
- tb2-template

### Audit Gate

State one classification:

- passed
- failed
- partial
- unavailable

Then record:

- reviewer_id
- command_or_route
- raw_review
- raw_stdout
- raw_stderr
- exit_code_or_timeout
- unavailable_reason
- substantive_findings_captured

Use `passed` only when raw reviewer output exists and contains findings or an explicit no-findings verdict. Template-only output, acknowledgement-only output, timeout, unavailable CLI/API, or lifecycle state without raw output must not be marked `passed`.

### Scope

State the reviewed scope exactly.

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

Use `accept` only when `Audit Gate` is `passed`.

### Next Action

One short paragraph with the exact next operational step.
