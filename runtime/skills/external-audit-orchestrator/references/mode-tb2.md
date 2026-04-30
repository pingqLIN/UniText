---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/mode-tb2.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/mode-tb2.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/mode-tb2.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Mode: TB2 Audit Template

Use this mode when you want an external reviewer path that is session-based, traceable, and reusable across providers.

## Cross-project reference

This mode explicitly reuses ideas from:

- `Q:\Projects\tb2-claude-subagent-workflow\README.md`
- `Q:\Projects\tb2-claude-subagent-workflow\docs\platform-baseline-matrix.md`

If this mode is selected, cite those paths in the final audit report.

## Current maturity note

The referenced TB2 project currently documents:

- built-in profiles for `claude`, `codex`, `copilot`, and `python-repl`
- `codex_relay`
- validated runtime baseline for core runtime flows

But the same project also records that:

- `python-repl` has real interactive validation
- `claude`, `codex`, and `copilot` are currently `metadata-only`

So treat TB2 `claude` and `codex` reviewer flows as templates until the user validates them in their own runtime.

## Procedure

1. build the audit packet
2. adapt it into the TB2 request JSON
3. route through `connect/send/read/disconnect` or higher-level relay shape
4. preserve transcript output
5. normalize transcript findings into the standard report format

## Recommended asset

Use [../assets/tb2/tb2-audit-request.template.json](../assets/tb2/tb2-audit-request.template.json) as the starting request shape.
Use [install-tb2-template.md](install-tb2-template.md) for the dry-run export path.
Use [../scripts/export-tb2-audit-request.ps1](../scripts/export-tb2-audit-request.ps1) to materialize the request into a target project.

## Good fit

- cross-provider experiments
- traceable long-running reviewer session
- future audit template library work

## Not preferred for v0.1

Do not make this the default v0.1 execution path until real reviewer profile validation exists for the intended provider CLI.
