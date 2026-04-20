---
runtime_projection: true
source_of_truth: registry/skills/azure-prepare/references/services/container-apps/scaling.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/azure-prepare/references/services/container-apps/scaling.md`
> Source of truth: `registry/skills/azure-prepare/references/services/container-apps/scaling.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Container Apps Scaling Patterns

## HTTP-based Scaling

Best for APIs and web applications:

```bicep
scale: {
  minReplicas: 1
  maxReplicas: 10
  rules: [
    {
      name: 'http-scaling'
      http: {
        metadata: {
          concurrentRequests: '100'
        }
      }
    }
  ]
}
```

## Queue-based Scaling

Best for background workers:

```bicep
scale: {
  minReplicas: 0
  maxReplicas: 30
  rules: [
    {
      name: 'queue-scaling'
      azureQueue: {
        queueName: 'orders'
        queueLength: 10
        auth: [
          {
            secretRef: 'storage-connection'
            triggerParameter: 'connection'
          }
        ]
      }
    }
  ]
}
```

## Service Bus Scaling

```bicep
scale: {
  minReplicas: 0
  maxReplicas: 20
  rules: [
    {
      name: 'servicebus-scaling'
      custom: {
        type: 'azure-servicebus'
        metadata: {
          queueName: 'myqueue'
          messageCount: '5'
        }
        auth: [
          {
            secretRef: 'servicebus-connection'
            triggerParameter: 'connection'
          }
        ]
      }
    }
  ]
}
```

## Recommendations

| Workload | Min Replicas | Max Replicas | Rule Type |
|----------|--------------|--------------|-----------|
| Production API | 1 | 10-20 | HTTP |
| Dev/Test API | 0 | 5 | HTTP |
| Background Worker | 0 | 30+ | Queue/Event |
| Scheduled Job | 0 | 1 | KEDA cron |
