# Local Path Map Template

> 狀態：Template Example

## Canonical Sources

- Skills: `/registry/skills`
- MCP: `/registry/mcp`
- Agents: `/registry/agents`
- Workflow: `/registry/workflow`

## Your Local Targets

- Claude Code: `<your-home>/.claude/skills`
- Gemini CLI: `<your-home>/.gemini/skills`
- Agents mirror: `<your-home>/.agents/skills`
- Codex config: `<your-home>/.codex/config.toml`
- Claude project MCP: `<repo>/.mcp.json`

## Notes

- 用你自己的家目錄與工作路徑取代 placeholder
- 不要把作者工作區的絕對路徑直接帶進正式專案
- 優先用 `local/scripts/bootstrap.py` 產生 machine-local path mapping
