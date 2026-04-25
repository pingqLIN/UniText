---
name: cloudflare-edge-security
description: Use when auditing or changing Cloudflare zone security, browser checks, bot protection, WAF custom rules, or skip rules for specific hosts and paths.
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

## Checks

- `security_level`
- `browser_check`
- bot-management settings
- custom rules that affect the MCP host

## References

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) when the incident also involves Access, Tunnel, DNS, or runtime state.
