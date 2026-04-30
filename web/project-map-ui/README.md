# Project Map UI

`web/project-map-ui` is the standalone source boundary for the UniText Project Map web UI.

The project owns:

- `build-project-map.py` - static artifact generator
- `project-map-template.html` - self-contained HTML shell
- `project-map-runtime.js` - browser runtime for navigation, governance inspection, refresh, and map controls

The legacy command still works through `local/scripts/build-project-map.py`, but new UI work should land here first.

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

## Compatibility Entry Point

Existing automation may still call:

```powershell
python local/scripts/build-project-map.py
```

That wrapper delegates to this project entrypoint. Do not add new Project Map UI logic under `local/scripts`; keep that folder as compatibility glue.

## Release Checks

Run the fast release gate before committing UI changes:

```powershell
python -m py_compile web/project-map-ui/build-project-map.py local/scripts/build-project-map.py local/scripts/resolve-agent-governance.py
node --check web/project-map-ui/project-map-runtime.js
python -m unittest tests.test_project_map_baseline tests.test_project_map_outputs tests.test_project_map_share_safe tests.test_project_map_browser_smoke
python web/project-map-ui/build-project-map.py --output-dir ops/project-map
python local/scripts/get-publishability-report.py
```
