# CLI Compatibility Matrix

> 狀態：Working Draft
> 最後更新：2026-03-23

| CLI | 版本基準 | UniText 依賴行為 | 目前狀態 | 最後驗證 |
|---|---|---|---|---|
| Claude Code | 2.1.63 | 讀取 `~/.claude/skills`、支援 project `.mcp.json` | Windows host delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | 從 `config.toml` 的 `skills_path` 讀取 machine-local runtime target，並可註冊 `[mcp_servers.unitext_registry]` | Windows host runtime bootstrap baseline verified | 2026-04-20 |
| Gemini CLI | 0.31.0 | 讀取 `~/.gemini/skills` 與 `~/.agents/skills` | Windows host delivery path verified | 2026-03-24 |
| Copilot CLI | 1.0.12 | 讀取 `AGENTS.md` / related instructions，並可透過 `~/.copilot/mcp-config.json` 註冊 `unitext-registry` | Windows host bootstrap baseline verified | 2026-04-02 |
| VS Code | 1.109.5 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |
| Windsurf | 1.108.2 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |

## Notes

- 這份矩陣記錄的是 UniText 當前依賴的 CLI 行為，而不是各 CLI 的完整能力。
- 每次 major version 變更後，應至少重新驗證一次 skills 與 mcp delivery。
- `delivery path verified` 代表已由驗證腳本確認 machine-local skills target 對齊 runtime source，並不等於完成端到端互動驗證。
- `bootstrap baseline verified` 代表目前 authoring host 已有 repo-level bootstrap + verify 證據，但不自動等於所有平台都完成驗證。
- 截至目前，只有 `Windows / PC` 完成較完整的 authoring-host 驗證；`macOS` 與 `Linux` 仍屬目標平台，而非已完整驗證平台。
- `Copilot CLI` 的目前定位、限制與後續 adapter 路線，另見 [../../docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](../../docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md)。
