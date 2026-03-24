# Rapport de progression du projet UniText

> Date du rapport : 2026-03-24
> Nature du rapport : état du projet / Status Report
> Périmètre : documents visibles dans le workspace, artefacts `registry/`, `local/`, `ops/`, et résultats de validation du tour actuel

## I. Résumé exécutif

`UniText` est passé d’une « baseline prête pour la revue externe » à une phase où il peut gérer un premier run multiplateforme, produire un template release candidate et créer un backup portable sous forme de bundle.

Les progrès les plus importants de ce tour sont :

- `mcp` est passé d’une seed purement illustrative à une base read-only réellement exécutable
- `bootstrap.py` et `verify-bootstrap.py` multiplateformes ont été ajoutés
- `skills_path` de Codex et le `.mcp.json` du projet ont été vérifiés en conditions réelles
- `create-git-bundle.py` a été ajouté pour réduire le risque lié à un seul workspace local

Dans l’ensemble, le projet n’est plus seulement constitué d’architecture et de documentation ; il dispose maintenant de :

- canonical registry
- base de sécurité pour les opérations
- flux destiné aux relecteurs
- flux d’export et de vérification du template
- chemin d’initialisation puis vérification multiplateforme
- base MCP exécutable

## II. État d’avancement actuel

### 1. Documents centraux et gouvernance

Documents déjà alignés :

- `README.md`
- `INDEX.md`
- `VISION.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `MILESTONES.md`
- `SECRET_HANDLING_GUIDELINES.md`

### 2. État du registry

Les quatre catégories de shared resources ont maintenant du contenu de revue :

- `skills`
  - réduit au groupe de revue `8 + 4`
- `agents`
  - contient `registry-curator`
- `mcp`
  - contient `claude-project-mcp-seed`
  - avec `definition.json` et `server.py` exécutable
- `workflow`
  - contient `claude-plans`

### 3. Scripts et flux exécutables

Le projet dispose maintenant de :

- scripts d’operations Windows-first
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
  - `export-template-package.ps1`
  - `verify-template-package.ps1`
- scripts de premier run multiplateformes
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`

### 4. Ligne Review et ligne Template

Déjà achevés :

- note de couverture pour relecteurs
- résumé des points forts pour relecteurs
- flux d’export du review package
- flux d’export et de vérification du template package
- skeleton local de départ
- exemples génériques `template-safe`

## III. Résultats de validation

Cette fois-ci, les vérifications suivantes ont été confirmées :

- `health-check.ps1` = `ok`
- `verify-delivery.ps1` passe
- `verify-bootstrap.py` = `ok`
- `skills_path` de Codex est aligné sur `Q:\UniText\registry\skills`
- le `.mcp.json` à la racine du repo a bien été écrit
- `claude-project-mcp-seed/server.py` a passé le smoke test du protocole MCP minimal
- `create-git-bundle.py` a produit un bundle backup avec succès

État quantifiable actuel :

- adopted skills = `12`
- invalid skills = `0`
- agent seed = `true`
- mcp seed = `true`
- workflow seed = `true`

## IV. Détermination des phases

| Phase | Détermination actuelle |
|---|---|
| Phase 1: Skills Registry Online | Terminée |
| Phase 2: Full Registry Baseline | Terminée au niveau baseline, et `mcp` n’est plus une simple stub |
| Phase 3: External Review Ready | Terminée |
| Phase 4: Template Release Ready | Niveau release candidate atteint, mais il est encore recommandé d’ajouter un backup distant et des vérifications CLI plus larges |

## V. Manques encore présents

### 1. Il est toujours recommandé d’ajouter un filet de sécurité distant

Même si un `git bundle` portable existe désormais, un remote backup formel reste une étape plus robuste.

### 2. `agents / workflow` restent encore des seeds

Ces deux catégories ne sont plus des racines vides, mais leur profondeur de contenu reste en deçà de celle du groupe `skills`.

### 3. `mcp` est exécutable mais encore minimal

Il suffit déjà pour la revue externe et le first-run baseline, mais il ne constitue pas encore un catalogue MCP riche.

### 4. La release du template possède encore une marge de productisation

Les points restants sont surtout :

- un nettoyage plus strict des artefacts local-only
- une stratégie de version pour les artefacts de release
- une validation plus large sur des utilisateurs non auteurs

## VI. Jugement global

Le positionnement le plus juste pour `UniText` est :

**external-review-ready baseline + template release candidate**

Cela signifie que le projet offre désormais :

- un canonical registry consultable
- un modèle d’operations gouverné
- un first-run multiplateforme exécutable
- une base MCP minimale réellement exécutable
- des review / template packages reproductibles

Le projet n’est donc plus seulement « mature sur le plan de la conception mais pauvre en réalisation » ; il est maintenant entré dans une phase où il peut être livré, vérifié et proposé comme candidat à publication.

