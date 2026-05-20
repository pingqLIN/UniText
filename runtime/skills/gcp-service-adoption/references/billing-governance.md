---
runtime_projection: true
source_of_truth: registry/skills/gcp-service-adoption/references/billing-governance.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/gcp-service-adoption/references/billing-governance.md`
> Source of truth: `registry/skills/gcp-service-adoption/references/billing-governance.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Billing Governance

This step is mandatory for every recommendation.

## Minimum billing output

Every recommendation should state:

- expected cost drivers
- rough monthly estimate range with assumptions
- whether cost belongs in an existing bill or isolated project
- recommended budget amount
- threshold alerts
- owner for bill review

## Cost-driver checklist

Consider these categories:

- baseline fixed cost
- request or invocation volume
- compute time
- memory or CPU allocation
- storage volume
- network egress
- logging retention
- BigQuery query or storage cost if billing export is used

## Budget policy baseline

Unless the user has a stronger policy, recommend:

- budget amount based on expected monthly midpoint plus contingency
- threshold alerts at 50%, 80%, 100%
- explicit billing owner
- explicit engineering owner
- monthly review cadence for new workloads

## Strong recommendations

- Enable or verify Cloud Billing export to BigQuery when the workload is expected to persist
- Use labels or an isolated project to preserve cost attribution
- Treat missing billing ownership as a blocker for production rollout
- Document whether the estimate is directional or validated with actual pricing inputs
- Prefer a dedicated FinOps or billing-admin project for Budget API and Pricing API administration

## Automation paths

- For live budget inspection or payload generation, use [scripts/gcp_budget_api.py](../scripts/gcp_budget_api.py)
- For billing-account pricing discovery, use [scripts/gcp_pricing_api.py](../scripts/gcp_pricing_api.py)
- For live API rules and constraints, read [pricing-and-budget-apis.md](pricing-and-budget-apis.md)

## Review questions

- What would make the cost spike unexpectedly?
- Is there a free tier and when does it stop protecting the bill?
- Is idle cost acceptable if the feature adoption is low?
- Should this workload be capped, rate-limited, or shielded behind quota controls?
