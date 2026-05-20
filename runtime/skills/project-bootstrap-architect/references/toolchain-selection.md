---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/toolchain-selection.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/toolchain-selection.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/toolchain-selection.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Toolchain Selection

Use this file after choosing the project archetype.
The goal is to make stack selection repeatable instead of arbitrary.

## Global defaults

- Prefer TypeScript for new JavaScript ecosystem projects unless the user explicitly wants plain JavaScript.
- Prefer `pnpm` for monorepos or multi-package workspaces.
- Prefer `npm` for a single small package when there is no workspace need.
- Prefer one test stack per repo. Do not mix multiple test runners without a reason.
- Add linting and formatting on day one for any project expected to live beyond a prototype.

## Language routing

Use the ecosystem-native baseline when the user explicitly chooses a language.

### Python

- package manager: `uv` by default, `pip` only if compatibility is the real priority
- project template: `src/` layout with `pyproject.toml`
- tests: `pytest`
- lint/format: `ruff`
- config baseline: `.python-version` when version pinning matters, `.env.example`, `pyproject.toml`

### Go

- package manager: built-in modules
- project template: `cmd/` for entrypoints, `internal/` for private packages, `pkg/` only when truly reusable
- tests: `go test`
- lint/format: `gofmt` and `golangci-lint` when the project is expected to grow
- config baseline: `go.mod`, `.env.example` if runtime config exists

### Rust

- package manager: Cargo
- project template: `src/main.rs` for binaries or `src/lib.rs` for libraries, add `crates/` only when a workspace is justified
- tests: built-in Cargo tests
- lint/format: `cargo fmt` and `clippy`
- config baseline: `Cargo.toml`, `.env.example` if runtime config exists

## CLI tool

- package manager: `npm` for one package, `pnpm` for workspace-based plugins
- runtime template: Node.js CLI with `commander` or minimal argument parsing
- tests: `vitest`
- lint/format: `eslint` + `prettier`
- config baseline: `.env.example`, `tsconfig.json`, `eslint.config.*`, `prettier.config.*`

## Web app

- package manager: `pnpm` if there is any chance of `apps/` plus `packages/`, otherwise `npm`
- framework template: `Next.js` for integrated full-stack React, `Vite + React` for front-end only apps
- tests: `vitest` for unit tests, `playwright` if browser E2E is needed
- lint/format: framework default linting plus `prettier`
- config baseline: `.env.example`, app config, browser test config, i18n-ready locale folders

## Browser extension

- package manager: `npm` for one extension, `pnpm` if shared packages or tooling are expected
- framework template: `Vite`-based extension scaffold for popup/options UI, plain TS modules for background/content if minimal UI
- tests: `vitest`
- lint/format: `eslint` + `prettier`
- config baseline: `manifest.json`, extension build config, locale folders if user-facing copy exists

## Service API

- package manager: `npm` for one service, `pnpm` for multi-service or shared package repos
- framework template: `Fastify` for lean typed APIs, `Express` only when ecosystem compatibility is the real priority
- tests: `vitest` or framework-native test stack
- lint/format: `eslint` + `prettier`
- config baseline: `.env.example`, migration config, app/server entrypoint, health route

## Desktop helper

- package manager: `npm` for one local agent or daemon, `pnpm` if UI plus agent or multiple packages are planned
- runtime template: Node.js local service by default; add Electron or Tauri only if the user explicitly needs a desktop UI shell
- tests: `vitest`
- lint/format: `eslint` + `prettier`
- config baseline: `.env.example`, local data dir strategy, logs dir strategy, prompt/config folder when model workflows exist

## Shared library or SDK

- package manager: `npm` unless the repo is part of a workspace
- runtime template: plain TypeScript library with explicit public exports
- tests: `vitest`
- lint/format: `eslint` + `prettier`
- config baseline: `package.json`, `tsconfig.json`, build config, `README.md`, examples

## Automation or worker service

- package manager: `npm` for one worker, `pnpm` for queue plus shared packages
- runtime template: Node.js worker service with isolated adapters and job modules
- tests: `vitest`
- lint/format: `eslint` + `prettier`
- config baseline: `.env.example`, scheduler or queue config, retry policy location, structured logging setup

## Escalation rules

- Choose monorepo only when there are clearly multiple deployable units or shared packages from day one.
- Choose SQLite over hosted databases for single-machine or local-first tools unless multi-user server state is explicit.
- Choose locale folders on day one for any product that shows end-user copy and is expected to support both English and Traditional Chinese.
