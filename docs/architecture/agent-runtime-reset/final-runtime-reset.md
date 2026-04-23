# UniText Runtime Reset — Final Reviewed Version

## Decision

UniText keeps `registry/` as the only canonical authoring source, introduces a tracked repo `runtime/` layer as the consumer-facing read model, and wires every CLI to machine-local targets that are rebuilt from `runtime/`, not from `registry/skills`.

This final version starts from the winning [template3-winner.md](template3-winner.md) direction, then integrates the strongest implementation detail from `template2-d.md` so the design matches what is actually shipped in this repo now.

## Final Architecture

| Layer | Role | Canonical | Mutability |
|---|---|---:|---:|
| `registry/` | Shared authoring source for skills, MCP, agents, workflow | Yes | Human-edited |
| `runtime/` | Tracked runtime read model, runtime entry docs, catalog, and skill projections | No | Generated + reviewed |
| machine-local targets | `~/.codex/skills`, `~/.claude/skills`, `~/.gemini/skills`, `~/.agents/skills` | No | Bootstrap-managed |
| `local/` | Bootstrap, verify, adapters, path maps, governance scripts | No | Human-edited |
| `ops/` | Evidence, backups, drift reports, acceptance output | No | Generated / append-only |

### Key rules

- No CLI should directly consume `registry/skills` in steady state.
- `runtime/` is the default first-read surface for consumer agents.
- `README.md` and `INDEX.md` remain human discovery docs, not runtime startup docs.
- `unitext-registry` remains the deep discovery backplane. It is not the default activation surface.
- Machine-local delivery stays reversible and audited.

## Runtime Surface

### Agent startup order

1. `RUNTIME.md`
2. `runtime/START.md`
3. `runtime/RULES.md`
4. `runtime/ROUTES.md`
5. `runtime/catalog.json`

### Runtime contents

- `RUNTIME.md`
  - stable root entrypoint for consumer agents
- `runtime/START.md`
  - shortest runtime startup instructions
- `runtime/RULES.md`
  - condensed safety and boundary rules for runtime work
- `runtime/ROUTES.md`
  - intent-to-entrypoint map
- `runtime/catalog.json`
  - machine-readable runtime inventory
- `runtime/skills/*/SKILL.md`
  - runtime projections that point back to canonical sources
- `runtime/agents/*/AGENT.md`
  - runtime projections for shared agents
- `runtime/workflow/*/WORKFLOW.md`
  - runtime projections for workflow entries

## Delivery Contract

### Current implementation

- `local/scripts/build-runtime-layer.py`
  - rebuilds tracked `runtime/` from canonical `registry/`
- `local/scripts/bootstrap.py`
  - rebuilds `runtime/`
  - aligns `~/.claude/skills`, `~/.gemini/skills`, and `~/.agents/skills` to `runtime/skills`
  - aligns Codex to `~/.codex/skills`
  - sets Codex `skills_path` to the Codex-local target, not to `registry/skills`
  - keeps `unitext-registry` MCP registration in place for deep discovery
- `local/scripts/verify-bootstrap.py`
  - fails when any target still points to `registry/skills`
  - verifies Codex `skills_path` against `~/.codex/skills`
  - verifies the local targets resolve to `runtime/skills`

### Explicitly rejected steady-state

- Codex `skills_path = ...registry/skills`
- treating `README.md` or `INDEX.md` as the default startup surface
- using runtime projections as new canonical source-of-truth

## Why this version

The winning template argued for a dedicated runtime root plus profile-oriented materialization. That is directionally correct, but the repo already benefits from a tracked `runtime/` layer that can be reviewed, committed, and used as the shared low-noise entrypoint.

This final version therefore takes a staged approach:

1. Stage 1, implemented now:
   - tracked repo `runtime/`
   - machine-local skill targets
   - runtime-first docs and catalog
   - bootstrap/verify cutover away from direct `registry/skills`
2. Stage 2, future enhancement if needed:
   - profile-specific local runtime bundles
   - `current` pointer semantics or per-profile local packs
   - richer apply/rollback runtime controls

That keeps the reset incremental and reviewable while still fixing the core leak: consumer agents defaulting into authoring surfaces.

## Acceptance Suite

The repo now carries the first runtime validation bundle under `runtime/validation/`:

- `tasks.md`
- `observer-guide.md`
- `scorecard.template.json`

These 20 tasks are the baseline for future subagent evaluation and drift checks. The suite explicitly checks:

- startup can begin from runtime entry docs
- default paths do not require `README.md` or `INDEX.md`
- runtime targets do not point back to `registry/skills`
- runtime inventory remains low-noise and machine-readable
- verification names the exact failing layer when cutover regresses

## Follow-up

The next iteration should add:

- profile metadata for `core`, `default`, and `full`
- stricter runtime budget checks in verify
- optional profile-specific local materialization when the tracked `runtime/` layer is not enough
- scripted execution of the 20-task suite with evidence written to `ops/`

Related follow-on artifacts:

- review gate closure: [reviews/review-gate-2-codex.md](reviews/review-gate-2-codex.md)
- legacy stream split plan: [../legacy-ingestion-modernization-plan.md](../legacy-ingestion-modernization-plan.md)
