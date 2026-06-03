# Project Selection

Use this file to determine whether the workload should land in an existing GCP project or a new one.

## Inventory checklist

At minimum, inspect:

- current authenticated account
- current default project
- candidate existing projects
- billing account availability
- APIs already enabled in each candidate project
- existing service accounts and IAM boundary expectations
- existing environment labels such as `env`, `owner`, `cost-center`

## Reuse an existing project when

- the same owning team already operates the workload there
- billing should roll up with the existing product
- IAM and secret access boundaries already align
- existing networking and region choices match the new workload
- observability and incident ownership are already established

## Prefer a new project when

- cost tracking must be isolated
- production blast radius needs a clean boundary
- the workload belongs to a different owner or business unit
- the service requires materially different IAM or network policy
- the workload is experimental and should not contaminate a stable production bill

## Decision output

Always state:

- candidate existing project or projects considered
- the reuse blockers, if any
- whether a new project is recommended
- the minimum setup still required even when reusing an existing project

## Enablement checklist

Tailor the list to the chosen service, but always consider:

- API enablement
- service account creation or reuse
- least-privilege IAM roles
- secret storage strategy
- region choice
- VPC, ingress, or egress constraints
- logging and metrics
- budget labels and ownership labels
