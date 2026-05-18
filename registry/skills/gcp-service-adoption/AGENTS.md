# AGENTS.md

Local rules for `Q:\gcp-service-adoption-skill`.

- Keep the project focused on a reusable GCP service-adoption skill, not a general GCP knowledge dump.
- Prefer extending `references/` over bloating `SKILL.md`.
- Keep references one level deep from `SKILL.md`.
- Keep scripts deterministic and CLI-friendly. Prefer JSON output when scripts summarize inventory or governance data.
- Do not add auxiliary docs like `README.md`, changelogs, or installation guides unless explicitly requested.
- Treat billing, budget thresholds, and ownership tracking as first-class workflow steps, not optional add-ons.
