---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/references/routing-matrix.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/references/routing-matrix.md`
> Source of truth: `registry/skills/cloudflare-governance/references/routing-matrix.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Cloudflare Routing Matrix

Use this matrix from `cloudflare-governance` when the user asks something broad or ambiguous.

| Intent or signal | Primary skill | Secondary skill | Scripts | Notes |
| --- | --- | --- | --- | --- |
| WARP connected but `warp=off`, split tunnel vs full tunnel, Windows vs WSL path | `cloudflare-zerotrust-device` | `cloudflare-governance` | `cloudflare-zerotrust-device/scripts/collect-cloudflare-zerotrust-baseline.ps1`, `cloudflare-zerotrust-device/scripts/verify-cloudflare-auth.ps1` | Local-first. Treat device policy as distinct from zone settings. |
| Verify `CF_API_TOKEN`, Global API Key, or tunnel API access | `cloudflare-zerotrust-device` | `cloudflare-governance` | `cloudflare-zerotrust-device/scripts/verify-cloudflare-auth.ps1` | Prefer API token. Fall back to Global API Key plus email. |
| Tunnel IDs, ingress mapping, hostname routing, DNS linkage, health routes | `cloudflare-tunnel-dns` | `cloudflare-runtime-sync` | Workspace `cloudflared` configs | Route here after auth is known. |
| Compare authoring/prod/staging tunnel config against runtime metadata and DNS tunnel records | `cloudflare-tunnel-dns` | `cloudflare-governance` | `cloudflare-tunnel-dns/scripts/check-tunnel-runtime-alignment.ps1` | Use after governance inventory when you want a read-only drift report. |
| Access app OAuth, DCR, redirect URIs, connector auth, Access policies for MCP | `cloudflare-access-mcp` | `cloudflare-governance` | None yet | Do not mix with tunnel routing unless the incident clearly spans both. |
| Zone security level, browser check, WAF, skip rules, bot settings | `cloudflare-edge-security` | `cloudflare-governance` | None yet | Zone-level, not device-level. |
| TB2 runtime split, release metadata, sync scripts, local service drift | `cloudflare-runtime-sync` | `cloudflare-tunnel-dns` | Runtime sync scripts | Workspace/runtime scope only. |
| Broad Cloudflare audit, family review, “check Cloudflare settings” | `cloudflare-governance` | One or more specialists | Script catalog below | Governance should classify before any deep procedure. |
| Cloudflare account/zone/tunnel/Access inventory before deciding next specialist | `cloudflare-governance` | One or more specialists | `cloudflare-governance/scripts/inventory-cloudflare-scope.ps1` | Use as the first read-only discovery pass for broad admin questions. |

## Negative Trigger Notes

- Do not route WARP or Zero Trust device questions to `cloudflare-edge-security`.
- Do not route tunnel or ingress questions to `cloudflare-access-mcp`.
- Do not route runtime split questions to `cloudflare-zerotrust-device`.
- Do not route broad family-review requests directly to a specialist unless the user explicitly names one.
