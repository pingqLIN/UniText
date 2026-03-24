# Carte des chemins AI CLI

> Statut : `Current Authoring Reference`
> Note : ce document enregistre le mappage de déploiement réel de ce repo pour aider la validation et la revue ; la vérité spec reste définie par la logique des chemins relatifs dans `registry/` et `local/scripts/`.

## Sources canoniques

- Skills : `Q:\UniText\registry\skills`
- MCP : `Q:\UniText\registry\mcp`
- Agents : `Q:\UniText\registry\agents`
- Workflow : `Q:\UniText\registry\workflow`

## Runtime Targets

### Claude Code

- Skills : `%USERPROFILE%\.claude\skills`
- Project MCP : `<repo>\.mcp.json`
- Notes :
  - la cible des skills doit pointer vers `registry\skills`
  - le MCP de niveau projet est généré par `local/scripts/bootstrap.py`

### Gemini CLI

- Skills : `%USERPROFILE%\.gemini\skills`
- Miroir secondaire des skills : `%USERPROFILE%\.agents\skills`
- Emplacement de la configuration MCP : `mcpServers` dans `%USERPROFILE%\.gemini\settings.json`

### Codex

- Fichier de configuration : `%USERPROFILE%\.codex\config.toml`
- Paramètre des skills : `skills_path = "Q:\\UniText\\registry\\skills"`
- Emplacement de la configuration MCP : `[mcp_servers.unitext_registry]`
- Notes :
  - le câblage des skills et du MCP est écrit par `local/scripts/bootstrap.py`
  - l’ancien chemin `C:\Dev\UniText\skills` n’est plus utilisé

### Workflow Notes

- source workflow Claude : `registry\workflow\claude-plans`
- état temporaire Gemini workflow : état interne du CLI
- Codex : aucun répertoire workflow autonome n’est configuré

## Vérification

- base du repo : `local/scripts/health-check.ps1`
- chemins de delivery : `local/scripts/verify-delivery.ps1`
- bootstrap first-run : `local/scripts/verify-bootstrap.py`

