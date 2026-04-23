# UniText × skill-0 — Visione di collaborazione

> Stato: Concept Draft
> Obiettivo: definire il rapporto tra `UniText` e `skill-0`, i possibili spazi di collaborazione e ciò che manca ancora.

## 1. Executive summary

`UniText` e `skill-0` non sono progetti concorrenti o duplicati; possono invece formare una relazione upstream / downstream:

- `UniText` gestisce **registry / delivery / governance** delle shared resources
- `skill-0` prende skill di livello alto e le scompone, normalizza e generalizza in un **insieme di atomic operation**

La collaborazione più sensata non è “chi sostituisce chi”, ma:

**UniText fornisce input canonici e un contenitore governabile, skill-0 fornisce decomposizione, normalizzazione e ricomposizione.**

## 2. Due problemi diversi

### UniText

UniText risolve:

- come canonicalizzare le shared resources
- come distribuirle tra più AI CLI
- come gestire le mutation con `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY`

In breve:

**distribution / governance problem**

### skill-0

skill-0 risolve:

- quali sono le unità operative minime di una skill di livello alto
- quali step sono primitive riusabili
- quali parti del testo sono solo descrizione superficiale e quali sono operazioni centrali
- se una skill può essere ricomposta in capacità più piccole, più generiche e più portabili

In breve:

**abstraction / compiler / normalization problem**

## 3. Relazione tra i due

Dal punto di vista di skill-0, il valore più alto di UniText non è solo quello di essere un repository da distribuire, ma anche:

- una sorgente stabile di skill di livello alto
- un corpus canonico con identità logica e metadata
- un dataset che può essere analizzato, confrontato e tracciato nel tempo

Quindi la relazione è:

| Project | Primary role |
|---|---|
| `UniText` | source of truth canonica per shared resources |
| `skill-0` | analyzer / decomposer / compiler delle skill di livello alto |

In una frase:

**UniText conserva le skill, skill-0 le scompone.**

## 4. Spazio di collaborazione attuale

Anche senza modificare lo schema principale di UniText, esistono già spazi di collaborazione:

### 4.1 Usare UniText come corpus di input

skill-0 può usare direttamente:

- `registry/skills/*/SKILL.md`
- i metadata catalog di `INDEX.md`
- il contratto di identità e canonical location di `RESOURCE_SPEC.md`

Così skill-0 analizza un corpus canonico pulito, non copie sparse e incoerenti.

### 4.2 Usare UniText come staging governato

Per ora gli output di skill-0 possono restare fuori dal registry canonico ed essere salvati in:

- `/operations`
- ad esempio `ops/analysis/skill-0/`

Questo permette di:

- evitare di sporcare troppo presto lo schema delle shared resources
- verificare se il formato dell’analisi è stabile
- trattare skill-0 come pipeline di analisi, non ancora come source canonica

### 4.3 Usare il flusso di review di UniText per valutare gli output derivati

Quando skill-0 produce:

- atom maps
- set di step normalizzati
- cluster di subroutine condivise
- candidate per la ricomposizione

questi output possono essere verificati con lo stesso mindset di review di UniText:

- l’identità è stabile?
- il naming è chiaro?
- il mapping verso la skill sorgente è tracciabile?
- serve una decisione umana sulla forma canonica?

## 5. Modalità di collaborazione più probabili

### Mode A — skill-0 come analyzer esterno

skill-0 usa UniText come fonte dati e produce report di analisi, ma non scrive nulla nel registry.

Adatto per:

- validare rapidamente il metodo di decomposizione
- fare skill overlap analysis
- trovare primitive riusabili

Vantaggi:

- costo d’ingresso minimo
- quasi nessuna modifica allo schema di UniText

Limiti:

- i risultati restano artifact laterali
- è difficile trasformarli subito in shared canonical resource

### Mode B — skill-0 come generatore sidecar

skill-0 legge `registry/skills` e genera sidecar machine-readable, ad esempio:

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

Vantaggi:

- mapping esplicito tra skill e atom
- più facile da usare con tooling rispetto a un semplice report

Limiti:

- si cominciano a toccare i confini dello schema di UniText
- bisogna decidere quali sidecar sono canonici e quali sono solo generati

### Mode C — le primitives diventano una risorsa di primo livello

Se la collaborazione matura, UniText potrebbe introdurre un nuovo resource type formale, per esempio:

- `/registry/primitives`
- oppure `/registry/operations`

In questo caso gli output di skill-0 non sarebbero più solo allegati di analisi, ma shared resources reali.

