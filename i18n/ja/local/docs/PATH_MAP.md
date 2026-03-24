# AI CLI Path Map

> 状態：Current Authoring Reference
> 注意：この文書は、この repo における現在の実際の deployment mapping を記録し、検証と審査を補助するためのものです。規格上の真相は、引き続き `registry/` と `local/scripts/` の相対 path 論理に従います。

## Canonical Sources

- Skills: `Q:\UniText\registry\skills`
- MCP: `Q:\UniText\registry\mcp`
- Agents: `Q:\UniText\registry\agents`
- Workflow: `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills: `%USERPROFILE%\.claude\skills`
- Project MCP: `<repo>\.mcp.json`
- Notes:
  - skills target は `registry\skills` を指すべき
  - project-level MCP は `local/scripts/bootstrap.py` で生成する

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP setting location: `%USERPROFILE%\.gemini\settings.json` の `mcpServers`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP setting location: `[mcp_servers.unitext_registry]`
- Notes:
  - skills と MCP の wiring はどちらも `local/scripts/bootstrap.py` が書き込む
  - 旧い `C:\Dev\UniText\skills` path はもう使わない

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: CLI internal state
- Codex: standalone workflow directory setting はない

## Verification

- repo baseline: `local/scripts/health-check.ps1`
- delivery paths: `local/scripts/verify-delivery.ps1`
- first-run bootstrap: `local/scripts/verify-bootstrap.py`
