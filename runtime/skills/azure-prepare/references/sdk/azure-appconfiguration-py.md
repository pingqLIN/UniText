---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/sdk/azure-appconfiguration-py.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/sdk/azure-appconfiguration-py.md`
> Source of truth: `registry/skills/azure-prepare/references/sdk/azure-appconfiguration-py.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# App Configuration — Python SDK Quick Reference

> Condensed from **azure-appconfiguration-py**. Full patterns (feature flags,
> snapshots, read-only settings, async client, labels)
> in the **azure-appconfiguration-py** plugin skill if installed.

## Install
pip install azure-appconfiguration azure-identity

## Quick Start

> **Auth:** `DefaultAzureCredential` is for local development. See [auth-best-practices.md](../auth-best-practices.md) for production patterns.

```python
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential
client = AzureAppConfigurationClient(base_url="https://<name>.azconfig.io", credential=DefaultAzureCredential())
```

## Best Practices
- Use labels for environment separation (dev, staging, prod)
- Use key prefixes for logical grouping (app:database:*, app:cache:*)
- Make production settings read-only to prevent accidental changes
- Create snapshots before deployments for rollback capability
- Use Entra ID instead of connection strings in production
- Refresh settings periodically in long-running applications
- Use feature flags for gradual rollouts and A/B testing
