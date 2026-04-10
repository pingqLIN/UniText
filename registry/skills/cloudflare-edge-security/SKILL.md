---
name: cloudflare-edge-security
description: Use when auditing or changing Cloudflare zone security, browser checks, bot protection, WAF custom rules, or skip rules for specific hosts and paths.
---

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

- [workspace baseline](../cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) when the incident also involves Access, Tunnel, DNS, or runtime state.
