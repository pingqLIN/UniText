---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/aks/addons.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/aks/addons.md`
> Source of truth: `registry/skills/azure-prepare/references/services/aks/addons.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# AKS - Add-ons

## Container Monitoring

```bicep
addonProfiles: {
  omsagent: {
    enabled: true
    config: {
      logAnalyticsWorkspaceResourceID: logAnalytics.id
    }
  }
}
```

## Azure CNI Networking

```bicep
networkProfile: {
  networkPlugin: 'azure'
  networkPolicy: 'calico'
}
```

## Azure Key Vault Provider

```bicep
addonProfiles: {
  azureKeyvaultSecretsProvider: {
    enabled: true
    config: {
      enableSecretRotation: 'true'
    }
  }
}
```

## Application Gateway Ingress Controller

```bicep
addonProfiles: {
  ingressApplicationGateway: {
    enabled: true
    config: {
      applicationGatewayId: appGateway.id
    }
  }
}
```

## Add-ons Summary

| Add-on | Purpose |
|--------|---------|
| omsagent | Container Insights monitoring |
| azureKeyvaultSecretsProvider | Mount Key Vault secrets as volumes |
| ingressApplicationGateway | Application Gateway as ingress controller |
| azurepolicy | Azure Policy for Kubernetes |
