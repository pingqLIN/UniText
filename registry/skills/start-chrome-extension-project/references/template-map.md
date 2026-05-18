# Template Map

This starter copies `assets/template/` into a new project.

## Root Files

- `manifest.json`: Manifest V3 baseline with popup, options page, storage permission, and placeholder metadata.
- `package.json`: Minimal Node toolchain using TypeScript and esbuild.
- `tsconfig.json`: TypeScript settings for the extension source.
- `.gitignore`: Ignore build output and local dependency folders.
- `README.md`: Project-specific setup and customization steps.

## Source Layout

- `src/background/index.ts`: Background service worker baseline.
- `src/content/index.ts`: Content script placeholder kept out of the manifest until the target hosts are known.
- `src/popup/`: Popup HTML and TypeScript entrypoint.
- `src/options/`: Options page HTML and TypeScript entrypoint.
- `src/shared/`: Shared storage and message helpers.

## Build Files

- `scripts/build.mjs`: Bundles TypeScript entrypoints and copies static assets into `dist/`.

## Audit Docs

- `docs/audit/security-review.md`: Security checklist and threat notes.
- `docs/audit/privacy-review.md`: Data handling, retention, and user disclosure notes.
- `docs/audit/permissions-review.md`: Permission and host scope decisions.
- `docs/audit/release-checklist.md`: Pre-release and store-readiness checklist.

## Assets

- `icons/`: Placeholder folder for final extension icons.
