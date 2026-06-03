# Service Mapping

Use this file to map a user capability to a primary Google Cloud service.
Prefer one primary recommendation plus a small alternative set.

## Common mappings

| Capability | Primary service | Common alternatives | Notes |
| --- | --- | --- | --- |
| Object and file storage | Cloud Storage | Filestore | Default to Cloud Storage unless POSIX semantics are required |
| Scheduled HTTP or job trigger | Cloud Scheduler | Workflows, Cloud Tasks | Scheduler is for time-based triggers, not durable queue semantics |
| Event bus and pub/sub messaging | Pub/Sub | Eventarc | Pub/Sub for messaging backbone, Eventarc for event routing into managed runtimes |
| Stateless containerized app | Cloud Run | GKE | Default to Cloud Run unless low-level cluster control is actually needed |
| Function-style event or HTTP code | Cloud Functions | Cloud Run | Prefer Cloud Run when the project may grow beyond function-style packaging |
| Secret storage | Secret Manager | none | Treat as standard companion service, not an optional enhancement |
| Model inference and managed AI | Vertex AI | Gemini API depending on product shape | Decide based on governance, model control, and integration needs |
| Analytics warehouse | BigQuery | Cloud SQL | BigQuery for analytics, not transactional app storage |
| Relational application data | Cloud SQL | AlloyDB, Firestore | Default to Cloud SQL unless scale or document model changes the fit |
| Document or key-value app data | Firestore | Cloud SQL | Prefer Firestore only when access patterns truly fit document storage |

## Selection prompts

Before finalizing, answer these:

- Is this workload request-response, event-driven, scheduled, or batch?
- Does the team need strong IAM and billing separation from existing workloads?
- Is there a durable data requirement or only integration with an existing system?
- Does the runtime need private networking, static egress, or VPC access?
- Is cost dominated by idle baseline, request volume, compute time, storage, or egress?

## Default companion services

When recommending a primary service, assume these companions may also be needed:

- Secret Manager
- Cloud Logging
- Cloud Monitoring and alerting
- Billing budget and threshold alerts
- labels for owner, environment, and cost-center
