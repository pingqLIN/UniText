# Local Scripts

Qui si trovano gli **script operativi locali**.

- `*.ps1` conserva la reference implementation Windows-first
- `*.py` offre i percorsi cross-platform per bootstrap / verify / backup

## Script attuali

- `bootstrap.py`
  - inizializza in modo cross-platform la delivery delle skills, il native-config di Codex e il `.mcp.json` del progetto
- `verify-bootstrap.py`
  - controlla in modo cross-platform che il first-run sia allineato al repo corrente
- `create-git-bundle.py`
  - crea un backup portabile in formato `git bundle`, riducendo il rischio di dipendere solo dal working tree locale
- `sync-skills.ps1`
  - sincronizza `registry/skills/` verso i target locali delle skills
- `scan-skills.ps1`
  - scansiona le candidate skills e produce i risultati della checklist di adozione
- `verify-delivery.ps1`
  - verifica che source e target comuni delle skills esistano, siano link o siano risolvibili
- `health-check.ps1`
  - esegue il controllo minimo di salute su registry e script
- `batch-adopt-skills.ps1`
  - migra in blocco le candidate skills dentro `registry/skills/`
- `generate-index-entries.ps1`
  - genera il blocco catalog necessario per `INDEX.md` a partire da `registry/skills/`
- `rollback-skills.ps1`
  - ripristina una skill specifica da un backup `ops/history/adopt_*`
- `export-review-package.ps1`
  - esporta in `ops/review-package/` cover note, highlights, documenti centrali, entry selezionate del registry e script minimi necessari alla review esterna
- `export-template-package.ps1`
  - esporta documenti template-safe, generic examples e starter layout in `ops/template-package/`
- `verify-template-package.ps1`
  - verifica che il template package esportato contenga la struttura starter necessaria e non includa contenuti solo per review o solo locali

## Nota di governance

- `sync-skills.ps1` e `batch-adopt-skills.ps1` devono rispettare:
  - dry-run prima di tutto
  - backup prima di ogni mutation
  - log tracciabili

## Nota di piattaforma

- il percorso first-run consigliato ora usa `bootstrap.py` e `verify-bootstrap.py`
- `sync-skills.ps1` resta come reference implementation per Windows PowerShell e come esempio di governance

