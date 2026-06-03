---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/references/family-review-2026-04-17.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/references/family-review-2026-04-17.md`
> Source of truth: `registry/skills/cloudflare-governance/references/family-review-2026-04-17.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Cloudflare Family Review 2026-04-17

## Outcome

- `cloudflare-governance` is now the default workspace entrypoint for Cloudflare operational and admin work.
- `cloudflare` remains the product and platform selection skill.
- Specialist skills now have clearer positive and negative triggers.
- Zero Trust device work now has a dedicated specialist skill and reusable scripts.

## Entry Model

| Entry type | Skill | Use for |
| --- | --- | --- |
| Platform architecture and product choice | `cloudflare` | Workers, Pages, storage, AI, networking product selection, IaC choice |
| Workspace operational routing | `cloudflare-governance` | WARP, Zero Trust device policy, Access, Tunnel, DNS, edge security, runtime drift |

## Specialist Coverage

| Skill | Scope |
| --- | --- |
| `cloudflare-zerotrust-device` | Local WARP, Zero Trust device behavior, split/full tunnel, Windows/WSL pathing, API credential verification |
| `cloudflare-access-mcp` | Access app OAuth, DCR, redirect URIs, MCP connector auth |
| `cloudflare-tunnel-dns` | Tunnel inventory, ingress, hostname routing, DNS linkage, health endpoints |
| `cloudflare-edge-security` | Zone security, browser checks, WAF, bot settings, skip rules |
| `cloudflare-runtime-sync` | Local TB2 runtime split, release metadata, sync scripts, service-state drift |

## Script Inventory

- `cloudflare-governance/scripts/inventory-cloudflare-scope.ps1`
- `cloudflare-zerotrust-device/scripts/verify-cloudflare-auth.ps1`
- `cloudflare-zerotrust-device/scripts/collect-cloudflare-zerotrust-baseline.ps1`
- `cloudflare-tunnel-dns/scripts/check-tunnel-runtime-alignment.ps1`

## Gaps Deferred

- No reusable Access/Tunnel/edge API inventory scripts yet.
- No automated baseline write-back into the maintenance-log project yet.
