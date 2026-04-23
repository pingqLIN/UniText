---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/common/health-check.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/common/health-check.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/common/health-check.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Health Check Endpoint

> **RECOMMENDED**: Add a health endpoint for monitoring and load balancer probes.

## Python

```python
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        '{"status":"healthy"}',
        mimetype="application/json",
        status_code=200
    )
```

## TypeScript

```typescript
import { app, HttpRequest, HttpResponseInit, InvocationContext } from '@azure/functions';

app.http('health', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: async (request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> => {
        return {
            status: 200,
            jsonBody: { status: 'healthy' }
        };
    }
});
```

## JavaScript

```javascript
const { app } = require('@azure/functions');

app.http('health', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: async () => ({
        status: 200,
        jsonBody: { status: 'healthy' }
    })
});
```

## C# (.NET)

```csharp
public class Health
{
    [Function("health")]
    public HttpResponseData Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get")] HttpRequestData req)
    {
        var response = req.CreateResponse();
        response.Headers.Add("Content-Type", "application/json");
        response.WriteString("{\"status\":\"healthy\"}");
        return response;
    }
}
```

## Java

```java
@FunctionName("health")
public HttpResponseMessage health(
        @HttpTrigger(name = "req", methods = {HttpMethod.GET}, authLevel = AuthorizationLevel.ANONYMOUS)
        HttpRequestMessage<Optional<String>> request,
        final ExecutionContext context) {
    
    return request.createResponseBuilder(HttpStatus.OK)
            .header("Content-Type", "application/json")
            .body("{\"status\":\"healthy\"}")
            .build();
}
```

## PowerShell

**health/function.json:**
```json
{
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "Request",
      "methods": ["get"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "Response"
    }
  ]
}
```

**health/run.ps1:**
```powershell
param($Request, $TriggerMetadata)

Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = '{"status":"healthy"}'
    ContentType = 'application/json'
})
```

## Usage Notes

- **Auth level**: Use `anonymous` for load balancer probes
- **Response**: Return JSON with at least `{"status":"healthy"}`
- **Extended checks**: Can add database connectivity, dependency checks
- **Route**: Standard route is `/api/health`
