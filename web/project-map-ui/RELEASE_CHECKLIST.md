# Project Map UI Release Checklist

Use this checklist before promoting Project Map UI changes into a formal release batch.

- Confirm `git status --short --branch` is clean before starting.
- Confirm source changes are under `web/project-map-ui/`, with only compatibility glue under `local/scripts/`.
- Run Python syntax checks for the generator, compatibility wrapper, and governance resolver.
- Run `node --check web/project-map-ui/project-map-runtime.js`.
- Run the project-map unit and browser smoke tests.
- Regenerate `ops/project-map` artifacts for local verification.
- Verify share-safe output does not expose native paths, governance write controls, or external AGENTS content.
- Run the repository publishability report.
- Commit locally only. Do not push or upload unless explicitly approved.
