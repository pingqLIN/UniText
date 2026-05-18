# Release Checklist

## Product Readiness

- [ ] Extension name and description match actual behavior
- [ ] Popup and options copy no longer contain starter text
- [ ] Required screenshots and icons exist
- [ ] README setup steps reflect the final toolchain

## Technical Readiness

- [ ] `npm run typecheck`
- [ ] `npm run build`
- [ ] Load `dist/` in Chrome and smoke test major flows
- [ ] Re-check permissions after implementation is complete

## Review Readiness

- [ ] Security review notes are current
- [ ] Permissions review is current
- [ ] Privacy claims match actual data handling
- [ ] No placeholder hosts, branding, or demo text remain
