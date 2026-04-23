# Lokale Skripte

Hier liegen die **lokalen Betriebsskripte**.

- `*.ps1` bleibt die Windows-first-Referenzimplementierung
- `*.py` liefert den plattformübergreifenden Pfad für `bootstrap` / `verify` / `backup`

## Aktuelle Skripte

- `bootstrap.py`
  - initialisiert plattformübergreifend Skills-Delivery, Codex native-config, Copilot MCP config und die projektlokale `.mcp.json`
- `verify-bootstrap.py`
  - prüft plattformübergreifend, ob das First-Run-Ergebnis zum aktuellen Repo passt, und akzeptiert sowohl die template-safe `.mcp.json`-Seed-Datei als auch lokal bootstrapped wiring
- `create-git-bundle.py`
  - erstellt ein portables `git bundle`-Backup und reduziert das Single-Point-of-Failure-Risiko eines reinen lokalen Worktrees
- `git-startup.ps1`
  - löst für eine neue Session den canonical base branch auf, verlangt einen sauberen Worktree, führt ein explizites Fast-Forward-Update aus und erstellt einen neuen Feature-Branch
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
- `verify-workspace-boundaries.ps1`
  - prüft, ob die tracked shared surfaces im aktuellen Authoring-Repo live workspace metadata, authoring-only docs oder operations state enthalten
- `get-publishability-report.ps1`
  - fasst local-only-, ops- und shared-surface-Änderungen der aktuellen Branch mit dem Ergebnis der Boundary-Prüfung zu einem lokalen Bericht für Push-Suitability zusammen
- `lib/workspace-sensitive-metadata.ps1`
  - lädt die gemeinsame `WORKSPACE_SENSITIVE_METADATA_RULES.json`, damit Boundary-, Template- und Publishability-Prüfungen dieselben Regeln nutzen
- `validate-workspace-sensitive-metadata-rules.ps1`
  - validiert Struktur, kompilierbare Regexe und eingebaute Fälle der gemeinsamen `WORKSPACE_SENSITIVE_METADATA_RULES.json`
- `preview-renormalize.ps1`
  - führt nur einen Dry-Run aus und zeigt vorab, wie viele tracked files `git add --renormalize .` berühren würde, damit der Blast Radius eines Line-Ending-Cleanups zuerst sichtbar wird
- `run-renormalize.ps1`
  - führt kontrolliertes Renormalisieren nach `repo / root / registry / i18n / local / template`-Scope aus; standardmäßig bleibt es beim Dry-Run, nur mit `-Apply` werden Änderungen gestaged, und ein `MaxFiles`-Guard schützt vor zu großen Batches
- `audit-i18n-drift.py`
  - liest `i18n/manifest.json`, listet pro Locale fehlende, veraltete oder von Git noch nicht verfolgte Übersetzungen auf und unterstützt `json / markdown`, Filter nach `locale / source-doc` sowie die Ausgabe eines Arbeitsberichts
- `export-rebuild-project.ps1`
  - exportiert das aktuelle Repo als fresh-project baseline, die neu benannt und neu initialisiert werden kann, nach `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - bestätigt zusätzlich zur Template-Package-Prüfung, dass Rebuild-Guide und Fresh-Project-Einstieg vorhanden sind

## Governance-Hinweis

- `sync-skills.ps1` und `batch-adopt-skills.ps1` müssen beide Folgendes einhalten:
  - zuerst dry-run
  - backup vor jeder Mutation
  - nachvollziehbares Log erzeugen

## Plattformhinweis

- Der neue First-Run-Pfad soll vorrangig `bootstrap.py` und `verify-bootstrap.py` verwenden.
- `sync-skills.ps1` bleibt als Windows PowerShell-Referenzimplementierung und Governance-Vorlage erhalten.
