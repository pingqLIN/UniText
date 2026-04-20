---
runtime_projection: true
source_of_truth: registry/skills/azure-validate/references/recipes/bicep/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-validate/references/recipes/bicep/errors.md`
> Source of truth: `registry/skills/azure-validate/references/recipes/bicep/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Bicep Validation Errors

| Error | Fix |
|-------|-----|
| `BCP035: Invalid type` | Check API version |
| `BCP037: Not a member` | Check resource schema |
| `BCP018: Expected character` | Fix syntax |
| `Module not found` | Check relative paths |
| `Template validation failed` | Review error details |

## Debug

```bash
az bicep build --file ./infra/main.bicep 2>&1
```
