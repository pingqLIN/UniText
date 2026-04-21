[English](../../README.md) | [Español](README.md)

# UniText

> **Un hub compartido de recursos, basado en texto nativo y registry-first, para múltiples AI CLIs.**
>
> Una interfaz compartida en texto plano para que Claude Code, Codex, Gemini CLI y otras herramientas compartan la misma definición de recursos.

---

## Lo Que UniText Está Haciendo En Realidad

UniText no es solo una carpeta con prompts, skills o plantillas de MCP. Es una forma gobernada de mantener una sola canonical definition para recursos de AI compartidos mientras separa el machine-local wiring, la activación local del proyecto y el historial operativo. La meta es evitar que cada CLI termine creando su propia copia, cada vez más desviada, de la misma capacidad.

Por eso este repositorio reúne `registry/`, `local/`, `ops/`, template export, rebuild flow, boundary verification, bootstrap y publishability checks en un mismo sistema. Lo que UniText intenta hacer de verdad es volver el tooling compartido de AI portable, reviewable y repeatable entre diferentes CLI, diferentes máquinas y distintas etapas del ciclo de vida de un proyecto.

---

## Por qué existe

Si usas más de una herramienta AI CLI, los recursos terminan dispersos:

- El mismo skill definido tres veces, en tres estados ligeramente distintos
- Configuraciones de servidores MCP en formatos que otras herramientas no pueden leer
- Instrucciones de agentes que sólo una CLI conoce
- Ninguna forma clara de saber cuál copia es la canónica

UniText resuelve esto con un registry compartido y una capa de entrega gobernada. **Una definición. Todas las herramientas.**

---

## Cómo funciona

```
UniText/
├── registry/          ← definiciones canónicas (qué existe)
│   ├── skills/        ← definiciones compartidas de skills
│   ├── mcp/           ← definiciones de servidores MCP
│   ├── agents/        ← instrucciones y personalidades de agentes
│   └── workflow/      ← runbooks, planes, convenciones
│
├── local/             ← capa de despliegue (cómo se conecta aquí)
│   ├── docs/          ← mapas de rutas, notas de despliegue
│   └── scripts/       ← scripts de sincronización para esta máquina
│
└── ops/               ← estado operacional (no recursos compartidos)
    └── history/       ← historial de auditoría con marcas de tiempo
```

La capa `registry/` es agnóstica a la plataforma: usa rutas lógicas canónicas (`/registry/skills`, `/registry/mcp`) en lugar de rutas absolutas específicas del sistema operativo. La capa `local/` resuelve esas rutas hacia tu máquina real.

---

## Arquitectura

**Registry-first, adapter-enabled, operations-governed.**

| Capa | Rol |
|-------|-----|
| **Registry** | Define qué recursos compartidos existen y su identidad canónica |
| **Adapter** | Entrega el contenido del registry a cada CLI (mirror, symlink, native-config, pointer) |
| **Operations** | Gobierna cuándo y cómo ocurren las mutaciones, con backup, dry-run y trazabilidad |

### Tipos de recurso

| Tipo | Raíz lógica | Qué va aquí |
|------|-------------|-------------|
| `skills` | `/registry/skills` | Definiciones de skills compartidas usadas por agentes AI |
| `mcp` | `/registry/mcp` | Definiciones de servidores MCP, entre CLIs |
| `agents` | `/registry/agents` | Instrucciones de agentes, personas, system prompts |
| `workflow` | `/registry/workflow` | Runbooks, plantillas de planeación, convenciones |

### Modos de entrega

Cada recurso puede entregarse de forma distinta según la capacidad de la CLI:

- `pointer` — sólo descubrimiento, sin copiar contenido
- `mirror` — copia local vía robocopy/rsync
- `symlink` — enlace a la fuente canónica en una ruta fija
- `native-config` — registrado en el propio formato de configuración de la CLI

---

## Empezar

### 1. Haz fork o clona este repositorio

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. Añade tu primer recurso

Crea un skill dentro de `registry/skills/`:

```
registry/skills/my-skill/
└── SKILL.md
```

`SKILL.md` mínimo:

```yaml
---
name: my-skill
description: What this skill does in one line
---

## Usage

Instructions for the AI agent...
```

### 3. Regístralo en el catálogo

Añade una entrada a `INDEX.md`:

| Campo | Valor |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. Inicializa el wiring local de tus CLIs

Prefiere la ruta de bootstrap multiplataforma:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` alinea los objetivos compartidos de skills, actualiza `skills_path` de Codex y escribe un `.mcp.json` local al proyecto para el baseline MCP incluido. `sync-skills.ps1` sigue disponible como implementación de referencia en Windows PowerShell.

---

## CLIs compatibles

| CLI | Modo de entrega | Notas |
|-----|----------------|-------|
| **Claude Code** | mirror / symlink | `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + MCP local de proyecto | `skills_path` y `[mcp_servers.*]` en `~/.codex/config.toml` |
| **GitHub CLI** | native-config | `config.yml` |

