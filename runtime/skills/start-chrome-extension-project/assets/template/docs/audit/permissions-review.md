---
runtime_projection: true
source_of_truth: registry/skills/start-chrome-extension-project/assets/template/docs/audit/permissions-review.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/start-chrome-extension-project/assets/template/docs/audit/permissions-review.md`
> Source of truth: `registry/skills/start-chrome-extension-project/assets/template/docs/audit/permissions-review.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
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
