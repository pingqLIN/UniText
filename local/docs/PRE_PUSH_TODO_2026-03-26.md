# Pre-Push Todo 2026-03-26

## Keep

- Keep the blocker summary from `PRE_PUSH_AUDIT_2026-03-26.md` as a historical snapshot only.
- Keep the valid audit findings about `generate-index-entries.ps1`, `verify-template-package.ps1`, and missing `LICENSE`.
- Keep the current release evidence boundary for Copilot as `bootstrap verified` but `runtime validation pending`.

## Fix

- [x] Remove the mistaken `registry/skills/microsoft-foundry/` copy from the workspace.
- [x] Move binary design assets out of the release surface and ignore `.del/`.
- [x] Fix `bootstrap.py` backup collisions during isolated test runs.
- [x] Fix `generate-index-entries.ps1` so `-Root` works even when the target repo only contains skills data.
- [x] Fix Windows PowerShell compatibility in `generate-index-entries.ps1`.
- [x] Fix `verify-template-package.ps1` so malformed metadata becomes a reportable issue instead of a hard crash.
- [x] Fix Windows test execution in `test_i18n_wave.py` by avoiding hard-coded `python3`.
- [x] Make `export-template-package.ps1` complete successfully when metadata files are rewritten in staging.
- [x] Add a root `LICENSE` file that matches the README `MIT` claim.

## Verify

- [x] `python -m unittest discover -s tests/security -v`
- [x] `powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1`
- [x] `powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path <latest-package>`
- [x] `python local/scripts/report-release-hygiene.py --json`
- [x] Confirm only intended tracked changes remain before push.
