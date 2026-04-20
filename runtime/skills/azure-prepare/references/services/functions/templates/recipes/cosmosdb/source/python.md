---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/cosmosdb/source/python.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/cosmosdb/source/python.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/cosmosdb/source/python.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Cosmos DB Trigger — Python

## Trigger Function

Replace the HTTP trigger function in `function_app.py` with this Cosmos DB trigger.

### function_app.py

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.cosmos_db_trigger(
    arg_name="documents",
    container_name="%COSMOS_CONTAINER_NAME%",
    database_name="%COSMOS_DATABASE_NAME%",
    connection="COSMOS_CONNECTION",
    lease_container_name="leases",
    create_lease_container_if_not_exists=True
)
def cosmos_trigger(documents: func.DocumentList):
    logging.info(f"Cosmos DB trigger function processed {len(documents)} document(s)")

    for doc in documents:
        logging.info(f"Document Id: {doc['id']}")
```

## Requirements

Add to `requirements.txt`:

```
azure-functions
```

> The Cosmos DB extension is included in the Functions v4 extension bundle — no additional pip package needed.

## local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "COSMOS_CONNECTION__accountEndpoint": "https://{accountName}.documents.azure.com:443/",
    "COSMOS_DATABASE_NAME": "documents-db",
    "COSMOS_CONTAINER_NAME": "documents"
  }
}
```

## Files to Modify in HTTP Base

- Replace contents of `function_app.py` (remove HTTP GET/POST handlers)

## Common Patterns

- [Error Handling](../../common/error-handling.md) — Try/catch + logging patterns
- [Health Check](../../common/health-check.md) — Health endpoint for monitoring
- [UAMI Bindings](../../common/uami-bindings.md) — Managed identity settings
