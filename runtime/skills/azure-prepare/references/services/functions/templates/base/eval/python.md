---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/base/eval/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/base/eval/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/base/eval/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Base HTTP Template - Python Eval

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| Code Syntax | ✅ PASS | AST parse successful |
| Function Routes | ✅ PASS | /api/hello, /api/health defined |
| v2 Model | ✅ PASS | Uses `func.FunctionApp()` decorator model |
| Health Endpoint | ✅ PASS | Anonymous auth, JSON response |

## Code Validation

```python
# Validated syntax and structure
import ast
with open('function_app.py') as f:
    ast.parse(f.read())
# ✅ Code syntax valid
```

## Test Date

2025-02-18

## Template Source

Generated from base template using `func init --python -m V2`

## Verdict

**PASS** - Base HTTP template code validates correctly for Python v2 model.
