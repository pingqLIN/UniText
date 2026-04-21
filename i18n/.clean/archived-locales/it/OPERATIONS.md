# UniText — Operations

> Stato: Template Base
> Ruolo: definire responsabilità dell’adapter / operations control plane, regole di delivery e confini di sicurezza.

Ogni delivery e mutation dovrebbe usare il contratto testuale di `UniText` come source of truth per registry e spec.

Se un’operazione tocca password, API key, token o credential, segui anche `SECRET_HANDLING_GUIDELINES.md`.

## 1. Ambito

Questo file copre:

- responsabilità degli adapter
- delivery modes
- delivery triggers
- adoption flow
- drift / repair
- mapping logico → fisico

Questo file non copre:

- lo schema dei metadata delle shared resources
- un’unica implementazione obbligatoria per ogni piattaforma
- lo stato storico dell’authoring repo locale

## 2. Delivery modes

| Mode | When to use |
|---|---|
| `pointer` | per discovery o per risorse non registrate come copia locale |
| `mirror` | quando la CLI ha bisogno di una copia locale o i symlink non sono stabili |
| `symlink` | quando serve un path fisso e l’ambiente supporta link stabili |
| `native-config` | quando la CLI offre una configurazione nativa per registrare le risorse |

Il `delivery mode` viene risolto dall’adapter durante l’operazione: non è una proprietà fissa della risorsa.

## 3. Regole di risoluzione del delivery

L’adapter dovrebbe considerare, in ordine:

1. se esiste un ingresso di configurazione nativo, usare `native-config`
2. se serve un path fisso e la piattaforma supporta i link stabili, usare `symlink`
3. se il symlink non è sicuro, usare `mirror`
4. se lo scopo principale è il discovery o un punto di ingresso, usare `pointer`

## 4. Trigger di delivery

Il delivery può partire solo da trigger espliciti:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Regole di sicurezza

### Dry-run first

Le seguenti operazioni dovrebbero produrre prima un piano di dry-run:

- `adopt`
- `repair`
- `sync` quando sovrascrive uno stato esistente

### Backup before mutation

Ogni operazione distruttiva dovrebbe avere:

- un backup o un punto di ripristino equivalente
- un record tracciabile dell’operazione
- condizioni di stop in caso di errore

### No silent canonicalization

Se trovi risorse con stesso nome ma contenuto diverso:

- fermati in review
- fai decidere esplicitamente all’operatore la canonical source

## 6. Adoption flow

1. `SCAN`
   - scansiona le fonti candidate e elenca le risorse adottabili con il loro stato di readiness
2. `REVIEW`
   - usa la checklist per verificare metadata, qualità del contenuto e validità della canonical source
3. `DRY-RUN`
   - mostra in anteprima quali target cambierebbero e se serve un backup
4. `ADOPT`
   - scrive il contenuto nella canonical location del registry; se sovrascrive, fa prima il backup
5. `DELIVER`
   - l’adapter consegna il contenuto del registry alla CLI corretta; se sovrascrive uno stato esistente, conserva log e backup
   - se la CLI supporta `native-config`, il bootstrap può scrivere una config locale alla macchina, ma la definizione canonica resta in `registry/`
6. `VERIFY`
   - verifica esistenza dei file, risoluzione dei path, delivery mode e condizioni di caricamento della CLI target

## 6.1 First-run baseline

Se l’obiettivo è far sì che un nuovo utente del template completi l’inizializzazione minima su macOS / Linux / Windows, dovresti fornire almeno:

- un `bootstrap` cross-platform
- un `verify` cross-platform
- un flusso di backup del repo portabile
- un baseline MCP realmente eseguibile

## 7. Operations state

I seguenti contenuti sono operations state, non shared resources:

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

Dovrebbero stare in `/operations` e non essere mescolati con `/registry`.

## 8. Mappatura logico-fisica

Il path logico è un contratto stabile; il path fisico dipende dal deployment.

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | fonti canoniche delle skill | cartella condivisa, sottodirectory del repo, path montato |
| `/registry/mcp` | definizioni canoniche MCP | cartella di configurazione, root del manifest generato |
| `/registry/agents` | root canonici per le istruzioni degli agent | directory dei profili agent, libreria di prompt condivisa |
| `/registry/workflow` | documenti workflow / runbook | cartella workflow, documenti locali del progetto |
| `/operations` | inventari, backup, drift log | cartella ops, state store, directory audit |

