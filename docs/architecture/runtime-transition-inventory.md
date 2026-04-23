# Runtime Transition Inventory

> Status: active inventory
> Date: 2026-04-20
> Purpose: classify which files are part of the current runtime-first baseline, which files remain active follow-on planning, and which files were only legacy design inputs.

## Current Runtime Baseline

These files now define the active runtime-first architecture and should remain in the normal read path:

- [RUNTIME.md](../../RUNTIME.md)
- [runtime/START.md](../../runtime/START.md)
- [runtime/RULES.md](../../runtime/RULES.md)
- [runtime/ROUTES.md](../../runtime/ROUTES.md)
- [runtime/catalog.json](../../runtime/catalog.json)
- `runtime/skills/*`, `runtime/agents/*`, `runtime/workflow/*`
- [local/scripts/build-runtime-layer.py](../../local/scripts/build-runtime-layer.py)
- [local/scripts/bootstrap.py](../../local/scripts/bootstrap.py)
- [local/scripts/verify-bootstrap.py](../../local/scripts/verify-bootstrap.py)
- [local/scripts/sync-skills.ps1](../../local/scripts/sync-skills.ps1)
- [README.md](../../README.md)
- [INDEX.md](../../INDEX.md)
- [OPERATIONS.md](../../OPERATIONS.md)
- [local/docs/CLI_COMPAT_MATRIX.md](../../local/docs/CLI_COMPAT_MATRIX.md)
- [registry/skills/conversation-memo](../../registry/skills/conversation-memo/SKILL.md)
- [registry/skills/obsidian-index-adapter](../../registry/skills/obsidian-index-adapter/SKILL.md)

## Active Follow-on Planning

These files are not part of the startup/runtime baseline, but remain active because they describe the next stream of work rather than the retired design debate:

- [legacy-ingestion-modernization-plan.md](legacy-ingestion-modernization-plan.md)

## Archived Design Inputs

The following source set was useful during the runtime reset decision, but is no longer part of the active architecture surface:

- `.del/agent-runtime-reset/final-runtime-reset.md`
- `.del/agent-runtime-reset/template1-brief.md`
- `.del/agent-runtime-reset/template2-a.md`
- `.del/agent-runtime-reset/template2-b.md`
- `.del/agent-runtime-reset/template2-c.md`
- `.del/agent-runtime-reset/template2-d.md`
- `.del/agent-runtime-reset/template2-e.md`
- `.del/agent-runtime-reset/template3-winner.md`
- `.del/agent-runtime-reset/reviews/ballot-*.md`
- `.del/agent-runtime-reset/reviews/score-summary.md`
- `.del/agent-runtime-reset/reviews/review-gate-2-codex.md`

These files were archived because they are design-stage materials, not the ongoing runtime contract. Their applicable content has been condensed into [runtime-baseline-history.md](runtime-baseline-history.md).

## Not Adopted Into The Shared Baseline

The following source-side item was intentionally not brought into the active baseline:

- `Q:\\UniText\\local\\scripts\\register-codex-skills.py`

Reason:

- it is a machine-local recovery utility
- it contains migration-era assumptions that are not part of the shared runtime contract
- the shared baseline already uses `build-runtime-layer.py` plus `bootstrap.py` / `verify-bootstrap.py`

## Reading Rule

Use this order when reasoning about the current architecture:

1. `RUNTIME.md`
2. `runtime/*`
3. runtime-related root docs and script docs
4. `runtime-baseline-history.md` when you need decision background
5. archived `.del/agent-runtime-reset/*` only when reconstructing the earlier design debate
