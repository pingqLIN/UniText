# UniText — Package de revue externe

> Statut : `Active Baseline`
> Utilité : définir ce que la revue externe doit regarder, ce qu’elle ne doit pas regarder, et comment produire un review package de manière répétable.

## 1. Objectif

`UniText` est déjà entré dans une phase de base prête pour la revue externe, mais l’attention doit se concentrer sur :

- la solidité de l’architecture centrale
- l’implantation réelle du canonical registry
- l’exécutabilité du modèle de sécurité des operations
- la capacité des shared resources sélectionnées à représenter la direction du projet

Le but de ce document est de condenser ces éléments en un package de revue reproductible, et non de remettre tel quel tout l’espace de travail de l’auteur.

## 2. Ordre de lecture recommandé

Les relecteurs externes devraient lire dans cet ordre :

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

Pour voir les vrais échantillons de ressources, continuez ensuite avec :

- le groupe `8 + 4` de `registry/skills/`
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- les scripts minimaux de gouvernance et les scripts cross-platform de premier lancement dans `local/scripts/`

## 3. Périmètre de revue

Le review package doit actuellement inclure :

- les documents centraux
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- les fichiers de gouvernance minimaux
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- les scripts de gouvernance minimaux
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- les shared resources sélectionnées
  - le groupe `8 + 4` de `registry/skills/`
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Hors périmètre

Les contenus suivants ne doivent pas constituer le corps principal de la revue externe :

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- les mappages de chemins propres à une machine et les restes d’environnement personnel
- les skills candidats non inclus dans la shortlist
- les contenus non suivis ou expérimentaux

`local/docs/authoring/` sert de référence à l’auteur ; ce n’est pas une source canonique pour la revue.

## 5. Commande d’export

À exécuter à la racine du dépôt :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

Sortie par défaut :

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

Pour vérifier le contenu sans écrire de fichiers :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

Avant l’export, il est recommandé d’exécuter au moins :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Pour vérifier l’alignement du delivery canonique des skills :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Lecture actuelle

Au 2026-03-24, `UniText` dispose de :

- une note de couverture et un résumé des points forts destinés aux relecteurs
- des documents centraux lisibles par une revue externe
- le groupe de skills sélectionné `8 + 4`
- une seed d’agent / workflow et une base MCP réellement exécutable
- un flux reproductible pour produire un review package
- un `bootstrap -> verify` multiplateforme
- un flux de backup portable sous forme de `git bundle`

La meilleure formulation actuelle est donc :

**external-review-ready baseline**

et non :

**fully generalized release template**

