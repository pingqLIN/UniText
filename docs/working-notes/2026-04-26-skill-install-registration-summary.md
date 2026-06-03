# Skill Install / Registration Summary

Date: 2026-04-26

## What was clarified

- `install skill` is the Codex skill installer flow for materializing skills into the Codex home skills library.
- The installer target is the machine-local Codex skills directory, not the UniText authoring tree.
- UniText keeps `registry/` as the canonical authoring source and `runtime/` as the consumer-facing read model.

## Current UniText contract

- `registry/skills` is the canonical shared skill source.
- `runtime/skills` is the projected runtime surface rebuilt from `registry/`.
- Codex should read its configured `skills_path` target only.
- Codex should not be pointed at `registry/skills` in steady state.
- Bootstrap and verify logic should treat direct `registry/skills` wiring as a mismatch.

## Practical consequence

- If a skill is installed through the Codex installer, it lands in the Codex home skills path.
- If a skill is governed inside UniText, it belongs in `registry/skills`, then gets projected into `runtime/skills`.
- Those two flows are related but not identical.
- If the active `skills_path` and the installer destination diverge, Codex runtime load and install output will drift apart.

## Stage 2 Mutation Boundaries

Stage 2 should separate registration from host takeover:

- `python local/scripts/build-runtime-layer.py --write`
  - rewrites tracked `runtime/` from `registry/`
  - does not modify `~/.codex/`
- `python local/scripts/bootstrap.py --dry-run`
  - reports the planned home-target changes
  - does not modify `~/.codex/`
- `python local/scripts/bootstrap.py --force`
  - backs up existing home targets under `ops/history/bootstrap_*`
  - syncs `runtime/skills` into `~/.codex/skills`
  - updates `~/.codex/config.toml` so `skills_path` points at the Codex-local skills target
  - removes legacy global `[mcp_servers.unitext_registry]` from Codex config when present
  - may update other declared CLI targets such as `~/.claude/skills`, `~/.gemini/skills`, `~/.agents/skills`, `~/.copilot/mcp-config.json`, and the project `.mcp.json`
- `python local/scripts/bootstrap.py --force --skip-codex`
  - keeps repo/runtime work separate from local Codex config remediation
  - should be preferred when the task is only registry/runtime registration

## Runtime Restore Rule

`runtime/` is a generated and reviewed read model. To restore it from the canonical project baseline:

1. Confirm the worktree state first.
2. Move the current `runtime/` aside only when preserving drift evidence is useful.
3. Run `python local/scripts/build-runtime-layer.py --write`.
4. Run `python local/scripts/verify-bootstrap.py --skip-codex` for repo-side validation when local Codex config should not be touched.
5. Run the full `python local/scripts/verify-bootstrap.py` only when host `.codex` wiring is intentionally part of the task.

Deleting `runtime/` is not a recovery mechanism by itself. The recovery mechanism is regeneration from `registry/` through `build-runtime-layer.py`, followed by verification.

## Relevant repo entry points

- `RUNTIME.md`
- `README.md`
- `local/config/integration-surfaces.json`
- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`
- `local/scripts/register-codex-skills.py`
- `local/scripts/README.md`
