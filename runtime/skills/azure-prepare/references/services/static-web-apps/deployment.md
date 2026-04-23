---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/static-web-apps/deployment.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/static-web-apps/deployment.md`
> Source of truth: `registry/skills/azure-prepare/references/services/static-web-apps/deployment.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Static Web Apps - Deployment

## azd Deploy (Default)

Standard deployment via Azure Developer CLI:

```bash
azd deploy
```

## GitHub-Linked Deployments

For CI/CD builds on Azure (instead of azd deploy):

```bicep
properties: {
  repositoryUrl: 'https://github.com/owner/repo'
  branch: 'main'
  buildProperties: {
    appLocation: 'src'
    apiLocation: 'api'
    outputLocation: 'dist'
  }
}
```

## Deployment Token

> ⚠️ **Security Warning:** Do NOT expose deployment tokens in ARM/Bicep outputs. Deployment outputs are visible in Azure portal deployment history and logs.

**Recommended approach** - retrieve token via Azure CLI and store directly in secret store:

```bash
# Capture token to variable (never echo or log)
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list --name <app-name> --query "properties.apiKey" -o tsv)

# Store directly in Key Vault
az keyvault secret set --vault-name <vault-name> --name swa-deployment-token --value "$DEPLOYMENT_TOKEN" --output none
```

**Do NOT do this** (exposes token in deployment history):
```bicep
// ❌ INSECURE - token visible in deployment history
// output deploymentToken string = staticWebApp.listSecrets().properties.apiKey
```
