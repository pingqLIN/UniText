---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/static-web-apps/routing.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/static-web-apps/routing.md`
> Source of truth: `registry/skills/azure-prepare/references/services/static-web-apps/routing.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Static Web Apps - Routing & Authentication

## Route Configuration

Create `staticwebapp.config.json` in the app root:

```json
{
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["authenticated"]
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/api/*", "/*.{png,jpg,gif}"]
  },
  "responseOverrides": {
    "404": {
      "rewrite": "/404.html"
    }
  }
}
```

## Authentication

### Built-in Providers

```json
{
  "routes": [
    {
      "route": "/admin/*",
      "allowedRoles": ["admin"]
    }
  ],
  "auth": {
    "identityProviders": {
      "azureActiveDirectory": {
        "registration": {
          "openIdIssuer": "https://login.microsoftonline.com/{tenant-id}",
          "clientIdSettingName": "AAD_CLIENT_ID",
          "clientSecretSettingName": "AAD_CLIENT_SECRET"
        }
      }
    }
  }
}
```

### Supported Providers

- Azure Active Directory / Entra ID
- GitHub
- Twitter
- Custom OpenID Connect

## Role-Based Access

```json
{
  "routes": [
    { "route": "/admin/*", "allowedRoles": ["admin"] },
    { "route": "/account/*", "allowedRoles": ["authenticated"] },
    { "route": "/*", "allowedRoles": ["anonymous"] }
  ]
}
```
