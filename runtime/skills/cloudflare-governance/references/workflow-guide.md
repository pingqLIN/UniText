---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/references/workflow-guide.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/references/workflow-guide.md`
> Source of truth: `registry/skills/cloudflare-governance/references/workflow-guide.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Workflow Guide

This shared guide stays template-safe. The live authoring-workspace checklist belongs in `local/docs/CLOUDFLARE_WORKFLOW_LIVE.md`.

## Recheck Order

1. Live Cloudflare API
2. Repo config files
3. Runtime files under the local runtime root
4. Public probes for `/health`, `/mcp`, and `/.well-known/oauth-authorization-server`

## Useful Checks

- Zone settings
- Access app OAuth and DCR
- Tunnel ingress and credentials file
- Runtime split between the authoring source repo and the deployed runtime root

## Useful Commands

- `curl.exe`
- `Get-Service`
- `Get-Process`
- `Get-Content`
- `rg`
