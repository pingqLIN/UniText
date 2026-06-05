# UniText — Codex Adapter Note

> Status: active baseline
> Last verified: 2026-06-04

This note maps UniText concepts to Codex-facing project surfaces. It is documentation only; it does not authorize global Codex configuration changes.

## Supported Surfaces

| UniText concept | Codex-facing surface | Delivery mode |
|---|---|---|
| Project instructions | `AGENTS.md` and project docs | `pointer` |
| Skills | configured `skills_path` or `.agents/skills` | `symlink` or `mirror` |
| MCP definitions | `.codex/config.toml`, `codex mcp`, or project MCP seed | `native-config` |
| Runtime catalog | `runtime/catalog.json` | `pointer` |

## Recommended Flow

1. Start from [RUNTIME.md](../../RUNTIME.md), not the full registry.
2. Rebuild runtime projections with `python local/scripts/build-runtime-layer.py`.
3. Preview delivery with `python local/scripts/bootstrap.py --dry-run`.
4. Apply only with `python local/scripts/bootstrap.py --force` after review.
5. Verify with `python local/scripts/verify-bootstrap.py`.

## Constraints

- Codex should consume the runtime projection or configured local skill target, not deep registry source by default.
- Do not silently write global `~/.codex/config.toml` from shared documentation.
- Keep project `.mcp.json` template-safe and avoid absolute machine paths in tracked config.
- Treat `runtime/catalog.json` as generated runtime inventory. Do not hand-edit it for docs-only changes.

## Verification

```powershell
python local/scripts/build-runtime-layer.py
python local/scripts/bootstrap.py --dry-run
python local/scripts/verify-bootstrap.py
python local/scripts/verify-workspace-boundaries.py --format json
```
