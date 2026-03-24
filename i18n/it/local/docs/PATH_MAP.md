# AI CLI Path Map

> Stato: Current Authoring Reference
> Nota: questo file documenta il mapping di deployment reale di questo repo, utile per verifica e review; la verità di specifica resta nei path logici di `registry/` e `local/scripts/`.

## Canonical Sources

- Skills: `Q:\UniText\registry\skills`
- MCP: `Q:\UniText\registry\mcp`
- Agents: `Q:\UniText\registry\agents`
- Workflow: `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills: `%USERPROFILE%\.claude\skills`
- Project MCP: `<repo>\.mcp.json`
- Note:
  - il target delle skills dovrebbe puntare a `registry\skills`
  - il MCP a livello progetto è generato da `local/scripts/bootstrap.py`

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP setting location: `mcpServers` in `%USERPROFILE%\.gemini\settings.json`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP setting location: `[mcp_servers.unitext_registry]`
- Note:
  - il wiring di skills e MCP viene scritto da `local/scripts/bootstrap.py`
  - non si usa più il vecchio path `C:\Dev\UniText\skills`

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: stato interno della CLI
- Codex: nessuna directory workflow autonoma

## Verification

- baseline del repo: `local/scripts/health-check.ps1`
- delivery paths: `local/scripts/verify-delivery.ps1`
- first-run bootstrap: `local/scripts/verify-bootstrap.py`

