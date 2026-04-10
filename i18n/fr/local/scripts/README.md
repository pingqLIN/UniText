# Local Scripts

Ce dossier contient les **scripts d’exploitation locaux**.

- `*.ps1` reste l’implémentation de référence Windows-first
- `*.py` fournit le chemin cross-platform pour `bootstrap` / `verify` / `backup`

## Current Scripts

- `bootstrap.py`
  - initialise de façon cross-platform le skills delivery, la configuration native de Codex, la configuration MCP de Copilot et le fichier `.mcp.json` du projet
- `verify-bootstrap.py`
  - vérifie de façon cross-platform que le résultat du first-run correspond au repo actuel, et accepte à la fois le seed template-safe de `.mcp.json` et un wiring local déjà bootstrappé
- `create-git-bundle.py`
  - crée une sauvegarde `git bundle` portable afin de réduire le risque de point de défaillance unique d’un worktree purement local
- `git-startup.ps1`
  - résout le canonical base branch pour une nouvelle session, impose un worktree propre, effectue un fast-forward explicite et crée une nouvelle feature branch
- `sync-skills.ps1`
  - synchronise `registry/skills/` vers les skills targets locaux
- `scan-skills.ps1`
  - scanne les skills candidates et produit le résultat du contrôle d’adoption
- `verify-delivery.ps1`
  - vérifie si la source et les skills targets courants existent, sont des liens et peuvent être résolus
- `health-check.ps1`
  - effectue une vérification minimale de santé sur le registry et les scripts
- `batch-adopt-skills.ps1`
  - déplace par lot les skills candidates vers `registry/skills/`
- `generate-index-entries.ps1`
  - génère à partir de `registry/skills/` le bloc de catalogue nécessaire à `INDEX`
- `rollback-skills.ps1`
  - restaure un skill donné à partir des sauvegardes `ops/history/adopt_*`
- `export-review-package.ps1`
  - exporte vers `ops/review-package/` la cover note, les highlights, les documents de base, les entrées registry sélectionnées et les scripts minimaux nécessaires à une revue externe
- `export-template-package.ps1`
  - exporte vers `ops/template-package/` les docs template-safe, les generic examples et la starter layout
- `verify-template-package.ps1`
  - vérifie que le template package exporté contient bien la structure starter requise et n’inclut pas de contenu review-only ou local-only
- `verify-workspace-boundaries.ps1`
  - vérifie que les tracked shared surfaces du repo d’authoring actuel ne mélangent pas de live workspace metadata, d’authoring-only docs ou d’operations state
- `get-publishability-report.ps1`
  - agrège les changements local-only / ops / shared-surface de la branche actuelle avec le résultat du boundary verify pour produire un rapport local de push suitability
- `lib/workspace-sensitive-metadata.ps1`
  - charge le fichier partagé `WORKSPACE_SENSITIVE_METADATA_RULES.json` afin que les validations de boundary, de template et de publishability utilisent le même jeu de règles
- `validate-workspace-sensitive-metadata-rules.ps1`
  - valide la structure, la compilation des regex et les cas intégrés du fichier partagé `WORKSPACE_SENSITIVE_METADATA_RULES.json`
- `preview-renormalize.ps1`
  - exécute uniquement un dry-run pour prévisualiser combien de tracked files seraient touchés par `git add --renormalize .`, afin de voir d’abord le blast radius d’un nettoyage des line endings
- `run-renormalize.ps1`
  - exécute un renormalize contrôlé par scope `repo / root / registry / i18n / local / template` ; le mode par défaut reste le dry-run, seuls les appels explicites avec `-Apply` mettent les changements en stage, et un garde-fou `MaxFiles` limite la taille du lot
- `audit-i18n-drift.py`
  - lit `i18n/manifest.json`, liste pour chaque locale les documents officiels manquants, en retard ou non suivis par Git, et prend en charge `json / markdown`, le filtrage par `locale / source-doc`, ainsi que la sortie directe vers un workboard
- `export-rebuild-project.ps1`
  - reconstruit le repo actuel en fresh-project baseline pouvant être renommée et réinitialisée, puis l’exporte vers `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - confirme, en plus de la validation du template package, la présence du guide de rebuild et du point d’entrée fresh-project

## Governance Note

- `sync-skills.ps1` et `batch-adopt-skills.ps1` doivent tous deux respecter :
  - dry-run first
  - backup before mutation
  - production de logs traçables

## Platform Note

- Le nouveau chemin de first-run doit privilégier `bootstrap.py` et `verify-bootstrap.py`.
- `sync-skills.ps1` reste l’implémentation de référence Windows PowerShell et le modèle de gouvernance.
