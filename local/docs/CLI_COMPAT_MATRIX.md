# CLI Compatibility Matrix

> 狀態：Working Draft
> 最後更新：2026-03-25

| CLI | 版本基準 | UniText 依賴行為 | 目前狀態 | 最後驗證 |
|---|---|---|---|---|
| Claude Code | 2.1.63 | 讀取 `~/.claude/skills`、支援 project `.mcp.json` | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | 從 `config.toml` 的 `skills_path` 讀取 skills，並可註冊 `[mcp_servers.unitext_registry]` | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | 讀取 `~/.gemini/skills` 與 `~/.agents/skills` | delivery path verified | 2026-03-24 |
| Copilot CLI | 1.0.11 | 讀取 `~/.copilot/skills`、repo `.github/copilot-instructions.md`，並可透過 `~/.copilot/mcp-config.json` 註冊 shared registry MCP | bootstrap baseline verified | 2026-03-25 |
| VS Code | 1.109.5 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |
| Windsurf | 1.108.2 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |

## Notes

- 這份矩陣記錄的是 UniText 當前依賴的 CLI 行為，而不是各 CLI 的完整能力。
- 每次 major version 變更後，應至少重新驗證一次 skills 與 mcp delivery。
- `delivery path verified` 代表已由 `verify-delivery.ps1` 確認 canonical skills path 對齊，並不等於完成端到端互動驗證。
- `bootstrap baseline verified` 代表 `bootstrap.py -> verify-bootstrap.py` 已能把該 CLI 的個人 skills / MCP baseline 對齊到 UniText registry，但仍不等於所有互動式工作流都已完成端到端驗證。
- `Copilot CLI` 的目前定位、限制與後續 adapter 路線，另見 [../../COPILOT_CLI_ADAPTER_NOTE.md](../../COPILOT_CLI_ADAPTER_NOTE.md)。
