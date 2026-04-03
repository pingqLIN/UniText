# UniText — Index

> Status: Template Base
> Rolle: Erster Lesepunkt für alle Menschen und AI-Agents, als Discovery-Einstieg.

`UniText` verwendet reinen Text als gemeinsame Schnittstelle und betont eine einheitliche Cross-CLI-Kompatibilität sowie AI-first Discovery.

## 1. Kerndokumente

Empfohlene Lesereihenfolge:

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

## 2. Ressourcenkatalog

Das Registry betrachtet aktuell die folgenden Shared-Resource-Typen:

| Typ | Logische Wurzel | Zweck |
|---|---|---|
| `skills` | `/registry/skills` | Skill-Definitionen, die von mehreren CLIs genutzt werden können |
| `mcp` | `/registry/mcp` | kanonische MCP-Definitionen |
| `agents` | `/registry/agents` | gemeinsame Agent-Anweisungen und Persona-Definitionen |
| `workflow` | `/registry/workflow` | gemeinsame Abläufe, Runbooks und Planning-Guidance |

Die folgenden Bereiche sind keine Shared-Resource-Typen:

| Bereich | Logische Wurzel | Rolle |
|---|---|---|
| `operations state` | `/operations` | Inventories, Backups, Drift-Logs, History-Records |

## 3. Form eines Starter-Katalogs

Ein minimaler Katalogeintrag sollte mindestens enthalten:

- `id`
- `type`
- `canonical_location`
- `status`

Empfohlen sind zusätzlich:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

Die vollständigen Feldregeln stehen in `RESOURCE_SPEC.md`.

## 4. Aktuelle Katalogeinträge

### Review Shortlist

Die aktuelle externe Review-Basis folgt dem `8 + 4`-Set aus [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) und nicht dem vollständigen Kandidatenpool.

### Review Package

Wenn du Material für externe Reviewer aufbereiten willst, nutze [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) als Einstieg und `local/scripts/export-review-package.ps1`, um ein wiederholbar erzeugbares Review Package zu erstellen.

Wenn du den kürzesten Einstieg direkt an Reviewer geben willst, lies zuerst:

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Wenn du ein sauberes Starter Package aufbereiten willst, lies [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) und nutze `local/scripts/export-template-package.ps1`.

Wenn du das exportierte Starter Package verifizieren willst, nutze `local/scripts/verify-template-package.ps1`.

Wenn du zuerst prüfen willst, ob die tracked shared surfaces im Authoring-Repo keine live workspace metadata enthalten, nutze `local/scripts/verify-workspace-boundaries.ps1`.

Wenn du vor einer künftigen Diskussion über Push-Suitability erst einen lokalen Bericht erstellen willst, nutze `local/scripts/get-publishability-report.ps1`.

Wenn du Shared-Metadata-Erkennungsregeln anpassen oder deren Beispiele verstehen willst, lies zuerst [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) und nutze danach `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`.

Wenn du das aktuelle Repo direkt zu einem neuen Starter Project umbauen willst, lies [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) und nutze:

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

Wenn du auf einem neuen Rechner den ersten `initialize -> verify`-Durchlauf ausführen willst, verwende bevorzugt:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Verwandte Konzeptnotizen

Wenn du die aktuelle repo-level Bootstrap-Baseline, die Einschränkungen und die weitere Cross-Platform-Verifikationsrichtung für `Copilot CLI` verstehen willst, lies [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md).

Wenn du bewerten willst, wie `UniText` mit `skill-0` zusammenarbeiten kann, lies [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

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

Die folgenden Skills existieren bereits im shared registry, gehören aber nicht zur aktuellen externen `8 + 4`-Shortlist.

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

| Feld | Wert |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Nutze einen Workflow-Adapter oder eine projektlokale Planzuordnung, je nach CLI-Fähigkeit. |

### MCP

| Feld | Wert |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Bootstrap schreibt eine Projekt-`.mcp.json`, einen Codex-native-config-Eintrag und einen Copilot-`~/.copilot/mcp-config.json`-Eintrag, der auf den gebündelten read-only MCP-Server zeigt. |

### Agents

| Feld | Wert |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Als gemeinsame Agent-Persona für Review- und Adoption-Aufgaben nutzbar; das tatsächliche Wiring hängt weiterhin von den CLI-Fähigkeiten ab. |

## 5. Beispielhafte Katalogeinträge

### Beispiel: Skill

| Feld | Wert |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Nutze den Skills-Adapter; der tatsächliche Modus hängt von CLI-Fähigkeiten und lokaler Umgebung ab. |

### Beispiel: MCP Definition

| Feld | Wert |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Über den MCP-Adapter registrieren; der endgültige Delivery-Modus hängt von CLI-Fähigkeiten und lokaler Umgebung ab. |

## 6. Discovery-Regeln

`INDEX.md` beantwortet:

- Welche Ressourcen es hier gibt
- Wo ihre logischen Positionen liegen
- Welche Spezifikation oder Betriebsdokumentation zuerst gelesen werden sollte

`INDEX.md` beantwortet nicht direkt:

- Absolute Pfade einer bestimmten Plattform
- Den final aufgelösten Delivery-Modus
- Die lokale Konfiguration eines bestimmten Author-Workspaces
- Wo local authoring plans, review notes oder live workspace baselines hingehören; dafür siehe `DOCUMENT_PLACEMENT_POLICY.md`

## 7. Wie dieses Baseline zu nutzen ist

### Für Menschen

1. Zuerst `VISION.md` lesen
2. Mit `INDEX.md` den eigenen Starter-Katalog aufbauen
3. Mit `RESOURCE_SPEC.md` die Ressourcenfelder definieren
4. Mit `OPERATIONS.md` die Plattform- und CLI-Anbindung definieren

### Für AI-Agents

1. `INDEX.md` zuerst als Discovery-Einstieg behandeln
2. Für Schema-Fragen `RESOURCE_SPEC.md` lesen
3. Für Delivery / Mutation `OPERATIONS.md` lesen
4. Niemals die Pfade einer einzelnen Bereitstellung als Spezifikationswahrheit behandeln
