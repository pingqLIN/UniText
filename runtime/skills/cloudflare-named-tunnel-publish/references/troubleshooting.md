---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-named-tunnel-publish/references/troubleshooting.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-named-tunnel-publish/references/troubleshooting.md`
> Source of truth: `registry/skills/cloudflare-named-tunnel-publish/references/troubleshooting.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Troubleshooting

## `cloudflared tunnel list` or `tunnel info` says `Authentication error`

Cause:

- the shared Cloudflare management login is stale

Fix:

1. report that shared Cloudflare auth has expired
2. ask for approval before touching `C:\Users\<user>\.cloudflared\cert.pem`
3. back up the old file
4. rerun `cloudflared.exe tunnel login`

Do not silently overwrite the shared cert.

## Tunnel creation succeeds but credential write fails with `Access is denied`

Typical message:

- tunnel was created but `cloudflared` could not write `C:\Users\<user>\.cloudflared\<id>.json`

Fix:

- rerun `cloudflared tunnel create` with `--credentials-file <project-local-json>`

This was the reliable fix in the Windows workflow that created:

- `Q:\Projects\<project>\.runtime\<project>-tunnel.json`

## Public URL returns `404` while localhost returns `200`

Check which path failed:

- quick tunnel
- named tunnel
- hostname mismatch

Quick tunnel-specific failure pattern:

- localhost is healthy
- `trycloudflare.com` URL returns `404`
- response headers include Cloudflare edge metadata

Interpretation:

- the quick tunnel path is unreliable for the current environment
- switch to a user-owned hostname on a named tunnel

## Browser opens a text-like document instead of the site

Do not assume the local HTML server is wrong.

Verify:

1. localhost returns `200`
2. localhost returns `Content-Type: text/html`
3. the public hostname returns the same content type

If localhost is healthy but the public URL is not, the issue is in the tunnel or edge path, not the HTML file itself.

## PowerShell `Invoke-WebRequest` fails with TLS or authentication noise

On this Windows environment, PowerShell web requests to Cloudflare can be misleading.

Preferred fallback:

- Python `urllib`

Use it for:

- Cloudflare API checks
- public hostname verification
- content-type confirmation

## `Resolve-DnsName` or networking cmdlets are missing

Do not block on that.

Fallbacks:

- verify through a real HTTPS request to the public hostname
- inspect the `cloudflared` runtime log
- use `python` request checks instead of relying on Windows networking cmdlets

## QUIC timeouts appear in the tunnel log

Interpret cautiously.

If the log later shows:

- `Registered tunnel connection`

then the tunnel is up even if some earlier QUIC attempts timed out.

## Cleanup is forgotten

Always report:

- origin PID
- tunnel PID
- exact `Stop-Process` command

Without cleanup details, a temporary publish path tends to linger longer than intended.
