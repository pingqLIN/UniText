---
name: cloudflare-tunnel-dns
description: Use when auditing or changing Cloudflare Tunnel, DNS hostnames, ingress routing, credentials files, or health endpoints for this workspace.
---

# Cloudflare Tunnel DNS

## Scope

- Tunnel IDs and credentials files
- DNS hostnames for MCP and health
- Ingress to local ports
- Public endpoint reachability

## Use This Skill When

- You need to confirm the active tunnel target.
- You need to update hostname to ingress mappings.
- You need to verify health and MCP routes from the public edge.

## Checks

- Tunnel ID and name
- Credentials file path
- Hostname -> local port mapping
- `/health` and `/mcp` routing

## References

- [workspace baseline](../cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) when hostname routing changes also require Access policy, edge-security, or runtime review.
