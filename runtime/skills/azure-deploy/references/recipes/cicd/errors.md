---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/recipes/cicd/errors.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/recipes/cicd/errors.md`
> Source of truth: `registry/skills/azure-deploy/references/recipes/cicd/errors.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# CI/CD Errors

| Error | Resolution |
|-------|------------|
| Authentication failed | Check service principal/federated credentials |
| Missing secrets | Add required secrets to repository |
| Missing variables | Add required variables |
| Pipeline timeout | Increase timeout or optimize deployment |
| Approval pending | Request approval in environment settings |

## GitHub Actions Debugging

Check workflow logs in Actions tab for detailed error messages.

## Azure DevOps Debugging

Check pipeline run logs for detailed error messages.
