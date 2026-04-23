---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/static-web-apps/region-availability.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/static-web-apps/region-availability.md`
> Source of truth: `registry/skills/azure-prepare/references/services/static-web-apps/region-availability.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# SWA Region Availability

⚠️ **NOT available in many common regions** — Check before deployment.

| ✅ Available | ❌ NOT Available (will FAIL) |
|-------------|------------------------------|
| `westus2` | `eastus` |
| `centralus` | `northeurope` |
| `eastus2` | `southeastasia` |
| `westeurope` | `uksouth` |
| `eastasia` | `canadacentral` |
| | `australiaeast` |
| | `westus3` |

## Recommended Regions

| Pattern | Use |
|---------|-----|
| SWA only | `westus2`, `centralus`, `eastus2`, `westeurope`, `eastasia` |
| SWA + backend | `westus2`, `centralus`, `eastus2`, `westeurope`, `eastasia` |
| SWA + Azure OpenAI | `eastus2` (only region with full overlap) |
