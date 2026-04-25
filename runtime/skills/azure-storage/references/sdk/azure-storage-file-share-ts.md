---
runtime_projection: true
source_of_truth: registry/skills/azure-storage/references/sdk/azure-storage-file-share-ts.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-storage/references/sdk/azure-storage-file-share-ts.md`
> Source of truth: `registry/skills/azure-storage/references/sdk/azure-storage-file-share-ts.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# File Shares — TypeScript SDK Quick Reference

> Condensed from **azure-storage-file-share-ts**. Full patterns (SAS generation,
> snapshots, range operations, streaming, copy operations)
> in the **azure-storage-file-share-ts** plugin skill if installed.

## Install
npm install @azure/storage-file-share @azure/identity

## Quick Start
```typescript
import { ShareServiceClient } from "@azure/storage-file-share";
import { DefaultAzureCredential } from "@azure/identity";
const client = new ShareServiceClient(`https://${accountName}.file.core.windows.net`, new DefaultAzureCredential());
```

## Best Practices
- Use connection strings for simplicity in development
- Use DefaultAzureCredential for **local development only** — in production, use ManagedIdentityCredential. See [auth-best-practices.md](../auth-best-practices.md)
- Set quotas on shares to prevent unexpected storage costs
- Use streaming for large files — `uploadStream`/`downloadToFile` for files > 256MB
- Use ranges for partial updates — more efficient than full file replacement
- Create snapshots before major changes — point-in-time recovery
- Handle errors gracefully — check `RestError.statusCode` for specific handling
- Use `*IfExists` methods for idempotent operations
