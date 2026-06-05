# UniText — Codex Adapter Note

> 狀態：active baseline
> Last verified: 2026-06-04

本 note 將 UniText concepts 對應到 Codex-facing project surfaces。它只是 documentation，不授權 global Codex configuration changes。

## Supported Surfaces

| UniText concept | Codex-facing surface | Delivery mode |
|---|---|---|
| Project instructions | `AGENTS.md` and project docs | `pointer` |
| Skills | configured `skills_path` or `.agents/skills` | `symlink` or `mirror` |
| MCP definitions | `.codex/config.toml`, `codex mcp`, or project MCP seed | `native-config` |
| Runtime catalog | `runtime/catalog.json` | `pointer` |

## Recommended Flow

1. 從 [RUNTIME.md](../../../../RUNTIME.md) 開始，而不是 full registry。
2. 使用 `python local/scripts/build-runtime-layer.py` rebuild runtime projections。
3. 使用 `python local/scripts/bootstrap.py --dry-run` preview delivery。
4. Review 後才用 `python local/scripts/bootstrap.py --force` apply。
5. 使用 `python local/scripts/verify-bootstrap.py` verify。

## Constraints

- Codex 預設應 consume runtime projection 或 configured local skill target，不直接 deep-read registry source。
- 不從 shared documentation 靜默寫入 global `~/.codex/config.toml`。
- Project `.mcp.json` 保持 template-safe，避免 tracked config 出現 machine absolute paths。
- `runtime/catalog.json` 是 generated runtime inventory；docs-only changes 不手動編輯。
