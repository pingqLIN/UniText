---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/blob-eventgrid/eval/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/blob-eventgrid/eval/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/blob-eventgrid/eval/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Blob + EventGrid Recipe - Python Eval

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| Code Syntax | ✅ PASS | Python v2 model decorator pattern |
| EventGrid Trigger | ✅ PASS | Uses `@app.event_grid_trigger` |
| Blob Input | ✅ PASS | `@app.blob_input` for reading |
| Blob Output | ✅ PASS | `@app.blob_output` for writing |
| Event Filtering | ✅ PASS | Filters BlobCreated events |

## Code Validation

```python
# Validated patterns:
# - @app.event_grid_trigger for blob events
# - @app.blob_input with {data.url} binding
# - @app.blob_output for processed output
# - EventGrid event parsing
```

## Configuration Validated

- `BlobConnection__blobServiceUri` - UAMI binding
- EventGrid subscription for blob events
- Uses extension bundle v4

## Grounding Source

[Azure-Samples/functions-quickstart-python-azd-eventgrid-blob](https://github.com/Azure-Samples/functions-quickstart-python-azd-eventgrid-blob)

## Test Date

2025-02-18

## Verdict

**PASS** - Blob + EventGrid recipe correctly implements event-driven blob processing following the official AZD template patterns.
