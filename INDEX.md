# UniText — Index

> Status: active baseline
> Role: human discovery and catalog orientation. Consumer agents should start at [RUNTIME.md](RUNTIME.md).

UniText is a registry-first governance workspace for shared AI agent resources. Use this page to find the right document or catalog excerpt without turning the README into a full manual.

## 1. Start Here

| Reader | Best first page | Why |
|---|---|---|
| New human reader | [README.md](README.md) | Public front door and quickstart |
| Agent or automation | [RUNTIME.md](RUNTIME.md) | Short, low-noise runtime entry |
| Maintainer | [VISION.md](VISION.md) | Architecture intent and non-goals |
| Adapter author | [RESOURCE_SPEC.md](RESOURCE_SPEC.md), then [OPERATIONS.md](OPERATIONS.md) | Metadata contract plus delivery rules |
| Release reviewer | [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md), [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Publishability and exclusion boundaries |

## 2. Core Docs

| File | Role |
|---|---|
| [README.md](README.md) | English authoritative publishable front door |
| [README.zh-TW.md](README.zh-TW.md) | Root Traditional Chinese companion |
| [RUNTIME.md](RUNTIME.md) | Agent-first runtime entrypoint |
| [VISION.md](VISION.md) | Architecture rationale |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | Shared resource metadata contract |
| [OPERATIONS.md](OPERATIONS.md) | Delivery modes, safety gates, and verification |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Authoring workspace vs. starter template |
| [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md) | Where docs and operational artifacts belong |
| [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) | Shared-surface metadata leak rules |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Secret and credential handling |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | Local-only and publication boundaries |

## 3. Adapter Notes

| Host | Note |
|---|---|
| Claude Code | [docs/adapters/CLAUDE_CODE_ADAPTER_NOTE.md](docs/adapters/CLAUDE_CODE_ADAPTER_NOTE.md) |
| Codex | [docs/adapters/CODEX_CLI_ADAPTER_NOTE.md](docs/adapters/CODEX_CLI_ADAPTER_NOTE.md) |
| GitHub Copilot | [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md) |
| Gemini / Antigravity | [docs/adapters/GEMINI_ANTIGRAVITY_ADAPTER_NOTE.md](docs/adapters/GEMINI_ANTIGRAVITY_ADAPTER_NOTE.md) |

Adapter notes describe host-specific compatibility and limitations. They do not authorize writes to global settings or remote services.

## 4. Resource Catalog

| Type | Logical root | Purpose |
|---|---|---|
| `skill` | `registry/skills` | Reusable skills and capability packs |
| `mcp` | `registry/mcp` | MCP definitions and adoption notes |
| `agent` | `registry/agents` | Shared personas and playbooks |
| `workflow` | `registry/workflow` | Runbooks, plan templates, and repeatable processes |

The runtime-facing catalog is [runtime/catalog.json](runtime/catalog.json). The schema and metadata expectations are in [RESOURCE_SPEC.md](RESOURCE_SPEC.md).

## 5. Current Catalog Excerpts

### Review Shortlist

The external-review shortlist is tracked in [docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md](docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md). It is a review-facing excerpt, not the full inventory.

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `registry/skills/pdf` | `active` |
| `docx` | Core 8 | `registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `registry/skills/theme-factory` | `active` |

### Workflow

| `id` | `canonical_location` | `status` |
|---|---|---|
| `claude-plans` | `registry/workflow/claude-plans` | `draft` |
| `heartbeat-protocol` | `registry/workflow/heartbeat-protocol` | `draft` |

### MCP

| `id` | `canonical_location` | `status` | Notes |
|---|---|---|---|
| `claude-project-mcp-seed` | `registry/mcp/claude-project-mcp-seed` | `active-baseline` | Template-safe project MCP seed; delivery remains explicit |

### Agents

| `id` | `canonical_location` | `status` |
|---|---|---|
| `registry-curator` | `registry/agents/registry-curator` | `active` |

## 6. Operations And Reports

| Task | Start here |
|---|---|
| Build or verify runtime projections | `python local/scripts/build-runtime-layer.py` |
| Bootstrap local CLI wiring | [OPERATIONS.md](OPERATIONS.md), then `python local/scripts/bootstrap.py --dry-run` |
| Verify workspace-sensitive boundaries | [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md), then `python local/scripts/verify-workspace-boundaries.py --format json` |
| Check i18n drift | `python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero` |
| Export review package | [docs/reviews/EXTERNAL_REVIEW_PACKAGE.md](docs/reviews/EXTERNAL_REVIEW_PACKAGE.md), then `local/scripts/export-review-package.ps1` |
| Export template package | [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md), then `local/scripts/export-template-package.ps1` |
| Build project map | [web/project-map-ui/README.md](web/project-map-ui/README.md) |

## 7. Discovery Rules

`INDEX.md` answers:

- which page to read
- where each resource family lives
- which current catalog excerpts are useful for review
- which script starts a common local check

`INDEX.md` does not answer:

- final host-specific absolute paths
- live machine configuration
- private plans, roadmaps, review notes, or operational state
- runtime startup context for agents

For those boundaries, use [RUNTIME.md](RUNTIME.md), [OPERATIONS.md](OPERATIONS.md), and [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md).
