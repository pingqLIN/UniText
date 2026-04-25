---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/event-grid/subscriptions.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/event-grid/subscriptions.md`
> Source of truth: `registry/skills/azure-prepare/references/services/event-grid/subscriptions.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Event Grid - Subscriptions

## Event Subscription

```bicep
resource eventGridSubscription 'Microsoft.EventGrid/topics/eventSubscriptions@2023-12-15-preview' = {
  parent: eventGridTopic
  name: 'order-processor-subscription'
  properties: {
    destination: {
      endpointType: 'WebHook'
      properties: {
        endpointUrl: 'https://my-api.azurecontainerapps.io/webhooks/orders'
      }
    }
    filter: {
      includedEventTypes: [
        'Order.Created'
        'Order.Updated'
      ]
    }
    retryPolicy: {
      maxDeliveryAttempts: 30
      eventTimeToLiveInMinutes: 1440
    }
  }
}
```

## Destination Types

### Webhook

```bicep
destination: {
  endpointType: 'WebHook'
  properties: {
    endpointUrl: 'https://my-api.example.com/events'
  }
}
```

### Azure Function

```bicep
destination: {
  endpointType: 'AzureFunction'
  properties: {
    resourceId: functionApp.id
  }
}
```

### Service Bus Queue

```bicep
destination: {
  endpointType: 'ServiceBusQueue'
  properties: {
    resourceId: '${serviceBus.id}/queues/events'
  }
}
```

### Event Hub

```bicep
destination: {
  endpointType: 'EventHub'
  properties: {
    resourceId: eventHub.id
  }
}
```

## Filtering

### Event Type Filter

```bicep
filter: {
  includedEventTypes: [
    'Order.Created'
    'Order.Shipped'
  ]
}
```

### Subject Filter

```bicep
filter: {
  subjectBeginsWith: '/orders/priority'
  subjectEndsWith: '.json'
}
```

### Advanced Filter

```bicep
filter: {
  advancedFilters: [
    {
      operatorType: 'NumberGreaterThan'
      key: 'data.amount'
      value: 100
    }
  ]
}
```
