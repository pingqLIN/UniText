---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/browser-extension-hard-requirements.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/browser-extension-hard-requirements.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/browser-extension-hard-requirements.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Browser Extension Hard Requirements

Use this file for Chrome or Chromium extension bootstrap work.

These are hard constraints. They matter more than personal folder taste because they directly affect whether the extension can load, run, and be distributed.

## Manifest first

- The build output must contain `manifest.json` at the extension root.
- Do not bury `manifest.json` under `src/`, `dist/chrome/inner/`, or another nested folder that the browser cannot load directly.
- Treat manifest generation as a first-class requirement in the scaffold.

## Manifest version

- Default to Manifest V3 for new Chrome extensions unless the user explicitly requires something else.
- Assume MV3 service worker constraints apply.

## Required runtime boundaries

A Chrome extension commonly has separate surfaces with different runtime rules:

- background service worker
- content scripts
- popup UI
- options page
- side panel, if used

Do not blur these into one generic app folder without keeping their packaging boundaries clear.

## Recommended source layout

For a modern TypeScript-based extension, prefer:

- `src/background/`
- `src/content/`
- `src/popup/`
- `src/options/`
- `src/sidepanel/` only if needed
- `src/shared/`
- `assets/`
- top-level manifest source or generated manifest config

The exact build tool can vary, but these surfaces should stay explicit.

## Build output rules

- The final packaged directory must be loadable as an unpacked extension.
- `manifest.json` must be at the output root.
- referenced scripts, styles, icons, and HTML files must resolve relative to that root.
- keep build output deterministic so zipping for distribution does not require manual rearranging.

## Content script rules

- Content scripts run in page contexts with extension restrictions.
- Do not assume they can use the same APIs as the popup or background service worker.
- Keep content script entrypoints separate from popup and background code.

## Background service worker rules

- In MV3, the background process is a service worker, not a persistent background page.
- Long-lived assumptions or node-style process assumptions should not drive the architecture.
- Put event-driven orchestration in the background worker and keep UI logic elsewhere.

## Permissions and host access

- Treat manifest permissions and host permissions as architecture-level decisions.
- Keep them explicit from the first scaffold.
- Do not hide required permissions in undocumented generated config.

## Distribution-sensitive files

At bootstrap time, plan for these artifacts:

- `manifest.json`
- required icons
- popup or options HTML entry files when applicable
- static assets referenced by manifest

If any of these are missing from the output plan, the scaffold is incomplete.

## i18n note

If the extension has user-facing UI, bootstrap locale support from day one:

- source locale folder
- target locale folder
- UI strings not hard-coded directly in popup or options components

## Anti-patterns

- one giant `src/app/` with no explicit popup/background/content split
- manifest only implied by build tooling and not represented in the scaffold plan
- output zip that requires manual file moving before loading into Chrome
- background, content, and popup code sharing hidden assumptions about runtime APIs

## Default advice

For a new Chrome extension, prefer a scaffold that another developer can recognize immediately as:

- MV3
- unpacked-loadable without manual patching
- explicit about extension surfaces
- explicit about permissions
- explicit about output root structure
