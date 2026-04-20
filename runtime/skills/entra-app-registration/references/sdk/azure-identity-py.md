---
runtime_projection: true
source_of_truth: registry/skills/entra-app-registration/references/sdk/azure-identity-py.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/entra-app-registration/references/sdk/azure-identity-py.md`
> Source of truth: `registry/skills/entra-app-registration/references/sdk/azure-identity-py.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Authentication — Python SDK Quick Reference

> Condensed from **azure-identity-py**. Full patterns (async,
> ChainedTokenCredential, token caching, all credential types)
> in the **azure-identity-py** plugin skill if installed.

## Install
```bash
pip install azure-identity
```

## Quick Start
> **Auth:** `DefaultAzureCredential` is for local development. See [auth-best-practices.md](../auth-best-practices.md) for production patterns.

```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
```

## Best Practices
- Use DefaultAzureCredential for **local development only** (CLI, PowerShell, VS Code). In production, use ManagedIdentityCredential — see [auth-best-practices.md](../auth-best-practices.md)
- Never hardcode credentials — use environment variables or managed identity
- Prefer managed identity in production Azure deployments
- Use ChainedTokenCredential when you need a custom credential order
- Close async credentials explicitly or use context managers
- Set AZURE_CLIENT_ID env var for user-assigned managed identities
- Exclude unused credentials to speed up authentication