Consulta [template/examples/local/docs/PATH_MAP.template.md](template/examples/local/docs/PATH_MAP.template.md) para la referencia completa de rutas por CLI.

---

## Reglas de gobernanza

UniText aplica una política de **sin cambios silenciosos**:

1. **Sólo triggers explícitos** — `bootstrap`, `sync`, `adopt`, `repair`
2. **Backup antes de cualquier mutación** — toda acción destructiva crea una instantánea con marca temporal en `ops/`
3. **Dry-run antes de la entrega** — previsualiza qué cambiará antes de que ocurra
4. **El conflicto detiene el flujo** — si dos versiones del mismo recurso difieren, el sistema se detiene para revisión humana
5. **Trazabilidad completa** — cada operación se escribe en `ops/history/`

Flujo formal de adopción: `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentación

| Archivo | Propósito |
|--------|-----------|
| [INDEX.md](INDEX.md) | Punto de entrada para discovery: qué recursos existen y dónde están |
| [VISION.md](VISION.md) | Principios de arquitectura y justificación de diseño |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Contrato de metadata para todos los shared resources |
| [OPERATIONS.md](OPERATIONS.md) | Modos de entrega, triggers y reglas de seguridad |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Diferencia entre repo de authoring y template del proyecto |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Límites para almacenar secretos, redacción y manejo de passwords/API keys |
| [MILESTONES.md](MILESTONES.md) | Objetivos de fase cuantificados y checkpoints de readiness para revisión externa |
| [docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md](docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md) | Conjunto curado de skills esenciales `8 + 4` para la ola de revisión actual |
| [docs/reviews/EXTERNAL_REVIEW_PACKAGE.md](docs/reviews/EXTERNAL_REVIEW_PACKAGE.md) | Alcance para revisores, orden de lectura y flujo de exportación repetible |
| [docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md](docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md) | Nota de envío para revisores externos |
| [docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md](docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md) | Resumen corto para orientación rápida |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Alcance de cleanup para release, exclusiones y flujo de exportación |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Checklist previo al release para un starter package |
| [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md) | Nota conceptual sobre cómo UniText puede colaborar con skill-0 como proyecto de descomposición y extracción de primitivas |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Límite local-first de publicación para agentes y colaboradores |

Orden de lectura: `docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md` → `docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `docs/concepts/SKILL0_COLLABORATION_VISION.md`

---

## Dos formas de usarlo

### Como template de arranque

Haz fork de este repo. Elimina `ops/history/`, `backup/` y las rutas de `local/` específicas de esta máquina. Pobla `registry/` con tus propios skills y definiciones MCP. Conecta `local/scripts/` a tu entorno.

### Como implementación de referencia

Lee los docs base para entender la arquitectura. Adapta los patrones: estructura del registry, spec de recursos, modos de entrega, y trazabilidad de operaciones a tu propio entorno.

---

## Principios de diseño

- **Registry first** — define antes de entregar
- **Discovery before automation** — conoce lo que existe antes de sincronizarlo
- **Platform-agnostic contracts** — rutas lógicas en las specs, rutas absolutas sólo en la capa local
- **Minimum viable metadata** — `id`, `type`, `canonical_location`, `status` bastan para empezar
- **Safe mutation** — dry-run + backup + trigger explícito, siempre
- **AI as consumer** — los modelos leen y actúan sobre el registry; no poseen la garantía de entrega

---

## Estado

| Componente | Estado |
|-----------|--------|
| Documentación base | Estable |
| Estructura del registry | Activa — raíces `skills/`, `mcp/`, `workflow/`, `agents/` presentes |
| Skills registry | Baseline activo — primer lote canónico adoptado, la adopción más amplia sigue en curso |
| Agents registry | Seed activo — entrada `registry-curator` creada |
| MCP registry | Baseline activo — definición canónica más servidor read-only ejecutable presente |
| Workflow registry | Seed borrador — documento de workflow más plantilla de plan presentes |
| Trazabilidad de operaciones | Activa |
| Scripts de sync, bootstrap y review | Baseline activo en `local/scripts/` |
| External review package | Baseline activo — guía para revisores y script de exportación presentes |
| Cleanup de template release | Release candidate — guía, checklist, export + verify, ejemplos genéricos y skeleton local presentes |

---

## Licencia

MIT

---

*Para personas que usan más de una herramienta AI y quieren una única fuente de verdad.*
