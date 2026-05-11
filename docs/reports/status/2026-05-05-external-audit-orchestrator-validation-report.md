# external-audit-orchestrator Validation Report And Development Plan

Date: 2026-05-05
Status: implemented and smoke-validated
Scope: `registry/skills/external-audit-orchestrator`, `runtime/skills/external-audit-orchestrator`, Codex local skill mirror, runtime projection support files, and the release smoke entrypoint.

## Executive Summary

`external-audit-orchestrator` now has a repeatable smoke entrypoint at `validation/run-smoke.ps1`.

The validation result is positive:

- Registry skill flow: pass.
- Runtime skill flow: pass.
- Codex mirror required support files: pass.
- External-audit-orchestrator runtime projection dry-run parity: pass.
- Global runtime dry-run drift: warning only, limited to unrelated runtime-local/manual surfaces outside this commit boundary.
- PowerShell parser checks: pass under Windows PowerShell and PowerShell 7 when `pwsh` is available.
- Packet scope variants: `WorkingTree`, `Staged`, `CommitRange`, `Path`, and `Manual` all have explicit pass evidence.

The main functional gap found during this pass was not the skill scripts themselves. It was that `references/release-checklist.md` already required `validation/run-smoke.ps1`, but the repository did not contain that runner. The runner has been added so the checklist now points to an executable validation path.

## Validation Design

The validation design covers three consumer paths:

1. Source-of-truth path: `registry/skills/external-audit-orchestrator`.
2. Repo runtime projection path: `runtime/skills/external-audit-orchestrator`.
3. Local Codex mirror path: `C:\Users\miles\.codex\skills\external-audit-orchestrator`.

The checks cover:

- Projection contract: PowerShell scripts and JSON assets exist in runtime while excluded metadata such as `desktop.ini` is not projected.
- Runtime parity: generated runtime dry-run output is clean against tracked runtime.
- Script syntax: parser checks for every skill `.ps1` script.
- Operational flows: packet build, report normalization, Claude reviewer bundle export, TB2 request export, and unified flow routing.
- Scope handling: `WorkingTree`, `Staged`, `CommitRange`, `Path`, and `Manual`.
- Mirror readiness: required Codex mirror files exist without mutating user config.

## Implemented Development Work

Added:

- `validation/run-smoke.ps1`

Updated:

- `local/scripts/build-runtime-layer.py`

The runtime builder now has a Windows fallback for directories that cannot be removed because another process is using them as its current working directory. In that case, it clears the directory children and continues rebuilding the runtime payload.

The runner performs:

- `python -m unittest tests.test_runtime_support_projection`
- `python local/scripts/build-runtime-layer.py --output-dir runtime/.runtime-dryrun-external-audit-smoke`
- parser checks for registry and runtime skill scripts
- optional PowerShell 7 parser checks when `pwsh` exists
- registry and runtime end-to-end smoke flows using separate fixture projects
- packet scope variant smoke checks
- Codex mirror support-file existence checks
- runtime-projected Markdown relative link existence checks

The runner uses temporary git fixtures under the system temp directory and removes generated smoke artifacts by default.
It parses the runtime dry-run JSON and fails unless `diff_summary.status` is `clean` and the write gate allows routine writes.

## Verification Results

Commands run from `Q:\UniText`:

```powershell
python -m unittest tests.test_runtime_support_projection
```

Result: pass, 2 tests.
Later updated result: pass, 3 tests after adding runtime Markdown link-existence coverage.
Latest focused result: pass, 12 tests when run with `tests.test_runtime_layer_diff_summary`.

```powershell
python local\scripts\build-runtime-layer.py --output-dir runtime\.runtime-dryrun-external-audit-check
```

Result: pass, `diff_summary.status` was `clean`.

```powershell
python local\scripts\build-runtime-layer.py --write
```

