---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/mode-same-provider.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/mode-same-provider.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/mode-same-provider.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Mode: Same-Provider Parallel Or Subagent Audit

Use this mode when the main development agent and the reviewer live in the same provider family.

This is the preferred `v0.1` path.

## Why this mode

- lowest packaging friction
- easiest to standardize
- easiest to keep read-only
- easiest to rerun after fixes

## Typical variants

### Claude Code

- create a project subagent in `.claude/agents/`
- make it read-only
- optionally add a `SubagentStop` or `PreToolUse` gate in `.claude/settings.json`
- install with dry-run first using [install-claude-same-provider.md](install-claude-same-provider.md)

Template assets in this skill:

- [../assets/claude/code-reviewer.md](../assets/claude/code-reviewer.md)
- [../assets/claude/settings.audit.json](../assets/claude/settings.audit.json)
- [../scripts/export-claude-reviewer-bundle.ps1](../scripts/export-claude-reviewer-bundle.ps1)

### Codex

- run a parallel task or subagent-style reviewer flow
- keep the reviewer focused on changed files or the named path
- do not mix review and auto-fix in the same first pass

## Required packet discipline

Before invoking the reviewer:

1. build the audit packet
2. include `Reference Inputs`
3. explicitly request read-only review
4. ask for JSON-first reviewer output
5. treat invalid JSON as an invalid or partial review, not a successful audit

## Suggested operating shape

1. main agent implements change
2. reviewer agent receives packet
3. reviewer returns the expected reviewer result JSON
4. main agent fixes or rejects findings
5. rerun reviewer if any warning-or-higher issue was addressed

## Expected reviewer result

The reviewer should return a JSON object with:

- `reviewer_id`
- `verdict`
- `findings`
- `assumptions`
- `reference_inputs_used`
- `confidence`
- `requires_rerun`

Use Markdown only for human-readable summaries inside JSON string fields. If the reviewer cannot complete the review, record the failure outside the reviewer result as a wrapper with `status` set to `timeout`, `invalid`, or `failed`.

## Attribution note

This mode design is based on official vendor docs for Codex and Claude Code. Cite those docs if they materially shaped the chosen workflow.
