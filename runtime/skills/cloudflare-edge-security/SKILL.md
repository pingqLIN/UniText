---
name: cloudflare-edge-security
description: Use when the request is specifically about Cloudflare zone-edge security, browser checks, bot protection, WAF custom rules, or skip rules for specific hosts and paths. Do not use for WARP and Zero Trust device policy, tunnel ingress, or Access OAuth review.
runtime_projection: true
source_of_truth: registry/skills/cloudflare-edge-security/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-edge-security/SKILL.md`
> Source of truth: `registry/skills/cloudflare-edge-security/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Edge Security

## Scope

- Zone security level
- Browser check / BIC
- Bot fight and crawler protection
- WAF custom rules and skip rules

## Use This Skill When

- A public endpoint is being challenged or blocked.
- You need to tune protection for a specific hostname or path.
- You need to check whether a rule is too broad.

## Do Not Use This Skill When

- The issue is about local WARP behavior or Zero Trust device policy.
- The issue is about tunnel inventory, DNS linkage, or ingress routing.
- The issue is about Access app OAuth, DCR, or redirect URIs.

## Checks

- `security_level`
- `browser_check`
- bot-management settings
- custom rules that affect the MCP host

## References

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) first for broad Cloudflare review, or when the incident also involves Access, Tunnel, DNS, runtime state, or local WARP/device behavior.
