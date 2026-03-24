# Mapa de Rutas para AI CLI

> Estado: referencia actual de authoring
> Nota: este archivo registra el mapeo real de despliegue de este repo para ayudar en verificación y revisión; la verdad de la spec sigue estando en la lógica de rutas relativas de `registry/` y `local/scripts/`.

## Fuentes Canónicas

- Skills: `Q:\UniText\registry\skills`
- MCP: `Q:\UniText\registry\mcp`
- Agents: `Q:\UniText\registry\agents`
- Workflow: `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills: `%USERPROFILE%\.claude\skills`
- MCP del proyecto: `<repo>\.mcp.json`
- Notes:
  - el target de skills debe apuntar a `registry\skills`
  - el MCP a nivel de proyecto lo genera `local/scripts/bootstrap.py`

### Gemini CLI

- Skills: `%USERPROFILE%\.gemini\skills`
- Secondary skills mirror: `%USERPROFILE%\.agents\skills`
- ubicación de settings MCP: `mcpServers` dentro de `%USERPROFILE%\.gemini\settings.json`

### Codex

- archivo de config: `%USERPROFILE%\.codex\config.toml`
- ajuste de skills: `skills_path = "Q:\\UniText\\registry\\skills"`
- ubicación de settings MCP: `[mcp_servers.unitext_registry]`
- Notes:
  - el wiring de skills y MCP lo escribe `local/scripts/bootstrap.py`
  - ya no se usa la ruta antigua `C:\Dev\UniText\skills`

### Workflow Notes

- fuente del workflow de Claude: `registry\workflow\claude-plans`
- estado temporal del workflow de Gemini: estado interno de la CLI
- Codex: no tiene un directorio standalone para workflow

## Verification

- baseline del repo: `local/scripts/health-check.ps1`
- rutas de delivery: `local/scripts/verify-delivery.ps1`
- bootstrap first-run: `local/scripts/verify-bootstrap.py`
