---
runtime_projection: true
source_of_truth: registry/skills/appinsights-instrumentation/references/sdk/azure-monitor-opentelemetry-py.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/appinsights-instrumentation/references/sdk/azure-monitor-opentelemetry-py.md`
> Source of truth: `registry/skills/appinsights-instrumentation/references/sdk/azure-monitor-opentelemetry-py.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Azure Monitor OpenTelemetry — Python SDK Quick Reference

> Condensed from **azure-monitor-opentelemetry-py**. Full patterns
> (Flask/Django/FastAPI, custom metrics, sampling, live metrics)
> in the **azure-monitor-opentelemetry-py** plugin skill if installed.

## Install
```bash
pip install azure-monitor-opentelemetry
```

## Quick Start
```python
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor()
```

## Best Practices
- Call configure_azure_monitor() early — before importing instrumented libraries
- Use environment variables for connection string in production
- Set cloud role name for multi-service Application Map
- Enable sampling in high-traffic applications
- Use structured logging for better log analytics queries
- Add custom attributes to spans for better debugging
- Use AAD authentication for production workloads
