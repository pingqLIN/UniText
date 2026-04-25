# UniText — Linee guida per la gestione dei secret

> Stato: Draft  
> Ruolo: definire i confini di archiviazione, i principi operativi e le regole di documentazione per password, API key, token e altri sensitive material.

## 1. Scopo

Questo documento risponde a domande come:

- quali dati vanno considerati secret
- dove non dovrebbero essere memorizzati i secret
- come registrare in UniText posizione e stato di un secret
- quando usare la CLI config e quando invece un OS secret store o un native helper

Non definisce l’implementazione finale di un prodotto specifico; definisce i confini di governance che UniText deve rispettare.

## 2. Definizione di secret

I seguenti elementi sono sempre considerati `secret` o `sensitive material`:

- password
- passphrase
- API key
- access token
- refresh token
- session token
- private key
- OAuth client secret
- cookie / session credential
- qualsiasi bearer credential che rappresenti l’identità dell’utente o del sistema

I seguenti elementi in genere non sono secret, ma possono comunque essere sensitive metadata:

- endpoint URL
- model name
- provider name
- account email
- stato di feature toggle
- stato key exists / missing
- data dell’ultimo aggiornamento della key

## 3. Principio base

I principi fondamentali di UniText sono:

1. `registry/` non deve contenere secret
2. `ops/` non deve contenere secret riutilizzabili
3. `local/` può registrare path, adapter e note di deployment, ma non secret in chiaro
4. i secret veri dovrebbero stare prima di tutto in un OS-level secret store
5. se non è possibile usare subito un OS secret store, i secret devono essere separati dalle configurazioni normali

In breve:

- `registry` è shared truth, non un secret vault
- `ops` è audit trail, non un credential archive
- `local` è un wiring overlay, non un archivio di testo in chiaro

## 4. Policy di storage per layer

| Layer | Can store secret? | Guidance |
|---|---|---|
| `registry/` | No | solo definizioni canoniche, schema, hint dell’adapter e metadata della risorsa |
| `ops/` | No | solo log redatti, metadata di backup, drift report e stato inventory |
| docs in `local/` | No | puoi documentare il tipo di storage del secret, non il secret stesso |
| CLI config | Conditional | solo se la CLI supporta nativamente secret basati su config e il rischio è accettabile |
| OS secret store | Yes | preferito; per esempio Windows DPAPI / Credential Manager, macOS Keychain, Linux Secret Service |
| in-memory session | Yes | accettabile come runtime material decrittato per breve tempo, non come unica fonte persistente |

## 5. Pattern approvati

### 5.1 Best pattern

Adatto a estensioni commerciali, tool desktop e adapter cross-CLI:

- le impostazioni non sensibili stanno in una normale config / storage
- i secret stanno nell’OS secret store
- all’avvio del runtime vengono iniettati nella memory del processo
- l’interfaccia mostra solo `stored / missing / last updated`, senza reinserire il valore in chiaro

### 5.2 Fallback accettabile

Se non esiste ancora un’integrazione con l’OS secret store:

- ogni provider / account deve avere il proprio secret separato
- i secret devono restare separati dalle impostazioni ordinarie
- content script / renderer / contesti non fidati non devono poter leggere direttamente
- audit ed export devono mostrare solo stato redatto
- il documento deve segnalarlo come `interim storage model`

### 5.3 Non accettabile

Non sono considerati conformi:

- scrivere la API key in `registry/`
- scrivere token in `ops/history/`
- incollare chiavi complete nelle note di deployment
- mescolare secret e impostazioni normali senza redaction
- includere chiavi reali nei review package o nei template package

## 6. Regole per registrare la posizione

I documenti possono registrare in quale layer si trova un secret, ma non il suo valore.

Esempi consentiti:

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- impostazioni non sensibili in `%USERPROFILE%\\.codex\\config.toml`
- `chrome.storage.local` solo per provider settings non sensibili
- `chrome.storage.session` per runtime material a breve durata

Esempi non consentiti:

- token completo
- API key completa
- header Authorization completo
- cookie riutilizzabile in forma integrale

## 7. Regole di documentazione

Quando un documento deve parlare di secret handling:

1. documenta solo la classe di storage, non il valore
2. usa solo esempi redatti
3. se un esempio è necessario, usa valori fittizi espliciti, ad esempio:

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. se un sistema può usare solo una modalità più debole, il documento deve indicare:
   - che si tratta di una soluzione temporanea
   - quali sono i rischi noti
   - quale sia il percorso di upgrade previsto

## 8. Regole di audit ed export

Qualsiasi review package, template package, export di inventory o ops snapshot deve:

- rimuovere il valore dei secret
- rimuovere le credential riutilizzabili
- conservare solo lo stato necessario e redatto

È consentito conservare:

- provider name
- endpoint
- key exists / missing
- scope o label della key
- last rotated at
- tipo di storage backend

## 9. Scala di priorità consigliata

L’ordine di preferenza di UniText per l’archiviazione dei secret è:

1. `OS secret store`
   - Windows: DPAPI / Credential Manager
   - macOS: Keychain
   - Linux: Secret Service / keyring
2. `native helper / native messaging host`
   - quando la CLI o l’estensione non possono persistere i secret in modo sicuro
3. `separated local secret store`
   - separato dalle configurazioni normali e non leggibile dai contesti non fidati
4. `runtime session only`
   - utile come supporto, ma non come strategia persistente unica

## 10. Checklist minima

Prima di introdurre una nuova risorsa o un nuovo adapter che gestisca secret, verifica almeno che:

- il secret sia escluso da `registry/`
- il secret sia escluso da `ops/`
- il documento registri solo location e stato, non il valore
- export e review package facciano redaction
- il backend di storage attuale sia documentato
- il percorso di upgrade sia documentato

## 11. Indicazioni pratiche per browser extension

Per i casi simili a una browser extension:

- i provider settings possono stare in extension local storage
- l’API key non dovrebbe essere mescolata con tutti gli altri provider settings in un unico valore condiviso
- ogni provider dovrebbe mantenere il proprio secret
- l’interfaccia dovrebbe supportare staged draft, senza perdere la key quando si cambia provider o si collassa un pannello
- per un livello di sicurezza più alto, conviene passare a native host + OS secret store, non solo all’extension storage

## 12. Posizione attuale di UniText

Ad oggi, la posizione ufficiale di UniText sulla gestione dei secret è:

- il canonical registry non contiene secret
- l’overlay locale può registrare il backend del secret e il tipo di path
- gli artifact operativi devono essere redatti
- se un’integrazione non usa ancora un OS secret store, va indicata esplicitamente come interim model

Questo documento deve essere considerato come:

- authoring guidance
- review checklist reference
- base line per future integrazioni adapter / secret-store

