---
name: cloudflare-named-tunnel-publish
description: "Use when the user wants to temporarily expose a localhost web app or static site on their own Cloudflare hostname using a named tunnel, especially for requests such as 掛在我的網域下, 暫時對外公開, named tunnel, local site publish, localhost to public URL, or quick-tunnel-to-custom-domain conversion. Do not use for quick tunnels, WARP-only issues, Access OAuth, Workers app deployment, or broad Cloudflare governance unless the task clearly spans those layers."
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/cloudflare-named-tunnel-publish/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-named-tunnel-publish/SKILL.md`
> Source of truth: `registry/skills/cloudflare-named-tunnel-publish/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Named Tunnel Publish

Use this skill for the narrow workflow of publishing a local site through a reversible Cloudflare named tunnel on a user-owned hostname.

Keep shared Cloudflare state changes minimal:

- prefer project-local tunnel credentials and config files
- treat `C:\Users\<user>\.cloudflared\cert.pem` as shared management state
- do not overwrite shared config files for unrelated services

## Use this skill for

- Publish `127.0.0.1:<port>` or a local static site to `https://<host>.<domain>`
- Replace a flaky quick tunnel with a user-owned Cloudflare hostname
- Create a project-local `cloudflared` config under `.runtime` or another repo-local runtime folder
- Verify that the public hostname really returns the expected HTML or API response
- Report the exact external URL and the cleanup path

## Do not use this skill for

- Quick tunnel experiments that do not need a named tunnel
- Cloudflare WARP, device posture, split tunnel, or Teams policy work
- Access OAuth, DCR, callback URL, or identity-provider setup
- Workers, Pages, or general Cloudflare app deployment
- Broad Cloudflare inventory or policy review across multiple products

## Workflow

### 1. Prove the local origin first

- Start or confirm the local server before touching Cloudflare.
- Verify the local origin returns the expected status and content type.
- For static sites, a simple local HTTP server is acceptable if the app does not require a framework dev server.

Read [references/workflow.md](references/workflow.md) for the exact command pattern and file layout.

### 2. Inventory shared Cloudflare state

- Check existing `cloudflared` configs, credential files, and named tunnels.
- Reuse the user domain only after confirming the requested hostname does not collide with an existing route.
- Treat shared `cert.pem` login state as sensitive and reversible.

### 3. Keep new artifacts project-local

- Write the new tunnel credential JSON into the project runtime folder, not the shared `.cloudflared` directory.
- Write the new `cloudflared` YAML config into the project runtime folder.
- Keep hostname-to-port routing isolated to the current project.

### 4. Repair management auth only when required

- If `cloudflared tunnel list`, `tunnel info`, or `tunnel route dns` return authentication errors, stop and report that the shared Cloudflare login is stale.
- Only back up or replace the shared `cert.pem` after explicit user approval.
- After fresh login, continue with named tunnel creation and DNS routing.

### 5. Create and run the named tunnel

- Create a dedicated named tunnel for the project.
- Map the requested hostname to that tunnel.
- Start `cloudflared tunnel run` with the project-local config.
- Keep the local origin process and the tunnel process IDs so the site can be torn down cleanly later.

### 6. Verify from the public edge

- Verify the final hostname, not just localhost.
- Confirm the public response matches the expected content type and status.
- On this Windows environment, prefer Python `urllib` when PowerShell web requests fail due to local TLS or Cloudflare-intercept issues.

Read [references/troubleshooting.md](references/troubleshooting.md) when verification disagrees with local origin health.

## Report format

Always end with:

- the exact external URL
- whether public verification returned the expected status and content type
- the active local server PID and tunnel PID when available
- the cleanup command to stop the temporary publish path

## Route to adjacent skills

- Use [cloudflare-tunnel-dns](../../../registry/skills/cloudflare-tunnel-dns/SKILL.md) when the task is mainly inventory, drift review, health endpoints, or hostname-to-ingress verification inside an existing workspace tunnel setup.
- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) when the request spans Access policy, Zero Trust device state, DNS governance, or cross-service Cloudflare review.
- Use [cloudflare-zerotrust-device](../../../registry/skills/cloudflare-zerotrust-device/SKILL.md) when the failure is primarily WARP or Teams pathing rather than named tunnel setup.
