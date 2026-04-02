# Current Baseline

This reference captures the current Cloudflare and local-service baseline for the TB2 workspace.

## Cloudflare

- Account ID: `00ba863c722b4372fa7efdd0e7c63b8d`
- Zone: `colorgeek.co`
- Zone ID: `37732a953a5cb59892aaaebddad4bbb4`
- Tunnel ID: `8f494f33-5983-4933-bb71-5812b56cad56`
- Tunnel name: `tb2-public-prod-20260330`
- Ingress:
  - `mcp.colorgeek.co` -> `http://127.0.0.1:3189`
  - `tb2-health.colorgeek.co` -> `http://127.0.0.1:3189`
- Access app: `tb2 MCP self-hosted`
- Access app ID: `59203b5c-9553-468a-880c-1936f3956aa9`
- OAuth enabled: `true`
- DCR enabled: `true`
- DCR redirect URIs:
  - `https://chatgpt.com/connector/oauth/Sfv7Ark1LNcp`
  - `https://chatgpt.com/connector/oauth/Sfv7ArklLNCp`
- Zone settings:
  - `security_level`: `medium`
  - `browser_check`: `on`
  - `bot_management.fight_mode`: `false`
  - `bot_management.crawler_protection`: `enabled`
  - `bot_management.ai_bots_protection`: `disabled`

## Local Runtime

- Source repo: `Q:\Projects\tb2-claude-subagent-workflow`
- Prod runtime: `Q:\Services\tb2-prod`
- Staging runtime: `Q:\Services\tb2-staging`
- Runtime release file: `Q:\Services\tb2-prod\release-info.json`
- Runtime cloudflared config: `Q:\Services\tb2-prod\ops\cloudflared.tb2.yml`
- Windows service `Cloudflared` exists but is `Stopped` and `Disabled`
