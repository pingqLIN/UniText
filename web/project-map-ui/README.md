# Project Map UI

`web/project-map-ui` is the standalone source boundary for the UniText Project Map web UI.

The project owns:

- `CONTRACT.md` - human-readable source/input/output/share-safe boundary
- `project_map_adapters.py` - root adapters for UniText, other project folders, and governance research folders
- `project_map_contract.py` - machine-readable contract used by the generator
- `build-project-map.py` - static artifact generator
- `project-map-template.html` - self-contained HTML shell
- `project-map-runtime.js` - browser runtime for navigation, governance inspection, refresh, and map controls

The legacy command still works through `local/scripts/build-project-map.py`, but new UI work should land here first.

## Completion Workflow

Use `docs/plans/PROJECT_MAP_WEB_CONSOLE_COMPLETION_PLAN_2026-06-05.md` for the current web-console completion pass.

Keep implementation changes in this folder unless the generator contract or tests require a narrow companion update elsewhere:

- edit `project-map-template.html` for HTML/CSS structure
- edit `project-map-runtime.js` for browser behavior
- regenerate `ops/project-map/*` artifacts after source changes
- keep `local/scripts/build-project-map.py` as compatibility glue only

The console completion target is an operator-grade governance surface: status, diagnostics, map controls, governance path analysis, and share-safe output must remain aligned.

## Build

From the repository root:

```powershell
python web/project-map-ui/build-project-map.py
```

This writes:

- `ops/project-map/project-map.json`
- `ops/project-map/site/project-map.html`
- `ops/project-map/site/project-map-share.html`
- `ops/project-map/site/project-map-handoff.md`
- `ops/project-map/site/project-map-handoff.json`

The default input/output/policy contract is documented in `CONTRACT.md` and emitted into the generated payload metadata.

## Root Adapters

`--repo-root` is now treated as an arbitrary governance root. The generator selects a `project_map_adapters.py` adapter from root markers:

- `unitext` for the full UniText repository shape.
- `governance-folder` for AGENTS-led project folders or future governance research folders.

Generated interactive HTML receives the active adapter configuration, so browser refresh uses the same marker, document, and registry-directory contract as the Python builder.

## Compatibility Entry Point

Existing automation may still call:

```powershell
python local/scripts/build-project-map.py
```

That wrapper delegates to this project entrypoint. Do not add new Project Map UI logic under `local/scripts`; keep that folder as compatibility glue.

## Release Checks

Run the fast release gate before committing UI changes:

```powershell
python -m py_compile web/project-map-ui/build-project-map.py web/project-map-ui/project_map_adapters.py web/project-map-ui/project_map_contract.py local/scripts/build-project-map.py local/scripts/resolve-agent-governance.py
node --check web/project-map-ui/project-map-runtime.js
python -m unittest tests.test_project_map_baseline tests.test_project_map_outputs tests.test_project_map_share_safe tests.test_project_map_browser_smoke
python web/project-map-ui/build-project-map.py --output-dir ops/project-map
python local/scripts/get-publishability-report.py
```
