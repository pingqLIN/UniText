# UniText — Index

> 狀態：active baseline
> 角色：human discovery 與 catalog orientation。Consumer agents 應從 [RUNTIME.md](../../RUNTIME.md) 開始。

UniText 是 shared AI agent resources 的 registry-first governance workspace。本頁協助人類讀者找到正確文件與 catalog excerpt，不讓 README 變成完整 manual。

## 1. Start Here

| Reader | Best first page | Why |
|---|---|---|
| New human reader | [README.md](../../README.md) | Public front door and quickstart |
| Agent or automation | [RUNTIME.md](../../RUNTIME.md) | Short, low-noise runtime entry |
| Maintainer | [VISION.md](../../VISION.md) | Architecture intent and non-goals |
| Adapter author | [RESOURCE_SPEC.md](../../RESOURCE_SPEC.md), then [OPERATIONS.md](../../OPERATIONS.md) | Metadata contract plus delivery rules |
| Release reviewer | [TEMPLATE_RELEASE_PACKAGE.md](../../TEMPLATE_RELEASE_PACKAGE.md), [NO_PUBLISH_POLICY.md](../../NO_PUBLISH_POLICY.md) | Publishability and exclusion boundaries |

## 2. Core Docs

| File | Role |
|---|---|
| [README.md](../../README.md) | English authoritative publishable front door |
| [README.zh-TW.md](../../README.zh-TW.md) | Root Traditional Chinese companion |
| [RUNTIME.md](../../RUNTIME.md) | Agent-first runtime entrypoint |
| [VISION.md](../../VISION.md) | Architecture rationale |
| [RESOURCE_SPEC.md](../../RESOURCE_SPEC.md) | Shared resource metadata contract |
| [OPERATIONS.md](../../OPERATIONS.md) | Delivery modes, safety gates, and verification |
| [DOCUMENT_PLACEMENT_POLICY.md](../../DOCUMENT_PLACEMENT_POLICY.md) | Where docs and operational artifacts belong |
| [NO_PUBLISH_POLICY.md](../../NO_PUBLISH_POLICY.md) | Local-only and publication boundaries |

## 3. Adapter Notes

| Host | Note |
|---|---|
| Claude Code | [docs/adapters/CLAUDE_CODE_ADAPTER_NOTE.md](../../docs/adapters/CLAUDE_CODE_ADAPTER_NOTE.md) |
| Codex | [docs/adapters/CODEX_CLI_ADAPTER_NOTE.md](../../docs/adapters/CODEX_CLI_ADAPTER_NOTE.md) |
| GitHub Copilot | [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](../../docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md) |
| Gemini / Antigravity | [docs/adapters/GEMINI_ANTIGRAVITY_ADAPTER_NOTE.md](../../docs/adapters/GEMINI_ANTIGRAVITY_ADAPTER_NOTE.md) |

Adapter notes 描述 host-specific compatibility 與 limitations；它們不是寫入 global settings 或 remote services 的授權。

## 4. Resource Catalog

| Type | Logical root | Purpose |
|---|---|---|
| `skill` | `registry/skills` | Reusable skills and capability packs |
| `mcp` | `registry/mcp` | MCP definitions and adoption notes |
| `agent` | `registry/agents` | Shared personas and playbooks |
| `workflow` | `registry/workflow` | Runbooks, plan templates, and repeatable processes |

Runtime-facing catalog 是 [runtime/catalog.json](../../runtime/catalog.json)。Schema 與 metadata expectations 在 [RESOURCE_SPEC.md](../../RESOURCE_SPEC.md)。

## 5. Operations And Reports

| Task | Start here |
|---|---|
| Build or verify runtime projections | `python local/scripts/build-runtime-layer.py` |
| Bootstrap local CLI wiring | [OPERATIONS.md](../../OPERATIONS.md), then `python local/scripts/bootstrap.py --dry-run` |
| Verify workspace-sensitive boundaries | [WORKSPACE_SENSITIVE_METADATA_RULES.md](../../WORKSPACE_SENSITIVE_METADATA_RULES.md), then `python local/scripts/verify-workspace-boundaries.py --format json` |
| Check i18n drift | `python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero` |
| Export template package | [TEMPLATE_RELEASE_PACKAGE.md](../../TEMPLATE_RELEASE_PACKAGE.md), then `local/scripts/export-template-package.ps1` |

## 6. Discovery Rules

`INDEX.md` 回答：該讀哪頁、各 resource family 在哪裡、哪些 catalog excerpts 適合 review、哪些 scripts 能啟動常見本地檢查。

`INDEX.md` 不回答：最終 host-specific 絕對路徑、live machine configuration、private plans、roadmaps、review notes、operational state、或 agents 的 runtime startup context。
