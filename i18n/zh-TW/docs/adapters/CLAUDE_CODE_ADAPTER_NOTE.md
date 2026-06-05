# UniText — Claude Code Adapter Note

> 狀態：active baseline
> Last verified: 2026-06-04

本 note 將 UniText concepts 對應到 Claude Code-facing project surfaces。它只是 documentation，不授權寫入 `.claude/`、global Claude settings 或 MCP configuration。

## Supported Surfaces

| UniText concept | Claude-facing surface | Delivery mode |
|---|---|---|
| Shared instructions | `CLAUDE.md` or project docs | `pointer` or `native-config` |
| Skills | `.claude/skills/<skill-name>/SKILL.md` | `mirror` or `symlink` |
| MCP definitions | `.mcp.json` or managed settings | `native-config` |
| Workflows | project docs or skill support files | `pointer` or `mirror` |

## Recommended Flow

1. Canonical content 留在 `registry/`。
2. 使用 `python local/scripts/build-runtime-layer.py` rebuild runtime projections。
3. 決定 Claude 要收到 mirrored copy、symlink，或只收到 pointer。
4. 碰 `.claude/` 前先 dry-run delivery plan。
5. Verify target surface 並保留 rollback evidence。

## Constraints

- Consumer runtime tasks 不應讓 Claude 直接指向 `registry/skills`。
- Mirrored 或 linked skill delivery 優先從 `runtime/skills` 出發。
- Machine-local Claude settings 不應進 shared docs，除非是 sanitized examples。
- 把 Claude notes 移進 publishable docs 前，先看 `NO_PUBLISH_POLICY.md`。
