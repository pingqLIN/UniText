# UniText — Indice

> Stato: Template Base
> Ruolo: primo punto di lettura per human e AI, usato per il discovery.

`UniText` usa il testo puro come interfaccia condivisa, puntando su compatibilità uniforme tra CLI e discovery AI-first.

## 1. Documenti centrali

Ordine consigliato di lettura:

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

## 2. Catalogo delle risorse

Al momento il registry si concentra su questi shared resource types:

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | definizioni di skill condivisibili tra più CLI |
| `mcp` | `/registry/mcp` | definizioni MCP canoniche |
| `agents` | `/registry/agents` | istruzioni e persona condivise per gli agent |
| `workflow` | `/registry/workflow` | processi condivisi, runbook e linee guida di planning |

I seguenti contenuti non sono shared resource type:

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventari, backup, drift log, record storici |

## 3. Forma minima del catalogo

Una catalog entry minima dovrebbe contenere almeno:

- `id`
- `type`
- `canonical_location`
- `status`

È consigliabile aggiungere anche:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Le regole complete dei campi sono in `RESOURCE_SPEC.md`.

## 4. Voci correnti del catalogo

### Review Shortlist

La shortlist della review esterna fa riferimento al set `8 + 4` di [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md), non all’intero pool di candidate skills.

### Review Package

Se devi preparare il materiale per una revisione esterna, usa [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) come entry point e lo script `local/scripts/export-review-package.ps1` per produrre un review package ripetibile.

Per un ingresso rapido del reviewer, guarda prima:

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Se devi preparare uno starter package pulito, leggi [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) e usa `local/scripts/export-template-package.ps1`.

Per verificare lo starter package esportato, usa `local/scripts/verify-template-package.ps1`.

Per completare la prima initialize → verify su una nuova macchina, usa preferibilmente:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

Per valutare la collaborazione tra `UniText` e `skill-0`, leggi [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

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
| `delivery_guidance` | Usa l’adapter del workflow o il mapping plan locale del progetto, a seconda delle capacità della CLI. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Il bootstrap scrive un `.mcp.json` project-local e una voce Codex native-config che punta al server MCP read-only integrato. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Usalo come persona condivisa per review e adoption; il wiring reale dipende dalle capacità della CLI. |

## 5. Esempi di catalog entries

### Esempio: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Usa l’adapter delle skills; la modalità risolta dipende dalle capacità della CLI e dall’ambiente locale. |

### Esempio: Definizione MCP

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Registralo tramite l’adapter MCP; la modalità finale dipende dalle capacità della CLI e dall’ambiente locale. |

## 6. Regole di discovery

`INDEX.md` risponde a:

- quali risorse esistono
- dove si trova il loro logical path
- quale documento di specifica o operations consultare

`INDEX.md` non risponde direttamente a:

- path assoluti di una piattaforma
- delivery mode finale già risolto
- configurazione locale di un authoring workspace

## 7. Come usare questo baseline

### Per le persone

1. Leggi prima `VISION.md`
2. Usa `INDEX.md` per costruire il tuo starter catalog
3. Usa `RESOURCE_SPEC.md` per definire i campi della risorsa
4. Usa `OPERATIONS.md` per definire il collegamento tra piattaforme e CLI

### Per gli AI agent

1. Usa `INDEX.md` come entry point di discovery
2. Leggi `RESOURCE_SPEC.md` quando ti serve uno schema
3. Leggi `OPERATIONS.md` quando ti serve delivery o mutation
4. Non trattare mai il path di un singolo deployment come verità di specifica

