# UniText — GitHub Copilot Adapter Note

> Status: active baseline
> Last verified: 2026-06-04

This note maps UniText concepts to GitHub Copilot-facing repository surfaces. It is documentation only; it does not authorize pushes, GitHub uploads, or public issue/PR creation.

## Supported Surfaces

| UniText concept | Copilot-facing surface | Delivery mode |
|---|---|---|
| Repo-wide instructions | `.github/copilot-instructions.md` | `native-config` |
| Path-specific instructions | `.github/instructions/*.instructions.md` | `native-config` when supported |
| Project instructions | `AGENTS.md` and repository docs | `pointer` |
| MCP definitions | project `.mcp.json` or supported Copilot MCP configuration | `native-config` |
| Skills | no general `SKILL.md` parity assumption | instruction-oriented projection |

## Current Baseline

UniText currently tracks:

- `.github/copilot-instructions.md`
- `.github/pull_request_template.md`
- `.mcp.json` as a template-safe project MCP seed
- `docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md` as this compatibility note

Copilot support should be described as instruction and MCP projection support, not as full parity with Claude/Codex skill folders.

## Recommended Flow

1. Keep canonical source under `registry/` or the authoritative docs.
2. Use `.github/copilot-instructions.md` for repo-wide instructions.
3. Use `.github/instructions/` only when a path-specific instruction surface is intentionally adopted.
4. Keep tracked MCP examples template-safe.
5. Verify any generated or revised GitHub-facing file against the no-publish policy.

## Constraints

- Adding GitHub templates does not grant permission to push or publish.
- Do not include private planning notes, strategy, social drafts, cross-project collaboration notes, or review packets in GitHub templates.
- Do not claim full cross-platform Copilot support without fresh evidence.
- Prefer descriptive links to UniText docs over copying large policy bodies into `.github/`.

## Verification

```powershell
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/get-publishability-report.py
python -m unittest tests.security.test_release_hygiene
```
