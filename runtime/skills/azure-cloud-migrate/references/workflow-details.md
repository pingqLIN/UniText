---
runtime_projection: true
source_of_truth: registry/skills/azure-cloud-migrate/references/workflow-details.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-cloud-migrate/references/workflow-details.md`
> Source of truth: `registry/skills/azure-cloud-migrate/references/workflow-details.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Workflow Details

## Status Tracking

Maintain a `migration-status.md` file in the output directory (`<source-folder>-azure/`):

```markdown
# Migration Status
| Phase | Status | Notes |
|-------|--------|-------|
| Assessment | ⬜ Not Started | |
| Code Migration | ⬜ Not Started | |
```

Update status: ⬜ Not Started → 🔄 In Progress → ✅ Complete → ❌ Failed

## Error Handling

| Error | Cause | Remediation |
|-------|-------|-------------|
| Unsupported runtime | Source runtime not available in target Azure service | Check target service's supported languages documentation |
| Missing service mapping | Source service has no direct Azure equivalent | Use closest Azure alternative, document in assessment |
| Code migration failure | Incompatible patterns or dependencies | Review scenario-specific guide in [lambda-to-functions.md](services/functions/lambda-to-functions.md) |
| `azd init` refuses non-empty directory | azd requires clean directory for template init | Use temp directory approach: init in empty dir, copy files back |

> For scenario-specific errors (e.g., Azure Functions binding issues, trigger configuration), see the error table in the corresponding scenario reference.
