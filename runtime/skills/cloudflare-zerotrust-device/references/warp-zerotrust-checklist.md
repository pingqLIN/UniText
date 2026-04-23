---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-zerotrust-device/references/warp-zerotrust-checklist.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-zerotrust-device/references/warp-zerotrust-checklist.md`
> Source of truth: `registry/skills/cloudflare-zerotrust-device/references/warp-zerotrust-checklist.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# WARP and Zero Trust Checklist

## Local-first checks

- `warp-cli status`
- `warp-cli settings`
- `warp-cli registration show`
- `warp-cli tunnel dump`
- `route print -4`
- Windows trace: `curl.exe https://www.cloudflare.com/cdn-cgi/trace`
- WSL trace: `wsl -d Ubuntu -- bash -lc "curl -s https://www.cloudflare.com/cdn-cgi/trace"`

## Interpretation rules

- `warp=off` with `Status update: Connected` usually means the public traffic being tested is not using full tunnel.
- `Allow Mode Switch: false` means the org is enforcing the mode from policy.
- `Operation not authorized in this context` after `warp-cli mode ...` confirms the client cannot override the policy locally.
- `Include mode` or a narrow tunnel dump usually means split tunnel or include-only routing.

## Credential verification

- API token verification endpoint:
  - `GET /client/v4/user/tokens/verify`
- Global API Key verification endpoint:
  - `GET /client/v4/user`
- Tunnel access smoke test:
  - `GET /client/v4/accounts/{account_id}/cfd_tunnel`

## Correlation targets

- Local WARP org name
- Local account ID from `warp-cli registration show`
- Workspace baseline account ID
- Tunnel account ID and tunnel inventory
- Zone hostname and Access app domain

## Good candidates for proceduralization

- Local WARP baseline collection
- API token vs Global API Key verification
- Account-level tunnel access smoke test
- Split tunnel vs full tunnel interpretation
- Windows vs WSL Cloudflare trace comparison
