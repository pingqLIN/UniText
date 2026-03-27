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

`bootstrap.py` aligns the shared skills targets, updates Codex `skills_path`, and upgrades the project `.mcp.json` to the active machine interpreter and repo root. `sync-skills.ps1` remains available as the Windows PowerShell reference implementation. Copilot CLI is part of the target baseline, but its adapter wiring is still tracked as a follow-up item rather than a verified first-run path. See [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md) for the current scope, constraints, and next-step definition.

### 5. Install Python dependencies

UniText now defines root-level dependency manifests with three layers:

- `requirements.txt`
  - core runtime for root-level bootstrap / verify / export flow
- `requirements-tooling.txt`
  - optional tooling used by validation helpers and active skill tooling
- `requirements-skill-local.txt`
  - skill-local dependencies for bundled scripts that are not part of the minimal starter runtime
- `requirements-dev.txt`
  - full contributor environment

Core runtime:

```bash
python -m pip install -r requirements.txt
```

Full contributor environment:

```bash
python -m pip install -r requirements-dev.txt
```

### 6. Run the baseline checks

Local validation mirrors the minimum GitHub Actions baseline:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
python -m unittest tests.security.test_hardening
```

The repository also ships a GitHub Actions baseline at `.github/workflows/ci.yml` with:

- a full Windows baseline job for health checks, regression tests, and export / verify smoke
- a macOS / Linux Python smoke job for portable bootstrap and proof-oriented tests

---

## Supported CLIs

UniText uses three support labels in this repository:

- `verified`
  - repeatable repo evidence exists for the stated scope
- `partial`
  - some validation exists, but the repo does not yet claim full end-to-end coverage
- `target`
  - intended support surface only; not yet verified in this repo

| CLI | Support Class | Verification Scope | Notes |
|-----|---------------|--------------------|-------|
| **Claude Code** | `verified` | `delivery path verified` | `.claude/settings.json`, project `.mcp.json`, and shared skills delivery path are part of the maintained baseline; this is not yet claimed as end-to-end task verification |
| **Gemini CLI** | `verified` | `delivery path verified` | shared skills delivery path is part of the maintained baseline; end-to-end interaction is not currently claimed |
| **Codex** | `partial` | `bootstrap path defined` | native config wiring is implemented through `bootstrap.py` and `config.toml`, but this repo does not currently claim a fully repeatable end-to-end bootstrap verification across fresh machines |
| **Copilot CLI** | `target` | `adapter pending` | intended to consume the shared MCP / skill baseline once a stable repo-level adapter path is defined |

See [template/examples/local/README.md](template/examples/local/README.md) for the starter local overlay, including the exported path-map stub at `template/examples/local/docs/PATH_MAP.template.md`.
See [local/docs/SUPPORT_PROOF_MATRIX.md](local/docs/SUPPORT_PROOF_MATRIX.md) for the current mapping between support claims and proof artifacts.
See [local/docs/DOCS_GOVERNANCE_RULES.md](local/docs/DOCS_GOVERNANCE_RULES.md) for the current interpretation rules around authoritative docs, review archive, translations, and workspace residue.

If you want to turn this repository into a clean new starter project rather than use the authoring workspace directly, follow [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md).

### Cross-Platform Baseline

The GitHub-hosted starter template has a broader target surface than the currently verified surface.

| Platform | Support Class | Verification Scope | Notes |
|----------|---------------|--------------------|-------|
| `Windows` | `verified` | `authoring + export baseline verified` | current scripts, review export flow, and template export flow are maintained and revalidated on Windows |
| `macOS` | `target` | `template target` | Python-based bootstrap flow is designed to be portable, but this repo does not currently claim repeated macOS validation evidence |
| `Linux` | `target` | `template target` | Python-based bootstrap flow is designed to be portable, but this repo does not currently claim repeated Linux validation evidence |

The tracked `.mcp.json` is a relative-path seed for fresh clones. The supported first-run path is still:

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

That route is the authoritative setup path because it pins the current machine interpreter, repo root, and Codex wiring without baking author-specific absolute paths into the shared template.

No platform in this README should be read as `end-to-end verified` unless that exact phrase is stated.

### Current Material Sets

UniText currently distinguishes three different material sets:

- `authoring review shortlist`
  - the maintainer-facing working set used to review and compare candidate skills
- `public release subset`
  - the GitHub-backed, publicly redistributable subset that can ship in exported review packages
- `local-only validation materials`
  - maintainer-local or non-release materials that may be used during dry-run validation but are not part of the public release surface

When these sets differ, exported packages are the release truth, not the authoring workspace.

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
| [requirements.txt](requirements.txt) | Root-level Python dependency entry point for the core runtime path |
| [requirements-tooling.txt](requirements-tooling.txt) | Optional tooling dependencies used by validation helpers and active skill tooling |
| [requirements-skill-local.txt](requirements-skill-local.txt) | Skill-local Python dependencies for bundled scripts outside the minimal runtime |
| [requirements-dev.txt](requirements-dev.txt) | Full contributor Python environment |
| [LICENSE](LICENSE) | License for the UniText project itself |
| [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) | Summary of third-party skill-source licenses and current holdback materials |
| `.github/workflows/ci.yml` | Minimal GitHub Actions baseline for dependency install, health checks, security tests, and export smoke checks |
| [local/docs/SUPPORT_PROOF_MATRIX.md](local/docs/SUPPORT_PROOF_MATRIX.md) | Current support-claim to proof-artifact mapping for CLI and platform surfaces |
| [local/docs/INDEPENDENT_VALIDATION_RUNBOOK.md](local/docs/INDEPENDENT_VALIDATION_RUNBOOK.md) | Checklist for non-author validation of bootstrap, export, and verify flows |
| [local/docs/INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md](local/docs/INDEPENDENT_VALIDATION_REPORT_TEMPLATE.md) | Fill-in template for independent operator validation results |
| [registry/skills/SOURCE_SCHEMA.md](registry/skills/SOURCE_SCHEMA.md) | Current schema and provenance expectations for `SOURCE.yaml` metadata |
| [docs/reviews/README.md](docs/reviews/README.md) | Review, audit, and advisory archive, including the decision chain and security review set |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | Curated `8 + 4` essential skills set for the current review wave |
| [SKILLS_PUBLIC_RELEASE_POLICY.md](SKILLS_PUBLIC_RELEASE_POLICY.md) | Public-release boundary for skills, including local-only validation materials vs publicly redistributable examples |
| [WORKSPACE_BOUNDARY.md](WORKSPACE_BOUNDARY.md) | Boundary between authoring workspace, tracked source, and exported package |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | Reviewer-facing scope, reading order, and repeatable package export flow |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | Submission note for external reviewers |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | Short-form review summary for fast orientation |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | Template release cleanup scope, exclusions, and export flow |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | Pre-release cleanup checklist for a starter package |
| [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md) | Fresh-project rebuild flow for turning the current repo into a clean starter baseline |
| [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md) | Scope note for bringing Copilot CLI into the same cross-platform starter baseline without overstating support |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | Concept note for how UniText can collaborate with skill-0 as a decomposition and primitive-extraction project |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Local-first publishing boundary for agents and collaborators |

Reading order: `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `PROJECT_MODES.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `REBUILD_AS_NEW_PROJECT.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md`

Review, audit, advisory, and remediation history is now grouped under [docs/reviews/README.md](docs/reviews/README.md) so the root stays focused on starter and architecture docs.

---

## Two Ways to Use This

### As a starter template

Fork this repo. Keep the shipped `.claude/settings.json`, `.mcp.json`, and `bootstrap -> verify` flow as the baseline for Claude / Codex / Gemini, and treat Copilot CLI as a target adapter to wire once its local config path is defined for your environment. Populate `registry/` with your own skills and MCP definitions, then run the local bootstrap flow for your machine.

The public starter package is intended to include only template-safe, publicly redistributable examples and skills. Authoring-only or restricted-license local validation materials may exist in the maintainer workspace, but they are not part of the public release surface.

Do not treat the current authoring workspace as the release source. Use exported packages as the publishable surface, and see [WORKSPACE_BOUNDARY.md](WORKSPACE_BOUNDARY.md) for the workspace / tracked / exported boundary.

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

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for third-party skill-source attribution and the current holdback set that is excluded from public packages.

---

*For people who use more than one AI tool and want a single source of truth.*
