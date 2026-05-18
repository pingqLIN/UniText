# Cloud Storage Playbook

Use this when the chosen primary service is Cloud Storage.

## Good fit

- File or object persistence
- Exports, archives, uploads, generated artifacts

## Companion setup

- APIs: `storage.googleapis.com`, `logging.googleapis.com`, `monitoring.googleapis.com`
- IAM: bucket-level least privilege for writers and readers
- Secrets: usually not primary, but adjacent workloads still need secret handling
- Networking: decide public, signed URL, or private-only access
- Observability: storage growth, request classes, object lifecycle, and egress

## Cost review points

- storage class
- object count and operations
- retrieval pattern
- cross-region or internet egress

## Reuse blockers

- existing project lacks clear bucket ownership boundaries
- retention or lifecycle policy conflicts with the new workload
