# AI CLI Path Map (2026-02-28)

> 狀態：Legacy Reference
> 注意：本文件描述的是某一組既有部署的路徑對照，不是 `UniText` 的跨平台規格真相。邏輯契約請以 `VISION.md`、`RESOURCE_SPEC.md`、`OPERATIONS.md` 為準。

## Unified Targets
- Skills: `C:\Dev\UniText\skills`
- MCP: `C:\Dev\UniText\mcp`
- Workflow: `C:\Dev\UniText\workflow`

## Codex
- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "C:\\Dev\\UniText\\skills"`
- MCP setting location: `[mcp_servers.*]` in `%USERPROFILE%\.codex\config.toml`
- Workflow path setting: not found as standalone setting

## Gemini CLI
- Global settings: `%USERPROFILE%\.gemini\settings.json`
- Workspace settings: `<project>\.gemini\settings.json`
- Skills discovery (official docs/source):
  - `%USERPROFILE%\.gemini\skills`
  - `%USERPROFILE%\.agents\skills`
  - `<project>\.gemini\skills`
  - `<project>\.agents\skills`
- MCP setting location: `mcpServers` in settings JSON
- MCP OAuth token file: `%USERPROFILE%\.gemini\mcp-oauth-tokens.json`
- Workflow temp/plans: internal `.gemini/tmp/...` (managed by CLI)

## Claude Code
- User runtime dir: `%USERPROFILE%\.claude`
- User meta config: `%USERPROFILE%\.claude.json`
- Session settings: `%USERPROFILE%\.claude\settings.json`
- Skills path (supported by product behavior/changelog): `%USERPROFILE%\.claude\skills` and project `.claude/skills`
- MCP config:
  - user/project state in `%USERPROFILE%\.claude.json`
  - project file `.mcp.json` (created at `C:\Dev\.mcp.json`)
- Workflow/plans path:
  - `plansDirectory` set to `C:\Dev\UniText\workflow\claude-plans`

## GitHub CLI (`gh`)
- Config files: `%APPDATA%\GitHub CLI\config.yml`, `hosts.yml`
- MCP: not native
- Skills: not native
- Workflow path (GitHub Actions): `<repo>\.github\workflows\*.yml`

## Applied Changes
- Updated `%USERPROFILE%\.codex\config.toml` skills path
- Updated `%USERPROFILE%\.claude\settings.json` with `plansDirectory`
- Created canonical folders under `C:\Dev\UniText`
- Created `C:\Dev\UniText\local\scripts\sync-skills.ps1` to mirror skills to:
  - `%USERPROFILE%\.claude\skills`
  - `%USERPROFILE%\.gemini\skills`
  - `%USERPROFILE%\.agents\skills`
- Created MCP canonical seed file: `C:\Dev\UniText\mcp\claude.mcp.json`
- Mirrored project MCP file: `C:\Dev\.mcp.json`

## Backups
- `C:\Dev\UniText\backup\20260228_185716\`