Vantaggi:

- nasce un vocabolario condiviso autentico
- si può supportare la ricomposizione cross-skill

Limiti:

- bisogna aggiornare il resource model di UniText
- servono nuovi metadata spec, adoption flow e regole di verifica

## 6. Cosa manca oggi

### 6.1 Manca un type canonico per le primitive

I resource type di primo livello di UniText sono ancora solo:

- `skills`
- `mcp`
- `agents`
- `workflow`

Non esistono ancora:

- `primitives`
- `operations`
- `atoms`

Quindi il risultato più importante di skill-0 non ha ancora un contenitore di primo livello in UniText.

### 6.2 Manca uno schema metadata per le unità atomiche

`RESOURCE_SPEC.md` è adatto alle shared resources ad alto livello, ma non definisce ancora:

- atom id
- operation signature
- preconditions / postconditions
- regole di composizione
- provenienza rispetto alla skill sorgente

### 6.3 Manca un flow di adozione per gli artifact derivati

UniText ha già un adoption flow per le skills, ma non ancora un flow dedicato ai casi in cui:

- la stessa skill produce set di atom diversi
- più skill condividono primitive simili ma non identiche
- un atom è abbastanza stabile da essere canonicalizzato

### 6.4 Manca un modello di verifica

Per portare gli output di skill-0 in una collaborazione più formale bisogna poter rispondere a domande come:

- la decomposizione è stabile?
- si può fare un round-trip di ricomposizione?
- migliora davvero il riuso cross-skill?
- oppure sta solo rinominando una descrizione già esistente?

### 6.5 Manca un confine chiaro tra analysis e canon

Ancora non esiste una regola netta per distinguere:

- quali output di skill-0 sono solo analysis
- quali sono già abbastanza solidi da diventare shared resource canoniche

Finché questo confine non è chiaro, l’approccio più sicuro è tenere gli output in `ops/analysis/skill-0/`.

## 7. Direzione consigliata nel breve periodo

La direzione più ragionevole non è cambiare subito lo schema core di UniText, ma seguire una collaborazione graduale:

**Mode A -> Mode B**

### Phase A — Analysis only

Prima:

- usa `registry/skills/*/SKILL.md` come input
- produci decomposition report
- salva tutto in `ops/analysis/skill-0/`

L’obiettivo non è canonicalizzare, ma verificare:

- la stabilità dell’estrazione degli atom
- la reale presenza di skill overlap
- quali primitive vale la pena conservare

### Phase B — Stable sidecars

Quando il formato si stabilizza, introduci:

- sidecar schema
- naming rules
- collegamento alla skill sorgente
- verifiche di base

In questa fase il resource type nuovo può ancora non esistere, ma puoi già creare:

- `skill -> atoms`
- `atom -> source skills`

### Phase C — First-class primitives

Se l’analisi dimostra valore, si può discutere se aggiungere a UniText:

- `/registry/primitives`
- `/registry/operations`

Solo a quel punto ha senso aggiornare formalmente:

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Primo set di deliverable concreti

Per iniziare davvero la collaborazione, i primi output utili non sono grandi cambi architetturali, ma:

1. definire uno schema draft per l’output di skill-0
2. scegliere 1 o 2 skill del Core 8 di UniText per un sample di decomposizione
3. salvare gli output in `ops/analysis/skill-0/`
4. confrontare:
   - gli atom condivisi tra skill diverse
   - il gap tra descrizione testuale e layer atomico
   - la possibilità di ricostruire un workflow minimo utile

## 9. Interpretazione strategica

Se la collaborazione ha successo, i ruoli di lungo periodo sono chiari:

- `UniText` diventa il canonical hub delle shared AI resources
- `skill-0` diventa il motore di normalizzazione e primitive extraction delle skill

In termini di layering:

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | risultato condiviso `UniText × skill-0` |

## 10. Posizione finale

La conclusione più accurata oggi è:

**`UniText` e `skill-0` sono fortemente correlati, ma non fanno doppio lavoro.**

Uno si occupa di governance e distribuzione, l’altro di scomposizione e astrazione.

Per questo, nel breve periodo, la collaborazione più sensata non è inserire subito `skill-0` nei quattro resource type già esistenti di UniText, ma:

**lasciare che `skill-0` usi UniText come canonical input corpus e che gli output inizino in `ops/analysis/skill-0/`.**

Quando il formato, il valore e il metodo di verifica saranno stabili, si potrà decidere se promuovere il layer delle primitive o delle operations a nuovo canonical resource type.

