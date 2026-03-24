# AGENTS.md

> Linee guida per gli AI agent che operano in qualsiasi repository.

Questo documento definisce le regole generali per gli AI agent: principi di esecuzione, stile di codice, coordinamento multi-model e gestione degli errori.

---

## 1. Execution Principles / Principi di esecuzione

> **Efficienza e autonomia senza sacrificare la sicurezza.**

| Principle | Guideline |
|---|---|
| **Parallel execution** | Parallelizza solo quando i task non hanno dipendenze, overlap o contraddizioni; altrimenti preferisci l’esecuzione sequenziale. |
| **Prefer automation** | Esegui senza chiedere conferma, a meno che manchino informazioni o ci siano rischi di sicurezza. |
| **Avoid unnecessary prompts** | Usa default ragionevoli e fai domande solo quando il caso è davvero ambiguo. |

---

## 2. Guiding Philosophy / Filosofia guida

### AI-First for Code & Inline Comments

Tutto il codice, i commenti inline e le descrizioni tecniche devono essere scritti principalmente per il consumo da parte dell’AI:

| Aspect | Guideline |
|---|---|
| **Variable/function names** | Usa nomi descrittivi e non ambigui. |
| **Code comments** | Spiega intenzione e contesto, così l’AI può ragionare meglio. |
| **Type annotations** | Includi i tipi per agevolare l’analisi statica dell’AI. |
| **Structured data** | Usa JSON/YAML con schema chiari. |

### Human-Readable Documentation

**Eccezione**: la documentazione per l’utente deve privilegiare la leggibilità umana.

| Requirement | Description |
|---|---|
| **Bilingual (recommended)** | Quando opportuno, fornisci cinese tradizionale (zh-TW) e inglese. |
| **Detailed explanations** | Copertura completa con esempi. |
| **Easy to read** | Struttura logica, gerarchia chiara e layout scansionabile. |

---

## 3. Code Style Guidelines / Stile del codice

### General Principles

| Principle | Description |
|---|---|
| **Single responsibility** | Tieni tutto in una funzione, salvo che sia davvero composabile o riusabile. |
| **Avoid `try`/`catch`** | Dove possibile, lascia propagare gli errori. |
| **No `any` type** | Evita variabili non tipizzate. |
| **Simple naming** | Preferisci nomi a una sola parola quando possibile. |
| **Type inference** | Affidati all’inferenza; usa tipi espliciti solo quando serve chiarezza o export. |
| **Functional methods** | Preferisci `flatMap`, `filter`, `map` ai cicli `for`. |

### Naming Conventions

Preferisci nomi brevi. Usa più parole solo se necessario:

```ts
// Good ✅
const foo = 1
function journal(dir: string) {}

// Bad ❌
const fooBar = 1
function prepareJournal(dir: string) {}
```

Se un valore viene usato una sola volta, inlinalo per ridurre il numero di variabili:

```ts
// Good ✅
const data = await readFile(path.join(dir, "data.json"))

// Bad ❌
const dataPath = path.join(dir, "data.json")
const data = await readFile(dataPath)
```

### Destructuring

Evita destrutturazioni inutili. Usa la notazione a punto per preservare il contesto:

```ts
// Good ✅
obj.a
obj.b

// Bad ❌
const { a, b } = obj
```

### Variables

Preferisci `const` a `let`. Usa ternari o early return invece di riassegnazioni:

```ts
// Good ✅
const foo = condition ? 1 : 2

// Bad ❌
let foo
if (condition) foo = 1
else foo = 2
```

### Control Flow

Evita `else`. Preferisci early return:

```ts
// Good ✅
function foo() {
  if (condition) return 1
  return 2
}

// Bad ❌
function foo() {
  if (condition) return 1
  else return 2
}
```

---

## 4. Markdown & Documentation Style

| Aspect | Convention |
|---|---|
| **Language** | Contenuto principale nella lingua locale, termini tecnici in inglese. |
| **Headings** | Usa titoli ATX (`#`, `##`, `###`), profondità massima 4. |
| **Lists** | `-` per elenchi non ordinati, `1.` per ordinati. |
| **Code blocks** | Specifica sempre il linguaggio. |
| **Tables** | Colonne allineate con pipe e separatore di intestazione. |
| **Links** | Per i documenti interni, preferisci path relativi. |

### Frontmatter (for Workflows)

```yaml
---
description: Breve descrizione dello scopo del workflow
---
```

### JSON Files

| Aspect | Convention |
|---|---|
| **Indentation** | 2 o 4 spazi, ma coerenti. |
| **Quotes** | Solo doppi apici. |
| **Trailing commas** | Non consentite (JSON rigoroso). |

---

