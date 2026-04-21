# Matriz de Compatibilidad de CLIs

> Estado: borrador de trabajo
> Última actualización: 2026-03-23

| CLI | Base de versión | Comportamiento del que depende UniText | Estado actual | Última verificación |
|---|---|---|---|---|
| Claude Code | 2.1.63 | lee `~/.claude/skills` y soporta `.mcp.json` del proyecto | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | lee skills desde `skills_path` en `config.toml` y puede registrar `[mcp_servers.unitext_registry]` | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | lee `~/.gemini/skills` y `~/.agents/skills` | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | workflow sólo como referencia, sin soporte nativo de skills | limitación conocida | 2026-03-02 |
| VS Code | 1.109.5 | no es consumidor directo de recursos; se usa sobre todo como authoring environment | limitación conocida | 2026-03-02 |
| Windsurf | 1.108.2 | no es consumidor directo de recursos; se usa sobre todo como authoring environment | limitación conocida | 2026-03-02 |

## Notes

- Esta matriz registra el comportamiento actual de las CLIs del que depende UniText, no la capacidad completa de cada CLI.
- Tras cualquier cambio de major version, debería volver a verificarse al menos una vez el delivery de skills y mcp.
- `delivery path verified` significa que `verify-delivery.ps1` ha confirmado el alineamiento de la ruta canónica de skills; no significa que se haya completado una verificación interactiva de extremo a extremo.
