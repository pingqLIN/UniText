# CLI Compatibility Matrix

> 状态：Working Draft
> 最后更新：2026-03-23

| CLI | 版本基准 | UniText 依赖行为 | 目前状态 | 最后验证 |
|---|---|---|---|---|
| Claude Code | 2.1.63 | 读取 `~/.claude/skills`、支援 project `.mcp.json` | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | 从 `config.toml` 的 `skills_path` 读取 skills，并可注册 `[mcp_servers.unitext_registry]` | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | 读取 `~/.gemini/skills` 与 `~/.agents/skills` | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | workflow 仅作参考，无 native skills 支援 | 已知限制 | 2026-03-02 |
| VS Code | 1.109.5 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |
| Windsurf | 1.108.2 | 非直接 resource consumer，主要作 authoring environment | 已知限制 | 2026-03-02 |

## Notes

- 这份矩阵记录的是 UniText 当前依赖的 CLI 行为，而不是各 CLI 的完整能力。
- 每次 major version 变更后，应至少重新验证一次 skills 与 mcp delivery。
- `delivery path verified` 代表已由 `verify-delivery.ps1` 确认 canonical skills path 对齐，并不等于完成端到端互动验证。