## 5. Multi-Agent Coordination

### Subagent Types

| Subagent Type | Purpose | Cost |
|---|---|---|
| `explore` | Esplorazione del codebase e matching di pattern | FREE |
| `librarian` | Documentazione, esempi OSS, documenti esterni | CHEAP |
| `oracle` | Review architetturale e ragionamento profondo | HIGH |
| `frontend-ui-ux-engineer` | Sviluppo visual UI/UX | CHEAP |
| `document-writer` | Documentazione tecnica | CHEAP |
| `multimodal-looker` | Analisi visiva di PDF e immagini | CHEAP |
| `general` | Task multi-step generici | MEDIUM |

### Workflow Source Convention

**Single Source of Truth**: `.agent/workflows/` è la source canonica per tutte le definizioni di workflow.

| Location | Purpose |
|---|---|
| `.agent/workflows/*.md` | **Canonical source** - modifica qui |
| Root `*.md` (workflow docs) | Documenti di riferimento / estesi |

---

## 6. Checkpoint & Execution Modes

### Checkpoint Syntax

```markdown
📍 **CHECKPOINT**: taskAnalysis
├── Verification item 1
├── Verification item 2
└── Final verification

[supervised] Action in supervised mode
[yolo] Action in YOLO mode
```

### Available Checkpoints

- `taskAnalysis` - analisi del task completata
- `resourceAllocation` - allocazione delle risorse confermata
- `preExecution` - conferma pre-esecuzione
- `phaseComplete` - fase completata
- `finalReview` - revisione finale

### Execution Modes

| Mode | Behavior |
|---|---|
| **supervised** | Si ferma ai checkpoint e richiede conferma dell’utente. |
| **yolo** | Continua automaticamente e si ferma solo sugli errori. |

---

## 7. Error Handling Patterns

| Error Type | Action |
|---|---|
| `RATE_LIMIT_EXCEEDED` | Riprova automaticamente |
| `TIMEOUT` | Riprova automaticamente |
| `TEMPORARY_FAILURE` | Riprova automaticamente |
| `AUTHENTICATION_FAILED` | Escalate to user |
| `QUOTA_EXHAUSTED` | Escalate to user |

---

## 8. Testing Guidelines

| Principle | Description |
|---|---|
| **Avoid mocks** | Usa implementazioni reali quando possibile. |
| **No logic duplication** | Non duplicare la logica del codice nei test. |
| **Integration over unit** | Preferisci test di integrazione che esercitano i percorsi reali. |

---

## 9. Important Constraints

### DO ✅

- Usa l’esecuzione parallela quando i task sono indipendenti.
- Mantieni coerenti i nomi di role e subagent nei documenti.
- Includi le annotazioni di tipo per tutti gli export.
- Usa YAML frontmatter nei documenti di workflow.

### DO NOT ❌

- Usare il tipo `any`.
- Creare nuovi nomi di role senza aggiornare l’inventory.
- Hardcodare i nomi dei modelli nei workflow.
- Rimuovere i checkpoint dai workflow supervised.

---

## Quick Reference

| What | Location |
|---|---|
| Role definitions | `resources/inventory.md` (if available) |
| Execution config | `config.json` (if available) |
| Workflow templates | `.agent/workflows/` |
| UI design rules | `resources/ui-design-guidelines.md` (if available) |

---

> [!NOTE]
> Questo documento è una **merged version** che combina le best practice di:
> - opencode/AGENTS.md (focus su TypeScript / execution efficiency)
> - global_workflows/AGENTS.md (focus sul coordinamento multi-model)

---

## No-Publish Rule

Questo repository contiene materiali che possono restare privati fino a quando l’utente non autorizza esplicitamente la pubblicazione.

Gli agent che operano in questo repository DEVONO seguire queste regole:

1. Non fare push dei commit verso alcun remote, a meno che l’utente non lo richieda esplicitamente.
2. Non caricare il contenuto del repository su GitHub, social network, documenti cloud, paste site o qualsiasi altro servizio di rete, a meno che l’utente non lo richieda esplicitamente.
3. Tratta come particolarmente sensibili, per impostazione predefinita:
   - bozze di post social
   - note di confronto tra progetti
   - discussioni di collaborazione cross-project
   - note di revisione
   - documenti di pianificazione strategica
4. Se l’utente chiede pubblicazione, push, upload o posting, pubblica solo il contenuto specificamente approvato.
5. In caso di dubbio, mantieni tutto in locale e chiedi prima di pubblicare.

## Scope Note

Questa politica si applica anche quando:

- esiste già un remote
- il repository è privato
- il contenuto sembra già pronto per la pubblicazione

Un repository privato non equivale ad autorizzazione automatica alla pubblicazione.

