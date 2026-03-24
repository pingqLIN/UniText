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
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_PACKAGE.md`
8. `EXTERNAL_REVIEW_COVER_NOTE.md`
9. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
10. `TEMPLATE_RELEASE_PACKAGE.md`
11. `TEMPLATE_RELEASE_CHECKLIST.md`
12. `SECRET_HANDLING_GUIDELINES.md`
13. `NO_PUBLISH_POLICY.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. Resource-Katalog

Aktuell betrachtet das Registry die folgenden Shared-Resource-Typen:

| Typ | Logische Wurzel | Zweck |
|---|---|---|
| `skills` | `/registry/skills` | Skill-Definitionen, die von mehreren CLIs genutzt werden können |
| `mcp` | `/registry/mcp` | kanonische MCP-Definitionen |
| `agents` | `/registry/agents` | gemeinsame Agent-Anweisungen und Persona-Definitionen |
| `workflow` | `/registry/workflow` | gemeinsame Prozesse, Runbooks, Planning-Guidance |

Die folgenden Bereiche sind keine Shared-Resource-Typen:

| Bereich | Logische Wurzel | Rolle |
|---|---|---|
| `operations state` | `/operations` | Inventories, Backups, Drift-Logs, History-Records |

## 3. Grundform eines Starter-Katalogs

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

Die aktuelle externe Review-Topliste folgt [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) und dessen `8 + 4`-Auswahl statt des vollständigen Kandidatenpools.

### Review Package

Wenn du Material für externe Reviewer aufbereiten willst, nutze [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) als Einstieg und `local/scripts/export-review-package.ps1`, um ein wiederholbar erzeugbares Review Package zu erstellen.

Wenn du den kürzesten Einstieg direkt an Reviewer geben willst, lies zuerst:

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

Wenn du ein sauberes Starter Package aufbereiten willst, lies [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) und nutze `local/scripts/export-template-package.ps1`.

Wenn du das exportierte Starter Package verifizieren willst, nutze `local/scripts/verify-template-package.ps1`.

Wenn du auf einem neuen Rechner den ersten `initialize -> verify`-Durchlauf ausführen willst, verwende bevorzugt:

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Verwandte Konzeptnotizen

Wenn du die Zusammenarbeit von `UniText` und `skill-0` bewerten willst, lies [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md).

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
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Bootstrap schreibt eine projektlokale `.mcp.json` und einen Codex-Native-Config-Eintrag, der auf den mitgelieferten read-only MCP-Server zeigt. |

### Agents

| Feld | Wert |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Als gemeinsame Agent-Persona für Review- und Adoption-Aufgaben verwenden; das tatsächliche Wiring hängt von der CLI-Fähigkeit ab. |

## 5. Beispiel-Katalogeinträge

### Beispiel: Skill

| Feld | Wert |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Nutze den Skills-Adapter; der aufgelöste Modus hängt von CLI-Fähigkeiten und lokaler Umgebung ab. |

### Beispiel: MCP-Definition

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

- welche Ressourcen es hier gibt
- wo ihre logische Position liegt
- welche CLIs unterstützt werden

`INDEX.md` beantwortet nicht direkt:

- absolute Pfade einer bestimmten Plattform
- den endgültig aufgelösten Delivery-Modus
- lokale Konfigurationen einer einzelnen Authoring-Umgebung

## 7. Nutzung dieser Baseline

### Für Menschen

1. zuerst `VISION.md` lesen
2. mit `INDEX.md` den eigenen Starter-Katalog aufbauen
3. mit `RESOURCE_SPEC.md` die Ressourcenfelder definieren
4. mit `OPERATIONS.md` Plattform- und CLI-Anbindung definieren

### Für AI-Agents

1. `INDEX.md` zuerst als Discovery-Einstieg lesen
2. bei Bedarf an Schema `RESOURCE_SPEC.md` lesen
3. bei Bedarf an Delivery / Mutation `OPERATIONS.md` lesen
4. niemals einen einzelnen Deployment-Pfad als Spezifikationstheorie behandeln
