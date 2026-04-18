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
6. `DOCUMENT_PLACEMENT_POLICY.md`
7. `WORKSPACE_SENSITIVE_METADATA_RULES.md`
8. `TEMPLATE_RELEASE_PACKAGE.md`
9. `TEMPLATE_RELEASE_CHECKLIST.md`
10. `REBUILD_AS_NEW_PROJECT.md`
11. `SECRET_HANDLING_GUIDELINES.md`
12. `NO_PUBLISH_POLICY.md`
13. `COPILOT_CLI_ADAPTER_NOTE.md`
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

À la date du `2026-04-18`, `registry/skills/` dans l’authoring tree contient `48` répertoires de skill. Le tableau ci-dessous est un review-facing catalog excerpt, pas un inventory dump complet.

### Review Package

Pour préparer un dossier destiné à des relecteurs externes, utilisez [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) comme point d’entrée, puis `local/scripts/export-review-package.ps1` pour produire un review package reproductible.

Pour l’entrée la plus courte destinée aux relecteurs, commencez par :

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Pour préparer un starter package propre, lisez [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) et utilisez `local/scripts/export-template-package.ps1`.

Pour vérifier le starter package exporté, utilisez `local/scripts/verify-template-package.ps1`.

Pour vérifier d’abord que les tracked shared surfaces du repo d’authoring ne contiennent pas de live workspace metadata, utilisez `local/scripts/verify-workspace-boundaries.ps1`.

Pour générer un rapport local avant toute discussion future sur la push suitability, utilisez `local/scripts/get-publishability-report.ps1`.

Pour ajuster les règles de détection des shared metadata ou comprendre les cas de règles, lisez d’abord [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md), puis utilisez `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`.

Pour reconstruire directement le repo actuel en un nouveau starter project, lisez [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md), puis utilisez :

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

Pour terminer un premier cycle `initialize → verify` sur une nouvelle machine, privilégiez :

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Notes conceptuelles associées

Pour comprendre la repo-level bootstrap baseline actuelle de `Copilot CLI`, ses limites et la direction de validation cross-platform à venir, consultez [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md).

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

### Workspace-Specific Skills

Les skills suivants existent déjà dans le shared registry, mais ne font pas partie de la shortlist externe actuelle `8 + 4`.

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `cloudflare` | Workspace | `/registry/skills/cloudflare` | `active` |
| `wrangler` | Workspace | `/registry/skills/wrangler` | `active` |
| `building-mcp-server-on-cloudflare` | Workspace | `/registry/skills/building-mcp-server-on-cloudflare` | `active` |
| `cloudflare-governance` | Workspace | `/registry/skills/cloudflare-governance` | `active` |
| `cloudflare-access-mcp` | Workspace | `/registry/skills/cloudflare-access-mcp` | `active` |
| `cloudflare-edge-security` | Workspace | `/registry/skills/cloudflare-edge-security` | `active` |
| `cloudflare-runtime-sync` | Workspace | `/registry/skills/cloudflare-runtime-sync` | `active` |
| `cloudflare-tunnel-dns` | Workspace | `/registry/skills/cloudflare-tunnel-dns` | `active` |
| `cloudflare-zerotrust-device` | Workspace | `/registry/skills/cloudflare-zerotrust-device` | `active` |

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
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Le bootstrap écrit un `.mcp.json` de projet, une entrée native-config de Codex et une entrée `~/.copilot/mcp-config.json` pour Copilot pointant vers le MCP server read-only embarqué. |

### Agents

| Champ | Valeur |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Peut être utilisé comme persona d’agent partagé pour les tâches de review et d’adoption ; le wiring réel dépend toujours des capacités du CLI. |

## 5. Exemples d’entrées de catalogue

### Exemple : Skill

| Champ | Valeur |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Utiliser l’adaptateur de skills ; le mode de résolution dépend des capacités du CLI et de l’environnement local. |

### Exemple : MCP Definition

| Champ | Valeur |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Enregistrer via l’adaptateur MCP ; le delivery mode final dépend des capacités du CLI et de l’environnement local. |

## 6. Discovery Rules

`INDEX.md` répond à :

- quelles ressources existent ici
- où se trouvent leurs positions logiques
- quel document de spécification ou d’exploitation il faut lire

`INDEX.md` ne répond pas directement à :

- un chemin absolu pour une plateforme donnée
- le delivery mode final une fois résolu
- la configuration locale d’un workspace d’auteur donné
- l’endroit où doivent aller les local authoring plans, review notes ou live workspace baselines ; pour cela, voir `DOCUMENT_PLACEMENT_POLICY.md`

## 7. How To Use This Baseline

### For Humans

1. Lire d’abord `VISION.md`
2. Utiliser `INDEX.md` pour construire son propre starter catalog
3. Utiliser `RESOURCE_SPEC.md` pour définir les champs de ressources
4. Utiliser `OPERATIONS.md` pour définir l’intégration plateforme / CLI

### For AI Agents

1. Traiter `INDEX.md` comme point d’entrée de discovery
2. Lire `RESOURCE_SPEC.md` quand un schéma est nécessaire
3. Lire `OPERATIONS.md` quand delivery / mutation est nécessaire
4. Ne pas traiter les chemins d’un déploiement unique comme vérité de spécification
