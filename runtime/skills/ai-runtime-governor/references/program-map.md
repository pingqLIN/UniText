---
runtime_projection: true
source_of_truth: registry/skills/ai-runtime-governor/references/program-map.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/ai-runtime-governor/references/program-map.md`
> Source of truth: `registry/skills/ai-runtime-governor/references/program-map.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Program Map

## Canonical Shared Roots

- `C:\Dev\AI_UNIFIED\skills`
- `C:\Dev\AI_UNIFIED\mcp`
- `C:\Dev\AI_UNIFIED\workflow`
- `C:\Dev\AI_UNIFIED\ops`

## Codex CLI

- Binary: `codex`
- User config: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path` in `config.toml`
- MCP setting: `[mcp_servers.*]` in `config.toml`
- Update channel: npm package / release binary

## Claude Code

- Binary: `claude`
- User settings: `%USERPROFILE%\.claude\settings.json`
- Runtime metadata: `%USERPROFILE%\.claude.json`
- Skills paths: `%USERPROFILE%\.claude\skills`, `<project>\.claude\skills`
- MCP: `%USERPROFILE%\.claude.json` and `<project>\.mcp.json`
- Workflow/plans: `%USERPROFILE%\.claude\plans` or `plansDirectory` setting
- Update channel: native updater + `autoUpdatesChannel`

## Gemini CLI

- Binary: `gemini`
- User settings: `%USERPROFILE%\.gemini\settings.json`
- Workspace settings: `<project>\.gemini\settings.json`
- Skills paths: `%USERPROFILE%\.gemini\skills`, `%USERPROFILE%\.agents\skills`, project variants
- MCP settings: `mcpServers` in settings
- MCP OAuth token store: `%USERPROFILE%\.gemini\mcp-oauth-tokens.json`
- Workflow temp/plans: `%USERPROFILE%\.gemini\tmp\...`
- Update channel: npm package

## GitHub CLI

- Binary: `gh`
- Config: `%APPDATA%\GitHub CLI\config.yml`, `hosts.yml`
- Workflow concept: repo `.github\workflows\*.yml`
- No native skills/mcp system

## IDE Layer

- VS Code settings: `%APPDATA%\Code\User\settings.json`
- Windsurf settings location varies by install; detect dynamically
- Common AI extensions may carry separate skill/mcp path settings

## Local Model Runtime Signals

- `ollama` command and `%USERPROFILE%\.ollama`
- Hugging Face cache: `%USERPROFILE%\.cache\huggingface`
- Python/Node runtime presence for local model orchestration scripts
