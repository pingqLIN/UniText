# UniText — Meilensteine

> Status: Aktiv
> Zweck: Definiert quantifizierbare Abschlusskriterien, die sowohl für externe Reviews als auch für interne Umsetzung gelten.

## Phase 1 — Skills Registry Online

- `registry/skills/` ist angelegt
- mindestens 5 Skills haben eine kanonische Adoption abgeschlossen
- `INDEX.md` enthält passende Catalog Entries
- `local/scripts/sync-skills.ps1` zeigt auf `registry/skills`
- `local/scripts/verify-delivery.ps1` kann Source- und Target-Status der Skills verifizieren
- `local/scripts/health-check.ps1` besteht die Basisprüfung

## Phase 2 — Full Registry Baseline

- `registry/agents/` ist angelegt
- `registry/mcp/` enthält mindestens ein nicht-leeres Beispiel, das lesbar bleibt
- `registry/workflow/` hat mindestens einen formal gelisteten Catalog Entry
- `scan` / `verify` / `sync` werden jeweils von minimalen Tools unterstützt
- `CLI_COMPAT_MATRIX.md` dokumentiert das aktuelle CLI-Verhalten und das letzte Verifikationsdatum

## Phase 3 — External Review Ready

- Git-Repository ist initialisiert
- `.gitignore` schließt local-only und große historische Artefakte aus
- `README.md`, `INDEX.md` und `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` sind konsistent
- `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md` definiert Review-Umfang, Lesereihenfolge und Ausschlüsse
- `docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md` und `docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md` sind als reviewer-facing entry docs nutzbar
- `SECRET_HANDLING_GUIDELINES.md` definiert die Governance-Grenzen und ist in die Kernlesereihenfolge aufgenommen
- `local/scripts/export-review-package.ps1` kann ein Review Package wiederholbar erzeugen
- es gibt einen plattformübergreifenden `bootstrap -> verify`-Pfad für den ersten Start
- externe Reviewer sehen direkt:
  - Kerndokumente der Architektur
  - die adoptierten kanonischen Skills
  - minimale Operations-Skripte
  - klare Meilensteine für die nächste Phase

## Phase 4 — Template Release Ready

- local-only artifacts gelangen nicht in das Veröffentlichungs-Paket
- der Template-Export-Prozess ist dokumentiert
- `TEMPLATE_RELEASE_PACKAGE.md` und `TEMPLATE_RELEASE_CHECKLIST.md` existieren
- `local/scripts/export-template-package.ps1` kann ein Starter Package wiederholbar erzeugen
- `local/scripts/verify-template-package.ps1` kann die Struktur des Starter Packages verifizieren
- `SECRET_HANDLING_GUIDELINES.md` ist in das Starter Package aufgenommen
- `local/scripts/create-git-bundle.py` kann ein portables Backup-Artefakt erzeugen
- es gibt template-safe generic examples für `skills`, `mcp`, `agents` und `workflow`
- es gibt ein template-safe `local/`-Skeleton
- `mcp` hat mindestens ein wirklich ausführbares Baseline-Element
- die Abdeckung der kanonischen Ressourcen wächst weiter in Richtung `skills`, `mcp`, `agents`, `workflow`
- mindestens 2 CLIs haben die Delivery-Verifikation tatsächlich bestanden
