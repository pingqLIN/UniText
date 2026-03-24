# UniText — External Review Package

> Status: Active Baseline  
> Zweck: Definiert, was externe Reviewer sehen sollen, was nicht, und wie sich ein Review Package wiederholbar erzeugen lässt.

## 1. Zweck

`UniText` befindet sich bereits in einer Baseline, die für externe Reviews geeignet ist. Der Review-Fokus soll aber auf Folgendem liegen:

- ist die Kernarchitektur sinnvoll
- ist das kanonische Registry tatsächlich umgesetzt
- ist das Operations-Sicherheitsmodell ausführbar
- reichen die ausgewählten Shared Resources aus, um die Stoßrichtung des Projekts zu repräsentieren

Dieses Dokument fasst diese Inhalte zu einem wiederholbar erzeugbaren Review-Paket zusammen, statt den gesamten Author-Workspace unverändert herauszugeben.

## 2. Empfohlene Lesereihenfolge

Externe Reviewer sollten in dieser Reihenfolge lesen:

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

Wenn echte Ressourcenbeispiele betrachtet werden sollen, geht es weiter mit:

- der `8 + 4`-Topliste in `registry/skills/`
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- den minimalen Governance-Skripten und den Cross-Platform-First-Run-Skripten in `local/scripts/`

## 3. Review Scope

Das Review Package sollte aktuell folgende Inhalte enthalten:

- Kerndokumente
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- minimale Governance-Dateien
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- minimale Governance-Skripte
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- ausgewählte Shared Resources
  - die `8 + 4`-Topliste in `registry/skills/`
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

Folgende Inhalte sollen nicht Hauptgegenstand des externen Reviews sein:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- lokale path mappings und persönliche Umgebungsreste
- nicht in die Shortlist aufgenommene Kandidaten-Skills
- nicht getrackte oder experimentelle Inhalte

`local/docs/authoring/` ist Arbeitsreferenz des Autors und keine kanonische Review-Quelle.

## 5. Export Command

Im Repo-Root ausführen:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

Standardausgabe:

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

Wenn du nur prüfen willst, ohne Dateien zu schreiben:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

Vor dem Export sollte mindestens einmal Folgendes laufen:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Wenn du die kanonische Skills-Delivery-Ausrichtung prüfen willst:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Aktuelle Einordnung

Stand 2026-03-24 verfügt `UniText` über:

- reviewer-facing Cover Note und Highlights Summary
- externe Review-fähige Kerndokumente
- die `8 + 4`-Topliste der Skills
- Agent- / Workflow-Seeds und ein ausführbares MCP-Baseline-Modell
- einen wiederholbar erzeugbaren Review-Paket-Workflow
- einen Cross-Platform-`bootstrap -> verify`-Pfad
- einen portablen `git bundle`-Backup-Pfad

Damit ist die passendste Einordnung derzeit:

**external-review-ready baseline**

und nicht:

**fully generalized release template**
