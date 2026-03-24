# CLI Compatibility Matrix

> Stato: Working Draft
> Ultimo aggiornamento: 2026-03-23

| CLI | Base version | Comportamento dipendente da UniText | Stato attuale | Ultima verifica |
|---|---|---|---|---|
| Claude Code | 2.1.63 | legge `~/.claude/skills`, supporta `.mcp.json` di progetto | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | legge le skills da `skills_path` in `config.toml` e può registrare `[mcp_servers.unitext_registry]` | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | legge `~/.gemini/skills` e `~/.agents/skills` | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | il workflow è solo di riferimento, non esiste supporto nativo alle skills | known limitation | 2026-03-02 |
| VS Code | 1.109.5 | non è un consumer diretto delle risorse; è soprattutto ambiente di authoring | known limitation | 2026-03-02 |
| Windsurf | 1.108.2 | non è un consumer diretto delle risorse; è soprattutto ambiente di authoring | known limitation | 2026-03-02 |

## Note

- questa matrice registra il comportamento attuale dei CLI di cui UniText dipende, non tutte le loro capacità
- dopo ogni major version change, è opportuno verificare di nuovo skills e delivery MCP
- `delivery path verified` significa che `verify-delivery.ps1` ha confermato l’allineamento del canonical skills path, non che sia stata completata una verifica interattiva end-to-end

