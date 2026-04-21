# UniText — Pacchetto di revisione esterna

> Stato: Active Baseline  
> Uso: definire cosa deve vedere la revisione esterna, cosa no e come generare il review package in modo ripetibile.

## 1. Scopo

`UniText` è già arrivato a un baseline adatto alla revisione esterna, ma il focus della review deve rimanere su:

- l’architettura centrale
- la canonical registry
- il modello di sicurezza delle operations
- le shared resources selezionate, sufficienti a rappresentare la direzione del progetto

L’obiettivo di questo documento è raccogliere questi elementi in un review package ripetibile, non consegnare l’intero workspace dell’autore così com’è.

## 2. Ordine di lettura consigliato

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

Per vedere esempi di risorse reali, guarda poi:

- il core `8 + 4` di `registry/skills/`
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- gli script minimi di governance e i file per il first-run cross-platform in `local/scripts/`

## 3. Ambito della review

Il review package dovrebbe includere:

- documenti centrali
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
  - `../reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- file minimi di governance
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- script minimi di governance
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
- shared resources selezionate
  - il core `8 + 4` in `registry/skills/`
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Fuori ambito

I seguenti contenuti non dovrebbero essere il centro della revisione esterna:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- mapping di path locali specifici e residui dell’ambiente personale
- candidate skills non incluse nella shortlist
- contenuti non tracciati o sperimentali

authoring notes and review archives è materiale di riferimento per l’autore, non una canonical review source.

## 5. Comando di export

Nel root del repository esegui:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

Output predefinito:

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

Per fare solo una verifica senza scrivere file:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validazione

Prima dell’export, è consigliato almeno un passaggio di:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Per verificare che la delivery delle canonical skills sia allineata:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Interpretazione attuale

Al 2026-03-24, `UniText` dispone di:

- cover note e highlights per i reviewer
- documenti centrali leggibili per la review esterna
- il set `8 + 4` di skills selezionate
- seed per agent / workflow e un baseline MCP eseguibile
- un flusso ripetibile per produrre il review package
- `bootstrap -> verify` cross-platform
- un flusso di backup portabile con `git bundle`

La posizione più corretta, oggi, è:

**external-review-ready baseline**

e non:

**fully generalized release template**
