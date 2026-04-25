# UniText — Checklist di rilascio template

> Uso: verifica rapida del cleanup minimo prima di esportare o pubblicare un template package.

## 1. Docs

- [ ] `README.md` è comprensibile anche senza il background personale dell’autore
- [ ] `INDEX.md` può funzionare come entry point di discovery
- [ ] `PROJECT_MODES.md` distingue chiaramente template e workspace di authoring
- [ ] `SECRET_HANDLING_GUIDELINES.md` definisce i confini dei secret e non contiene credential reali
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` è aggiornato
- [ ] `MILESTONES.md` riflette lo stato attuale delle phase

## 2. Cleanup Boundaries

- [ ] il template package non contiene `backup/`
- [ ] il template package non contiene `recovered_*`
- [ ] il template package non contiene `.bak_*`
- [ ] il template package non contiene `ops/history/`
- [ ] il template package non contiene documenti solo per review
- [ ] il template package non contiene path assoluti specifici della macchina

## 3. Esempi

- [ ] almeno 1 generic skill example
- [ ] almeno 1 generic agent example
- [ ] almeno 1 generic mcp example
- [ ] almeno 1 generic workflow example
- [ ] almeno 1 generic local overlay skeleton
- [ ] lo starter package include un percorso cross-platform `bootstrap -> verify`

## 4. Validation

- [ ] `health-check.ps1` passa
- [ ] `export-template-package.ps1 -DryRun` mostra il contenuto del package
- [ ] `export-template-package.ps1` produce il package con successo
- [ ] `verify-template-package.ps1` passa
- [ ] `bootstrap.py --dry-run` mostra in anteprima l’inizializzazione in un ambiente pulito
- [ ] `verify-bootstrap.py` verifica il wiring del first-run
- [ ] il package contiene `manifest.json`
- [ ] il package contiene `release.json`

## 5. Release Call

Se tutti i punti precedenti sono completati, il risultato può essere considerato:

**adatto a essere trattato come template release candidate**

Se invece restano boundary locali poco chiari, esempi incompleti o una verifica CLI insufficiente, allora il risultato resta:

**template release cleanup baseline**

