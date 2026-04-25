---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/eval/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/eval/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/eval/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Event Hubs Recipe - Python Eval

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| Code Syntax | ✅ PASS | Python v2 model decorator pattern |
| Event Hub Trigger | ✅ PASS | Uses `@app.event_hub_message_trigger` |
| Batch Processing | ✅ PASS | Cardinality.MANY for throughput |
| Output Binding | ✅ PASS | `@app.event_hub_output` decorator |
| Health Endpoint | ✅ PASS | Anonymous auth |

## Code Validation

```python
# Validated patterns:
# - @app.event_hub_message_trigger with consumer_group
# - @app.event_hub_output for sending events
# - List[func.EventHubEvent] for batch processing
# - Proper event metadata logging (partition, sequence)
```

## Configuration Validated

- `EventHubConnection__fullyQualifiedNamespace` - UAMI binding
- `%EVENTHUB_NAME%` - Runtime config
- `%EVENTHUB_CONSUMER_GROUP%` - Consumer group
- Uses extension bundle v4

## Test Date

2025-02-18

## Verdict

**PASS** - Event Hubs recipe correctly implements both trigger and output bindings with proper batch processing and UAMI pattern.
