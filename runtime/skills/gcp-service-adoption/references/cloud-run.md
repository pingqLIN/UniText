---
runtime_projection: true
source_of_truth: registry/skills/gcp-service-adoption/references/cloud-run.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/gcp-service-adoption/references/cloud-run.md`
> Source of truth: `registry/skills/gcp-service-adoption/references/cloud-run.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Cloud Run Playbook

Use this when the chosen primary service is Cloud Run.

## Good fit

- Stateless HTTP service
- Containerized workloads
- Variable traffic with low idle tolerance

## Companion setup

- APIs: `run.googleapis.com`, `artifactregistry.googleapis.com`, `logging.googleapis.com`, `monitoring.googleapis.com`, `secretmanager.googleapis.com`
- IAM: service runtime identity, deployer identity, artifact registry read access, service account user binding
- Secrets: prefer Secret Manager rather than env files for production credentials
- Networking: decide ingress mode, egress path, and whether Serverless VPC Access is required
- Observability: request count, latency, error rate, cold-start complaints, and budget burn

## Cost review points

- request volume
- CPU and memory allocation
- minimum instances if used
- egress

## Reuse blockers

- existing project has broad public ingress defaults that do not fit the workload
- billing ownership is unclear
- no label discipline for cost attribution
