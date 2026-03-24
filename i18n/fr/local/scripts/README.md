# Scripts Locaux

Ce répertoire contient les **scripts d’opérations locales**.

- `*.ps1` conserve une implémentation de référence Windows-first
- `*.py` fournit les chemins multiplateformes de `bootstrap` / `verify` / `backup`

## Scripts actuels

- `bootstrap.py`
  - initialise de manière multiplateforme la delivery des skills, la configuration native Codex et le `.mcp.json` du projet
- `verify-bootstrap.py`
  - vérifie de façon multiplateforme que le premier run correspond bien au repo actuel
- `create-git-bundle.py`
  - crée un backup portable sous forme de `git bundle`, ce qui réduit le risque de dépendre d’un seul workspace local
- `sync-skills.ps1`
  - synchronise `registry/skills/` vers les cibles locales de skills
- `scan-skills.ps1`
  - scanne les skills candidats et produit les résultats de contrôle d’adoption
- `verify-delivery.ps1`
  - vérifie l’existence de la source et des cibles habituelles, le type de lien et la capacité de résolution
- `health-check.ps1`
  - effectue un contrôle de santé minimal sur le registry et les scripts
- `batch-adopt-skills.ps1`
  - déplace les skills candidats par lot vers `registry/skills/`
- `generate-index-entries.ps1`
  - génère les blocs de catalogue nécessaires pour INDEX à partir de `registry/skills/`
- `rollback-skills.ps1`
  - restaure un skill ciblé à partir du backup `ops/history/adopt_*`
- `export-review-package.ps1`
  - exporte vers `ops/review-package/` la note de couverture, les highlights, les documents centraux, les entrées de registry sélectionnées et les scripts minimaux nécessaires à la revue externe
- `export-template-package.ps1`
  - exporte vers `ops/template-package/` les docs `template-safe`, les exemples génériques et le starter layout
- `verify-template-package.ps1`
  - vérifie que le template package exporté contient la structure starter requise et qu’il ne contient ni contenu réservé à la revue ni éléments local-only

## Note de gouvernance

- `sync-skills.ps1` et `batch-adopt-skills.ps1` doivent tous deux respecter :
  - `dry-run` d’abord
  - backup avant mutation
  - journal traçable

## Note de plateforme

- pour le premier run, privilégier `bootstrap.py` et `verify-bootstrap.py`
- `sync-skills.ps1` reste l’implémentation de référence PowerShell Windows et un modèle de gouvernance

