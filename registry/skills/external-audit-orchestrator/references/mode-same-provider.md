---
---

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
4. ask for severity-ordered findings
5. require findings or an explicit no-findings verdict in the first response

Use a narrow first prompt: name the exact files or scope, forbid edits, and request the normalized audit report. If the reviewer returns only acknowledgement text, lifecycle state, or a request for confirmation, classify the gate as failed and switch lanes.

## Suggested operating shape

1. main agent implements change
2. reviewer agent receives packet
3. reviewer returns severity-ordered findings
4. main agent fixes or rejects findings
5. rerun reviewer if any warning-or-higher issue was addressed

## Failure handling

Same-provider subagents can appear to complete while only acknowledging AGENTS/runtime instructions. That is not approval. Apply [reviewer-gate-failures.md](reviewer-gate-failures.md) before using `accept`.

## Attribution note

This mode design is based on official vendor docs for Codex and Claude Code. Cite those docs if they materially shaped the chosen workflow.
