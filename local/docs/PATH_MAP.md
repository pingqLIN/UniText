# AI CLI Path Map (Archived 2026-02-28)

> 狀態：Archived Legacy Reference
> 注意：本文件描述的是舊部署對照，不是 `UniText` 的現行 canonical path 真相。現行 skills source 以 repo 內 `registry/skills/` 與 `local/scripts/` 的相對路徑邏輯為準。

## Unified Targets
- Skills: `C:\Dev\UniText\skills`（舊）
- MCP: `C:\Dev\UniText\mcp`
- Workflow: `C:\Dev\UniText\workflow`

## Current Direction

- 現行 canonical skills source：`registry/skills/`
- 現行 delivery 驗證目標：使用者家目錄下 `.claude/skills`、`.gemini/skills`、`.agents/skills`
- 歷史 `C:\Dev\UniText\skills` 路徑應視為 pre-registry 版本

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
