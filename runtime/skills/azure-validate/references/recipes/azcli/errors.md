---
runtime_projection: true
source_of_truth: registry/skills/azure-validate/references/recipes/azcli/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-validate/references/recipes/azcli/errors.md`
> Source of truth: `registry/skills/azure-validate/references/recipes/azcli/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# AZCLI Validation Errors

| Error | Fix |
|-------|-----|
| `AADSTS700082: Token expired` | `az login` |
| `Please run 'az login'` | `az login` |
| `AADSTS50076: MFA required` | `az login --use-device-code` |
| `AuthorizationFailed` | Request Contributor role |
| `npm ci` fails with `missing: package-lock.json` | Run `npm install --package-lock-only` in the service directory before building |
| `Template validation failed` | Check Bicep syntax |

## Debug

```bash
az <command> --verbose --debug
```
