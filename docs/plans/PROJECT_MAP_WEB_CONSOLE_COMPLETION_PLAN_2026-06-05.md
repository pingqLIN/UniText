# Project Map Web Console Completion Plan

Date: `2026-06-05`

Scope:

- `web/project-map-ui/project-map-template.html`
- `web/project-map-ui/project-map-runtime.js`
- `web/project-map-ui/README.md`
- generated `ops/project-map/*` artifacts
- focused Project Map tests when behavior changes

Out of scope:

- unrelated UniText public-document rewrites already present in the worktree
- publishing or uploading the ignored Stitch handoff package
- changing `local/scripts` except through existing compatibility behavior

## Objective

Finish the UniText Project Map web console as an operator-grade governance surface derived from the Stitch/Alexandria handoff, while keeping `web/project-map-ui` as the source boundary described in the README.

The completion target is not a new visual concept. It is a runtime-integrated console pass that makes the current page easier to operate, easier to review, and easier to validate.

## Design Brief

Purpose: help operators inspect UniText runtime projection, registry mapping, diagnostics, governance source layering, and handoff output from one local static web console.

Audience: UniText maintainers and AI agents working from local Windows paths. They need dense information, direct controls, and clear source/status evidence.

Surface: product UI / internal governance console, not a marketing page.

Constraints:

- static generated HTML with embedded browser runtime
- share-safe output must strip native paths, governance source content, write controls, and operator-only panels
- missing DOM nodes in share-safe mode must not throw runtime errors
- mobile must remain a single-column cockpit with reachable map and governance controls

Memorable move: the console should read like a maintained governance instrument: browse map first, then inspect diagnostics and rule layering without losing local safety boundaries.

## Anti-Attractor Preflight

Reject these defaults during implementation:

- generic SaaS hero composition or promotional copy
- purple/cyan gradient chrome or gradient headlines
- nested card piles that hide the actual map or governance evidence
- duplicate navigation/filter surfaces competing for attention
- decorative glassmorphism that weakens scanability
- mobile behavior that merely shrinks desktop density until labels overlap

## Work Items

### 1. Recoverable Stitch Package Removal

- Move ignored `stitch_unitext_impeccable_project_map` contents into sibling `.del/stitch_unitext_impeccable_project_map`.
- Leave no tracked deletion noise because the package is local-only and ignored.
- If the source directory itself is locked by the active session, move its contents and retry removing the empty shell after validation.

Acceptance:

- original package content exists under `.del`
- original package source has no remaining files
- Git status shows no tracked deletion for the Stitch package

### 2. README Completion Contract

- Update `web/project-map-ui/README.md` so line 3's source-boundary statement is backed by a completion workflow.
- Add a short "Completion Plan" section pointing maintainers to this plan, the source files, generated artifacts, and release gate.
- Keep the README operational, not promotional.

Acceptance:

- README tells future agents where source edits belong
- README includes the exact completion/release checks
- README does not imply `local/scripts` owns new UI logic

### 3. Console Status Rail

- Add a compact operator status rail near the workspace header.
- Show generated time, adapter, page mode, diagnostics counts, active workspace page, and current visual settings.
- Keep it hidden from share-safe output if it exposes operator-only context.

Acceptance:

- rail updates when workspace page, theme/tone/text scale, or diagnostics state changes
- rail text fits on desktop and mobile without overlapping controls
- share-safe output does not expose native paths or operator-only source details

### 4. Governance Deep Scan Readiness

- Strengthen the existing governance analysis path input as the explicit Deep Scan readiness control.
- Add a clear path status message that distinguishes repo/workspace/global-home/external classification and verified vs browser-only string classification.
- Highlight matching funnel layers after governance resolution.

Acceptance:

- entering a path and resolving governance updates source status, funnel state, and result text
- external paths are labeled as unresolved/evidence-only unless explicitly available
- no report write occurs during path analysis

### 5. Diagnostics Terminal

- Add an operations terminal ledger under diagnostics/export.
- Render `SYS_OK`, `INFO`, `WARN`, and `ERR` rows from generated diagnostics, browser scan capability, selected adapter, and share-safe state.
- Keep diagnostics concise and status-colored without turning the page into a long log.

Acceptance:

- broken references produce `WARN` or `ERR`
- healthy generated state produces a visible `SYS_OK`
- terminal rows update after browser refresh when the runtime data changes

### 6. Responsive And Interaction Polish

- Verify masthead/workspace focus behavior, viewport controls, minimap, tabs, and text scale on desktop and mobile.
- Fix only concrete overlap, blank-state, or unreachable-control issues found during browser checks.
- Preserve existing runtime-first information architecture.

Acceptance:

- desktop and mobile screenshots show non-overlapping controls
- map viewport controls remain reachable
- governance funnel becomes usable in a narrow viewport
- no console/page errors are observed during browser smoke

## Review Gate

Before implementation:

- perform a read-only plan review against this document
- treat acknowledgement-only review as failed
- revise the plan if the review finds a real blocker

After implementation:

- perform a read-only implementation review against the accepted plan
- fix accepted findings
- only then commit and push the focused change set

## Validation Gate

Run:

```powershell
python -m py_compile web/project-map-ui/build-project-map.py web/project-map-ui/project_map_adapters.py web/project-map-ui/project_map_contract.py local/scripts/build-project-map.py local/scripts/resolve-agent-governance.py
node --check web/project-map-ui/project-map-runtime.js
python -m unittest tests.test_project_map_baseline tests.test_project_map_outputs tests.test_project_map_share_safe tests.test_project_map_browser_smoke
python web/project-map-ui/build-project-map.py --output-dir ops/project-map
python local/scripts/get-publishability-report.py
```

Also perform browser verification on:

- `ops/project-map/site/project-map.html`
- `ops/project-map/site/project-map-share.html`

## Done Criteria

- Stitch handoff package is recoverably removed from the active source location.
- README documents the `web/project-map-ui` source boundary and completion workflow.
- Console status rail exists and updates.
- Governance Deep Scan path analysis is visibly classifiable and evidence-safe.
- Diagnostics terminal ledger exists and updates from runtime data.
- Generated Project Map artifacts are rebuilt.
- Validation gate passes or any residual blocker is explicitly documented.
- Final read-only implementation review passes.
