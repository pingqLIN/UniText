---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/recipes/terraform/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/recipes/terraform/errors.md`
> Source of truth: `registry/skills/azure-deploy/references/recipes/terraform/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Terraform Errors

| Error | Resolution |
|-------|------------|
| State lock error | Wait or `terraform force-unlock <lock-id>` |
| Resource exists | `terraform import <resource>` |
| Backend denied | Check storage permissions |
| Provider error | `terraform init -upgrade` |

## Cleanup (DESTRUCTIVE)

```bash
terraform destroy -auto-approve
```

Selective:
```bash
terraform destroy -target=azurerm_container_app.api
```

⚠️ Permanently deletes resources.
