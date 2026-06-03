# Permissions Review

## Current Manifest Baseline

- `permissions`: `["storage"]`
- `host_permissions`: `[]`

## Review Table

| Capability | Needed now | Reason | Narrow alternative |
| --- | --- | --- | --- |
| storage | yes | Save local extension preferences | none |
| activeTab | no | Add only if temporary tab access is enough | prefer this before host access |
| scripting | no | Add only for programmatic injection | check if static content script is enough |
| host permissions | no | Add exact domains only | avoid `<all_urls>` |

## Decisions

- Replace this section with the final permission rationale before release
