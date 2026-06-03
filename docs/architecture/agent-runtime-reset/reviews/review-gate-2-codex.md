# Runtime Reset Review Gate 2

> Reviewer: Codex
> Date: 2026-04-20
> Scope: runtime-reset baseline after live cutover, before legacy ingestion work starts

## Reviewed Surface

- `RUNTIME.md`
- `runtime/START.md`
- `runtime/RULES.md`
- `runtime/ROUTES.md`
- `runtime/catalog.json`
- `local/scripts/build-runtime-layer.py`
- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`
- `local/scripts/sync-skills.ps1`
- root docs and adapter docs touched by runtime-first cutover

## Findings

### 1. Medium: `bootstrap.py` still rewrote tracked `.mcp.json` into machine-specific form

Evidence before fix:

- repo policy already treated tracked `.mcp.json` as a template-safe relative-path seed
- live `bootstrap.py --force` still rendered repo-root `.mcp.json` with machine-local interpreter and absolute repo path
- current cutover therefore required manual restoration of `.mcp.json` after bootstrap

Impact:

- repeated local bootstrap could reintroduce machine-specific tracked drift
- runtime-reset baseline stayed semantically inconsistent: docs said “keep the seed”, implementation said “rewrite the seed”

Resolution:

- `local/scripts/bootstrap.py` now renders the tracked project MCP file as the template-safe seed
- project MCP change detection now compares parsed JSON bodies, so no-op rewrites do not fire just because of trailing newline differences
- main docs and MCP seed docs were aligned to the new behavior

### 2. Medium: `verify-bootstrap.py` did not share bootstrap’s home-directory fallback logic

Evidence before fix:

- `bootstrap.py` already had a guarded `get_home_dir()` fallback for `Path.home()` failure cases
- `verify-bootstrap.py` still called `Path.home()` directly in multiple places

Impact:

- on the same environment where bootstrap had to fall back, verify could still fail even though delivery was correct
- this broke the intended `bootstrap -> verify` contract on edge-case hosts

Resolution:

- `local/scripts/verify-bootstrap.py` now reuses the same fallback strategy as bootstrap
- all home-scoped target paths are derived from the resolved home directory once

## Verification

Executed after fixes:

- `python -m py_compile Q:\UniText\local\scripts\build-runtime-layer.py Q:\UniText\local\scripts\bootstrap.py Q:\UniText\local\scripts\verify-bootstrap.py`
- `python Q:\UniText\local\scripts\build-runtime-layer.py --write`
- `python Q:\UniText\local\scripts\bootstrap.py --dry-run`
- `python Q:\UniText\local\scripts\verify-bootstrap.py`

Observed result:

- `verify-bootstrap.py` returned `"ok": true`
- `bootstrap.py --dry-run` reported `project_mcp.mode = "template-seed"` and `project_mcp.changed = false`

## Gate Result

Pass.

No additional blocking defects remain in the reviewed runtime-reset baseline after the fixes above.

## Deferred But Known

- `i18n/*` still contains startup-language drift and was intentionally left for a later pass
- the 20-task runtime acceptance suite baseline exists but was not rerun as a full multi-agent evaluation in this review
- profile-specific runtime bundles (`core` / `default` / `full`) remain future work, not part of the current baseline gate
