---
name: notepad-plus-plus-plugin-workflow
description: Use for Notepad++ plugin extension work, including preparing a plugin project before development, fixing or extending a plugin during development, finishing and packaging a plugin, and updating an already listed Plugins Admin extension through GitHub Releases and the official nppPluginList JSON workflow.
---

# Notepad Plus Plus Plugin Workflow

## Overview

Use this workflow for Notepad++ plugins, especially plugins intended for Plugins Admin distribution through `notepad-plus-plus/nppPluginList`.

Always identify the active repository first. Keep plugin source/release work separate from `nppPluginList` entry updates.

## Phase 1: Development Prep

Before editing plugin code:

1. Confirm the repo root, branch, remotes, and worktree state.
2. Identify the plugin name, DLL name, target architecture, and release repo.
3. Verify the Notepad++ plugin contract:
   - exported plugin functions are present
   - plugin DLL name matches the Plugins Admin `folder-name`
   - package layout can place the DLL at the ZIP root
4. Check build prerequisites:
   - Visual Studio/MSBuild or CMake/NMake path
   - Notepad++ SDK/header files
   - x86/x64/ARM64 targets that are expected to ship
5. Record the intended distribution track:
   - local-only testing
   - GitHub release only
   - official Plugins Admin update via `nppPluginList`

Do not update the official plugin list before a release ZIP exists and has a final SHA-256.

## Phase 2: Development Fixes

When modifying or debugging a plugin:

1. Make narrowly scoped source changes in the plugin repo.
2. Preserve the Notepad++ plugin ABI and exported function names unless the task explicitly requires changing them.
3. Prefer real build/test paths over mocks:
   - build the target architecture
   - install into a local or portable Notepad++ plugin folder
   - verify menu commands, docking windows, context menus, config paths, and cleanup/unload behavior as applicable
4. If Plugins Admin packaging is involved, keep package requirements in view:
   - ZIP only
   - plugin DLL at ZIP root
   - optional docs under `doc/<folder-name>/`
5. Keep any local API keys, tokens, logs, build artifacts, and private configs out of release packages and git tracking.

## Phase 3: Development Complete

Before treating plugin development as complete:

1. Update the plugin binary version resource to the intended release version.
2. Build every architecture intended for distribution.
3. Create or refresh release ZIP packages.
4. Confirm each ZIP contains the correct root-level DLL and expected optional files.
5. Compute SHA-256 for each final ZIP.
6. Smoke test from the packaged ZIP, not only from the build output.
7. Draft release notes with:
   - plugin version
   - architecture
   - Notepad++ compatibility notes
   - install/update notes
8. Commit plugin repo changes separately from any `nppPluginList` changes.

## Phase 4: Updating A Listed Plugin

Official Plugins Admin updates are driven by `notepad-plus-plus/nppPluginList`, not by pushing the plugin repo alone.

Use this sequence:

1. In the plugin repo, publish a GitHub Release with the final ZIP asset.
2. Verify the release asset URL is a direct downloadable `.zip` URL.
3. Compute the final ZIP SHA-256 after upload or verify the uploaded asset matches the local hash.
4. In a fork/branch of `notepad-plus-plus/nppPluginList`, update only the relevant architecture JSON:
   - `src/pl.x86.json` for 32-bit
   - `src/pl.x64.json` for 64-bit
   - `src/pl.arm64.json` for ARM64
5. Update the plugin entry fields:
   - `version`: exact plugin DLL binary version
   - `id`: SHA-256 of the final ZIP
   - `repository`: direct ZIP download URL
   - `homepage`, `description`, `author` only if they changed
6. Preserve `folder-name`; changing it changes the installed plugin identity.
7. Add `npp-compatible-versions` and `old-versions-compatibility` when compatibility boundaries changed.
8. Test locally with a debug Notepad++ build and local `nppPluginList.json` when possible:
   - install
   - update from an older installed version
   - remove
9. Open a PR to `notepad-plus-plus/nppPluginList`.
10. Explain that the official list is built into signed `nppPluginList.dll`; users see the update only after the official list release/distribution catches up.

## Required Fields Reminder

For Plugins Admin entries, enforce these rules:

- `folder-name` must be unique and match the plugin DLL basename.
- `version` must match the plugin binary version.
- `id` must be SHA-256 of the downloadable ZIP package.
- `repository` must be a direct `.zip` download URL.
- ZIP root must contain the plugin DLL.
- Documentation inside `doc/` installs under `plugins/doc/<folder-name>/`.

## Response Style

When reporting progress, separate:

- plugin repo status
- packaged release asset status
- nppPluginList status
- local Plugins Admin test status

If the user asks whether an update is "published", distinguish:

- released in the plugin GitHub repo
- merged into official `nppPluginList`
- available to users through the signed Plugins Admin list
