---
name: start-chrome-extension-project
description: Scaffold a new Chrome extension project starter with a Manifest V3 baseline, TypeScript build setup, required folders, and built-in audit documentation. Use when Codex needs to start a Chrome extension from scratch, prepare a secure extension repo skeleton, or add permission, privacy, and release review documents before implementation.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/start-chrome-extension-project/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/start-chrome-extension-project/SKILL.md`
> Source of truth: `registry/skills/start-chrome-extension-project/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Start Chrome Extension Project

## Overview

Create a reusable Chrome extension starter from `assets/template/` and tailor it to the user's project name, purpose, and target directory.
Use the bundled scaffold script when you want a deterministic copy of the template with placeholder values replaced.

## Workflow

1. Ask for the extension name, short description, target path, and core use case if they are missing. If the user does not answer, continue with conservative placeholders and note the unresolved items.
2. Ask for the narrowest possible `permissions`, `host_permissions`, and `content_scripts.matches` values. If the user does not answer, keep `host_permissions` empty, prefer the smallest safe permission set, and record the open decision in `docs/audit/`.
3. Run `scripts/scaffold_chrome_extension.py` to copy `assets/template/` into the target project.
4. Update `manifest.json`, UI copy, and `docs/audit/` to match the actual extension behavior.
5. Build the project and flag any remaining gaps such as icons, host scopes, or store-readiness items. The generated `extension/` directory is the Chrome Load unpacked root; `dist/` is not the load target.

## Required Decisions

- Extension purpose and user-facing summary
- Whether launch scope needs a popup, options page, background worker, and content script
- Exact Chrome permissions and whether `activeTab` is enough
- Exact sites or URL patterns for host access
- Whether the starter should stay local-only or prepare for Chrome Web Store submission

Do not default to broad host access. If the user does not know the final scope yet, leave `host_permissions` empty and note the decision in the audit docs.
Treat the question phase as helpful but non-blocking unless the target path already exists and is non-empty, or another safety issue would make automatic scaffolding risky.

## Scaffold The Starter

Run:

```powershell
python scripts/scaffold_chrome_extension.py `
  --target "<windows-project-root>\my-extension" `
  --name "My Extension" `
  --description "Describe the extension clearly"
```

The script copies `assets/template/` into the target directory and replaces:

- `__EXTENSION_NAME__`
- `__EXTENSION_DESCRIPTION__`
- `__PROJECT_SLUG__`
- `__YEAR__`

If the target directory already exists and is not empty, stop and let the user decide whether to choose a new path or merge manually.

## Customize After Scaffolding

- Update `manifest.json` first. Remove unused capabilities before editing any UI.
- Replace the placeholder audit notes in `docs/audit/` with project-specific decisions.
- Add real icon assets before publishing. The starter intentionally leaves the icon folder lightweight.
- Wire `src/content/index.ts` into `manifest.json` only after the target URL patterns are known.
- Keep the TypeScript starter minimal until the user chooses additional tooling.

## Audit Guidance

Read [references/audit-rules.md](references/audit-rules.md) when the user asks for security, privacy, permissions, data handling, or store-readiness guidance.
Read [references/template-map.md](references/template-map.md) when you need a fast inventory of the generated files and why they exist.

Generated projects include:

- `docs/audit/security-review.md`
- `docs/audit/privacy-review.md`
- `docs/audit/permissions-review.md`
- `docs/audit/release-checklist.md`

Treat these as living project docs. Update them as decisions change instead of leaving the template text untouched.

## Resources

- `scripts/scaffold_chrome_extension.py`: Copy the starter into a target project and replace placeholders.
- `assets/template/`: Manifest V3 starter with TypeScript, popup, options, background, shared code, docs, build script, and generated `extension/` load-root convention.
- `references/audit-rules.md`: Chrome extension review baseline for least privilege, privacy, and release checks.
- `references/template-map.md`: File-by-file explanation of the starter layout.

## Output Standard

When using this skill for a user request, deliver:

1. The scaffolded project path
2. Any permissions or host access that still need confirmation
3. Any audit checklist items that remain unresolved
