---
runtime_projection: true
source_of_truth: registry/skills/start-chrome-extension-project/assets/template/docs/audit/privacy-review.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/start-chrome-extension-project/assets/template/docs/audit/privacy-review.md`
> Source of truth: `registry/skills/start-chrome-extension-project/assets/template/docs/audit/privacy-review.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Privacy Review

## Data Inventory

| Data type | Collected | Stored where | Leaves device | Why needed |
| --- | --- | --- | --- | --- |
| preference value | yes | `chrome.storage.sync` | no | Save starter configuration |
| page content | no | n/a | n/a | add only when feature requires it |
| telemetry | no | n/a | n/a | add only with explicit product decision |

## Checks

- [ ] Every collected field is documented
- [ ] The extension can explain why each field is needed
- [ ] Any network destination is documented
- [ ] Retention behavior is documented
- [ ] User-facing privacy copy matches real behavior

## Notes

- Replace this starter content before release
- If the extension does not collect personal data, say so directly in product copy
