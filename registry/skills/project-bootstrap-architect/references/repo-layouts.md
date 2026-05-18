# Repo Layouts

Choose the smallest scaffold that still matches the archetype.

## CLI tool

Default:

- `package.json`
- `tsconfig.json`
- `src/index.ts`
- `src/commands/`
- `src/lib/`
- `test/`
- `.env.example`
- `README.md`

Use a single package unless the CLI clearly ships shared packages or plugins.

## Web app

Default single-app layout:

- `src/app/`
- `src/components/`
- `src/features/`
- `src/lib/`
- `src/styles/`
- `public/`
- `locales/en/`
- `locales/zh-TW/`
- `.env.example`

Default monorepo layout when backend or shared packages are first-class:

- `apps/web/`
- `apps/api/`
- `packages/ui/`
- `packages/config/`
- `packages/i18n/`

## Browser extension

Default:

- `src/background/`
- `src/content/`
- `src/popup/`
- `src/options/`
- `src/shared/`
- `assets/`
- `manifest.json`
- `locales/en/`
- `locales/zh-TW/`

## Service API

Default:

- `src/index.ts`
- `src/server/`
- `src/routes/`
- `src/services/`
- `src/db/`
- `src/lib/`
- `test/`
- `migrations/`
- `.env.example`

## Desktop helper

Default:

- `src/index.ts`
- `src/agent/`
- `src/tools/`
- `src/integrations/`
- `src/state/`
- `src/prompts/`
- `data/`
- `.env.example`
- `README.md`

If the project has user-facing UI, add:

- `locales/en/`
- `locales/zh-TW/`

## Shared library or SDK

Default:

- `src/index.ts`
- `src/core/`
- `src/types/`
- `test/`
- `examples/`
- `README.md`

## Automation or worker service

Default:

- `src/index.ts`
- `src/jobs/`
- `src/workers/`
- `src/adapters/`
- `src/lib/`
- `src/state/`
- `test/`
- `.env.example`

## i18n rule

If the project contains user-facing copy, bootstrap locale structure on day one:

- `locales/en/` as source of truth
- `locales/zh-TW/` as first target

Do not scatter UI strings directly through feature code if the app is expected to be bilingual.
