# UniText — Index

> Statut : `Template Base`
> Rôle : premier point de lecture pour les humains et les IA, utilisé pour la discovery.

`UniText` utilise le texte brut comme interface partagée et met l’accent sur une compatibilité unifiée entre CLI ainsi que sur une discovery AI-first.

## 1. Core Docs

Ordre de lecture recommandé :

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_PACKAGE.md`
8. `EXTERNAL_REVIEW_COVER_NOTE.md`
9. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
10. `TEMPLATE_RELEASE_PACKAGE.md`
11. `TEMPLATE_RELEASE_CHECKLIST.md`
12. `SECRET_HANDLING_GUIDELINES.md`
13. `NO_PUBLISH_POLICY.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. Catalogue des ressources

Le registry s’intéresse actuellement aux types de shared resources suivants :

| Type | Racine logique | Rôle |
|---|---|---|
| `skills` | `/registry/skills` | Définitions de skills partageables entre plusieurs CLI |
| `mcp` | `/registry/mcp` | Définitions canoniques MCP |
| `agents` | `/registry/agents` | Instructions d’agent et personas communs |
| `workflow` | `/registry/workflow` | Flux partagés, runbooks et guidance de planification |

Les éléments suivants ne sont pas des shared resource types :

| Zone | Racine logique | Rôle |
|---|---|---|
| `operations state` | `/operations` | inventaires, backups, journaux de dérive, historiques |

## 3. Forme du catalogue de départ

Une entrée minimale du catalogue doit contenir au moins :

- `id`
- `type`
- `canonical_location`
- `status`

Il est recommandé d’ajouter aussi :

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Les règles complètes sur les champs se trouvent dans `RESOURCE_SPEC.md`.

## 4. Entrées actuelles du catalogue

### Review Shortlist

La base de revue externe suit maintenant l’ensemble sélectionné de `8 + 4` skills défini dans [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md), et non plus l’ensemble complet des candidats.

### Review Package

Pour préparer un dossier destiné à des relecteurs externes, utilisez [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) comme point d’entrée, puis `local/scripts/export-review-package.ps1` pour produire un review package reproductible.

Pour l’entrée la plus courte destinée aux relecteurs, commencez par :

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Pour préparer un starter package propre, lisez [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) et utilisez `local/scripts/export-template-package.ps1`.

Pour vérifier le starter package exporté, utilisez `local/scripts/verify-template-package.ps1`.

Pour terminer un premier cycle `initialize → verify` sur une nouvelle machine, privilégiez :

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Notes conceptuelles associées

Pour évaluer la façon dont `UniText` peut collaborer avec `skill-0`, consultez [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

### Skills

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `/registry/skills/pdf` | `active` |
| `docx` | Core 8 | `/registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `/registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `/registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `/registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `/registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `/registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `/registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `/registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `/registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `/registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `/registry/skills/theme-factory` | `active` |

### Workflow

| Champ | Valeur |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Utiliser un adaptateur de workflow ou un mapping local de plans selon les capacités du CLI. |

### MCP

| Champ | Valeur |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Le bootstrap écrit un `.mcp.json` de projet plus une entrée native-config Codex pointant vers le serveur MCP read-only intégré. |

### Agents

| Champ | Valeur |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | À utiliser comme persona d’agent partagé pour les tâches de revue et d’adoption ; le câblage réel dépend des capacités du CLI. |

## 5. Exemples d’entrées du catalogue

### Exemple : Skill

| Champ | Valeur |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Utiliser l’adaptateur de skills ; le mode final dépend des capacités du CLI et de l’environnement local. |

### Exemple : définition MCP

| Champ | Valeur |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Enregistrer via l’adaptateur MCP ; le mode de livraison final dépend des capacités du CLI et de l’environnement local. |

## 6. Règles de discovery

`INDEX.md` répond à :

- quelles ressources existent ici
- où se trouve leur emplacement logique
- quels documents de spec ou d’opérations consulter ensuite

`INDEX.md` ne répond pas directement à :

- le chemin absolu d’une plateforme
- le mode de delivery final une fois résolu
- la configuration locale d’un espace de travail auteur

## 7. Comment utiliser cette base

### Pour les humains

1. Lire d’abord `VISION.md`
2. Utiliser `INDEX.md` pour construire son starter catalog
3. Utiliser `RESOURCE_SPEC.md` pour définir les champs des ressources
4. Utiliser `OPERATIONS.md` pour définir les liens entre plateformes et CLI

### Pour les agents IA

1. Commencer par utiliser `INDEX.md` comme point d’entrée de la discovery
2. Lire `RESOURCE_SPEC.md` lorsqu’un schéma est nécessaire
3. Lire `OPERATIONS.md` lorsqu’un delivery ou une mutation est nécessaire
4. Ne jamais considérer le chemin d’un déploiement unique comme la vérité du contrat
