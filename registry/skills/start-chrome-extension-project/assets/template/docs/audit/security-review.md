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
