# Matrice de compatibilité CLI

> Statut : `Working Draft`
> Dernière mise à jour : 2026-03-23

| CLI | Référence de version | Comportement requis par UniText | Statut actuel | Dernière vérification |
|---|---|---|---|---|
| Claude Code | 2.1.63 | Lit `~/.claude/skills` et prend en charge un `.mcp.json` de projet | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | Lit les skills depuis `skills_path` dans `config.toml` et peut enregistrer `[mcp_servers.unitext_registry]` | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | Lit `~/.gemini/skills` et `~/.agents/skills` | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | Le workflow n’est qu’une référence ; pas de prise en charge native des skills | limite connue | 2026-03-02 |
| VS Code | 1.109.5 | Pas un consommateur direct de ressources ; sert surtout d’environnement d’authoring | limite connue | 2026-03-02 |
| Windsurf | 1.108.2 | Pas un consommateur direct de ressources ; sert surtout d’environnement d’authoring | limite connue | 2026-03-02 |

## Notes

- Cette matrice documente le comportement CLI sur lequel UniText s’appuie aujourd’hui, pas l’ensemble des capacités de chaque CLI.
- Après chaque changement de version majeure, il faut au minimum revérifier les deliverys des skills et du MCP.
- `delivery path verified` signifie que `verify-delivery.ps1` a confirmé l’alignement du chemin canonique des skills ; cela ne veut pas dire qu’une interaction complète de bout en bout a déjà été validée.

