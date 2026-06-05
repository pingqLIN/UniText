# UniText — Claude Code Adapter Note

> Status: active baseline
> Last verified: 2026-06-04

This note maps UniText concepts to Claude Code-facing project surfaces. It is documentation only; it does not authorize writes to `.claude/`, global Claude settings, or MCP configuration.

## Supported Surfaces

| UniText concept | Claude-facing surface | Delivery mode |
|---|---|---|
| Shared instructions | `CLAUDE.md` or project docs | `pointer` or `native-config` |
| Skills | `.claude/skills/<skill-name>/SKILL.md` | `mirror` or `symlink` |
| MCP definitions | `.mcp.json` or managed settings | `native-config` |
| Workflows | project docs or skill support files | `pointer` or `mirror` |

## Recommended Flow

1. Keep canonical content under `registry/`.
2. Rebuild runtime projections with `python local/scripts/build-runtime-layer.py`.
3. Decide whether Claude should receive a mirrored copy, a symlink, or only a pointer.
4. Dry-run the delivery plan before touching `.claude/`.
5. Verify the target surface and preserve rollback evidence.

## Constraints

- Do not point Claude directly at `registry/skills` when the task expects a consumer runtime view.
- Prefer `runtime/skills` as the source for mirrored or linked skill delivery.
- Keep machine-local Claude settings out of shared docs unless they are sanitized examples.
- Use `NO_PUBLISH_POLICY.md` before moving Claude-related notes into publishable docs.

## Verification

Use the generic documentation and boundary checks first:

```powershell
python local/scripts/build-runtime-layer.py
python local/scripts/verify-workspace-boundaries.py --format json
```

If a delivery script writes to a Claude-owned surface, verify the target path and backup output before accepting the change.
