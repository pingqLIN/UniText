---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/timer/eval/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/timer/eval/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/timer/eval/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Timer Recipe Evaluation

**Date:** 2026-02-19T04:18:00Z
**Recipe:** timer
**Language:** Python
**Status:** ✅ PASS

## Deployment

| Property | Value |
|----------|-------|
| Function App | `func-api-gxlcc37knhe2m` |
| Resource Group | `rg-timer-func-dev` |
| Region | eastus2 |
| Base Template | `functions-quickstart-python-http-azd` |

## Test Results

### Health Endpoint
```bash
curl "https://func-api-gxlcc37knhe2m.azurewebsites.net/api/health?code=<key>"
```

**Response:**
```json
{"status": "healthy", "schedule": "0 */5 * * * *"}
```

### Functions Deployed
- `timer_trigger` - TimerTrigger (every 5 minutes)
- `health_check` - HTTP GET /health

## Configuration Applied

### App Settings
```
TIMER_SCHEDULE: "0 */5 * * * *"
```

### Source Code
- Replaced `function_app.py` with timer trigger code
- No IaC changes required (uses base Storage)

## Verdict

✅ **PASS** - Timer recipe works correctly:
- Timer trigger registered with correct schedule
- Health endpoint returns configured schedule
- No additional Azure resources required
