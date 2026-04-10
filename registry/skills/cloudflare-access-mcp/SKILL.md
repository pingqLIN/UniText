---
name: cloudflare-access-mcp
description: Use when auditing or changing Cloudflare Access OAuth, DCR, redirect URIs, policies, or MCP connector authentication for this workspace.
---

# Cloudflare Access MCP

## Scope

- Access applications
- OAuth metadata and DCR
- Redirect URI allowlists
- Policies for ChatGPT or other MCP clients

## Use This Skill When

- A connector login fails with invalid redirect, invalid target, or OAuth errors.
- You need to add or verify callback URLs for ChatGPT or another MCP client.
- You need to inspect Access app policy coverage or OAuth metadata.

## Checks

- Access app ID and name
- OAuth enabled state
- DCR enabled state
- Redirect URIs
- User and service-token policies

## References

- [workspace baseline](../cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) when the issue also involves Tunnel, DNS, edge security, or runtime drift.
