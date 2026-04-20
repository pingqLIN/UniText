# UniText — Pacchetto di rilascio template

> Stato: Active Baseline  
> Uso: definire gli obiettivi del template release cleanup, il perimetro e il flusso di export ripetibile.

## 1. Scopo

Il template release di `UniText` non deve essere un dump del workspace dell’autore, ma un package che:

- conserva architettura e specifiche centrali
- conserva gli esempi minimi utili
- esclude gli artifact local-only
- esclude i residui storici di governance
- può essere forkato o clonato e ampliato da altri

La posizione del package è:

**starter template**

e non:

**authoring workspace snapshot**

## 2. Contenuti da includere

Il template package dovrebbe includere:

- documenti centrali
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
- config root template-safe
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
- metadata di rilascio
  - `manifest.json`
  - `release.json`

## 3. Contenuti da escludere

Il template package non dovrebbe includere:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- path assoluti della macchina, account personali e home directory
- documenti specifici della review
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Comando di export

Nel root del repository esegui:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

Output predefinito:

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

Per fare solo una verifica senza scrivere file:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

Per verificare il package esportato:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

Dopo l’export, il primo percorso consigliato per un nuovo utente è:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Interpretazione dell’export

Il template package esportato rappresenta:

- il contratto centrale di UniText
- un layout starter pulito
- un piccolo set di esempi generici

Non rappresenta:

- lo stato di lavoro completo dell’autore
- tutte le skills adottate
- tutte le prove di review / audit
- il wiring locale già completato

## 6. Interpretazione attuale

Al 2026-03-24, `UniText` dispone di:

- review package esterno
- documenti entry per reviewer
- baseline di template release cleanup
- script per esportare ripetutamente il template package
- skeleton dell’overlay locale starter
- script di verifica del template package
- metadata di rilascio
- script cross-platform per il first-run
- flusso di backup portabile con bundle

La lettura più corretta oggi è:

**template release candidate**

e non:

**authoring workspace snapshot**
