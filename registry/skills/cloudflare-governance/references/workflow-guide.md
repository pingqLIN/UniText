# Workflow Guide

## Recheck Order

1. Live Cloudflare API
2. Repo config files
3. Runtime files under `Q:\Services`
4. Public probes for `/health`, `/mcp`, and `/.well-known/oauth-authorization-server`

## Useful Checks

- Zone settings
- Access app OAuth and DCR
- Tunnel ingress and credentials file
- Runtime split between `Q:\Projects\tb2-claude-subagent-workflow` and `Q:\Services\tb2-prod`

## Useful Commands

- `curl.exe`
- `Get-Service`
- `Get-Process`
- `Get-Content`
- `rg`
