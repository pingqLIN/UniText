---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/source/javascript.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/source/javascript.md`
> Source of truth: `registry/skills/azure-prepare/references/services/functions/templates/recipes/eventhubs/source/javascript.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# JavaScript Event Hubs Trigger

## Dependencies

**package.json:**
```json
{
  "dependencies": {
    "@azure/functions": "^4.0.0"
  }
}
```

## Source Code

**src/functions/eventHubTrigger.js:**
```javascript
const { app } = require('@azure/functions');

app.eventHub('eventHubTrigger', {
    connection: 'EventHubConnection',
    eventHubName: '%EVENTHUB_NAME%',
    cardinality: 'many',
    consumerGroup: '%EVENTHUB_CONSUMER_GROUP%',
    handler: async (messages, context) => {
        if (Array.isArray(messages)) {
            context.log(`Event Hub trigger processed ${messages.length} messages`);
            for (const message of messages) {
                context.log(`Message: ${JSON.stringify(message)}`);
            }
        } else {
            context.log(`Event Hub trigger processed message: ${JSON.stringify(messages)}`);
        }
    }
});
```

**src/functions/healthCheck.js:**
```javascript
const { app } = require('@azure/functions');

app.http('health', {
    methods: ['GET'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        return {
            status: 200,
            jsonBody: { 
                status: 'healthy',
                trigger: 'eventhubs'
            }
        };
    }
});
```

## Files to Remove

- `src/functions/httpTrigger.js`

## App Settings Required

```
EventHubConnection__fullyQualifiedNamespace=<namespace>.servicebus.windows.net
EventHubConnection__credential=managedidentity
EventHubConnection__clientId=<uami-client-id>
EVENTHUB_NAME=<hub-name>
EVENTHUB_CONSUMER_GROUP=$Default
```

## Common Patterns

- [Node.js Entry Point](../../common/nodejs-entry-point.md) — **REQUIRED** src/index.js setup
- [Error Handling](../../common/error-handling.md) — Try/catch + logging patterns
- [Health Check](../../common/health-check.md) — Health endpoint for monitoring
- [UAMI Bindings](../../common/uami-bindings.md) — Managed identity settings
