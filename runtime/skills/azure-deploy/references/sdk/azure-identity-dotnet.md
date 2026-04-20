---
runtime_projection: true
source_of_truth: registry/skills/azure-deploy/references/sdk/azure-identity-dotnet.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-deploy/references/sdk/azure-identity-dotnet.md`
> Source of truth: `registry/skills/azure-deploy/references/sdk/azure-identity-dotnet.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Authentication — .NET SDK Quick Reference

> Condensed from **azure-identity-dotnet**. Full patterns (ASP.NET DI,
> sovereign clouds, brokered auth, certificate credentials)
> in the **azure-identity-dotnet** plugin skill if installed.

## Install
dotnet add package Azure.Identity

## Quick Start

> **Auth:** `DefaultAzureCredential` is for local development. See [auth-best-practices.md](../auth-best-practices.md) for production patterns.

```csharp
using Azure.Identity;
var credential = new DefaultAzureCredential();
```

## Best Practices
- Use DefaultAzureCredential for **local development only**. In production, use deterministic credentials (ManagedIdentityCredential) — see [auth-best-practices.md](../auth-best-practices.md)
- Reuse credential instances — single instance shared across clients
- Configure retry policies for credential operations
- Enable logging with AzureEventSourceListener for debugging auth issues
