# Secret Manager Playbook

Use this when the chosen primary service is Secret Manager.

## Good fit

- Centralized secret storage for workloads already using managed GCP services
- Need for auditable access instead of local secret files

## Companion setup

- APIs: `secretmanager.googleapis.com`, `logging.googleapis.com`
- IAM: `roles/secretmanager.secretAccessor` only for runtime identities that need it
- Secrets: define naming, version rotation, and owner
- Networking: usually minimal, but note private-access expectations when relevant
- Observability: audit access logs and rotation events

## Cost review points

- secret version count
- access frequency

## Reuse blockers

- existing project has unclear secret ownership or shared high-privilege service accounts
- rotation and audit expectations are not documented
