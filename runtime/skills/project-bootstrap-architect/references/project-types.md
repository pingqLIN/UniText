---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/project-types.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/project-types.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/project-types.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Project Types

Use this file to map user intent to one primary archetype.

## CLI tool

Use when the main user experience is terminal-first.

Signals:

- command-line utility
- developer tool
- automation runner
- local assistant shell

Typical outputs:

- `src/cli/`
- `src/commands/`
- config loader
- terminal-friendly logging

## Web app

Use when the main surface is browser UI owned by the project.

Signals:

- dashboard
- authenticated app
- internal tool
- SaaS product
- admin panel

Typical outputs:

- `apps/web/` or `src/app/`
- `components/`
- `features/`
- `lib/`
- `public/`
- locale folders for UI copy

## Browser extension

Use when the app runs primarily inside the browser extension model.

Signals:

- popup
- side panel
- content script
- background worker

Typical outputs:

- `src/background/`
- `src/content/`
- `src/popup/`
- `src/options/`
- `manifest.json`

## Service API

Use when the primary responsibility is serving network requests.

Signals:

- REST API
- webhook handler
- auth server
- JSON backend

Typical outputs:

- `src/server/`
- `src/routes/`
- `src/services/`
- `src/db/`
- migration strategy

## Desktop helper

Use when the project coordinates local tools, files, OS automation, or local models.

Signals:

- tray app
- local daemon
- local agent
- desktop automation

Typical outputs:

- `src/agent/`
- `src/tools/`
- `src/integrations/`
- `src/state/`
- local config and logs directories

## Shared library or SDK

Use when the main deliverable is imported by other projects.

Signals:

- npm package
- reusable toolkit
- shared utility layer

Typical outputs:

- `src/`
- `test/`
- public API entrypoint
- typed exports

## Automation or worker service

Use when the project runs scheduled jobs or queue-driven work.

Signals:

- cron
- queue consumer
- scraper
- background processor

Typical outputs:

- `src/jobs/`
- `src/workers/`
- `src/adapters/`
- `src/state/`
- robust logging and retry strategy
