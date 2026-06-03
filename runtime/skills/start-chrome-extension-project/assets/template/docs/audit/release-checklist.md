---
runtime_projection: true
source_of_truth: registry/skills/start-chrome-extension-project/assets/template/docs/audit/release-checklist.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/start-chrome-extension-project/assets/template/docs/audit/release-checklist.md`
> Source of truth: `registry/skills/start-chrome-extension-project/assets/template/docs/audit/release-checklist.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Release Checklist

## Product Readiness

- [ ] Extension name and description match actual behavior
- [ ] Popup and options copy no longer contain starter text
- [ ] Required screenshots and icons exist
- [ ] README setup steps reflect the final toolchain

## Technical Readiness

- [ ] `npm run typecheck`
- [ ] `npm run build`
- [ ] Load `extension/` in Chrome and smoke test major flows
- [ ] Re-check permissions after implementation is complete

## Review Readiness

- [ ] Security review notes are current
- [ ] Permissions review is current
- [ ] Privacy claims match actual data handling
- [ ] No placeholder hosts, branding, or demo text remain
