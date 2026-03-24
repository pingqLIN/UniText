# UniText — Índice

> Estado: Template Base
> Rol: punto de primera lectura para todas las personas y agentes AI, usado para discovery.

`UniText` usa texto plano como interfaz compartida y pone el foco en compatibilidad unificada entre CLIs y discovery AI-first.

## 1. Documentos Base

Orden de lectura recomendado:

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

## 2. Catálogo de Recursos

Actualmente el registry cubre los siguientes tipos de shared resource:

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | Definiciones de skill compartidas entre múltiples CLIs |
| `mcp` | `/registry/mcp` | definiciones canónicas de MCP |
| `agents` | `/registry/agents` | instrucciones y personas compartidas de agentes |
| `workflow` | `/registry/workflow` | procesos compartidos, runbooks y guías de planeación |

Los siguientes contenidos no son tipos de shared resource:

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories, backups, drift logs y registros de historial |

## 3. Forma Mínima del Catálogo

Una entrada mínima del catálogo debe incluir al menos:

- `id`
- `type`
- `canonical_location`
- `status`

Se recomienda además incluir:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Las reglas completas de los campos están en `RESOURCE_SPEC.md`.

## 4. Entradas Actuales del Catálogo

### Lista de Skills para Revisión

La revisión externa actual se basa en el conjunto curado `8 + 4` de [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md), y no en todo el pool de candidatos.

### Paquete de Revisión

Si quieres organizar material para revisores externos, usa [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) como entrada y ejecuta `local/scripts/export-review-package.ps1` para generar un review package reproducible.

Si quieres una entrada mínima para revisores, primero mira:

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Release de Template

Si quieres organizar un starter package limpio, consulta [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) y usa `local/scripts/export-template-package.ps1`.

Si quieres verificar el starter package exportado, usa `local/scripts/verify-template-package.ps1`.

Si quieres completar el primer `initialize → verify` en una máquina nueva, usa preferentemente:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Notas Relacionadas

Si quieres evaluar cómo `UniText` puede colaborar con `skill-0`, consulta [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

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

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Usa un workflow adapter o un mapeo de plan local del proyecto, según la capacidad de la CLI. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Bootstrap escribe un `.mcp.json` del proyecto y una entrada native-config de Codex que apunta al servidor MCP read-only incluido. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Úsalo como persona de agente compartida para tareas de revisión y adopción; el wiring real depende de la capacidad de la CLI. |

## 5. Ejemplos de Entradas de Catálogo

### Ejemplo: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Usa el skills adapter; el modo final depende de las capacidades de la CLI y del entorno local. |

### Ejemplo: Definición MCP

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Regístralo a través del MCP adapter; el modo final de entrega depende de las capacidades de la CLI y del entorno local. |

## 6. Reglas de Discovery

`INDEX.md` responde a:

- qué recursos existen aquí
- dónde está la ubicación lógica de cada recurso
- qué CLI están soportadas

`INDEX.md` no responde directamente a:

- rutas absolutas de una plataforma
- el modo de entrega final ya resuelto
- la configuración local del workspace de un autor

## 7. Cómo Usar Esta Base

### Para Humanos

1. Primero lee `VISION.md`
2. Usa `INDEX.md` para construir tu propio starter catalog
3. Usa `RESOURCE_SPEC.md` para definir los campos del recurso
4. Usa `OPERATIONS.md` para definir el acoplamiento entre plataformas y CLIs

### Para Agentes AI

1. Usa `INDEX.md` como entrada de discovery
2. Si necesitas schema, lee `RESOURCE_SPEC.md`
3. Si necesitas delivery o mutation, lee `OPERATIONS.md`
4. No tomes ninguna ruta de despliegue específica como verdad normativa
