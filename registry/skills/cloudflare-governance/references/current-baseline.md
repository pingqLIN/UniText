# Current Baseline

This reference captures the canonical fields that a Cloudflare workspace baseline should document without carrying live workspace values.

The live authoring-workspace copy belongs in `local/docs/CLOUDFLARE_WORKSPACE_BASELINE.md`, not in `registry/`.

## Cloudflare

- Account label: `workspace-account-label`
- Zone hostname: `workspace.example.com`
- Zone ID: `zone-id-redacted`
- Tunnel ID: `tunnel-id-redacted`
- Tunnel name: `workspace-tunnel-name`
- Ingress:
  - `mcp.workspace.example.com` -> `http://127.0.0.1:0000`
  - `health.workspace.example.com` -> `http://127.0.0.1:0000`
- Access app: `workspace-access-app`
- Access app ID: `access-app-id-redacted`
- OAuth enabled: `true`
- DCR enabled: `true`
- DCR redirect URIs:
  - `<connector-oauth-redirect-uri-redacted>`
- Zone settings:
  - `security_level`: `medium`
  - `browser_check`: `on`
  - `bot_management.fight_mode`: `false`
  - `bot_management.crawler_protection`: `enabled`
  - `bot_management.ai_bots_protection`: `disabled`

## Local Runtime

- Source repo: `<authoring-repo-path>`
- Prod runtime: `<prod-runtime-path>`
- Staging runtime: `<staging-runtime-path>`
- Runtime release file: `<runtime-release-file>`
- Runtime cloudflared config: `<cloudflared-config-path>`
- Windows service `Cloudflared`: `<service-state>`
