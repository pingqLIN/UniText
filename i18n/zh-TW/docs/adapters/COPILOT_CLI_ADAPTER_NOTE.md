# UniText — GitHub Copilot Adapter Note

> 狀態：active baseline
> Last verified: 2026-06-04

本 note 將 UniText concepts 對應到 GitHub Copilot-facing repository surfaces。它只是 documentation，不授權 push、GitHub upload 或 public issue/PR creation。

## Supported Surfaces

| UniText concept | Copilot-facing surface | Delivery mode |
|---|---|---|
| Repo-wide instructions | `.github/copilot-instructions.md` | `native-config` |
| Path-specific instructions | `.github/instructions/*.instructions.md` | `native-config` when supported |
| Project instructions | `AGENTS.md` and repository docs | `pointer` |
| MCP definitions | project `.mcp.json` or supported Copilot MCP configuration | `native-config` |
| Skills | no general `SKILL.md` parity assumption | instruction-oriented projection |

## Current Baseline

UniText 目前追蹤：

- `.github/copilot-instructions.md`
- `.github/pull_request_template.md`
- `.mcp.json` as a template-safe project MCP seed
- `docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md` as this compatibility note

Copilot support 應描述為 instruction 與 MCP projection support，不應聲稱與 Claude/Codex skill folders 完全對等。

## Recommended Flow

1. Canonical source 留在 `registry/` 或 authoritative docs。
2. 使用 `.github/copilot-instructions.md` 放 repo-wide instructions。
3. 只有在明確 adoption path-specific instruction surface 時，才使用 `.github/instructions/`。
4. Tracked MCP examples 保持 template-safe。
5. 驗證任何 generated 或 revised GitHub-facing file 是否符合 no-publish policy。

## Constraints

- Adding GitHub templates 不代表可以 push 或 publish。
- GitHub templates 不應包含 private planning notes、strategy、social drafts、cross-project collaboration notes、review packets。
- 沒有 fresh evidence 時，不聲稱 full cross-platform Copilot support。
- 優先用 descriptive links 指到 UniText docs，不在 `.github/` 複製大量 policy body。
