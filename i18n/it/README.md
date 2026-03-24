[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [한국어](../ko/README.md) | [Italiano](README.md)

# UniText

> **Un hub di risorse condivise, text-native e registry-first per più AI CLI.**
>
> Testo puro come interfaccia condivisa, così Claude Code, Codex, Gemini CLI e altri strumenti possono usare la stessa definizione di risorse.

---

## Perché esiste

Se usi più di un tool AI CLI, le tue risorse finiscono per disperdersi:

- la stessa skill definita tre volte, con tre stati leggermente diversi
- configurazioni MCP in formati che gli altri strumenti non riescono a leggere
- istruzioni per agent note solo a una singola CLI
- nessun modo chiaro per capire quale copia sia canonica

UniText risolve questo problema con un registry condiviso e un layer di delivery governato. **Una definizione. Tutti gli strumenti.**

---

## Come funziona

```
UniText/
├── registry/          ← definizioni canoniche (ciò che esiste)
│   ├── skills/        ← definizioni condivise delle skill
│   ├── mcp/           ← definizioni dei server MCP
│   ├── agents/        ← istruzioni e persona degli agent
│   └── workflow/      ← runbook, piani, convenzioni
│
├── local/             ← overlay di deployment (come è collegato qui)
│   ├── docs/          ← path map, note di deployment
│   └── scripts/       ← script di sync per questa macchina
│
└── ops/               ← stato operativo (non sono shared resources)
    ├── baseline.json
    ├── inventory.latest.json
    └── history/       ← audit trail con timestamp
```

Il layer `registry/` è platform-agnostic: usa logical canonical paths (`/registry/skills`, `/registry/mcp`) invece di path assoluti specifici del sistema operativo. Il layer `local/` risolve questi riferimenti sulla macchina reale.

---

## Architettura

**Registry-first, adapter-enabled, operations-governed.**

| Layer | Ruolo |
|-------|------|
| **Registry** | Definisce quali shared resources esistono e la loro identità canonica |
| **Adapter** | Consegnano i contenuti del registry a ogni CLI (mirror, symlink, native-config, pointer) |
| **Operations** | Governa quando e come avvengono le mutation, con backup, dry-run e audit trail |

### Tipi di risorsa

| Tipo | Logical Root | Cosa contiene |
|------|-------------|----------------|
| `skills` | `/registry/skills` | definizioni condivise di skill usate dagli agent AI |
| `mcp` | `/registry/mcp` | definizioni MCP cross-CLI |
| `agents` | `/registry/agents` | istruzioni per agent, persona e system prompt |
| `workflow` | `/registry/workflow` | runbook, template di pianificazione, convenzioni |

### Delivery modes

Ogni risorsa può essere consegnata in modo diverso, a seconda delle capacità della CLI:

- `pointer` — solo discovery, nessuna copia del contenuto
- `mirror` — copia locale via robocopy/rsync
- `symlink` — link a path fisso verso la sorgente canonica
- `native-config` — registrata nel formato di configurazione della CLI

---

## Come iniziare

### 1. Forka o clona questo repository

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. Aggiungi la tua prima risorsa

Crea una skill sotto `registry/skills/`:

```
registry/skills/my-skill/
└── SKILL.md
```

`SKILL.md` minimo:

```yaml
---
name: my-skill
description: Cosa fa questa skill in una sola riga
---

## Usage

Istruzioni per l’AI agent...
```

### 3. Registrala nel catalogo

Aggiungi una voce in `INDEX.md`:

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. Configura il wiring locale della tua CLI

Preferisci il percorso di bootstrap cross-platform:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` allinea i target condivisi delle skills, aggiorna `skills_path` di Codex e scrive un `.mcp.json` project-local per il baseline MCP integrato. `sync-skills.ps1` resta disponibile come reference implementation in Windows PowerShell.

---

## CLI supportate

| CLI | Delivery Mode | Notes |
|-----|--------------|-------|
| **Claude Code** | mirror / symlink | `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `skills_path` e `[mcp_servers.*]` in `~/.codex/config.toml` |
| **GitHub CLI** | native-config | `config.yml` |

Vedi [local/docs/PATH_MAP.md](local/docs/PATH_MAP.md) per il riferimento completo dei path per CLI.

---

## Regole di governance

UniText applica una politica di **no silent changes**:

1. **Solo trigger espliciti** — `bootstrap`, `sync`, `adopt`, `repair`
2. **Backup prima di ogni mutation** — ogni azione distruttiva crea uno snapshot con timestamp in `ops/`
3. **Dry-run prima del delivery** — visualizza in anticipo cosa cambierà
4. **Il conflitto ferma il flusso** — se due versioni della stessa risorsa differiscono, il sistema si ferma per la revisione umana
5. **Audit trail completo** — ogni operazione viene scritta in `ops/history/`

Flusso formale di adozione: `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentazione

| File | Scopo |
|------|-------|
| [INDEX.md](INDEX.md) | Entry point per il discovery — quali risorse esistono e dove si trovano |
| [VISION.md](VISION.md) | Principi architetturali e rationale di design |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Contratto dei metadata per tutte le shared resources |
| [OPERATIONS.md](OPERATIONS.md) | Delivery mode, trigger e regole di sicurezza |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Distinzione tra repository di authoring e template di progetto |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Regole di archiviazione, redaction e gestione di password/API key |
| [MILESTONES.md](MILESTONES.md) | Obiettivi quantitativi delle fasi e checkpoint di readiness per la review esterna |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Set curato `8 + 4` di skill essenziali per l’ondata di review corrente |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Ambito per i reviewer, ordine di lettura e flusso ripetibile di export del package |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Nota di invio per i reviewer esterni |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Riassunto breve per orientarsi rapidamente |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Ambito, esclusioni e flusso di export per il cleanup del rilascio template |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Checklist di pre-release per uno starter package |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | Nota concettuale su come UniText può collaborare con skill-0 come progetto di decomposizione ed estrazione di primitive |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Confine di pubblicazione local-first per agent e collaboratori |

Ordine di lettura: `EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## Due modi per usarlo

### Come starter template

Forka questo repo. Rimuovi `ops/history/`, `backup/` e i path specifici di `local/` di questa macchina. Popola `registry/` con le tue skill e definizioni MCP. Adatta `local/scripts/` al tuo ambiente.

### Come reference implementation

Leggi i documenti centrali per capire l’architettura. Adatta i pattern — struttura del registry, resource spec, delivery modes, audit trail operativo — al tuo setup.

---

## Principi di design

- **Registry first** — definisci prima di consegnare
- **Discovery before automation** — conosci ciò che esiste prima di sincronizzarlo
- **Platform-agnostic contracts** — path logici nelle specifiche, path assoluti solo nell’overlay locale
- **Minimum viable metadata** — `id`, `type`, `canonical_location`, `status` bastano per iniziare
- **Safe mutation** — dry-run + backup + trigger esplicito, sempre
- **AI as consumer** — i modelli leggono e agiscono sul registry; non garantiscono la delivery

---

## Stato

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active — root `skills/`, `mcp/`, `workflow/`, `agents/` presenti |
| Skills registry | Active baseline — primo batch canonico adottato, l’adozione più ampia è ancora in corso |
| Agents registry | Active seed — creato l’entry `registry-curator` |
| MCP registry | Active baseline — definizione canonica più server read-only eseguibile presenti |
| Workflow registry | Draft seed — documento workflow più template di piano presenti |
| Operations audit trail | Active |
| Sync, bootstrap and review scripts | Active baseline in `local/scripts/` |
| External review package | Active baseline — reviewer guide e script di export presenti |
| Template release cleanup | Release candidate — template package guide, checklist, script export + verify, generic examples e skeleton di overlay locale presenti |

---

## Licenza

MIT

---

*Per chi usa più di un tool AI e vuole una single source of truth.*

