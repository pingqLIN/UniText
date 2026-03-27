# CLI Compatibility Matrix

> 狀態：Working Draft
> 最後更新：2026-03-27

| CLI / Surface | 版本基準 | UniText 依賴行為 | Support Class | Verification Scope | 最後驗證 |
|---|---|---|---|---|---|
| Claude Code | 2.1.63 | 讀取 `~/.claude/skills`、支援 project `.mcp.json` | `verified` | `delivery path verified` | 2026-03-27 |
| Codex CLI | 0.106.0 | 從 `config.toml` 的 `skills_path` 讀取 skills，並可註冊 `[mcp_servers.unitext_registry]` | `partial` | `bootstrap path defined` | 2026-03-27 |
| Gemini CLI | 0.31.0 | 讀取 `~/.gemini/skills` 與 `~/.agents/skills` | `verified` | `delivery path verified` | 2026-03-27 |
| Copilot CLI | target baseline | 目標是消費 shared MCP / skill baseline，但目前尚無已固定的 repo-level adapter 路徑 | `target` | `adapter pending` | 未驗證 |
| VS Code | 1.109.5 | 非直接 resource consumer，主要作 authoring environment | `partial` | `authoring environment only` | 2026-03-02 |
| Windsurf | 1.108.2 | 非直接 resource consumer，主要作 authoring environment | `partial` | `authoring environment only` | 2026-03-02 |

## Notes

- 這份矩陣記錄的是 UniText 當前依賴的 CLI 行為，而不是各 CLI 的完整能力。
- 每次 major version 變更後，應至少重新驗證一次 skills 與 mcp delivery。
- `verified` 代表 repo 內已有可重跑證據支撐該 verification scope，不等於自動涵蓋所有操作情境。
- `partial` 代表已有實作與部分驗證，但 repo 尚未聲稱 full end-to-end readiness。
- `target` 代表該 CLI 或平台屬於 starter template 目標面，尚未在 repo 內完成驗證。
- `delivery path verified` 代表 canonical skills path 與 project-local wiring 已被驗證，並不等於完成端到端互動驗證。
- `bootstrap path defined` 代表 bootstrap 與 native-config 路徑已在 repo 中定義，但不應被讀成 fresh-machine end-to-end verified。
- `adapter pending` 代表該 CLI 已列入 starter template 目標，但目前只定義目標方向，尚未在 repo 內固定交付方式。
- proof artifact 對照另見 [SUPPORT_PROOF_MATRIX.md](SUPPORT_PROOF_MATRIX.md)。
- 目前 README 與 release files 另外區分三類材料：
  - `authoring review shortlist`
  - `public release subset`
  - `local-only validation materials`
- `Copilot CLI` 的目前定位、限制與後續 adapter 路線，另見 [../../COPILOT_CLI_ADAPTER_NOTE.md](../../COPILOT_CLI_ADAPTER_NOTE.md)。
