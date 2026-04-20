---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/static-web-apps/bicep.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/static-web-apps/bicep.md`
> Source of truth: `registry/skills/azure-prepare/references/services/static-web-apps/bicep.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Static Web Apps - Bicep Patterns

## Basic Resource

```bicep
resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: '${resourcePrefix}-${serviceName}-${uniqueHash}'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    buildProperties: {
      appLocation: '/'
      apiLocation: 'api'
      outputLocation: 'dist'
    }
  }
}
```

## Custom Domain

```bicep
resource customDomain 'Microsoft.Web/staticSites/customDomains@2022-09-01' = {
  parent: staticWebApp
  name: 'www.example.com'
  properties: {}
}
```

## Application Settings

For the integrated API:

```bicep
resource staticWebAppSettings 'Microsoft.Web/staticSites/config@2022-09-01' = {
  parent: staticWebApp
  name: 'appsettings'
  properties: {
    DATABASE_URL: '@Microsoft.KeyVault(VaultName=${keyVault.name};SecretName=db-url)'
  }
}
```

## Deployment Token

> ⚠️ **Security Warning:** Do NOT expose deployment tokens in Bicep outputs.

See [deployment.md](deployment.md) for secure token handling.
