---
runtime_projection: true
source_of_truth: registry/skills/start-chrome-extension-project/assets/template/docs/audit/security-review.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/start-chrome-extension-project/assets/template/docs/audit/security-review.md`
> Source of truth: `registry/skills/start-chrome-extension-project/assets/template/docs/audit/security-review.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Security Review

## Scope

- Extension name: `__EXTENSION_NAME__`
- Current purpose: `__EXTENSION_DESCRIPTION__`

## Required Checks

- [ ] `manifest.json` uses Manifest V3
- [ ] Permissions are reduced to the minimum needed for launch
- [ ] No remote code loading is introduced
- [ ] No secrets are bundled into the extension package
- [ ] Message passing between extension contexts is documented
- [ ] Content script injection scope is reviewed before enablement

## Threat Notes

- Document any page data the extension can access
- Document any data that leaves the browser
- Document any privileged action performed by the background worker
