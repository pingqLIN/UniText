---
runtime_projection: true
source_of_truth: registry/skills/azure-validate/references/recipes/terraform/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-validate/references/recipes/terraform/errors.md`
> Source of truth: `registry/skills/azure-validate/references/recipes/terraform/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Terraform Validation Errors

| Error | Fix |
|-------|-----|
| `Backend init failed` | Check storage account access |
| `Provider version conflict` | Update required_providers |
| `State lock failed` | Wait or force unlock |
| `Validation failed` | Check terraform validate output |

## Debug

```bash
TF_LOG=DEBUG terraform plan
```
