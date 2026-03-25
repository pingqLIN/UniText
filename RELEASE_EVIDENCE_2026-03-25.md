# Release Evidence 2026-03-25

## Scope

This evidence bundle covers the interrupted-run / release-integrity hardening work completed on 2026-03-25.

The implementation goal was to prevent false-success release artifacts when an operator or AI agent is interrupted mid-run, and to make bootstrap/export/verify flows produce auditable completion state rather than ambiguous partial output.

## Commit Boundary

Recommended commit scope for the implementation commit:

- `local/scripts/bootstrap.py`
- `local/scripts/export-template-package.ps1`
- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-bootstrap.py`
- `local/scripts/verify-template-package.ps1`
- `local/scripts/verify-rebuild-project.ps1`
- `local/scripts/lib/release-integrity.ps1`
- `tests/security/test_hardening.py`
- `tests/security/test_interrupted_run_integrity.py`

Recommended optional follow-up documentation commit:

- `FINAL_RELEASE_DEVELOPMENT_PLAN_2026-03-25.md`
- `RELEASE_EVIDENCE_2026-03-25.md`

## Exclusions

The following files should stay out of the implementation commit because they are environment-local, generated, or unrelated noise:

- `.mcp.json`
  This was rewritten by local `bootstrap.py --force` to machine-specific absolute paths and is verification evidence, not portable source.
- `ops/history/bootstrap_20260325_175121_478901/`
- `ops/history/bootstrap_20260325_175216_250548/`
  These runs are ignored by `.gitignore` and should remain evidence only.
- `local/scripts/scan-skills.ps1`
  Pre-existing unrelated modification.
- The large unrelated dirty-tree set under `i18n/`, `registry/skills/`, images, PSD assets, and security review drafts.

## Delivered Changes

### 1. Release export integrity

- Template and rebuild export now write into staging directories first.
- `manifest.json`, `release.json`, and `generation-state.json` are written atomically.
- Completion is represented explicitly with:
  - `generation_state`
  - `completed_at`
  - `completion_marker`
  - `source_commit`
  - `workspace_dirty`
- Final package paths are finalized only after metadata and content are complete.

### 2. Verifier hardening

- Template and rebuild verifiers now validate:
  - required files
  - forbidden residual paths
  - release target
  - generation state
  - relative path discipline
  - item count consistency
  - expected verifier binding
- Staging-like or incomplete packages are rejected.

### 3. Bootstrap integrity

- `bootstrap.py` now uses atomic writes for:
  - `config.toml`
  - `.mcp.json`
  - `state.json`
  - `summary.json`
- Bootstrap runs now record step-by-step execution state and fail closed.
- `verify-bootstrap.py` now performs structural validation instead of substring checks.
- The Codex `skills_path` write path was corrected so it lands at top-level TOML, not inside `[tui]`.

### 4. Test coverage

- PowerShell-dependent tests now skip cleanly when `pwsh` is unavailable.
- Added isolated bootstrap integrity coverage.
- Added interrupted metadata rejection coverage.

## Validation Evidence

### Local validation completed in this environment

- `python3 -m py_compile local/scripts/bootstrap.py local/scripts/verify-bootstrap.py`
  Result: passed
- `python3 -m unittest tests.security.test_hardening`
  Result: passed, 7 tests, 3 skipped
- `python3 -m unittest tests.security.test_interrupted_run_integrity`
  Result: passed, 4 tests, 2 skipped
- `python3 local/scripts/bootstrap.py --dry-run`
  Result: passed, reported `generation_state = "dry_run"`
- `python3 local/scripts/bootstrap.py --force`
  Result: passed
- `python3 local/scripts/verify-bootstrap.py`
  Result: passed with `"ok": true`

### Bootstrap evidence chain

Latest successful local bootstrap run:

- `ops/history/bootstrap_20260325_175216_250548/summary.json`

Observed state:

- `generation_state = "complete"`
- `current_step = "finalize"`
- all planned steps marked `complete`
- skills targets aligned:
  - `/root/.claude/skills`
  - `/root/.gemini/skills`
  - `/root/.agents/skills`

### PowerShell execution evidence

The PowerShell implementation line was additionally verified by the execution subagent on Windows PowerShell 7:

- template export passed
- template verify passed
- rebuild export passed
- rebuild verify passed

This matters because the current local Linux environment does not provide `pwsh`, so direct PowerShell runtime validation is only partially available here.

## Suggested Commit Plan

Implementation commit:

```bash
git -C /mnt/q/UniText add \
  local/scripts/bootstrap.py \
  local/scripts/export-template-package.ps1 \
  local/scripts/export-rebuild-project.ps1 \
  local/scripts/verify-bootstrap.py \
  local/scripts/verify-template-package.ps1 \
  local/scripts/verify-rebuild-project.ps1 \
  local/scripts/lib/release-integrity.ps1 \
  tests/security/test_hardening.py \
  tests/security/test_interrupted_run_integrity.py
```

Suggested commit message:

```text
harden release integrity and interrupted-run verification
```

Optional documentation commit:

```bash
git -C /mnt/q/UniText add \
  FINAL_RELEASE_DEVELOPMENT_PLAN_2026-03-25.md \
  RELEASE_EVIDENCE_2026-03-25.md
```

Suggested commit message:

```text
document final release plan and evidence bundle
```

## Go / No-Go

For this workstream alone, the status is `GO`.

Reasons:

- bootstrap integrity is now verifiable
- release export state is no longer ambiguous
- incomplete artifacts are rejectable
- test coverage exists for the most important non-happy-path cases

This does not mean the whole repository is release-clean. It means the interrupted-run / release-integrity workstream is now implemented, validated, and separable for commit and review.

For the remaining dirty worktree, use `local/scripts/report-release-hygiene.py` to separate release-scope changes from machine-specific, generated, and stray blocker categories before deciding the next commit boundary.
