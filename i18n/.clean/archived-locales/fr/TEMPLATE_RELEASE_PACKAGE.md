# UniText — Package de release du template

> Statut : `Active Baseline`
> Utilité : définir les objectifs, le périmètre et le flux d’export répétable du template release cleanup.

## 1. Objectif

Le template release de `UniText` ne doit pas consister à empaqueter tel quel l’espace de travail de l’auteur. Il doit produire une version qui :

- conserve l’architecture et les specs centrales
- conserve les exemples minimaux utilisables
- exclut l’état local uniquement
- exclut les résidus historiques de gouvernance
- convient à d’autres personnes qui forkent ou clonent le projet pour l’étendre ensuite

Le positionnement du package est :

**starter template**

et non :

**authoring workspace snapshot**

## 2. À inclure

Le template package doit actuellement inclure :

- documents centraux
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- config racine `template-safe`
  - `.gitignore`
- exemples génériques
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- skeleton de couche locale de départ
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- métadonnées de release
  - `manifest.json`
  - `release.json`

## 3. À exclure

Le template package ne doit pas inclure :

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- les comptes utilisateurs réels, le home directory et les chemins absolus
- les documents spécifiques à la revue
  - `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md`
  - `docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md`
  - `docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Commande d’export

À la racine du dépôt :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

Sortie par défaut :

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

Pour vérifier le contenu sans écrire de fichier :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

Pour vérifier le package exporté :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

Après export, le chemin de first-run recommandé pour les nouveaux utilisateurs est :

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Interprétation de l’export

Le package exporté représente :

- le contrat central d’UniText
- une mise en page starter propre
- un ensemble minimal d’exemples génériques

Il ne représente pas :

- l’état de travail complet de l’auteur
- tous les skills déjà adoptés
- toutes les preuves de revue / d’audit
- le câblage local déjà totalement terminé

## 6. Lecture actuelle

Au 2026-03-24, `UniText` dispose déjà de :

- un package de revue externe
- des documents d’entrée destinés aux relecteurs
- une base de nettoyage pour le template release
- un script d’export reproductible du template package
- un skeleton local de départ
- un script de vérification du template package
- des métadonnées de release
- des scripts de first-run multiplateformes
- un flux de backup portable via bundle

La meilleure lecture actuelle est donc :

**template release candidate**

et non :

**authoring workspace snapshot**
