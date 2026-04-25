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

## Relevant repo entry points

- `RUNTIME.md`
- `README.md`
- `local/config/integration-surfaces.json`
- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`
- `local/scripts/register-codex-skills.py`
- `local/scripts/README.md`

