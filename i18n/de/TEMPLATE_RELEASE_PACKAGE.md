# UniText — Template Release Package

## 2026-03-27 Synchronisierungshinweis

Für diese Übersetzung gelten die folgenden release-boundary Regeln als current baseline:

- in ein öffentliches Package dürfen nur öffentlich redistributable skills aufgenommen werden
- wenn shared skills aufgenommen werden, sollten sie `SOURCE.yaml` oder gleichwertige Provenance-Daten mitliefern
- `local-only validation materials` sowie `proprietary / restricted-license skills` dürfen nicht in das öffentliche Package
- wenn sich Authoring-Workspace und Export unterscheiden, ist das exported package die release truth

Bei Abweichungen gilt der [englische Leitfaden](../../TEMPLATE_RELEASE_PACKAGE.md) als authoritative version.

> Status: Active Baseline  
> Zweck: Definiert Ziel, Umfang und wiederholbaren Exportfluss für die Template-Bereinigung.

## 1. Zweck

`UniText`-Template-Release sollte nicht den kompletten Author-Workspace unverändert verpacken, sondern eine Ausgabe liefern, die:

- die Kernarchitektur und die Specs beibehält
- minimale nutzbare Beispiele enthält
- local-only state ausschließt
- historische Governance-Reste ausschließt
- für andere Personen geeignet ist, um zu fork / clone und selbst zu erweitern

Diese Package ist positioniert als:

**starter template**

und nicht als:

**authoring workspace snapshot**

## 2. Enthalten

Das Template Package sollte aktuell enthalten:

- Kerndokumente
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `SKILLS_PUBLIC_RELEASE_POLICY.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
  - `.mcp.json`
  - `.claude/settings.json`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- öffentlich lizenzierte und redistributable skills
  - nur Skill-Entries, deren Lizenzgrenze für öffentliche Packages geklärt ist
  - wenn shared skills enthalten sind, sollen sie `SOURCE.yaml` oder gleichwertige Herkunftsdaten mitliefern
- runnable MCP baseline
  - `registry/mcp/claude-project-mcp-seed/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- release metadata
  - `manifest.json`
  - `release.json`

## 3. Ausschließen

Das Template Package soll nicht enthalten:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- reale Benutzernamen, Home-Verzeichnisse und absolute Pfade
- local-only validation materials
  - skills oder Hilfsmaterialien, die für Dry-Run / Authoring-Validierung genutzt werden, aber nicht öffentlich redistributable sind
- proprietary / restricted-license skills
  - Skill-Dateien oder Assets, deren Lizenzgrenze keine öffentliche Redistribution erlaubt oder nicht eindeutig klärt
- review-spezifische Dokumente
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Export Command

Im Repo-Root ausführen:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

Standardausgabe:

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

Wenn du nur prüfen willst, ohne zu schreiben:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

Wenn du das exportierte Paket verifizieren willst:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

Wenn du statt eines allgemeinen Template-Packages direkt ein neues Starter-Projekt exportieren willst:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-rebuild-project.ps1 -Path .\ops\rebuild-project\<package-name>
```

Nach dem Export ist der empfohlene First-Run-Pfad für neue Nutzer:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

Wenn dein System nur `python3` bereitstellt, ersetze `python` durch `python3`.

## 5. Interpretation des Exports

Ein exportiertes Template Package steht für:

- den kanonischen Vertrag von UniText
- ein sauberes Starter-Layout
- eine minimale Menge generischer Beispiele
- einen wiederholbaren cross-platform `bootstrap -> verify`-Pfad
- eine `.claude/settings.json`, die Claude direkt lesen kann
- einen `.mcp.json`-Seed für project-local MCP
- eine shared baseline, an die ein zukünftiger Copilot-CLI-Adapter anschließen kann
- template-safe, öffentlich redistributable skills / examples
  - wenn etwas mehr als `example-skill` enthalten ist, soll es auf einen klaren Upstream zurückführbar sein

Es steht nicht für:

- den vollständigen aktuellen Arbeitsstand des Autors
- alle adoptierten Skills
- alle maintainer-lokalen Validierungsmaterialien
- alle Review- / Audit-Belege
- die vollständig eingerichtete lokale Delivery-Verdrahtung
- bereits auf jeder Maschine abgeschlossene Interpreter-Pinning-Arbeit

## 5.1 Skills Release Rule

Für den Template Release gelten bei Skills diese Regeln:

- öffentlich redistributable skills dürfen in das Package
- wenn aktive shared skills enthalten sind, sollen sie Herkunftsdaten mitliefern
- Skills mit unklarer oder eingeschränkter Lizenz dürfen nicht in das Package
- local-only validation materials dürfen im Authoring-Workspace existieren, aber nicht Teil des öffentlichen Packages werden

Wenn ein Dry-Run oder eine Validierung lokal andere Skills genutzt hat, darf die Dokumentation festhalten:

- dass die Validierung lokal erfolgreich durchgeführt wurde
- dass die betreffenden Materialien wegen Lizenz- oder Release-Boundary-Gründen nicht im öffentlichen Package enthalten sind

Die Dokumentation darf aber nicht den Eindruck erzeugen, dass:

- diese Skills im öffentlichen Package enthalten seien
- UniText diese Skills selbst öffentlich weiterverteilen dürfe

## 6. Aktuelle Einordnung

Stand 2026-03-27 verfügt `UniText` über:

- ein External Review Package
- reviewer-facing Entry Docs
- eine Baseline für die Template Release Bereinigung
- ein wiederholbar erzeugbares Export-Skript für Template Packages
- ein Starter-Skeleton für das lokale Overlay
- ein Verifikationsskript für Template Packages
- Release-Metadaten
- Cross-Platform-First-Run-Skripte
- einen portablen Bundle-Backup-Flow

Daher ist die passendste Einordnung:

**template release candidate**

und nicht:

**authoring workspace snapshot**

