# Release Evidence 2026-03-26

## Scope

This evidence bundle captures the current release-gating baseline after aligning release hygiene tooling, adding Copilot session verification, and collecting a repeatable local evidence chain.

## Environment

- generated_at: `2026-03-26T00:27:44`
- repo_root: `/mnt/q/UniText`
- pwsh_available: `false`
- copilot_available: `true`

## Verification Summary

- `verify_bootstrap`: `ok`
- `security_tests`: `ok`
- `i18n_wave`: `ok`
- `release_hygiene`: `not_ok`
- `unitext_mcp_smoke`: `ok`
- `copilot_session`: `not_ok`

## Key Findings

- `verify-bootstrap.py` status: `true`
- `report-i18n-wave.py` safe_to_split: `true`
- `report-release-hygiene.py` blockers: `314`
- `unitext-registry` manual MCP initialize smoke: `true`
- Copilot final payload parsed: `true`
- Copilot `unitext-registry` status during prompt: `failed`

## PowerShell Boundary

- `pwsh` is not available in this Linux/WSL environment, so `export-template-package.ps1` and `verify-template-package.ps1` were not re-run here.
- Existing PowerShell-backed template export remains a documented boundary rather than freshly collected evidence in this run.

## Raw Commands

- `verify_bootstrap`: `/usr/bin/python3 local/scripts/verify-bootstrap.py`
- `security_tests`: `/usr/bin/python3 -m unittest discover -s tests/security -v`
- `i18n_wave`: `/usr/bin/python3 local/scripts/report-i18n-wave.py --json`
- `release_hygiene`: `/usr/bin/python3 local/scripts/report-release-hygiene.py --json`
- `unitext_mcp_smoke`: `python3 registry/mcp/claude-project-mcp-seed/server.py --root /mnt/q/UniText`
- `copilot_session`: `/usr/bin/python3 local/scripts/verify-copilot-session.py --use-project-mcp`
