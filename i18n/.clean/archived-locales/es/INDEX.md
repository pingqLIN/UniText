# UniText — Index

> Estado: `Template Base`
> Rol: primer punto de lectura para humanos y AI, usado como entrada de discovery.

`UniText` utiliza texto plano como interfaz compartida y pone énfasis en una compatibilidad unificada entre CLI y en una discovery AI-first.

## 1. Core Docs

Orden de lectura recomendado:

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
13. `docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md`
14. `docs/concepts/SKILL0_COLLABORATION_VISION.md`

## 2. Catálogo de recursos

El registry considera actualmente los siguientes tipos de shared resources:

| Tipo | Raíz lógica | Propósito |
|---|---|---|
| `skills` | `/registry/skills` | Definiciones de skills reutilizables entre varios CLI |
| `mcp` | `/registry/mcp` | Definiciones MCP canónicas |
| `agents` | `/registry/agents` | Instrucciones y personas de agent compartidas |
| `workflow` | `/registry/workflow` | Flujos compartidos, runbooks y guidance de planificación |

Los siguientes elementos no son shared resource types:

| Área | Raíz lógica | Rol |
|---|---|---|
| `operations state` | `/operations` | inventarios, backups, registros de drift e historiales |

## 3. Forma del starter catalog

Una entrada mínima del catálogo debe incluir al menos:

- `id`
- `type`
- `canonical_location`
- `status`

También se recomienda añadir:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Las reglas completas de campos están en `RESOURCE_SPEC.md`.

## 4. Entradas actuales del catálogo

### Review Shortlist

La base actual de revisión externa sigue el conjunto `8 + 4` definido en [docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md](docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md), y no el conjunto completo de candidatos.

### Review Package

Si quieres preparar material para revisores externos, usa [docs/reviews/EXTERNAL_REVIEW_PACKAGE.md](docs/reviews/EXTERNAL_REVIEW_PACKAGE.md) como punto de entrada y `local/scripts/export-review-package.ps1` para producir un review package reproducible.

Si quieres dar a los revisores la entrada más corta posible, empieza por:

- [docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md](docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md)
- [docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md](docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Si quieres preparar un starter package limpio, lee [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) y usa `local/scripts/export-template-package.ps1`.

Si quieres verificar el starter package exportado, usa `local/scripts/verify-template-package.ps1`.

Si primero quieres comprobar que las tracked shared surfaces del repo de authoring no contienen live workspace metadata, usa `local/scripts/verify-workspace-boundaries.ps1`.

Si quieres generar un informe local antes de una futura discusión sobre push suitability, usa `local/scripts/get-publishability-report.ps1`.

Si quieres ajustar las reglas de detección de shared metadata o entender sus casos, lee primero [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) y después usa `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`.

Si quieres reconstruir directamente el repo actual como un nuevo starter project, lee [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) y usa:

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

Si quieres completar el primer flujo `initialize → verify` en una máquina nueva, prioriza:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Notas conceptuales relacionadas

Si quieres entender la repo-level bootstrap baseline actual de `Copilot CLI`, sus límites y la dirección de validación cross-platform, consulta [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md).

Si quieres evaluar cómo puede colaborar `UniText` con `skill-0`, consulta [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md).

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

Los siguientes skills ya existen en el shared registry, pero no forman parte de la shortlist externa actual `8 + 4`.

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

### Workflow

| Campo | Valor |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Usar un workflow adapter o un project-local plan mapping según la capacidad del CLI. |

### MCP

| Campo | Valor |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | El bootstrap escribe un `.mcp.json` de proyecto, una entrada native-config de Codex y una entrada `~/.copilot/mcp-config.json` para Copilot que apunta al MCP server read-only incluido. |

### Agents

| Campo | Valor |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Puede usarse como persona de agent compartida para tareas de revisión y adopción; el wiring real sigue dependiendo de la capacidad del CLI. |

## 5. Ejemplos de entradas de catálogo

### Ejemplo: Skill

| Campo | Valor |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Usa el adaptador de skills; el modo final depende de las capacidades del CLI y del entorno local. |

### Ejemplo: MCP Definition

| Campo | Valor |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Regístralo mediante el adaptador MCP; el delivery mode final depende de las capacidades del CLI y del entorno local. |

## 6. Discovery Rules

`INDEX.md` responde a:

- qué recursos existen aquí
- dónde están sus ubicaciones lógicas
- qué documento de especificación u operación conviene leer

`INDEX.md` no responde directamente a:

- una ruta absoluta de una plataforma concreta
- el delivery mode final ya resuelto
- la configuración local de un author workspace específico
- dónde deben ir local authoring plans, review notes o live workspace baselines; para eso, consulta `DOCUMENT_PLACEMENT_POLICY.md`

## 7. How To Use This Baseline

### For Humans

1. Leer primero `VISION.md`
2. Usar `INDEX.md` para construir tu propio starter catalog
3. Usar `RESOURCE_SPEC.md` para definir los campos de recursos
4. Usar `OPERATIONS.md` para definir la integración entre plataforma y CLI

### For AI Agents

1. Tratar `INDEX.md` como entrada de discovery
2. Leer `RESOURCE_SPEC.md` cuando se necesite esquema
3. Leer `OPERATIONS.md` cuando se necesite delivery / mutation
4. No tratar las rutas de un único despliegue como verdad de especificación
