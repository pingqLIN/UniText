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
