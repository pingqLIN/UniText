# UniText — Template Release Package

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
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
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
- `local/docs/authoring/`
- `local/docs/PATH_MAP.md`
- reale Benutzernamen, Home-Verzeichnisse und absolute Pfade
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

Nach dem Export ist der empfohlene First-Run-Pfad für neue Nutzer:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Interpretation des Exports

Ein exportiertes Template Package steht für:

- den kanonischen Vertrag von UniText
- ein sauberes Starter-Layout
- eine minimale Menge generischer Beispiele

Es steht nicht für:

- den vollständigen aktuellen Arbeitsstand des Autors
- alle adoptierten Skills
- alle Review- / Audit-Belege
- die vollständig eingerichtete lokale Delivery-Verdrahtung

## 6. Aktuelle Einordnung

Stand 2026-03-24 verfügt `UniText` über:

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
