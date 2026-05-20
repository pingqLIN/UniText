---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/mode-cli-mcp.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/mode-cli-mcp.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/mode-cli-mcp.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/mode-cli-mcp.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/mode-cli-mcp.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Mode: External CLI Or MCP Audit

Use this mode when the reviewer is exposed through a stable CLI or MCP interface.

## Why this mode

- more automatable than web review
- easier to archive raw request and response
- compatible with local wrappers and CI-style flows

## Procedure

1. build the audit packet
2. send it to the CLI or MCP tool in read-only mode
3. capture raw stdout or transcript
4. normalize the result into the standard report format

## Guardrails

- require deterministic input shape
- keep the reviewer read-only unless the user asked for auto-fix
- capture the exact command or MCP tool name in the report notes
- if the reviewer depends on another project wrapper, list that wrapper in `Reference Inputs`

## Good fit

- CodeRabbit CLI
- provider-specific CLI reviewers
- local MCP server wrapping a reviewer model

## Bad fit

- unstable interactive TUI without transcript capture
- hidden browser automation when the user expects visible review
