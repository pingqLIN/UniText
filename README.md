[English](README.md) | [繁體中文](i18n/zh-TW/README.md) | [简体中文](i18n/zh-CN/README.md) | [日本語](i18n/ja/README.md) | [Deutsch](i18n/de/README.md) | [Français](i18n/fr/README.md) | [Español](i18n/es/README.md) | [한국어](i18n/ko/README.md) | [Italiano](i18n/it/README.md)

# UniText

> **A text-native, registry-first shared resource hub for multiple AI CLIs.**
>
> 純文本作為共享介面，讓 Claude Code、Codex、Gemini CLI、Copilot CLI 等工具共用同一套資源定義。

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
    └── history/       ← timestamped audit trail
```

The `registry/` layer is platform-agnostic — it uses logical canonical paths (`/registry/skills`, `/registry/mcp`) rather than OS-specific absolute paths. The `local/` layer resolves those to your actual machine. The shared repo baseline includes a template-safe `.mcp.json` seed and `.claude/settings.json`, while `bootstrap.py` upgrades them to active machine wiring when needed.

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

If your system exposes Python as `python3`, replace `python` with `python3`.

`bootstrap.py` aligns the shared skills targets, updates Codex `skills_path`, upgrades the project `.mcp.json` to the active machine interpreter and repo root, and registers the same `unitext-registry` MCP server in `~/.copilot/mcp-config.json` when `Copilot CLI` is present. `sync-skills.ps1` remains available as the Windows PowerShell reference implementation. Copilot keeps using repo instructions from `AGENTS.md` / related files rather than a duplicated skills delivery path. See [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md) for the current scope, constraints, and remaining gaps.

---

## Supported CLIs

| CLI | Delivery Mode | Notes |
|-----|--------------|-------|
| **Claude Code** | mirror / symlink + project-local settings | `.claude/settings.json`, repo `.mcp.json`, `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `skills_path` and `[mcp_servers.*]` in `~/.codex/config.toml` |
| **Copilot CLI** | global MCP config + repo instructions | `~/.copilot/mcp-config.json` for MCP wiring; repo instructions come from `AGENTS.md` / related files |

See [template/examples/local/README.md](template/examples/local/README.md) for the starter local overlay, including the exported path-map stub at `template/examples/local/docs/PATH_MAP.template.md`.

If you want to turn this repository into a clean new starter project rather than use the authoring workspace directly, follow [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md).

### Cross-Platform Baseline

The GitHub-hosted starter template is intended to support:

- `Claude Code`
- `Codex`
- `Gemini CLI`
- `Copilot CLI`
- `Windows`
- `macOS`
- `Linux`

The tracked `.mcp.json` is a relative-path seed for fresh clones. The supported first-run path is still:

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

That route is the authoritative setup path because it pins the current machine interpreter, repo root, and Codex wiring without baking author-specific absolute paths into the shared template.

`verify-bootstrap.py` accepts either:

- the tracked template-safe `.mcp.json` seed
- or the locally bootstrapped `.mcp.json` that points at the current machine interpreter and repo root

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
| [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) | Schema, maintenance rules, and validation flow for workspace-sensitive metadata detection |
| [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md) | Placement matrix for shared, local, authoring, and operations documents |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Secret storage, redaction, and password/API key handling boundaries |
| [MILESTONES.md](MILESTONES.md) | Quantified phase goals and external-review readiness checkpoints |
| [BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md](BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md) | Reusable template for documenting boundary drift incidents and permanent controls |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Curated `8 + 4` essential skills set for the current review wave |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Reviewer-facing scope, reading order, and repeatable package export flow |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Submission note for external reviewers |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Short-form review summary for fast orientation |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Template release cleanup scope, exclusions, and export flow |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Pre-release cleanup checklist for a starter package |
| [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) | Fresh-project rebuild flow for turning the current repo into a clean starter baseline |
| [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md) | Scope note for bringing Copilot CLI into the same cross-platform starter baseline without overstating support |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | Concept note for how UniText can collaborate with skill-0 as a decomposition and primitive-extraction project |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Local-first publishing boundary for agents and collaborators |

Reading order: `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `PROJECT_MODES.md` → `WORKSPACE_SENSITIVE_METADATA_RULES.md` → `DOCUMENT_PLACEMENT_POLICY.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `REBUILD_AS_NEW_PROJECT.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md`

The authoring repo is not automatically publish-safe just because template or rebuild exports validate cleanly. Use `local/scripts/verify-workspace-boundaries.ps1` when you need a repo-side boundary check for tracked shared surfaces.

---

## Two Ways to Use This

### As a starter template

Fork this repo. Keep the shipped `.claude/settings.json`, `.mcp.json`, and `bootstrap -> verify` flow as the baseline for Claude / Codex / Gemini. If `Copilot CLI` is installed, the same bootstrap flow also registers `unitext-registry` into `~/.copilot/mcp-config.json` while leaving repo instructions to `AGENTS.md` / related files. Populate `registry/` with your own skills and MCP definitions, then run the local bootstrap flow for your machine.

### As a reference implementation

Read the core docs to understand the architecture. Adapt the patterns — registry structure, resource spec, delivery modes, operations audit trail — to your own setup.

---

## Design Principles

- **Registry first** — define before you deliver
- **Discovery before automation** — know what exists before syncing it
- **Platform-agnostic contracts** — logical paths in specs, absolute paths only in local overlay
- **Repo-level line ending policy** — keep text normalization in tracked `.gitattributes`, not in author-specific Git settings
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
