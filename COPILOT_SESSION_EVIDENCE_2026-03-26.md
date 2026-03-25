# Copilot Session Evidence 2026-03-26

## Scope

This note captures a repeatable non-interactive `copilot` verification run from the repo root using:

```bash
python3 local/scripts/verify-copilot-session.py --use-project-mcp
```

The goal is to separate three questions:

1. Can `copilot` run a non-interactive session in this repo?
2. Does it load the repo instructions surface?
3. Does the project MCP attach path succeed during that session?

## Observed Result

- `copilot` binary: present
- non-interactive prompt: succeeded
- final JSON payload: parsed successfully
- repo instructions surface: effectively used
- project MCP attach (`unitext-registry`): failed with timeout

## Verified Evidence

The final assistant payload reported:

```json
{
  "registry_roots": [
    "/registry/skills",
    "/registry/mcp",
    "/registry/agents",
    "/registry/workflow"
  ],
  "copilot_status": "bootstrap-verified personal config + repo instructions",
  "catalog_exclusions_path": "registry/catalog-exclusions.json"
}
```

This confirms that the Copilot session can read the canonical repo guidance and return the expected high-level UniText shape.

## Runtime Gap

During the same run, the MCP status summary reported:

- `unitext-registry`: `failed`
- error: `MCP error -32001: Request timed out`

That means the current status should remain:

`bootstrap baseline verified; broader runtime validation pending`

## Boundary Interpretation

- The Copilot CLI binary works in this environment.
- The repository instructions path is usable.
- The read-only UniText MCP server itself is not dead; separate manual MCP initialize smoke still succeeds locally.
- The unresolved gap is specifically the Copilot session path for project MCP attachment, not the existence of the server process or the bootstrap file surfaces alone.

## Recommended Next Step

Treat `local/scripts/verify-copilot-session.py` as the repeatable evidence collector for this boundary.

Only promote Copilot beyond bootstrap verification after `unitext-registry` stops timing out during the session-level attach path.
