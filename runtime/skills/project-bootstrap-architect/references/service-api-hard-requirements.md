---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/service-api-hard-requirements.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/service-api-hard-requirements.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/service-api-hard-requirements.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Service API Hard Requirements

Use this file for backend API, webhook service, auth service, or JSON server bootstrap work.

These are not style preferences. They affect whether the service can start, expose a stable contract, and be deployed without hidden handwork.

## Clear runtime entrypoint

- The scaffold must define one obvious application entrypoint.
- Another developer should be able to tell where the server starts without hunting through the repo.
- Prefer a clear path such as `src/index.*`, `src/main.*`, or `src/server/index.*`.

## Separate HTTP boundary from business logic

- Do not collapse route declarations, request parsing, domain logic, and persistence into one giant file.
- Keep at least these boundaries explicit in the scaffold:
  - app or server bootstrap
  - routes or controllers
  - services or use cases
  - storage or DB access

If these boundaries are missing at bootstrap time, the service will drift into framework-shaped spaghetti too quickly.

## Health and environment baseline

At bootstrap time, plan for:

- one health or readiness route
- one environment example file
- one explicit configuration loading path

If the service cannot be started and sanity-checked quickly, the scaffold is incomplete.

## Config is part of the architecture

- Runtime configuration must not be scattered through random modules.
- There should be one clear configuration boundary, usually under `src/config/`, `src/lib/config.*`, or equivalent.
- Secrets should never be hard-coded into source files.

## Persistence boundary must be explicit

If the service uses durable data:

- the scaffold must show where DB access lives
- the scaffold must show where schema or migrations live
- the scaffold must not mix direct SQL or ORM calls through route handlers

Even if migrations are not fully implemented yet, the location and ownership need to be visible from day one.

## Request contract should be testable

- The scaffold should make request and response contracts easy to test.
- Do not hide all behavior in framework magic with no obvious seam for unit or integration tests.
- Prefer one test path from the beginning, even if only smoke-level at first.

## Build and deploy output must be predictable

- Another developer should know what command starts the service locally.
- Another developer should know what artifact or process is deployed.
- Avoid scaffolds that require manual file moves, shell history knowledge, or undocumented env setup to boot.

## Required first-wave files or surfaces

For most API services, the bootstrap output should account for:

- app entrypoint
- route registration
- config loader
- environment example
- health route
- test command

If any of these are absent from the plan, the service scaffold is probably underspecified.

## API-specific anti-patterns

- one huge `server.ts` containing everything
- routes directly performing persistence and business rules
- no health endpoint
- no environment example
- no visible storage layer for stateful services
- hidden startup logic in scripts without a clear source entrypoint

## Default advice

For a new service API, prefer a scaffold that another developer can recognize immediately as:

- having one clear entrypoint
- having one clear config boundary
- having one clear route layer
- having one clear service layer
- having one clear persistence boundary when data exists
- being startable and smoke-testable on day one
