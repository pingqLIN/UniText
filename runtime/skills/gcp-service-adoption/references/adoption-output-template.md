---
runtime_projection: true
source_of_truth: registry/skills/gcp-service-adoption/references/adoption-output-template.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/gcp-service-adoption/references/adoption-output-template.md`
> Source of truth: `registry/skills/gcp-service-adoption/references/adoption-output-template.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Adoption Output Template

Use this template for the final recommendation.

## 1. Requested capability

- What the project needs
- What assumptions were made

## 2. Recommended GCP service

- Primary service
- Alternatives considered
- Why the primary service wins

## 3. Existing-project fit

- Candidate project or projects
- Billing fit
- IAM and ownership fit
- Observability fit

## 4. Reuse or new-project decision

- Decision
- Main reasons
- Known blockers

## 5. Required setup checklist

- APIs
- IAM and service accounts
- secrets
- networking
- observability
- labels and ownership metadata

## 6. Cost and budget plan

- Monthly estimate range and assumptions
- Main cost drivers
- Budget amount
- Alert thresholds
- Billing owner

## 7. Ongoing tracking plan

- Technical owner
- Review cadence
- Key metrics
- Trigger for revisiting the architecture
