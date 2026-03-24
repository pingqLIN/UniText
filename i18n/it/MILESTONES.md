# UniText — Milestone

> Stato: Active
> Obiettivo: definire condizioni quantitative di completamento condivise da revisione esterna ed esecuzione interna.

## Phase 1 — Skills Registry Online

- `registry/skills/` esiste
- almeno 5 skills hanno completato la canonical adoption
- `INDEX.md` contiene le relative catalog entries
- `local/scripts/sync-skills.ps1` punta a `registry/skills`
- `local/scripts/verify-delivery.ps1` può verificare lo stato di source e target delle skills
- `local/scripts/health-check.ps1` supera i controlli base

## Phase 2 — Full Registry Baseline

- `registry/agents/` esiste
- `registry/mcp/` ha almeno 1 esempio non vuoto e leggibile
- `registry/workflow/` ha almeno 1 catalog entry formalmente elencata
- le operazioni `scan` / `verify` / `sync` hanno un supporto minimo di strumenti
- `CLI_COMPAT_MATRIX.md` registra il comportamento dei CLI dipendenti e la data dell’ultima verifica

## Phase 3 — External Review Ready

- il repository Git è inizializzato
- `.gitignore` esclude i contenuti locali e i grossi artifact storici
- `README.md`, `INDEX.md` e `PROJECT_STATUS_REPORT_2026-03-23.md` sono allineati
- `EXTERNAL_REVIEW_PACKAGE.md` definisce ambito, ordine di lettura e contenuti esclusi
- `EXTERNAL_REVIEW_COVER_NOTE.md` e `EXTERNAL_REVIEW_HIGHLIGHTS.md` sono disponibili come entry docs per reviewer
- `SECRET_HANDLING_GUIDELINES.md` definisce i confini di governance ed è incluso nell’ordine di lettura
- `local/scripts/export-review-package.ps1` può produrre il review package in modo ripetibile
- è disponibile un percorso cross-platform `bootstrap -> verify`
- la revisione esterna può vedere direttamente:
  - i documenti architetturali centrali
  - le canonical skills adottate
  - gli script operativi minimi
  - i prossimi milestone in modo chiaro

## Phase 4 — Template Release Ready

- gli artifact locali non entrano nel pacchetto di rilascio
- il processo di export del template è documentato
- `TEMPLATE_RELEASE_PACKAGE.md` e `TEMPLATE_RELEASE_CHECKLIST.md` esistono
- `local/scripts/export-template-package.ps1` può produrre starter package in modo ripetibile
- `local/scripts/verify-template-package.ps1` può verificare la struttura dello starter package
- `SECRET_HANDLING_GUIDELINES.md` è incluso nello starter package
- `local/scripts/create-git-bundle.py` può produrre un backup artifact portabile
- esistono generic examples template-safe per `skills`, `mcp`, `agents` e `workflow`
- esiste uno skeleton `local/` template-safe
- `mcp` ha almeno un baseline realmente eseguibile
- la copertura delle canonical resources continua a espandersi su `skills`, `mcp`, `agents` e `workflow`
- almeno 2 CLI superano realmente la delivery verification

