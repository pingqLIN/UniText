---
name: cloudflare-governance
description: Use when deciding which Cloudflare governance skill to use, or when doing a broad baseline/dry-run review across Access, tunnel, DNS, edge security, and local runtime settings.
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/SKILL.md`
> Source of truth: `registry/skills/cloudflare-governance/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Governance

## Purpose

This is the routing skill for Cloudflare-related work in this workspace.

## Use This Skill When

- You need to decide which Cloudflare sub-skill should handle the task.
- You want a broad baseline check before a narrower action.
- You need a dry-run summary that spans more than one Cloudflare layer.

## Route To

- Access and OAuth or DCR: [cloudflare-access-mcp](../../../registry/skills/cloudflare-access-mcp/SKILL.md)
- Tunnel and DNS: [cloudflare-tunnel-dns](../../../registry/skills/cloudflare-tunnel-dns/SKILL.md)
- Edge security and WAF: [cloudflare-edge-security](../../../registry/skills/cloudflare-edge-security/SKILL.md)
- Local runtime sync and release state: [cloudflare-runtime-sync](../../../registry/skills/cloudflare-runtime-sync/SKILL.md)

## Baseline

- [current-baseline.md](references/current-baseline.md)
- [dry-run-report.md](references/dry-run-report.md)
- [workflow-guide.md](references/workflow-guide.md)

## Handoff Rule

- Start here when the task touches more than one Cloudflare layer.
- Route down to a focused sub-skill once the active change surface is clear.
- Route back here if the task expands across Access, Tunnel, DNS, edge security, and runtime state.
