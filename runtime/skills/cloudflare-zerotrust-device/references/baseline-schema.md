---
runtime_projection: true
source_of_truth: registry/skills/cloudflare-zerotrust-device/references/baseline-schema.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-zerotrust-device/references/baseline-schema.md`
> Source of truth: `registry/skills/cloudflare-zerotrust-device/references/baseline-schema.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Zero Trust Baseline Schema

The baseline collection script should emit a JSON object with these top-level keys:

- `collectedAt`
- `computerName`
- `accountIdHint`
- `tools`
- `warp`
- `windows`
- `wsl`
- `correlation`
- `networkProbes`

## Required subfields

### `tools`

- `warpCliAvailable`
- `wslAvailable`
- `cloudflaredAvailable`

### `warp`

- `statusText`
- `settingsText`
- `registrationText`
- `tunnelDumpText`
- `summary`

### `windows`

- `routeText`

### `wsl`

- `distrosText`
- `ubuntuAvailable`
- `routeText`

### `correlation`

- `localAccountId`
- `localOrganization`
- `accountIdHint`
- `accountIdMatches`

### `networkProbes`

- `windowsTraceText`
- `wslTraceText`
- `errors`

## `warp.summary`

- `organization`
- `accountId`
- `mode`
- `allowModeSwitch`
- `alwaysOn`
- `routingMode`
- `includeModeDetected`
- `excludeModeDetected`
- `policyLocked`

Keep the JSON stable even when some tools are missing. Missing data should be represented by `null`, `false`, or an empty list rather than by deleting keys.
