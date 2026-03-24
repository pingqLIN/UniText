# AI CLI Path Map

> 状态：Current Authoring Reference
> 注意：本文件记录这个 repo 目前的实际 deployment mapping，用来辅助验证与审查；规格真相仍以 `registry/` 与 `local/scripts/` 的相对路径逻辑为准。

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
  - skills target 应指向 `registry\skills`
  - project-level MCP 由 `local/scripts/bootstrap.py` 产生

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP setting location: `%USERPROFILE%\.gemini\settings.json` 的 `mcpServers`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP setting location: `[mcp_servers.unitext_registry]`
- Notes:
  - skills 与 MCP wiring 都由 `local/scripts/bootstrap.py` 写入
  - 不再使用旧的 `C:\Dev\UniText\skills` 路径

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: CLI internal state
- Codex: 无 standalone workflow directory setting

## Verification

- repo baseline: `local/scripts/health-check.ps1`
- delivery paths: `local/scripts/verify-delivery.ps1`
- first-run bootstrap: `local/scripts/verify-bootstrap.py`
