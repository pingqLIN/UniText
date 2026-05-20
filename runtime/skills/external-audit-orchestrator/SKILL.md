---
name: external-audit-orchestrator
description: Standardize development-time external audit workflows. Use when a project requires another agent or external AI service to audit changes before acceptance, or when the user wants a fixed procedure for preparing audit packets, routing reviews to Claude/Codex/web/CLI/TB2 paths, and preserving explicit source attribution for cross-project references.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/SKILL.md`
> Source of truth: `registry/skills/external-audit-orchestrator/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# External Audit Orchestrator

Use this skill to turn ad hoc external review into a repeatable procedure.

Package version: `0.1.4`

Release checklist: `references/release-checklist.md`

This skill is for orchestration, not for doing the code review itself. Its job is to:

- choose the right audit mode
- prepare a consistent audit packet
- route the packet to a reviewer path
- require explicit source attribution when other projects or obvious references are used
- normalize findings into one report shape

## Required rules

1. If you used another local project, external repository, official documentation, article, or obvious reference to shape the audit or recommendation, record it in `Reference Inputs`.
2. For local cross-project references, include the exact path and the reason it was consulted.
3. For web references, include the URL and why it mattered.
4. Do not present external or cross-project conclusions as if they came from the current project alone.

Read [references/reference-sources.md](references/reference-sources.md) if you need the current baseline source inventory for this skill package.
Read [references/source-attribution-policy.md](references/source-attribution-policy.md) before producing any final audit report.
Read [references/install-claude-same-provider.md](references/install-claude-same-provider.md) when the chosen mode is Claude Code same-provider audit.
Read [references/install-tb2-template.md](references/install-tb2-template.md) when the chosen mode is TB2 template export.
Read [references/mode-codex-exec.md](references/mode-codex-exec.md) when the chosen mode is Codex non-interactive audit.

## Audit modes

Choose one mode only unless the user explicitly wants comparison across multiple reviewers.

- Same-provider parallel or subagent audit:
  Use [references/mode-same-provider.md](references/mode-same-provider.md)
- External web audit:
  Use [references/mode-web-manual.md](references/mode-web-manual.md)
- External CLI or MCP audit:
  Use [references/mode-cli-mcp.md](references/mode-cli-mcp.md)
- Codex non-interactive audit:
  Use [references/mode-codex-exec.md](references/mode-codex-exec.md)
- TB2 audit template:
  Use [references/mode-tb2.md](references/mode-tb2.md)

## Core workflow

1. Determine scope.
   - `working-tree`
   - `staged`
   - `commit-range`
   - `path`
   - `manual-question`

2. Build the audit packet.
   - Use `scripts/build-audit-packet.ps1`
   - Follow the shape in [references/audit-packet-format.md](references/audit-packet-format.md)
   - Prefer [scripts/run-external-audit-flow.ps1](scripts/run-external-audit-flow.ps1) when you want one entrypoint for packet build plus mode-specific export

3. Choose the review path.
   - Same-provider if the user wants the most stable v0.1 path
   - Codex exec if the reviewer should be Codex in a scripted or CI-style workflow
   - Web if the user wants visible human-supervised review
   - CLI/MCP if the user already has an external toolchain
   - TB2 if the goal is traceable external process orchestration

4. Run the audit as read-only unless the user explicitly asked for auto-fix.

5. Normalize the result into one report.
   - Use the required output contract in [references/report-format.md](references/report-format.md)
   - Prefer [scripts/normalize-audit-report.ps1](scripts/normalize-audit-report.ps1) when converting raw reviewer output into the standard report shape
   - Always include `Reference Inputs`

6. Decide next action.
   - `accept`
   - `fix-and-rerun`
   - `escalate-to-human`
   - `archive-only`

## Assets

- Claude reviewer subagent template:
  [assets/claude/code-reviewer.md](assets/claude/code-reviewer.md)
- Claude hook config example:
  [assets/claude/settings.audit.json](assets/claude/settings.audit.json)
- Audit report template:
  [assets/report/external-audit-report.template.md](assets/report/external-audit-report.template.md)
- Codex exec audit report schema:
  [assets/codex/audit-report.schema.json](assets/codex/audit-report.schema.json)
- Web prompt template:
  [assets/web/external-audit-request.md](assets/web/external-audit-request.md)
- TB2 request template:
  [assets/tb2/tb2-audit-request.template.json](assets/tb2/tb2-audit-request.template.json)

## Script

- Packet builder:
  [scripts/build-audit-packet.ps1](scripts/build-audit-packet.ps1)
- TB2 execution evidence adapter:
  [scripts/convert-tb2-execution-evidence.ps1](scripts/convert-tb2-execution-evidence.ps1)
- Claude bundle exporter:
  [scripts/export-claude-reviewer-bundle.ps1](scripts/export-claude-reviewer-bundle.ps1)
- Audit report normalizer:
  [scripts/normalize-audit-report.ps1](scripts/normalize-audit-report.ps1)
- Codex exec request exporter:
  [scripts/export-codex-exec-request.ps1](scripts/export-codex-exec-request.ps1)
- TB2 request exporter:
  [scripts/export-tb2-audit-request.ps1](scripts/export-tb2-audit-request.ps1)
- Unified flow runner:
  [scripts/run-external-audit-flow.ps1](scripts/run-external-audit-flow.ps1)

## v0.1 guardrails

- Prefer same-provider or web-manual mode first.
- Prefer `codex-exec` over TB2 `codex` when the reviewer should be Codex and the operator wants non-interactive automation.
- Treat TB2 `claude` and `codex` profiles as reusable templates, not fully proven production reviewers, until the user validates those profiles in their real runtime.
- Do not hide source provenance. If another project materially influenced the audit, cite it every time.
