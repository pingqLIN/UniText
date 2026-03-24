# UniText — Visione

> Stato: Template Base
> Principio: usare contratti logici, non assumere come precondizione alcun singolo sistema operativo, struttura di cartelle o modalità di deployment.

## 1. Cos’è UniText

`UniText` è un shared resource hub text-native, registry-first e AI-first, pensato per permettere a più sistemi AI CLI / agent di condividere definizioni e modalità di adozione tramite un unico contratto testuale.

Si compone di due livelli:

1. `Registry`
   - definisce shared resources, canonical identity e contratto minimo
2. `Adapter / Operations Control Plane`
   - collega il contenuto del registry ai diversi CLI e gestisce install, sync, adopt e repair

## 2. Problema che risolve

UniText affronta la frammentazione tipica della condivisione di risorse tra strumenti diversi:

- skills sparse in punti diversi
- definizioni MCP distribuite in formati di configurazione differenti
- istruzioni per gli agent non riutilizzabili
- convenzioni di workflow difficili da mantenere tra tool diversi
- assenza di un’interfaccia testuale comune, facile da leggere per AI e persone

## 3. Posizionamento architetturale

**Registry-first, adapter-enabled, operations-governed**

Principi chiave:

- senza registry non esistono origine comune e semantica comune
- senza adapter il registry non può arrivare davvero ai vari CLI
- l’AI è un consumer e un collaboratore importante, ma non l’unico meccanismo affidabile di integrazione

## 4. Tipi di risorsa

Tipi shared resource predefiniti:

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` non è un shared resource type e deve restare separato in `/operations`.

## 5. Discovery e delivery

`INDEX.md` gestisce discovery e risponde a:

- quali risorse esistono
- dove si trova il percorso logico di ciascuna
- quali CLI sono supportati

`OPERATIONS.md` gestisce delivery e risponde a:

- come un certo CLI ottiene le risorse
- quando eseguire install, sync, adopt e repair
- come viene risolto il delivery mode

Delivery modes disponibili:

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Trigger di delivery

Il delivery può partire solo da trigger espliciti:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

Le operazioni distruttive devono sempre rispettare:

- dry-run prima di tutto
- backup prima di ogni mutation
- nessuna decisione silenziosa sulla canonical source

## 7. Modello di adozione

### Soft Adoption

- introdurre prima il discovery
- non forzare subito la migrazione di risorse esistenti

### Formal Adoption

Flusso formale:

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

Se esistono risorse con stesso nome ma contenuto diverso, il flusso deve fermarsi in `REVIEW / DRY-RUN`.

## 8. Set di documentazione

Documenti centrali:

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Strategia dei path

I documenti principali usano logical canonical paths, per esempio:

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

I path assoluti e le impostazioni specifiche della piattaforma appartengono solo al deployment mapping, non al contratto di visione.

## 10. Principi di design

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. Posizionamento in una frase

> UniText è un shared resource hub text-native, registry-first e AI-first che, tramite adapter chiari e un operations control plane, consente a più AI CLI di scoprire, adottare e condividere in sicurezza gli stessi canonical resources.

