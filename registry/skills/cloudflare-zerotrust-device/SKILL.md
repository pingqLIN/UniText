---
name: cloudflare-zerotrust-device
description: Use when the request is specifically about Cloudflare WARP, Zero Trust device behavior, split tunnel vs full tunnel interpretation, Windows and WSL traffic path through WARP, or Cloudflare API credential verification. Trigger for tasks like "why is WARP connected but warp=off", "check full-tunnel vs split-tunnel", "compare WARP org to Cloudflare account", "verify CF_API_TOKEN or Global API Key", or "test Cloudflare Tunnel API access". Do not use for tunnel ingress, DNS routing, Access OAuth, or zone-edge security unless the issue is explicitly a local WARP/device incident.
metadata:
  runtime_support_files: true
---

# Cloudflare Zero Trust Device

## Scope

- Local `warp-cli` state and policy interpretation
- Zero Trust org and account correlation
- Split tunnel vs full tunnel checks
- Windows and WSL traffic path through WARP
- Cloudflare API token and Global API Key verification
- Account-level tunnel API access checks

## Default Entry

- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) first for broad Cloudflare requests.
- Use this skill directly when the request is already clearly about local WARP behavior, Zero Trust device policy, or Cloudflare credential validation.

## Workflow

1. Collect local state before making assumptions.
   - Check `warp-cli status`, `warp-cli settings`, `warp-cli registration show`, and `warp-cli tunnel dump`.
   - For routing symptoms, compare `route print`, WSL `ip route`, and Cloudflare trace output from both Windows and WSL.
2. Identify whether the behavior is policy-controlled.
   - If `Allow Mode Switch: false` or `warp-cli mode ...` returns `Operation not authorized`, treat the device as policy-locked.
   - If trace shows `warp=off` while WARP is connected, determine whether the org is using split tunnel or include-only policy before blaming the client.
3. Correlate local and account evidence.
   - Compare local WARP org and account identifiers with workspace baseline files and tunnel inventory.
   - Keep account-level and zone-level facts separate from local client state.
4. Verify API credentials with the bundled script when account checks are needed.
   - Use [scripts/verify-cloudflare-auth.ps1](scripts/verify-cloudflare-auth.ps1).
   - Use [scripts/collect-cloudflare-zerotrust-baseline.ps1](scripts/collect-cloudflare-zerotrust-baseline.ps1) when you need a reusable local evidence pack before making routing or policy claims.
   - Prefer API tokens first.
   - Fall back to Global API Key plus email only when necessary.
5. Route to a narrower Cloudflare skill once the active change surface is clear.
   - Access app, OAuth, DCR, or redirect URIs -> [cloudflare-access-mcp](../cloudflare-access-mcp/SKILL.md)
   - Tunnel ingress, hostnames, or health routing -> [cloudflare-tunnel-dns](../cloudflare-tunnel-dns/SKILL.md)
   - WAF, browser check, bot rules, or skip rules -> [cloudflare-edge-security](../cloudflare-edge-security/SKILL.md)
   - Runtime split and local TB2 service state -> [cloudflare-runtime-sync](../cloudflare-runtime-sync/SKILL.md)

## Safety

- Never print full API tokens or Global API Keys.
- If the user pasted a secret into chat, recommend rotating it after validation or admin work is done.
- Treat `cloudflared cert.pem` as tunnel-management evidence, not as a substitute for Zero Trust admin API credentials.

## References

- [warp-zerotrust-checklist.md](references/warp-zerotrust-checklist.md)
- [baseline-schema.md](references/baseline-schema.md)
