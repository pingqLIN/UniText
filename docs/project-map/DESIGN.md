# Project Map Console Design Notes

> Scope: `web/project-map-ui/project-map-template.html`, `web/project-map-ui/project-map-runtime.js`, and the generated project-map pages. `local/scripts/build-project-map.py` is only a compatibility wrapper.

## Intent

The project map is an operator-facing governance console, not a landing page or a long-form document view. It should help an agent or human quickly inspect runtime-first structure, registry mappings, diagnostics, and handoff artifacts.

Keep the existing information architecture. Improve tone through color roles, contrast, density, and component discipline rather than decorative layout changes.

## Visual Language

- Use a restrained tool surface: neutral backgrounds, clear borders, moderate shadows, and one dominant accent.
- Keep status colors reserved for diagnostics, warnings, errors, and selected state.
- Avoid body-wide gradients, ornamental shapes, soft glass decoration, and oversized hero treatments.
- Keep major panels structured and quiet; prefer border plus subtle elevation over decorative depth.
- Buttons and controls should read as utility controls, not promotional chips.

Current visual controls:

- Color tone: `mono`, `muted`, `vivid`
- Theme: `light`, `dark`
- Text scale: `xs`, `sm`, `md`, `lg`, `xl`

These variants must not change layout structure, component order, or interaction semantics.

## Layout Rules

- Preserve the primary scan path: summary -> filters -> map -> detail.
- Keep the desktop surface wide and operational.
- Use workspace pages to separate browse, diagnostics/export, and governance work instead of growing one long page.
- In grid map mode, resource types read top to bottom, while nodes within a type lane expand horizontally.
- On small screens, collapse to a single column without changing semantic order.
- If a mode removes operator-only controls, runtime JavaScript must guard missing DOM nodes rather than throwing.

## Browser Verification

Generated pages must render in a real browser without console or page errors:

- interactive page: `project-map.html`
- share-safe page: `project-map-share.html`

The unittest baseline includes a Playwright smoke test for this. Heavier visual quality review, screenshots, or Lighthouse should remain a separate gate.

## Acceptance Criteria

Accept changes when:

- the page feels like a trustworthy control surface
- share-safe output does not expose operator-only controls or native paths
- interactive controls degrade safely when absent from a generated mode
- browser smoke passes without console/page errors
- visual changes preserve the runtime-first reading model

Reject changes when:

- the console starts behaving like a marketing or editorial page
- visual personality comes mainly from ornament
- runtime and registry relationships become harder to scan
- generated share-safe HTML needs operator-only controls to avoid JavaScript errors
