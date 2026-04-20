---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/recipes/bicep/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/recipes/bicep/errors.md`
> Source of truth: `registry/skills/azure-deploy/references/recipes/bicep/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Bicep Errors

| Error | Resolution |
|-------|------------|
| Syntax error | `az bicep build` to check |
| Missing parameter | Add to parameters file |
| Invalid property | Check `mcp_bicep_get_az_resource_type_schema` |
| Resource conflict | Check existing resources |
| Deployment failed | `az deployment sub show --name <name>` |
| Permission denied | Verify RBAC roles |

## Cleanup (DESTRUCTIVE)

```bash
az group delete --name <rg-name> --yes
```

⚠️ Permanently deletes ALL resources in the group.
