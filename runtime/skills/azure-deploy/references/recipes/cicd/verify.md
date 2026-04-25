---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/recipes/cicd/verify.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/recipes/cicd/verify.md`
> Source of truth: `registry/skills/azure-deploy/references/recipes/cicd/verify.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# CI/CD Verification

Check pipeline run status:
- **GitHub**: Actions tab → workflow run
- **Azure DevOps**: Pipelines → pipeline run

## Verify Deployed Resources

```bash
az resource list --resource-group <rg-name> --output table
```

## Health Check

```bash
curl -s https://<endpoint>/health | jq .
```

## Report Results to User

> ⛔ **MANDATORY** — You **MUST** present the deployed endpoint URLs to the user in your response.

Extract endpoints from the pipeline output or query them directly via `az` CLI. Present a summary including all service URLs as fully-qualified `https://` links. If any command returns a bare hostname (e.g. `myapp.azurewebsites.net`), always prepend `https://`. Do NOT end your response without including them.
