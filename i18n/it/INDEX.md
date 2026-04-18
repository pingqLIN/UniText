# UniText — Index

> Stato: `Template Base`
> Ruolo: primo punto di lettura per umani e AI, usato come ingresso di discovery.

`UniText` usa il testo puro come interfaccia condivisa e mette l’accento su una compatibilità unificata tra CLI e su una discovery AI-first.

## 1. Core Docs

Ordine di lettura consigliato:

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

## 2. Catalogo delle risorse

Il registry considera attualmente i seguenti tipi di shared resources:

| Tipo | Radice logica | Ruolo |
|---|---|---|
| `skills` | `/registry/skills` | Definizioni di skill riutilizzabili da più CLI |
| `mcp` | `/registry/mcp` | Definizioni MCP canoniche |
| `agents` | `/registry/agents` | Istruzioni e personas condivise degli agent |
| `workflow` | `/registry/workflow` | Flussi condivisi, runbook e planning guidance |

Gli elementi seguenti non sono shared resource types:

| Area | Radice logica | Ruolo |
|---|---|---|
| `operations state` | `/operations` | inventari, backup, log di drift e storico |

## 3. Forma dello starter catalog

Una voce minima del catalogo dovrebbe contenere almeno:

- `id`
- `type`
- `canonical_location`
- `status`

Si consiglia di aggiungere anche:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Le regole complete sui campi si trovano in `RESOURCE_SPEC.md`.

## 4. Voci attuali del catalogo

### Review Shortlist

L’attuale base per la review esterna segue il set `8 + 4` definito in [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md), non l’intero pool di candidati.

Alla data `2026-04-18`, `registry/skills/` nell’authoring tree contiene `48` directory di skill. La tabella seguente è un review-facing catalog excerpt, non un inventory dump completo.

### Review Package

Per preparare materiale per reviewer esterni, usa [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) come punto di ingresso e `local/scripts/export-review-package.ps1` per produrre un review package ripetibile.

Se vuoi fornire ai reviewer il percorso più breve possibile, inizia da:

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Per preparare uno starter package pulito, leggi [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) e usa `local/scripts/export-template-package.ps1`.

Per verificare lo starter package esportato, usa `local/scripts/verify-template-package.ps1`.

Se vuoi prima verificare che le tracked shared surfaces del repo di authoring non contengano live workspace metadata, usa `local/scripts/verify-workspace-boundaries.ps1`.

Se vuoi generare un report locale prima di discutere in futuro la push suitability, usa `local/scripts/get-publishability-report.ps1`.

Se vuoi modificare le regole di rilevazione dei shared metadata o capirne i casi, leggi prima [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md), poi usa `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`.

Se vuoi ricostruire direttamente il repo attuale come un nuovo starter project, leggi [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) e usa:

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

Se vuoi completare il primo ciclo `initialize → verify` su una nuova macchina, dai priorità a:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Note concettuali correlate

Per capire l’attuale repo-level bootstrap baseline di `Copilot CLI`, i suoi limiti e la direzione futura della validazione cross-platform, consulta [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md).

Per valutare come `UniText` possa collaborare con `skill-0`, consulta [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

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

Le seguenti skill esistono già nel shared registry, ma non fanno parte dell’attuale shortlist esterna `8 + 4`.

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

| Campo | Valore |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Usa un workflow adapter o un project-local plan mapping in base alle capacità del CLI. |

### MCP

| Campo | Valore |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Il bootstrap scrive un `.mcp.json` di progetto, una voce native-config di Codex e una voce `~/.copilot/mcp-config.json` per Copilot che punta al MCP server read-only incluso. |

### Agents

| Campo | Valore |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Può essere usato come persona condivisa per compiti di review e adoption; il wiring reale dipende comunque dalle capacità del CLI. |

## 5. Esempi di voci di catalogo

### Esempio: Skill

| Campo | Valore |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Usa l’adattatore per skills; la modalità finale dipende dalle capacità del CLI e dall’ambiente locale. |

### Esempio: MCP Definition

| Campo | Valore |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Registralo tramite l’adattatore MCP; la delivery mode finale dipende dalle capacità del CLI e dall’ambiente locale. |

## 6. Discovery Rules

`INDEX.md` risponde a:

- quali risorse esistono qui
- dove si trovano le loro posizioni logiche
- quale documento di specifica o operativo conviene leggere

`INDEX.md` non risponde direttamente a:

- un percorso assoluto di una piattaforma specifica
- la delivery mode finale già risolta
- la configurazione locale di uno specifico author workspace
- dove devono stare local authoring plans, review notes o live workspace baselines; per questo vedi `DOCUMENT_PLACEMENT_POLICY.md`

## 7. How To Use This Baseline

### For Humans

1. Leggi prima `VISION.md`
2. Usa `INDEX.md` per costruire il tuo starter catalog
3. Usa `RESOURCE_SPEC.md` per definire i campi delle risorse
4. Usa `OPERATIONS.md` per definire l’integrazione tra piattaforma e CLI

### For AI Agents

1. Tratta `INDEX.md` come punto di ingresso di discovery
2. Leggi `RESOURCE_SPEC.md` quando serve uno schema
3. Leggi `OPERATIONS.md` quando serve delivery / mutation
4. Non trattare i percorsi di un singolo deployment come verità di specifica
