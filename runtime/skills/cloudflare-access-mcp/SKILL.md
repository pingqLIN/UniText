---
name: cloudflare-access-mcp
description: Use when auditing or changing Cloudflare Access OAuth, DCR, redirect URIs, policies, or MCP connector authentication for this workspace.
runtime_projection: true
source_of_truth: registry/skills/cloudflare-access-mcp/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-access-mcp/SKILL.md`
> Source of truth: `registry/skills/cloudflare-access-mcp/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
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

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) when the issue also involves Tunnel, DNS, edge security, or runtime drift.
