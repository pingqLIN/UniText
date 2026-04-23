---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/references/cloudflare-family-review-checklist.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/references/cloudflare-family-review-checklist.md`
> Source of truth: `registry/skills/cloudflare-governance/references/cloudflare-family-review-checklist.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Cloudflare Family Review Checklist

Use this after changing any Cloudflare skill.

## Routing

- Broad Cloudflare prompts route to `cloudflare-governance`.
- Explicit specialist prompts still match the intended specialist directly.
- Each prompt in the review set has one clear primary skill.

## Boundaries

- `cloudflare-zerotrust-device` only covers local WARP, device policy interpretation, auth verification, and evidence collection.
- `cloudflare-tunnel-dns` only covers tunnel, hostname, ingress, and DNS.
- `cloudflare-access-mcp` only covers Access app auth, DCR, redirect URIs, and MCP connector auth.
- `cloudflare-edge-security` only covers zone security, WAF, browser check, and bot rules.
- `cloudflare-runtime-sync` only covers local runtime split and release-state issues.

## Scripts

- Every Cloudflare script appears in `script-catalog.md`.
- Every script has one owning specialist skill.
- Every script can fail safely without printing secrets.
- Governance-owned scripts stay read-only and discovery-oriented.

## Consistency

- Terminology is consistent across the family: account, zone, tunnel, Access, Zero Trust, WARP.
- Handoff links point to the right adjacent skills.
- Relative file links resolve correctly.
