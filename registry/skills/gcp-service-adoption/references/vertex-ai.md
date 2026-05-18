# Vertex AI Playbook

Use this when the chosen primary service is Vertex AI.

## Good fit

- Managed model inference
- Model tuning or training workflows
- Need for Google-managed ML governance and ecosystem integration

## Companion setup

- APIs: `aiplatform.googleapis.com`, `logging.googleapis.com`, `monitoring.googleapis.com`, `secretmanager.googleapis.com`
- IAM: Vertex AI user role plus service-account usage boundaries
- Secrets: centralize API credentials and external integration tokens in Secret Manager
- Networking: confirm region, residency, and whether private connectivity is required
- Observability: quota, latency, error classes, spend burn, and per-model usage

## Cost review points

- request volume or token volume
- model class or endpoint type
- training job time
- stored artifacts and egress

## Reuse blockers

- existing project mixes unrelated experimental and production AI spend
- quota ownership is unclear
- no budget alerting for bursty model usage
