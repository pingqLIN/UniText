---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/sql/eval/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/sql/eval/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/sql/eval/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# SQL Recipe - Python Eval

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| Code Syntax | ✅ PASS | Python v2 model decorator pattern |
| SQL Input | ✅ PASS | Uses `@app.sql_input` decorator |
| SQL Output | ✅ PASS | Uses `@app.sql_output` decorator |
| SQL Trigger | ✅ PASS | Change tracking with `@app.sql_trigger` |
| Health Endpoint | ✅ PASS | Anonymous auth |

## Code Validation

```python
# Validated patterns:
# - @app.sql_input for reading data
# - @app.sql_output for writing data
# - @app.sql_trigger for change detection
# - Parameterized queries with @param
```

## Configuration Validated

- `SqlConnectionString` - Connection string or UAMI
- Table/view names configurable
- Uses SQL extension bundle

## Grounding Source

[Azure-Samples/functions-quickstart-python-azd-sql](https://github.com/Azure-Samples/functions-quickstart-python-azd-sql)

## Test Date

2025-02-18

## Verdict

**PASS** - SQL recipe correctly implements input, output, and trigger bindings following the official AZD template patterns.
