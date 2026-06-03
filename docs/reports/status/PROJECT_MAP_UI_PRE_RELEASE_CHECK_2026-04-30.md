# Project Map UI Pre-Release Check

Date: `2026-04-30`
Branch: `feature/project-map-ui-standalone`
Worktree: `Q:\UniText-wt-web-ui-split`

## Scope

This batch splits the Project Map web UI source into a standalone project boundary:

- `web/project-map-ui/build-project-map.py`
- `web/project-map-ui/project-map-runtime.js`
- `web/project-map-ui/project-map-template.html`
- `web/project-map-ui/README.md`
- `web/project-map-ui/RELEASE_CHECKLIST.md`

Legacy `local/scripts/project-map-*` files now remain only as compatibility entrypoints or markers. New Project Map UI implementation work should land under `web/project-map-ui/`.

## Worktree Cleanup

After cleanup, registered Git worktrees are expected to be limited to:

- `Q:\UniText` on `main`
- `Q:\UniText-wt-web-ui-split` on `feature/project-map-ui-standalone`

Older registered worktrees were removed from Git's worktree registry. The previous `Q:\UniText-wt-ui` directory was moved into `Q:\.del` for reversible cleanup. `Q:\UniText-wt-project-map-b` no longer appears in Git's worktree registry, but Windows left an empty residual directory that may need a later manual unlock/removal.

## Verification

Passed:

- `python -m py_compile web\project-map-ui\build-project-map.py local\scripts\build-project-map.py local\scripts\resolve-agent-governance.py`
- `node --check web\project-map-ui\project-map-runtime.js`
- `python -m unittest tests.test_project_map_baseline tests.test_project_map_outputs tests.test_project_map_share_safe tests.test_project_map_browser_smoke`
- `python web\project-map-ui\build-project-map.py --output-dir ops\project-map`
- `python local\scripts\verify-workspace-boundaries.py`
- `python -m unittest discover -s tests -p "test*.py"`: 94 passed, 1 skipped

Known environment-bound result:

- `python local\scripts\verify-bootstrap.py` fails in this worktree because user-level Claude/Gemini/Agents symlinks and Copilot MCP config intentionally point at the primary `Q:\UniText` checkout, not this temporary feature worktree. Do not rebind global runtime targets just to satisfy a feature-worktree check.

## Release Notes

- The web UI now has an explicit standalone project home under `web/project-map-ui`.
- Existing automation can continue to call `python local/scripts/build-project-map.py`.
- Tests were updated to validate the new source boundary and legacy wrapper.
- Registry/catalog tests were aligned with the current baseline where `microsoft-foundry` and `impeccable` are active skills and the Azure family is no longer part of the registry baseline.

## Publish Boundary

No push or upload has been performed. This report is local-only until the user explicitly approves publication.
