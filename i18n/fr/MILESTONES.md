# UniText — Jalons

> Statut : `Active`
> Objectif : définir des critères de complétion quantifiables, communs à la revue externe et à l’exécution interne.

## Phase 1 — Skills Registry Online

- `registry/skills/` existe
- au moins 5 skills ont terminé l’adoption canonique
- `INDEX.md` contient les entrées de catalogue correspondantes
- `local/scripts/sync-skills.ps1` pointe vers `registry/skills`
- `local/scripts/verify-delivery.ps1` peut vérifier l’état source et cible des skills
- `local/scripts/health-check.ps1` passe les vérifications de base

## Phase 2 — Full Registry Baseline

- `registry/agents/` existe
- `registry/mcp/` contient au moins un exemple non vide et lisible
- `registry/workflow/` contient au moins une entrée de catalogue listée officiellement
- les opérations `scan` / `verify` / `sync` disposent toutes d’un support minimal
- `CLI_COMPAT_MATRIX.md` documente les comportements CLI dépendants et la dernière date de validation

## Phase 3 — External Review Ready

- le dépôt Git est initialisé
- `.gitignore` exclut les artefacts locaux et les gros historiques
- `README.md`, `INDEX.md`, `PROJECT_STATUS_REPORT_2026-03-23.md` sont alignés
- `EXTERNAL_REVIEW_PACKAGE.md` définit le périmètre, l’ordre de lecture et les éléments exclus
- `EXTERNAL_REVIEW_COVER_NOTE.md` et `EXTERNAL_REVIEW_HIGHLIGHTS.md` sont prêts comme documents d’entrée pour les relecteurs
- `SECRET_HANDLING_GUIDELINES.md` est en place et intégré à l’ordre de lecture principal
- `local/scripts/export-review-package.ps1` peut produire un review package de manière reproductible
- un chemin `bootstrap -> verify` multiplateforme pour le premier lancement est disponible
- la revue externe peut voir directement :
  - les documents centraux
  - les skills canoniques déjà adoptés
  - les scripts d’opérations minimaux
  - les jalons clairs de la phase suivante

## Phase 4 — Template Release Ready

- les artefacts locaux ne sont pas inclus dans le package de publication
- le flux d’export du template est documenté
- `TEMPLATE_RELEASE_PACKAGE.md` et `TEMPLATE_RELEASE_CHECKLIST.md` existent
- `local/scripts/export-template-package.ps1` peut produire un starter package de façon reproductible
- `local/scripts/verify-template-package.ps1` peut vérifier la structure du starter package
- `SECRET_HANDLING_GUIDELINES.md` est inclus dans le starter package
- `local/scripts/create-git-bundle.py` peut produire un artefact de backup portable
- il existe des exemples génériques `template-safe` pour `skills`, `mcp`, `agents`, `workflow`
- il existe un `local/` skeleton `template-safe`
- `mcp` dispose d’au moins une base réellement exécutable
- la couverture des shared resources continue de s’étendre à `skills`, `mcp`, `agents`, `workflow`
- au moins 2 CLI ont validé la delivery de manière réelle

