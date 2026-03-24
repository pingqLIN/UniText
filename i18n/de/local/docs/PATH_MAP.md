# AI CLI Path Map

> Status: Current Authoring Reference
> Hinweis: Dieses Dokument beschreibt das aktuelle Deployment-Mapping dieses Repos und dient der Verifikation und dem Review. Die eigentliche Spezifikation bleibt die logische Pfadlogik in `registry/` und `local/scripts/`.

## Canonical Sources

- Skills: `Q:\UniText\registry\skills`
- MCP: `Q:\UniText\registry\mcp`
- Agents: `Q:\UniText\registry\agents`
- Workflow: `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills: `%USERPROFILE%\.claude\skills`
- Project MCP: `<repo>\.mcp.json`
- Hinweise:
  - das Skills-Ziel soll auf `registry\skills` zeigen
  - das projektweite MCP wird von `local/scripts/bootstrap.py` erzeugt

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- MCP location: `mcpServers` in `%USERPROFILE%\.gemini\settings.json`

### Codex

- Config file: `%USERPROFILE%\.codex\config.toml`
- Skills setting: `skills_path = "Q:\\UniText\\registry\\skills"`
- MCP location: `[mcp_servers.unitext_registry]`
- Hinweise:
  - sowohl Skills- als auch MCP-Wiring werden von `local/scripts/bootstrap.py` geschrieben
  - der alte Pfad `C:\Dev\UniText\skills` wird nicht mehr verwendet

### Workflow Notes

- Claude workflow source: `registry\workflow\claude-plans`
- Gemini workflow temp state: interner CLI-Status
- Codex: kein eigenständiges Workflow-Verzeichnis als Setting

## Verification

- Repo-Baseline: `local/scripts/health-check.ps1`
- Delivery paths: `local/scripts/verify-delivery.ps1`
- First-Run-Bootstrap: `local/scripts/verify-bootstrap.py`
