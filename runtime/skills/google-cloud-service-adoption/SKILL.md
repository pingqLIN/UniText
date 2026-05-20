---
name: google-cloud-service-adoption
description: Alias entrypoint for Google Cloud and GCP service adoption work. Use when the user triggers $google-cloud-service-adoption or asks about Google Cloud projects, GCP services, Google APIs, Google OAuth, Google billing, or related Google platform setup that should route into the gcp-service-adoption workflow.
metadata:
  short-description: Alias for Google Cloud and GCP adoption
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/google-cloud-service-adoption/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/google-cloud-service-adoption/SKILL.md`
> Source of truth: `registry/skills/google-cloud-service-adoption/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Google Cloud Service Adoption Alias

This is a thin alias skill.

Use this skill when the user triggers `$google-cloud-service-adoption` or uses broad Google Cloud or GCP platform wording, but the actual task is about:

- Google Cloud or GCP service selection
- Google API enablement
- Google OAuth setup for an application
- Google Cloud project placement, billing, budgets, or governance
- Multi-project Google Cloud capability planning

When triggered, immediately use the `gcp-service-adoption` skill as the primary workflow.

Do not use this alias for:

- generic web search about Google
- consumer Google product help with no GCP or project component
- unrelated Google topics that are not about platform adoption or setup

## Routing rule

1. Treat this skill as an alias only.
2. Open and follow `gcp-service-adoption`.
3. Keep the final answer grounded in the actual Google Cloud or GCP task, not in the alias itself.
