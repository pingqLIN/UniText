# Pricing and Budget APIs

Use this file when the skill needs live billing administration data instead of only a local template.

## Official paths

- Pricing API for public and billing-account-specific pricing
- Cloud Billing Budget API for listing, creating, and updating budgets
- Cloud Billing export to BigQuery for durable cost analysis

## What the official docs say

- Google documents the Pricing API as the way to get service, SKU, and price information. Public pricing requests use an API key, while billing-account-specific pricing can be queried with authenticated requests against billing-account resources.
- Google documents the Cloud Billing Budget API as a programmable way to list, create, patch, and delete budgets for a billing account.
- Google explicitly recommends using a separate FinOps-focused project for billing administration workflows.
- Google notes that the Budget API itself is free, but Pub/Sub notifications incur standard Pub/Sub charges.

## Local implementation rules

- Prefer authenticated REST calls using `gcloud auth print-access-token`.
- Treat listing budgets and pricing as safe read-only operations.
- Treat budget creation or updates as guarded operations. Default to dry-run payload generation unless the user explicitly wants a live API call.
- When calling the Budget API, include `x-goog-user-project` with the project where the Budget API is enabled.
- Keep BigQuery billing export as a governance recommendation unless the user explicitly asks to mutate billing configuration.

## Scripts

- `scripts/gcp_budget_api.py`
  - `preflight` to check whether the Budget API is enabled for the chosen `api-user-project`
  - `list` to inspect existing budgets
  - `payload` to generate a request body
  - `create` to print or optionally apply a budget request
- `scripts/gcp_pricing_api.py`
  - `list-sku-groups` with optional `--match` and `--limit`
  - `list-group-skus` with optional `--match` and `--limit`
  - `list-sku-prices`
  - `get-sku-price`

## Source links

- Budget API setup: https://docs.cloud.google.com/billing/docs/how-to/budget-api-setup
- Budget API usage: https://docs.cloud.google.com/billing/docs/how-to/budget-api
- Pricing API usage: https://docs.cloud.google.com/billing/docs/how-to/get-pricing-information-api
- Billing export setup: https://cloud.google.com/billing/docs/how-to/export-data-bigquery-setup
