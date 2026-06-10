# UniText

[Quick Start](#quick-start) · [Who Should Read What](#who-should-read-what) · [Repository Model](#repository-model) · [Safety](#safety-and-publication) · [Key Documents](#key-documents) · [Contributing](#contributing) · [English](README.md)

> Registry-first governance for shared AI agent resources across Claude Code, Codex, Gemini / Antigravity, GitHub Copilot, and adjacent runtimes.

![Status](https://img.shields.io/badge/status-active_baseline-brightgreen)
![Runtime](https://img.shields.io/badge/runtime-Python_3%20%7C%20PowerShell_5%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

UniText keeps reusable skills, MCP definitions, agent instructions, workflows, and runtime rules in one canonical registry. It then projects a smaller runtime-facing layer and delivers into host tools through local, reviewed, and verifiable operations.

## What UniText is

UniText is:

- **registry-first** for shared resources
- **runtime-first** for agent startup
- **local-first** for delivery, verification, and evidence
- **adapter-aware** across multiple AI runtimes

## Why teams use it

Use UniText when the same reviewed resource must stay consistent across more than one host surface.

Do not use UniText as:

- secret vault
- silent global config mutator
- automatic publication permission

## Quick Start

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\git-startup.ps1
python .\local\scripts\bootstrap.py --dry-run
python .\local\scripts\bootstrap.py --force
python .\local\scripts\verify-bootstrap.py
```

### macOS / Linux

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

## Who Should Read What

| Reader | Start here | Then read |
|---|---|---|
| New human reader | `README.md` | `INDEX.md` |
| Human reader in Traditional Chinese | `README.zh-TW.md` | `INDEX.md` |
| Agent or automation | `RUNTIME.md` | `runtime/START.md`, `runtime/catalog.json` |
| Maintainer | `VISION.md` | `OPERATIONS.md` |
| Contributor | `CONTRIBUTING.md` | `OPERATIONS.md` |

## Repository Model

| Layer | Purpose | Typical contents |
|---|---|---|
| `registry/` | Canonical shared resources | skills, MCP definitions, agents, workflows |
| `runtime/` | Agent-facing read model | startup files and projections |
| `local/` | Machine-local delivery overlay | bootstrap, verify, sync, local notes |
| `ops/` | Operational evidence | reports, backups, review packages |
| `template/` | Release-safe starter material | examples and bootstrap inputs |

## Safety and Publication

UniText is **local-first**. A clean publishability report, private remote, or repository template does not grant permission to push, upload, paste, or publish content.

Before any external publication step, read:

- `NO_PUBLISH_POLICY.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `WORKSPACE_SENSITIVE_METADATA_RULES.md`

## Key Documents

| File | Why it exists |
|---|---|---|
| `INDEX.md` | Human navigation and task routing |
| `RUNTIME.md` | Agent-first startup surface |
| `VISION.md` | Architecture intent and non-goals |
| `OPERATIONS.md` | Delivery modes, gates, rollback, and verification |
| `DOCUMENT_PLACEMENT_POLICY.md` | Document placement and publication boundaries |
| `RESOURCE_SPEC.md` | Shared resource metadata contract |
| `docs/README.md` | Landing page for long-form supporting docs |

## Contributing

See `CONTRIBUTING.md` before proposing documentation, governance, registry, runtime, or adapter changes.

## License

[MIT License](LICENSE)
