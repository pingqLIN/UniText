# Lokale Skripte

Hier liegen die **lokalen Betriebsskripte**.

- `*.ps1` bleibt die Windows-first-Referenzimplementierung
- `*.py` liefert den plattformübergreifenden Pfad für `bootstrap` / `verify` / `backup`

## Aktuelle Skripte

- `bootstrap.py`
  - plattformübergreifende Initialisierung von Skills-Delivery, Codex native config und projektlokaler `.mcp.json`
- `verify-bootstrap.py`
  - plattformübergreifende Prüfung, ob das First-Run-Ergebnis mit dem aktuellen Repo übereinstimmt
- `create-git-bundle.py`
  - erstellt ein portables `git bundle`-Backup und reduziert das Single-Point-of-Failure-Risiko eines reinen lokalen Worktrees
- `sync-skills.ps1`
  - synchronisiert `registry/skills/` auf die lokalen Skills-Ziele
- `scan-skills.ps1`
  - scannt Kandidaten-Skills und gibt das Adoption-Prüfergebnis aus
- `verify-delivery.ps1`
  - prüft, ob Source und die üblichen Skills-Ziele existieren, ob sie Links sind und ob sie auflösbar sind
- `health-check.ps1`
  - führt einen Minimal-Health-Check für Registry und Skripte aus
- `batch-adopt-skills.ps1`
  - verschiebt Kandidaten-Skills stapelweise nach `registry/skills/`
- `generate-index-entries.ps1`
  - erzeugt aus `registry/skills/` den Catalog-Block für den `INDEX`
- `rollback-skills.ps1`
  - stellt einen bestimmten Skill aus `ops/history/adopt_*`-Backups wieder her
- `export-review-package.ps1`
  - exportiert die für externe Reviews benötigten Cover Note, Highlights, Kerndokumente, ausgewählte Registry-Einträge und minimale Skripte nach `ops/review-package/`
- `export-template-package.ps1`
  - exportiert template-safe Docs, generic examples und das Starter-Layout nach `ops/template-package/`
- `verify-template-package.ps1`
  - prüft, ob das exportierte Template Package die nötige Starter-Struktur enthält und keine review-only- oder local-only-Inhalte mitbringt

## Governance-Hinweis

- `sync-skills.ps1` und `batch-adopt-skills.ps1` müssen beide Folgendes einhalten:
  - zuerst dry-run
  - backup vor jeder Mutation
  - nachvollziehbares Log erzeugen

## Plattformhinweis

- Der neue First-Run-Pfad soll vorrangig `bootstrap.py` und `verify-bootstrap.py` verwenden.
- `sync-skills.ps1` bleibt als Windows PowerShell-Referenzimplementierung und Governance-Vorlage erhalten.
