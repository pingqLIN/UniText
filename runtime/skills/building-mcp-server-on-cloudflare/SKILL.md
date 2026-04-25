---
name: building-mcp-server-on-cloudflare
description: Use when building or deploying remote MCP servers on Cloudflare Workers, including OAuth authentication and production deployment.
runtime_projection: true
source_of_truth: registry/skills/building-mcp-server-on-cloudflare/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/building-mcp-server-on-cloudflare/SKILL.md`
> Source of truth: `registry/skills/building-mcp-server-on-cloudflare/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Building MCP Servers on Cloudflare

## Use This Skill

- When you want to build a remote MCP server on Cloudflare Workers.
- When you need MCP tools, OAuth, or production deployment on Cloudflare.
- When you need Cloudflare-specific MCP server patterns rather than generic MCP guidance.

## Scope

- MCP tools and resource handlers
- OAuth authentication and callback handling
- Worker deployment and runtime configuration
- Cloudflare-specific production concerns

## First Check

- Load the latest Cloudflare and MCP docs before relying on API details.
- Prefer the current Cloudflare MCP guidance over pre-trained assumptions.

## References

- Use the official Cloudflare docs and MCP docs for the exact server pattern.

## Related Skills

- Use [mcp-builder](../../../registry/skills/mcp-builder/SKILL.md) for general MCP server design patterns that are not Cloudflare-specific.
- Use [wrangler](../../../registry/skills/wrangler/SKILL.md) when the task is mainly local dev, deploy, or `wrangler` config.
- Use [cloudflare](../../../registry/skills/cloudflare/SKILL.md) when you first need to choose the right Cloudflare product boundary.
