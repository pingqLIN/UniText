# Local Port Allocation and Registry

Use this reference when a new project starts a local web app, API, MCP server, browser bridge, daemon, worker UI, WebSocket server, or any long-running localhost service.

## Principles

- Prefer one project-owned block instead of ad hoc ports.
- Record intended ports before starting long-running services.
- Keep actual machine-specific reservations local when they expose private paths, account names, or temporary tunnels.
- Do a dry-run check before updating shared config or starting a server.
- Avoid common default collisions unless the framework requires them and the port is free.

## Recommended Port Block

Allocate a contiguous 10-port block in `31000-39999`.

| Offset | Role |
| --- | --- |
| `+0` | primary frontend or UI |
| `+1` | API server |
| `+2` | WebSocket, SSE, or realtime bridge |
| `+3` | admin dashboard |
| `+4` | worker, queue, or background service |
| `+5` | database inspector or local console |
| `+6` | MCP or agent bridge |
| `+7` | test harness or replay server |
| `+8` | docs, Storybook, or preview |
| `+9` | reserved |

Example: if the project base is `31740`, frontend is `31740`, API is `31741`, and MCP is `31746`.

## Registry Locations

Use two layers:

- Repo-tracked intent: `ops/local-ports.json`
- Machine-local allocation ledger: `Q:\Projects\.local-port-registry.json`

If the central ledger does not exist, create it only after showing a dry-run summary. In public or portable templates, document the ledger path as optional local operator state.

## Registration Schema

```json
{
  "project": "example-project",
  "root": "Q:\\Projects\\example-project",
  "basePort": 31740,
  "ports": {
    "frontend": 31740,
    "api": 31741,
    "mcp": 31746
  },
  "owner": "local",
  "updatedAt": "2026-05-19"
}
```

## Preflight Checks

Before starting a server:

```powershell
Get-NetTCPConnection -LocalPort <port> -ErrorAction SilentlyContinue
Test-NetConnection 127.0.0.1 -Port <port>
```

If a required ecosystem default is used, such as `3000`, `5173`, `8000`, or `9222`, record it as an alias and still reserve a high-port fallback.

## Bootstrap Output

For projects with localhost services, include:

- selected base port
- role-to-port table
- registry path
- environment variables to set, such as `PORT`, `API_PORT`, or `MCP_PORT`
- collision check command
- whether the registration was dry-run only or applied
