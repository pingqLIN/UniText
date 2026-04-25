---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/recipes/azcli/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/recipes/azcli/errors.md`
> Source of truth: `registry/skills/azure-deploy/references/recipes/azcli/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Azure CLI Errors

| Error | Resolution |
|-------|------------|
| Not authenticated | `az login` |
| Subscription not found | `az account list` |
| Deployment failed | `az deployment sub show --name <name>` |
| Template error | `az deployment sub validate` |
| Permission denied | Verify RBAC roles |
| Quota exceeded | Request increase or change region |

## Cleanup (DESTRUCTIVE)

```bash
az group delete --name <rg-name> --yes
```

⚠️ Permanently deletes ALL resources in the group.
