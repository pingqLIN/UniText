# UniText — Vision

> Status: Template Base
> Prinzip: Logischen Verträgen folgen, nicht irgendeinem einzelnen Betriebssystem, Verzeichnislayout oder Deployment-Muster.

## 1. Was UniText ist

`UniText` ist ein text-natives, registry-first, AI-first Shared Resource Hub, damit mehrere AI-CLI- / Agent-Systeme dieselben Textverträge für Ressourcen-Definitionen und Adoption nutzen können.

Es besteht aus zwei Schichten:

1. `Registry`
   - definiert Shared Resources, kanonische Identität und minimale Verträge
2. `Adapter / Operations Control Plane`
   - verbindet den Registry-Inhalt mit verschiedenen CLIs und behandelt Install, Sync, Adopt und Repair

## 2. Welches Problem es löst

`UniText` löst die Fragmentierung, die beim Teilen von Ressourcen über Tools hinweg oft entsteht:

- Skills liegen an mehreren Orten verstreut
- MCP-Definitionen sind auf verschiedene Konfigurationsformate verteilt
- Agent-Anweisungen lassen sich nicht gemeinsam nutzen
- Workflow-Konventionen sind schwer zwischen Tools zu übertragen
- es fehlt eine für AI gut lesbare, versionskontrollfreundliche Textschnittstelle

## 3. Architekturposition

Offizielle Position:

**Registry-first, adapter-enabled, operations-governed**

Kernprinzipien:

- ohne Registry gibt es keine gemeinsame Quelle und keine gemeinsame Semantik
- ohne Adapter lässt sich das Registry nicht tatsächlich in jede CLI bringen
- AI ist ein wichtiger Consumer und Kollaborateur, aber nicht der einzige verlässliche Integrationsmechanismus

## 4. Ressourcentypen

Standard-Shared-Resource-Typen:

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` gehört nicht zu den Shared-Resource-Typen und soll separat unter `/operations` liegen.

## 5. Discovery und Delivery

`INDEX.md` ist für Discovery zuständig und beantwortet:

- welche Ressourcen existieren
- wo die logische Position jeder Ressource liegt
- welche CLIs unterstützt werden

`OPERATIONS.md` ist für Delivery zuständig und beantwortet:

- wie eine bestimmte CLI Ressourcen erhält
- wann Install, Sync, Adopt und Repair ausgeführt werden
- wie der Delivery-Modus aufgelöst wird

Verfügbare Delivery-Modi:

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Delivery-Triggers

Delivery darf nur durch explizite Trigger gestartet werden:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

Alle destruktiven Operationen müssen Folgendes einhalten:

- zuerst Dry-Run
- zuerst Backup
- niemals die kanonische Quelle stillschweigend festlegen

## 7. Adoption-Modell

### Soft Adoption

- erst Discovery einführen
- bestehende Ressourcen nicht sofort zur Migration zwingen

### Formale Adoption

Formaler Adoption-Flow:

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

Wenn gleichnamige Ressourcen mit unterschiedlichem Inhalt gefunden werden, muss der Flow bei `REVIEW / DRY-RUN` stoppen.

## 8. Dokumentationssatz

Kerndokumente:

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Pfadstrategie

Der Haupttext verwendet logische kanonische Pfade, zum Beispiel:

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

Absolute Pfade und plattformspezifische Einstellungen gehören nur ins Deployment-Mapping, nicht in die Vision-Spezifikation.

## 10. Designprinzipien

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. Position in einem Satz

> UniText ist ein text-natives, registry-first, AI-first Shared Resource Hub, das über eine klare Adapter- und Operations-Control-Plane mehreren AI-CLIs erlaubt, dieselben kanonischen Ressourcen sicher zu entdecken, zu übernehmen und gemeinsam zu nutzen.
