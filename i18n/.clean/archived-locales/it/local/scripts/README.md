# Local Scripts

Qui si trovano gli **script operativi locali**.

- `*.ps1` resta l’implementazione di riferimento Windows-first
- `*.py` fornisce il percorso cross-platform per `bootstrap` / `verify` / `backup`

## Current Scripts

- `bootstrap.py`
  - inizializza in modo cross-platform il skills delivery, la native-config di Codex, la configurazione MCP di Copilot e il file `.mcp.json` del progetto
- `verify-bootstrap.py`
  - verifica in modo cross-platform che il risultato del first-run sia allineato con il repo attuale, e accetta sia il seed template-safe di `.mcp.json` sia un wiring locale già bootstrapped
- `create-git-bundle.py`
  - crea un backup `git bundle` portabile e riduce il rischio di single point of failure di un worktree puramente locale
- `git-startup.ps1`
  - risolve il canonical base branch per una nuova sessione, richiede un worktree pulito, esegue un aggiornamento esplicito in fast-forward e crea un nuovo feature branch
- `sync-skills.ps1`
  - sincronizza `registry/skills/` verso i skills targets locali
- `scan-skills.ps1`
  - esegue la scansione delle skill candidate e restituisce il risultato del controllo di adozione
- `verify-delivery.ps1`
  - verifica se la source e i consueti skills targets esistono, se sono link e se sono risolvibili
- `health-check.ps1`
  - esegue un controllo minimo di salute su registry e script
- `batch-adopt-skills.ps1`
  - sposta in blocco le skill candidate dentro `registry/skills/`
- `generate-index-entries.ps1`
  - genera da `registry/skills/` il blocco di catalogo necessario per `INDEX`
- `rollback-skills.ps1`
  - ripristina una skill specifica dai backup `ops/history/adopt_*`
- `export-review-package.ps1`
  - esporta in `ops/review-package/` la cover note, gli highlights, i documenti centrali, le voci selezionate del registry e gli script minimi necessari per la review esterna
- `export-template-package.ps1`
  - esporta in `ops/template-package/` docs template-safe, generic examples e starter layout
- `verify-template-package.ps1`
  - verifica che il template package esportato contenga la struttura starter necessaria e non includa contenuti review-only o local-only
- `verify-workspace-boundaries.ps1`
  - verifica che le tracked shared surfaces dell’attuale repo di authoring non mescolino live workspace metadata, authoring-only docs o operations state
- `get-publishability-report.ps1`
  - aggrega le modifiche local-only / ops / shared-surface del branch attuale con il risultato del boundary verify per produrre un report locale di push suitability
- `lib/workspace-sensitive-metadata.ps1`
  - carica il file condiviso `WORKSPACE_SENSITIVE_METADATA_RULES.json` affinché le verifiche di boundary, template e publishability usino lo stesso set di regole
- `validate-workspace-sensitive-metadata-rules.ps1`
  - valida struttura, compilazione delle regex e casi incorporati del file condiviso `WORKSPACE_SENSITIVE_METADATA_RULES.json`
- `preview-renormalize.ps1`
  - esegue solo un dry-run per mostrare in anteprima quanti tracked files verrebbero toccati da `git add --renormalize .`, così da valutare prima il blast radius di una pulizia dei line endings
- `run-renormalize.ps1`
  - esegue un renormalize controllato per scope `repo / root / registry / i18n / local / template`; il default resta il dry-run, solo `-Apply` mette in stage le modifiche e un guard `MaxFiles` limita la dimensione del batch
- `audit-i18n-drift.py`
  - legge `i18n/manifest.json`, elenca per ogni locale quali documenti ufficiali sono mancanti, obsoleti o ancora non tracciati da Git, e supporta `json / markdown`, filtri per `locale / source-doc` e output diretto verso un workboard
- `export-rebuild-project.ps1`
  - ricostruisce il repo attuale come fresh-project baseline rinominabile e reinizializzabile, esportandolo in `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - oltre alla validazione del template package, conferma la presenza della guida di rebuild e del punto di ingresso fresh-project

## Governance Note

- Sia `sync-skills.ps1` sia `batch-adopt-skills.ps1` devono rispettare:
  - dry-run first
  - backup before mutation
  - generazione di log tracciabili

## Platform Note

- Il nuovo percorso di first-run deve privilegiare `bootstrap.py` e `verify-bootstrap.py`.
- `sync-skills.ps1` resta l’implementazione di riferimento Windows PowerShell e il modello di governance.
