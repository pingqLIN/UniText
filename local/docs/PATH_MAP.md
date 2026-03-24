# AI CLI Path Map

> 狀態：Current Authoring Reference
> 注意：本文件記錄這個 repo 目前的實際 deployment mapping，用來輔助驗證與審查；規格真相仍以 `registry/` 與 `local/scripts/` 的相對路徑邏輯為準。

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
  - skills target 應指向 `registry\skills`
  - project-level MCP 由 `local/scripts/bootstrap.py` 產生

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP setting location: `%USERPROFILE%\.gemini\settings.json` 的 `mcpServers`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP setting location: `[mcp_servers.unitext_registry]`
- Notes:
  - skills 與 MCP wiring 都由 `local/scripts/bootstrap.py` 寫入
  - 不再使用舊的 `C:\Dev\UniText\skills` 路徑

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: CLI internal state
- Codex: 無 standalone workflow directory setting

## Verification

- repo baseline: `local/scripts/health-check.ps1`
- delivery paths: `local/scripts/verify-delivery.ps1`
- first-run bootstrap: `local/scripts/verify-bootstrap.py`