Result: pass. This also validated the Windows current-directory lock fallback in the runtime builder.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\validation\run-smoke.ps1 -SkipCodexMirror
```

Result: pass. All smoke checks completed successfully.
The smoke runner now gates `external-audit-orchestrator` registry/runtime projection parity directly and reports unrelated global runtime drift as a warning.

Manual pre-run checks also passed for:

- registry and runtime flow parity
- `WorkingTree`, `Staged`, `CommitRange`, `Path`, and `Manual` packet scopes
- Codex mirror presence of `SKILL.md`, `scripts/build-audit-packet.ps1`, `scripts/run-external-audit-flow.ps1`, `assets/tb2/tb2-audit-request.template.json`, and `assets/claude/settings.audit.json`

## Development Plan

Completed:

1. Confirm dirty worktree and avoid overwriting unrelated changes.
2. Read current skill instructions, scripts, release checklist, projection builder, and existing projection tests.
3. Design a validation matrix for code, projection, runtime, mirror, and operational calls.
4. Execute baseline tests and smoke checks.
5. Add the missing release smoke runner.
6. Re-run the complete smoke runner successfully.
7. Send the report and plan to reviewer agents.
8. Fix release reviewer findings:
   - runtime dry-run parity now fails on `diff_summary.status != clean`
   - registry and runtime flow smoke use separate fixture projects
   - PowerShell 7 parser checks cover both registry and runtime scripts
   - release checklist documents `-SkipCodexMirror` for portable/CI environments
9. Add runtime Markdown relative link-existence coverage.
10. Add no-TB2 fallback guidance:
   - TB2 template export remains a handoff artifact only.
   - `same-provider-subagent` is the default fallback when live TB2 reviewer tools are unavailable.
   - `external-web` is the visible human-supervised fallback when no local subagent path exists.
11. Harden smoke/runtime checks for local overlay and Windows filesystem behavior:
   - ignore local metadata files such as `desktop.ini`
   - preserve runtime-local `source-command*` skills and `heartbeat-protocol` workflow overlay
   - use unique dry-run output directories and retry cleanup
   - require `fallback_when_tb2_unavailable` in TB2 template flow output

Recommended next maintenance items:

1. Add the smoke runner to CI only if the repository has a suitable Windows runner; it depends on PowerShell and git.
2. Consider a narrower `-SkipCodexMirror` default for CI, because `C:\Users\miles\.codex` is a local workstation path.

No additional code change is currently required for the `external-audit-orchestrator` operational scripts based on the current smoke evidence.

## Remaining Risks

- The repository was dirty before this work started. This report separates the new smoke runner from pre-existing changes, but it does not assert ownership over unrelated modified or untracked files.
- TB2 mode remains template-only as stated by the skill documentation; this smoke validates request materialization, not a real TB2 provider execution.
- External web and external CLI/MCP modes are operator handoff modes; this smoke validates packet creation and routing instructions, not a third-party service response.
- A full-repository runtime projection cleanup remains out of scope for this commit; the smoke runner now separates that global drift warning from the external-audit-orchestrator release gate.

## Reference Inputs

- `local-project`: `registry/skills/external-audit-orchestrator/SKILL.md` - declared workflow, assets, scripts, and mode boundaries.
- `local-project`: `registry/skills/external-audit-orchestrator/references/release-checklist.md` - required smoke entrypoint and release validation expectations.
- `local-project`: `local/scripts/build-runtime-layer.py` - runtime projection implementation and support-file copy contract.
- `local-project`: `tests/test_runtime_support_projection.py` - projection regression coverage.
- `local-project`: `docs/plans/EXTERNAL_AUDIT_ORCHESTRATOR_RUNTIME_PROJECTION_DRIFT_FIX_PLAN_2026-05-05.md` - prior projection drift remediation plan.
- `local-project`: `docs/working-notes/2026-05-05-external-audit-orchestrator-runtime-projection-drift.md` - prior diagnosis of registry/runtime/Codex mirror drift.
