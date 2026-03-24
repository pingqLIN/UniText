# UniText — Modalità di Progetto

> Stato: Template Base
> Obiettivo: distinguere tra repository di authoring e starter/template distribuito all’esterno.

## 1. Due modalità

### Local Development Project

Usato dall’autore per sviluppo continuo, adozione, correzione e governance.

Può includere:

- inventories
- backups
- drift logs
- migration artifacts
- note specifiche della piattaforma

### Project Template

Usato per permettere ad altri di inizializzare la propria istanza di `UniText`.

Dovrebbe includere:

- contratti logici
- documentazione centrale
- esempi minimi
- regole indipendenti dalla piattaforma

Non dovrebbe includere:

- path assoluti locali
- tracce personali d’uso
- snapshot di backup
- drift history
- valori predefiniti legati a un solo deployment

## 2. Regola pratica

Se un contenuto descrive:

- come `UniText` dovrebbe funzionare
  - allora va meglio nel `Project Template`
- come è configurato attualmente il workspace dell’autore
  - allora va meglio nel `Local Development Project`

## 3. Regola di pubblicazione

Quando si pubblica un template:

1. mantenere la documentazione centrale e gli esempi template-safe
2. rimuovere gli artifacts di stato locali
3. rimuovere valori specifici di path / account / macchina
4. riscrivere la reference implementation come esempi astratti

