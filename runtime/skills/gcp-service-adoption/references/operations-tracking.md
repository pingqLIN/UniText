---
runtime_projection: true
source_of_truth: registry/skills/gcp-service-adoption/references/operations-tracking.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/gcp-service-adoption/references/operations-tracking.md`
> Source of truth: `registry/skills/gcp-service-adoption/references/operations-tracking.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Operations Tracking

Use this file to define the post-adoption tracking plan.

## Required owners

- product or feature owner
- technical owner
- billing owner
- incident contact

## Minimum tracking fields

- chosen GCP service
- target project
- environment
- region
- APIs enabled
- service account and IAM notes
- budget amount
- alert thresholds
- success metrics
- risk notes
- next review date

## Review cadence

Recommend this baseline unless the user provides a better one:

- weekly review during first rollout phase
- monthly service and cost review after stabilization
- quarterly access and IAM review

## Suggested operational metrics

- usage volume
- error rate
- latency or job duration
- monthly spend
- budget burn percentage
- alert count

## Alert handling

Budget alerts should route to named humans, not only shared inboxes.
When budgets breach 80% early, require an explicit review of traffic, retention, and architecture assumptions.
