# CLI Compatibility Matrix

> Status: Working Draft
> Letzte Aktualisierung: 2026-03-23

| CLI | Versionsbasis | Verhalten, auf das UniText angewiesen ist | Aktueller Status | Letzte Verifikation |
|---|---|---|---|---|
| Claude Code | 2.1.63 | liest `~/.claude/skills` und unterstützt project `.mcp.json` | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | liest Skills aus `skills_path` in `config.toml` und kann `[mcp_servers.unitext_registry]` registrieren | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | liest `~/.gemini/skills` und `~/.agents/skills` | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | Workflow nur als Referenz, keine native Skills-Unterstützung | bekannte Einschränkung | 2026-03-02 |
| VS Code | 1.109.5 | kein direkter Resource Consumer, hauptsächlich Authoring-Umgebung | bekannte Einschränkung | 2026-03-02 |
| Windsurf | 1.108.2 | kein direkter Resource Consumer, hauptsächlich Authoring-Umgebung | bekannte Einschränkung | 2026-03-02 |

## Hinweise

- Diese Matrix dokumentiert das CLI-Verhalten, auf das UniText aktuell angewiesen ist, nicht die vollständigen Fähigkeiten der CLIs.
- Nach jeder Major-Version sollte mindestens einmal erneut verifiziert werden, dass Skills- und MCP-Delivery noch funktionieren.
- `delivery path verified` bedeutet, dass `verify-delivery.ps1` die Übereinstimmung des kanonischen Skills-Pfads bestätigt hat; das ist nicht dasselbe wie eine vollständige End-to-End-Interaktionsprüfung.
