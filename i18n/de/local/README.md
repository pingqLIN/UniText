# Lokales Overlay

Dieses Verzeichnis enthält **lokale Bereitstellung, Skripte, Pfadzuordnungen und andere nicht-kernige Overlay-Inhalte**.

Der Zweck ist einfach:

- die lokale Konfiguration nicht in die Kernkonzepte des Root-Verzeichnisses einsickern zu lassen
- lokale Anpassungen zentral zu verwalten
- das gesamte `local/` bei Bedarf löschen und neu aufbauen zu können

## Inhalt

- `docs/`
  - lokale Deploymentspezifikationen und Zuordnungsdokumente
- `scripts/`
  - Skripte für die Ausführung auf diesem Rechner

## Aktuelle Dateien

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - die vor dem Refactoring erhaltene, erweiterte Kernfassung der Authoring-Dokumente
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - aktuelle Hinweise zur lokalen MCP-Bereitstellung und Anbindung
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - Referenz auf die aktuelle Bereitstellung und den historischen Pfadvergleich
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - aktuelle Hinweise zur lokalen Workflow-Anbindung
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - lokales Synchronisationsskript

## Regel

Wenn ein Inhalt beschreibt:

- wie dieses System funktionieren sollte
  - dann gehört er nicht in `local/`
- wie diese Instanz aktuell konfiguriert ist
  - dann gehört er in `local/`
