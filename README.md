# UniText

> **A text-native, registry-first shared resource hub for multiple AI CLIs.**
>
> 純文本作為共享介面，讓 Claude Code、Codex、Gemini CLI 等工具共用同一套資源定義。

---

## Why This Exists

If you use more than one AI CLI tool, your resources end up scattered:

- The same skill defined three times, in three slightly different states
- MCP server configs in formats none of your other tools can read
- Agent instructions that only one CLI knows about
- No way to tell which copy is canonical

UniText solves this with a single shared registry and a governed delivery layer. **One definition. Every tool.**

---

## How It Works

```
UniText/
├── registry/          ← canonical definitions (what exists)
│   ├── skills/        ← shared skill definitions
│   ├── mcp/           ← MCP server definitions
│   ├── agents/        ← agent instructions & personas
│   └── workflow/      ← runbooks, plans, conventions
│
├── local/             ← deployment overlay (how it's wired here)
│   ├── docs/          ← path maps, deployment notes
│   └── scripts/       ← sync scripts for this machine
│
└── ops/               ← operations state (not shared resources)
    ├── baseline.json
    ├── inventory.latest.json
    └── history/       ← timestamped audit trail
```

The `registry/` layer is platform-agnostic — it uses logical canonical paths (`/registry/skills`, `/registry/mcp`) rather than OS-specific absolute paths. The `local/` layer resolves those to your actual machine.

---

## Architecture

**Registry-first, adapter-enabled, operations-governed.**

| Layer | Role |
|-------|------|
| **Registry** | Defines what shared resources exist and their canonical identity |
| **Adapter** | Delivers registry content to each CLI (mirror, symlink, native-config, pointer) |
| **Operations** | Governs when and how mutations happen — with backup, dry-run, and audit trail |

### Resource Types

| Type | Logical Root | What Goes Here |
|------|-------------|----------------|
| `skills` | `/registry/skills` | Shared skill definitions used by AI agents |
| `mcp` | `/registry/mcp` | MCP server definitions, cross-CLI |
| `agents` | `/registry/agents` | Agent instructions, personas, system prompts |
| `workflow` | `/registry/workflow` | Runbooks, planning templates, conventions |

### Delivery Modes

Each resource can be delivered differently depending on CLI capabilities:

- `pointer` — discovery only, no content copy
- `mirror` — local copy via robocopy/rsync
- `symlink` — fixed-path link to canonical source
- `native-config` — registered in the CLI's own config format

---

## Getting Started

### 1. Fork or clone this repository

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. Add your first resource

Create a skill under `registry/skills/`:

```
registry/skills/my-skill/
└── SKILL.md
```

Minimum `SKILL.md`:

```yaml
---
name: my-skill
description: What this skill does in one line
---

## Usage

Instructions for the AI agent...
```

### 3. Register it in the catalog

Add an entry to `INDEX.md`:

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. Bootstrap your local CLI wiring

Prefer the cross-platform bootstrap path:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` aligns the shared skills targets, updates Codex `skills_path`, and writes a project-local `.mcp.json` for the bundled MCP baseline. `sync-skills.ps1` remains available as the Windows PowerShell reference implementation.

---

## Supported CLIs

| CLI | Delivery Mode | Notes |
|-----|--------------|-------|
| **Claude Code** | mirror / symlink | `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `skills_path` and `[mcp_servers.*]` in `~/.codex/config.toml` |
| **GitHub CLI** | native-config | `config.yml` |

See [local/docs/PATH_MAP.md](local/docs/PATH_MAP.md) for the full per-CLI path reference.

---

## Governance Rules

UniText enforces a **no silent changes** policy:

1. **Explicit triggers only** — `bootstrap`, `sync`, `adopt`, `repair`
2. **Backup before any mutation** — every destructive action creates a timestamped snapshot in `ops/`
3. **Dry-run before delivery** — preview what will change before it happens
4. **Conflict stops the flow** — if two versions of the same resource differ, the system stops for human review
5. **Full audit trail** — every operation is written to `ops/history/`

Formal adoption flow: `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentation

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | Discovery entry point — what resources exist and where |
| [VISION.md](VISION.md) | Architecture principles and design rationale |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Metadata contract for all shared resources |
| [OPERATIONS.md](OPERATIONS.md) | Delivery modes, triggers, and safety rules |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Authoring repo vs. project template distinction |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Secret storage, redaction, and password/API key handling boundaries |
| [MILESTONES.md](MILESTONES.md) | Quantified phase goals and external-review readiness checkpoints |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Curated `8 + 4` essential skills set for the current review wave |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Reviewer-facing scope, reading order, and repeatable package export flow |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Submission note for external reviewers |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Short-form review summary for fast orientation |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Template release cleanup scope, exclusions, and export flow |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Pre-release cleanup checklist for a starter package |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | Concept note for how UniText can collaborate with skill-0 as a decomposition and primitive-extraction project |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Local-first publishing boundary for agents and collaborators |

Reading order: `EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## Two Ways to Use This

### As a starter template

Fork this repo. Strip `ops/history/`, `backup/`, and `local/` paths specific to this machine. Populate `registry/` with your own skills and MCP definitions. Wire up `local/scripts/` to your environment.

### As a reference implementation

Read the core docs to understand the architecture. Adapt the patterns — registry structure, resource spec, delivery modes, operations audit trail — to your own setup.

---

## Design Principles

- **Registry first** — define before you deliver
- **Discovery before automation** — know what exists before syncing it
- **Platform-agnostic contracts** — logical paths in specs, absolute paths only in local overlay
- **Minimum viable metadata** — `id`, `type`, `canonical_location`, `status` is enough to start
- **Safe mutation** — dry-run + backup + explicit trigger, always
- **AI as consumer** — models read and act on the registry; they don't own the delivery guarantee

---

## Status

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active — `skills/`, `mcp/`, `workflow/`, `agents/` roots present |
| Skills registry | Active baseline — first canonical batch adopted, broader adoption still in progress |
| Agents registry | Active seed — `registry-curator` entry created |
| MCP registry | Active baseline — canonical definition plus runnable read-only server present |
| Workflow registry | Draft seed — workflow doc plus plan template present |
| Operations audit trail | Active |
| Sync, bootstrap, and review scripts | Active baseline in `local/scripts/` |
| External review package | Active baseline — reviewer guide and export script present |
| Template release cleanup | Release candidate — template package guide, checklist, export + verify scripts, generic examples, and local overlay skeleton present |

---

## License

MIT

---

*For people who use more than one AI tool and want a single source of truth.*
