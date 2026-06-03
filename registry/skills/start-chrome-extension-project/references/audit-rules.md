# Chrome Extension Audit Rules

Use this reference when tailoring the generated starter or reviewing an existing extension project.

## Baseline Rules

- Default to Manifest V3.
- Keep `permissions` and `host_permissions` as narrow as possible.
- Do not add `"<all_urls>"` unless the user explicitly needs it and understands the review cost.
- Do not ship remote code, remote script loaders, or eval-like behavior.
- Treat any collection of page content, identifiers, cookies, or browsing activity as privacy-relevant.
- Add a written justification for every permission and every host pattern.

## Security Review Focus

- Confirm the extension can work with `activeTab` before requesting broader access.
- Review every message channel between popup, options, background, and content scripts.
- Validate all externally-derived data before rendering it into extension pages.
- Keep secrets out of the extension bundle. Assume client-side code is inspectable.
- Prefer static assets and bundled scripts over runtime downloads.
- Verify that storage usage matches the minimum persistence needed for the feature.

## Privacy Review Focus

- Document what user data is collected, where it is stored, and why it is needed.
- Distinguish optional telemetry from core product functionality.
- If data leaves the browser, document destination, retention, and opt-in or opt-out behavior.
- If no personal data is collected, state that explicitly in the generated docs.
- Keep `docs/audit/privacy-review.md` updated as behavior changes.

## Release Review Focus

- Make sure the extension name, description, and screenshots match real behavior.
- Replace placeholder icons and branding before any packaging or store submission.
- Re-check permissions after implementation. Starter-time assumptions often drift.
- Build from a clean tree and load the built `dist/` folder in Chrome for smoke testing.
- Keep the audit docs alongside the code so later reviewers can see why decisions were made.
